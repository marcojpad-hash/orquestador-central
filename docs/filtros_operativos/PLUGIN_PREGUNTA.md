# Plugin pregunta
**Versión:** 1.0  
**Tipo:** filtro operativo transversal: clasificar la estructura de la pregunta o del enunciado antes de usarla como evidencia.  
**Alcance:** cualquier pregunta, consigna o texto que vaya a tratarse como marco de una lectura o de un perfil. No pertenece al Motor U6; U6 es un consumidor.  
**Nunca decide H ni emite veredicto.**

Índice del apartado: [`README.md`](README.md). Es hermano del [sombrero blanco](SOMBRERO_BLANCO.md), no el sombrero mismo.

## 1. Origen
Se armó el **14 de septiembre de 2026** (hora de CDMX), en la misma plática del sombrero blanco, sesión `56d9fab0-f92f-4850-a04b-6f55ff03e508`.

De madrugada Mj rechazó el plugin corto por lista de frases (t203u, t204u, t207u): un diccionario «siempre se encuentra la forma de cómo saltárselo». A las 01:57, t205u, la identificación objetiva del input «sería tal cual un filtro», no perfilamiento.

A las 07:48, t292u (texto que ella avaló, con prefacio oral), quedó la misión:

> «Clasificar la estructura de la pregunta antes de interpretar su contenido como evidencia.»

Cadena que ella avaló ese día:

`INPUT → qué está preguntando → unidades lingüísticas objetivables → valoración/adjetivización → estructura narrativa → ruido retórico/lógico → qué puede trazarse → PERFIL` (solo banderas).

Prohibido: `INPUT → palabras fuertes → patrón → perfil`.

Trazabilidad ≠ sesgo (t292u): sesgo es «esta característica está inclinando el resultado»; trazabilidad es «puedo señalar qué elemento del input produjo esta clasificación y qué naturaleza lingüística tenía».

Beristáin, falacias y Copi entran aquí como capas de esa cadena, no como motores aparte de predicción. Recuento posterior: página de Notion [SOMBRERO BLANCO + plugin pregunta](https://app.notion.com/p/3e152e5cb10c8105b38be389515ebd17) (19–20 sep), que no es la fuente original.

## 2. Función esencial
Antes de tratar una pregunta o un enunciado como evidencia de perfil, decir qué clase de información trae: qué se pregunta, qué es objetivable, qué es valoración, qué es narrativa, qué es ruido retórico o lógico, y qué se puede trazar. El perfil, si aparece, son banderas, no una apuesta.

El sombrero blanco es la lente de admisión de hechos. Este plugin es la lente sobre **cómo viene armada** la pregunta.

## 3. Entrada y salida
**Entrada:** una pregunta, una consigna o un texto usado como marco.

**Salida:**
- qué se está preguntando;
- unidades objetivables (y su trazo);
- valoración o adjetivización;
- narrativa;
- ruido retórico o lógico (con remisión a [`BERISTAIN.md`](BERISTAIN.md) y [`FALACIAS.md`](FALACIAS.md) / [`COPI.md`](COPI.md) cuando aplique);
- qué es trazable;
- banderas de perfil o de pregunta dirigida, si las hay.

**No sale:** H, HIT, familia del 244, ni la respuesta al contenido de la pregunta.

## 4. Qué no es
- No es un diccionario de trampas léxicas («quién es», «es ambicioso», «qué va a pasar»). Esa fue la v1 que Mj rechazó.
- No es para «predecir mejor» ni para subir el HIT (t292u; también el recuento de Notion).
- No es el sombrero blanco, aunque se usan juntos: primero (o en paralelo) lo medible; aquí, la estructura de la enunciación.
- No es un patrón del 244. Tropos y falacias no se convierten en patrones nuevos del catálogo.
- No contesta el veredicto que la pregunta ya trae armado (t206u: el filtro no debe responder «sí, a huevo ese güey era un culero»).

## 5. Consumidores
En el Motor U6, rama `alterno/cameo-pesos`:

- [`plugin_pregunta_dirigida_v0_5_1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/plugin_pregunta_dirigida_v0_5_1.py) — fuga en corpus, P∧O, cotejo con sellado post-Z, post hoc, y el clasificador de falacias.
- [`plugin_pregunta_detras_v2.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/plugin_pregunta_detras_v2.py) (v2.3.2) — función del lexema (campo vs etiqueta), corrección sintáctica del léxico, tropos estructurales (lítote, hipérbole).
- Los llama [`guardianes_control_v1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/guardianes_control_v1.py) después del predictor.
- Inventario: [MAPA_GUARDIANES.md §2.2–2.3](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/docs/MAPA_GUARDIANES.md)

Ambos declaran no tocar Engine V5 ni 244 y no inventar H. Highlight only.

**Ataduras y defectos de ese cableado:**
- Los docstrings siguen diciendo «PROPUESTA» / «no cablear al limpio sin OK», pero el MAPA y `guardianes_control_v1` sí los corren en la corrida U6. Hay un desfase entre la etiqueta del archivo y el cableado real.
- La v1 por lista de frases quedó atrás de propósito; si alguien reactivara ese diccionario, repetiría lo que Mj rechazó el 14-sep.
- Corren amarrados al caso U6 (pregunta del caso, sellado post-Z, textos de cortes), después de la apuesta, no como filtro previo y agnóstico de cualquier input del orquestador.
- `plugin_pregunta_dirigida.py` (sin sufijo de versión) es un archivo corto de 13 líneas, distinto del v0.5.1; no confundirlos.
- Ese cableado no redefine el método. Sin tocar Engine V5 ni el 244.
