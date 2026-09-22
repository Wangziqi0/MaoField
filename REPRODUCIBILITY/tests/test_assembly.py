"""Deterministic packaging/source tests, not scientific replication counts."""
import unittest,tempfile,sys,json,hashlib,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'REPRODUCIBILITY/experiment'))
import assemble_lean
import replay_lean
from unittest.mock import patch
class AssemblyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.raw=assemble_lean.default_raw();cls.tmp=tempfile.TemporaryDirectory();cls.out=Path(cls.tmp.name)/'project';cls.rec=assemble_lean.assemble(cls.raw,cls.out)
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def test_root_execute_identity_refused(self):
  with patch.object(replay_lean.os,'getuid',return_value=0):
   with self.assertRaises(ValueError):replay_lean.nonroot_user()
 def test_nonroot_identity_explicit(self):
  with patch.object(replay_lean.os,'getuid',return_value=1000),patch.object(replay_lean.os,'getgid',return_value=1001):self.assertEqual(replay_lean.nonroot_user(),'1000:1001')
 def test_five_candidates(self):self.assertEqual(self.rec['candidate_count'],5)
 def test_standard_mapping(self):
  rows=json.loads((self.out/'candidate_manifest.json').read_text());self.assertEqual([(r['visible_candidate_ordinal'],r['original_request_number']) for r in rows if r['condition_original_label']=='STANDARD'],[(1,2),(2,3)])
 def test_truncated_request_has_no_candidate(self):
  rows=json.loads((self.out/'request_to_candidate.json').read_text());row=next(r for r in rows if r['condition_original_label']=='STANDARD' and r['original_request_number']==1);self.assertIsNone(row['candidate_name']);self.assertEqual(row['no_candidate_reason'],'TRUNCATED_NO_VISIBLE_BODY_NOT_COMPILED')
 def test_unchanged_candidates(self):
  for row in json.loads((self.out/'candidate_manifest.json').read_text()):self.assertEqual((self.out/'saved_candidates'/row['candidate_name']).read_bytes(),(self.raw/row['source']).read_bytes())
 def test_no_terminal_in_common_source(self):self.assertFalse((self.out/'Branch/Direct.lean').exists())
 def test_node_goal_origin(self):
  self.assertEqual(assemble_lean.sha(self.out/'Checkpoint/NodeGoal.lean'),'571a45c575a39523475c96b3789d331ba2c07a0c80e8fb477790a5d6e1b299d7')
 def test_dependency_lock_exact(self):self.assertEqual((self.out/'lake-manifest.json').read_bytes(),(self.raw/'10_CURRENT_RUN/history/workspace/lake-manifest.json').read_bytes())
 def test_no_local_import_missing(self):self.assertEqual(self.rec['unresolved_local_imports'],[])
 def test_no_compilation_in_assembly(self):self.assertEqual(self.rec['new_Lean_compilations'],0)
 def test_no_output_overwrite(self):
  with self.assertRaises(FileExistsError):assemble_lean.assemble(self.raw,self.out)
 def test_tamper_detected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'a.txt').write_text('wrong');(p/'PACKAGE_MANIFEST.json').write_text(json.dumps({'files':[{'path':'a.txt','bytes':1,'sha256':'0'*64}]}))
   with self.assertRaises(ValueError):assemble_lean.verify_raw(p)
 def test_independent_assembly_same_mathematical_files(self):
  with tempfile.TemporaryDirectory() as d:
   other=Path(d)/'project';r=assemble_lean.assemble(R/'REPRODUCIBILITY/experiment/raw',other)
   for row in r['files']:
    if row['assembled_path'].endswith('.lean'):self.assertEqual((other/row['assembled_path']).read_bytes(),(self.out/row['assembled_path']).read_bytes())
 def test_all_review_json_valid(self):
  for p in (R/'REPRODUCIBILITY/experiment/raw').rglob('*.json'):json.loads(p.read_text())
 def test_no_hidden_reasoning_in_review_streams(self):
  for p in (R/'REPRODUCIBILITY/experiment/raw').rglob('wire.bin'):
   self.assertNotIn('"reasoning_content":',p.read_text());self.assertNotIn('"reasoning":',p.read_text())
if __name__=='__main__':unittest.main()
