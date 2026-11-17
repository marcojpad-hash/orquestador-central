# Método de rigor
**Versión:** 1.1  
**Tipo:** filtro operativo transversal de rigor de lectura (Holmes/Sherlock, Hécate y Schopenhauer).  
**Alcance:** cualquier lectura o cadena de hipótesis. No pertenece al Motor U6; U6 es un consumidor.  
**Nunca decide H ni emite veredicto.**

Índice del apartado: [`README.md`](README.md). Regla de implementación: [`DERIVA_POR_SIMPLIFICACION.md`](DERIVA_POR_SIMPLIFICACION.md).

## ESPECIFICACIÓN FUNCIONAL A CABLEAR (objetivo)

Esta es la función que debe cablearse. La referencia no es el plugin actual del Motor U6.

### Referencia

Texto del método, **14 de septiembre de 2026**, en el dossier V15.1: [`METODO_HECATE_HOLMES_SCHOPENHAUER.txt`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/fuentes_originales/202609/DOSSIER_V15_1_20260914/docs/METODO_HECATE_HOLMES_SCHOPENHAUER.txt). Se corre **después** de la corrida, a mano o en un txt. «Si no aplica, se escribe "no"». «No motor, no plugin, no 244.» «No puntúa. No anula el JSON. Es el software de pensar.»

Esa misma mañana Mj lo nombra como protocolo, **t251u, 05:27** (hora de CDMX):

> «por eso tenemos a EKT y Holmes y Schopenhauer, que te dicen, ese es ese es el protocolo, si no me equivoco, es y es de las chidas porque dice, es lo que estamos viendo, es lo que queríamos ver o lo que se está mostrando en el en en la en la trazabilidad en el en lo que se está haciendo. O sea, no meter riesgos.»

En **t323u, 09:41** (hora de CDMX) Mj pega una lectura que cita ese texto (el cuaderno post-corrida aplicado a sí mismo). Las definiciones operativas salen del txt del dossier, no de las respuestas de esa lectura.

El **17 de noviembre de 2026, t1271u, 05:21** (hora de CDMX), Mj precisa qué se les había puesto:

> «ECA te pusimos que era el tercero excluido, pero no sé cómo se manejó. Schopenhauer, no me acuerdo cómo lo estaban manejando. Que era lo de que no te creyeras todo, o sea, lo que el dato que viene de ti. ¿Es es tuyo o es algo que estás queriendo, es es es el dato que viene de lo que infieres o es el dato que tú estás queriendo obligar?»

En t1271u nombró a Sherlock como el tercer filtro pero no terminó la frase («¿Y Sherlock o es el a Sherlock?»). La función de Holmes/Sherlock que sí está escrita desde el 14-sep, y que el plugin aún cita en su plantilla, es: «¿Los tokens salieron de HECHOS del corte o de la tesis que yo ya traía?»

### Lo que debe hacer

Se corre **después** de la lectura o la corrida. Si no aplica, se escribe «no»; no se salta. Cada marca es trazable al fragmento, token o tramo que la dispara. Solo marca. **No decide H ni apuesta.** El automático no sustituye las cuatro líneas humanas; tampoco puede reducirse a buscar unas cadenas y declarar el método cumplido.

**Holmes / Sherlock.** Entrada: los tokens o apoyos que se están usando y el corte (o texto) del que deberían salir. Pregunta: ¿salieron de hechos del corte o de la tesis previa? El método del 14-sep añade: «¿Qué hecho NO mapeé porque no me convenía?» Si el letrero nació de la tesis previa, se anota `SESGO_DE_TEORIA`. «Holmes: la teoría entra al final.» Salida: marca con traza (token → fuente: hecho del corte o tesis), o «no».

**Hécate.** Entrada: la lectura, la cadena de cortes y las opciones que se consideraron o se cerraron. Mj (t1271u) lo puso como **el tercero excluido**. En el método del 14-sep esa pieza es «¿Forcé una sola lámpara? (tercero excluido)», junto a otras tres preguntas del mismo bloque (Watzlawick / «la cura que enferma»): ¿pedí otro corte o token igual porque el anterior no «cerraba»?; ¿traté el contrario como solución?; ¿declaré ley para «aclarar»? Si sí, se anota `MAS_DE_LO_MISMO` o `CLARIFINANTE`. Salida: marca con traza a la opción excluida, a la repetición o a la «ley» declarada, o «no». Forzar una sola lámpara debe marcarse aunque el letrero #1 cambie de un corte a otro.

**Schopenhauer.** Entrada: el dato o la defensa que se está sosteniendo, y el tablero o la evidencia. Mj (t1271u): no creerte todo; el dato que viene de ti, ¿es tuyo, es lo que infieres, o es lo que estás queriendo obligar? El método del 14-sep: «¿Estoy defendiendo mi tanteo anterior o leyendo el tablero?»; analogía vendida como identidad; persistencias vendidas como ley. Si sí, se anota `ESTRATAGEMA`, no hallazgo. Salida: marca con traza al fragmento de defensa o imposición, o «no».

Formato de salida mínimo:

```json
{
  "caso": "…",
  "holmes": {"aplica": true, "marca": "SESGO_DE_TEORIA", "traza": "…"},
  "hecate": {"aplica": true, "marca": "CLARIFINANTE", "traza": "…"},
  "schopenhauer": {"aplica": false, "marca": "no", "traza": null},
  "sigue_en_cuaderno": "si/no",
  "can_decide_H": false
}
```

### Criterios de aceptación / tests

- **Holmes:** una lectura cuyos apoyos salen de la tesis previa, no de hechos del corte, debe marcar `SESGO_DE_TEORIA` (con traza token→fuente) aunque el texto **no** contenga «se llama», «es kant», «es freud» ni «es monroe». Nombrar un apellido no es la definición de la función.
- **Hécate:** forzar una sola lámpara (tercero excluido) debe marcar aunque la cadena de top1 cambie. Pedir «más de lo mismo» porque el tramo anterior no cerraba debe marcar. Repetir el mismo letrero cuatro cortes puede ser un síntoma de «más de lo mismo»; no agota la función.
- **Schopenhauer:** defender u obligar un dato (propio, inferido o impuesto) debe poder marcarse sin la frase literal «como yo dije», con traza al fragmento.
- Si no aplica, la salida escribe «no». No se omite el bloque.
- Cada marca lleva traza. Ninguna sale como veredicto ni como H.

### Versión actual vs debe hacer

| | Actual: [`plugin_metodo_rigor.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/plugin_metodo_rigor.py) (rama `alterno/cameo-pesos`; el SHA es el mismo que el del dossier del 14-sep) | Debe hacer |
|---|---|---|
| Holmes / Sherlock | Salta solo si la hipótesis contiene «se llama», «es kant», «es freud» o «es monroe». | ¿Los tokens salieron de hechos del corte o de la tesis previa? Traza token→fuente. |
| Hécate | Salta solo si `cadena_top1` repite el mismo letrero 4 cortes (`HECATE_MAS_DE_LO_MISMO`). El tercero excluido no se revisa. | Tercero excluido (¿forcé una sola lámpara?) y el resto del bloque del 14-sep. |
| Schopenhauer | Salta solo si el inverso contiene «como yo dije». | ¿El dato es tuyo, lo que infieres, o lo que quieres obligar? ¿Defiendo el tanteo o leo el tablero? |
| Plantilla | Cuatro líneas humanas (holmes / hecate / schopenhauer / sigue_en_cuaderno). La nota dice: «auto no sustituye las 4 líneas humanas». | La plantilla se conserva. El automático tiene que intentar esas preguntas, no sustituirlas por tres cadenas. |
| Traza / H | Las alarmas automáticas no trazan al fragmento fuente. `can_decide_H` no está en el plugin; el envoltorio declara que no decide H. | Toda marca con traza. Nunca decide H. |

El envoltorio [`guardianes_control_v1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/guardianes_control_v1.py) (`g_rigor`) llama a ese mismo plugin y añade dos marcas amarradas a U6: `HOLMES_TOP1_SIN_TOKENS_DE_HECHO` (el top1 no trae `favor_tokens` en `own_evidence`) y `SCHOPENHAUER_TABLERO_EN_CONTRA` (masa en contra mayor que a favor). Tampoco implementan el origen del token, el tercero excluido ni la distinción tuyo / inferido / obligado.

### Estado

**DEGRADADA (relajada)**, según [`DERIVA_POR_SIMPLIFICACION.md`](DERIVA_POR_SIMPLIFICACION.md). El plugin automático nunca implementó el método del 14-sep: lo redujo a tres alarmas por cadenas. La plantilla humana conserva las preguntas; lo cableado no.

Mj señala (**t1272u, 17 de noviembre de 2026, 05:23**, hora de CDMX) que fue el bot (Puta 3) quien lo cableó y declaró que «todo quedaba ya consistente y concordante» unas semanas antes de la salida del 20 de octubre al repositorio (cuando empezaron a usar GitHub; «una o dos antes de esa»), sin verificar la función: «al parecer, se […] lo volviste más laxo. Más relajado.» En el índice de transcripts no aparece, fuera de t1272u, la frase literal «consistente y concordante»; queda como señalamiento de Mj, no como cita localizada del mensaje original del bot.

Cualquier consumidor que diga «método de rigor aplicado» u «Holmes/Hécate/Schopenhauer ejecutados» sin cumplir lo exigido en «Lo que debe hacer» y en «Criterios de aceptación» es falso.

## 1. Origen

La primera mención oral de Mj que se localizó es **t251u** (14 de septiembre de 2026, 05:27, hora de CDMX), citada arriba. El texto operativo está en el dossier V15.1 del mismo día. La precisión de función está en **t1271u** (17 de noviembre de 2026). Este documento no identifica el método con «Game of Assassin»: Mj dijo ese mismo día que esa pieza no le suena a Schopenhauer ni al clasificador de falacias.

## 2. Función esencial

Obligar, *después* de una lectura o de una apuesta, las tres preguntas del método (Holmes, Hécate, Schopenhauer) y si eso sigue en el cuaderno. Son alarmas trazables, no una prueba que cierre el caso. El detalle a cablear está en la especificación de arriba.

## 3. Entrada y salida

Las de la especificación funcional a cablear. **No sale** una H nueva, un recálculo de puntaje ni un veredicto.

## 4. Qué no es

- No es «Game of Assassin» (pendiente, no identificado; Mj dijo que no le suena a Schopenhauer ni a falacias).
- No es el clasificador de falacias ni Copi.
- No es el hombre de acero ni el décimo hombre (controles de la apuesta U6, de otro tipo).
- No puntúa, no toca F y no debe fusionarse a Engine V5.
- El automático no sustituye las preguntas humanas del cuaderno; tampoco las cumple por buscar tres cadenas.

## 5. Consumidores

En el Motor U6, rama `alterno/cameo-pesos`:

- [`plugin_metodo_rigor.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/plugin_metodo_rigor.py) (`PLUGIN_METODO_RIGOR`, bloque `SHERLOCK_RIGOR`)
- Lo envuelve [`guardianes_control_v1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/guardianes_control_v1.py) después del predictor, y hay una llamada previa en laterales como sensor, no como decisor.
- Inventario: [MAPA_GUARDIANES.md §2.7](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/docs/MAPA_GUARDIANES.md)

Declara no tocar F, no puntuar y, en el envoltorio, `can_decide_H=False`. Solo marca. Ese cableado está **DEGRADADO** respecto de la especificación de arriba. No redefine el método. Sin tocar Engine V5 ni el 244.
