# Sombrero blanco
**Versión:** 1.1  
**Tipo:** método de trabajo y control operativo transversal del orquestador.  
**Alcance:** cualquier input humano y cualquier frente (pregunta, relato, biografía, orden, auditoría, handoff). No pertenece a un proyecto ni al Motor U6. U6 es solo un consumidor más; su cableado actual se describe al final, no define el método.  
**No es:** una herramienta del motor, un diccionario de palabras, un perfilador, un productor de veredictos o H, ni una copia de los controles especializados de U6 (Z90, sello, filtro 017, catálogo 244, StinkBox). Esos controles viven en [`../CONTROLES_MOTOR_U6.md`](../CONTROLES_MOTOR_U6.md).

## 1. Qué es
El sombrero blanco es la lente de admisión del input: se queda con lo objetivamente medible y visible, y aparta el adorno, el juicio y la etiqueta. El ruido se puede anotar; no entra como hecho y no produce veredicto.

Fuente de la función: plática de Mj con Puta 3 el **14 de septiembre de 2026** (hora de CDMX), sesión `56d9fab0-f92f-4850-a04b-6f55ff03e508`. La primera enseñanza es **t204u, 01:54**. La página de Notion [SOMBRERO BLANCO + plugin pregunta](https://app.notion.com/p/3e152e5cb10c8105b38be389515ebd17) es un recuento del 19–20 de septiembre, no la fuente original.

En varios mensajes de esa misma mañana (t292u, t293u, t299u) Mj introduce el texto en voz oral y a continuación avala un bloque más pulido, casi seguro pegado de otro modelo. Esas formulaciones se citan como material que ella le enseñó al orquestador ese día, no como transcripción de su habla literal en cada oración.

Este documento forma parte de los [filtros operativos transversales](README.md).

## ESPECIFICACIÓN FUNCIONAL A CABLEAR (objetivo)

Esta es la función que debe cablearse. La referencia no es ninguna pieza actual del Motor U6.

### Referencia

La versión manual del **14 de septiembre de 2026** (hora de CDMX): ejercicio *El niño proletario* (Lamborghini), `FILTRO_TRAZA_BRUTO`, mensajes **t350u–t353u**. Ítems 01–06 son hechos; 07–10 son lecturas forzadas. Esa es la función. Ninguna versión cableada la implementó.

### Lo que debe hacer

Por cada frase del input:

1. **Partirla en unidades observables:** QUIÉN (actor) / QUÉ (acción) / DÓNDE / EN QUÉ ORDEN (secuencia) / relación observable.
2. **Apartar como ruido tipado:** juicio (moral o estético), adjetivo valorativo, metáfora o figura (lente [Beristáin](BERISTAIN.md)), etiqueta de género o escuela, intención atribuida, conclusión disfrazada de dato (lente [Copi](COPI.md)). Lo que dice un personaje se registra como *dicho*, no como hecho del mundo. **Esta última regla es del bot (11 de noviembre de 2026, hora de CDMX), no de Mj.**
3. **Trazar** cada unidad al fragmento exacto del texto fuente (offset o cita literal).
4. **No borrar el ruido:** anotarlo aparte. El ruido nunca alimenta H ni apuesta.
5. **No decidir veredicto.**

Formato de salida mínimo:

```json
{
  "hechos": [
    {"unidad": "niño", "clase": "quién (actor)", "traza": "el niño"},
    {"unidad": "sombrero", "clase": "qué (objeto)", "traza": "el sombrero"}
  ],
  "ruido": [
    {"fragmento": "cruel", "tipo": "juicio moral", "traza": "era cruel"},
    {"fragmento": "muy bonito", "tipo": "juicio estético", "traza": "estaba muy bonito"}
  ]
}
```

Ejemplo: el input «el niño era cruel y el sombrero estaba muy bonito» produce esos dos hechos (niño = actor, sombrero = objeto) y esos dos ruidos (cruel = juicio moral; muy bonito = juicio estético).

### Criterios de aceptación / tests

- La frase «el niño era cruel y el sombrero estaba muy bonito» debe producir dos ruidos tipados (juicio moral y juicio estético), sin perder los dos hechos.
- Un texto que diga literalmente «juicio estético» no debe tirarse entero por coincidir con una cadena fija.
- Cada hecho lleva traza al fragmento fuente.
- El `FILTRO_TRAZA_BRUTO` de Lamborghini (hechos 01–06 frente a lecturas forzadas 07–10) se reproduce como caso de prueba: misma separación, misma trazabilidad.

### Versión actual vs debe hacer

| | 27-sep-2026 (`_protocol_quality` en [`MOTOR_V15_3_UNICO_20260927.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/MOTOR_V15_3_UNICO_20260927.py)) | Parche 010a, 6-oct-2026 ([`sidecar_sombrero_blanco_filtro_v1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/sidecar_sombrero_blanco_filtro_v1.py)) | Debe hacer |
|---|---|---|---|
| Unidad de trabajo | Lista de 5 frases, solo sobre la pregunta. De los cortes solo cuenta tokens (longitud de P/A/C). | La misma lista de 5 frases, también sobre textos de corte. Si coincide, tira el texto entero. | Parte cada frase en QUIÉN / QUÉ / DÓNDE / EN QUÉ ORDEN / relación observable. |
| Juicio, adjetivo, figura | No los aparta. | No los aparta. | Los aparta como ruido tipado (lentes Beristáin y Copi). |
| Traza al fragmento fuente | No. | No. | Obligatorio (offset o cita literal). |
| Ruido anotado | `PROTOCOL_NOISE_RE` sobre la pregunta (incluye la cadena «sombrero blanco»). | La misma lista; «sombrero blanco» sigue en su propia lista de ruido. Excluye notas de armado. Reporta tokens fuera de catálogo. Revisa la salida. | El nombre del método no es ruido. El ruido se anota aparte; no se borra ni se usa para tirar el texto entero. Fuera de catálogo y notas de armado no son esta función. |
| Sello de cumplimiento | Escribe `ENFORCED` y `facts_only_boundary=True` fijos, sin revisar. | Quitó el aprobado fijo. `can_decide_H=False`. | No decide veredicto. No declara cumplimiento si no hace lo de arriba. |
| ¿Cumple esta spec? | No. | No. | — |

Ninguna de las dos versiones parte frases, aparta juicio/adjetivo/figura ni traza cada unidad al texto fuente.

### Estado

**NO CABLEADO.** La implementación U6 actual no cumple esta especificación. Cualquier consumidor que diga «sombrero blanco aplicado» sin cumplir lo exigido en «Lo que debe hacer» y en «Criterios de aceptación» es falso.

## 2. Lugar en el gobierno del orquestador
- Complementa la [separación epistemológica](../REGLAS_OPERATIVAS_UNIVERSALES.md) (OBSERVADO / INFERIDO / PROPUESTO, etc.): el sombrero decide qué puede siquiera presentarse como hecho del input, antes de etiquetar afirmaciones de trabajo.
- No sustituye a los [guardianes operativos agnósticos](../GUARDIANES_OPERATIVOS_AGNOSTICOS.md) (runner, cola, watchdog, sandbox). Es un control de admisión y lectura, no de ejecución.
- No sustituye el [contrato de interacción con Mj](../COMO_TRABAJAR_CON_MJ.md).
- Los controles del Motor U6 son de otro tipo y no se mezclan con este método.

## 3. Principios

### 3.1 Solo entra lo objetivamente medible; el juicio es ruido
> «la idea sería poder ver […] objetivamente la situación. […] es el equivalente a decir, “Ay, mira qué bonito color blanco en el sombrero”. No, ahí tú tendrías que reconocer, a ver, ¿qué es lo que […] objetivamente medible? Sombrero blanco. Eso es a lo que me refiero a ese tipo de cosas.»  
> — Mj, t204u, 2026-09-14 01:54 (hora de CDMX)

> «mi modelo lo estoy entrenando para que si yo le digo, el sombrero blanco está muy bonito, el modelo diga ok, dato, sombrero, color blanco, tan tan, lo otro es ruido.»  
> — Mj, t348u, 2026-09-14 10:52 (hora de CDMX)

### 3.2 Es un filtro de admisión, no perfilamiento
> «es la identificación objetiva dentro de el input […]. Eso ni siquiera sería […] una parte del perfilamiento per se, sería tal cual un filtro.»  
> — Mj, t205u, 2026-09-14 01:57 (hora de CDMX)

Si hay marcajes, son banderas (highlight), no luces de un tablero ni levantamiento de tokens.

### 3.3 No es un diccionario: mira la función, no el lexema
> «Se nos quita muchísimo ruido y nos hace un diccionario que no tiene que ser un diccionario. Nada más tiene que ser un especie de protocolo que le siga.»  
> — Mj, t207u, 2026-09-14 02:01 (hora de CDMX)

Un diccionario «siempre se encuentra la forma de cómo saltárselo» (Mj, t204u). En el texto que ella avala en t201u: «La unidad de control no es la palabra: es la función que está cumpliendo dentro de la pregunta.»

### 3.4 Primero se registra lo que se ve; la estructura sale después
Texto que Mj le pasa al bot en t299u («Ira igual esto te ayuda»), 2026-09-14 08:04 (hora de CDMX):

> «No necesitas empezar preguntando: “¿Esto es melodrama?” Empiezas con: ¿Qué ocurrió? FECHA LUGAR ACTOR/ENTIDAD ACCIÓN SECUENCIA RELACIÓN CON OTROS HECHOS»

> «No clasificar primero para después buscar los hechos. Extraer los hechos primero para descubrir qué estructura los organiza.»

> «Registrar lo que se ve; dejar que la estructura observada determine qué se activa.»

El género, la alegoría o la etiqueta no se imponen a la entrada. Si aparecen, aparecen al final como consecuencia de los hechos. Una fecha solo entra si está en el texto y es observable; inventarla no es sombrero blanco. El veto posterior de años en el contenido del Motor U6 es un control de ese motor, no de este método.

### 3.5 Cada elemento debe poder regresarse a su fuente en el texto
> «si el filtro puede demostrar de dónde sacó cada elemento. […] Si puede hacer ese regreso sin meter la interpretación crítica, ahí sí estamos viendo el filtro funcionando como queríamos.»  
> — Mj, t352u, 2026-09-14 11:01 (hora de CDMX)

### 3.6 Hecho de campo no es etiqueta de perfil sobre el sujeto
«La ambición aparece durante su etapa empresarial» puede ser un fenómeno en una ventana; «¿Es un ambicioso?» ya perfila (texto avalado en t201u). Mj, t206u: el filtro no debe contestar «sí, a huevo ese güey era un culero». Marca cómo viene armada la pregunta; no emite el veredicto.

### 3.7 El ruido se anota aparte; no alimenta el veredicto
En el ejercicio de *El niño proletario* (t350u–t351u, 10:56–10:57, hora de CDMX) Mj pide irse a los hechos aunque el texto «tiene mucho ruido», y que el filtro demuestre la fuente sin interpretación crítica (t352u). El listado bruto pedido en t353u (el bot lo nombró `FILTRO_TRAZA_BRUTO` en t353s0) trata alegoría política, juicio estético, autobiografía autor=narrador y etiqueta de «vanguardia» como lectura, no como hecho, salvo que el texto lo diga explícito.

### 3.8 Trazabilidad no es lo mismo que sesgo
Texto avalado por Mj en t292u, 2026-09-14 07:48 (hora de CDMX):

- Sesgo: «Esta característica está inclinando el resultado.»
- Trazabilidad: «Puedo señalar qué elemento del input produjo esta clasificación y qué naturaleza lingüística tenía.»

La segunda es auditable. Por eso el listado bruto de t353u: ver si el sesgo es de quien pregunta o de la lectura.

### 3.9 El plugin de pregunta es hermano, no el sombrero mismo
Misión, en t292u: «Clasificar la estructura de la pregunta antes de interpretar su contenido como evidencia.»

Cadena: `INPUT → qué está preguntando → unidades lingüísticas objetivables → valoración/adjetivización → estructura narrativa → ruido retórico/lógico → qué puede trazarse → PERFIL` (solo banderas).

Prohibido: `INPUT → palabras fuertes → patrón → perfil`. Tropos y falacias son instrumentos de lectura, no patrones de un catálogo predictivo.

## 4. Entrada y salida esperadas

**Entrada:** cualquier texto o pregunta humana, sin presuponer dominio, motor ni catálogo.

**Salida:**
1. **Hechos admitidos**, cada uno en unidades observables: quién / qué / dónde / en qué orden / qué relación se ve. Si el texto trae una fecha, puede anotarse como hecho del texto, no como dato inventado. Cada hecho lleva su **trazo** (cita, fragmento o localizador del texto de origen).
2. **Ruido anotado aparte**, con tipo: juicio, adjetivo valorativo, alegoría, intención atribuida, etiqueta de género, figura retórica u otro adorno. El ruido no se borra del expediente; no se usa como hecho ni como veredicto.
3. **Banderas** de cómo viene armada la pregunta o el enunciado (por ejemplo, perfilamiento del sujeto, valoración previa, marco sesgado). Son highlight, no decisión.
4. **Nunca** un veredicto, una H, un perfil concluyente ni un género impuesto a la entrada.

## 5. Lo que no es (y lo que no se le atribuye a Mj)
- No es un diccionario de frases ni una regex de palabras prohibidas.
- No es perfilamiento ni levantamiento de familia, token o hipótesis.
- No es productor de H ni de apuestas.
- **«Solo lo filmable»** no lo dijo Mj. Es una paráfrasis posterior del bot (t411s0, 2026-09-19 22:59, hora de CDMX) de «objetivamente medible» (t204u) y «Registrar lo que se ve» (t299u).
- **De Bono / «sombreros de pensar» / «white hat»:** no aparecen en esa plática. No se le atribuyen a Mj.
- **«Lo que dicen los actores se registra, pero no como hecho del mundo»** aparece el 11 de noviembre de 2026 en un análisis del bot, no en la enseñanza del 14 de septiembre. No forma parte de esta especificación como principio de origen.
- No es el guardián de la Z90, el sello del freeze, el filtro 017, el cierre del catálogo 244 ni StinkBox. Eso es del Motor U6: [`../CONTROLES_MOTOR_U6.md`](../CONTROLES_MOTOR_U6.md).

## 6. Ejemplo mínimo
Input: «el sombrero blanco está muy bonito».

| Unidad | Clase | Trazo |
|---|---|---|
| sombrero | hecho (qué / objeto) | «sombrero» en el input |
| color blanco | hecho (cualidad observable) | «blanco» en el input |
| «muy bonito» | ruido: juicio estético | «está muy bonito» en el input |

No entra como hecho que el sombrero «esté bonito». No hay veredicto, perfil ni H.

## 7. Estado de la implementación cableada actual
La especificación a cablear, los tests y la comparación 27-sep / 010a están en [ESPECIFICACIÓN FUNCIONAL A CABLEAR](#especificación-funcional-a-cablear-objetivo). Este método, en el orquestador, es una especificación de trabajo. No se afirma aquí que exista un ejecutor automático transversal que lo cumpla.

Un consumidor posterior es el **Motor U6**, en la rama `alterno/cameo-pesos` de `marcojpad-hash/motor-u6-storage`. Ahí el nombre quedó cableado a piezas de higiene de protocolo y de catálogo, no a esta función:

- [`sidecar_sombrero_blanco_filtro_v1.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/sidecar_sombrero_blanco_filtro_v1.py) (PATCH 010a)
- [`plugin_sombrero_blanco_token.py`](https://github.com/marcojpad-hash/motor-u6-storage/blob/alterno/cameo-pesos/motor/motor/plugin_sombrero_blanco_token.py)

**Qué conservó de la plática:** el rol declarado de no alimentar al predictor (`feeds_predictor=False`, `can_decide_H=False`), acorde con «es un filtro, no perfilamiento».

**Qué se perdió o deformó:**
- No parte el texto en quién / qué / dónde / orden / relación observable.
- No distingue hecho de juicio, adjetivo, alegoría, intención ni etiqueta de género, salvo que coincida con unas pocas cadenas fijas.
- No examina la función del lexema (campo vs etiqueta de perfil).
- No exige trazabilidad («de dónde salió cada elemento»).
- No anota el ruido aparte para que no alimente H: casi no clasifica ese ruido.
- El plugin de token solo estaciona hallazgos fuera del catálogo 244 en StinkBox; no implementa el sombrero.
- Defecto grave: `PROTOCOL_NOISE_RE` incluye la cadena **«sombrero blanco»**, de modo que el propio nombre del método queda tratado como ruido de protocolo.
- Al reducirse a un diccionario de frases, hace lo que Mj rechazó en t204u y t207u: algo que se puede saltar reformulando.

Ese cableado no redefine el método. Corregirlo, si se hace, pertenece al repositorio del motor, sin tocar Engine V5 ni el catálogo 244, y sin hacer de este documento un parche de U6.

## 8. Lentes de apoyo (no diccionario)
El sombrero blanco no carga un diccionario de palabras prohibidas. Para ver la **función** de cada palabra o frase (hecho vs juicio, literal vs figurado), se apoya en dos lentes hermanas de este apartado:

- **[Beristáin](BERISTAIN.md)** aporta el catálogo para reconocer lo figurado (metáfora, hipérbole, lítote, etc.) y apartarlo como ruido, en vez de leerlo como hecho.
- **[Copi](COPI.md)** aporta cómo detectar cuándo una frase mete una conclusión o un juicio disfrazado de dato (falacias, inferencias).

Se usan como lentes, no como listas de palabras que se puedan saltar reformulando (t204u, t207u, t278u).

**Gómez de Silva queda fuera**, por decisión de Mj (17 de noviembre de 2026, hora de CDMX): con Beristáin basta. No se integra a este filtro.
