# Falacias
**Versión:** 1.0  
**Tipo:** filtro operativo transversal de lógica (formas falaces en la enunciación).  
**Alcance:** cualquier pregunta o texto cuya forma pueda estar inclinando la lectura. No pertenece al Motor U6; U6 es un consumidor.  
**Nunca decide H ni emite veredicto.**

Índice del apartado: [`README.md`](README.md).

## 1. Origen
El **14 de septiembre de 2026** (hora de CDMX), en la misma plática del sombrero blanco y del plugin pregunta, sesión `56d9fab0-f92f-4850-a04b-6f55ff03e508`:

- t280u, 07:18: «Falacias y copi»
- t291u, 07:48: «A ver Beristain Copi y falacias»

En t292u / t293u (textos que Mj avaló ese día): la capa lógica marca si «la estructura del razonamiento está haciendo algo que merezca una bandera», como sidecar de lectura, no como uno de los 244 patrones. Cada capa puede corregir a la anterior. «Palabra ≠ … ≠ tropo ≠ falacia ≠ señal del fenómeno.»

Mj confirmó el 17 de noviembre de 2026 que este filtro **existe**, y que **no** es lo que ella llama «Game of Assassin».

En Notion (20-sep-2026) quedó un conflicto documental viejo entre una SPEC pendiente y una nota de PASS; eso es historial de auditoría, no una definición nueva del método.

## 2. Función esencial
Señalar formas falaces o sospechosas en cómo está armado el enunciado (por ejemplo, afirmar el consecuente, causa aparente por sucesión, pregunta compleja), sin contestar el fondo ni traducir la forma en un rasgo del sujeto. Es highlight: «así viene armada esta parte»; no «entonces es culpable / entonces es H1».

Es hermano de Copi, no el mismo filtro. Copi examina validez de pasos con reglas de inferencia y reemplazo; este clasificador mira formas frecuentes en el texto o en la pregunta.

## 3. Entrada y salida
**Entrada:** una pregunta o un texto, partido en unidades que se puedan señalar.

**Salida:**
- marcas por tipo de forma (en el consumidor U6 actual: `AF`, `AD`, `CS`, `BC1`, `BC2`, `PQ`, `EQ`), con trazo al fragmento;
- severidad o estado (`DETECTADA` / `POSIBLE`, u equivalente) cuando la forma no es nítida;
- solo banderas: limpio / marca / error de ejecución.

**No sale:** veredicto, H, perfil, ni la “corrección” del argumento.

## 4. Qué no es
- No es Copi ([`COPI.md`](COPI.md)), aunque se pidieron juntos y se complementan.
- No es Beristáin: una lítote o una hipérbole es figura; una falacia es un paso de razonamiento en mala forma.
- No es «Game of Assassin» (pendiente, no identificado).
- No es un patrón del 244 ni un freno que tumbe el tubo por default.
- No declara que el contenido sea falso; declara que la forma no sostiene lo que parece sostener.

## 5. Consumidores
En el Motor U6, rama `alterno/cameo-pesos`:

- El clasificador vive dentro de [`plugin_pregunta_dirigida_v0_5_1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/plugin_pregunta_dirigida_v0_5_1.py) (capa 0.5.0/0.5.1: `detectar_falacias`).
- Lo corre [`guardianes_control_v1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/guardianes_control_v1.py) después del predictor, en el bloque `FALACIAS`.
- Inventario: [MAPA_GUARDIANES.md §2.3](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/docs/MAPA_GUARDIANES.md)

Declara no tocar Engine V5 ni 244 y no inventar H. Solo marca (vecino de Beristáin).

**Ataduras y defectos de ese cableado:**
- Está empaquetado dentro del plugin de pregunta dirigida, no como método independiente del orquestador.
- Corre amarrado a los textos y a la pregunta del caso U6, después de la apuesta, no como filtro previo y agnóstico de cualquier input.
- La forma se detecta con reglas locales (condicionales, «cada vez que», etc.); no sustituye una lectura humana de la argumentación completa.
- Ese cableado no redefine el método. Sin tocar Engine V5 ni el 244.
