# Guardianes operativos agnósticos
**Versión:** 1.0  
**Tipo:** especificación funcional de controles operativos  
**Alcance:** sistemas de agentes, automatizaciones, pipelines y trabajos ejecutables de cualquier dominio.  
**No es:** una copia de guardianes U6, un contrato de patrones ni una implementación ligada a un lenguaje, framework o motor.

## 1. Principio de extracción
Se extraen responsabilidades y comportamientos observables, no nombres internos, fórmulas, contratos, estructuras de datos ni dependencias de U6. Un guardián es agnóstico si puede especificarse y probarse sin conocer patrones, vectores, hipótesis, fórmulas ni estados privados de un motor particular.

## 2. Separación de capas
- **Política cognitiva de interacción:** cómo interpretar instrucciones y trabajar con Mj; definida en `COMO_TRABAJAR_CON_MJ.md`.
- **Gobierno transversal:** autoridad, alcance, permisos, seguridad, concurrencia y evidencia.
- **Control operativo:** supervisión de procesos, workers, colas, recursos, tiempos, reintentos, aislamiento y validación.
- **Adaptadores de proyecto:** traducen señales y resultados locales a interfaces comunes.
- **Controles especializados:** lógica propia de un motor o dominio; permanece en su proyecto y no se generaliza por analogía.

## 3. Catálogo funcional
| Control | Función independiente de implementación | Condición de intervención | Evidencia mínima |
|---|---|---|---|
| Orquestador / planificador | Descompone un objetivo en unidades, fija dependencias, orden y criterios de aceptación. | Antes de iniciar una ejecución multi-paso. | Plan, dependencias y estado de cada unidad. |
| Runner / ejecutor | Ejecuta una unidad autorizada en el entorno declarado. | Cuando precondiciones y permisos están satisfechos. | ID de ejecución, entrada, entorno, salida y código de retorno. |
| Worker | Realiza una unidad delimitada sin apropiarse de la autoridad global. | Cuando recibe tarea, contexto mínimo y límites explícitos. | Resultado, archivos afectados y estado. |
| Cola | Conserva tareas pendientes, asignadas, en curso, terminadas o fallidas. | Cuando hay concurrencia, espera o capacidad limitada. | Identificador estable y transiciones de estado. |
| Contrato de entrada/salida | Comprueba que los datos cumplen estructura y restricciones declaradas. | Antes de ejecutar y al producir salida. | Resultado de validación y errores por campo/paso. |
| Verificador | Contrasta el resultado con criterios mecánicos y reproducibles. | Después de cada paso y al cierre. | Comando/check, versión, salida y PASS/FAIL. |
| Logger / registro | Conserva eventos relevantes con tiempo, correlación y origen. | Durante todo el ciclo de vida. | Eventos ordenados y vinculables a la ejecución. |
| Monitor | Observa salud, progreso, consumo y señales de fallo. | Durante ejecuciones activas. | Métricas, umbrales y alertas. |
| Watchdog | Detecta ausencia de progreso, bloqueo o vencimiento de plazo. | Al superar un umbral definido sin señal de vida/progreso. | Último progreso, umbral y acción tomada. |
| Gestor de límites | Impone cuotas de tiempo, intentos, concurrencia, memoria u otros recursos. | Antes y durante la ejecución. | Límite configurado, medición y resultado. |
| Política de reintentos | Decide si un fallo es transitorio y si se permite reintentar, con límite y espera. | Solo para clases de error declaradas como recuperables. | Causa, número de intento y decisión. |
| Aislamiento / sandbox | Limita archivos, red, secretos, permisos y efectos laterales de una tarea. | Cuando el trabajo ejecuta código o toca recursos no confiables. | Perfil de aislamiento y recursos permitidos. |
| Recuperación | Reanuda desde el último punto seguro o revierte efectos parciales. | Ante fallo recuperable o interrupción. | Punto de recuperación, acciones y estado final. |
| Auditor independiente | Revisa salida y evidencia sin depender del relato del ejecutor. | Cuando riesgo o contrato exige separación de funciones. | Dictamen y criterios comprobados. |

## 4. Ciclo de control
1. **Admisión:** identificar objetivo, autoridad, alcance, entrada, salida y riesgo.
2. **Preparación:** validar contrato, permisos, recursos y dependencias.
3. **Ejecución:** asignar worker/runner; registrar inicio y correlación.
4. **Supervisión:** observar progreso, límites, logs y señales de vida.
5. **Control de paso:** verificar cada salida antes de liberar el paso siguiente.
6. **Recuperación:** clasificar fallo; reintentar solo si está permitido y es seguro.
7. **Cierre:** validar salida final, registrar evidencia y liberar recursos.
8. **Auditoría:** revisión independiente cuando corresponda.

## 5. Estados comunes
`DRAFT`, `READY`, `QUEUED`, `RUNNING`, `WAITING`, `PASSED`, `FAILED`, `BLOCKED`, `CANCELLED`, `RECOVERING`, `COMPLETED`.  
Los proyectos pueden mapear sus estados locales a estos estados; no tienen que renombrar sus estados internos.

## 6. Reglas de seguridad y recuperación
- No reintentar automáticamente acciones no idempotentes sin mecanismo de deduplicación o compensación.
- No repetir toda una cadena si el contrato permite reanudar desde el primer paso fallido.
- Un fallo de verificación bloquea únicamente los pasos dependientes, salvo que comprometa la integridad global.
- El watchdog detecta y reporta; no debe matar procesos ni borrar datos sin política explícita.
- El sandbox limita daños; no reemplaza revisión de permisos ni validación.
- Logs no deben almacenar secretos ni datos sensibles innecesarios.
- Los límites y reintentos deben ser finitos, configurables y visibles.
- El ejecutor no puede validar por sí solo una salida cuando el contrato exige verificador independiente.

## 7. Resultados de los controles
- `PASS`: evidencia suficiente; continuar.
- `WARN`: riesgo aceptado y registrado; continuar solo si la política lo permite.
- `BLOCK`: detener la unidad afectada y dependencias.
- `NOT_APPLICABLE`: control no pertinente; razón registrada cuando importe.

## 8. Prueba de agnosticismo
Un control solo se etiqueta **AGNÓSTICO_VALIDADO** cuando:
1. su definición no menciona conceptos privados de un proyecto;
2. sus entradas y salidas se expresan mediante una interfaz neutral;
3. puede probarse con al menos dos implementaciones o proyectos distintos;
4. no necesita importar código, patrones ni datos del motor de origen;
5. su prueba demuestra el mismo comportamiento funcional en ambos contextos.

Hasta entonces, etiquetar **AGNÓSTICO_PROPUESTO**. La similitud de nombres o intención no demuestra independencia.

## 9. Relación con U6
U6 es una fuente de experiencia y casos de prueba, no una dependencia del coordinador. Los controles de latencia, revisión adversarial, consistencia, polaridad, hipótesis, patrones o cualquier otro mecanismo cognitivo propio permanecen especializados hasta que se formule una abstracción neutral y se pruebe fuera de U6. No modificar el motor ni el catálogo para desarrollar esta especificación.
