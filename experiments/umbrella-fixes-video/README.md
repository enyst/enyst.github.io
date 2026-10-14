# Verify everything, thus fix everything

A narrated video (4:43, 1920×1080) about what came after the first full
run of the OpenHands Agent Server feature map: every medium and low bug fixed,
one pull request each, proven against the map, with a "Decision needed" section
wherever a choice belongs to a maintainer (umbrella issue
[#5653](https://github.com/OpenHands/software-agent-sdk/issues/5653)). It is
drawn with [Manim](https://www.manim.community/) in the 3Blue1Brown style and
embedded on [verify/fix-everything.html](../../verify/fix-everything.html).

- `umbrella-fixes.mp4`: the video (H.264 + AAC)
- `umbrella_fixes.py`: the Manim scenes; every number and snippet on screen lives here
- `narration.py`: the narration text, voiced with
  [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (Apache-2.0, open
  weights), voice `af_heart`
- `music.py`: a quiet, low ambient score synthesized with numpy (no samples),
  cued to the scene changes
- `mix.py`: lays the narration on each scene and ducks the music under it
- `voice/durations.json`: how long each scene's narration runs
- `stills/`: a few frames (`title.png` is the poster)

## Render it yourself

```sh
pip install kokoro soundfile          # Python 3.10–3.12, CPU is fine
python narration.py                   # writes voice/*.wav and voice/durations.json
pip install manim numpy
manim -r 1920,1080 --fps 30 umbrella_fixes.py UmbrellaFixes   # also writes scene_times.json
python music.py                       # writes music.wav
python mix.py media/videos/umbrella_fixes/1080p30/UmbrellaFixes.mp4
```

Each scene lasts as long as its narration, and `cue()` in the scene script
waits for the narrator to reach a phrase, so editing the text in
`narration.py` and running the steps again keeps picture and voice in step.
