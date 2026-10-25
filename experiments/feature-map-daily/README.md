# Feature Map Daily

A short film (2:05, 1920×1080, with a quiet generated score; all words are on
screen) about one daily pass of the OpenHands Agent Canvas feature map
(verify-openhands), and one change it verified from end to end:
[OpenHands PR #18870](https://github.com/OpenHands/OpenHands/pull/18870), which
masks secret values in the agent's request card and in Settings. It is embedded
on [verify/feature-map-daily.html](../../verify/feature-map-daily.html).

The film shows the map at full scale (28 families, 798 behaviors), what the
24 October 2026 daily pass touched (11 merged PRs, 8 families), what it recorded
(pass, fail, xfail, xpass, blocked, not-run), then zooms into F14 and the row
`F14.value-reveal`, and plays real before/after recordings side by side.

- `feature-map-daily.mp4`: the film (H.264 + AAC)
- `storyboard.md`: shots, timings and sources for every number
- `video.html`: the animation; `renderFrame(t)` draws any moment, `window.CLIPS`
  places the recordings
- `render.mjs`: renders frames with Playwright, composites the recordings with
  ffmpeg and adds the score
- `score.py`: the score, synthesized with numpy (no samples)
- `clips/`: the four live recordings, made with `control-openhands browser record`
- `stills/`: film frames, and crops of the four "typed" screenshots used on the page
- `fonts/`: Instrument Serif, DM Sans, JetBrains Mono (SIL Open Font License)

## How the recordings were made

Two worktrees of OpenHands/OpenHands, one at `4d1c4d1` (the commit before the
merge) and one at `04f6dd5` (the merge of #18870), each launched with its own
`control-openhands launch --new` (Agent Server 1.58.1, automation 1.25.1) and
driven with the same commands:

```sh
control-openhands browser viewport 1600x900
control-openhands browser goto /settings/secrets
control-openhands browser record start --feature F14.value-reveal --name settings-before --fps 20
control-openhands browser click 'testid=add-secret-button'
control-openhands browser type 'testid=add-secret-form >> testid=name-input' QA_DEMO_TOKEN
control-openhands browser type 'testid=add-secret-form >> testid=value-input' sk-demo-0000-not-a-real-key
# after only: click Show secret, then Hide secret
control-openhands browser eval "…tagName, type, autocomplete of the value field…"
control-openhands browser click 'testid=add-secret-form >> testid=submit-button'
control-openhands browser record stop
```

The request-card clips used `conversation start --prompt "Call the request_secret
tool with name QA_DEMO_TOKEN …"` (deepseek-flash, one tool call) and the same
typing on `testid=secret-request-card`. The value is a dummy; the secrets were
deleted afterwards. `browser eval` read `TEXTAREA textarea` before and
`INPUT password new-password` after.

## Render it yourself

```sh
npm install playwright@1.56.1     # or link any Playwright whose Chromium you have
python3 score.py score.wav
node render.mjs stills 3 15 28 40 57 70 82 97 113 121
node render.mjs video --workers 4 --audio score.wav --audio-gain -9
```

Open `video.html?play` through any local web server to watch the animation
live (without the recordings), or `video.html?t=57` for one frame.
