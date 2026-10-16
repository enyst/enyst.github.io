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
change, now merged. The dated page snapshot tracks twenty-two merged proposals,
including the latest focus, context Usage, connection banner, and spec-note cleanup
changes. Merged #18504 tracks the composer context popover as the twenty-second
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
records that #18504 merged on 16 October after passing CI and bot approval. The separate consent backend-scope batch is documented below.

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

At the dated status snapshot, #18504, #18508 and model profile messages
in #18510 are merged. Destructive buttons in #18513 are ready with green CI and bot review requested;
launch feedback in #18515 is ready with real Before/After evidence, passing CI,
and an initial all-hands-bot review request. Recording heads and media hashes stay attached
to the source revisions actually captured.

## Model profile messages

[#18510](https://github.com/OpenHands/OpenHands/pull/18510) addresses
[bug #18509](https://github.com/OpenHands/OpenHands/issues/18509) with semantic
colors for saved profile feedback. The ten-second `model-messages-before-after.mp4`
and eight-second GIF compare exact main `3419bdb4f7` with head `e71b4499fa`.
Only the real model-message component is shown, using generated QA profiles and
a synthetic loopback endpoint. The key readout is presence-only. No user
conversation content or credential value is visible; no model turn ran.

`model-messages-source.json` records 40 settled normal/hover captures across five
themes and desktop/phone viewports, source crops, idle/no-usage proof, named
artifact hashes, and explicit empty-hint/shared-wrapper coverage limits.
The source-branch audit reaches 659 warnings and 47 raw-color findings; it is
independent of the consent proposal. Main and proposal audits stay separately
recorded in `progress.json`. All earlier films and their recording heads remain.

The full CI run at `e71b4499fa` passed on Ubuntu and Windows: 9,097 tests
passed across 837 files (one skipped, seven todo), app/library builds passed,
and the package dry-run passed. Browser playback and the direct MP4 download
were also verified; the downloaded bytes match the source manifest.

## Shared destructive buttons

[#18513](https://github.com/OpenHands/OpenHands/pull/18513) addresses
[bug #18512](https://github.com/OpenHands/OpenHands/issues/18512) with semantic
colors for ghost and filled destructive BrandButton variants. The 18-second
`brand-button-before-after.mp4` includes original very quiet ambience; its silent
GIF lasts 16.01 seconds. Component-only source pixels show the generated local
delete-profile fixture and disabled built-in demo-app footer, without user data
or credential values. No model turn ran.

`brand-button-source.json` preserves exact base `8238b7af82` and after
`f52f2f7b29`, asset hashes, source crops, 80 actual theme/viewport/state captures,
and successful fixture delete/uninstall checks. Changed ghost text reaches
4.94:1 and filled text 4.89:1 at their minima. Filled labels already passed at
baseline; the reproduced contrast defect concerns ghost labels. Other variants,
Cloud/ACP and DigitalOcean are outside the recorded scope.

## Launch error feedback

[#18515](https://github.com/OpenHands/OpenHands/pull/18515) addresses
[bug #18514](https://github.com/OpenHands/OpenHands/issues/18514). The 14-second
`launch-before-after.mp4` and 12.01-second silent GIF show only the generic
real launch error card. Generated inert local metadata plus stopping the own
registered backend before Start triggers a real failed request, before any
source installation or model execution. No private path or user content appears.

`launch-source.json` pins base `8238b7af82` and after `6e1abb6408`, forty actual
creation-failure measurements, missing-source coverage, functional trust/retry
and Go Home checks, asset hashes and limits. Heading contrast reaches 4.94:1
and retry text 10.66:1 at the after minima. Retry already passed at baseline;
its change follows the theme. Source installation and Cloud/ACP authorization
are outside this recording's scope.

## Managed-agent focus: draft trace

Draft [#18520](https://github.com/OpenHands/OpenHands/pull/18520) records four
focus-token substitutions at `f7caf58063`. `managed-agent-focus-draft-source.json`
is a static palette audit, with a 3.26:1 minimum on the evaluated surfaces.
Authenticated affected-state evidence needs an authorized DigitalOcean Managed
Agents connection, an agent and a session, which the disposable stack lacks.
[Issue #18517](https://github.com/OpenHands/OpenHands/issues/18517) remains
unreproduced/unready; the description validator requires live proof. There is no
movie or authenticated-state verification claim, and no bot review request.

## Automation validation decoration

[#18526](https://github.com/OpenHands/OpenHands/pull/18526) addresses
[bug #18519](https://github.com/OpenHands/OpenHands/issues/18519) with three
raw-color replacements in error decoration. `automation-validation-before-after.mp4`
is ten seconds with original very quiet ambience; the silent GIF is eight seconds.
The real invalid-cron saved draft and Test guard run without model calls or dispatch.

`automation-validation-source.json` pins base `8238b7af82` and after
`2487541846`, forty actual desktop/phone captures across five themes, source crops,
asset hashes, behavior checks and limits. Existing baseline text already passed;
after minima remain 4.58:1 for the pill and 4.78:1 for the alert. The independent
head audit reports zero errors and 665 warnings, separate from historical main
and other proposal inventories. Other controls and Cloud integration are excluded.

## Device authorization feedback

Draft [#18528](https://github.com/OpenHands/OpenHands/pull/18528) addresses
[bug #18527](https://github.com/OpenHands/OpenHands/issues/18527). The 18-second
`device-auth-before-after.mp4` and 16.01-second silent GIF show actual local
warning/error components at base `8238b7af82` and after `bd30e4c7df`.
`QA-NOT-REAL` is visibly an invalid fixture; temporary issued-link pixels stay
private. No account grant, persistent key/backend save, or model turn occurred
during these auth captures. The borrowed baseline runtime's unrelated earlier
checks are outside this evidence.

`device-auth-source.json` records 140 genuine captures, five themes and both
viewports, scoped contrast minima, actual retry/cancel behavior, exact source
selection, hashes and limits. Successful Cloud authorization remains unverified;
its success icon uses separately labeled automated/static palette evidence.
Existing unrelated muted copy is outside the changed-text contrast claim.
Automation #18526 is now ready with green CI and its initial bot review requested.

## Parallel color proposals — 2026-10-16T08:23:31+00:00

- [#18529](https://github.com/OpenHands/OpenHands/pull/18529): Readable model saves. `bulk-model-dialog-before-after.mp4` is ten seconds with tiny original ambience; its silent GIF is eight seconds. `bulk-model-dialog-source.json` records exact base/after heads and actual scoped evidence. Two reported raw-color findings and six additional fixed-white uses are migrated. Unchanged shared muted copy and general hover behavior are outside this normal-state claim.
- [#18532](https://github.com/OpenHands/OpenHands/pull/18532): Theme-matched file chooser. `manifest-file-chooser-before-after.mp4` is ten seconds with tiny original ambience; its silent GIF is eight seconds. `manifest-file-chooser-source.json` records exact base/after heads and actual scoped evidence. One reported raw-color finding is removed. The existing focus recipe remains visible; this evidence does not claim a complete focus-indicator accessibility audit.
- [#18534](https://github.com/OpenHands/OpenHands/pull/18534): Readable hook diagnostics. `hook-diagnostics-before-after.mp4` is ten seconds with tiny original ambience; its silent GIF is eight seconds. `hook-diagnostics-source.json` records exact base/after heads and actual scoped evidence. Three reported raw-color findings and an unreported local badge map are migrated. Shared event titles, outer chevrons and unchanged muted child labels remain outside the changed-text claim.
- [#18535](https://github.com/OpenHands/OpenHands/pull/18535): Readable built-in critic score. `critic-messages-before-after.mp4` is ten seconds with tiny original ambience; its silent GIF is eight seconds. `critic-messages-source.json` records exact base/after heads and actual scoped evidence. Live proof covers score 0, header, stars, percentage, border and hint. Categories, detail expansion, intermediate and success scores, and probabilities remain live-unverified; separately labeled palette and existing behavior checks supplement this limited proof.

All four are draft at this publication snapshot while CI/readiness completes. Device authorization #18528 is now ready, and BrandButton #18513 and launch #18515 have bot approval. Budget #18533 and managed-agent #18520 remain draft for explicit backend/authenticated-state prerequisites. No current integrated-main warning count or rule-severity promotion is claimed. Markdown #18530 and chat #18531 evidence remain in progress.

## Chat-status feedback

[#18531](https://github.com/OpenHands/OpenHands/pull/18531), issue #18523,
compares base 8238b7af82 with 5b8ed56a6d. The eighteen-second
`chat-status-before-after.mp4` has four genuine component scenes, clear captions
and very quiet original ambience; the silent GIF is sixteen seconds. Forty
scoped measurements cover actual pending history loading and actual tool timeouts
in five themes, desktop and phone. Fetches resume ten to twenty generated user
messages. The neighboring generic header text remains outside the color claim.
Source metadata excludes conversation identifiers and private paths.

## Markdown links on actual supported surfaces

[#18530](https://github.com/OpenHands/OpenHands/pull/18530), focused issue #18522,
uses corrected head a0818714a239c8a957d4dd23f038779cc7de4822 versus 8238b7af82.
The 26-second `markdown-links-before-after.mp4` and 24-second silent GIF show
chat, Note alert and file-backed plan links before and after, with tiny original
ambience. All 140 actual captures include normal and hover measurements for
ordinary links, all five single alert types and a plan in five themes, desktop
and phone. All changed links pass 4.5:1 and retain safe destination attributes.
Only links are claimed; existing alert chrome and arbitrary nested composites
remain outside scope. The old 8ddc packet was held, not published as complete
evidence. Exact heads, source crops, actual values and hashes live in
`markdown-links-source.json`. CI/readiness is separate in progress.json.

## Final wave status — 2026-10-16T17:56:09+00:00

25 of 36 tracked proposals are merged, 9 are ready (including 5 approved),
and 2 remain draft for the explicit managed-agent authentication and budget
backend prerequisites. All 23 films and direct downloads remain intact.
Historical capture-time CI statuses and source heads are preserved; current
PR states and exact checks are recorded separately in progress.json.
