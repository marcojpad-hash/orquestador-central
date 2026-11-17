# Suite de aceptación transversal para guardianes

**Estado:** fixtures de aceptación preparados; todavía no son una implementación ni una ejecución de guardianes.  
**Base documental:** inventario 1.1, commit `736915b1c258c5a878192f72d000570f020d9dd8`, y las especificaciones funcionales enlazadas abajo.  
**Propósito:** disponer de entradas adversariales y resultados exigibles para comprobar el trabajo de cableado de cualquier consumidor, incluido el PR U6 de Grok, sin duplicar ni modificar ese trabajo.

## Alcance y separación

Esta suite pertenece al Orquestador Central. No importa módulos U6, no ejecuta el motor, no modifica Engine V5 ni el catálogo 244, y no genera H, perfiles, puntajes o veredictos.

Especificaciones de referencia:

- [Sombrero blanco](../../docs/filtros_operativos/SOMBRERO_BLANCO.md)
- [Plugin pregunta](../../docs/filtros_operativos/PLUGIN_PREGUNTA.md)
- [Copi](../../docs/filtros_operativos/COPI.md)
- [Falacias](../../docs/filtros_operativos/FALACIAS.md)
- [Beristáin](../../docs/filtros_operativos/BERISTAIN.md)
- [Método de rigor](../../docs/filtros_operativos/METODO_RIGOR.md)
- [Regla de deriva por simplificación](../../docs/filtros_operativos/DERIVA_POR_SIMPLIFICACION.md)

## Qué contiene

`acceptance_cases.json` reúne casos positivos, negativos y adversariales. Cada caso declara:

- entrada exacta;
- guardián/capa que debe responder;
- resultados mínimos exigidos;
- resultados prohibidos;
- propiedad que el caso protege.

Los resultados esperados son criterios semánticos, no cadenas de salida obligatorias. Se acepta redacción equivalente si conserva la función, la traza y los límites del método.

## Reglas transversales de aprobación

1. **Trazabilidad:** cada hecho, ruido o marca debe señalar el fragmento de origen. No se acepta una etiqueta sin traza.
2. **No borrado:** el sombrero blanco conserva hechos y aparta el ruido en un canal separado; nunca elimina la frase completa por una palabra coincidente.
3. **No dependencia léxica:** cambiar la formulación sin cambiar la función no debe hacer desaparecer la marca.
4. **No contaminación:** una metáfora, juicio, falacia o hipótesis no se convierte por sí sola en hecho, rasgo de persona, perfil ni H.
5. **No decisión:** Copi, Falacias, Beristáin, Plugin pregunta y Método de rigor solo clasifican o marcan. Ninguno decide H, puntúa o emite veredicto.
6. **No omisión silenciosa:** pieza ausente, error de importación, excepción o desactivación deben quedar visibles como fallo/no ejecutado. Nunca se presentan como PASS.
7. **Flags auditables:** si un modo operativo permite desactivar una pieza, la salida debe registrar quién/qué la desactivó, el motivo y el estado resultante. Un flag silencioso invalida la corrida.
8. **Método de rigor completo:** Holmes, Hécate y Schopenhauer deben aparecer siempre; cuando no aplique, se registra explícitamente `no`.
9. **No acoplamiento:** la suite no presupone el catálogo 244, top1, F, geometría ni datos internos de U6 para evaluar las funciones transversales.
10. **Regresión anti-deriva:** no se aprueba una versión reducida a frases, conectores, listas cerradas o un único síntoma cuando la especificación exige función/estructura.

## Matriz de cobertura

| Capa | Casos | Núcleo de aceptación |
|---|---|---|
| Sombrero blanco | SB-01 a SB-03 | hechos conservados, ruido tipado, trazas, resistencia a frase fija |
| Plugin pregunta | PP-01 | estructura de pregunta y capas diferenciadas; no responder el contenido |
| Copi | CP-01 y CP-02 | inferencia válida vs afirmación del consecuente; no confundir validez con verdad |
| Falacias | FA-01 y FA-02 | forma marcada aunque cambie la redacción; no declarar falsedad del contenido |
| Beristáin | BE-01 y BE-02 | figura identificada por operación contextual, no por inventario de palabras |
| Método de rigor | MR-01 a MR-03 | Holmes, tercero excluido de Hécate, Schopenhauer; cada marca trazable |
| Integridad de ejecución | OP-01 y OP-02 | fallo visible ante ausencia y desactivación silenciosa |

## Condición de uso en una futura auditoría

Una implementación solo puede declararse **conforme** cuando:

- ejecuta el conjunto completo contra estos fixtures;
- reporta resultado por ID de caso;
- conserva entrada, versión del guardián y trazas;
- demuestra que no se generó H ni se alteró el motor/catálogo;
- publica recibo reproducible y pruebas automatizadas en verde.

Esta carpeta no afirma que nada de lo anterior ya se haya ejecutado. Es la base independiente para hacerlo y para contrastar el PR de Grok cuando exista.
