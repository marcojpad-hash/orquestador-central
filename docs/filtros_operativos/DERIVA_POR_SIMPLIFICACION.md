# Deriva por simplificación
**Versión:** 1.0  
**Tipo:** advertencia y regla operativa transversal del orquestador.  
**Alcance:** el Motor U6 y cualquier consumidor o implementador de piezas del orquestador.  
**No es:** un filtro de admisión del input, un permiso para recortar una función en nombre de la eficiencia, ni un sustituto de los [filtros operativos](README.md).

## Advertencia

Patrón observado por Mj el **17 de noviembre de 2026** (hora de CDMX): cuando el trabajo se vuelve adversarial, los modelos de lenguaje que implementan tienden a simplificar de más y a eliminar partes porque parece más eficiente. Eso va contra lo que se está construyendo.

### Ejemplo documentado: sombrero blanco

La separación hecho/juicio se perdió al cablearse. El detalle está en [SOMBRERO_BLANCO.md](SOMBRERO_BLANCO.md) (especificación funcional a cablear):

- **14-sep-2026** (hora de CDMX), versión manual: `FILTRO_TRAZA_BRUTO` (t350u–t353u). Ítems 01–06 hechos; 07–10 lecturas forzadas, con traza al texto fuente.
- **27-sep-2026:** lista de 5 frases, solo sobre la pregunta; de los cortes solo cuenta tokens. Escribe `ENFORCED` y `facts_only_boundary=True` fijos, sin revisar.
- **Parche 010a, 6-oct-2026:** la misma lista también sobre textos de corte; sigue sin separar hecho de juicio, adjetivo ni figura, y no traza.

Ninguna versión cableada implementó la función del 14-sep. El estado vigente de esa pieza es **NO CABLEADO**, no «aplicado».

### Otros síntomas

- Estados «aprobado», `EXECUTED` o `ENFORCED` fijos, sin verificar.
- Piezas reducidas a un diccionario o a una lista de frases.
- Funciones renombradas que ya no hacen lo original.

## Regla obligatoria

Aplica al motor y a cualquier consumidor del orquestador.

Antes de dar por buena una pieza o un cambio, revisar los **checkpoints anteriores** (no los ejercicios, que pesan menos) para ver qué se metió en cada versión y qué evolucionó o cambió su función inicial.

Por pieza hay que dejar escrito:

1. Función original, con fuente.
2. Función en cada checkpoint.
3. Qué se perdió y qué se agregó.
4. Veredicto: **FIEL** / **DEGRADADA** / **CAMBIÓ DE FUNCIÓN**.

Si una pieza está **DEGRADADA** o **CAMBIÓ DE FUNCIÓN** sin decisión explícita de Mj, es **fallo, no eficiencia**. Se reporta y se restaura la función original. Simplificar solo vale si conserva la función y lo prueba un test.

### Plantilla de auditoría

| Pieza | Función original (fuente) | Checkpoint / versión | Función en esa versión | Perdió / agregó | Veredicto |
|---|---|---|---|---|---|
| | | | | | FIEL / DEGRADADA / CAMBIÓ DE FUNCIÓN |

### Dónde viven los checkpoints conocidos

Se citan solo rutas verificadas. Un pack que no esté en GitHub sigue siendo obligatorio si está en el workspace del bot; no estar en el repo no autoriza a saltarlo.

- **Expediente 20260927.** El comparativo de versiones del 27 de septiembre de 2026 (hora CST, según su propio README) está en el workspace del bot: `/workspace/COMPARATIVO_VERSIONES_EXPEDIENTE_20260927`. No está integrado a un repositorio. En `marcojpad-hash/motor-u6-storage` sí está el ejecutable de esa fecha: [`motor/motor/MOTOR_V15_3_UNICO_20260927.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/MOTOR_V15_3_UNICO_20260927.py) (también en `main`).
- **Checkpoint de unificación 20261011.** Está en el workspace del bot: `/workspace/UNIFICADO_20261011` (incluye `B_CHECKPOINT` y `B_HISTORICO`). **No está integrado al repo.** Lo declara [`docs/HANDOFF_MOTOR_GROK.md`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/docs/HANDOFF_MOTOR_GROK.md) del motor: «Checkpoint unificación 20261011: no integrado al repo (solo en workspace del bot)». El archivo [`motor/capa_llm/FIXTURE_MOCK_CONSULTA_20261011.json`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/capa_llm/FIXTURE_MOCK_CONSULTA_20261011.json) es un fixture de la capa LLM, no el checkpoint.
- **`motor-u6-storage` desde el 24 de octubre de 2026.** Repositorio [`marcojpad-hash/motor-u6-storage`](https://github.com/marcojpad-hash/motor-u6-storage), commit inicial `afa0717` («Storage inicial motor U6»). La historia posterior se lee en git. Rama de trabajo vigente: `alterno/cameo-pesos`. En el mismo repo, `fuentes_originales/202609/` conserva packs anteriores (dossier V15.1 del 14-sep y protocolo Mozart del 15-sep); son fuentes históricas, no el checkpoint 20261011.

Si aparece otro checkpoint con fecha y ruta verificables, se añade a esta lista. No se inventan rutas.
