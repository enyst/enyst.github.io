# React, then do the thing

A short narrated film (1:27, 1920×1080) about conversation reactions in
OpenHands: an experimental switch, an agent that answers “wait, actually” with
a 👍 and keeps working, a person's ❤️ on the answer, and reactions that are
still there after a server restart. It is embedded on
[arch/conversation-reactions.html](../../arch/conversation-reactions.html).

The screen parts are a real run, not a mock-up: Agent Canvas built from the
verify branch of [OpenHands #19503](https://github.com/OpenHands/OpenHands/pull/19503)
(`1e9d355`), against an Agent Server from
[software-agent-sdk #6609](https://github.com/OpenHands/software-agent-sdk/pull/6609)
(`c4beabb`, with its TypeScript client built locally until a release includes it),
driven with `control-openhands` from the verify-openhands skill, in the Paper
theme, with `deepseek/deepseek-flash`. The workspace was a small git repository
whose `AGENTS.md` asks for short answers and a 👍 when plans change (see the page
for why).

- `reactions.mp4`: the film (H.264 + AAC)
- `clips/`: the three `browser record` captures (flag, main run, restore)
- `plan.py`: the edit: which part of each recording plays in which scene, at what speed
- `reactions.py`: the Manim layer (rendered transparent, on top of the recordings)
- `narration.py`: the narration, voiced with [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
  (Apache-2.0, open weights), voice `af_heart`
- `score.py`: a light score and the reaction “pop” sounds, synthesized with numpy (no samples)
- `mix.py`, `compose.py`: the sound mix and the final picture
- `emoji/`: 👍 ❤️ 👀 from [Noto Emoji](https://github.com/googlefonts/noto-emoji) (Apache-2.0)
- `stills/`: a few frames (`poster.png` is the poster)

## Render it yourself

```sh
pip install kokoro soundfile manim numpy   # Python 3.12; espeak-ng and pango dev headers
python narration.py                         # voice/*.wav, voice/durations.json
manim -t -r 1920,1080 --fps 30 reactions.py Reactions   # also writes scene_times.json, marks.json
python score.py && python mix.py
python compose.py media/videos/reactions/1080p30/Reactions.mov
```

Each scene lasts as long as its narration (or its recording, if longer);
`plan.py` holds the timing that the Manim layer, the sounds and the
composition all share.
