"""Create one original Spanish-Mexican voice reference with Qwen VoiceDesign."""
from pathlib import Path
import json
import os
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

ROOT = Path(__file__).resolve().parent
PROFILE = json.loads((ROOT / "voice_profile.json").read_text(encoding="utf-8"))
MODEL_ID = PROFILE.get("design_model", "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign")
DEVICE = os.getenv("VOICE_DEVICE_MAP", "cuda:0")
DTYPE = getattr(torch, os.getenv("VOICE_DTYPE", "bfloat16"))
OUT = ROOT / PROFILE["reference_audio"]
TEXT = (
    "La naturaleza está llena de fenómenos extraordinarios. "
    "Hoy vamos a explicar un dato curioso con claridad, precisión y sin exageraciones. "
    "Observa cómo cambia el mundo cuando entendemos lo que ocurre detrás de cada fenómeno."
)
INSTRUCTION = PROFILE.get(
    "voice_design_instruction",
    "Create an original adult male Mexican Spanish narrator. Medium-low register, "
    "warm but restrained, clear diction, stable pace, natural Mexico City pronunciation, "
    "broadcast-quality, no exaggerated acting. Do not imitate a specific person or existing voice."
)

def main():
    model = Qwen3TTSModel.from_pretrained(
        MODEL_ID, device_map=DEVICE, dtype=DTYPE
    )
    wavs, sr = model.generate_voice_design(
        text=TEXT, language="Spanish", instruct=INSTRUCTION
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(OUT), wavs[0], sr)
    (OUT.parent / "reference.txt").write_text(TEXT, encoding="utf-8")
    PROFILE["reference_text"] = TEXT
    (ROOT / "voice_profile.json").write_text(
        json.dumps(PROFILE, ensure_ascii=False, indent=2) + chr(10), encoding="utf-8"
    )
    print(f"REFERENCE_CREATED={OUT}")
    print(f"SAMPLE_RATE={sr}; SAMPLES={len(wavs[0])}")

if __name__ == "__main__":
    main()
