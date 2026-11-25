#!/usr/bin/env python3
"""Ruta condicional del lateral de contexto enunciativo.

Uso (paso del runner secuencial):
  python runtime/diagnostics/ruta_contexto_enunciativo.py --input <archivo.txt> --out <reporte.json>
Lee el input, decide con debe_observar() si trae contenido enunciativo y,
solo entonces, ejecuta analyze(). Si no trae, escribe un reporte mínimo
SIN_ACTIVACION y sale 0: pasa en silencio sin romper nada.
No decide, no veta, no modifica el input: solo observa y reporta.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from lateral_contexto_enunciativo import analyze, debe_observar, VERSION, CAN_DECIDE_H

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    texto = Path(a.input).read_text(encoding="utf-8")
    activa, motivo = debe_observar(texto)
    if not activa:
        reporte = {"version": VERSION, "estado": "SIN_ACTIVACION", "motivo": motivo,
                   "observaciones": [], "senales": [],
                   "candados": {"can_decide_H": CAN_DECIDE_H, "escribe_H": False,
                                "escribe_patterns": False, "reordena_candidatos": False,
                                "modifica_input": False},
                   "ruta": "condicional"}
    else:
        reporte = analyze([{"text": texto, "origin": "INPUT"}])
        reporte["estado"] = "ACTIVA"
        reporte["motivo"] = motivo
        reporte["ruta"] = "condicional"
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(reporte, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"contexto enunciativo: {reporte['estado']} ({motivo}) -> {a.out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
