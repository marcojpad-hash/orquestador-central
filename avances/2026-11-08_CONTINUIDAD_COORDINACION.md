# Handoff — continuidad de coordinación

- instruction_id: MJ-CONTINUIDAD-20261108; origen: mensaje directo de Mj, referencia de conversación pt1064u. Texto conservado en el registro de `COORDINATION/COMO_TRABAJAMOS.md`. Esta referencia identifica procedencia; no es un token de autenticación para un servicio.
- Objetivo: que el siguiente modelo continúe desde GitHub sin depender de este bot ni sus créditos.
- Repo de autoridad: `marcojpad-hash/orquestador-central`; publicación documental solicitada. SHAs entregados: consultar historia de los archivos/commits de esta entrega; el documento no inventa SHA de sí mismo.
- Alcance: guía COMO_TRABAJAMOS, punteros README/AGENTS, conciliación de instrucción runtime + v2.1 + sandbox; instrucciones y prompts autocontenidos para Muse de VM persistente/gateway y pipeline CAPCOT. No cambios en código, workflows, permisos, secretos, motor, CAPCOT ni ledger.
- Hechos: fuentes reales leídas por API; `REGISTRY/PROJECTS.yaml` incluye CAPCOT y deja Imaginantes sin repo separado; workflows de orquestador revisados no se disparan por estas rutas documentales. Cambios remotos se acreditan sólo tras recibo de escritura y relectura.
- Consistencia: v2.1 no es schema ejecutable; concurrencia máxima tres; formatos LLM requieren suplemento distinto de retry de job inválido; publicación documental autorizada no activa runtime ni sustituye PR/merge de producción; gateway persistente nuevo complementa jobs aislados Actions.
- Hallazgos CAPCOT: plantilla +4%/fallback y README con otras voces contradicen JorgeNeural +7%/−2Hz sin fallback; se documenta corrección futura, sin editar CAPCOT. QA vigente duración 60–120s; no publicar videos en este encargo.
- Pruebas: NO_EJECUTADAS_POR_INSTRUCCION_DE_MJ. Sin parser/validador de contratos, motor, instalación, smoke, APIs LLM, render, publicación audiovisual ni dispatches.
- Estado de agentes: reparto documental, capacidades/endpoints de Muse y demás por comprobar. No bus/gateway/VM operativos acreditados.
- Siguiente acción: el modelo que retome lee COMO_TRABAJAMOS y la última orden; puede preparar lo autorizado sin esperar al bot. Muse recibe `docs/PROMPT_MUSE_VM.md` o `docs/PROMPT_MUSE_VIDEO.md`; si no tiene acceso, entrega bundle completo al implementador autorizado. Aprovisionar/correr necesita otra autorización; merge requiere PR/SHA y aprobación de Mj.
- Handoff: ENTREGADO documentalmente cuando se confirme su escritura; ningún receptor externo se declara RECIBIDO sin ACK real.
