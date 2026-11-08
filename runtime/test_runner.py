import json, unittest
from pathlib import Path
from sequential_runner import validate, check, SCHEMA_URI
ROOT=Path(__file__).resolve().parents[1]
class ContractTests(unittest.TestCase):
 def setUp(self): self.x=json.loads((ROOT/"examples/sequential-verifiable-v1.example.json").read_text())
 def test_example_schema_validates(self): validate(self.x)
 def test_missing_marker_rejected(self):
  self.x.pop("$schema")
  with self.assertRaises(ValueError): validate(self.x)
 def test_wrong_archetype_rejected(self):
  self.x["_contract"]="OTHER"
  with self.assertRaises(ValueError): validate(self.x)
 def test_empty_steps_rejected(self):
  self.x["steps"]=[]
  with self.assertRaises(ValueError): validate(self.x)
 def test_pre_post_contract_fields_required(self):
  self.x["steps"][0].pop("postconditions")
  with self.assertRaises(ValueError): validate(self.x)
if __name__=="__main__": unittest.main()
