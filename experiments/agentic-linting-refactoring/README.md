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

## Remaining open work — 2026-10-16T22:02:00+00:00

33 of 36 tracked proposals are merged. Open status: 1 ready, 2 draft.
The ready hook proposal has green CI and its earlier inline thread is
resolved; approval remains required. Managed-agent and budget drafts retain
green test/build checks, while description validation still needs authentic
affected-state proof. Fresh read-only checks confirmed the account/runtime
prerequisites. All 23 films, source snapshots and historical audits are preserved.

## Budget lifecycle and SDK prerequisite — 2026-10-18T04:26:36+00:00

33 of 36 tracked proposals are merged; two are open and non-draft, and one is
draft. Hook #18534 is approved with green CI. Budget #18533 is non-draft at
50ae78643fb497b028bdddf6adfd0dea366b5b49; tests/builds pass, while description
validation still requires genuine live meter media before merge. Managed-agent
#18520 remains draft pending authenticated-state evidence.

Existing SDK [issue #5561](https://github.com/OpenHands/software-agent-sdk/issues/5561)
and [PR #5603](https://github.com/OpenHands/software-agent-sdk/pull/5603) are work
in progress. Conflicts and two inline findings are fixed at 091882a47; CI is
running, and a separately confirmed reservation-pricing gap is being corrected
before bot review. This is not an approved hard-budget contract. Per-run limits
differ from the current meter's lifetime-cost/task-cap values; client and Canvas
integration is still required. Live capture remains blocked by the normal local
launcher memory guard. All 23 films, source
snapshots and historical audit objects are preserved.

## SDK admission repair and companion guide — 2026-10-18T05:43:29+00:00

All 36 tracked Canvas proposals were rechecked: 33 merged, two open and
non-draft, one draft. Their media and account prerequisites remain explicit.

SDK [PR #5603](https://github.com/OpenHands/software-agent-sdk/pull/5603) is
published at 10bcfc30179d2338697377228f78975764dd024c (product code dceb668511cb6ccbc9e16dd3320b1a5d2019144b).
Local verification passed 122 focused and 1,725 broader LLM/local/remote
conversation tests. Full exact-head CI is green and the initial bot review
was requested after CI passed. Documentation companion
[PR #970](https://github.com/OpenHands/docs/pull/970) is ready at
4662e5ec98e67941fb0aa49b0b64c07ea3ca303a with green PR checks; its original
bot request is preserved. The two unrelated docs sync workflow definitions
still fail validation on unchanged docs main; those are not PR checks.

The SDK proposal remains unmerged and unreleased. It does not populate
`max_budget_per_task`; matching current-run usage snapshots in Agent Server
REST/WebSocket metrics, followed by client and Canvas integration, are still
required. Live meter capture remains blocked by the normal launcher memory
guard. All 23 films, source assets, and historical lint audits are unchanged.

## Fresh main audit and three small drafts — 2026-10-19T01:21:26+00:00

The new integrated-main audit at `83c9b64af66fae23a64aa07de6a3706cdab1144c`
records zero errors and 616 warnings: 521 arbitrary values in 176 files,
89 inline styles in 45 files, and six reported palette colors in two files.
`main-lint-audit-2026-10-19-83c9b64af6.json` is the full public, relative-path audit.
The original `lintAudit` and two older main audits remain unchanged.

The reported six are not the complete color backlog. The proposed five-owner
scan in [#18643](https://github.com/OpenHands/OpenHands/pull/18643) exposes
34 additional genuine palette declarations, for 40 under that scope. The broad
all-string probe's 46 includes six unrelated or valid-token findings. Seven
exact legacy-token exceptions remain necessary, and arbitrary hexadecimal
colors are owned by the separate arbitrary-value rule. No severity is promoted.

[#18641](https://github.com/OpenHands/OpenHands/pull/18641) replaces four
inline status colors with exact existing classes; 35 focused tests and local
type/app/library checks pass.
[#18642](https://github.com/OpenHands/OpenHands/pull/18642) moves two chooser
slide styles to static utilities; 30 focused tests pass and a real recording
is in progress. The five-owner scan passes five focused tests and changes no UI.
All three remain draft: CI is running and description validation is red.
No live affected-state pass is claimed from read-only API probes.

The cohort now contains 39 proposals: 34 merged, one open non-draft and four
drafts. Only the three new entries were refreshed in this update; the original
36 retain their 18 October status snapshot. Existing budget work, all 23 films,
media hashes and recording source heads are preserved.

## Class-map scan ready for review — 2026-10-19T01:46:02+00:00

[#18643](https://github.com/OpenHands/OpenHands/pull/18643) is ready at
`65828a3d51b91cc93ebdd3bb0519cdffd5a80b11`: all 13 current checks pass,
two are skipped, and the initial all-hands-bot review is requested and pending.
Its CI summary remains tooling evidence; no Canvas rendering claim is added.
The cohort has 34 merged, two open non-draft and three draft proposals.
The status-class and chooser-slide drafts still need matching live captures
under the normal launcher memory guard. Their existing check snapshots, the
original 36-PR snapshot, historical audits, budget work and all 23 films remain
unchanged.

## 19 October 2026 — macOS verification launcher prerequisite

PR [#18645](https://github.com/OpenHands/OpenHands/pull/18645), issue [#18644](https://github.com/OpenHands/OpenHands/issues/18644): original unused-memory guard refuses a real run despite native available memory above the unchanged 2,000 MiB threshold. Verification-only fix `743f204fd4c845a93d11fff3f8b973c65ecd6ade` passes 100 tests and launches the actual stack with doctor passing. `macos-memory-source.json` records original output, after doctor output, reviewed screenshot and exact hashes. UI captures can now proceed; CI remains pending. This prerequisite is outside the 39-proposal lint cohort.

## Status-color film published and scan approved — 2026-10-19T02:30:23+00:00

The 24th film, `status-classes-before-after.mp4`, shows the same colors before
and after [#18641](https://github.com/OpenHands/OpenHands/pull/18641): actual
+3/-1 git counts, an actual 404 toast and a real backend-disconnection CircleX.
It has clear Before/After labels, quiet original ambience, a same-origin MP4
download for Slack, a silent GIF, poster and captions. `status-classes-source.json`
records product heads 83c9b64af6/6e93317744 separately from the baseline
verification harness 743f204fd4, both SDK 1.55.1 runs, crops, hashes and limits.
Matching capture is complete, while the PR remains draft until its separate
media/readiness update. Only the five approved film files were added.

[#18643](https://github.com/OpenHands/OpenHands/pull/18643) now has all-hands-bot
approval on 65828a3d51 and no pending reviewer. The original 36-PR snapshot,
all historical audits, budget work and all 23 prior films remain unchanged.
The independent launcher [#18645](https://github.com/OpenHands/OpenHands/pull/18645)
remains draft, with 12 checks passed, one pending and two skipped in its last
CI snapshot. Its capture run is fully stopped and all owned ports closed;
only cleanup metadata changed in `macos-memory-source.json`.

## Chooser film published; status colors ready — 2026-10-19T02:38:28+00:00

The 25th main film, `backend-chooser-before-after.mp4`, preserves the full
70.54-second desktop and phone recordings at 1× speed, adding short chapter
cards, uniform letterboxing and tiny original ambience. The page has a
same-origin MP4 download for Slack, an eight-second excerpt GIF, poster,
captions and `backend-chooser-provenance.json`. All eight authentic originals
are copied byte-for-byte under `backend-chooser-raw/`; reduced-motion clips
are linked separately and clearly labelled. No credential, provisioning or
managed-agent execution is claimed.

Matching capture for [#18642](https://github.com/OpenHands/OpenHands/pull/18642)
is complete; the PR remains draft until its independent media/readiness update.
[#18641](https://github.com/OpenHands/OpenHands/pull/18641) is ready at
6e93317744, with 13 current checks passed, two skipped and its initial
all-hands-bot review requested. The scan #18643 remains approved; launcher
#18645 retains its last Ubuntu-pending snapshot. All 24 prior films, historical
audits, original 36-PR snapshot, budget work and launcher proof are unchanged.

## Final readiness snapshot — 2026-10-19T02:43:28+00:00

All four current PRs are ready, each with 13 checks passed and two skipped;
there are no current failed or pending checks. Status colors #18641, chooser
slides #18642 and independent launcher repair #18645 each have their initial
all-hands-bot review requested and pending. The class-map scan #18643 remains
approved at 65828a3d51 with no pending reviewer. All heads are unchanged.

The 39-proposal lint cohort now contains 34 merged, four open non-draft and
one draft. Launcher #18645 remains separate at 743f204fd4. Its capture run
is fully stopped, all owned ports closed and private run state purged.
Both published UI MP4s were independently served as HTTP 200 video/mp4 with
SHA-256 values matching their manifests. All 25 main films, original 36 dated
entries, historical audits, budget work, capture limits and media bytes remain
unchanged. This update makes no PR changes or review requests.
