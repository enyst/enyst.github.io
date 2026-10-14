# Neural narration upgrade

This directory generates a new narration track without editing recorded video or
publishing files. The selected synthetic English voice is Kokoro `af_heart`, not
GPT audio and not a clone of a person. The screenplay is copied verbatim from
the existing five recorded demonstrations and final report-count card.

## Backend and provenance

- **Model:** [Kokoro-82M v1.0](https://huggingface.co/hexgrad/Kokoro-82M), full-precision ONNX, local CPU inference. Its model card declares **Apache-2.0**.
- **Wrapper:** [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx), version 0.6.1, **MIT** license. A copy of its notice is `wrapper_license.md`.
- **Assets:** [model-files-v1.1](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.1). The filename `kokoro-v1.0.onnx` identifies the model generation; the release tag identifies the conversion/assets. The release is mutable, so the manifest records the actual downloaded SHA256 hashes.
- **Pronunciation:** eSpeak NG via `phonemizer` and `espeakng-loader`. Software dependencies retain their respective licenses; these tools perform local text-to-phoneme conversion.
- **Voice:** `af_heart`, American English. The [upstream voice table](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) gives it training-data grade A; this is an upstream estimate, not an objective rating of this particular narration. The reviewed upstream documents do not state an additional attribution requirement for generated English `af_heart` audio.

The model and voice bank are not intended for inclusion in the report download.
Publish `synthesize.py`, `requirements-lock.txt`, this document, the generated
audio, and `voice-manifest.json` as appropriate. Preserve applicable notices if
redistributing upstream software or model assets.

## Reproduce

Create an isolated Python 3.12 environment and install `requirements-lock.txt`.
Download these files into this directory:

```
https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.onnx
https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin
```

Verify their SHA256 values:

```
beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a  kokoro-v1.0.onnx
bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d  voices-v1.0.bin
```

Generate all sixteen narration segments:

```
.venv/bin/python synthesize.py --voice af_heart --speed 1.0 --threads 4
```

Generate a single sample:

```
.venv/bin/python synthesize.py --voice am_michael --speed 1.0 \
  --source ../lock-stall/01-opening.txt --output pilot/am_michael-opening.wav
```

Outputs are mono 24 kHz PCM16 WAV files with their original `.txt` files alongside.
No time stretching, loudness normalization, music, or cues are applied here.
The final remix applies its own timing and loudness adjustment, and retains the
original recorded video stream.

## Validation

`voice-manifest.json` records model/script/text/audio hashes, package versions,
voice/speed, natural duration, peak/RMS, and successful audio decode for every
segment. The generation script rejects empty, non-finite, or clipped waveforms.
The pilot durations are 9.363 seconds for `af_heart` (166.6 words per minute) and
10.222 seconds for `am_michael` (152.6 words per minute), both at model speed 1.0.
These checks establish file integrity and pace; they do not replace listening.
