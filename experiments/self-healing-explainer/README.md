# Self-Healing, from the ground up

A narrated explainer (5 min 21 s, 1920×1080) of the Self-Healing Codebase
Project. Software factories now change code at the speed of agents, and that
needs a safety net. The video builds the net one piece at a time: a promise
the app makes, the feature map, the `control-openhands` CLI that drives the
real app, the daily pass, a known bug kept as an expected failure, a fix
proven before and after, and the loop that closes the issue.

It follows one real bug, OpenHands
[#17899](https://github.com/OpenHands/OpenHands/issues/17899): the Git name
and email saved in Settings never reached the agent's commits. Every piece
passed on its own, and the name was lost between them. The before/after
screenshots are the real ones from the fix,
[#18425](https://github.com/OpenHands/OpenHands/pull/18425), which was still
open when this was made (18 October 2026).

Everything is open: [Manim Community Edition](https://www.manim.community/)
for the animation, [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
(open weights) with the `af_heart` voice for the narration, and a low score
synthesized with numpy.

- `self-healing.mp4`: the video (H.264 + AAC)
- `narration.md`: the narration, one paragraph per scene
- `selfheal.py`: the Manim scene; `cue()` starts each animation on its sentence
- `tts.py`: reads `narration.md`, writes one wav per scene and `timings.json`
- `score.py`: synthesizes the score (pads, a sub bass, a few soft bells, reverb)
- `stills/`: a few frames

## Render it yourself

The scene also needs the three screenshots from #18425's `.pr/17899/`
(`settings-saved.png`, `main-conversation.png`, `fix-conversation.png`) next
to `selfheal.py`, converted to RGBA.

```sh
pip install "kokoro>=0.9.4" soundfile scipy      # Python 3.12
python3 tts.py narration.md                       # seg01.wav … seg11.wav, timings.json
pip install manim "pillow<11.3"                   # Pillow 13 breaks image fades in Manim 0.22
manim -qh --frame_rate 30 -o out selfheal.py SelfHealing
python3 score.py 325 score.wav
ffmpeg -i media/videos/selfheal/1080p30/out.mp4 -i score.wav -filter_complex \
  "[0:a]aresample=44100,volume=9dB,asplit=2[v][sc];[1:a]volume=-16dB[m0];\
[m0][sc]sidechaincompress=threshold=0.03:ratio=4:attack=80:release=900[m];\
[v][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]" \
  -map 0:v -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k \
  -movflags +faststart self-healing.mp4
```
