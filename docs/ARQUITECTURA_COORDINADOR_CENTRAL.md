# Arquitectura del coordinador central
**Versión:** 0.1  
**Estado:** diseño operativo inicial.

## 1. Propósito
`orquestador-central` es el plano de control común de los proyectos. Gobierna cómo se organiza y verifica el trabajo; no absorbe el código ni los datos de los proyectos.

## 2. Modelo: plano de control y repositorios autónomos
No existe una jerarquía nativa de repositorios en GitHub donde uno sea padre y los demás ramas. Los repositorios mantienen historias, permisos, ramas, releases y ciclos propios.

La relación se implementa mediante contratos enlazados, un registro central y handoffs:

```text
                 orquestador-central
             (reglas y plano de control)
                        |
        +---------------+----------------+
        |               |                |
   CAPCOT repo       Motor U6 repo    Otros repos
   contrato local    contrato local  contrato local
   cola y medios     motor y tests   artefactos propios
```

El coordinador no copia ni centraliza los archivos canónicos de los proyectos. Registra dónde están y quién tiene autoridad sobre ellos.

## 3. Capas del coordinador
1. **Gobierno:** reglas universales, seguridad, autoridad y criterios de cierre.
2. **Registro:** catálogo de proyectos, repositorios, ramas principales, responsables, contratos y estado.
3. **Agentes:** identidades e interfaces concretas, capacidades verificadas, permisos y costos.
4. **Planificación:** órdenes, subtareas, dependencias, prioridad y criterios de aceptación.
5. **Ejecución:** enrutamiento a herramientas/agentes especializados; no presume que el coordinador pueda ejecutar todo.
6. **Guardianes:** controles transversales antes/durante/después de una acción.
7. **Evidencia:** pruebas, commits, recibos, logs, hashes y auditorías.
8. **Continuidad:** memoria de decisiones, handoffs y recuperación entre sesiones.

## 4. Autoridad documental
- Este repositorio es autoridad para reglas globales, catálogo y coordinación.
- Cada repositorio de proyecto es autoridad para su código, datos, contratos y resultados locales.
- Un proyecto enlaza la versión vigente de las reglas globales desde su README/AGENTS.md.
- Si un proyecto necesita una excepción, la documenta localmente con motivo y alcance; no modifica silenciosamente la regla global.

## 5. Registro central mínimo
Cada proyecto debe registrar:
- project_id y nombre;
- repositorio y visibilidad;
- rama activa y commit conocido;
- README, AGENTS y contrato local;
- archivos protegidos y restricciones;
- agentes autorizados y permisos confirmados;
- estado operativo y último handoff;
- pruebas de aceptación y responsable de QA.

Cada agente debe registrar identidad exacta, interfaz, capacidades probadas, permisos, límites, costo y fecha de verificación.

## 6. Flujo de una orden
1. Recibir solicitud y clasificarla como consulta, análisis, propuesta o ejecución.
2. Identificar proyectos y contratos afectados.
3. Consultar estado y evitar duplicación.
4. Descomponer en subtareas y asignar responsables.
5. Ejecutar guardianes de intención, autoridad, alcance, capacidad y seguridad.
6. Ejecutar y probar.
7. Ejecutar guardianes de evidencia, calidad y continuidad.
8. Registrar resultado en los repositorios adecuados.
9. Entregar cierre con pruebas y bloqueos externos, si existen.

## 7. Relación con los guardianes de Motor U6
La idea de guardianes/firewall desarrollada alrededor de U6 se trata como antecedente y posible fuente de patrones, no como paquete que se copia entero al coordinador. Primero se separan:
- controles operativos universales (aplicables a cualquier trabajo);
- controles de seguridad y gobernanza;
- guardianes especializados del motor predictivo U6.

No modificar el motor, patrones ni contratos canónicos para extraer esta capa. La extracción se hará mediante análisis y adaptación en un módulo independiente.

## 8. Separación entre comportamiento, guardianes y arquetipos\n1. **Comportamiento de interacción:** `docs/COMO_TRABAJAR_CON_MJ.md`. Regula cómo se interpreta y conduce el trabajo con Mj; no es lógica de ejecución.\n2. **Guardianes operativos agnósticos:** `docs/GUARDIANES_OPERATIVOS_AGNOSTICOS.md`. Especifica funciones de control por responsabilidades observables, sin importar código ni contratos de U6.\n3. **Arquetipos de familia:** documentos independientes con activación explícita. El primero es `docs/ARCHETYPE-SEQUENTIAL-VERIFIABLE-v1.md`, acompañado por su JSON Schema y ejemplo. Sin marca reconocida no se aplica; con marca pero sin runner compatible, permanece declarado y no ejecutado.\n4. **Adaptadores de proyecto:** cada repo decide si adopta el arquetipo y cómo integra sus controles. La autoridad local sigue gobernando detalles técnicos y restricciones.\n\nLa extracción desde U6 debe ser semántica: conservar la función útil de un control, reformularla en términos neutrales y probarla fuera del motor. No copiar implementaciones, nombres internos, dependencias, patrones ni contratos del motor.\n\n## 9. Secuencia de implementación
**Fase 1 — Normativa:** reglas universales, contrato multi-modelo y guardianes definidos.
**Fase 2 — Inventario:** registro de repositorios, contratos, ramas, agentes, permisos y responsables.
**Fase 3 — Operación:** órdenes, estados, handoffs y bitácora central.
**Fase 4 — Automatización:** validadores y guardianes automáticos donde exista una prueba objetiva.
**Fase 5 — Integración:** enlaces y validación de cumplimiento en los repositorios de proyecto.

No automatizar una regla ambigua. Primero debe existir una definición comprobable y casos de prueba.

## 10. Principio de diseño
El coordinador central dirige y verifica; los proyectos conservan autonomía técnica; los agentes ejecutan según capacidad real; el usuario mantiene la autoridad final sobre objetivos, decisiones reservadas y permisos.
