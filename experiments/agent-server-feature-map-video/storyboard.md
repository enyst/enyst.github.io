# The map that keeps itself honest: storyboard

A 2 min 24 s film (1920×1080, 30 fps, H.264) about the `verify-agent-server`
skill from [OpenHands/software-agent-sdk PR #5621](https://github.com/OpenHands/software-agent-sdk/pull/5621)
and what its full replay found. The images are made in a canvas with the
palette and fonts of this site's `brand.css`.

**The character.** The story needs someone to root for, so the feature map is
a character: a small folded paper map with a gold map pin, big eyes, a dotted
trail and an X on its body. It never speaks. It watches, nods, holds its
breath, jumps and waves. It has appeal because its shape is simple (a folded
rectangle, two eyes, one pin) and because it reacts to everything the
audience should notice. Lasseter's credo, story and character first,
technology in service of them, decides what goes on screen. Each shot carries
one idea. The numbers and code are real, but they come in only when the
character, or the story, needs them.

**Sources for every fact on screen:** the PR's
`.agents/skills/verify-agent-server/` (SKILL.md, the feature map, the CLI's
`map run` output vocabulary: `xfail`, `xpass`, "known bug no longer
reproduces: update the map"), `.pr/verify-agent-server-replay.md` (the
per-family replay table drawn in shot 8), umbrella issue #5653 and
[the tracker page](https://enyst.github.io/arch/agent-server-bug-tracker.html).
Security-relevant findings appear only as the public titles of the four
hardening PRs.

## Shot list

| # | Time | Shot | What happens | Lasseter principle it leans on |
|---|---|---|---|---|
| 1 | 0:00–0:09 | **Hook: 203 routes** | Route pills pop in one after another while the counter climbs to 203, with a few real route names drifting up. The grid dims and holds a beat, then *"How do you know it all works?"* | **Staging** (one quiet, enormous surface), **slow in / slow out** on the count, **timing** (a held beat before the question) |
| 2 | 0:09–0:17.5 | **The gap** | Three spotlights light parts of the grid: unit tests, the OpenAPI breakage check, live-server tests. Dark patches remain. Caption: none of them let an agent drive the real server end to end and tell a stale instruction from a real bug. | **Staging** with light: the gaps are the subject. **Exaggeration**: spotlights overshoot as they open. |
| 3 | 0:17.5–0:27 | **Meet the map** | A folded ball bounces in on arcs, crouches, then pops up and unfolds into the character. The pin wobbles, it blinks, looks at us, then looks to the title: *verify-agent-server*, PR #5621, adapted from Lauren Tan's (@poteto) pstack verification skills. It waves as three chips name the parts. | **Anticipation** (the crouch), **squash and stretch** (volume-preserving), **follow-through** (the pin), **arcs** (the bounce), **appeal** |
| 4 | 0:27–0:40.5 | **1 · The control CLI** | A terminal types real commands from the F18 recipe: `launch --new`, then a `PUT` of the redaction placeholder, then the `GET … --check … # bug` that answers `404 Secret not found`, recorded as an expected failure. Cards slide in beside it: isolated servers, `--expect`/`--check`, fixtures, evidence with secrets redacted, DeepSeek (an open-weights model). The map watches from below and nods at each answer. | **Pose to pose** (each command is a key pose; typing fills the in-betweens), **overlapping action** (each card's accent bar lands after the card), **arcs** (cards enter on curved paths), **secondary action** (the map nodding) |
| 5 | 0:40.5–0:54 | **2 · The feature map** | 34 family tiles (F01 Server status … F34 TypeScript client) pop in as a diagonal wave. Counters land with a bounce: 34 families, 930 sub-feature IDs, 193 / 203 routes owned and driven, 10 excluded with reasons. Then everything dims except F18, which grows into the real bullet `F18.secret-empty-value` and its three-line recipe. The map peeks in to read along. | **Overlapping action** (the wave), **follow-through** (counters overshoot and settle), **staging** (one bullet at a time), **slow in / slow out** (the card growing out of its tile) |
| 6 | 0:54–1:05.5 | **3 · Known bugs as expected failures** | The `# bug` marker glows. One branch draws to **XFAIL · expected failure** ("the run stays green"). A beat later a "fix" travels the other branch and **XPASS · unexpected pass** bursts open ("the run fails until someone updates the map"). The map looks left, then right with a gasp and a hop. *A living contract, not a snapshot.* | **Anticipation** (the pause before the fix travels), **exaggeration** (XPASS pops larger than life, then settles), **arcs** (both branches), **secondary action** (the map's head turns) |
| 7 | 1:05.5–1:17.5 | **A full agentic run** | The 34 families sit on a ring with the map at the hub. Gold author agents fly out on arcs and prove recipes, mint reviewer agents re-drive each family on fresh servers, a completeness critic orbits the whole ring (the map's eyes follow it), red hardening agents stamp `# bug` markers, then a replay wave runs round the ring. | **Arcs** (every flight is curved), **overlapping action** (agents launch staggered, trails lag behind), **secondary action** (the map tracking the critic), **straight-ahead action** (the wave) |
| 8 | 1:17.5–1:31.5 | **The reveal** | `control-agent-server map run --all --fresh --record` is typed. The map crouches and holds its breath, then hops aside. One column per family fills from the real replay table: mint passes, gold expected failures, grey blocked. Counters run with the fill to **771 pass · 156 expected failures · 6 blocked**, then two zeros stamp in: **0 failures, 0 unexpected passes**. The map jumps for joy. | **Anticipation** (the held breath), **straight-ahead action** (the columns fill cell by cell), **timing** (the zeros arrive alone, after the counters settle), **follow-through** (counters and zeros overshoot), **squash and stretch** (the celebration hops) |
| 9 | 1:31.5–1:43.5 | **What it found** | A severity bar grows: 1 high, 37 medium, 89 low, 8 trivial (about 135 bugs). Seven category cards fly out of one deck on arcs and settle with a little rotational wobble: state not saved, validation gaps, the one high (data loss on key change), responsiveness, WebSocket and process lifecycle, server/client contracts, git and file edge cases. | **Arcs** (cards fan out from one point), **follow-through** (rotation settles after landing), **staging** (the one high gets the red border) |
| 10 | 1:43.5–1:55.5 | **The twist** | The bullet `F20.sdk-get-llm-linked` sits at XFAIL (issue #5514). PR #4952 pulls back, then sweeps in: "merged upstream". A replay pulse reaches the tile, which flips to **XPASS · unexpected pass: known bug no longer reproduces: update the map** (the CLI's real hint). The map leaps in surprise, lands, grins. The tile settles to **PASS · map updated**. *The map caught the fix the moment it landed.* | **Anticipation** (the PR card's pull-back), **squash and stretch** (the flip squashes the tile to a line and opens it with overshoot), **exaggeration** (the tallest jump in the film, wide eyes), **timing** (surprise first, delight a beat later) |
| 11 | 1:55.5–2:04.5 | **Outcome** | 31 new issues (#5622–#5652), 6 existing issues reproduced, 1 umbrella (#5653). A wall of real issue titles scrolls past, bending along an arc. Tracker URL. | **Follow-through** (numbers land and settle), **arcs** (the scrolling column curves), **slow in / slow out** (the scroll) |
| 12 | 2:04.5–2:13 | **Handled privately** | Security-relevant findings were reported privately. The four public hardening PRs, titles only: #5657, #5659, #5660, #5661. Then the review of community PR #4813 (BSmick6): five follow-ups offered as fixes on a branch. | **Staging** (nothing else on screen, no detail beyond public titles), **arcs** with **follow-through** (cards slide in, accent bars land after) |
| 13 | 2:13–2:24 | **Invitation** | *Open source. Reproducible.* `control-agent-server map run --all --fresh` types out. Links to the PR and the tracker. The map waves, crouches, folds itself back up and fades out. | **Appeal** (the wave goodbye), **anticipation** (a crouch before it folds), **squash and stretch** (the last hop) |

## Principles everywhere

- **Slow in / slow out**: every move uses cubic ease-in-out, ease-out or
  ease-out-back curves (`E.io`, `E.out`, `E.back` in `video.html`). Nothing
  moves linearly except the cursor blink.
- **Follow-through**: a damped spring (`wobble`, `settle`) on the map's pin
  after every landing, on counters when they finish, on cards when they land.
- **Squash and stretch**: `hop()` crouches before take-off (anticipation),
  stretches with speed, squashes on landing and settles. The x scale is
  `1/√sq`, so the map keeps its volume.
- **Secondary action**: the map's eyes always look at what matters in the
  shot: the terminal, the bullet card, the critic agent, the tile that flips.
- **Timing**: each idea gets a beat on its own. Reading time grows with text
  length. The biggest reveals, the zeros and the XPASS, come after a short
  hold.
- **Solid drawing**, in a flat-design sense: one consistent palette and type
  system (Instrument Serif headlines, DM Sans body, JetBrains Mono code), the
  same lamplit background in every shot.

## Production notes

- `video.html` draws any moment `t` with `renderFrame(t)`, so frames can be
  rendered in any order and in parallel. Open it in a browser with `?play`
  to watch in real time, or `?t=95` for a single frame.
- `render.mjs` serves the folder locally, drives headless Chromium with
  Playwright, and pipes PNG frames into ffmpeg (libx264, CRF 20,
  `yuv420p`, `+faststart`).
- Fonts are the OFL-licensed `@fontsource` builds of the site's three
  families, included in `fonts/`.
- The film has no audio track; all of its words are on screen.
