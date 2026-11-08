# Runtime ejecutable (MVP)

## Qué está conectado
- GitHub Actions ejecuta el runner en un entorno efímero aislado del runner hospedado.
- El runner exige marca y contrato `SEQUENTIAL-VERIFIABLE-v1`, procesa pasos en orden y bloquea la cadena al primer fallo.
- Cada ejecución escribe eventos JSONL con inicio, comandos, tiempos, salida, fallo y cierre.
- Cada comando tiene timeout; se ejecuta sin shell, con entorno reducido y scripts Python confinados al workspace.
- El workflow usa permisos mínimos de solo lectura, desactiva persistencia de credenciales y conserva logs/salidas como artefacto.

## Cómo lanzar
En GitHub: Actions → Sequential Verifiable Runner → Run workflow. El input por defecto ejecuta el ejemplo integrado. Se puede indicar otra ruta JSON marcada.

## Contrato de los pasos
`action` y `verify` son comandos directos `python ruta/al_adaptador.py argumentos...`; no se permite shell ni ejecutables arbitrarios en este MVP. Los adaptadores deben vivir dentro del repositorio. No introducir entradas no confiables en workflows ejecutables.

## Límites explícitos
- Esto es un MVP de ejecución dentro de un repositorio, no un orquestador multi-repo ni un servicio persistente 24/7.
- La cola/concurrencia usa la primitiva de GitHub Actions; no existe todavía una base de datos de tareas.
- El sandbox es el runner efímero hospedado por GitHub, no una VM privada persistente.
- El watchdog inicial son timeouts de comando y job; no detecta todavía bloqueos semánticos.
- Los logs son artefactos de Actions, no almacenamiento permanente.
- No se conecta a proveedores LLM ni MCP: los controles deterministas no necesitan API. La integración MCP se añadirá como adaptador cuando haya un servicio MCP concreto que consumir.
