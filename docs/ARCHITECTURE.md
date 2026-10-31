# Arquitectura técnica

## Vista lógica

```text
Canales de entrada
  ChatGPT | Grok | Claude | Gemini | Meta | GitHub | otros
                   |
             Adaptadores
                   |
          Gateway de instrucciones
                   |
       Identidad + autenticación + deduplicación
                   |
          Registro de instrucciones
                   |
       Clasificador / recuperador de contexto
                   |
             Planificador
                   |
          Router de capacidades
           /       |       \
     Especialista  Especialista  Especialista
           \       |       /
             Supervisor
                   |
        Verificación de evidencia
                   |
       Memoria + auditoría + estado
                   |
        Respuesta al canal de origen
```

## Componentes de despliegue

1. **GitHub repository:** contratos, configuración versionada, memoria documental e historial de cambios.
2. **Coordinator API:** servicio HTTPS que recibe eventos de los adaptadores y expone operaciones autenticadas.
3. **Operational database:** instrucciones, estados, locks, colas, ejecuciones, idempotencia y métricas.
4. **Worker/agent runtime:** ejecuta planes y llama a proveedores de modelos según capacidades y permisos.
5. **GitHub App:** acceso a repositorios instalados con permisos mínimos.
6. **Scheduler/queue:** tareas periódicas, reintentos, límites de concurrencia y recuperación.
7. **Observability:** logs estructurados, auditoría, alertas y trazas.

GitHub Actions puede ejecutar validaciones y trabajos programados, pero no sustituye por sí solo al servicio persistente que recibe webhooks, coordina sesiones y mantiene colas.

## Flujo de instrucción

1. Adaptador autentica el origen y valida que la orden procede del propietario.
2. Gateway asigna instruction_id, registra timestamp, canal y payload.
3. Capa de idempotencia evita procesar dos veces la misma orden.
4. Clasificador identifica proyecto, intención, sensibilidad y prioridad.
5. Context retriever consulta memoria y políticas del proyecto.
6. Planner divide el trabajo en subtareas con criterios de aceptación.
7. Router elige agentes por capacidad, disponibilidad, coste y permisos.
8. Workers ejecutan y devuelven evidencia estructurada.
9. Supervisor verifica entregables y pruebas.
10. Estado y memoria se actualizan; el adaptador entrega respuesta al canal de origen.

## Desacoplamiento

El contrato del agente no depende de un proveedor concreto. Cada proveedor implementa un adaptador. Si una plataforma no ofrece API/webhook para el caso requerido, se ofrece una entrada alternativa autenticada (por ejemplo, formulario o endpoint compartido) sin simular acceso a sesiones privadas.

## Seguridad

- OAuth/GitHub App; evitar tokens personales de alcance amplio.
- Secret manager externo para credenciales.
- Allowlist de repositorios y rutas.
- Aislamiento por proyecto.
- Límites de coste, tiempo y concurrencia.
- Reintentos idempotentes.
- Registro append-only de eventos relevantes.
- Aprobaciones explícitas para operaciones de alto impacto.
- Pruebas y rollback.
