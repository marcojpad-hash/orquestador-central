# Hoja de ruta de implementación

## Fase 0 — Contrato y gobierno (hecho en esta entrega)
- Identidad, autoridad y autonomía inicial.
- Arquitectura desacoplada de proveedores.
- Protocolo universal de instrucciones.
- Contrato de agentes y resultados.
- Modelo de datos y registros iniciales.
- Mapa de proyectos conocido.

## Fase 1 — Núcleo mínimo ejecutable
- Implementar API autenticada.
- Implementar almacenamiento transaccional y cola.
- Implementar registro, deduplicación y estados.
- Implementar consola web móvil en español.
- Implementar entrada manual universal y entrada GitHub.
- Añadir pruebas automatizadas y despliegue.

## Fase 2 — GitHub como primer adaptador operativo
- Crear GitHub App propia.
- Instalarla solo en repositorios seleccionados.
- Permisos mínimos: metadata read, contents read/write según alcance, issues read/write, pull requests read/write solo donde se autorice.
- Escanear repositorios instalados y registrar rutas protegidas.
- Abrir tareas, preparar ramas y producir PRs verificables.

## Fase 3 — Primer modelo y primer especialista
- Integrar un proveedor de LLM mediante API.
- Enrutar una tarea simple de extremo a extremo.
- Registrar tokens/coste/latencia cuando estén disponibles.
- Validar salidas con esquema y pruebas.
- Mantener fallback manual si el proveedor falla.

## Fase 4 — Canales externos
- Integrar Grok, Claude, Gemini, ChatGPT y Meta según interfaces oficiales disponibles.
- Añadir retorno de respuesta al canal de origen cuando la API lo permita.
- Probar autenticación de propietario y deduplicación entre canales.
- Documentar limitaciones específicas por proveedor.

## Fase 5 — Memoria y supervisión multiagente
- Recuperación de contexto por proyecto.
- Delegación paralela y dependencias.
- Revisión independiente de entregables.
- Detección de conflictos y decisiones obsoletas.
- Tablero global.

## Fase 6 — Autoactualización controlada
- Descubrimiento de repositorios y capacidades dentro del alcance autorizado.
- Actualización de catálogo de agentes y conectores.
- Evaluación de salud y rendimiento.
- Propuestas automáticas de cambios al propio sistema.
- Pruebas en rama aislada y rollback.
- Promoción de autonomía solo con aprobación del propietario.

## Criterio de salida de cada fase

Una fase se declara completada únicamente con código desplegado, prueba ejecutada, evidencia registrada y documentación actualizada. La creación de documentos de diseño no equivale a implementación ejecutable.
