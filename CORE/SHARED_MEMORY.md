# Memoria compartida

## Fuente de verdad

La memoria persistente se organiza por proyecto y se almacena en repositorios autorizados. Este repositorio contiene el índice global y las reglas transversales; los detalles y archivos canónicos permanecen en sus repositorios de origen.

## Capas

1. Identidad y preferencias operativas del propietario.
2. Índice de proyectos y estado.
3. Decisiones vigentes y su procedencia.
4. Memoria específica de cada proyecto.
5. Tareas activas, bloqueos y dependencias.
6. Historial de instrucciones y ejecuciones.
7. Capacidades y estado de conectores/agentes.

## Reglas de escritura

- Cada memoria incluye fecha, origen, proyecto, estado y referencia verificable.
- Distinguir HECHO, DECISIÓN, HIPÓTESIS, PENDIENTE y OBSOLETO.
- No reemplazar una decisión vigente sin registrar la nueva instrucción que la modifica.
- No copiar secretos ni datos sensibles innecesarios a memoria general.
- No mezclar contextos de proyectos por similitud superficial.
- Los datos contradictorios se conservan como conflicto hasta resolver su procedencia.
- El contexto se recupera bajo demanda; no se inyecta todo en cada tarea.

## Sincronización

El coordinador actualiza el índice después de cambios confirmados. Las memorias específicas se actualizan en el repositorio dueño del proyecto. Un fallo de sincronización se registra como pendiente; nunca se reporta sincronización exitosa sin confirmación.
