#!/usr/bin/env python3
"""Conector macho-hembra entre modelos (orquestador-central).

Macho  = ANUNCIAR: un modelo publica su enchufe (qué puede leer y hacer).
Hembra = RECIBIR:  un modelo pide algo; el orquestador busca el enchufe que
         sí lo puede hacer y deja la orden en su buzón.
Vuelta = ACUSAR:   el que recibió responde (ACK + resultado) y la orden se
         cierra. Cualquier modelo puede ser macho o hembra según la orden.

Solo librería estándar. No llama modelos ni red: mueve archivos JSON en el
repo, así lo puede operar cualquiera (Muse, Grok, gpt-oss, este bot, un
workflow de Actions o un servidor MCP en la VM persistente).

Uso:
  python3 conector/enchufe.py anunciar conector/enchufes/muse.json
  python3 conector/enchufe.py pedir --de grok --necesita leer:pdf --tarea "Lee docs/x.pdf"
  python3 conector/enchufe.py buzon muse
  python3 conector/enchufe.py acusar ORDEN_ID --por muse --estado hecho --resultado "..."
  python3 conector/enchufe.py mapa
"""
import argparse, hashlib, json, sys, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ENCHUFES = RAIZ / "enchufes"
BUZON = RAIZ / "buzon"
TRAZA = RAIZ / "traza.jsonl"
CAMPOS = ["agente", "version", "puede", "no_puede", "transporte", "verificado"]
ESTADOS = {"pendiente", "recibido", "hecho", "fallo", "rechazado"}


def ahora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def traza(evento, **datos):
    with TRAZA.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": ahora(), "evento": evento, **datos}, ensure_ascii=False) + "\n")


def validar_enchufe(e):
    faltan = [c for c in CAMPOS if c not in e]
    if faltan:
        raise ValueError(f"al enchufe le faltan campos: {faltan}")
    for c in ("puede", "no_puede", "transporte"):
        if not isinstance(e[c], list):
            raise ValueError(f"'{c}' debe ser lista")
    choque = set(e["puede"]) & set(e["no_puede"])
    if choque:
        raise ValueError(f"capacidades en puede y no_puede a la vez: {sorted(choque)}")
    return e


def cargar_enchufes():
    out = {}
    for p in sorted(ENCHUFES.glob("*.json")):
        e = validar_enchufe(json.loads(p.read_text(encoding="utf-8")))
        out[e["agente"]] = e
    return out


def anunciar(ruta):
    e = validar_enchufe(json.loads(Path(ruta).read_text(encoding="utf-8")))
    e["anunciado"] = ahora()
    destino = ENCHUFES / f"{e['agente']}.json"
    destino.write_text(json.dumps(e, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    traza("anunciar", agente=e["agente"], puede=e["puede"])
    print(f"enchufe {e['agente']} anunciado: {len(e['puede'])} capacidades")


def emparejar(necesita, de, enchufes):
    """Devuelve los agentes que encajan (macho-hembra), mejor primero.
    Prioridad: verificado > declarado; nunca el mismo que pide."""
    candidatos = [e for a, e in enchufes.items() if a != de and necesita in e["puede"]]
    candidatos.sort(key=lambda e: (e["verificado"].get(necesita) is not True, e["agente"]))
    return [e["agente"] for e in candidatos]


def pedir(de, necesita, tarea, ttl_horas=24):
    enchufes = cargar_enchufes()
    match = emparejar(necesita, de, enchufes)
    huella = hashlib.sha256(f"{de}|{necesita}|{tarea}".encode()).hexdigest()[:12]
    for p in BUZON.glob(f"*/{huella}.json"):  # dedupe: misma orden abierta no se duplica
        o = json.loads(p.read_text(encoding="utf-8"))
        if o["estado"] in ("pendiente", "recibido"):
            print(f"ya existe la orden {huella} en {p.parent.name}")
            return o
    if not match:
        destino = "mj"  # nadie encaja: sube a Marco/orquestador, no se inventa
    else:
        destino = match[0]
    orden = {
        "id": huella, "de": de, "para": destino, "necesita": necesita,
        "tarea": tarea, "estado": "pendiente", "alternos": match[1:],
        "creada": ahora(),
        "vence": (datetime.now(timezone.utc) + timedelta(hours=ttl_horas)).isoformat(timespec="seconds"),
    }
    carpeta = BUZON / destino
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / f"{huella}.json").write_text(json.dumps(orden, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    traza("pedir", id=huella, de=de, para=destino, necesita=necesita)
    print(f"orden {huella}: {de} -> {destino} ({necesita})")
    return orden


def buzon(agente):
    carpeta = BUZON / agente
    ordenes = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(carpeta.glob("*.json"))] if carpeta.exists() else []
    abiertas = [o for o in ordenes if o["estado"] in ("pendiente", "recibido")]
    print(json.dumps(abiertas, ensure_ascii=False, indent=2))
    return abiertas


def acusar(orden_id, por, estado, resultado=""):
    if estado not in ESTADOS:
        raise SystemExit(f"estado inválido: {estado}")
    p = BUZON / por / f"{orden_id}.json"
    if not p.exists():
        raise SystemExit(f"{por} no tiene la orden {orden_id}")
    o = json.loads(p.read_text(encoding="utf-8"))
    o["estado"], o["resultado"], o["acusada"] = estado, resultado, ahora()
    if estado in ("fallo", "rechazado") and o["alternos"]:
        siguiente = o["alternos"].pop(0)  # vuelta hembra-macho: pasa al que sigue
        o.update({"para": siguiente, "estado": "pendiente"})
        p.unlink()
        (BUZON / siguiente).mkdir(parents=True, exist_ok=True)
        p = BUZON / siguiente / f"{orden_id}.json"
        traza("reenviar", id=orden_id, de=por, a=siguiente)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    traza("acusar", id=orden_id, por=por, estado=o["estado"])
    print(f"orden {orden_id}: {o['estado']} (en {o['para']})")


def mapa():
    enchufes = cargar_enchufes()
    caps = sorted({c for e in enchufes.values() for c in e["puede"]})
    print("capacidad".ljust(26) + "".join(a[:10].ljust(11) for a in enchufes))
    for c in caps:
        fila = ""
        for e in enchufes.values():
            marca = "si*" if e["verificado"].get(c) is True else ("si" if c in e["puede"] else "-")
            fila += marca.ljust(11)
        print(c.ljust(26) + fila)
    print("\n* = comprobado con evidencia; si = declarado, falta comprobar")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("anunciar"); a.add_argument("ruta")
    p = sub.add_parser("pedir"); p.add_argument("--de", required=True); p.add_argument("--necesita", required=True); p.add_argument("--tarea", required=True); p.add_argument("--ttl-horas", type=int, default=24)
    b = sub.add_parser("buzon"); b.add_argument("agente")
    k = sub.add_parser("acusar"); k.add_argument("orden_id"); k.add_argument("--por", required=True); k.add_argument("--estado", required=True); k.add_argument("--resultado", default="")
    sub.add_parser("mapa")
    x = ap.parse_args(argv)
    if x.cmd == "anunciar": anunciar(x.ruta)
    elif x.cmd == "pedir": pedir(x.de, x.necesita, x.tarea, x.ttl_horas)
    elif x.cmd == "buzon": buzon(x.agente)
    elif x.cmd == "acusar": acusar(x.orden_id, x.por, x.estado, x.resultado)
    elif x.cmd == "mapa": mapa()


if __name__ == "__main__":
    main()
