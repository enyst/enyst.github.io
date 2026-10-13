# Neural narration update

The published highlights and five narrated uncut MP4s now use **Kokoro-82M v1.0**, the stock English **af_heart** voice, generated locally through **kokoro-onnx 0.6.1**. The narration is synthetic. No OpenAI speech credential was configured in this environment; this is Kokoro narration.

The screenplay, recorded API/client observations, video frames, severity totals, musical score and failure-cue positions are retained. Narration was normalized to -18 LUFS and fitted to the existing speech windows. Captions were retimed to complete utterances. Every MP4's compressed video stream has the same SHA-256 as before the audio replacement; full audio/video decoding passes.

Model: https://huggingface.co/hexgrad/Kokoro-82M (Apache2.0).
Inference wrapper: https://github.com/thewh1teagle/kokoro-onnx (MIT).
Voice documentation: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md.

See voice-manifest.json for actual downloaded model/voice-bank hashes and generation settings. The release tag and underlying model version differ; hashes pin the assets. Model weights and Python package caches are not published here. synthesize.py and requirements-lock.txt reproduce the voice generation; upgrade_voice.py performs the score/cue remix and video-stream preservation checks.

record.py remains the original capture workflow, whose initial voice was libflite. The neural audio upgrade operates on those real recordings; recorded-reproductions.webm retains their untouched browser capture.
