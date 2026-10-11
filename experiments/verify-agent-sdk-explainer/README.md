# Verifying the agent SDK

A short explainer (2 min 8 s, 1920×1080, with a quiet generated score) about
how the OpenHands [software-agent-sdk](https://github.com/OpenHands/software-agent-sdk)
is verified the way an agent uses it: a feature map with stable IDs, the
`control-agent-server` CLI from [PR #5621](https://github.com/OpenHands/software-agent-sdk/pull/5621),
saved evidence, and known bugs kept as expected failures (umbrella issue
[#5653](https://github.com/OpenHands/software-agent-sdk/issues/5653)). It ends
with the full replay: 771 pass, 156 known bugs reproduced, 6 blocked, no
surprises. It is drawn with [Manim](https://www.manim.community/), in the
3Blue1Brown style.

- `verify-agent-sdk-explainer.mp4`: the video (H.264 + AAC; all words are on screen)
- `verify_sdk.py`: the Manim scene; every number on screen lives here
- `music.py`: synthesizes the score with numpy (no samples), cued to the scene changes
- `stills/`: a few frames

## Render it yourself

```sh
pip install manim numpy
manim -qh verify_sdk.py VerifySDK      # writes the video and scene_times.json
python3 music.py                       # reads scene_times.json, writes music.wav
ffmpeg -i media/videos/verify_sdk/1080p60/VerifySDK.mp4 -i music.wav \
  -c:v copy -c:a aac -shortest -movflags +faststart verify-agent-sdk-explainer.mp4
```

To update the numbers, edit them in `verify_sdk.py` and render again.
