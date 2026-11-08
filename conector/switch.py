#!/usr/bin/env python3
"""Switch dinámico de entradas entre modelos.

Cuando cualquier modelo recibe un input de Mj, lo DIFUNDE: el switch deja
la misma entrada para todos los demás enchufes que estén encendidos. Es
dinámico: no hay lista fija; entra cualquiera que tenga enchufe en
conector/enchufes/ y no esté apagado en conector/switch.json.

- Si dos modelos reciben el mismo input, solo se difunde una vez (huella).
- Cada modelo ve sus entradas pendientes y las marca como tomadas.
- Solo librería estándar, sin red.

Uso:
  python3 conector/switch.py difundir --de muse --texto "lo que dijo Mj"
  python3 conector/switch.py pendientes grok
  python3 conector/switch.py tomar <id> --por grok
  python3 conector/switch.py apagar gpt-oss   |   encender gpt-oss
  python3 conector/switch.py estado
"""
import argparse, hashlib, json
from pathlib import Path

try:
    from . import enchufe as E
except ImportError:
    import enchufe as E

RAIZ = Path(__file__).resolve().parent
ENTRADAS = RAIZ / "entradas"
SWITCH = RAIZ / "switch.json"


def leer_switch():
    return json.loads(SWITCH.read_text(encoding="utf-8")) if SWITCH.exists() else {"apagados": []}


def guardar_switch(s):
    SWITCH.write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def encendidos():
    apag = set(leer_switch()["apagados"])
    return [a for a in E.cargar_enchufes() if a not in apag]


def huella(texto):
    normal = " ".join(texto.split()).lower()
    return hashlib.sha256(normal.encode()).hexdigest()[:12]


def difundir(de, texto, canal="chat"):
    hid = huella(texto)
    p = ENTRADAS / f"{hid}.json"
    if p.exists():  # otro modelo ya lo difundió: solo se suma como receptor
        e = json.loads(p.read_text(encoding="utf-8"))
        e["entregas"].setdefault(de, "tomada")
        e["entregas"][de] = "tomada"
        p.write_text(json.dumps(e, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        E.traza("switch_duplicado", id=hid, de=de)
        print(f"entrada {hid} ya estaba difundida; {de} marcado como receptor")
        return e
    destinos = [a for a in encendidos() if a != de]
    e = {"id": hid, "origen": de, "canal": canal, "texto": texto,
         "recibida": E.ahora(),
         "entregas": {de: "tomada", **{a: "pendiente" for a in destinos}}}
    ENTRADAS.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(e, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    E.traza("switch_difundir", id=hid, de=de, a=destinos)
    print(f"entrada {hid}: {de} -> {', '.join(destinos) or 'nadie'}")
    return e


def pendientes(agente):
    out = []
    for p in sorted(ENTRADAS.glob("*.json")):
        e = json.loads(p.read_text(encoding="utf-8"))
        if e["entregas"].get(agente) == "pendiente":
            out.append(e)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return out


def tomar(eid, por):
    p = ENTRADAS / f"{eid}.json"
    if not p.exists():
        raise SystemExit(f"no existe la entrada {eid}")
    e = json.loads(p.read_text(encoding="utf-8"))
    e["entregas"][por] = "tomada"
    p.write_text(json.dumps(e, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    E.traza("switch_tomar", id=eid, por=por)
    print(f"entrada {eid} tomada por {por}")


def poner(agente, apagado):
    s = leer_switch(); ap = set(s["apagados"])
    ap.add(agente) if apagado else ap.discard(agente)
    s["apagados"] = sorted(ap); guardar_switch(s)
    E.traza("switch_apagar" if apagado else "switch_encender", agente=agente)
    print(f"{agente}: {'apagado' if apagado else 'encendido'}")


def estado():
    apag = set(leer_switch()["apagados"])
    for a in E.cargar_enchufes():
        print(f"{a.ljust(10)} {'apagado' if a in apag else 'encendido'}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("difundir"); d.add_argument("--de", required=True); d.add_argument("--texto", required=True); d.add_argument("--canal", default="chat")
    p = sub.add_parser("pendientes"); p.add_argument("agente")
    t = sub.add_parser("tomar"); t.add_argument("id"); t.add_argument("--por", required=True)
    for n in ("apagar", "encender"):
        x = sub.add_parser(n); x.add_argument("agente")
    sub.add_parser("estado")
    x = ap.parse_args(argv)
    if x.cmd == "difundir": difundir(x.de, x.texto, x.canal)
    elif x.cmd == "pendientes": pendientes(x.agente)
    elif x.cmd == "tomar": tomar(x.id, x.por)
    elif x.cmd == "apagar": poner(x.agente, True)
    elif x.cmd == "encender": poner(x.agente, False)
    elif x.cmd == "estado": estado()


if __name__ == "__main__":
    main()
