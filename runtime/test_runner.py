import json, unittest
from pathlib import Path
from sequential_runner import validate
ROOT=Path(__file__).resolve().parents[1]
class RunnerContractTests(unittest.TestCase):
    def test_example_contract_passes(self):
        x=json.loads((ROOT/"examples/sequential-verifiable-v1.example.json").read_text())
        validate(x)
    def test_unmarked_contract_fails(self):
        x=json.loads((ROOT/"examples/sequential-verifiable-v1.example.json").read_text())
        x.pop("$schema")
        with self.assertRaises(ValueError): validate(x)
    def test_empty_steps_fail(self):
        x=json.loads((ROOT/"examples/sequential-verifiable-v1.example.json").read_text())
        x["steps"]=[]
        with self.assertRaises(ValueError): validate(x)
if __name__=="__main__": unittest.main()
