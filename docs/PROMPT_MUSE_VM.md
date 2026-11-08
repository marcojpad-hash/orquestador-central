# PROMPT PARA MUSE — prepara una máquina persistente de agentes, sin desplegar todavía

Soy Mj. Necesito que cualquier modelo pueda continuar mi trabajo sin depender de los créditos de un bot. Yo no programo ni cableo: entrega un paquete completo, no piezas para que yo las una. Tu tarea inicial es producir implementación y PR/bundle revisables; **no ejecutar, instalar, aprovisionar, autenticar, abrir puertos, enviar jobs, gastar ni fusionar ahora**. No afirmes que creaste una VM o que pasaron pruebas que no ejecutaste.

## Contexto y fuentes imprescindibles

- Reglas: https://github.com/marcojpad-hash/orquestador-central/blob/main/COORDINATION/COMO_TRABAJAMOS.md
- Instrucción completa: https://github.com/marcojpad-hash/orquestador-central/blob/main/docs/INSTRUCCION_VM_AGENTES_CODIGO.md
- Especificación: https://github.com/marcojpad-hash/orquestador-central/blob/main/docs/orchestrator.v2.1.json
- Puente/base: https://github.com/marcojpad-hash/orquestador-central/blob/main/docs/INSTRUCCION_RUNTIME_TESTBED_PUENTE.md
- Pruebas sandbox: https://github.com/marcojpad-hash/orquestador-central/blob/main/docs/INSTRUCCION_SANDBOX_VM.md
- Motor: https://github.com/marcojpad-hash/motor-u6-storage/blob/main/docs/HANDOFF_MOTOR_GROK.md

Repos privados: verificar acceso real; si tu chat no tiene GitHub/terminal, dilo y entrega archivos completos con rutas, diff y un único bloque para que un agente autorizado aplique el bundle. No uses supuestos contenidos de enlaces inaccesibles: marca dependencias pendientes y no inventes contexto. No me pidas hacer cableado manual.

## Lo que debes preparar, paso por paso

1. Lee las fuentes y confirma capacidades, repo/ref/SHA y mandato. La v2.1 es documental no activa; único array raíz `steps`, no `runtime.pasos_en_orden`, no es schema ni programa. No cambies flags para fingir permiso.
2. Diseña VM Linux **persistente/encendida con disco durable**, preferentemente VPS aprobado; Oracle Always Free sólo si capacidad/cuenta lo permiten y advirtiendo reclamación de instancias ociosas. Codespaces se suspende: no cumple always-on. El job de pruebas puede ser efímero, el gateway no.
3. Prepara bootstrap idempotente, lockfile de versiones, policy, schemas de jobs/resultados y servicios systemd. Instala sólo después de futura aprobación, como usuarios no root: Claude Code, OpenCode, Aider, Codex, Gemini CLI compatible con cuenta/licencia, Repomix, Node≥22, Python 3.12, Git y SQLite. No instalar un modelo GPU por defecto.
4. Referencias de comandos reales, para el bootstrap futuro (no ejecutarlos ahora): `npm install -g @anthropic-ai/claude-code`; `npm install -g @opencode/cli`; `pipx install aider-chat`; `npm install -g @openai/codex`; `npm install -g @google/gemini-cli`; `npm install -g repomix`. Sustituye paquetes por versiones exactas comprobadas en lockfile; no prometas gratuidad/licencia universal. Fuentes: https://code.claude.com/docs/en/setup , https://opencode.ai/download , https://aider.chat/docs/install.html , https://geminicli.com/docs/get-started/installation/ , https://repomix.com/guide/installation .
5. Reutiliza, tras auditoría, https://github.com/drewstone/cli-bridge o https://opencode.ai/docs/server/ . OpenCode interno documenta `opencode serve --hostname 127.0.0.1 --port 4096`; no lo expongas sin control ni publiques endpoints shell/auth/config. No importar cookies/tokens ni evadir cuotas de proveedores. Instalar ≠ autenticar.
6. Implementa gateway autenticado y cola SQLite durable con transacciones: `POST /v1/jobs`, `GET /v1/jobs/<id>`, eventos/cancelación, health/readiness. Son endpoints propios propuestos: debes materializarlos. Payload de repo/SHA y adapter_id allowlisted, nunca shell libre ni credenciales. Dedupe, leases/fencing, TTL, límites, estados honestos, verificador independiente, checkpoint sólo tras paso realmente verificado. Restart/reboot no repite efectos no idempotentes ni crea PASS.
7. Cada CLI recibe al empezar reglas/handoff fijados y hash de lectura; no asumas que todas cargan el mismo archivo. Engine V5 y canon 244 son **readonly incluso en sandbox**; baseline confiable, mount readonly y hash/diff antes/después. Sin root, sudo o credenciales de publisher en el job. No cambiar voz CAPCOT: si el job toca video, únicamente edge-tts es-MX-JorgeNeural, rate +7%, pitch −2Hz.
8. Un cliente Grok/ChatGPT/Claude/bot con conector autorizado manda un job y lee el recibo sin necesitar ejecutar las otras CLIs. Un chat sin herramientas no puede llamar mágicamente al servidor: genera handoff completo. Bus GitHub alternativo, máximo seis turnos, ACK no equivale a verificación. No activar clientes ahora.
9. JSONL sanitizado, backups/recuperación, hashes y cuotas; tres intentos totales para transitorios dentro de deadline, nunca evadir rechazo de seguridad. Secrets sólo canales aprobados: Actions/Codespaces para sus entornos y credenciales systemd/gestor para VPS, aisladas por proveedor. No claves en repo/log/argv/prompts. Crear una cuenta VPS no autentica todos los proveedores; reconoce consentimientos humanos reales.
10. Opcional self-hosted runner: servicio/usuario aislado y repos privados de confianza, sin PRs/forks no confiables ni token privilegiado accesible al agente; preferir Actions→gateway. Entrega un único bootstrap futuro revisado/cloud-init, sin URL de instalador inventada, y PR sin merge. Una interacción humana de hosting puede ser inevitable; tú haces el resto una vez autorizado.

## Entregables y aceptación

Entrega árbol completo, archivos enteros, locks/versiones, schemas, systemd, adaptadores, plan de secretos sin valores, threat model, rollback preservando datos y pruebas propuestas. Si tienes escritura autorizada, PR de implementación en orquestador; si no, bundle descargable/completo más un bloque para aplicarlo. No ejecutar workflows por publicar archivos sin revisar triggers.

Pruebas para una fase posterior: cada CLI declara capacidad real, contrato inválido bloquea, autenticación/aislamiento, job→recibo→verificación, timeout/cancel, reboot recupera cola sin duplicación, restauración backup, Engine/244 inalterados, ningún secreto en logs y cliente sin permiso rechazado. Hoy marcarlas NO_EJECUTADAS. Producción: PR + checks/CEB aplicables + mi “merge” al PR/SHA; nada automático.

Reporta: qué preparaste, qué no hiciste, repo/rama/SHA/PR o bundle real, versiones y fuentes, bloqueos exactos, coste no autorizado y un solo siguiente paso para hosting/credenciales si faltan. No inventes comandos/flags de automatización CLI: comprobar `--help` en la fase futura autorizada y registrar compatibilidad.
