# The map that keeps itself honest

A short animated film (2 min 24 s, 1920×1080) about the `verify-agent-server`
skill in [OpenHands/software-agent-sdk PR #5621](https://github.com/OpenHands/software-agent-sdk/pull/5621):
a control CLI, an executable feature map of the Agent Server's 34 feature
families, and known bugs kept as expected failures. The film also shows what
the map's full replay found, and the moment an upstream fix turned a known
bug into an unexpected pass.

The film's character, a small folded paper map, is animated with John
Lasseter's principles from "Principles of Traditional Animation Applied to 3D
Computer Animation" (SIGGRAPH 1987). [storyboard.md](storyboard.md) lists every
shot with its timing and the principles it uses.

- `agent-server-feature-map.mp4`: the film (H.264, no audio; all words are on screen)
- `storyboard.md`: shot list, timings, principles, sources
- `stills/`: a few frames
- `video.html`: the animation; `renderFrame(t)` draws any moment
- `render.mjs`: renders frames with Playwright and encodes them with ffmpeg
- `fonts/`: Instrument Serif, DM Sans, JetBrains Mono (SIL Open Font License, from `@fontsource`)

## Render it yourself

```sh
npm install playwright@1.56.1          # any version whose Chromium you have
node render.mjs stills 8 86 107        # PNG stills into stills/
node render.mjs video --workers 4      # writes agent-server-feature-map.mp4
```

Open `video.html?play` through any local web server to watch it live, or
`video.html?t=86` to see one frame.
