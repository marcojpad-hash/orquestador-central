# orquestador-central
Orquestador central: plano de control, reglas globales, memoria compartida, registro de órdenes y enrutador de agentes.

## Gobierno universal
1. [Reglas operativas universales](docs/REGLAS_OPERATIVAS_UNIVERSALES.md) — reglas obligatorias para cualquier trabajo, agente o proyecto.
2. [Arquitectura del coordinador central](docs/ARQUITECTURA_COORDINADOR_CENTRAL.md) — relación entre el coordinador y los repositorios autónomos.
3. [Contrato de trabajo multi-modelo](docs/CONTRATO_TRABAJO_MULTI_MODELO.md) — operación entre agentes y modelos.
4. [Registro de capacidades](docs/CAPACIDADES_MODELOS.md) — capacidades verificadas por interfaz y sesión.
5. [Plantilla de handoff](docs/PLANTILLA_HANDOFF_MULTI_MODELO.md) — continuidad entre agentes.

## Inicio obligatorio para cualquier modelo
1. Leer las reglas operativas universales.
2. Leer la arquitectura y el contrato multi-modelo.
3. Declarar/actualizar capacidades en el registro.
4. Leer README, AGENTS.md y contrato local del proyecto afectado.
5. Confirmar repositorio, rama, commit, permisos y alcance antes de escribir.

## Autoridad
Este repositorio gobierna reglas transversales y coordinación. Cada repositorio especializado conserva la autoridad sobre su propio código, datos, contratos y entregables. Los demás repositorios no son ramas de este: se conectan mediante referencias, contratos, registros y handoffs.
