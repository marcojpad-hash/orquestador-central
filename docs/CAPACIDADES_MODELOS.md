# Registro de capacidades por agente/modelo
**Corte inicial:** 2026-11-07  
**Última actualización:** 2026-11-10 (registro de Muse/Pecas)  
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
| Muse / Pecas (Muse Spark, app + VM Linux) | Confirmada (repos públicos marcojpad-hash) | Confirmada vía PR; sin push directo a main; sin permiso Workflows en la app de GitHub; no crea repos por API | Sí; evidencia: reprodujo 2 fallas del runner ejecutando (2026-11-10), tests 5/5, ejecutó validar_storyboard.py | Sí; evidencia: navegador (GitHub, YouTube Studio, TikTok, grok.com) | Sí genera medios (montaje, imágenes); publicación solo manual por Marco | CONFIRMADO con alcance limitado |

## Ficha completada — Muse / Pecas (2026-11-10)

- **Identidad y versión visible:** Muse / Pecas (Muse Spark)
- **Proveedor / interfaz:** Muse app + VM Linux (navegador cloud y en-app KINGKONG X), conector GitHub
- **Cuenta o identidad GitHub exacta:** marcojpad-hash (vía app de Muse, acceso a todos los repositorios)
- **Repositorios y ramas que puede leer:** todos los públicos de marcojpad-hash
- **Repositorios y ramas que puede escribir:** vía PR a main (no push directo); sin permiso Workflows; no crea repos por API (403 verificado)
- **Herramientas conectadas:** terminal/VM (python3, ffmpeg, git), navegador, GitHub connector, Groq (gpt-oss-120b, gratis), Gemini (gemini-3-flash-preview, gratis)
- **Puede ejecutar terminal/código:** sí; evidencia: reprodujo 2 fallas del runner ejecutando (2026-11-10), tests 5/5, ejecutó validar_storyboard.py (falló 8 errores, corregido y re-verificado OK)
- **Puede ejecutar pruebas:** sí; evidencia: tests del runner 5/5, validador ejecutado
- **Puede usar web:** sí; evidencia: navegador (GitHub, YouTube Studio, TikTok, grok.com)
- **Puede generar medios/publicar:** sí genera medios (montaje de video, imágenes, voz Kokoro); publicación solo manual por Marco
- **Cuotas y costo:** Muse semanal gratis 100% usado (reinicia 2026-11-13 17:24 CST); fondo adicional 2% usado; Groq/Gemini gratis
- **Límites de contexto, archivos y ejecución:** app de GitHub sin permiso Workflows; binarios no pasan por conector (máx 16 MiB UTF-8); VM sin GPU/Docker
- **Fecha de prueba y resultado:** 2026-11-10; PR #5 orquestador-central (runner, abierto, no fusionado)
- **Estado:** CONFIRMADO con alcance limitado

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
