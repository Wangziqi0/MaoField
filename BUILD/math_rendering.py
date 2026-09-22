"""Repair native Office Math property order for interoperable equation rendering.

The source mathematics is unchanged. m:dPr children are serialised in schema order
begChr, sepChr, endChr, grow, shp, ctrlPr. The previous converter wrote endChr before
sepChr; our rendering reproduction displayed default right parentheses. Reordering
preserves auto-sized, editable delimiters, unlike raster equation screenshots.
"""
from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import json
NS={'m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
ORDER=['begChr','sepChr','endChr','grow','shp','ctrlPr']
def repair(doc):
    records=[]
    for dp in doc.element.findall('.//m:dPr',NS):
        children=list(dp);before=[c.tag.split('}')[-1] for c in children]
        after=sorted(children,key=lambda c:ORDER.index(c.tag.split('}')[-1]) if c.tag.split('}')[-1] in ORDER else len(ORDER))
        for c in children:dp.remove(c)
        for c in after:dp.append(c)
        records.append({'before':before,'after':[c.tag.split('}')[-1] for c in after],
                        'values':{c.tag.split('}')[-1]:c.get(qn('m:val')) for c in after}})
    for mr in doc.element.findall('.//m:r',NS):
        tt=mr.find('m:t',NS)
        if tt is None:continue
        in_sub=any(a.tag==qn('m:sub') for a in mr.iterancestors())
        if (in_sub and tt.text in ('+','−','-','*','∗')) or tt.text in ('max','min'):
            rp=mr.find('m:rPr',NS)
            if rp is None:rp=OxmlElement('m:rPr');mr.insert(0,rp)
            if rp.find('m:nor',NS) is None:rp.append(OxmlElement('m:nor'))
    return {'native_equation_count':len(doc.element.findall('.//m:oMath',NS)),
            'delimiter_containers_checked':len(records),
            'delimiter_orders_changed':sum(x['before']!=x['after'] for x in records),
            'delimiter_properties':records,'method':'schema-order repair; native editable Office Math retained'}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);p.add_argument('--log',type=Path)
    a=p.parse_args();doc=Document(a.source);r=repair(doc);doc.save(a.output)
    if a.log:a.log.write_text(json.dumps(r,ensure_ascii=False,indent=2))
    print(json.dumps(r,ensure_ascii=False,indent=2))
