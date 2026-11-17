# Ejecutar la suite de aceptación

Desde la raíz del repositorio:

```bash
python tests/guardianes/run_acceptance.py
python -m unittest discover -s tests/guardianes -p 'test_*.py' -v
```

El runner carga los fixtures y busca adaptadores reales en `adapters.json`. Cada adaptador se registra como `"guardian_id": "modulo_python:funcion"` y recibe el caso completo. Debe devolver `status=EXECUTED`, los criterios satisfechos, las conductas prohibidas observadas, las marcas con traza y `can_decide_H=false`.

**No hay adaptadores semánticos instalados en esta rama.** Por diseño, el primer comando debe terminar `BLOCKED` con 15 casos bloqueados, no con un PASS artificial. Los tests unitarios prueban el contrato del runner (bloqueo por ausencia, PASS con adaptador de prueba, fallo por criterio omitido, marca sin traza y prohibición de decidir H); no prueban la corrección semántica de los guardianes.
