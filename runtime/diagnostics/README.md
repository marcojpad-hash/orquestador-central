# Diagnósticos de input

Los módulos de esta carpeta son guardianes observacionales agnósticos. No deciden el resultado de un proyecto ni modifican sus datos canónicos.

## Contexto enunciativo

- Núcleo: `lateral_contexto_enunciativo.py`.
- Adaptador JSON ejecutable: `run_contexto_enunciativo.py`.
- Contrato: `docs/filtros_operativos/ORIENTACION_ENUNCIATIVA.md`.
- Pruebas: `runtime/test_runner.py`.

Uso desde un proyecto o desde el runner secuencial:

```bash
python runtime/diagnostics/run_contexto_enunciativo.py --input examples/contexto_enunciativo.example.json --output artifacts/contexto_enunciativo.json
```

La salida conserva procedencia y fragmentos, clasifica juicios y funciones lingüísticas, y genera señales de revisión. No infiere motivaciones, no etiqueta al enunciador como sesgado y no decide H. La implementación U6 es una copia funcional adaptada y se ejecuta en su paquete de guardianes.
