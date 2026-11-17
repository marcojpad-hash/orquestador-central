# Copi
**Versión:** 1.0  
**Tipo:** filtro operativo transversal de lógica.  
**Alcance:** cualquier input o cadena de razonamiento que se pretenda presentar como inferencia válida. No pertenece al Motor U6; U6 es un consumidor.  
**Nunca decide H ni emite veredicto.**

Índice del apartado: [`README.md`](README.md).

## 1. Origen
Mj lo pidió por nombre el **14 de septiembre de 2026** (hora de CDMX), sesión `56d9fab0-f92f-4850-a04b-6f55ff03e508`:

- t280u, 07:18: «Falacias y copi»
- t291u, 07:48: «A ver Beristain Copi y falacias»

El 14 de octubre (t773u, 03:49, hora de CDMX) lo volvió a dictar como «copy», junto al sombrero blanco, falacias y Beristáin. El 17 de noviembre de 2026 confirmó que «copy» es Copi.

En t292u y t293u (14-sep, textos que ella avaló ese día): las falacias y la lógica son una capa de lectura del input, no patrones nuevos de un catálogo predictivo. «Palabra ≠ intención ≠ función sintáctica ≠ carga semántica ≠ tropo ≠ falacia ≠ señal del fenómeno.»

Fuente teórica del consumidor U6: Irving Copi, *Introducción a la lógica* (así lo declara el propio módulo).

## 2. Función esencial
Comprobar si un paso se sostiene como inferencia o reemplazo, y señalar cuando la forma es una falacia espejo (por ejemplo, afirmar el consecuente o negar el antecedente). No dice si la conclusión es “verdadera” en el mundo ni qué perfil o apuesta corresponde. Marca consistencia o su ausencia; deja traza de qué regla o qué rotura vio.

## 3. Entrada y salida
**Entrada:** un texto, una pregunta o una cadena de pasos que se presentan como razonamiento (premisas y conclusión, condicionales, disyunciones).

**Salida:**
- pasos que corresponden a una regla de inferencia o de reemplazo, o que no corresponden;
- falacias espejo detectadas, con el trazo al fragmento o al paso;
- cuando no hay frontera clara, un estado de no resuelto (átomos que no se pueden emparejar, conclusión que introduce un átomo nuevo, etc.);
- solo banderas: limpio / marca / no resuelto.

**No sale:** una H, un veredicto, un perfil, ni la corrección automática del argumento.

## 4. Qué no es
- No es un diccionario de palabras “ilógicas”.
- No es el clasificador de falacias del plugin pregunta (ese es un filtro hermano: [`FALACIAS.md`](FALACIAS.md)).
- No es el sombrero blanco: no decide qué es hecho o adorno; decide si la forma lógica se sostiene.
- No es un patrón del catálogo 244 ni un productor de apuestas.
- No sustituye evidencia: un razonamiento válido puede partir de premisas falsas; el filtro no convierte validez en hecho.

## 5. Consumidores
Hoy hay una implementación en el Motor U6, rama `alterno/cameo-pesos` de `marcojpad-hash/motor-u6-storage`:

- [`guardian_logica_copi_v1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/guardian_logica_copi_v1.py) (v1.0.1-20260927, `LOGICA_COPI`)
- Lo llama [`guardianes_control_v1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/guardianes_control_v1.py) después del predictor.
- Inventario: [MAPA_GUARDIANES.md §2.4](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/docs/MAPA_GUARDIANES.md)

El núcleo proposicional (tablas de verdad; 9 reglas de inferencia —MP, MT, SH, SD, DC/Abs, Simp, Conj, Ad, más DD como extra— y 10 de reemplazo) es genérico y declara `can_decide_H=False`.

**Ataduras y defectos de ese cableado:**
- Los adaptadores (b) y (c) están amarrados a U6: regla de cierre del motor (`DETERMINADO` / latencia / compuerta) y cadena del top1 por corte (non sequitur, subdeterminación H1/H2).
- Solo marca. Un `NO_RESUELTO` puede retener el cierre vía `ruta_cierre_latente`, pero no escribe H ni `patterns`.
- Antes del 27-sep-2026 la especificación existía y el sidecar llegaba a devolver `copi=None`; este archivo fue la primera implementación en código, según su propio docstring.
- Ese cableado no redefine el método. Corregirlo, si se hace, pertenece al repositorio del motor, sin tocar Engine V5 ni el catálogo 244.
