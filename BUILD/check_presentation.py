from pathlib import Path
import re,json,csv,zipfile,hashlib,math,sys
import fitz
from lxml import etree as E
from PIL import Image
import argparse,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=p.parse_args();R=args.root.resolve()
subprocess.run([sys.executable,str(R/'BUILD/count_words.py'),'--root',str(R)],check=True,capture_output=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
NS={'m':'http://schemas.openxmlformats.org/officeDocument/2006/math','w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
counts=json.loads((R/'QA/WORD_COUNTS.json').read_text()); checks={}
checks['title_length']=counts['title_characters']<=75
checks['summary_length']=counts['abstract_words']<=200
checks['extended_article_text_guideline']=counts['summary_and_main_words_excluding_headings_math']<=4300
checks['methods_guideline']=counts['methods_words_excluding_headings_and_availability']<=3000
checks['legends']=all(v<250 for v in counts['legends'].values())
checks['main_subheadings']=all(v<=40 for v in counts['main_subheadings'].values())
media={sha(p):p.name for p in (R/'FIGURES').glob('*.png')}
docx=[]
for p in list((R/'SUBMISSION').glob('*.docx'))+list((R/'EDITORIAL').glob('ONE_PAGE_SYNOPSIS_ZH.docx')):
 with zipfile.ZipFile(p) as z:
  xml=E.fromstring(z.read('word/document.xml'))
  ms=xml.findall('.//m:oMath',NS)
  if p.stem in ('manuscript','supplementary_information'):assert ms
  expected={'begChr':0,'sepChr':1,'endChr':2,'grow':3,'shp':4,'ctrlPr':5}
  dps=xml.findall('.//m:dPr',NS)
  for d in dps:
   order=[expected.get(E.QName(c).localname,99) for c in d];assert order==sorted(order)
  matched=[]
  if p.stem=='manuscript':
   for n in z.namelist():
    if n.startswith('word/media/'):
     h=hashlib.sha256(z.read(n)).hexdigest();assert h in media,(n,'EMBED_MISMATCH');matched.append(media[h])
   assert len(matched)==5
   assert xml.find('.//w:lnNumType',NS) is not None
   for d in xml.findall('.//wp:extent',NS):assert abs(int(d.get('cx'))/36000-180)<.01
  docx.append({'file':str(p.relative_to(R)),'native_Office_Math':len(ms),'delimiters_schema_order':True,'embedded_figures':matched})
checks['docx_native_math_and_media']=True
pdf=[]
for p in list((R/'SUBMISSION').glob('*.pdf'))+list((R/'EDITORIAL').glob('ONE_PAGE_SYNOPSIS_ZH.pdf')):
 d=fitz.open(p); text='\n'.join(x.get_text() for x in d)
 assert '\ufffd' not in text,(p,'replacement character')
 assert p.stat().st_size<30_000_000
 pdf.append({'file':str(p.relative_to(R)),'pages':len(d),'bytes':p.stat().st_size,'replacement_characters':0,'sha256':sha(p)})
figures=[]
for p in sorted((R/'FIGURES').glob('*.pdf')):
 d=fitz.open(p);w=d[0].rect.width*25.4/72;h=d[0].rect.height*25.4/72
 assert abs(w-180)<.05 and h<=170
 fonts=d.get_page_fonts(0,full=True);assert not any(f[2]=='Type3' for f in fonts)
 svg=p.with_suffix('.svg');tx=svg.read_text();assert '<text' in tx and '<image' not in tx
 with Image.open(p.with_suffix('.png')) as im:
  dpi=im.info.get('dpi'); assert dpi and abs(dpi[0]-600)<.1
 figures.append({'file':p.name,'width_mm':w,'height_mm':h,'fonts':[(f[2],f[3]) for f in fonts],'editable_SVG_text':True,'no_raster_in_SVG':True,'PNG_dpi':dpi,'PDF_sha256':sha(p)})
checks['figures_vector_and_size']=True
with (R/'SOURCE_DATA/figure2_analytic_curve.csv').open() as stream:rows=list(csv.DictReader(stream))
maxerr=0
for x in rows:
 g,r,v=map(float,[x['g'],x['r'],x['v']]);a=abs(g*g+2*(1+v)*g-r);b=abs(g*g+2*(1-v)*g-r)
 maxerr=max(maxerr,abs(a-float(x['abs_E_plus'])),abs(b-float(x['abs_E_minus'])),abs(max(a,b)-float(x['worst_case'])))
assert maxerr<1e-14
checks['analytic_table_recomputed']=True
record=json.loads((R/'QA/LOCAL_REPRODUCTION/records/attempts.json').read_text());source=json.loads((R/'SOURCE_DATA/attempts.json').read_text())
assert record==source
assert len(record)==6 and sum(isinstance(x['compiler_returncode'],int) for x in record)==5
checks['all_six_requests_five_candidates_reproduced']=True
j=json.loads((R/'SUBMISSION/system_fields.json').read_text());m=(R/'SUBMISSION/manuscript.md').read_text()
a=re.search(r'^\*\*(As AI[^\n]+)\*\*$',m,re.M).group(1)
a=re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]+(?:[–,][⁰¹²³⁴⁵⁶⁷⁸⁹]+)*','',a)
assert a==j['abstract'] and a in (R/'SUBMISSION/system_fields.md').read_text()
checks['metadata_abstract_matches']=True
report={'checks':checks,'docx':docx,'pdf':pdf,'figures':figures,'analytic_table_rows':len(rows),'maximum_numeric_roundoff':maxerr,'word_counts':counts,'new_model_calls':0,'new_Lean_runs':0,'visual_review_is_separate':True}
(R/'QA/PRESENTATION_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
assert all(checks.values());print(json.dumps({'checks':len(checks),'all_passed':True,'pdf_pages':sum(i['pages'] for i in pdf if 'integrated' not in i['file'])},indent=2))
