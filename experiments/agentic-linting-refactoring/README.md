# Agentic linting Before / After

The 84-second film accompanies [the rollout page](../../arch/agentic-linting-refactoring.html).
`agentic-linting-before-after.mp4` is the original 1080p H.264/AAC export,
with faststart for streaming. The page offers an ordinary same-origin MP4
download as well as inline playback. There is no release asset or login dependency.

The UI clips were recorded through `control-openhands browser record` on real
production Canvas builds, using local Agent Server 1.54.0 and Chrome. The same
baseline was captured before combining the four proposal heads in an isolated
worktree for the after run. No credentials were submitted, and no LLM was needed.
The lint-only sections use the results of actual ESLint probes.

`sources.json` records the source commits, capture setup, chapters, media hash,
and original synthesized music method. `progress.json` records the separate,
dated GitHub status snapshot used by the page. `poster.jpg` is the film's frame
at 30 seconds; it shows the actual secret-selection comparison. `captions.vtt`
describes the on-screen changes; the soundtrack contains quiet music only.

The source PRs retain the detailed tests, contrast measurements, app evidence,
and reproducible capture recipes. The combined film includes the secret-selection
change, now merged. The dated page snapshot tracks twenty-one merged proposals,
including the latest focus, context Usage, connection banner, and spec-note cleanup
changes. Ready-for-review #18504 tracks the composer context popover as the twenty-second
proposal, with its real Before/After evidence available, passing CI, and bot approval. Recording source
heads stay unchanged when the PR status snapshot is refreshed.

## Git Sync semantic colors

The 79-second Before/After film,
`git-sync-semantic-colors-before-after.mp4`, shows the same failed
repository check and sync cycle in Light+ before and after PR #18346. Short
title cards identify the hard-coded red utilities and their semantic
feedback-token replacement. The page offers inline playback and a direct MP4
download.

Both clips were recorded with `control-openhands` from production
Canvas builds and local Agent Server 1.54.0 in isolated baseline and PR
worktrees. No credentials or model calls were used. The soundtrack reuses the
Notebook's original ambient bed at a very low level (mean -46.1 dBFS, maximum
-33.2 dBFS). The matching poster, captions, chapter times, revisions, and media
hash are in `git-sync-semantic-colors-poster.png`,
`git-sync-semantic-colors-captions.vtt`, and
`git-sync-semantic-colors-sources.json`.

## Composer context popover

[#18504](https://github.com/OpenHands/OpenHands/pull/18504) addresses
[bug #18505](https://github.com/OpenHands/OpenHands/issues/18505). Its 18-second
`context-popover-before-after.mp4` compares real warning/danger states in Light+
at base `0c7c2258a8` and head `8189e21472`, using production Canvas, Agent Server
1.55.1, and DeepSeek Flash. The movie crops only the popover and blank composer
controls, excluding all conversation/sidebar content. It labels every Before/After
scene and contains original synthesized ambience at a maximum -42.9 dBFS.

The matching GIF, poster, captions, five-theme comparison, and component-only PNGs
are named in `context-popover-source.json`, which preserves hashes, source heads,
crop coordinates, configured context budgets, and 60 desktop/phone measurements.
The scoped warning/danger text, fill, and boundary checks pass; existing muted
Solarized text and the phone popover's 2 px left-edge clip remain unchanged.
The movie and screenshots document the proposed head. The dated status snapshot
records that #18504 is ready for review with bot approval; it is not
merged. The consent backend-scope text is the next separate color batch.

## Consent backend scope

[#18508](https://github.com/OpenHands/OpenHands/pull/18508) addresses
[bug #18507](https://github.com/OpenHands/OpenHands/issues/18507) with a single
scope-line color replacement. `consent-scope-before-after.mp4` is a ten-second
H.264/AAC film with original very quiet ambience; its silent GIF is eight seconds.
Both show only the real consent form on an isolated Local loopback backend,
without any conversation or account content. No model call or credential was used.

`consent-scope-source.json` preserves exact before/after heads, crop coordinates,
20 measurements across five themes and desktop/phone, behavior checks, and named
artifact hashes. The backend-scope line reaches 12.25–16.29:1; other description
colors are unchanged. Unchecking consent, confirming, and reloading still keeps
the preference false. The dated status snapshot keeps the proposal-head lint
counts separate from the base-main audit and tracks review/merge status.
