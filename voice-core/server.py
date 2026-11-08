"""Shared Qwen3-TTS voice service. Requires an authorized reference recording."""
from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock

import soundfile as sf
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from qwen_tts import Qwen3TTSModel

ROOT = Path(__file__).resolve().parent
PROFILE_PATH = Path(os.getenv("VOICE_PROFILE", ROOT / "voice_profile.json"))
DEVICE_MAP = os.getenv("VOICE_DEVICE_MAP", "cuda:0")
DTYPE = os.getenv("VOICE_DTYPE", "bfloat16")
app = FastAPI(title="Shared Voice Core", version="0.1.0")
model = None
clone_prompt = None
profile = None
lock = Lock()


class SynthesisRequest(BaseModel):
    text: str = Field(min_length=1, max_length=12000)
    output_path: str | None = None


@app.on_event("startup")
def load_voice():
    global model, clone_prompt, profile
    if not PROFILE_PATH.exists():
        raise RuntimeError(f"Voice profile missing: {PROFILE_PATH}")
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    audio = (ROOT / profile["reference_audio"]).resolve()
    if not audio.is_file():
        raise RuntimeError(f"Authorized reference audio missing: {audio}")
    if not profile.get("reference_text") or profile["reference_text"].startswith("TRANSCRIPCION_"):
        raise RuntimeError("Set the exact transcript of the reference recording.")
    model = Qwen3TTSModel.from_pretrained(
        profile["model"], device_map=DEVICE_MAP, dtype=DTYPE
    )
    clone_prompt = model.create_voice_clone_prompt(
        ref_audio=str(audio),
        ref_text=profile["reference_text"],
        x_vector_only_mode=bool(profile.get("x_vector_only_mode", False)),
    )


@app.get("/health")
def health():
    return {
        "status": "ready" if model is not None and clone_prompt is not None else "not_ready",
        "voice_id": profile.get("voice_id") if profile else None,
        "engine": "qwen3-tts",
        "model": profile.get("model") if profile else None,
    }


@app.post("/synthesize")
def synthesize(req: SynthesisRequest):
    if model is None or clone_prompt is None:
        raise HTTPException(503, "Voice model is not loaded")
    try:
        with lock:
            wavs, sr = model.generate_voice_clone(
                text=req.text,
                language=profile.get("language", "Spanish"),
                voice_clone_prompt=clone_prompt,
                non_streaming_mode=True,
            )
        if not wavs:
            raise RuntimeError("Model returned no audio")
        output = Path(req.output_path) if req.output_path else ROOT / "out" / "speech.wav"
        if not output.is_absolute():
            output = (ROOT / output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(output), wavs[0], sr)
        return {"status": "generated", "voice_id": profile["voice_id"],
                "engine": "qwen3-tts", "sample_rate": sr,
                "output_path": str(output), "samples": int(len(wavs[0]))}
    except Exception as exc:
        raise HTTPException(500, f"Synthesis failed: {type(exc).__name__}: {exc}") from exc
