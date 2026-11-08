# Runner integrado + sandbox de pruebas U6 en GitHub Actions

**Instrucción documental para Grok App; alternativa: otro agente con permisos efectivos comprobados.**
**Propietario: Mj. Fecha: 8 de noviembre de 2026, CDMX (America/Mexico_City, UTC−6).**

## 0. Qué estamos definiendo y qué NO se ejecuta ahora

Preparar el entorno para que pruebas autorizadas del motor corran **de verdad en GitHub Actions**, sin depender de que un modelo simule ejecución ni de que Mj conecte piezas. Esta instrucción es un documento, no una VM creada ni un permiso de ejecución.

En esta entrega: **no crear la rama, workflows, contenedores, permisos, secretos ni PR; no correr JSON, pruebas, smoke, búsquedas, calibraciones, modelos o dispatches.** Sólo se prepara este documento. La eventual publicación documental tampoco activa el sistema.

Después de autorización expresa, Grok realiza el montaje completo y entrega evidencia. Mj sólo decide el alcance y, llegado el momento, da un único **“merge”** referido a un PR y SHA concretos. No se le pide programar, instalar Docker ni pegar comandos por partes.

La sandbox permite ejecutar código revisado sin depender del juicio probabilístico de un LLM; **no elimina sus políticas ni sustituye las autorizaciones**. Una negativa no se evade mediante prompts, sesiones o herramientas distintas. Ante una tarea legítima que un modelo no pueda hacer, el scheduler puede usar un adaptador determinista autorizado y registrar el motivo; no inventar PASS ni forzar al modelo a aprobar.

## 1. Base real y lectura obligatoria

### Motor: `marcojpad-hash/motor-u6-storage`

Rutas comprobadas por lectura de GitHub al preparar esta instrucción:

- `motor/motor/`: implementación del motor y laterales.
- `motor/motor/ceb_runtime_v0_6_flow.py`: CEB.
- `casos/fabrica/fabrica.py`: fábrica.
- `docs/HANDOFF_MOTOR_GROK.md` y `docs/CEB_INVESTIGAR_Y_RESOLVER.md`.
- `tests/test_ceb_caldero_honestidad.py`, `tests/test_ceb_alertas_multipieza.py`.
- `.github/workflows/fabrica-real-traza.yml` y `.github/workflows/fabrica-lote-diario.yml`.

**No copiar y ejecutar directamente `fabrica-real-traza.yml`:** actualmente incluye regeneración de manifiestos, permisos `contents: write` y un paso que hace push a `main`. Sus verificaciones de candados y CEB son antecedentes útiles; su publicación directa a producción NO es el patrón de sandbox solicitado. No modificar ese workflow en esta fase.

### Plano de control: `marcojpad-hash/orquestador-central`

Leer `README.md`, `AGENTS.md`, `CORE/AUTHORITY.md`, `PROTOCOL/INSTRUCTIONS.md`, `REGISTRY/AGENTS.yaml`, `docs/CONTRATO_TRABAJO_MULTI_MODELO.md`, además de:

- `docs/INSTRUCCION_RUNTIME_TESTBED_PUENTE.md`.
- **`docs/orchestrator.v2.1.json`**, no v2.0. Tiene un único array raíz **`steps`**. No tiene `runtime.pasos_en_orden` operativo.
- `runtime/README.md`, `runtime/sequential_runner.py` y el contrato local antes de proponer reutilización.

**Hallazgo importante de la versión publicada:** v2.1 es declarativa, sus adaptadores no están implementados/allowlisted y `schema_semantics.configuration_schema` sigue en `null`. No existe un “JSON Schema de respuestas LLM ya implementado en v2.1” que podamos afirmar que estamos usando. La fase de implementación deberá materializar y versionar los esquemas suplementarios aquí definidos y validarlos; no convertir `expected_output` en un esquema ni tratar este documento como ejecución autorizada.

### Aislamiento red-team: `marcojpad-hash/red-teaming-safety-u6`

Leer `docs/SPEC_RE_TEAM_WHITE_HAT_HOMEOSTASIS_U6.md`, `ledger/ACTIVE.md` y `.github/workflows/aislar-subcorridas-adversarial.yml`. Conservar su principio **una subcorrida por job/proceso aislado**. No disparar ese workflow ni escribir en su ledger por haber pasado un smoke de infraestructura.

Antes de implementar, recuperar SHA completo de cada fuente, revisar cambios recientes y contratos locales; fijar referencias y hashes en un manifiesto. No asumir que Contents/PR write permite modificar workflows, disparar Actions o administrar protección de ramas.

## 2. La “VM” correcta para nuestra forma de trabajar

- **Rama `sandbox-testing`:** referencia Git de trabajo creada desde un SHA de `main`, no clon físico ni aislamiento de ejecución. No contiene ni protege secretos por ser rama distinta.
- **VM de ejecución:** un job efímero `ubuntu-24.04` hospedado por GitHub Actions, con checkout del SHA exacto de `sandbox-testing` autorizado. Mj no aporta un servidor ni usa la box del bot.
- **Contenedor opcional:** `container:` o Docker Compose dentro de ese job si hay necesidad demostrada. Un directorio, `SANDBOX_MODE=TRUE` o un bind mount del repo no son un sandbox de seguridad.
- **Producción:** nada ejecuta ni escribe el motor de `main`. El único añadido inicial que puede requerirse allí es un dispatcher mínimo y manual, mediante PR aprobado, porque GitHub exige presencia del workflow en la rama predeterminada. Esta excepción de bootstrap se documenta y aprueba; no se esconde bajo “main intacta”.

No usar `git checkout sandbox-testing` con `check=False`. El checkout y la validación de SHA deben fallar de forma visible; nunca continuar en `main` por error. `git pull` sin ref fijado hace la prueba irreproducible. No usar `docker compose up` en la box ni en el teléfono.

Para pruebas iniciales: fuentes canónicas de sólo lectura, salida en directorio temporal, sin token de escritura ni secretos LLM en el job ejecutor. Código potencialmente hostil queda fuera del MVP; si se requiere más adelante, exige aislamiento revisado, red restringida, límites CPU/memoria/pids, sin Docker socket montado y sin modo privilegiado. El contenedor compartiendo host no equivale a una VM adicional.

## 3. Separación de planos y activación futura

### Plano confiable de control

Valida identidad/autorización, repo/ref/SHA, límites, contratos y candados. Usa código revisado y fijado a commit; **no ejecuta scripts de `sandbox-testing` con credenciales de escritura**. Resuelve las solicitudes a adaptadores allowlisted; el texto de un LLM no se transforma en shell.

### Ejecutor de pruebas

Job con `contents: read`, checkout sin credenciales persistidas y fuente fijada. Las pruebas sólo escriben en su workspace temporal y artefactos. Búsquedas/API, si se autorizan después, mediante job separado de alcance mínimo, Secrets sólo para ese adaptador y presupuesto conocido; no exponerlos a código arbitrario de sandbox.

### Verificador independiente

Comprueba recibos, exit codes, contenido, hashes, CEB y ausencia de cambios protegidos. No acepta `ok:true` del creador como prueba. La ausencia de archivo, resultado vacío o tamaño correcto no agota la verificación semántica.

### Publicador de evidencia

Job separado, código confiable, escritor único, `contents: write` únicamente cuando esté autorizado publicar evidencia. Descarga artefactos identificados por run/attempt, valida nombres/tamaños/hashes, rechaza traversal/symlinks, sanitiza secretos y **no ejecuta artefactos**. Confirma exclusivamente `avances/sandbox/<run_id>-<attempt>/` en `sandbox-testing`, nunca en `main`. Token de publicación limitado a la operación; GitHub no aplica por sí mismo restricciones por ruta: el publicador debe comprobar la allowlist antes del commit.

**No activar ahora.** Después se necesitarán permisos de workflow/Actions y acceso de lectura cruzada a los privados. Contents/PR write de Grok no implica Secrets, administración ni permisos de workflows. No concederse permisos ni tocar protecciones para resolver un 403; registrar exactamente el permiso faltante.

## 4. Árbol objetivo (futuro, no crear ahora)

```text
marcojpad-hash/orquestador-central/
  docs/INSTRUCCION_SANDBOX_VM.md                  # este documento
  docs/INSTRUCCION_RUNTIME_TESTBED_PUENTE.md       # contrato base, preservar
  docs/orchestrator.v2.1.json                     # especificación base, preservar
  schemas/llm-bridge-response-v1.schema.json      # nuevo suplemento propuesto
  schemas/sandbox-job-v1.schema.json             # nuevo contrato activable, pendiente
  COORDINATION/bus/messages/<message_id>.json     # bus sólo cuando se autorice
  COORDINATION/bus/events/<event_id>.json

marcojpad-hash/motor-u6-storage/ [sandbox-testing]
  sandbox_runtime/
    runner_main.py
    llm_bridge.py
    adapter_registry.py
    verify_results.py
    execution-plan.json                         # un solo array steps tipado
    source-manifest.json                        # refs/hashes de v2.1 y schemas
    contracts/llm-bridge-response-v1.schema.json  # copia fijada y hash comprobado
    contracts/sandbox-job-v1.schema.json
    policy/protected-paths.json                 # inventario completo, confiable
    tests/test_contracts.py
    tests/test_runner_integrity.py
    tests/test_bridge_need_bus.py
    tests/test_watchdog_checkpoints.py
    container/compose.yaml                      # opcional, no requisito del MVP
  .github/workflows/sandbox-testing.yml          # dispatcher y jobs revisados
  avances/sandbox/<run_id>-<attempt>/
    events.jsonl
    report.json
    manifest.json
    ceb.json
    checksums.sha256
  motor/motor/                                  # Engine/244 intactos
  casos/fabrica/                                # no convertir fixture en caso real

GitHub Actions artifacts:
  sandbox-<run_id>-<attempt>/
    events.jsonl
    report.json
    manifest.json
    ceb.json
    checkpoints/                               # sólo pasos reales verificados
```

La ubicación del código nuevo es lateral. El inventario de rutas protegidas se deriva de los contratos y manifiestos canónicos de `main` confiable; no de un archivo editable por la propia prueba. No basta bloquear un único nombre de Engine o contar que siguen existiendo 244 entradas.

## 5. Runner: un plan tipado, no coincidencias de texto

Reutilizar las políticas de v2.1 mediante adaptador explícito versionado. No pasarlo directamente al runner secuencial existente ni quitar sus candados. La especificación base mantiene `activation_status=DOCUMENTAL_NO_ACTIVO` y flags apagados; una activación futura requiere un contrato activable nuevo y autorización externa autenticada, no cambiar booleanos silenciosamente.

`execution-plan.json` tendrá un solo `steps` con campos obligatorios `id`, `type`, `adapter_id`, `verify_adapter_id`, `depends_on`, `required`, `timeout_seconds`, entradas/salidas y criterios de aceptación. El `type` se añade en el plan derivado, **no se adivina mirando `"smoke" in step_id` o `"mapa" in step_id`**.

Correspondencia propuesta con los IDs reales de v2.1:

| Etapa | type explícito | Función |
|---|---|---|
| S01_VALIDATE | VALIDATE | autorización, schemas, DAG y candados |
| S02_MAP | MAP | leer mapa/snapshot fijado; no llamar LLM por defecto |
| S03_SMOKE_GATE | SMOKE_GATE | gate real autorizado; no PASS constante |
| S04_CACHE | CACHE | sólo recibos reales válidos por hashes/permiso |
| S05_QUEUE | QUEUE | dependencias y leases; pendientes durables |
| S06_ISOLATE | ISOLATE | workspace/aislamiento revisado |
| S07_EXECUTE | EXECUTE | adaptador real o petición al bus |
| S08_VERIFY | VERIFY | verificador independiente, no el LLM creador |
| S09_CHECKPOINT | CHECKPOINT | reconciliar persistencia de pasos ya verificados |
| S10_FINALIZE | FINALIZE | evidencia, resumen y limpieza segura |

Registrar JSONL desde bootstrap y en cada transición, no esperar S10. Finalizador de error independiente de la secuencia: debe preservar lo disponible aunque falle S01. Cada paso real guarda su checkpoint al verificarse; S09 no retrasa todos los checkpoints hasta el final del batch.

Políticas heredadas: máximo tres workers para tareas independientes; heartbeat 5 s, stale 20 s, máximo de tarea 120 s incluyendo esperas/verificación y máximo de run 600 s; tres intentos totales para transitorios idempotentes, con esperas 5/15 s dentro del deadline. Timeout termina el grupo de procesos y reconcilia side effects; no reinicio infinito. Resume sólo desde el último checkpoint verificado con hashes idénticos y artefacto durable.

## 6. Pruebas reales, FIXTURE y CEB

Eliminar la función que retorna PASS incondicionalmente. Un fixture sirve para comprobar el transporte/contrato, no para demostrar ejecución de motor, búsqueda o calibración.

- `execution_kind=FIXTURE` se traduce a **`SIMULADO_FIXTURE`** para el reporte CEB; nunca cuenta como ejecución real de una pieza requerida, ni genera checkpoint de producción.
- Una prueba determinista que se ejecuta realmente puede probar una propiedad de infraestructura; eso no convierte sus datos sintéticos en búsqueda real o en resultado del motor.
- Una pieza requerida no invocada, API pendiente, intento fallido o fixture en lugar de ejecución real → **`FALLO_EJECUCION`**. Omisión sólo con contrato verificable; estado desconocido → `REQUIERE_CONTRATO`, no verde.
- La pausa documental actual se reporta `NO_EJECUTADO_POR_INSTRUCCION_DE_MJ`, no como fallo observado del motor.
- Pruebas iniciales reales, después de autorización: integridad de Engine/244; contratos y errores de entrada; CEB fixture/no-invocación; request/response/ACK del bus simulado; watchdog y checkpoint ante fallo. Para pruebas CEB ya existen los archivos citados; revisar dependencias y comportamiento antes de elegir los comandos exactos.
- Prueba posterior de un caso real de fábrica/Caldero: caso y corte temporal aprobados, salida aislada, recibos de proveedor y candados; no recalibrar pesos ni reescribir lotes de producción. No reusar el workflow que empuja manifiestos a `main`.

CEB verde para promoción exige piezas requeridas ejecutadas de verdad y verificadas, sin errores ocultos ni desactivar compuertas (`FABRICA_PIEZAS_REQUERIDAS=0` no es un arreglo). Un smoke de fixture puede pasar su prueba de infraestructura, **no autoriza promover el motor**.

## 7. Bridge LLM: contrato estricto sin fingir resultados

El puente no es el verificador final. Su trabajo es convertir una respuesta válida en una **propuesta** o solicitud estructurada. No asumir que un API LLM tiene el buscador de su app; búsqueda real requiere adaptador o receptor con capacidad comprobada.

### Suplemento propuesto `llm-bridge-response-v1.schema.json`

Esquema nuevo coherente con v2.1; **no se afirma que ya exista en el repo**. En la implementación posterior se validará tanto el esquema como las respuestas con Draft 2020-12 y resolución local, sin referencias de red implícitas. Rechazar JSON duplicado, NaN, texto/fences externos, tipos extraños, claves extra, payload >1 MiB o IDs fuera de la solicitud. Las correcciones de formato no vuelven segura una acción prohibida.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/marcojpad-hash/orquestador-central/schemas/llm-bridge-response-v1.schema.json",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "task_id", "request_id", "status", "result", "needs", "reason", "verified"],
  "properties": {
    "schema_version": {"const": "1.0"},
    "task_id": {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$"},
    "request_id": {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$"},
    "status": {"enum": ["PROPOSED", "NEEDS_ACTION", "REJECTED", "UNABLE"]},
    "result": {"type": ["string", "null"], "maxLength": 16000},
    "needs": {
      "type": "array", "maxItems": 4,
      "items": {
        "type": "object", "additionalProperties": false,
        "required": ["type", "query_or_test_id"],
        "properties": {
          "type": {"enum": ["SEARCH", "SANDBOX_TEST"]},
          "query_or_test_id": {"type": "string", "minLength": 1, "maxLength": 2000}
        }
      }
    },
    "reason": {"type": ["string", "null"], "maxLength": 2000},
    "verified": {"const": false}
  },
  "allOf": [
    {
      "if": {"properties": {"status": {"const": "PROPOSED"}}},
      "then": {"properties": {"result": {"type": "string", "minLength": 1}, "needs": {"maxItems": 0}}}
    },
    {
      "if": {"properties": {"status": {"const": "NEEDS_ACTION"}}},
      "then": {"properties": {"result": {"type": "null"}, "needs": {"minItems": 1}, "reason": {"type": "string", "minLength": 1}}}
    },
    {
      "if": {"properties": {"status": {"enum": ["REJECTED", "UNABLE"]}}},
      "then": {"properties": {"result": {"type": "null"}, "needs": {"maxItems": 0}, "reason": {"type": "string", "minLength": 1}}}
    }
  ]
}
```

El modelo no puede producir un veredicto `VERIFIED` ni un recibo de ejecución. El adaptador al formato batch de v2.1 completa `ok/status/evidence_refs/execution_kind` a partir del controlador y verificador, no copiando una afirmación del LLM. `REJECTED` y `UNABLE` son respuestas legítimas: registrar causa y enrutar sólo alternativas seguras y autorizadas.

### Reparación de formato: límite N explícito

Máximo **dos solicitudes de corrección**, tres respuestas totales, por salida malformada del modelo, dentro del presupuesto y deadline global; no múltiples bucles retry anidados. Enviar sólo errores de contrato sanitizados y conservar las respuestas fallidas sanitizadas. Agotado N → `CONTRACT_REJECTED`, sin ejecutar ni checkpoint.

Esto es una política suplementaria de reparación de **respuestas LLM**, no reintentar un contrato de job inválido (v2.1 lo bloquea). Autoridad insuficiente, rechazo de seguridad, permisos/API ausentes y esquema de entrada inválido no se “corrigen” insistiendo al modelo. Como puede consumir llamadas, queda apagada en esta fase y necesita presupuesto futuro.

### `NEEDS_ACTION` → bus, no “el LLM ya buscó”

`SEARCH` y `SANDBOX_TEST` son solicitudes distintas. El controlador valida su alcance, clasifica los datos, resuelve `query_or_test_id` contra adaptadores/test IDs permitidos y construye un request en el bus de `orquestador-central`. No ejecutar esa cadena como comando ni inventar que la app tiene búsqueda integrada.

Cada mensaje incluye conversation_id, instruction_id autenticada por referencia externa, parent/in_reply_to, idempotency_key, refs fijadas, TTL, hop_count y emisor/receptor ligados a identidad comprobada. ACK sólo prueba recepción. Mientras llega resultado real, paso `WAITING_DEPENDENCY`, sin PASS ni checkpoint. No mantener el runner dormido indefinidamente: persistir pendiente y continuar en otro run autorizado. Máximo seis turnos, leases/fencing, dead-letter y dedupe como v2.1. Sin receptor/API: `PENDIENTE_RECEPTOR`; no saltarse políticas ni falsificar resultado.

Los esquemas documentales del bus actual tienen `execution_authorized=false`: la futura fase activable debe crear un contrato compatible versionado, no desactivar el candado de la propuesta. La solicitud y su payload nunca conceden permisos.

## 8. Candados Engine/244, incluso dentro de sandbox

Antes y después de cada suite y antes de publicar evidencia/promover:

1. Obtener el inventario completo de Engine/244 y contratos protegidos desde baseline confiable de `main` fijada a SHA. Verificar también que esa política y el verificador no se cambiaron para relajar el candado.
2. Exigir diff vacío de esas rutas entre baseline y SHA de sandbox; no sólo diff desde el merge-base si éste oculta cambios acumulados.
3. Comprobar hashes del snapshot antes/después, cambios staged/unstaged, archivos borrados/renombrados/no rastreados y destinos de symlink. No basta `git diff` final: una prueba pudo modificar y restaurar. Montar fuentes protegidas readonly y rechazar escritura durante ejecución.
4. El verificador confiable falla si cualquier ruta protegida cambió. No auto-restaurar para ocultar el fallo ni regenerar manifiestos para legalizarlo.
5. Revalidar contra el `main` vigente antes de promoción; cambio de baseline o código invalida recibos previos.

La sandbox puede leer y ejecutar el motor autorizado, pero **no modificar Engine/244 ni siquiera experimentalmente**. Calibración significa medir/reportar, no ajustar pesos canónicos en esta tarea. Cualquier excepción necesitaría otro mandato; este documento no la concede.

## 9. Workflow: requisitos y esqueleto documental

### El problema real de los disparadores por rama

GitHub exige que el workflow de `workflow_dispatch` y `repository_dispatch` exista en la rama predeterminada. `repository_dispatch` ejecuta el workflow de esa rama, **no cambia automáticamente a `sandbox-testing`**. Por ello:

- Arranque mínimo: crear en sandbox el código y preparar un PR de **bootstrap** que añada exclusivamente el dispatcher manual revisado a `main`, sin disparadores push/cron y sin cambiar el motor. No fusionarlo sin Mj.
- Después del bootstrap aprobado, el dispatcher confiable de `main` selecciona el SHA autorizado de sandbox y prepara el job efímero. `workflow_dispatch` puede dirigirse a una ref, pero un dispatcher que va a publicar con credenciales debe mantener su lógica privilegiada en la ref confiable; no ejecutar el YAML arbitrario de sandbox con write.
- `repository_dispatch` recibe sólo tipo fijo e IDs/SHAs acotados. Validar actor, orden y pertenencia del SHA a `sandbox-testing`; payload no puede ampliar repos/rutas, activar permisos ni inyectarse en `run:`.
- Si se exige literalmente **cero cambios en `main`, incluido el dispatcher**, no prometer que esos eventos funcionarán con un workflow que existe únicamente en sandbox. Registrar `PENDIENTE_BOOTSTRAP`; alternativa posterior: dispatcher existente y aprobado de orquestador, con permiso cruzado y checkout remoto de sandbox. No cambiar la rama predeterminada como atajo.

Fuentes: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows y https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow .

### Esqueleto (NO instalado, NO listo para ejecutar)

Los jobs están deshabilitados deliberadamente con `if: false`; los SHA de acciones son marcadores. Antes de implementar deberán sustituirse por commits completos comprobados, materializar los adaptadores y someter el workflow a revisión. **No copiar ahora a `.github/workflows`.** Los comentarios describen obligaciones que no implementa el esqueleto.

```yaml
name: U6 sandbox controlado
on:
  workflow_dispatch:
    inputs:
      sandbox_sha:
        description: SHA completo autorizado de sandbox-testing
        required: true
        type: string
      instruction_id:
        description: Referencia de orden autenticada fuera del payload
        required: true
        type: string
  repository_dispatch:
    types: [u6_sandbox_request_v1]
permissions:
  contents: read
concurrency:
  group: u6-sandbox-control
  cancel-in-progress: false
jobs:
  authorize:
    if: ${{ false }}  # PREPARACIÓN: activar sólo tras autorización y contrato nuevo
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    permissions:
      contents: read
    # Validar evento/actor/orden externamente; checkout del control confiable fijado.
    # Comprobar ref sandbox-testing, SHA, schemas, permisos y política protegida.
    # Resolver lectura privada de orquestador mediante GitHub App mínima aprobada.
    # Emitir sandbox_sha, control_sha, policy_hash y receipts acotados/verificados.
    steps:
      - name: Autorización y fijación de fuentes
        run: exit 1  # Falla cerrada: falta implementar el controlador revisado.

  execute:
    if: ${{ false }}
    needs: authorize
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    permissions:
      contents: read
    # container: imagen-revisada@sha256:DIGEST_VERIFICADO  # opcional
    # Checkout del SHA de sandbox aprobado, persist-credentials false.
    # No secretos ni token de escritura en el entorno del código de pruebas.
    # Fuentes protegidas readonly, salidas temporales, red según allowlist.
    # Ejecutar plan tipado con adaptadores reales; verificar y persistir checkpoints.
    # En fallos preservar reporte y JSONL; nunca fabricar PASS.
    steps:
      - name: Ejecutor pendiente de implementación
        run: exit 1
      - name: Conservar evidencia incluso ante fallo
        if: always()
        uses: actions/upload-artifact@SHA_COMPLETO_VERIFICADO
        with:
          name: sandbox-${{ github.run_id }}-${{ github.run_attempt }}
          path: artifacts/
          if-no-files-found: error
          retention-days: 14

  publish-evidence:
    if: ${{ false }}
    needs: [authorize, execute]
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    permissions:
      contents: write
      actions: read
    # En la implementación: correr incluso si execute falla, pero sólo con authorize válido.
    # Control confiable fijado; descargar artefacto del run propio; NUNCA ejecutarlo.
    # Verificar/sanitizar; commit único sólo avances/sandbox/<run>-<attempt>/
    # a sandbox-testing. Releer ref, CAS y reconciliar conflictos sin force-push.
    # Un fallo de escritura deja EVIDENCIA_PENDIENTE_COMMIT, no éxito silencioso.
    steps:
      - name: Publicador confiable pendiente de implementación
        run: exit 1
```

Este esquema **no demuestra ninguna prueba pasada**. Al materializarlo, la implementación debe conservar incluso errores de autorización con reporte mínimo sanitizado sin conceder escritura. `always()` no debe convertirse en permiso para publicar si falló autorización. No usar `pull_request_target` para ejecutar código de sandbox con Secrets.

Si se elige Compose: imagen fijada por digest, sin `build: .` arbitrario sin revisión, mounts readonly de fuentes, salida separada writable, usuario no root, sin Docker socket y timeout aplicado al grupo completo. `SANDBOX_MODE` es metadato, no control de acceso. No instalar un segundo servidor persistente ni `init_sandbox.sh` que Mj tenga que correr.

## 10. Evidencia, publicación y promoción

**Dos copias de evidencia futura:** artefactos Actions y archivos sanitizados append-only en `sandbox-testing/avances/sandbox/<run_id>-<attempt>/`. Nunca JSONL compartido con varios jobs escribiendo ni commits a `main` de los workers. Correcciones = nueva entrada/evento, no reescribir el pasado. JSONL incluye event_id, run/task/step/attempt, estado, execution_kind, proveedor, duraciones, errores sanitizados y refs/hashes. Reportar horas humanas en CDMX.

El publicador centraliza escritura y verifica diff de commit limitado a avances. No publicar secretos, entradas sensibles ni el workspace entero. Conservar evidencia de fallo antes de limpiar; error de artefacto/commit se reporta, no se traga con `|| true`. Una nueva evidencia commit cambia HEAD: el reporte debe distinguir **SHA de código probado** de **SHA de commit de evidencia**. La promoción exige probar/verificar el SHA final candidato o acreditar rigurosamente el diff sólo documental; preferir nuevo run fijado si hay duda. No fingir que un check de un SHA viejo cubre el PR actual.

Promoción a `main` exclusivamente mediante PR, con:

- Diff acotado a laterales/runner y documentación autorizados, sin Engine/244 ni cambio de contrato canónico.
- CEB verde real, candados y pruebas de aceptación del SHA candidato; fixtures separados.
- Baseline y recibos vigentes; resolución de conflictos sin force-push ni regeneración evasiva de hashes.
- Protección de `main`: PR obligatorio, checks requeridos, sin force-push/borrado ni bypass por el bot; invalidar aprobaciones al cambiar contenido relevante. Si no está configurada, informar al administrador autorizado; Contents/PR write no permite garantizarla ni habilitarla por sí solo.
- **Un único “merge” explícito de Mj**, asociado al PR y SHA ya revisados. No sustituirlo por un verde, etiqueta, texto del LLM o aprobación de otro agente. Si cambia el SHA de código tras aprobar, la autorización anterior no cubre ese cambio.

El PR de bootstrap requiere su propio “merge” cuando llegue el momento, porque añade infraestructura a `main`; no usar la aprobación futura del motor para aprobarlo retroactivamente. No hay auto-merge ni autoaprobación.

## 11. Criterios de aceptación (diseñar ahora, ejecutar sólo después)

1. El runner lee v2.1 fijada a SHA y deriva un único `steps` tipado, sin búsquedas por substring; schema/adapter explícitos y versiones registradas.
2. Falta de autorización, SHA/ref incorrectos o esquema de configuración ausente bloquean sin ejecutar; no simular `SANDBOX_READY` tras error de Git.
3. Prueba de fallo real falla, suite que no se invoca aparece como no ejecutada, fixture se etiqueta y jamás vuelve verde una pieza requerida de CEB.
4. Respuestas LLM válidas pasan sólo el contrato; formatos inválidos agotan N y bloquean. `REJECTED/UNABLE` no disparan intentos para evadir políticas. `NEEDS_ACTION` produce mensaje correlacionado, no ejecución inventada.
5. Bus demuestra dedupe, leases, ACK real y expiración; ausencia de receptor queda pendiente. Prueba con fixtures del bus no se presenta como dos modelos conversando realmente.
6. Cualquier diff/hash/escritura sobre Engine/244 bloquea, incluso dentro de sandbox; CI verifica política confiable y baseline, no sólo nombre de archivos.
7. Timeout detiene procesos; checkpoint sólo tras verificador real; hashes alterados invalidan resume; no avanzar dependencias con PASS constante.
8. JSONL y manifiestos se conservan en artefactos y avances de sandbox con escritor único; fallos también, sin secretos ni ejecución de artefactos en el publicador privilegiado.
9. Ningún paso ejecuta/pushea motor en `main`; bootstrap manual explícito, triggers sin push/cron al comienzo, protecciones comprobadas y promoción mediante PR + “merge” de Mj.
10. Entrega futura totalmente cableada por el agente: enlaces a rama, workflow, runs, artefactos, avances, PR y hashes; distinguir IMPLEMENTADO, EJECUTADO, VERIFICADO y PENDIENTE. No pedir a Mj cableado manual.

**Estado actual de todos esos criterios:** especificados, no probados. No se ha levantado una VM ni ejecutado una prueba con este documento.

## 12. Decisión A/B/C

**Recomendación: C + A mínimo, en ese orden.** C significa preparar rama y workflow hospedado con candados; A significa después añadir pruebas reales pequeñas y adaptadores explícitos de búsqueda/verificación. No significa que un prompt active el buscador de una app ni calibración automática de pesos. B (suite de PASS ficticio) aporta poco: conservar únicamente fixtures útiles para probar contratos y fallos, separados de resultados reales.

Primero preparar infraestructura y su PR de bootstrap; después de autorización de ejecución, un smoke real de integridad/CEB, y sólo entonces un caso real acotado. No arrancar con fábrica masiva, todos los modelos y calibración a la vez.

## 13. Bloque de tres líneas para Grok (para después, cuando Mj decida)

> Lee `marcojpad-hash/orquestador-central/docs/INSTRUCCION_SANDBOX_VM.md`, la instrucción del puente y `docs/orchestrator.v2.1.json`; prepara `sandbox-testing` en `motor-u6-storage` con runner tipado, esquemas, candados y workflow Actions según ese contrato.
> No ejecutes ni hagas dispatches todavía; prepara el bootstrap manual necesario mediante PR, sin modificar Engine/244, secretos o permisos ni fusionar a main; tú cableas todo, yo no.
> Entrega rama, diff y PR con lo implementado y lo pendiente; después decidiré la ejecución y daré “merge” únicamente al PR/SHA aprobado.
