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
