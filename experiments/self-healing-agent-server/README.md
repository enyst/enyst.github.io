# Self-Healing, for the Agent Server

A narrated explainer (5 min 32 s, 1920×1080) of the Self-Healing Codebase
Project, told from the Agent Server side. It builds three safety nets for a
codebase that agents change faster than people can read (design review where
it matters, constraints on possible code, and self-healing when it breaks
anyway), then follows three real Agent Server bugs that people using a UI
over REST would feel:

| Story | Issue | Fix |
|---|---|---|
| The goal chip stays "running" forever after a restart, and Stop answers "success" | [#5627](https://github.com/OpenHands/software-agent-sdk/issues/5627) | [#5772](https://github.com/OpenHands/software-agent-sdk/pull/5772) (merged) |
| One failed run freezes every window for about 5 s | [#5633](https://github.com/OpenHands/software-agent-sdk/issues/5633) | [#5780](https://github.com/OpenHands/software-agent-sdk/pull/5780) (merged) |
| After a key change, saving one unrelated setting erases stored keys | [#5622](https://github.com/OpenHands/software-agent-sdk/issues/5622) | [#5758](https://github.com/OpenHands/software-agent-sdk/pull/5758) (open) |

Everything is open: [Manim Community Edition](https://www.manim.community/)
for the animation, [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
(open weights, Apache-2.0) with the `af_heart` voice for the narration, and a
low score synthesized with numpy.

- `self-healing-agent-server.mp4`: the video (H.264 + AAC)
- `narration.py`: the narration, one entry per scene, and the Kokoro synthesis
- `self_healing.py`: the Manim scenes; `cue()` starts each animation on its phrase
- `music.py`: the score, which follows the scene times and beats the render writes
- `mix.py`: lays the narration on the video and ducks the music under it
- `stills/`: a few frames

## Render it yourself

```sh
pip install manim kokoro soundfile "misaki[en]"   # Python 3.12, libpango1.0-dev, ffmpeg; no LaTeX
python -m spacy download en_core_web_sm
python narration.py                               # voice/*.wav, voice/durations.json
manim -r 1920,1080 --fps 30 --disable_caching self_healing.py SelfHealing
python music.py                                   # music.wav
python mix.py media/videos/self_healing/1080p30/SelfHealing.mp4   # writes self-healing.mp4
```
