# Reglas duras — 1 página (leer primero)

Esta página resume las reglas que no se negocian. Lee los documentos completos solo si tu tarea toca ese tema. Contratos completos: `CONTRATO_TRABAJO_MULTI_MODELO.md`, `INSTRUCCION_RUNTIME_TESTBED_PUENTE.md`, `INSTRUCCION_SANDBOX_VM.md`, `REGLAS_OPERATIVAS_UNIVERSALES.md`.

## Verificación
- **Ejecutar, no solo leer.** Código leído no es código ejecutado. Un "PASS" sin ejecutar es "revisión estática, NO ejecutada".
- **Creador ≠ verificador.** Nadie verifica su propio trabajo; lo revisa otro agente o una prueba ejecutada.
- **Fixture ≠ ejecución real.** Un resultado viejo o un ejemplo no prueba que el paso nuevo funcione (frescura: la salida debe ser posterior al inicio de la corrida).
- **Evidencia primero.** Sin ruta, commit, hash o salida ejecutada, no se declara recepción, ejecución, prueba ni publicación.

## Lo protegido (no se toca sin autorización expresa de Mj)
- **Motor U6:** Engine V5 y catálogo 244 son referencia fija, prohibido tocarlos. Nada de motor/runtime a main sin PR y merge de Mj.
- **Archivos canónicos y secretos:** nunca escribir claves, tokens, `.env`, credenciales o cookies en GitHub, prompts, commits ni handoffs. Usar GitHub Secrets.
- **No force-push, no cambiar protección de rama como atajo.**

## Git y main
- Preferir ramas de trabajo y PR. Cambios pequeños y enfocados.
- **Excepción operativa (2026-11-10):** los 4 workflows automatizados de motor-u6-storage (`auditar-corridas-actions`, `fabrica-lote-diario`, `fabrica-real-traza`, `update-mortality-wpp`) empujan a main solo artefactos generados en rutas designadas; nunca tocan Engine, catálogo 244 ni código fuera de manifiestos.

## Bandeja (bus)
- Ciclo completo: PENDIENTE → RECIBIDO (con evidencia) → EN_PROCESO → ENTREGADO → VERIFICADO → resueltos/. No se archiva como resuelto solo por recibir el handoff.
- Si algo no está cubierto por las reglas, se marca como hueco de contrato, no se inventa una regla nueva.

## Mj (Marco)
- **Mj no cablea nada.** Él da indicaciones; los modelos ejecutan. No pedirle que autorice, suba, confirme o revise cada paso. Solo interviene para una contraseña/confirmación imprescindible o cuando él detecta un error.
- **Nada con dinero.** Solo niveles gratuitos. Un patrocinio es recibir dinero: decidirlo con Mj antes de aceptar nada.
- **El sistema no depende de que Mj esté despierto.** De noche, solo trabajo que no lo necesita.

## Costo
- Cero gasto sin visto bueno de Mj. Reportar costo y esperar aprobación. Preferir herramientas deterministas + modelos locales/gratuitos.
- No lanzar agentes ni lecturas masivas si bastan unas pocas comprobaciones.
