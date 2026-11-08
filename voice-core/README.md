# Shared Voice Core

Servicio único de síntesis para que CAPCOT, U6 y otros consumidores usen **el mismo modelo, referencia de voz y perfil**. Los clientes no eligen voces por su cuenta: envían texto al servicio.

## Por qué Qwen3-TTS

El modelo oficial Qwen3-TTS-12Hz-1.7B-Base admite clonación desde audio de referencia, español y licencia Apache-2.0 declarada por el proyecto/model card. La licencia del modelo no concede derechos sobre una grabación de terceros: la referencia debe ser propia o contar con autorización verificable.

No se copia ni se extrae el modelo privado de Microsoft Edge TTS. Si se busca una voz cercana al estilo de es-MX-JorgeNeural, se crea una identidad original con rasgos generales (español mexicano, voz masculina adulta, dicción clara, ritmo sobrio); no se presenta como clon exacto ni se reutiliza audio de Edge sin permiso.

## Instalación

Requiere Python 3.12 y, para el modelo 1.7B, una GPU compatible con memoria suficiente. En el servidor:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r voice-core/requirements.txt
cp voice-core/voice_profile.example.json voice-core/voice_profile.json
```

Coloca una grabación autorizada y limpia en `voice-core/voices/narrador_es_mx_01/reference.wav`, edita el perfil con su transcripción literal y ejecuta:

```bash
VOICE_PROFILE=voice-core/voice_profile.json uvicorn server:app --app-dir voice-core --host 0.0.0.0 --port 8787
```

En despliegues reales, proteger el endpoint con autenticación y TLS; no exponerlo públicamente sin control de acceso.

## API

- `GET /health`: estado del modelo y voice_id.
- `POST /synthesize`: JSON `{"text":"Texto para narrar","output_path":"out/clip.wav"}`.

El servicio carga el modelo y construye el prompt de voz una sola vez al arrancar. Cada síntesis reutiliza esa misma referencia/prompt; no vuelve a seleccionar una voz distinta por petición.

## Criterios de consistencia

1. Un solo `voice_id`, checkpoint y referencia por identidad.
2. No cambiar idioma, referencia, transcripción, prompt ni versión del modelo sin versionar el perfil.
3. Segmentar textos largos por párrafos/frases y unir WAV sin cambiar parámetros.
4. Validar muestras de control: misma frase corta, números, nombres propios, siglas y texto largo.
5. Comparar similitud de hablante y estabilidad perceptual entre muestras; no declarar equivalencia con Jorge sin evaluación humana A/B.
6. Conservar la grabación de referencia y su autorización fuera del repositorio; nunca subir audio privado o claves a Git.

## Estado honesto

El código y la interfaz quedan preparados, pero la síntesis real no puede declararse probada hasta aportar una referencia autorizada y ejecutar el modelo en un host con GPU compatible. El teléfono Android no debe tratarse como servidor de inferencia para el checkpoint 1.7B. Edge TTS queda como fallback temporal, no como identidad compartida.
