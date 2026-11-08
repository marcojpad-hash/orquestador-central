# Auditoría de accesos de agentes — 2026-11-07

## Alcance
Repositorios principales:
- marcojpad-hash/orquestador-central
- marcojpad-hash/ChatGPT-migracion
- marcojpad-hash/motor-u6-storage
- marcojpad-hash/capcot-capsulas-imaginantes (rama feature/capcot-video-discovery-continuity)

## Evidencia confirmada
La conexión GitHub autenticada como la cuenta propietaria `marcojpad-hash` devuelve permisos `admin=true`, `maintain=true`, `push=true` en los cuatro repositorios consultados. Por tanto, la conexión usada para esta intervención sí puede escribir en los repositorios.

## Lo que NO quedó comprobado
No se pudo enumerar la lista de colaboradores, identificar las cuentas GitHub exactas de Copilot, Grok app, Imaginantes/Grok Bot o Claude, ni consultar las reglas de protección de ramas desde las acciones disponibles en esta conexión.

El conector disponible permite consultar el permiso de un colaborador si se conoce su username, pero no expone aquí una acción para listar colaboradores ni para modificar sus permisos o reglas de protección. No se inventaron usernames ni se alteró la protección de ramas como atajo.

## Estado
- Permiso de la cuenta propietaria conectada: **CONFIRMADO — ADMIN** en los cuatro repositorios.
- Permisos de Copilot: **NO_PROBADO**.
- Permisos de Grok app: **NO_PROBADO**.
- Permisos de Imaginantes/Grok Bot: **NO_PROBADO**.
- Permisos de Claude/Claude Code: **NO_PROBADO**.
- Restricciones de rama / rulesets: **NO_INSPECCIONADOS**.
- Cambios de permisos efectuados: **NINGUNO**.

## Siguiente paso administrativo exacto
Identificar en GitHub Settings → Collaborators (o Manage access) el username real de cada integración/bot y revisar su rol por repositorio. Revisar Settings → Rules → Rulesets / Branch protection para saber si el 403 procede de una regla de rama y no del rol del colaborador. Con los usernames confirmados, consultar los permisos individuales y cambiar únicamente los que Mj autorice, registrando antes/después.

No conceder Admin indiscriminadamente. Para agentes que solo deben entregar commits en ramas de trabajo, el permiso mínimo suele ser Write; mantener Admin solo para quien administra repositorio y reglas.
