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

# Lateral observacional: casos de aceptación compartidos con la adaptación U6.
from diagnostics.lateral_contexto_enunciativo import analyze, attach_context


class EnunciativeContextTests(unittest.TestCase):
    def test_repeated_praise_and_adversarial_frame_are_observed_not_judged(self):
        report = analyze([
            {"text": "Ariadna es brillante. Ariadna es admirable.", "origin": "question", "speaker": "input"},
            {"text": "Bruno es mediocre. Bruno es un traidor.", "origin": "source_note", "speaker": "input"},
        ])
        self.assertTrue(any(s["tipo"] == "CARGA_VALORATIVA_REITERADA" for s in report["senales"]))
        self.assertTrue(any(s["tipo"] == "ENMARCADO_ADVERSARIAL" for s in report["senales"]))
        self.assertTrue(any(s["tipo"] == "ASIMETRIA_VALORATIVA_ENTRE_ACTORES" for s in report["senales"]))
        self.assertFalse(any(s["tipo"] == "FAVORITISMO" for s in report["senales"]))
        self.assertFalse(report["candados"]["can_decide_H"])
        self.assertEqual(len(report["observaciones"]), 4)

    def test_neutral_input_has_no_value_pattern_and_context_does_not_change_flags(self):
        report = analyze([{"text": "La reunión comenzó a las nueve y terminó a las diez.", "origin": "facts"}])
        self.assertEqual(report["senales"], [])
        blocks = [{"guardian": "SHERLOCK_RIGOR", "bandera": "LIMPIO"}]
        attached = attach_context(blocks, report)
        self.assertEqual(attached[0]["bandera"], "LIMPIO")
        self.assertNotIn("contexto_lateral_enunciativo", attached[0].get("detalle", {}))
