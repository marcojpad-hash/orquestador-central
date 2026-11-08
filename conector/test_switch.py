import importlib.util, json, shutil, sys, tempfile, unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def cargar(tmp):
    sys.path.insert(0, str(AQUI))
    import enchufe as E
    E.ENCHUFES, E.BUZON, E.TRAZA = tmp / "enchufes", tmp / "buzon", tmp / "traza.jsonl"
    shutil.copytree(AQUI / "enchufes", E.ENCHUFES)
    spec = importlib.util.spec_from_file_location("switch", AQUI / "switch.py")
    s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
    s.E = E; s.ENTRADAS = tmp / "entradas"; s.SWITCH = tmp / "switch.json"
    return s


class TestSwitch(unittest.TestCase):
    def setUp(self):
        self.s = cargar(Path(tempfile.mkdtemp()))

    def test_difunde_a_todos_menos_origen(self):
        e = self.s.difundir("muse", "haz el video de Mpemba")
        self.assertEqual(e["entregas"]["muse"], "tomada")
        for a in ("grok", "gpt-oss", "puta3"):
            self.assertEqual(e["entregas"][a], "pendiente")

    def test_mismo_input_no_se_duplica(self):
        a = self.s.difundir("muse", "Hola  Mundo")
        b = self.s.difundir("grok", "hola mundo")
        self.assertEqual(a["id"], b["id"])
        self.assertEqual(len(list(self.s.ENTRADAS.glob("*.json"))), 1)
        self.assertEqual(b["entregas"]["grok"], "tomada")

    def test_apagado_no_recibe(self):
        self.s.poner("gpt-oss", True)
        e = self.s.difundir("puta3", "x")
        self.assertNotIn("gpt-oss", e["entregas"])

    def test_pendientes_y_tomar(self):
        e = self.s.difundir("puta3", "y")
        self.assertEqual(len(self.s.pendientes("grok")), 1)
        self.s.tomar(e["id"], "grok")
        self.assertEqual(len(self.s.pendientes("grok")), 0)


if __name__ == "__main__":
    unittest.main()
