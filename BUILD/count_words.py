from pathlib import Path
import re,json
import argparse
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=p.parse_args();R=args.root.resolve()
s=(R/'SUBMISSION/manuscript.md').read_text()
def clean(t):
 t=re.sub(r'\$\$.*?\$\$',' ',t,flags=re.S)
 t=re.sub(r'\$[^$]+\$',' ',t)
 t=re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]+(?:[–,][⁰¹²³⁴⁵⁶⁷⁸⁹]+)*','',t)
 t=re.sub(r'[`*_#]','',t)
 return t
# Count visible prose words, excluding LaTeX displays and inline notation.
def wc(t):return len(re.findall(r"[A-Za-z0-9]+(?:[’'\-–][A-Za-z0-9]+)*",clean(t)))
a=re.search(r'^\*\*(AI [^\n]+)\*\*$',s,re.M).group(1)
a= re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]+(?:[–,][⁰¹²³⁴⁵⁶⁷⁸⁹]+)*','',a)
body=s.split('## Introduction\n',1)[1].split('## References',1)[0]
methods=s.split('## Methods\n',1)[1].split('### Data availability',1)[0]
cl=(R/'SUBMISSION/cover_letter.md').read_text()
clbody=cl.split('Dear Editors,',1)[1].split('Yours sincerely',1)[0]
legends=re.findall(r'^\*\*((?:Fig\. [1-4]|Extended Data (?:Fig\.|Table) 1) \|.+)$',s,re.M)
record={'date':'2026-09-23','count_rule':'ASCII alphanumeric word tokens with internal apostrophe/hyphen/en dash; displays and inline LaTeX excluded; superscript citations excluded; section headings excluded from body by separate heading removal where stated.',
 'indexed_title':'Why can equal results lead to different scientific futures',
 'title_characters':len('Why can equal results lead to different scientific futures'),
 'abstract_words':wc(a),'main_body_words_excluding_headings_math':wc(re.sub(r'^#+.*$','',body,flags=re.M)),
 'summary_and_main_words_excluding_headings_math':wc(a)+wc(re.sub(r'^#+.*$','',body,flags=re.M)),
 'methods_words_excluding_headings_and_availability':wc(re.sub(r'^#+.*$','',methods,flags=re.M)),
 'cover_letter_body_words':wc(clbody),'cover_letter_all_text_words':wc(cl),
 'legends':{re.match(r'[^|]+',t).group(0).strip():wc(t) for t in legends},
 'main_figures':4,'extended_figures':1,'extended_tables':1,'main_references':20,
 'main_subheadings':{x:len(x) for x in re.findall(r'^## (.+)$',s,re.M) if x not in ['References','Figure legends','Methods','Author information and declarations','Extended Data']},
 'submission_sent':False}
(R/'QA/WORD_COUNTS.json').write_text(json.dumps(record,indent=2,ensure_ascii=False))
print(json.dumps(record,indent=2))
