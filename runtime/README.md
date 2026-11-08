# Runtime ejecutable (MVP)

## Qué está conectado
- GitHub Actions es el coordinador hospedado: no requiere PC, servidor propio ni n8n.
- El runner exige marca y contrato `SEQUENTIAL-VERIFIABLE-v1`, procesa pasos en orden y se detiene al primer fallo.
- Cada ejecución escribe eventos JSONL; los workflows conservan logs y salidas como artefactos durante 14 días.
- Los comandos del runner son adaptadores Python locales, sin shell, con timeout, entorno reducido y confinamiento al repositorio.
- Los validadores JSON Schema y YAML se instalan desde `runtime/requirements.txt` tanto en CI como en ejecución manual.

## Uso desde Android
1. Abrir el repositorio en GitHub.
2. Entrar en **Actions**.
3. Elegir **Sequential Verifiable Runner** y pulsar **Run workflow**.
4. Mantener la ruta de ejemplo o indicar un contrato JSON marcado que ya exista en el repositorio.
5. Consultar el resultado y descargar el artefacto de ejecución.

## Cerebro LLM opcional
El workflow **AI Task Assistant** permite enviar una instrucción a Groq o Gemini mediante una API key guardada como GitHub Secret. La respuesta se conserva como artefacto; no ejecuta código, no modifica repositorios y no publica cambios automáticamente. Esto separa razonamiento probabilístico de ejecución determinista y evita que una respuesta del modelo se convierta directamente en una orden privilegiada.

Secrets requeridos según proveedor:
- Groq: `GROQ_API_KEY`.
- Gemini: `GEMINI_API_KEY`.

El modelo se elige al lanzar el workflow. Los nombres, cuotas y disponibilidad dependen del proveedor y deben verificarse allí; no se asume gratuidad permanente ni fallback automático. No pegues claves en archivos, prompts, issues ni commits.

## Contrato de pasos
`action` y `verify` son comandos directos `python ruta/al_adaptador.py argumentos...`; no se permite shell ni ejecutables arbitrarios en este MVP. Los adaptadores deben vivir dentro del repositorio. No introducir entradas no confiables en workflows ejecutables.

## Límites explícitos
- MVP hospedado por GitHub Actions; no es un servicio persistente 24/7 ni una cola multi-repo.
- No hay todavía escritura automática a repositorios hijos. Para eso hace falta definir un token de alcance mínimo y permisos confirmados por repositorio.
- La IA produce propuestas, no tiene autoridad para aprobar, desplegar, publicar o modificar archivos.
- Los logs son artefactos de Actions, no almacenamiento permanente.
- Los guardianes deterministas pueden bloquear entradas y ejecuciones; la intención, autoridad y permisos siguen requiriendo declaración y verificación explícitas.
