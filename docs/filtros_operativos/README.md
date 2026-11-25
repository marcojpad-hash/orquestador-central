# Filtros operativos transversales
**Versión:** 1.2  
**Tipo:** índice de métodos de trabajo del orquestador.  
**Alcance:** cualquier input humano y cualquier frente. No son el Motor U6, ni geometría, ni política, ni los controles especializados de ese motor (Z90, sello, filtro 017, catálogo 244, StinkBox), documentados en [`../CONTROLES_MOTOR_U6.md`](../CONTROLES_MOTOR_U6.md). Tampoco sustituyen a los [guardianes operativos agnósticos](../GUARDIANES_OPERATIVOS_AGNOSTICOS.md) (runner, cola, watchdog, sandbox).

Son lentes de lectura y admisión: lógica, retórica y separación de hecho y ruido. Ninguno decide H ni emite veredicto. Si un proyecto los cablea (hoy, el Motor U6), ese cableado es un **consumidor**, no la definición del método.

Las especificaciones de este apartado no afirman que exista ya un ejecutor automático transversal. Donde hay código, se declara en «Consumidores».

La implementación de estos filtros está sujeta a la regla de [deriva por simplificación](DERIVA_POR_SIMPLIFICACION.md): recortar la función original porque «parece más eficiente» es fallo, no un atajo válido. Antes de dar por buena una pieza, hay que confrontarla con los checkpoints anteriores.

## Filtros con especificación

| Filtro | Función en una línea | Spec |
|---|---|---|
| Sombrero blanco | Admite lo objetivamente medible; anota el juicio y el adorno como ruido. | [SOMBRERO_BLANCO.md](SOMBRERO_BLANCO.md) |
| Copi | Revisa consistencia lógica (inferencia, reemplazo, falacias espejo). | [COPI.md](COPI.md) |
| Falacias | Marca formas falaces en la pregunta o el texto, sin resolver el fondo. | [FALACIAS.md](FALACIAS.md) |
| Beristáin | Detecta tropos y figuras para que lo figurado no se lea como hecho. | [BERISTAIN.md](BERISTAIN.md) |
| Plugin pregunta | Clasifica la estructura de la pregunta antes de usarla como evidencia. | [PLUGIN_PREGUNTA.md](PLUGIN_PREGUNTA.md) |
| Método de rigor | Alarmas de rigor de lectura (Holmes, Hécate, Schopenhauer). | [METODO_RIGOR.md](METODO_RIGOR.md) |
| Contexto enunciativo | Registra juicios, orientación valorativa y patrones discursivos; aporta contexto a otros controles sin emitir veredictos. | [ORIENTACION_ENUNCIATIVA.md](ORIENTACION_ENUNCIATIVA.md) |

Mj confirmó (17 de noviembre de 2026, hora de CDMX) que en su dictado «copy» es Copi y «Very Stein» es Beristáin.

## Regla de implementación

[Deriva por simplificación](DERIVA_POR_SIMPLIFICACION.md). No es un filtro más de este índice: es la regla que obliga a no dar por cableada una pieza si, al simplificarla, perdió o cambió su función original sin decisión explícita de Mj.

## Inventario del cableado

El cableado real en el consumidor Motor U6 (qué detectan, si bloquean o solo marcan, si se pueden saltar, veredicto FIEL / DEGRADADA / CAMBIÓ DE FUNCIÓN; y, en la sección de adicionales, NO CABLEADA) está en [INVENTARIO_GUARDIANES_PROTOCOLO.md](INVENTARIO_GUARDIANES_PROTOCOLO.md). Ese inventario no redefine los métodos: confronta el código con estas specs. Incluye piezas hermanas que no tienen ficha propia aquí (pregunta detrás v2, sesgo de lectura, polaridad, autoevidencia, filtro 017, relleno 013) y una sección de piezas adicionales y mal cableadas (CEB, Z90, candados, consulta dirigida, verificador de salida, traducción 021, deriva, trazabilidad temporal).

## Pendiente, sin especificación

- **Game of Assassin.** Aparece en el dictado de Mj (t1258u, 2026-11-17 02:44, hora de CDMX) junto a los filtros de lógica y retórica. No está identificado en las fuentes. Mj confirmó que **no** es el clasificador de falacias ni Schopenhauer; dijo que no le suena a esos, aunque esos también existen. No se asume Ockham, Gödel ni ningún otro nombre. Queda pendiente de que ella lo nombre con claridad. No hay spec.

## Qué no se especifica aquí

- **Popper** (falsabilidad) y **Wittgenstein**: no hay definición de Mj en las fuentes. No se crean specs.
- Los controles del Motor U6 (Z90, hash, 017, 244, StinkBox, candados de corrida): van en [`../CONTROLES_MOTOR_U6.md`](../CONTROLES_MOTOR_U6.md).
