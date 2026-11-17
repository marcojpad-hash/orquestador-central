# Controles especializados del Motor U6
**Versión:** 1.0  
**Tipo:** mapa de controles propios del Motor U6, registrado en el orquestador para no confundirlos con los métodos transversales.  
**Autoridad de implementación:** el repositorio del proyecto, `marcojpad-hash/motor-u6-storage`. Este documento no modifica el motor, no toca Engine V5 ni el catálogo 244, y no generaliza estos controles a otros frentes.  
**No es el sombrero blanco.** El sombrero blanco es un método transversal del orquestador ([`SOMBRERO_BLANCO.md`](SOMBRERO_BLANCO.md)), válido para cualquier input humano. Los controles de esta página son del motor predictivo U6.

La [arquitectura del coordinador](ARQUITECTURA_COORDINADOR_CENTRAL.md) y los [guardianes operativos agnósticos](GUARDIANES_OPERATIVOS_AGNOSTICOS.md) ya distinguen controles universales de controles especializados de un dominio. Aquí se enumeran estos últimos para el Motor U6.

## 1. Guardián de la Z90
En modo predictivo no debe entrar ningún corte posterior a la Z90. El motor no ve el caso completo: solo lo anterior al corte. Las fechas que sirven para vigilar esa ventana viven en el **sobre** del caso, no como contenido que el predictor use para perfilar. Un caso que intente meter datos post-Z en modo predictivo debe rechazarse (en la rama vigente, el código de salida previsto para ese rechazo es 8).

Este control no es el sombrero blanco: no decide qué es hecho o juicio; decide qué ventana temporal puede verse.

## 2. Hash / sello del freeze
Toda corrida que se declare sellada lleva un hash del freeze. El sello no se quita ni se reescribe para acomodar un resultado. Sirve de candado anti post-hoc: primero se sella, después se revela o se juzga HIT/PARCIAL/REFUTA, sin alterar lo congelado.

## 3. Filtro 017 y veto de nombres, años y fechas en el contenido
El contenido que entra al tubo va anónimo: no deben colarse nombres, años ni fechas en los cortes que el predictor lee. Las fechas de control de la ventana permanecen en el sobre (véase §1).

Este veto es una precisión de diseño del motor, no una regla del sombrero blanco. En la plática que definió el sombrero, una fecha podía anotarse si estaba en el texto y no era inventada. Aquí se aparta del contenido precisamente para no dar pistas de identidad ni de desenlace.

## 4. Catálogo 244 cerrado y tokens fuera de catálogo a StinkBox
El catálogo de 244 patrones (`patterns_final_v14.json`) no se edita en este trabajo. Un token que no pertenece al vocabulario del catálogo no entra a canon ni decide H; se reporta y se estaciona en StinkBox para revisión posterior.

## 5. PROTOCOL_NOISE_RE y campos probabilísticos prohibidos
En el cableado actual del motor, una regex de ruido de protocolo y un conjunto de campos prohibidos (`probability`, `probabilidad`, `weight`, `peso`, `confidence`, `confianza`, `prob`, etc.) evitan que metadatos de armado o cifras de confianza se cuelen como hecho o como voto.

Esto es higiene del tubo, no la función del sombrero blanco. Además, en la implementación cableada la regex incluye la cadena «sombrero blanco», lo cual es un defecto respecto del método transversal: se documenta en [`SOMBRERO_BLANCO.md`](SOMBRERO_BLANCO.md#7-estado-de-la-implementación-cableada-actual).

## 6. No tocar Engine V5 ni el catálogo 244
Quedan protegidos, entre otros, `Engine_V5_CANONICO_SOLO.py` / la línea `MOTOR_V15_3_UNICO_*` y `patterns_final_v14.json`. No se alteran H, pesos, catálogo ni contratos predictivos desde el orquestador ni desde un “arreglo” de sombrero blanco. Una propuesta de cambio canónico se detiene y se eleva a Mj.

## 7. Candados de corrida
Sin pretender un inventario exhaustivo del runtime, quedan como candados propios del motor, no del sombrero:

- No ajustar el protocolo ni el umbral Z a mitad de una corrida ya iniciada.
- No declarar HIT, cierre o “ya quedó” sin evidencia del proceso (log, sello, recibo). Un cambio de umbral o de cortes a medio vuelo contamina la corrida.
- No fingir que H1 es simplemente el Top-1 del tablero cuando el contrato de la corrida lo prohíbe.
- No absorber, a mitad de vuelo, ruido de protocolo (fechas o títulos metidos después, re-cortes, revelaciones del ciego).
- El autor del input no es el sujeto del caso ciego; revelar identidad o post-Z antes de tiempo invalida el ejercicio.
- Fixture no equivale a ejecución real del componente.

## 8. Relación con el sombrero blanco
Pueden usarse en la misma corrida, en capas distintas:

1. El sombrero blanco (método del orquestador) admite hechos observables y anota el ruido de cualquier input, incluido el que después se traduzca a cortes.
2. Estos controles del motor vigilan ventana, sello, anonimato, catálogo e integridad de la corrida.

Ninguno sustituye al otro. Un fallo de Z90, de sello o de 017 no se “arregla” con el sombrero; un juicio colado como hecho no se “arregla” con el guardián de la Z.
