# Recorded verification films

`record.py` runs each reproduction command and records its actual stdout in a
Chromium browser evidence panel using Playwright's browser video recorder. It
does not simulate server responses or replay invented evidence. Every featured
finding must be independently confirmed and must produce the expected signal
during recording; otherwise production stops without claiming confirmation.

The visual design uses an original dark mathematical canvas, blue contract
diagrams, and yellow observed failures. Current MP4 audio uses local Kokoro-82M v1.0 af_heart neural narration (the original capture used libflite),
an original quiet D-minor/suspended score, and a three-note ascending cue when
the confirmed failure first appears. An English subtitle track and standalone
SRT and WebVTT accompany each final MP4. Narration is synthesized, not a human voice.

Run with local network access allowed (Chromium requires sockets):

```sh
python /workspace/verification-artifacts/video/record.py manifest.json
```

Each final film directory includes:

- `agent-server-verification.mp4`: narrated film with score and subtitles.
- `recorded-reproductions.webm`: browser recorder output before audio mixing.
- `live-evidence.json`: timestamped, credential-redacted actual process output.
- `timeline.json`: speech and observation cue timestamps.
- `narration.srt`, `narration.vtt`, speech `.txt` files, and `.wav` files: accessible screenplay.
- `summary.png`: the film's complete confirmed-finding count card.

The `workflow-validation-only` and `workflow-smoke` directories are recording
pipeline checks. They are excluded from the actual bug report and its counts.

The neural narration upgrade is documented in [voice-upgrade/README.md](voice-upgrade/README.md). The original video streams and raw browser recordings are preserved.
