# Lateral de contexto enunciativo — contrato transversal

**Versión:** 1.0  
**Tipo:** guardián operativo observacional, transversal y agnóstico.  
**Estado:** implementación inicial; la equivalencia funcional con U6 se prueba por casos compartidos.  
**Identificador de código:** `LATERAL_CONTEXTO_ENUNCIATIVO_V1_0`.

## 1. Propósito

Registrar cómo se presenta y valora la información: juicios expresados, atribuciones, orientación positiva/negativa, repetición, encuadre adversarial, cierre discursivo de alternativas y funciones lingüísticas. El resultado describe el input y su procedencia; no diagnostica al enunciador.

La observación discursiva es distinta de la admisión factual. Sombrero Blanco sigue admitiendo hechos objetivamente medibles y separando el ruido factual. Este lateral conserva los juicios como hechos del discurso: «el enunciador calificó X como brillante» puede observarse aunque «X es brillante» no esté demostrado.

## 2. Entradas y procedencia

Cada registro puede contener:
- `text`: fragmento íntegro.
- `origin`: ruta/campo/fuente dentro del input.
- `speaker`: enunciador explícitamente identificado; si falta, `NO_IDENTIFICADO_EN_INPUT`.
- `attributed_to`: persona o voz a la que el texto atribuye la expresión, si el input lo declara.

No se infiere la identidad real de un hablante por el estilo. Se conserva la diferencia entre quien transmite y quien aparece citado.

## 3. Dimensiones observadas

### Juicios
Estético, valorativo, moral, predictivo, especulativo, normativo, causal, intencional, epistémico y comparativo. Se registra fragmento, término, tipo, polaridad y procedencia.

### Funciones del lenguaje
Funciones de Bühler (representativa, expresiva y apelativa), etiquetas heurísticas de Jakobson (referencial, emotiva, conativa, fática, metalingüística y poética) y metafunciones de Halliday (ideacional, interpersonal y textual). Saussure aporta la teoría del signo y la distinción lengua/habla, no esta taxonomía funcional.

### Comportamiento discursivo
Reiteración de cargas valorativas, asimetría entre actores, encuadre adversarial y cierre de alternativas. La omisión selectiva requiere un corpus de contraste; no se infiere de un texto aislado.

## 4. Salidas

- Observaciones atómicas trazadas al fragmento y a su origen.
- Conteos por actor solo cuando el actor aparece explícitamente identificable.
- Señales de patrón para revisión, nunca veredictos.
- Referencias contextuales para Sherlock/Holmes, Hécate, Schopenhauer, Falacias, Copi, Beristáin y Plugin Pregunta.
- Candados explícitos: no decide H, no escribe H, no escribe patrones, no reordena candidatos y no modifica el input.

## 5. Cableado orgánico

El lateral corre en paralelo con Sombrero Blanco. No sustituye, modifica ni condiciona su admisión factual. Sus señales se adjuntan como contexto trazable a los controles operativos pertinentes. Cada control conserva su especificación, autoridad y salida. Una referencia contextual no equivale a ejecutar el método referido ni a declarar que encontró una falacia, sesgo o intención.

La adaptación U6 se integra en el paquete de guardianes posterior al predictor. La copia agnóstica se ejecuta en el plano central y puede ser consumida por cualquier proyecto mediante un adaptador. Las dos implementaciones conservan el mismo contrato y se prueban con casos compartidos; ninguna sustituye a la otra.

### 5.1 Ruta condicional

En el plano central el lateral no corre siempre: se activa solo cuando el input trae contenido enunciativo que observar. La ruta es el adaptador `runtime/diagnostics/ruta_contexto_enunciativo.py`, invocable como paso del runner secuencial. El predicado `debe_observar()` decide con los propios marcadores del lateral — juicios de `JUDGMENT_RULES`, función apelativa (`CONATIVE`), cierre discursivo (`EXCLUSION`) y encuadre adversarial (`ADVERSARIAL`) — y nombra en el motivo la familia que disparó, para que la activación quede legible en el reporte.

Dos estados posibles, ambos con salida 0 (un input neutro no es un fallo y no detiene la corrida):
- `ACTIVA`: el input trae contenido enunciativo; se ejecuta `analyze()` y se escribe el reporte completo.
- `SIN_ACTIVACION`: el input es neutro o puramente factual; se escribe un reporte mínimo y la ruta pasa en silencio.

Fragmento del paso para el contrato secuencial:

```json
{
  "name": "contexto-enunciativo-condicional",
  "action": "python runtime/diagnostics/ruta_contexto_enunciativo.py --input artifacts/input.txt --out artifacts/contexto-enunciativo.json",
  "expected": "Reporte de contexto enunciativo (ACTIVA o SIN_ACTIVACION)",
  "verify": "python runtime/verify_file.py --path artifacts/contexto-enunciativo.json --min-bytes 1",
  "retry_safe": true,
  "preconditions": [{"kind": "exists", "path": "artifacts/input.txt"}],
  "postconditions": [
    {"kind": "exists", "path": "artifacts/contexto-enunciativo.json"},
    {"kind": "min_bytes", "path": "artifacts/contexto-enunciativo.json", "value": 1}
  ]
}
```

Los filtros rígidos y verificables (validación de contrato, resto de adaptadores, CI) no se tocan y siguen corriendo siempre. El lateral sigue siendo observacional: no decide ni veta nada.

## 6. Límites epistemológicos

- Una valoración expresada es un dato del discurso, no una propiedad demostrada del objeto.
- Una repetición o asimetría es una señal, no prueba de favoritismo.
- No se atribuyen motivaciones, prejuicios, personalidad ni intenciones como hechos.
- No se confunde predicción o especulación del input con predicción del motor.
- No se generan valores especulativos propios.
- Las señales solo justifican ampliar lectura, contrastar fuentes o activar controles pertinentes.

## 7. Pruebas de aceptación

1. Dos elogios explícitos al mismo actor deben conservar ambos fragmentos y producir `CARGA_VALORATIVA_REITERADA`.
2. Dos elogios a un actor y dos descalificaciones a otro deben producir `ASIMETRIA_VALORATIVA_ENTRE_ACTORES`, sin emitir `FAVORITISMO` ni veredicto.
3. Un texto factual neutro no debe generar señales valorativas.
4. Los controles hermanos reciben referencias contextuales sin que cambien sus banderas.
5. La salida conserva `can_decide_H=false` y no modifica la entrada.
