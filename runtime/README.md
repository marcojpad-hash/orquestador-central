# Núcleo ejecutable — MVP 0.1

Servicio HTTP mínimo construido con la biblioteca estándar de Python. Incluye autenticación Bearer, SQLite persistente, registro de instrucciones, deduplicación por clave idempotente, cola básica de tareas, reclamación de tareas, recepción de resultados y auditoría.

## Ejecutar

Requiere Python 3.10 o posterior. Desde la raíz del repositorio:

```sh
export ORCHESTRATOR_OWNER_TOKEN='genera-un-secreto-largo-y-unico'
export ORCHESTRATOR_DB='./data/orchestrator.sqlite3'
python runtime/server.py
```

El servicio escucha en 127.0.0.1:8080 por defecto. Para exponerlo fuera del dispositivo/host local, configurar un proxy HTTPS y controles de red. No desplegar públicamente sin TLS, gestión de secretos y endurecimiento operativo.

## API

- `GET /health` — salud, sin datos privados.
- `POST /v1/instructions` — requiere Bearer; JSON: `{"text":"...","idempotency_key":"...","origin":"bridge","project":"capcot","priority":"normal"}`.
- `GET /v1/instructions/{id}` — requiere Bearer; devuelve instrucción y tareas.
- `POST /v1/tasks/claim` — requiere Bearer; JSON opcional `{"worker":"nombre"}`; reclama atómicamente la siguiente tarea.
- `POST /v1/tasks/{id}/result` — requiere Bearer; JSON con `status` (completed/partial/blocked/failed) y evidencia en el resto del objeto.

La clave idempotente evita crear órdenes duplicadas. La reclamación usa una transacción SQLite inmediata para evitar que dos workers reclamen simultáneamente la misma tarea.

## Pruebas

```sh
cd runtime
python -m unittest discover -s ../tests -v
```

## Límites del MVP

Este núcleo no integra todavía proveedores LLM, plataformas de chat, OAuth/GitHub App, interfaz móvil ni despliegue persistente administrado. La autenticación es un único secreto de propietario y no sustituye un sistema multiusuario. Mantener el servicio en localhost hasta configurar HTTPS, secret manager, copias de seguridad y límites de abuso.
