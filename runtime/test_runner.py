import json, subprocess, sys, tempfile, unittest
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

    def test_cli_adapter_writes_observational_report(self):
        import json
        import subprocess
        import sys
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "input.json"
            target = root / "out" / "report.json"
            source.write_text(json.dumps({"records": [
                {"text": "Ariadna es brillante. Ariadna es admirable.", "speaker": "input"},
                {"text": "Bruno es mediocre. Bruno es un traidor.", "speaker": "input"}
            ]}), encoding="utf-8")
            script = Path(__file__).resolve().parent / "diagnostics" / "run_contexto_enunciativo.py"
            proc = subprocess.run([sys.executable, str(script), "--input", str(source), "--output", str(target)],
                                  capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads(target.read_text(encoding="utf-8"))
            self.assertTrue(any(s["tipo"] == "ASIMETRIA_VALORATIVA_ENTRE_ACTORES" for s in result["senales"]))
            self.assertFalse(result["candados"]["can_decide_H"])

# Ruta condicional del lateral: la puerta se abre solo cuando el input trae
# contenido enunciativo; con input neutro la ruta pasa en silencio (SIN_ACTIVACION).
class ContextoEnunciativoRutaTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent / "diagnostics"))
        from lateral_contexto_enunciativo import debe_observar  # noqa: E402
        self.debe_observar = debe_observar
        self.adapter = Path(__file__).resolve().parent / "diagnostics" / "ruta_contexto_enunciativo.py"

    def test_puerta_activa_con_juicios(self):
        activa, motivo = self.debe_observar("Ese funcionario es un corrupto deshonesto; su gestión fue terrible y destruirá la institución.")
        self.assertTrue(activa)
        self.assertIn("juicio", motivo)

    def test_puerta_activa_con_funcion_apelativa(self):
        activa, _ = self.debe_observar("Debes revisar esto ahora y dime qué opinas.")
        self.assertTrue(activa)

    def test_puerta_silencio_con_input_neutro(self):
        activa, motivo = self.debe_observar("El agua hierve a 100 grados Celsius a nivel del mar. La fotosíntesis ocurre en los cloroplastos.")
        self.assertFalse(activa)
        self.assertIn("neutro", motivo)

    def _run_adapter(self, text):
        tmp = Path(tempfile.mkdtemp())
        inp = tmp / "input.txt"; inp.write_text(text, encoding="utf-8")
        out = tmp / "reporte.json"
        r = subprocess.run([sys.executable, str(self.adapter), "--input", str(inp), "--out", str(out)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(out.read_text(encoding="utf-8"))

    def test_ruta_escribe_reporte_completo_cuando_activa(self):
        rep = self._run_adapter("Ese funcionario es un corrupto deshonesto; su gestión fue terrible.")
        self.assertEqual(rep["estado"], "ACTIVA")
        self.assertTrue(rep["observaciones"])
        self.assertIs(rep["candados"]["can_decide_H"], False)

    def test_ruta_pasa_en_silencio_cuando_neutro(self):
        rep = self._run_adapter("El volcán Paricutín nació en 1943 en Michoacán.")
        self.assertEqual(rep["estado"], "SIN_ACTIVACION")
        self.assertEqual(rep["observaciones"], [])

    def test_ruta_no_decide_ni_veta(self):
        rep = self._run_adapter("Ese funcionario es un corrupto deshonesto; su gestión fue terrible.")
        self.assertTrue(all(v is False for v in rep["candados"].values()))
        self.assertNotIn("veredicto", rep)
        self.assertNotIn("decision", rep)

if __name__ == "__main__":
    unittest.main()
