# Contrato de agentes especialistas

## Registro mínimo de agente

- agent_id
- display_name
- specialty
- supported_projects
- capabilities
- prohibited_actions
- accepted_input_schema
- output_schema
- provider
- endpoint/adapter_ref
- availability
- permission_scope
- verification_requirements

## Asignación

El router selecciona por:
1. Especialidad demostrada.
2. Compatibilidad con reglas del proyecto.
3. Herramientas y acceso realmente disponibles.
4. Disponibilidad y límites.
5. Calidad histórica verificada.
6. Coste y latencia, cuando se conozcan.

No seleccionar por marca o popularidad sin evidencia.

## Delegación

Toda tarea delegada contiene:
- instruction_id y task_id.
- Objetivo y contexto mínimo suficiente.
- Archivos/repositorios autorizados.
- Límites y acciones prohibidas.
- Entregable esperado.
- Criterios de aceptación.
- Plazo, si fue indicado.
- Forma de reportar evidencia.

## Resultados

El agente devuelve:
- status: completed | partial | blocked | failed
- summary
- artifacts
- changed_paths
- commit_or_run_refs
- tests_and_results
- assumptions
- unresolved_questions
- provenance

El coordinador verifica el resultado. La afirmación del agente no constituye por sí sola evidencia de ejecución.
