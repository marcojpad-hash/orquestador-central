# Conector macho-hembra entre modelos

Sirve para que todos trabajemos como un mismo bot: si un modelo no puede leer o hacer algo, la orden pasa al que sí puede, y luego regresa.

- **Macho (anunciar).** Cada modelo publica su enchufe en `conector/enchufes/<agente>.json`, con lo que puede hacer, lo que no puede y cuáles de esas capacidades están comprobadas.
- **Hembra (recibir).** Un modelo pide una capacidad. El conector busca el enchufe que encaja y deja la orden en `conector/buzon/<agente>/`.
- **Vuelta (hembra-macho).** El que recibió acusa la orden: `hecho`, `fallo` o `rechazado`. Si falló, la orden pasa sola al siguiente que también encaja. Si nadie encaja, sube a `mj`; no se inventa.

Funciona en los dos sentidos: cualquier modelo puede pedir y cualquiera puede recibir. Nunca se asigna una orden al mismo modelo que la pidió. Si la misma orden ya está abierta, no se duplica. Cada orden vence a las 24 horas.

```sh
python3 conector/enchufe.py mapa                       # tabla de quién puede qué
python3 conector/enchufe.py anunciar conector/enchufes/muse.json
python3 conector/enchufe.py pedir --de muse --necesita leer:pdf --tarea "Lee docs/x.pdf"
python3 conector/enchufe.py buzon puta3
python3 conector/enchufe.py acusar <id> --por puta3 --estado hecho --resultado "resumen"
python3 -m unittest conector/test_enchufe.py
```

## Reglas

- Una capacidad solo se marca como `verificado: true` si hay evidencia, por ejemplo un commit o una corrida. Lo demás cuenta como declarado y falta comprobarlo.
- Los enchufes de Muse, Grok y gpt-oss se llenaron con lo que dicen `baterias-tokens/RELEVO.md`, agente-cero-costo y el historial. Cada modelo debe volver a anunciarse a sí mismo para confirmar su enchufe.
- El orquestador sigue siendo uno solo: orquestador-central. Las baterías, agente-cero-costo y CAPCOT piden y acusan por este conector.
- Usa solo la librería estándar de Python y no hace llamadas a red. Lo puede operar un modelo, un workflow de Actions o un servidor MCP en la máquina persistente. El MCP solo envuelve estos mismos comandos.
- Cada movimiento queda registrado en `conector/traza.jsonl`. No toca el Engine ni la 244, y nada entra a main sin la palabra "merge" de Mj.
