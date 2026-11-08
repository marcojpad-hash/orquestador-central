# Máquina persistente + gateway para agentes de código

**Diseño documental, no despliegue. Mj no cablea nada. 8 de noviembre de 2026, CDMX.**

Leer primero [`COORDINATION/COMO_TRABAJAMOS.md`](../COORDINATION/COMO_TRABAJAMOS.md). Esta entrega sólo deja instrucciones. No crear cuentas/VM, instalar, autenticar, abrir puertos, enviar jobs, ejecutar CLIs ni activar servicios ahora.

## 1. Corrección de arquitectura

Mj pide una **máquina persistente encendida**, con disco y servicios que sobrevivan a los jobs y a los créditos de este bot. No es el runner efímero de `INSTRUCCION_SANDBOX_VM.md`, ni un Codespace que se suspende por inactividad. Es una capa adicional: **VPS/VM persistente = plano de control/gateway; trabajos = procesos/contenedores aislados; Actions = entrada opcional**. La sandbox efímera anterior sigue siendo válida para pruebas; no se promete que ella aloje el gateway 24/7.

Preferencia: VM Linux de bajo costo con presupuesto aprobado, inicialmente 2 vCPU/4–8 GiB como estimación de diseño para CLIs remotas, un worker por defecto y sin GPU. Medir luego; varios agentes concurrentes/render de video necesitan más recursos. Alternativa Oracle Always Free sólo si cuenta/región/capacidad lo permiten. No prometer gratis ni disponibilidad permanente: Oracle puede reclamar instancias ociosas y hay límites de capacidad. No generar carga falsa para evitarlo. Fuente: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm . Codespaces/devcontainer queda como entorno de desarrollo opcional, no hosting always-on.

La VM mantiene CLI instaladas: Claude Code, OpenCode, Aider, Codex y Gemini CLI cuando su cuenta/licencia lo permita, además de Git, Python 3.12, Node 22+, pipx, ripgrep, SQLite y Repomix. **Instalado ≠ autenticado ≠ habilitado ≠ CLI disponible para toda cuenta.** No arrancar todos los agentes ni usar modelos pagos por defecto.

## 2. Antecedentes abiertos: decisión mínima

- **OpenCode server**: https://opencode.ai/docs/server/ . API HTTP/OpenAPI y sesiones; comando documentado `opencode serve --hostname 127.0.0.1 --port 4096`. Tiene autenticación con `OPENCODE_SERVER_PASSWORD`. Mantener loopback y poner autenticación de gateway; no exponer APIs de shell/config/auth públicamente.
- **cli-bridge**: https://github.com/drewstone/cli-bridge . Puente HTTP compatible con múltiples coding CLIs y reanudación de sesiones. Es candidato muy cercano al requisito; su README lo describe como herramienta personal/loopback, no servicio multiusuario endurecido. Auditar licencia, commit, mecanismos de auth, sesiones y adaptadores antes de adoptar; no afirmar que Aider o todos los proveedores están soportados sin comprobarlos.
- **CLIProxyAPI**: https://github.com/router-for-me/CLIProxyAPI . Antecedente de pasarela multiproveedor; no equivale a una cola de trabajos de repositorio con verificación. Sus funciones de importación de credenciales/rotación de cuentas no se autorizan aquí. No extraer cookies/tokens, reutilizar sesiones fuera del soporte oficial ni evadir cuotas/políticas.

**Elección:** gateway pequeño con cola durable + adaptadores revisados; reutilizar cli-bridge o OpenCode server donde encajen, no reimplementar protocolos sin necesidad. Aider/CLI no soportada va por adaptador de subprocess con argv fijo, timeout y recibo; nunca comandos arbitrarios del payload. Revisar seguridad/proveedor antes de automatizar suscripciones: acceso en web no implica permiso o API para uso desatendido.

## 3. Instalación real documentada, no ejecutada

Fuentes consultadas el 8 de noviembre de 2026. Estos comandos son referencias oficiales sin fijar versión, **no un instalador listo ni una orden de ejecutarlos ahora**. El implementador debe resolver versiones actuales compatibles a un lockfile, revisar integridad/licencia y reproducir la imagen con versiones exactas; nunca `latest` en cada arranque.

| Herramienta | Método real publicado | Fuente |
|---|---|---|
| Claude Code | `npm install -g @anthropic-ai/claude-code`; instalador nativo recomendado: `curl -fsSL https://claude.ai/install.sh \| bash` | https://code.claude.com/docs/en/setup |
| OpenCode | `npm install -g @opencode/cli` en la línea actual; no mezclar con paquete antiguo `opencode-ai` sin revisar versión | https://opencode.ai/download y https://opencode.ai/docs/ |
| Aider | `pipx install aider-chat` con Python compatible (preferir 3.12); alternativa oficial `python -m pip install aider-install` y `aider-install` | https://aider.chat/docs/install.html |
| Codex CLI | `npm install -g @openai/codex` | https://www.npmjs.com/package/@openai/codex |
| Gemini CLI | `npm install -g @google/gemini-cli` | https://geminicli.com/docs/get-started/installation/ |
| Repomix | `npm install -g repomix`; Node ≥22 | https://repomix.com/guide/installation |

No ejecutar un instalador remoto con pipe sin revisión al desplegar: descargar, fijar versión y comprobar integridad según el proveedor. No `sudo npm install -g`; prefijo de instalación del usuario o build controlado. La edición actual del README de Gemini CLI advierte cambios de elegibilidad/licencia: comprobar la cuenta concreta; no prometer API gratuita ni soporte universal (https://github.com/google-gemini/gemini-cli). Graphify y otros mapas quedan opcionales/no verificados; Repomix no autoriza exportar secretos o todo el repo a un proveedor.

## 4. Servicios persistentes y almacenamiento

Árbol propuesto de la VM, no creado:

```text
/opt/mj-agents/releases/<version>/    gateway/worker/adapters revisados, readonly
/var/lib/mj-agents/queue.sqlite      jobs, eventos, leases, idempotency y cuotas
/var/lib/mj-agents/jobs/<job_id>/     entradas, salidas, manifiestos, checkpoints
/var/lib/mj-agents/snapshots/         repos fijados a SHA, Engine/244 readonly
/var/log/mj-agents/events.jsonl      eventos sanitizados append-only
/etc/mj-agents/policy.json           repos/rutas/adaptadores y límites aprobados
/run/credentials/                   secretos suministrados por systemd, no por jobs
```

`mj-agent-gateway.service`: recibe/consulta/cancela jobs. `mj-agent-worker.service`: drena cola con lease/fencing y ejecuta adaptadores. `opencode.service` opcional sólo en loopback, bajo usuario independiente. Activación futura mediante systemd, con `Restart=on-failure`, backoff acotado, inicio al arrancar, límites de memoria/CPU y usuario sin privilegios; no loops de tokens. No usar sistema de supervisión para revivir un job no idempotente a ciegas.

Gateway+un worker: SQLite con transacciones/WAL y disco persistente; claims atómicos, intentos y TTL. Reinicio recupera pendientes/leases expiradas, **no marca RUNNING como PASS**. Backups cifrados, snapshot coherente de SQLite, rotación de logs y prueba de restauración autorizada. Si se escala a varios hosts, reevaluar almacenamiento/cola; no compartir SQLite por NFS.

Esqueleto documental de unit (no instalar):

```ini
[Unit]
Description=Mj agents gateway
After=network-online.target
[Service]
User=mj-gateway
Group=mj-gateway
WorkingDirectory=/opt/mj-agents/current
ExecStart=/opt/mj-agents/current/venv/bin/python -m mj_gateway --bind 127.0.0.1:8787
Restart=on-failure
RestartSec=10
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/var/lib/mj-agents /var/log/mj-agents
# LoadCredential y permisos por servicio: completar sin escribir secretos aquí.
[Install]
WantedBy=multi-user.target
```

El worker necesita política distinta para sus directorios, ejecutables y credenciales por proveedor. Mantener usuarios, homes y permisos separados. Rootless containers o aislamiento revisado por job; sin Docker socket o llaves de administrador en el entorno del agente. No basta chmod si el agente es dueño del archivo o tiene sudo. Engine/244 montados readonly desde snapshot confiable y verificados antes/después; cambios de código sólo en laterales de una rama autorizada.

## 5. Interfaz universal HTTP/cola (propuesta, pendiente de implementar)

- `POST /v1/jobs`: contrato tipado, máximo 1 MiB; retorna 202 y job_id.
- `GET /v1/jobs/<id>`: estado/recibos; `GET /v1/jobs/<id>/events`: JSONL/SSE sanitizado con cursor.
- `POST /v1/jobs/<id>/cancel`: cancelación autorizada e idempotente.
- `GET /healthz`: liveness; `/readyz`: cola/worker disponibles sin exponer secretos.

Job incluye instruction_id, conversation_id, idempotency_key, tipo permitido, repo/ref/SHA, adapter_id, entradas/hashes, límites y criterios de verificación. **No acepta `command`, shell libre, rutas arbitrarias, cookies, secretos ni autoaprobación.** Autenticación por cliente, autorización por repo/ruta/adaptador, cuotas y separación de proyectos; identidad no se toma de `from_agent`. TLS/reverse proxy privado o red privada revisada, rate limits y auditoría. OpenCode interno no se publica directamente.

Cualquier modelo **con un conector HTTP/MCP autorizado o acceso al bus** puede enviar el contrato y leer resultados sin ejecutar por sí mismo Claude/Codex/etc. Un chat sin herramientas no puede llamar la VM mágicamente: produce un job/handoff completo para que el adaptador conectado lo reciba; un único bloque de transferencia, no cableado para Mj. No prometer despertar Meta AI/Grok/ChatGPT web automáticamente. El bus GitHub sigue como transporte alternativo/correlación y memoria; no requiere este bot.

Secrets en Secrets de Actions para el camino Actions; Codespaces secrets sólo para desarrollo. En VPS: almacén de secretos/credenciales systemd con ACL por servicio y aprovisionamiento aprobado; no copiar todos los secretos de Actions al disco del worker. No pasar claves en argumentos CLI, prompts, imágenes Docker o archivos versionados. Cada proveedor puede requerir consentimiento/login distinto: **un solo signup no autentica a cinco proveedores**. Si se requiere interacción del propietario, usar canal seguro de autenticación, nunca pedirle claves en chat.

Opcional: registrar VM como self-hosted runner de repos privados de confianza, con permisos y aprobación específicos. **Nunca ejecutar PRs/forks no confiables en el host persistente con secretos**. Usuario runner separado, sin privilegios de gateway/credenciales ni acceso general a código canónico writable; preferir que Actions sólo entregue job al gateway. Persistencia de máquina no significa workspace compartido entre tareas.

## 6. Inicio obligatorio y aceptación

Cada job recupera el SHA aprobado de `COORDINATION/COMO_TRABAJAMOS.md`, reglas locales y orden vigente; registra hash de lectura. El wrapper de cada CLI inyecta el mismo handoff de tarea y límites, sin asumir que todas leen `AGENTS.md`/`CLAUDE.md` de igual forma. Si faltan reglas, contrato o verificador → BLOCK. No usar opciones que deshabiliten protecciones/aprobaciones globalmente.

Para declarar operativo, después de otra autorización: CLIs instaladas con versiones/hashes; capacidades/licencias por CLI comprobadas; gateway autenticado en loopback/ingress seguro; job→recibo→verificación; cola sobrevive reboot sin duplicar side effects; watchdog/leases/cancel funcionan; fallos LLM no destruyen control; JSONL+backup+restauración; Engine/244 readonly y hashes intactos; sin secretos en resultados; merge sólo PR + checks/CEB aplicables + “merge” de Mj. No declarar que una instalación vacía o un fixture cumple esas pruebas.

## 7. Qué sí necesita una intervención humana única

Mj elige proveedor/autoriza gasto o confirma su VM existente; crea/autoriza cuenta y acceso inicial si aún no existe, posiblemente tarjeta/verificación del proveedor. El agente prepara después **un solo bootstrap completo, idempotente y revisado**, o cloud-init por consola autorizada, no una lista de piezas. No existe todavía bootstrap confiable ni URL de instalación propia: no inventarla. Credenciales/consentimientos de cada proveedor que lo exija se completan por canales seguros; pueden ser varios. El agente realiza instalación/cableado tras autorización y deja servicio verificable; no pedir a Mj operar cinco terminales todos los días.

## 8. PROMPT PARA MUSE

El prompt completo, autocontenido y versionado es [`docs/PROMPT_MUSE_VM.md`](PROMPT_MUSE_VM.md). Se entrega junto con este documento, no depende del historial del bot. Si Muse no tiene lectura/escritura/terminal, debe entregar el bundle completo y declarar esa limitación; no fingir despliegue ni cargar a Mj la integración.

### Texto autocontenido para copiar a Muse

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


### Bloque para Grok (preparación futura)

> Lee `COORDINATION/COMO_TRABAJAMOS.md` y `docs/INSTRUCCION_VM_AGENTES_CODIGO.md` en `marcojpad-hash/orquestador-central`; prepara por PR una máquina persistente con gateway/cola y adaptadores CLI, no un Codespace efímero.
> No aprovisiones, instales, abras puertos ni actives servicios ahora; deja bootstrap, locks, systemd, schemas y pruebas preparados, Engine/244 readonly y Secrets fuera del repo.
> Entrega un paquete completo y el PR; pide sólo la decisión de hosting/credenciales que realmente falte. No fusiones: yo daré “merge” al PR/SHA aprobado.


## Anexo: devcontainer opcional, NO máquina always-on

Sólo para desarrollar/revisar el mismo código; Codespaces puede suspenderse y generar costo, así que no alojar ahí el gateway persistente. El agente preparará una imagen preinstalada a partir de versiones bloqueadas; no instalar ni arrancar CLIs automáticamente al abrir el contenedor. Esqueleto documental (digest/imagen pendientes de resolución, no creado):

```json
{
  "name": "mj-agents-dev-only",
  "build": {"dockerfile": "Dockerfile"},
  "remoteUser": "vscode",
  "containerEnv": {"MJ_EXECUTION_ENABLED": "false"},
  "postStartCommand": ["bash", ".devcontainer/read-rules-only.sh"],
  "shutdownAction": "stopContainer"
}
```

`Dockerfile` y `read-rules-only.sh` son artefactos futuros que deben entregarse completos; el segundo sólo muestra reglas fijadas y no ejecuta jobs ni autenticaciones. Nada de secretos dentro de la imagen. Los candados de Engine/244 siguen exigidos por montajes/política independiente, no por este JSON.
