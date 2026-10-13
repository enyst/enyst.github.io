#!/usr/bin/env python3
"""Reproduce neural narration locally with Kokoro-82M v1.0 on CPU.

No API credentials, cloud speech request, voice cloning, or source-video edits.
Run with the isolated .venv/bin/python. See README.md for model downloads.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path

import numpy as np
import onnxruntime as ort
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parent
VIDEO = ROOT.parent
FAMILIES = ("lock-stall", "upload-atomic", "secret-loss", "git-space", "ts-binary")
PARTS = ("01-opening", "01-observation", "ending")
BASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_model(threads: int) -> Kokoro:
    options = ort.SessionOptions()
    options.intra_op_num_threads = threads
    options.inter_op_num_threads = 1
    options.log_severity_level = 3
    session = ort.InferenceSession(
        str(ROOT / "kokoro-v1.0.onnx"),
        sess_options=options,
        providers=["CPUExecutionProvider"],
    )
    return Kokoro.from_session(session, str(ROOT / "voices-v1.0.bin"))


def synthesize(model: Kokoro, source: Path, target: Path, voice: str, speed: float) -> dict:
    """Keep the source text exact; return unnormalized natural-duration PCM audio."""
    source_bytes = source.read_bytes()
    text = source_bytes.decode("utf-8").strip()
    if not text:
        raise ValueError(f"Empty speech input: {source}")
    start = time.monotonic()
    samples, sample_rate = model.create(text, voice=voice, speed=speed, lang="en-us")
    samples = np.asarray(samples)
    if samples.ndim != 1 or not len(samples) or not np.isfinite(samples).all():
        raise ValueError(f"Invalid generated waveform: {source}")
    if np.abs(samples).max() >= 1:
        raise ValueError(f"Clipped generated waveform: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    sf.write(target, samples, sample_rate, subtype="PCM_16")
    target.with_suffix(".txt").write_bytes(source_bytes)
    seconds = len(samples) / sample_rate
    decoded, decoded_rate = sf.read(target)
    assert decoded_rate == sample_rate and len(decoded) == len(samples)
    assert np.isfinite(decoded).all()
    return {
        "source": str(source), "source_sha256": sha256(source),
        "output": str(target), "output_sha256": sha256(target),
        "text_output": str(target.with_suffix(".txt")),
        "voice": voice, "speed": speed, "sample_rate": sample_rate,
        "channels": 1, "subtype": "PCM_16", "duration_seconds": seconds,
        "words": len(text.split()), "words_per_minute": len(text.split()) * 60 / seconds,
        "inference_seconds": time.monotonic() - start,
        "peak": float(np.abs(decoded).max()),
        "rms": float(np.sqrt(np.mean(decoded ** 2))),
        "audio_decode": "pass", "time_stretch_applied": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--voice", default="af_heart")
    parser.add_argument("--speed", default=1.0, type=float)
    parser.add_argument("--threads", default=4, type=int)
    parser.add_argument("--source", type=Path, help="Single UTF-8 screenplay file")
    parser.add_argument("--output", type=Path, help="Single WAV target")
    args = parser.parse_args()
    if bool(args.source) != bool(args.output):
        parser.error("--source and --output must be supplied together")
    model = load_model(args.threads)
    if args.source:
        print(json.dumps(synthesize(model, args.source, args.output, args.voice, args.speed)))
        return
    records = []
    jobs = [(VIDEO / family / (part + ".txt"), ROOT / "generated" / family / (part + ".wav"))
            for family in FAMILIES for part in PARTS]
    jobs.append((VIDEO / "final-highlights/full-report-counts.txt",
                 ROOT / "generated/final-highlights/full-report-counts.wav"))
    for source, target in jobs:
        record = synthesize(model, source, target, args.voice, args.speed)
        records.append(record)
        print(json.dumps(record), flush=True)
    assets = [{"file": name, "source": BASE + name, "sha256": sha256(ROOT / name),
               "bytes": (ROOT / name).stat().st_size}
              for name in ("kokoro-v1.0.onnx", "voices-v1.0.bin")]
    manifest = {
        "backend": "Kokoro-82M v1.0, full-precision ONNX, local CPU inference",
        "voice": args.voice, "speed": args.speed, "language": "en-us",
        "license": {"model": "Apache-2.0", "kokoro_onnx_wrapper": "MIT",
                    "model_card": "https://huggingface.co/hexgrad/Kokoro-82M",
                    "wrapper": "https://github.com/thewh1teagle/kokoro-onnx",
                    "voice_documentation": "https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md"},
        "phonemizer": "espeak-ng via phonemizer and espeakng-loader",
        "threads": {"intra_op": args.threads, "inter_op": 1},
        "python": platform.python_version(),
        "packages": {name: importlib.metadata.version(name) for name in
                     ("kokoro-onnx", "onnxruntime", "soundfile", "numpy", "phonemizer", "espeakng-loader")},
        "model_assets": assets,
        "script_sha256": sha256(Path(__file__)),
        "api_key_required": False, "voice_clone": False,
        "narration_wording_changed": False, "published_files_modified": False,
        "normalization_or_time_stretch": "None; the final remix performs its own loudness and timing adjustment.",
        "outputs": records,
    }
    (ROOT / "voice-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"complete": True, "wav_count": len(records),
                      "manifest": str(ROOT / "voice-manifest.json")}), flush=True)


if __name__ == "__main__":
    main()
