# Modelo de datos inicial

## Entidades

### Instruction
instruction_id, idempotency_key, owner_actor_id, origin_platform, origin_session_ref, original_text, received_at, project_id, priority, status.

### Project
project_id, name, repository, branch_policy, protected_paths, project_rules_ref, memory_ref, active_agents.

### Task
task_id, instruction_id, parent_task_id, project_id, title, objective, assigned_agent_id, status, acceptance_criteria, created_at, updated_at.

### Agent
agent_id, provider, specialty, capabilities, constraints, endpoint_ref, credential_ref, permission_scope, health_status, performance_metrics.

### Execution
execution_id, task_id, agent_id, started_at, finished_at, status, evidence_refs, changed_paths, run_ref.

### Decision
decision_id, owner_instruction_id, project_id, decision_text, effective_at, supersedes, status.

### AuditEvent
event_id, actor, action, resource, timestamp, result, evidence_ref, correlation_id.

## Reglas de integridad

- UUIDs para identificadores globales.
- Timestamps ISO-8601 UTC.
- Referencias explícitas entre instrucción, tareas, ejecuciones y evidencia.
- Eventos de auditoría append-only.
- Estados controlados por enumeraciones.
- Secretos guardados fuera de Git.
- Los archivos YAML de REGISTRY son configuración inicial, no base de datos transaccional.
