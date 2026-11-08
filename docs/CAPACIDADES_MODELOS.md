# Registro de capacidades por agente/modelo
**Corte inicial:** 2026-11-07  
**Regla:** registrar solo capacidades probadas en una interfaz concreta. Este registro no se hereda automáticamente entre planes, sesiones o cuentas.

## Estado actual

| Agente / interfaz | Lectura GitHub | Escritura GitHub | Ejecución de código | Web/investigación | Medios/publicación | Estado |
|---|---|---|---|---|---|---|
| ChatGPT conectado a GitHub (cuenta marcojpad-hash) | Confirmada | Confirmada en repositorios accesibles; escribir por API de contenidos | No se presume en este conector | Confirmada en sesión actual | No se presume | CONFIRMADO con alcance limitado |
| Imaginantes / Grok Bot | No comprobada en esta sesión | No comprobada en esta sesión | No comprobada | No comprobada | Capacidad definida por contrato CAPCOT; ejecución actual no comprobada | NO_PROBADO aquí |
| Grok app | No comprobada en esta sesión | No comprobada | No comprobada | Depende de la sesión | Depende de la sesión | NO_PROBADO |
| GitHub Copilot / coding agent | No comprobada para identidad concreta | No comprobada para identidad concreta | Depende del agente y entorno | Depende del entorno | No aplica por defecto | NO_PROBADO |
| Claude / Claude Code | No comprobada para identidad concreta | No comprobada para identidad concreta | Depende de la interfaz | Depende de la interfaz | No aplica por defecto | NO_PROBADO |
| Modelo local / open-weight | No disponible hasta instalar/configurar cliente y servidor | No disponible hasta integrar Git | Depende del runtime | Puede ser local o no tener web | No aplica por defecto | NO_PROBADO |

## Ficha que cada agente debe completar

Copiar una ficha por agente, no por marca genérica:

- **Identidad y versión visible:**
- **Proveedor / interfaz:** (web, app, CLI, IDE, bot, API, local)
- **Cuenta o identidad GitHub exacta:**
- **Repositorios y ramas que puede leer:**
- **Repositorios y ramas que puede escribir:**
- **Herramientas conectadas:**
- **Puede ejecutar terminal/código:** sí/no; evidencia:
- **Puede ejecutar pruebas:** sí/no; evidencia:
- **Puede usar web:** sí/no; evidencia:
- **Puede generar medios/publicar:** sí/no; evidencia:
- **Cuotas y costo:** gratis / cuota incluida / créditos / API de pago / cómputo local / desconocido
- **Límites de contexto, archivos y ejecución:**
- **Fecha de prueba y resultado:**
- **Estado:** CONFIRMADO / LIMITADO / NO_DISPONIBLE / NO_PROBADO / BLOQUEADO

## Regla de actualización

No registrar “Copilot tiene escritura” o “Grok recibió el paquete” por inferencia. Registrar la cuenta GitHub exacta, la prueba y la ruta/commit/acuse que lo demuestre. Si la identidad del bot no está clara, pedir al administrador que la identifique en GitHub; no adivinar usuarios.
