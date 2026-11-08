"""Shared Qwen3-TTS voice service. Reference audio is generated locally from an original voice design."""
from __future__ import annotations

import json
import os
import secrets
from pathlib import Path
from threading import Lock
from uuid import uuid4

import soundfile as sf
import torch
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from qwen_tts import Qwen3TTSModel

ROOT = Path(__file__).resolve().parent
PROFILE_PATH = Path(os.getenv("VOICE_PROFILE", ROOT / "voice_profile.json"))
DEVICE_MAP = os.getenv("VOICE_DEVICE_MAP", "cuda:0")
DTYPE = getattr(torch, os.getenv("VOICE_DTYPE", "bfloat16"))
API_TOKEN = os.getenv("VOICE_API_TOKEN", "")
app = FastAPI(title="Shared Voice Core", version="0.1.0")
model = None
clone_prompt = None
profile = None
lock = Lock()


class SynthesisRequest(BaseModel):
    text: str = Field(min_length=1, max_length=12000)


@app.on_event("startup")
def load_voice():
    global model, clone_prompt, profile
    if not PROFILE_PATH.exists():
        raise RuntimeError(f"Voice profile missing: {PROFILE_PATH}")
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    audio = (ROOT / profile["reference_audio"]).resolve()
    if not audio.is_file():
        raise RuntimeError(f"Voice reference missing: {audio}")
    reference_text = profile.get("reference_text", "")
    if (not reference_text or reference_text.startswith("TRANSCRIPCION_")
            or reference_text.startswith("GENERATED_BY_")):
        raise RuntimeError("Generate the reference first with bootstrap_voice.py.")
    model = Qwen3TTSModel.from_pretrained(
        profile["model"], device_map=DEVICE_MAP, dtype=DTYPE
    )
    clone_prompt = model.create_voice_clone_prompt(
        ref_audio=str(audio),
        ref_text=reference_text,
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
def synthesize(req: SynthesisRequest, authorization: str | None = Header(default=None)):
    if not API_TOKEN:
        raise HTTPException(503, "Set VOICE_API_TOKEN before enabling synthesis")
    expected = f"Bearer {API_TOKEN}"
    if not authorization or not secrets.compare_digest(authorization, expected):
        raise HTTPException(401, "Invalid bearer token")
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
        out_dir = ROOT / "out"
        out_dir.mkdir(parents=True, exist_ok=True)
        output = out_dir / f"{uuid4().hex}.wav"
        sf.write(str(output), wavs[0], sr)
        return FileResponse(
            output,
            media_type="audio/wav",
            filename=output.name,
            headers={"X-Voice-ID": profile["voice_id"], "X-Sample-Rate": str(sr)},
        )
    except Exception as exc:
        raise HTTPException(500, f"Synthesis failed: {type(exc).__name__}: {exc}") from exc
