# Convención de marcas y contratos

## Principio
Una marca declara el tipo de contrato; no ejecuta nada por sí sola. El consumidor debe reconocerla, cargar el contrato correcto, validarlo y detener la ejecución si falla.

## Marcas por formato
- Markdown: YAML frontmatter entre `---`. Campos mínimos del arquetipo: `name`, `description`, `archetype`. Solo un loader/validador que inspeccione esos campos puede activarlo.
- JSON: `$schema` debe apuntar al archivo de esquema publicado y `_contract` identifica la versión del contrato de ejecución. El runner carga el esquema local autorizado y valida el documento antes de ejecutar.
- Código: shebang (`#!`) selecciona intérprete; no es marca de arquetipo. Una pragma como comentario `# @archetype: sequential-verifiable-v1` puede declarar intención, pero solo herramientas que la inspeccionen la reconocen.
- Design by Contract: las precondiciones se comprueban antes de cada paso; las postcondiciones después. Fallo = BLOCK y no se continúa.
- Magic bytes: identificación de formatos binarios, no activador de contratos de agentes.

## Arquetipo secuencial
El runner reconoce exclusivamente `SEQUENTIAL-VERIFIABLE-v1` y su URI de esquema canónica. No interpreta marcas desconocidas como autorización. Ejecuta adaptadores Python locales sin shell, registra eventos y comprueba condiciones declaradas.

## Ejemplo frontmatter
```yaml
---
name: sequential-verifiable
description: Trabajo secuencial con validación mecánica
archetype: sequential-verifiable-v1
---
```

## Regla de seguridad
No se ejecuta un archivo Markdown por tener frontmatter. El frontmatter habilita clasificación/validación, nunca autorización para ejecutar código arbitrario. La autorización, el alcance y las capacidades siguen siendo guardianes independientes.
