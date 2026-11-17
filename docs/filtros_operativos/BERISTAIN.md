# Beristáin
**Versión:** 1.0  
**Tipo:** filtro operativo transversal de retórica (tropos y figuras).  
**Alcance:** cualquier texto o pregunta donde lo figurado pueda colarse como hecho o como perfil. No pertenece al Motor U6; U6 es un consumidor.  
**Nunca decide H ni emite veredicto.**

Índice del apartado: [`README.md`](README.md).

## 1. Origen
Mj lo señaló el **14 de septiembre de 2026**, 06:41 (hora de CDMX), t266u, sesión `56d9fab0-f92f-4850-a04b-6f55ff03e508`:

> «Es el de helena Beristain checa ese y afines»

A las 07:14, t278u, corrigió el modo de integrarlo:

> «Yo no le diría “mete todos los tropos”, porque eso fue precisamente lo que Claudia interpretó de manera demasiado literal y terminó haciendo una lista pequeña.»

Pidió una especificación de arquitectura para tropos dentro del plugin de la pregunta, no un inventario corto metido a martillazos. A las 07:48, t291u: «A ver Beristain Copi y falacias».

El 14 de octubre (t773u) lo dictó como «Bernstein». El 17 de noviembre de 2026 confirmó que «Very Stein» es Beristáin (distorsión fonética del dictado).

Fuente teórica que usó el consumidor U6: Helena Beristáin, *Diccionario de retórica y poética* (OCR 1995), declarada en el propio módulo.

En t292u / t293u (textos que ella avaló): los tropos son una capa que pregunta si la expresión funciona literalmente o mediante una operación retórica; no son patrones nuevos del 244. Cada capa puede corregir a la anterior.

## 2. Función esencial
Reconocer cuándo el lenguaje está operando como figura (metáfora, metonimia, lítote, hipérbole, etc.) para que esa operación no se lea como hecho filmable, como atributo del sujeto o como evidencia de perfil. La figura se anota; no se borra, y no se traduce sola en un rasgo del mundo ni en una H.

## 3. Entrada y salida
**Entrada:** un texto o una pregunta, en unidades señalables.

**Salida:**
- figuras detectadas, con familia o tipo (por ejemplo, metasemema vs metalogismo), definición breve y trazo al fragmento;
- indicación de si la figura está empujando una lectura literal, un perfil o un sesgo de la pregunta;
- solo banderas: limpio / marca / error.

**No sale:** un género impuesto («esto es sátira, luego…»), un veredicto, ni una H.

## 4. Qué no es
- No es «meter todos los tropos» en una lista cerrada que se pueda burlar con otra formulación (t278u).
- No es Copi ni el clasificador de falacias: una figura no es, por sí sola, un paso inválido.
- No es el sombrero blanco, aunque lo complementa: el sombrero aparta el juicio; Beristáin explica cuando el juicio o el “hecho” llega disfrazado de tropo.
- No es un patrón del 244 ni un productor de apuestas.
- No declara la “intención del autor”. Declara una operación lingüística observable en el texto.

## 5. Consumidores
En el Motor U6, rama `alterno/cameo-pesos`:

- [`guardian_tropos_beristain_v1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/guardian_tropos_beristain_v1.py)
- Lo corre [`guardianes_control_v1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/guardianes_control_v1.py) al final del paquete, y se corrige con los vecinos lógicos (falacias, Copi).
- Inventario: [MAPA_GUARDIANES.md](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/docs/MAPA_GUARDIANES.md)

Candados declarados en el módulo: `can_decide_H=False`; no escribe H ni `patterns`; no reordena candidatos. Función declarada: «impedir que lenguaje figurado se lea literal como evidencia/perfil».

**Ataduras y defectos de ese cableado:**
- Está amarrado a la corrida U6 (textos del caso, post-predictor). No es un filtro previo y agnóstico del orquestador.
- El catálogo del archivo es un inventario de figuras con códigos de implementación; hay que no recaer en la lista corta que Mj rechazó en t278u, ni tratar el catálogo como el método entero.
- Solo marca. El MAPA lo describe como siempre en marcha dentro de `correr_guardianes`, sin detener la corrida.
- Hay también tropos estructurales (lítote, hipérbole) en [`plugin_pregunta_detras_v2.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/plugin_pregunta_detras_v2.py); son el mismo frente retórico, no un segundo método.
- Ese cableado no redefine el método. Sin tocar Engine V5 ni el 244.
