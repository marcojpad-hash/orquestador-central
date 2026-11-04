# Registro de ejecución — MVP 0.1

Fecha: 2026-10-31
Rama: feature/core-mvp-l1
PR: https://github.com/marcojpad-hash/orquestador-central/pull/1

## Ejecutado

- Añadido `runtime/server.py`: servidor HTTP basado en biblioteca estándar, autenticación Bearer obligatoria para rutas privadas, SQLite, recepción de instrucciones, clave idempotente, creación de tarea, reclamación transaccional y recepción de resultados.
- Añadido `tests/test_server.py`: pruebas de creación de instrucción/tarea, deduplicación y rechazo de prioridad inválida.
- Añadida documentación de ejecución y endpoints en `runtime/README.md`.
- Añadida workflow `.github/workflows/core-tests.yml` para Python 3.12.
- Abierto PR draft #1 para revisión aislada; no se fusionó a main.

## Evidencia

- Commits de archivos: 2a7aca5780d1769fb5994799104c41220e764150; 4477a99fcdc36e11707a3baebdf483932d4ff30a; adaff7db63d62fbf39df5de0a389dac89e5bb97d; 19ec21a10075879a8ae46dc594d7d8849aa16fd1; 972751a10204884d1702171787648f56744b154b.
- PR: https://github.com/marcojpad-hash/orquestador-central/pull/1
- El conector no devolvió ejecuciones de Actions asociadas al SHA del PR en la consulta realizada. Por tanto, CI aún no está certificado como verde y no se declara que las pruebas hayan pasado.

## Seguridad y límites

- Servicio escucha en 127.0.0.1 por defecto; no se desplegó ni publicó.
- El secreto se lee de variable de entorno; no se guardó ningún secreto en Git.
- No se conectaron modelos, canales externos ni repositorios de Motor U6/CAPCOT.
- La API es un MVP de un solo propietario, no un servicio endurecido para Internet.
- La rama y PR permanecen separados de main para evitar integrar código sin ejecución de pruebas confirmada.

## Siguiente ejecución técnica

1. Ejecutar la workflow en un contexto permitido por GitHub Actions y corregir cualquier fallo observado.
2. Añadir pruebas HTTP de autenticación, cola y resultado.
3. Incorporar migraciones, expiración/recuperación de tareas atascadas y control de tamaño/validación más estrictos.
4. Desplegar solo tras configurar secret manager, HTTPS, persistencia, backups y aprobación de infraestructura.
