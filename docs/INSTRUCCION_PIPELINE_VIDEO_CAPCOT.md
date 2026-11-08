# Pipeline propio CAPCOT: storyboard → voz oficial → visuales → MP4 → QA

**Preparación documental. Sin generación, render, instalación, publicación ni workflows en esta entrega. 8 de noviembre de 2026, CDMX.**

Leer primero [`COORDINATION/COMO_TRABAJAMOS.md`](../COORDINATION/COMO_TRABAJAMOS.md). El código y datos del producto pertenecen a `marcojpad-hash/capcot-capsulas-imaginantes`, no al repo de motor ni a esta documentación. Mj no cablea nada; otro modelo implementará el paquete completo cuando se autorice.

## 1. Reutilizar lo existente, no reconstruir otro CAPCOT

Rutas consultadas vía GitHub:

- `docs/RECETA_CAPSULA.md`: narrativa, voz, estructura, estilos, fuentes, audio y criterios.
- `docs/AHORRO_RECURSOS_PIPELINE.md`: **frames estáticos + FFmpeg**, preview 540×960 antes de HD, I2V excepcional.
- `ajustes_entre_modelos/HANDOFF_GROK_PRODUCCION.md` y `salidas/_ops/2026-10-28_HANDOFF_TOTAL_grok_principal.md`: handoffs existentes. Referencias históricas de fecha/cuota no sustituyen el estado actual.
- `templates/storyboard_vertical.template.json`, `proyectos/<id>/storyboard.json`, `cola/entrada/<id>/storyboard.json`: entradas reales. Ejemplos recientes: `proyectos/2026-11-07_barreleye-4k/storyboard.json` y su paquete de cola.
- `scripts/validar_storyboard.py`, `scripts/generar_frames.py`, `scripts/montar_capsula.py`, `scripts/qa_capsula.py`, `scripts/metadata.py`, `tools/tts/narrate.py`: componentes ya existentes; leer contratos/flags antes de extenderlos.

**No tocar ahora esos archivos ni generar paquetes en una cola activa.** Preparar después cambios pequeños en una rama del repo CAPCOT y PR, no implementar un segundo renderer en orquestador.

### Contradicciones detectadas que la implementación futura debe corregir

`templates/storyboard_vertical.template.json` aún contiene `rate: +4%` y fallback a otra voz; `tools/tts/README.md` permite voz alternativa/Piper. Eso contradice la regla vigente de ahorro y la petición de Mj. **Prevalece `es-MX-JorgeNeural`, `rate=+7%`, `pitch=-2Hz`, motor edge-tts, sin fallback de voz.** Si el endpoint no responde, tarea bloqueada/reintentable con límites y se conserva paquete, no voz nueva ni PASS simulado. El script `tools/tts/narrate.py` declara ya esos defaults correctos; defaults no bastan si la entrada puede cambiarlos: el validador debe imponerlos.

La receta tiene referencias antiguas a 75–90/60–95 s y una actualización posterior que acepta 60–120 s; el QA actual comprueba **60–120 s**. Respetar esta última regla sin inflar con silencio y medir audio real. La plantilla 16:9 antigua no es la entrada vertical vigente. Ningún texto histórico que permita `--publicar` autoriza publicación en este encargo: **entrega para subida manual en YouTube/TikTok**.

## 2. Entradas y preferencias explícitas

Storyboard vertical validado: project_id único, idioma es-MX, 9:16, narración por escena, source_ids para cada afirmación, fuentes originales/DOI verificables y fechas, target_duration_seconds, estilo_id y export. Usar el contrato del repo; no insertar cadenas de ejemplo `A|B` como si fueran valores válidos.

Preferencias visuales como datos: estilo del catálogo existente, paleta, assets, encuadre/movimiento y restricciones editoriales; mismas preferencias por cápsula y rotación vigente de `data/rotacion.json`. No regenerar todo al cambiar una línea ni repetir mecánicamente estilo/estructura. Respetar arco, gancho y firma “Esto fue Datos y ociosidades.”; no prometer QA factual automatizado sólo por comprobar enlaces.

Voz invariable:

```json
{"engine":"edge-tts","voice_id":"es-MX-JorgeNeural","rate":"+7%","pitch":"-2Hz"}
```

`edge-tts` es cliente abierto de un **servicio remoto**, no motor TTS offline ni voz incluida en el repo; necesita red y está sujeto a disponibilidad/condiciones. Fuente: https://github.com/rany2/edge-tts . No prometer que la máquina persistente produce voz sin conectividad o que otro motor reproduce la misma voz.

## 3. Pipeline con gates y recibos

1. **INPUT_VALIDATE:** congelar storyboard/contrato/hashes, fuentes y preferencias; negar cambios de voz; dedupe por contenido y versión, sin reutilizar fallos como cache hit.
2. **TTS:** usar `tools/tts/narrate.py`/integración existente de `montar_capsula.py`, con voz/parámetros fijos. Guardar audio y word boundaries/timeline; retry limitado para transitorios; errores explícitos. Si el montaje ya sintetiza, no generar una segunda voz innecesariamente: separar caché/adaptador sin duplicar TTS.
3. **PREVIEW_VISUALS:** placeholders etiquetados sólo para revisión 540×960; nunca entregar placeholder como visual final ni llamar a modelos externos ahora. Vista previa visual/editorial aprobada antes de gastar HD.
4. **FINAL_VISUALS:** imágenes permitidas/licenciadas; Pillow/SVG/Matplotlib para tarjetas/mapas/gráficos, Inkscape o Blender si aportan valor. Opcional ComfyUI/Diffusers con modelo/licencia/hardware revisados, sin instalar pesos ni asumir GPU gratis. Los datos científicos del gráfico proceden de fuentes, no de la imagen generada. No usar frames vacíos o repetitivos para fingir producción completa.
5. **ASSEMBLY:** extender `scripts/montar_capsula.py`, FFmpeg vertical con movimiento sobre fijas, cortes, ASS/subtítulos y cama propia autorizada; no I2V completo por defecto. Final H.264/AAC, 1080×1920, 30 fps, yuv420p y faststart, audio sin recortes. Preview 540×960 marcado NO_PUBLICABLE.
6. **QA:** verificador independiente, medidas técnicas + revisión editorial/fuentes. Guardar cada check, medición, umbral, evidencia y estado; fallo bloquea paquete FINAL, no se ignora.
7. **PACKAGE:** MP4 final, storyboard, fuentes/metadata/licencias, subtítulos y QA/manifest/logs. Publicar únicamente a almacenamiento aprobado cuando se autorice; nada de subir a canales automáticamente.

El controlador determinista usa adaptadores allowlisted; no ejecuta prompts como comandos. Persistir pasos verificados y hashes; fuente/código/entrada cambiados invalidan checkpoint. Engine/244 permanecen readonly y completamente ajenos a este pipeline.

## 4. QA medible, no “el archivo existe”

| Check | Criterio de aceptación propuesto / vigente |
|---|---|
| Decodificación | ffprobe + decodificación completa sin error fatal; streams de video/audio presentes |
| Duración | 60–120 s conforme al QA actual; proximidad a objetivo registrada, sin rellenar con silencio |
| Resolución/formato | final 1080×1920, 9:16, H.264/AAC, 30 fps; preview separado 540×960 |
| Audio | audio realmente no silencioso en narración, sin clipping audible; no basta stream AAC vacío |
| Loudness | objetivo final −14 LUFS integrado ±1 LU, vigente en QA; true peak objetivo ≤−1.5 dBTP como gate propuesto a revisar en implementación |
| Subtítulos | cobertura textual ≥99% según receta, todos los timestamps dentro de audio/video, orden monotónico y bloques ≤3 palabras; gaps de narración >0.9 s se investigan conforme receta |
| Sincronía | usar boundaries reales y comprobar offsets por escena; tolerancia inicial propuesta 200 ms requiere validación auditiva, no declarar exactitud de voz por comparación textual |
| Negro/congelados | detectar blackdetect/freezedetect; gate propuesto: segmento negro inesperado ≥0.25 s falla, excepto intervalos declarados del diseño; no confundir fondo negro estilístico con frame perdido |
| Narrativa/fuentes | arco, voz correcta, estilo coherente, cifras/fuentes verdaderas y derechos/licencias; requiere revisión independiente, no sólo un regex |

Umbrales “propuestos” no se afirman implementados ni sustituyen contratos locales a escondidas. `qa_capsula.py` actual contiene checks de duración/resolución/codecs/fps/loudness, pero no asumir que cubre ya todo lo anterior. QA debe manejar FFmpeg fallido, métricas faltantes y NaN como fallo/inconcluso, no PASS. Normalización final de dos pasadas cuando sea necesaria; medir de nuevo el MP4 entregable.

Herramientas de referencia: `ffprobe`, filtros FFmpeg `ebur128`, `loudnorm`, `silencedetect`, `blackdetect` y `freezedetect` (https://ffmpeg.org/ffmpeg-filters.html). Su señal necesita contexto; no certifica hechos, derechos ni calidad perceptual por sí sola.

## 5. Paquete y ejecución futura

```text
proyectos/<id>/storyboard.json             # entrada versionada autorizada
proyectos/<id>/frames/                    # assets según gitignore/política
salidas/<id>/
  salida.mp4
  narracion.mp3
  subtitulos.srt
  subtitulos.ass
  storyboard.json
  metadata.json
  descripcion_youtube.txt
  caption_tiktok.txt
  fuentes.md
  licencias.json
  qa.json
  manifest.json                          # hashes/SHA/tool versions/voz
  events.jsonl
```

Estos nombres complementarios son propuestos; conservar nombres existentes que consumidores usan y documentar la correspondencia. No meter MP4, imágenes pesadas o tokens a Git si el repo los excluye; artefacto/almacenamiento autorizado con checksum y retención. El destino puede ser un job aislado de Actions o worker de la VM persistente aprobada; el render CPU no garantiza velocidad para generar imágenes por modelos ni evita coste de servicios remotos.

Sin credenciales de publicación YT/TikTok en el worker; no llamar `scripts/publicar.py --ejecutar`, `--publicar`, APIs de subida ni navegador autenticado. Entregar archivo y textos para subida manual. Estado final `PAQUETE_VERIFICADO_PARA_SUBIDA_MANUAL`, **no PUBLICADO**. Un paquete incompleto mantiene errores y pendientes, no un MP4 silencioso o con voz distinta.

## 6. PROMPT PARA MUSE

Prompt completo autocontenido: [`docs/PROMPT_MUSE_VIDEO.md`](PROMPT_MUSE_VIDEO.md). Muse debe reutilizar paths reales, entregar PR/bundle completo según sus capacidades y decir qué no ejecutó; no fingir acceso ni pedirle a Mj que integre pedazos.

### Texto autocontenido para copiar a Muse

# PROMPT PARA MUSE — prepara el pipeline CAPCOT completo, voz JorgeNeural intocable

Soy Mj. Quiero nuestro pipeline propio de código: storyboard JSON → voz oficial → visuales según preferencias → montaje MP4 9:16 → QA → paquete para subir manualmente a YouTube/TikTok. Yo no cableo nada. Entrega implementación completa y PR/bundle, **sin instalar, ejecutar, generar voz/imágenes, renderizar, publicar ni activar workflows todavía**. No afirmar pruebas o producción inexistentes.

## Contexto autocontenido y rutas reales

Reglas: https://github.com/marcojpad-hash/orquestador-central/blob/main/COORDINATION/COMO_TRABAJAMOS.md
Instrucción: https://github.com/marcojpad-hash/orquestador-central/blob/main/docs/INSTRUCCION_PIPELINE_VIDEO_CAPCOT.md
Repo producto: https://github.com/marcojpad-hash/capcot-capsulas-imaginantes
Leer en ese repo `README.md`, `AGENTS.md` si existe, `docs/RECETA_CAPSULA.md`, `docs/AHORRO_RECURSOS_PIPELINE.md`, `ajustes_entre_modelos/HANDOFF_GROK_PRODUCCION.md`, `templates/storyboard_vertical.template.json`, `scripts/validar_storyboard.py`, `scripts/generar_frames.py`, `scripts/montar_capsula.py`, `scripts/qa_capsula.py`, `scripts/metadata.py`, `tools/tts/narrate.py`. Ejemplo real: `proyectos/2026-11-07_barreleye-4k/storyboard.json`. Estos paths son referencias, no un permiso para ejecutar scripts.

Si no puedes leer el repo privado o tu chat no tiene terminal/escritura, declara esa limitación y entrega bundle completo con archivos/rutas/diff para un agente autorizado; no inventes contenidos ni me pases piezas que tenga que integrar.

## Implementación que debes preparar

1. Confirma repo/ref/SHA, capacidades y alcance. Reutiliza el pipeline existente, no crear un renderer paralelo en orquestador. Los datos/código viven en CAPCOT; Engine V5/canon 244 de motor-u6-storage no se tocan nunca.
2. Valida storyboard vertical: proyecto único, español México, escenas/arco, narración, source_ids, fuentes originales/DOI, fechas y preferencias (estilo/paleta/encuadre) del catálogo. No rellenar con datos científicos inventados. La política editorial/fuentes se revisa independientemente.
3. Impón **edge-tts, voice_id=es-MX-JorgeNeural, rate=+7%, pitch=-2Hz**, siempre. `tools/tts/narrate.py` ya declara defaults correctos; el validador debe rechazar otra voz/parámetros. La plantilla antigua `+4%`, Chirp y README con Piper/Dalia son conflictos históricos, no autorizaciones. Si edge-tts falla, BLOCK/retry limitado, **jamás otra voz**.
4. La referencia de comando futuro del wrapper existente es `python tools/tts/narrate.py guion.txt audio/narracion.mp3 es-MX-JorgeNeural +7% -2Hz`; no ejecutarla hoy. edge-tts es cliente de servicio remoto, no TTS offline: https://github.com/rany2/edge-tts . Evita doble síntesis si montar_capsula ya la hace; caché por texto/voz/parámetros/versiones y recibos reales.
5. Preview barato 540×960, placeholders claramente sólo borrador; aprobación visual antes de HD. Final con frames propios/licenciados y gráficos/mapas de datos reales. Opciones abiertas: Pillow/Matplotlib/SVG, Inkscape/Blender si aportan; ComfyUI/Diffusers opcional con pesos/licencia/GPU/costo revisados. No prometer imágenes por IA gratis en CPU ni convertir placeholder en final.
6. Reutiliza montaje FFmpeg (`scripts/montar_capsula.py`): vertical 1080×1920, 30 fps, H.264/AAC y yuv420p, faststart; fijas con movimiento, ASS y cama propia/permitida, ducking. No I2V de toda la cápsula, ni silencio para alargar. Voz medida/boundaries alimentan timeline/subtítulos.
7. Comandos de referencia existentes para una futura fase autorizada: `python3 scripts/validar_storyboard.py proyectos/<id>/storyboard.json --check-doi`; `python3 scripts/montar_capsula.py proyectos/<id>/storyboard.json -o salidas/<id>/salida.mp4 --borrador` para preview; mismo montaje sin `--borrador` para final; `python3 scripts/qa_capsula.py salidas/<id>/salida.mp4 proyectos/<id>/storyboard.json`. Los `<id>` deben resolverse a rutas permitidas. Leer flags actuales antes; no ejecutar ahora. El QA final de resolución no debe aprobar preview de 540×960.
8. Extiende QA independiente: duración vigente 60–120 s (referencias 75–90/60–95 antiguas no son gate actual); streams y audio no silencioso; 1080×1920/30fps/codecs; loudness final −14 LUFS ±1; true peak objetivo propuesto ≤−1.5 dBTP; subtítulos ≥99% cobertura, ≤3 palabras/bloque, timeline válido, sincronía medida; negro inesperado ≥0.25 s como umbral propuesto contextual y revisión de congelados. Herramientas `ffprobe`, `ebur128`, `loudnorm`, `silencedetect`, `blackdetect`, `freezedetect`: https://ffmpeg.org/ffmpeg-filters.html . Métricas faltantes/error/NaN no son PASS. Aceptación perceptual/editorial no se garantiza con regex.
9. Guarda manifiesto con input/code/tool hashes, voz exacta, derechos/provenance y JSONL continuo sanitizado. Checkpoints sólo pasos ejecutados/verificados, creador distinto del verificador. Conserva evidencia de fallo; fuente/código cambiado invalida resume. Sin token de publicación en worker; aislamiento por job y presupuesto explícito.
10. Paquete `salidas/<id>/`: salida.mp4, narración, SRT/ASS, storyboard, fuentes.md, licencias.json, metadata, descripción YouTube, caption TikTok, qa.json, manifest y events.jsonl. Mantén nombres reales/consumidores al extender. No commitear MP4/png/tokens si gitignore/política los excluye; usa artefacto/almacenamiento aprobado con hash/retención.
11. **No llamar `--publicar`, `scripts/publicar.py --ejecutar`, API de subida ni navegador autenticado.** Estado final futuro PAQUETE_VERIFICADO_PARA_SUBIDA_MANUAL, nunca PUBLICADO. No cambiar rutinas de publicación existentes por este encargo. El agente deja todo cableado; yo sólo recibiré el paquete.

## Entregables y aceptación

Produce rama/PR de código CAPCOT si tienes mandato/herramientas; en otro caso bundle autocontenido con archivos completos y un bloque para que un agente autorizado lo aplique. Incluye correcciones de plantilla/voz, adaptadores, QA, dependencias fijadas, pruebas propuestas y migración sin romper consumers. No fusionar main; PR + checks aplicables + mi “merge” al PR/SHA. Documentación no es video generado.

Pruebas futuras: voz distinta rechazada, endpoint TTS fallido no cambia voz, preview nunca final, storyboard sin fuente falla, MP4 silencioso/resolución errónea/subtítulos fuera de tiempo/frames negros inesperados fallan; final válido sólo tras QA técnico y editorial. Hoy todas NO_EJECUTADAS. Reporta repo/ref/SHA/PR o bundle, qué reutilizaste, conflictos corregidos, qué NO ejecutaste/publicaste, ubicación de entregables y siguiente paso mínimo. No prometas que puedo subir un archivo que no generaste.


### Bloque para Grok (para después)

> Lee `COORDINATION/COMO_TRABAJAMOS.md` y `docs/INSTRUCCION_PIPELINE_VIDEO_CAPCOT.md` en `marcojpad-hash/orquestador-central`; prepara por PR la extensión del pipeline existente de `capcot-capsulas-imaginantes`, no un renderer paralelo.
> Conserva edge-tts es-MX-JorgeNeural +7%/−2Hz sin fallback; storyboard→preview→visuales finales→FFmpeg→QA→paquete para subida manual. Engine/244 intactos.
> No instales, generes, renderices, publiques ni actives workflows todavía; entrega código completo, contratos, pruebas propuestas y PR/bundle, sin merge hasta mi aprobación.
