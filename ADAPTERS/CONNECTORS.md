# Adaptadores de plataformas

## Objetivo

Permitir que cualquier plataforma conectada funcione como una puerta de entrada y salida al mismo coordinador. El núcleo no debe depender de que el propietario use una sesión específica.

## Estado inicial

| Plataforma | Entrada posible | Condición |
|---|---|---|
| GitHub | Issues, Discussions, App/webhook o API | App instalada y permisos configurados |
| ChatGPT | App/connector/API compatible o entrada puente | Depende de capacidades y acceso del producto |
| Grok | API, bot o webhook compatible | Requiere credenciales y mecanismo de integración |
| Claude | API, MCP o integración compatible | Requiere configuración del proveedor |
| Gemini | API o integración compatible | Requiere configuración del proveedor |
| Meta | APIs y webhooks de productos Meta compatibles | Requiere app, permisos y revisión según producto |
| Otros | Adaptador con contrato común | Debe autenticar al propietario |

No se presupone que una plataforma permita leer el historial privado de sus sesiones. Un adaptador solo puede recibir los mensajes que el usuario envíe explícitamente por una vía integrada.

## Contrato HTTP propuesto

- POST /v1/instructions
- GET /v1/instructions/{instruction_id}
- GET /v1/tasks/{task_id}
- POST /v1/tasks/{task_id}/result
- POST /v1/agents/heartbeat
- GET /v1/capabilities

Todos los endpoints requieren autenticación fuerte, autorización por alcance y protección contra replay.

## Puente universal inicial

Mientras no existan todos los adaptadores nativos, el sistema tendrá una entrada web autenticada y una entrada GitHub Issue. El usuario podrá pegar o reenviar allí cualquier instrucción; el origen se registrará manualmente si no existe identidad verificable del canal.
