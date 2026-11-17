# Método de rigor
**Versión:** 1.0  
**Tipo:** filtro operativo transversal de rigor de lectura (alarmas Holmes, Hécate y Schopenhauer).  
**Alcance:** cualquier lectura o cadena de hipótesis donde convenga preguntar si se está defendiendo lo visto, repitiendo el mismo letrero o colando un nombre que no debería estar. No pertenece al Motor U6; U6 es un consumidor.  
**Nunca decide H ni emite veredicto.**

Índice del apartado: [`README.md`](README.md).

## 1. Origen
No hay, en las fuentes revisadas, una enseñanza primera de Mj que lo nombre «método de rigor» o que defina una por una las tres alarmas. El filtro **sí existe** como pieza de control: el 14 de octubre de 2026 (t773s3719, hora de CDMX) el inventario de la corrida lo listó junto a Copi, Beristáin y falacias, como «falacias y rigor, que son Holmes, Hécate y Schopenhauer (`metodo_rigor`)».

Mj, el 17 de noviembre de 2026, dijo que esas piezas también existen, y que **«Game of Assassin» no le suena a ellas** (en particular, no es Schopenhauer ni el clasificador de falacias). Este documento describe el método de rigor que está en las fuentes; no lo identifica con «Game of Assassin».

La función que se puede afirmar sale del código y del [MAPA_GUARDIANES.md §2.7](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/docs/MAPA_GUARDIANES.md), no de una cita de Mj que fije el diseño.

## 2. Función esencial
Obligar cuatro preguntas de rigor *después* de una lectura o de una apuesta, sin puntuar y sin fusionarse a un motor predictivo:

- **Holmes:** ¿los apoyos son hechos, o la hipótesis ya nombra lo que no debería nombrar (por ejemplo, un apellido en un ejercicio ciego)?
- **Hécate:** ¿se pidió “más de lo mismo”, un letrero que no cambia a lo largo de varios tramos?
- **Schopenhauer:** ¿se defiende el tanteo propio («como yo dije») en lugar de leer el tablero o la evidencia?
- Y si eso sigue en el cuaderno o no.

Son alarmas, no una prueba que cierre el caso.

## 3. Entrada y salida
**Entrada:** el resultado de una lectura o corrida (en el consumidor U6: cadena de top1, hipótesis, texto “inverso” o de defensa) y, cuando exista, la evidencia de hecho que se dice usar.

**Salida:**
- banderas de alarma, si se disparan, con una línea de motivo;
- la plantilla de las cuatro preguntas, aunque el automático no sustituya la lectura humana;
- solo marcas: limpio / marca / error.

**No sale:** una H nueva, un recálculo de puntaje, ni un veredicto.

## 4. Qué no es
- No es «Game of Assassin» (pendiente, no identificado; Mj dijo que no le suena a Schopenhauer ni a falacias).
- No es el clasificador de falacias ni Copi.
- No es el hombre de acero ni el décimo hombre (esos son controles de la apuesta U6, de otro tipo).
- No puntúa, no toca F y no debe fusionarse a Engine V5.
- El automático no sustituye las preguntas humanas del cuaderno (lo declara el propio plugin).

## 5. Consumidores
En el Motor U6, rama `alterno/cameo-pesos`:

- [`plugin_metodo_rigor.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/plugin_metodo_rigor.py) (`PLUGIN_METODO_RIGOR`, bloque `SHERLOCK_RIGOR`)
- Lo envuelve [`guardianes_control_v1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/guardianes_control_v1.py) después del predictor, y hay una llamada previa en laterales como sensor, no como decisor.
- Inventario: [MAPA_GUARDIANES.md §2.7](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/docs/MAPA_GUARDIANES.md)

Declara no tocar F, no puntuar y `can_decide_H=False`. Solo marca.

**Ataduras y defectos de ese cableado:**
- El plugin suelto es muy corto (alarmas literales: letrero idéntico en 4 cortes; hipótesis que contiene fórmulas tipo «se llama» / apellidos de ejemplo; la frase «como yo dije»). El bloque de `guardianes_control` lo extiende con la cadena top1 por corte, tokens de hecho del top1 y masa a favor vs en contra: eso ya está amarrado a U6 (`own_evidence`, tablero).
- Corre sobre la corrida del motor, no como cuaderno agnóstico de cualquier lectura del orquestador.
- El automático, por diseño, no sustituye las cuatro líneas humanas.
- Ese cableado no redefine el método. Sin tocar Engine V5 ni el 244.
