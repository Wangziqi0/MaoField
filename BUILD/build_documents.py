"""Build editable manuscript and supporting DOCX files from maintained Markdown."""
from pathlib import Path
import json
from typeset_documents import generate
R=Path(__file__).resolve().parents[1]
JOBS=[('SUBMISSION/manuscript','main'),('SUBMISSION/supplementary_information','si'),
('SUBMISSION/cover_letter','support'),('SUBMISSION/title_page','support'),
('SUBMISSION/declarations','support'),('SUBMISSION/software_checklist','support'),
('SUBMISSION/reporting_summary_responses','support'),('SUBMISSION/SIGuide','support'),
('EDITORIAL/ONE_PAGE_SYNOPSIS_ZH','zh')]
if __name__=='__main__':
 result=[]
 for stem,kind in JOBS:
  src=R/(stem+'.md');out=R/(stem+'.docx')
  result.append(generate(src,out,kind))
 (R/'QA/DOCUMENT_BUILD.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))
