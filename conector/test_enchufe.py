import importlib.util, json, shutil, tempfile, unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def cargar(tmp):
    spec = importlib.util.spec_from_file_location("enchufe", AQUI / "enchufe.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.ENCHUFES, m.BUZON, m.TRAZA = tmp / "enchufes", tmp / "buzon", tmp / "traza.jsonl"
    shutil.copytree(AQUI / "enchufes", m.ENCHUFES); m.BUZON.mkdir()
    return m


class TestConector(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()); self.m = cargar(self.tmp)

    def test_macho_hembra_y_vuelta(self):
        o = self.m.pedir("muse", "leer:pdf", "Lee docs/a.pdf")
        self.assertEqual(o["para"], "puta3")          # Muse no lee PDF; lo recibe quien sí
        self.m.acusar(o["id"], "puta3", "hecho", "ok")
        d = json.loads((self.m.BUZON / "puta3" / f"{o['id']}.json").read_text())
        self.assertEqual(d["estado"], "hecho")

    def test_nunca_a_si_mismo_y_sin_match_sube_a_mj(self):
        o = self.m.pedir("puta3", "leer:pdf", "x")
        self.assertNotEqual(o["para"], "puta3")
        self.assertEqual(o["para"], "mj")

    def test_fallo_pasa_al_alterno(self):
        o = self.m.pedir("gpt-oss", "escribir:github_pr", "abre PR")
        primero = o["para"]; self.assertTrue(o["alternos"])
        self.m.acusar(o["id"], primero, "fallo", "sin permiso")
        self.assertTrue(any((self.m.BUZON / a / f"{o['id']}.json").exists() for a in o["alternos"]))

    def test_dedupe(self):
        a = self.m.pedir("grok", "leer:notion", "lee pagina")
        b = self.m.pedir("grok", "leer:notion", "lee pagina")
        self.assertEqual(a["id"], b["id"])

    def test_enchufe_contradictorio_se_rechaza(self):
        with self.assertRaises(ValueError):
            self.m.validar_enchufe({"agente": "x", "version": "1", "puede": ["a"], "no_puede": ["a"], "transporte": [], "verificado": {}})


if __name__ == "__main__":
    unittest.main()
