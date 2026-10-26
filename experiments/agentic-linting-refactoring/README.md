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

## Fresh main audit and two palette batches — 20 October 2026

The actual full lint command passes at exact main `8d39305538c1d17a30cbe477e57a0e18fcee7d95`:
**0 errors and 645 warnings across 1,408 linted files**. The breakdown is
522 arbitrary-value findings in 177 files, 83 inline-style findings in 42 files,
and 40 palette findings in seven files. Another 47 hardcoded-color messages
belong to the arbitrary-value total. Typecheck and formatting pass.
`main-lint-audit-2026-10-20-8d39305538.json` preserves all active messages with relative paths, exact
commands and runtime versions; its SHA-256 is
`62315fdf08d20d0484ea2d180a94c5e393f4df3eb2f1a86cbe8aa3a857c84a0d`.
The 616-warning audit at 83c9b64af6 remains unchanged dated history, alongside
the earlier audits. The new proposals do not change that 645-warning main result.

[#18694](https://github.com/OpenHands/OpenHands/pull/18694), issue
[#18693](https://github.com/OpenHands/OpenHands/issues/18693), removes two fixed
failure-dot palette classes at `123afde75d2c94caff4b3a0e31fae2b461d20857`. It is ready with eight checks
passed, six skipped and all-hands-bot approval at this exact head. The PR remains open. All 112 focused tests
pass. The 54.2-second
`health-dots-before-after.mp4`, silent GIF, poster, captions, source manifest
and original-capture ZIP preserve the actual missing-command MCP and stopped
secondary-backend paths. Forty paired captures span five themes and both
viewports using Agent Server/SDK 1.56.0. Baseline contrast already passed 3:1;
minimum sampled nontext contrast changes from 3.107 to 3.774:1. Eight superseded
wrong-cause light-theme screenshots are explicitly excluded. No model turn,
authenticated Cloud/ACP session or custom embedded-host visual pass is claimed.

[#18696](https://github.com/OpenHands/OpenHands/pull/18696), issue
[#18695](https://github.com/OpenHands/OpenHands/issues/18695), removes twenty
palette warnings through five alert-owned roles at `e2c79483dd4fda6099686ee4b165d79cef4e5937`. Five families,
labels, icons and parsing remain; quieter 5% tints and contrast body ink cover
nested alerts. The actual Files prose regression first reproduced 3.376:1
Solarized emphasis, then passed with scoped emphasis/headings/code/kbd/caption/
marker roles; bold links retain link ink and ordinary Markdown is unchanged.
All 69 focused tests and full local lint pass with 0 errors and 625 warnings.
Independent implementation review is clear. Actual Before/After capture spans
five themes, desktop/phone and agent chat, user Markdown and Files previews.
The `markdown-alerts-*` film, GIF, poster, captions, provenance, paired matrix
and 140-image evidence ZIP are assembled. The 53.8-second film is 1440 × 1120,
with quiet original ambience. Selected live title/icon contrast improves from
1.003:1 to at least 4.558:1; body/emphasis reaches at least 8.520:1 and links
at least 4.848:1. Both platform jobs and media-description validation pass:
eight checks passed and six skipped. The initial bot review is requested and
pending; no approval or merge is claimed.

Both capture stacks are stopped, all owned ports closed and private run state
purged. Recording heads and final hashes belong to their source manifests.
All 25 earlier films, their 50 MP4 download links, historical audits, original 39
PR objects, budget records and completed approvalWatch are retained. The cohort
currently has 41 proposals: 37 merged, 3 open non-draft and 1 draft. Both new
proposals are ready with green current checks. All-hands-bot approved the health
dots at exact `123afde75d`; its initial Markdown review is pending. The existing non-draft budget policy case is separate from these
two batches; the remaining draft requires authorized DigitalOcean evidence.

Twelve start-task badge/indicator palette findings are currently unreachable
through an ordinary Local or Cloud launch: `useStartTasks` returns `[]`, and
its selector excludes READY/ERROR. Restoring real list data and deciding
terminal-state visibility is separate product work before live evidence.
Managed-agent focus retains its authorized DigitalOcean-resource prerequisite;
budget-meter cleanup retains its existing description-policy gate and separate
SDK/client/Canvas integration path. A next independent style candidate is the
Markdown diff-preview's one 600 px `maxHeight` warning; preserve the shared
`MAX_DIFF_EDITOR_HEIGHT_PX` owner and verify its real old/new view before changing it.


## Integrated main and two ready layout batches — 21 October 2026

The fresh exact-main audit at `630e587a0de0b4106173ba0d39ac865d60a51a5a`
passes the full lint command with **0 errors and 618 warnings across 1,417 linted
files**, with diagnostics in 194 files: 517 arbitrary-value findings in 177 files,
83 inline-style findings in 42 files, and 18 palette findings in four files.
The 47 additional hardcoded-color findings across 20 files are included in the
arbitrary-value total. Typecheck and formatting pass.
`main-lint-audit-2026-10-21-630e587a0d.json` preserves all active messages,
relative paths, commands and runtime versions. Its SHA-256 is
`781fa6883e4c194b5ef2b72445ed14fa598bd35793c3c10b5504360a5bd574b0`.
The original audit and all four earlier main audits remain unchanged.

Health dots [#18694](https://github.com/OpenHands/OpenHands/pull/18694) merged
on 20 October at `2026-10-20T19:13:45Z` as
`3c1cb1a6551464001c46988648a2dad9c32107f7`; Markdown alerts
[#18696](https://github.com/OpenHands/OpenHands/pull/18696) merged at
`2026-10-20T19:13:24Z` as `87b9496342c935b7fc35db29d2384cab9e49e425`.
Their 22 removed palette findings account for part of the 27-warning reduction
from the historical 645-warning audit. Seven arbitrary-value warnings disappeared
with the old automation setup prompt stack, offset by two new profile-picker
warnings. The merged films keep their exact captured heads and media hashes.

Two new independent ready batches each remove one configured inline-style warning:

- [#18762](https://github.com/OpenHands/OpenHands/pull/18762), issue
  [#18757](https://github.com/OpenHands/OpenHands/issues/18757), uses a static
  `max-height` utility consuming a numeric custom property backed by the existing
  600 px `MAX_DIFF_EDITOR_HEIGHT_PX` owner. Exact head
  `499ddf307010062beac5dfa30ac85f49083bbe88` passes 17 existing focused tests,
  typecheck, formatting, app/library builds and the compiled scoped CSS check.
- [#18763](https://github.com/OpenHands/OpenHands/pull/18763), issue
  [#18758](https://github.com/OpenHands/OpenHands/issues/18758), uses a static
  width utility consuming the existing 268 px
  `CONVERSATION_OVERVIEW_COLUMN_WIDTH_PX` owner through a numeric custom property.
  Exact head `bde133fb5e75019021bbf603c62567ea4aa3a741` preserves the outer Framer
  Motion animation and passes 11 focused tests, typecheck, formatting, app/library
  builds and the compiled CSS check.

An independent review of the code and emitted CSS is clear at both exact heads.
Matching actual `control-openhands` Before/After checks are complete and both film
packets are published. Each PR is ready at its unchanged exact head, with eight
checks passed, six skipped and no failed or pending checks, including successful
media-description validation. The initial all-hands-bot reviews were requested on
21 October and are pending. These scoped branch results do not change the
separately measured integrated-main count of 618.

The current cohort has **43 proposals: 39 merged, three open non-draft and one
draft**. The existing non-draft budget cleanup retains its policy gate and
SDK/client/Canvas prerequisites. Managed-agent focus retains its authorized
DigitalOcean-resource and live-evidence prerequisites. The twelve remaining
start-task palette findings still lack an ordinary Local/Cloud launch path:
`useStartTasks` returns `[]` and excludes READY/ERROR. All original 39 PR objects,
the completed `approvalWatch`, 27 existing films and their 54 MP4 download links
are preserved. The previous 41-proposal snapshot remains dated history.

The next independent small candidate is the static 18 px automation-run
sparkline track, owned by `AUTOMATION_RUN_ACTIVITY_TRACK_PX`. Verify its real
card/list consumers before migrating it; duration-derived per-bar heights
retain separate runtime ownership. Seven exact legacy-token exceptions and
other dynamic, renderer and accessibility owners remain part of the staged audit.


## Static-style live evidence — 21 October 2026

The Markdown preview packet, `markdown-preview-cap-*`, compares exact main
`630e587a0d` with `499ddf3070`: sixteen geometry/scrolling pairs have no differences,
and twelve pairs also preserve captured text excerpts/button states. Real uncommitted
and historical old/new Markdown plus Diff mode are exercised in Chrome at
1440 × 1000 and 390 × 844, with representative Neutral, Light+ and DeepSea checks.
Long previews stay 600 px high; short desktop previews measure 185/221 px and the
phone preview 209 px. Real scroll positions reach 800/700 px with no horizontal
page overflow. The selected packet contains 20 PNGs and four original clips.
Four initial After theme screenshots raced rendering and are replaced by settled,
verified captures. Existing Monaco disposal issue #17567 occurred in both phases:
three baseline events, including a discarded recording attempt, and two After
events, with no other captured page-error message. It is outside this patch.

The overview packet, `overview-column-width-*`, compares the same main with
`bde133fb5e`: fourteen paired semantic/layout checks have no differences. The
visible inner/outer columns stay 268 px wide around a 240 px card; opening,
closing and side-panel exclusion are preserved. Width checks cover 1440, 1100,
1024 and 390 px, with representative Neutral, Light+ and DeepSea checks. The
selected packet contains 18 PNGs and five original clips; one initial baseline
phone screenshot is superseded for state proof by a separately recorded pressed-on
DOM measurement. Existing #16792 reproduces in both phases: the phone/tablet toggle can be pressed while no
overview card is rendered. That state is not counted as a visible-column pass
or a fix. The fresh overview After run has zero page errors.

Both packets use real Local Agent Server/SDK 1.56.0, automation 1.22.0 and Canvas
1.29.0 through `control-openhands` and Google Chrome. Build fingerprints are
`8e676f49549e7308` Before, `5eaccd708ea64185` preview After, and
`d6a9fbc5aa60245d` overview After. Bounded DeepSeek Flash responses used no tools
and recorded zero ActionEvents. No mocks or verifier source/driver edits were
used. All three owned stacks are stopped, private run state is purged and owned
ports are closed. The `*-sources.json` manifests preserve these checks and limits;
final MP4/GIF/poster/captions and selected-original ZIP packets are assembled.


The published preview film is 34.6 seconds and the overview film 33.2 seconds,
both 1440 × 1120 H.264/AAC exports with tiny original synthesized ambience. The
page retains all 27 earlier films/54 MP4 download links; these two new sections
bring it to 29 films/58 links. Each `*-sources.json` records the final named media
hashes and bytes, with capture provenance, paired measurements, a silent GIF and
selected-original ZIP. Film, GIF and original MP4 downloads return HTTP 200 with
matching full SHA-256 values. Media were published in Notebook commit
`f6829d1fbe8baf5ce310f60a40440d60678beb27`; both PRs are ready and their initial
bot reviews are requested, with no approval or merge claimed.


## Layout merge and review follow-up — 22 October 2026

Overview width [#18763](https://github.com/OpenHands/OpenHands/pull/18763)
merged at `2026-10-21T23:22:38Z` (22 October 01:22 Stockholm) as
`ea2f42bf6e6c58ab1a2f753df7c3912b37c9a6d8`, after bot approval. Its film
and source manifest remain pinned to the actual recorded `bde133fb5e` head.

Markdown preview [#18762](https://github.com/OpenHands/OpenHands/pull/18762)
now has test-only follow-up `0876b39f76b314d1a8fcc5bc71c8730f36664e19`. The
original bot review verified the implementation but requested a functional
CSS-contract guard. All 23 focused diff-viewer tests pass; mutations of the CSS
reader, custom-property writer and removal of the cap each fail the new test.
The [inline finding is answered](https://github.com/OpenHands/OpenHands/pull/18762#discussion_r4343018059)
and the solved thread is resolved. Current exact-head CI is green: eight passed, six skipped and none failed
or pending, including Ubuntu, Windows and required media-description validation.
The new all-hands-bot review explicitly requested by the user was requested at
`2026-10-21T23:38:08.145901+00:00` (22 October 01:38 Stockholm). The bot
[approved exact `0876b39f76`](https://github.com/OpenHands/OpenHands/pull/18762#pullrequestreview-5607576348)
at `2026-10-21T23:43:44Z` (01:43 Stockholm), confirming the old finding is
resolved and no material gaps remain. It independently verified four guard
mutations fail: reader mismatch, writer mismatch, removed cap utility and
a 900 px cap. The PR remains open; this update performs no merge. The 34.6-second film still records product head `499ddf3070`;
the test follow-up does not change the captured product source.

The current 44-proposal cohort is **40 merged, three open non-draft and one draft**.
The separate 18 px sparkline-track batch is in progress under
[issue #18787](https://github.com/OpenHands/OpenHands/issues/18787), with 34
focused tests passing. Ready [#18788](https://github.com/OpenHands/OpenHands/pull/18788)
at `e89f502061bc89ddb7811352a471b13d4c5126d5` removes one target-file warning
(eight to seven, zero errors) and passes typecheck, formatting and app/library
builds. Its compiled CSS-contract guard fails reader mismatch, writer mismatch
and removed-class mutations. Actual `control-openhands` capture now verifies 24 fixed-geometry pairs with
zero differences across Dashboard grid/list and Home pinned card/activity row,
desktop/phone and Neutral/Light+/DeepSea. Tracks remain 16 × 18 px with two 4 px
bars and 8 × 18 px link targets. Eight actual bar deep links work. The 48 selected
PNGs and four original clips accompany the published film. The PR is ready at
its unchanged exact head, with eight checks passed, six skipped and none failed
or pending. Its initial all-hands-bot review was requested at
`2026-10-21T23:49:16.143763+00:00` (22 October 01:49 Stockholm) and is pending. Four independent genuine DeepSeek Flash runs used
only finish actions and produced zero browser/app errors. Their natural durations
differ: Before 42.867/35.692 seconds yields 11/10 px bars; After 24.066/22.180
seconds yields 10/10 px bars. All 96 individual bar-height formula checks pass.
No identical-pixel or equal dynamic-bar-height claim is made. Both fixtures are
deleted, both owned stacks stopped, all ten ports closed and private state purged. Duration-derived bar heights retain their runtime owner.

A fresh complete main audit at `ea2f42bf6e6c58ab1a2f753df7c3912b37c9a6d8`
now records **0 errors and 617 warnings across 1,419 linted files**, with
diagnostics in 193 files: 517 arbitrary-value findings, 82 inline-style findings
and 18 palette findings. Full lint, configured machine ESLint, typecheck and
formatting pass. The sole normalized diagnostic change from the previous
618-warning audit is the merged overview-column width finding. The public
`main-lint-audit-2026-10-22-ea2f42bf6e.json` has SHA-256
`c16d1d6eee9eedb9985feb9802334c4036b6ec76e1009750c0cee39aa1912ce9`.
The earlier 618-warning audit remains pinned to `630e587a0d`. All five previous
main audit objects and twelve proposal audit objects are preserved unchanged;
the new audit is a sixth entry. All 29 films/58 MP4 download links, original
recording heads, prior proposal metadata, the completed approval watch and
existing prerequisite records remain. No preview or sparkline proposal reduction
is counted on integrated main.


## Automation activity-track film — 22 October 2026

The new `automation-activity-track-*` packet compares exact merged main
`ea2f42bf6e` with proposal `e89f502061`. The approved 31.4-second 1440 × 1120
film is assembled, with clear Before/After labels, normal six-second
desktop excerpts per phase, complete 3.9/4.1-second phone clips and actual
Light+ pinned-card details. Its caption says “Same 18 px track · Real run
durations differ.” Tiny original ambience accompanies the film. The source
manifest, silent GIF, poster, captions and selected-original ZIP are finalized
and published in `0f8803ceee6d8a5dc0786018386aac267c19d492`. Immutable
film/GIF downloads return HTTP 200 and match full SHA-256 values. The PR is
ready at its unchanged exact head, with eight checks passed, six skipped and
none failed or pending, including required media-description validation. Its
initial all-hands-bot review is requested and pending. Ambience measures −52.5 dBFS mean and
−42.9 dBFS peak. The film SHA-256 is
`2d6ece4cc61a19dc59816ea7e4fbe075241c2ae546fec1f4cd29e2aa1c3108a9`;
the source manifest SHA-256 is
`dd5fce4847a8e4d21e1400dbc6dd16c1e03ea30e0f0a659ea4c8ab20c511e8bc`.
The added page section preserves all 29 previous films and 58 MP4 download
links, bringing the page to 30 films and 60 MP4 download links.


## Next small ownership batches — 22 October 2026

The maintainer merged Markdown preview #18762 at `2026-10-22T01:40:11Z`
as `20bb37e39d7268bfd176f54b3d2e461d3b2ada57`, then activity track #18788 at
`01:40:46Z` as `70b8f9069dec3d1c39a04d755521ebe6bd252aab` (03:40 Stockholm).
Both had bot approval and green exact-head CI. Their captured product heads,
media hashes and limits remain unchanged. This update performs no merge.

A fresh locked install, full lint, typecheck, formatting and machine ESLint
pass at exact main `70b8f9069d`: **0 errors and 615 warnings across 1,419 files**,
with diagnostics in 192 files — 517 arbitrary-value, 80 inline-style and 18
palette findings. Only the two merged preview/track findings disappear from
the prior 617-warning inventory. Main also includes unrelated Canvas 1.30,
extensions 0.33 release and Mars opt-in changes. The public
`main-lint-audit-2026-10-22-70b8f9069d.json` has SHA-256
`8df2711affa0ca96c803da644331b17fb662c37f6870123854568f3b831cce58`.
All six earlier main audit objects and twelve proposal audits remain unchanged.

Two independent ready proposals each remove two scoped inline-style findings:

- [Sidebar #18805](https://github.com/OpenHands/OpenHands/pull/18805), issue
  #18803, at `546e76f1e1809899fdbef98412c5da633435c329`: the existing 250 ms
  `MOBILE_DRAWER_TRANSITION_MS` still owns CSS duration and the removal timer.
  Thirty focused tests pass; all four reader/writer/removed-utility/early-timer
  mutations fail. Target lint drops four warnings to two, with zero errors.
- [Tree #18804](https://github.com/OpenHands/OpenHands/pull/18804), issue
  #18802, at `290c2368052c2c54f67c95c421390b9e45356b72`: the same 8 px base,
  12 px per depth and 16 px file offset feed a static padding reader. Thirty-two
  tests pass, including the real CSS contract and native Space/Enter behavior.
  All six folder/file reader/writer/removed-utility mutations fail. Target lint
  drops two warnings to zero; app/library CSS and ESM/CommonJS wiring pass.

Typecheck, formatting, app/library builds and independent implementation reviews
pass for both. Each has **eight current checks passed, six skipped, none failed
or pending**, including Ubuntu, Windows and required media-description validation.
Initial all-hands-bot reviews were requested after green CI and verified pending
at `2026-10-22T03:42:42.017175+00:00` for tree and `03:42:47.088784+00:00` for
sidebar (05:42 Stockholm). Neither new proposal is approved or merged here.
Their unmerged reductions are not counted in main's 615-warning total.

### Authentic runtime evidence

Sidebar: six style/layout pairs and fifteen control/route pairs match across
Neutral/Light+/DeepSea, 1440 × 1000 desktop and 390 × 844 phone. Close, Escape,
backdrop and navigation preserve outcomes. CSS duration is exactly 250 ms;
sampled visible closing intervals span 236–238 ms Before and 237–246 ms After.
These are DOM-presence samples, not exact timer-start or every-frame timing.
Actual reduced-motion preference is false. Forced emulation is unavailable in
the normal CLI, so no forced live pass is claimed; its compiled contract is tested.
The selected sidebar source set is 18 PNGs and two original clips.

Tree: all 36 indentation/content contracts and 24 control pairs match across Files
root through depth three and plugin manifest/nested skill. Thirty raw geometry
pairs match exactly; six plugin-phone pairs retain a 16 px absolute row-y offset
because the actual After run-cache path wraps to four lines versus three Before.
Relative indentation, row size/x, colors, selection/content and controls match.
Raw offsets remain; no 36-pair zero-geometry-difference or pixel-identity claim
is made. Two bounded actual DeepSeek Flash turns provide the conversation
context; zero ActionEvents are recorded. Titles, Thinking and elapsed labels
differ naturally. The selected tree source set is 40 PNGs and eight raw clips.

Final source sets match the collapsed Getting started card through actual UI
controls and reset open files through normal close buttons. Initial expanded-card
captures are superseded and excluded. Real production Canvas 1.30.0, Local Agent
Server/SDK 1.56.0, automation 1.22.0 and Chrome run through unchanged
`control-openhands`. Captured baseline 70b8f9069d/build c73929d5131944fc,
sidebar 546e76f1e1/build dfdde6888d0dedfd and tree 290c236805/build 8b2236968d5f6516
remain exact. All four owned runs are stopped, private state purged and owned
ports closed. Zero browser/app errors are recorded. No mocks or verifier edits.

### Films and preservation

`mobile-sidebar-duration-*` is 26.2 seconds at 25 fps, keeping the full 6.32/6.48-second
phone clips. `file-tree-indentation-*` is 31.8 seconds at 30 fps, keeping complete
Files/plugin desktop and plugin-phone clips plus actual Light+ context/detail
crops. Source 15 fps frames are duplicated without a speed change. Both films are
1440 × 1120 with tiny original ambience (means −52.9/−52.6 dBFS; peak −42.9 dBFS).
The 58 original PNGs, ten complete raw clips and two actual lossless tree-detail
PNGs remain downloadable with source hashes and sanitized provenance.

All final MP4/GIF/poster/captions/source/provenance/ZIP packets are published in
Notebook commit `9d241d3ada0d621d7f794f36413700801563197c`. All 25 critical
immutable files return HTTP 200 and match full SHA-256 values. All six live Pages
film/GIF/ZIP downloads also return 200 with matching hashes; Pages MP4s have
`video/mp4` Content-Type. Raw GitHub MP4 downloads use `application/octet-stream`.
Sidebar film SHA-256 is
`b15579730a1cb2ec01cfa218e508dcc6fce797b4369111fc1141720100fe1d1d`;
source manifest is `14402ea14b1cbc8fb5439c28340890a458fd899039c4dbdb65cfdf5b9ff17ca0`.
Tree film is `df3479189febf3545420d7a824b27a2d6a0dbafe3d3b76be378d02dc29c0912f`;
source manifest is `366905a74b6d507ba4777f271c20701cac1d18086ca388352bfa57b40679b7bb`.

The 46-proposal cohort is **42 merged, three open non-draft and one draft**.
Budget #18533 remains open/non-draft; managed-agent focus #18520 remains draft.
Their bodies and prerequisites are unchanged. All 30 earlier films/60 download
anchors, 561 prior non-doc assets, attribution history, unaffected prior proposal
objects, earlier audits, recorded heads and the finished approval watch are
preserved. The two additional sections bring the page to **32 films/64 MP4 download
links**. Earlier README text remains an unchanged published prefix.


## 23 October 2026: phase offsets and duration-owned bar heights

Snapshot `2026-10-23T06:38:58.021657+00:00` (Stockholm display time). The maintainer merged tree
[#18804](https://github.com/OpenHands/OpenHands/pull/18804) at 07:18 Stockholm as
`f0254fd6a3e5d891e998da0293162ff872a6868f`, then sidebar
[#18805](https://github.com/OpenHands/OpenHands/pull/18805) at 07:19 as
`3083e1aa1660bd45769b01e5ad5ded0b6c4be302`. Both unchanged recorded heads
received all-hands-bot approval on 22 October with no inline findings. Their
historical media and verification remain pinned to their recorded source heads.

Audited main `3083e1aa16` passes locked installation, full lint, typecheck,
formatting and machine ESLint: **611 warnings, zero errors, 1,420 linted files,
191 diagnostic files**. Inventory: 517 arbitrary values in 177 files, 76 inline
styles in 38 files and 18 palette findings in four files. The
[public audit](main-lint-audit-2026-10-23-3083e1aa16.json) has SHA-256
`4a2db83d8e6807621eacae3e9c54677e7adb75d9fa5fc69fd71453a8e4fa01fc`.
The sidebar/tree merges remove four inline findings. An unrelated automation
prompt width replaces one arbitrary-width diagnostic with another, without
changing that rule’s count. Both new branches independently remove one warning;
neither is integrated in the 611-warning measurement.

### Onboarding offsets: ready with matching published evidence

[PR #18856](https://github.com/OpenHands/OpenHands/pull/18856), issue #18854,
at `edf5f19e877b33130e9f42d94ed793e05f7deb0d`, moves the phase-derived percentage
to `--onboarding-slide-offset` and native `translate-x-(--onboarding-slide-offset)`.
The phase formula, active/inactive positioning, Next/Back handlers and configured
300 ms transition are unchanged. All 34 tests pass; three reader/writer/removed
reader mutations fail. Target lint falls from two warnings to one, retaining the
existing arbitrary max height. Typecheck, formatting, app/library builds and real
emitted CSS checks pass; independent implementation review found no material issue.
The standalone onboarding route is not a public library JavaScript consumer.

All **43 paired geometry states match** across genuine healthy Local first-run
Next/Back and documented preview routes in all five themes, at desktop 1440 × 1000
and phone 390 × 844. Healthy Local has three phases; four-phase backend addition
and four-to-three collapse remain existing unit/CSS-contract coverage. No live
backend-down, public authentication or exact wall-clock animation-time claim.
Before transform matrices and After individual translate are normalized using
actual rectangles. No model or credentials are used; zero browser/app errors.
Both owned runs stopped, private state purged and owned ports closed.

Exact source/build: Before `3083e1aa16` / `e702ca2a7aca7a47`; After `edf5f19e87` /
`fa7f57783f9a371d`. Production Canvas 1.32.0, Agent Server/SDK 1.58.1,
automation 1.25.1, extensions 0.35.0 and Chrome use unchanged `control-openhands`.
The 25.92-second, 25 fps, 1440 × 1120 H.264/AAC film retains full original selected
clips without speed changes, with quiet original ambience (mean −52.5 dBFS,
peak −42.4). The packet includes 64 PNGs, ten full raw clips and 83 ZIP members.
[Sources](onboarding-slide-offset-sources.json), [MP4](onboarding-slide-offset-before-after.mp4),
[GIF](onboarding-slide-offset-before-after.gif) and [original evidence](onboarding-slide-offset-evidence.zip)
are published at [immutable Notebook `0e6de40f05`](https://github.com/enyst/enyst.github.io/commit/0e6de40f0560d2327bfbde40d80f95ff51013844).
Critical downloads return HTTP 200 with full SHA-256 matches. Film SHA-256:
`c5ff711e39f8cf7ec8779aeb4880a41f9127a33af3fb9b550de8f56bf2dbcfd2`.
Eight checks pass and six skip. [All-hands-bot approved exact head `edf5f19e87`](https://github.com/OpenHands/OpenHands/pull/18856#pullrequestreview-5624777083)
on 23 October at `2026-10-23T06:36:00Z` (08:36 Stockholm), with no material
correctness, security, compatibility or architecture findings and no inline comments.
The PR remains ready and open. Automation bar heights still awaits its initial bot review.

### Automation bar heights: ready with matching published evidence

[PR #18857](https://github.com/OpenHands/OpenHands/pull/18857), issue #18855,
at `087e91d34a9ac8ee5954e8e741774ccf7cc1713d`, feeds the existing duration result
to `--automation-run-bar-height` and native `h-(--automation-run-bar-height)`.
The duration helper, 6/15/11 px metrics, one-second timer and 18 px track retain
their owners. All 47 tests across seven suites pass; four reader/writer/removed
reader/timer mutations fail. Target lint falls seven warnings to six; independent
full branch lint passes at 610. Typecheck, formatting, builds and real emitted
CSS/app JavaScript checks pass. This route-owned component is not exported in
public library JavaScript. Independent implementation review found no material issue.

All **182 computed-height/duration checks pass** against each run’s own server
timestamps and unchanged mapping. Five themes cover the common Dashboard grid
at desktop/phone; Neutral desktop/phone covers all four app consumers. Eight real
keyboard Enter navigations per phase reach target URLs. No visible selected-row
highlight proof is claimed. Genuine matched Running grows **7 → 8 → 9 px** on both
phases in fresh one-run Neutral 1440 × 1000 captures with Getting started expanded.
The initial 12.48-second Before clip is authentic Pending/unknown **11 px fallback**,
not growth. Earlier After Solarized/four-run/collapsed-card motion is separate
context coverage, excluded from the matched film. The 6/15 px clamps remain unit
coverage. No synthetic statuses, timestamps, run rows, LLM calls or credentials.

Real bounded SDK LocalWorkspace workers send canonical callbacks; the server owns
completion timestamps. A plain exit-zero setup attempt without the callback is
excluded from completion proof. Original phases build fingerprints
`e702ca2a7aca7a47` Before and `1379495a41a2bc43` After. Matched growth reuses those
exact assets with `builtThisRun: false`. All four sparkline runs stopped, private
state purged and owned ports closed. Correct final custom-property writer and
computed height both read 11 px after actual completion. An earlier optional probe
queried an unused property and supplies no writer proof. Actual computed heights,
the unchanged map and compiled reader/writer guards supply the contract.
The frozen film is **32.56 seconds**, 814 frames at 25 fps, 1440 × 1120,
H.264/yuv420p with AAC and fast start. Original quiet ambience measures −52.5 dBFS
mean and −42.5 peak. The matching packet includes 48 original PNGs, eight full
raw clips and a 68-member ZIP, with full source hashes and decoded-media checks.
The valid silent GIF represents all 260 samples at 8 fps; identical holds merge
into 229 encoded frames, with an explicit final 60 ms still hold to retain the
32.56-second elapsed playback. No motion interpolation.
[Sources](automation-bar-height-sources.json), [comparison](automation-bar-height-comparison.json),
[MP4](automation-bar-height-before-after.mp4), [GIF](automation-bar-height-before-after.gif)
and [original evidence](automation-bar-height-evidence.zip) are published at
[immutable Notebook `5658681094`](https://github.com/enyst/enyst.github.io/commit/5658681094b9e28ba0a30f8e7d40e26d83d9fc75).
Critical raw downloads return HTTP 200 with full SHA-256 matches.
Film SHA-256: `ad8d16a702e8db7fefb16f5c45d8b3dd8b0f9083e2178236e6c4da2aa5c85c62`.
All eight current checks pass and six skip, including code CI and required media
description validation. The unchanged proposal head is ready; its initial
all-hands-bot request is verified and pending, with no review submitted yet.
No approval or merge is claimed. Live Pages deployment remains unverified here
and is checked separately after the final document push.

### Preservation

The **48-proposal cohort has 44 merged, three open non-draft and one draft**.
Budget #18533 and managed-agent focus #18520 retain their existing records and
prerequisites. All 44 unaffected prior proposal objects, seven prior main audits,
twelve prior proposal audits, 32 films/64 download anchors, 654 old assets
(114,840,526 bytes), exact recording heads and the finished approval watch are
preserved. The two new sections add two films/four download anchors: **34 films/68 MP4
download links**. All 88 published onboarding assets and 73 published automation assets remain unchanged. This README’s earlier published text is an unchanged byte prefix.

Upstream main advanced during capture to `a832d9a2850ffd8c12c14597a545b454f349ff42`. The 611-warning audit remains pinned to `3083e1aa16`; the newer lifecycle revision has not been re-audited. Proposal heads, media sources and their CI receipts are unchanged.


## 24 October lifecycle and exact-main audit

Onboarding offsets [#18856](https://github.com/OpenHands/OpenHands/pull/18856)
merged at 06:59:47 UTC as `3dce57817d13db6572dd50c1e5436d0ffe397fd0`.
Automation bar heights [#18857](https://github.com/OpenHands/OpenHands/pull/18857)
merged at 07:00:37 UTC as `084a4106040a0d64a02ac04eecf88ea8a8a8f31b`.
Both bot and maintainer approvals are retained in `progress.json`, including
their exact review bodies, submitted times and commit identities. Recording
heads, historical checks and published media remain attached to the captured
source revisions.

The existing cohort is **48 proposals: 46 merged, one open non-draft and one
draft**. All 46 other proposal objects, eight earlier main audits, fourteen
proposal audits, 34 video elements, 68 MP4 download anchors, 816 experiment
assets and the completed approval watch are preserved. This README's entire
earlier content remains an unchanged byte prefix.

Fresh exact integrated main **`084a410604` passes with 0 errors and 612 warnings**
across 1,425 linted files, with diagnostics in 193 files: 520 arbitrary-value,
74 inline-style and 18 palette findings. The two merged inline findings are
removed; three unrelated arbitrary-value findings are added, for a net +1.
Fresh committed-lock installation, full lint, typecheck, formatting and machine
ESLint all pass. The [complete public audit](main-lint-audit-2026-10-24-084a410604.json)
is copied unchanged, SHA-256 `a928b8c551bd68d76e8d8cdbb0572f841a65c16aa3fa7c1c554f86b32dcfb5d0`.
The earlier 611-warning audit and all earlier audit objects remain unchanged.
Any later lifecycle tip must be recorded separately from the exact audit source.
No new proposal ID, readiness claim or film is added here.


## New draft ownership batches · 24 October

Backend panel height [#18902](https://github.com/OpenHands/OpenHands/pull/18902),
issue [#18900](https://github.com/OpenHands/OpenHands/issues/18900), is a draft at
`c183f4bc3cd3d024b8438e43a8de5be90503d3b9`. The positive measured height, observer,
nested `auto` fallback, height-only 300 ms transition and reduced-motion behavior
retain their owners. Local checks pass 31 focused tests, typecheck, formatting
and app/library CSS; target-file warnings fall 13 → 11 (one inline-style and one
arbitrary-value finding). Its [specific Notebook section](../../arch/agentic-linting-refactoring.html#backend-panel-height-film)
currently records pending evidence.

Files tree width [#18903](https://github.com/OpenHands/OpenHands/pull/18903),
issue [#18901](https://github.com/OpenHands/OpenHands/issues/18901), is a draft at
`ab650488ed6a9db47bdc14b9682458a2fdc1683f`. The real resize hook, 224 px default,
160–480 px bounds and storage/persistence remain unchanged. Local checks pass
51 tests across five suites, typecheck, formatting and app/library CSS and
JavaScript wiring; target-file warnings fall 3 → 2 (one inline-style finding).
Its [specific Notebook section](../../arch/agentic-linting-refactoring.html#files-tree-width-film)
currently records pending evidence.

Independent code review passes with low code risk and no material findings.
Overall approval remains pending authentic matched runtime evidence and required
current-head CI/PR gates. Both PRs remain **draft**, CI has started, and no bot
review is requested. No final media, runtime-version set, publication result or
final CI counts are claimed. The exact-main audit remains **612 warnings and
0 errors at `084a410604`**; independent draft reductions are not integrated.

The cohort is now **50 proposals: 46 merged, one open non-draft and three
drafts**. All 48 existing proposal objects, nine measured main audits, fourteen
earlier proposal audits, all 34 films and 68 MP4 download anchors, prior source
assets, the completed approval watch and existing prerequisites are preserved.
This addition creates two text-only feature anchors; no video tag or media path
is added. The final PR media updates must link each draft's own Notebook
feature/video anchor.


## Completed matching films · drafts retained

Both matching Before/After packets are frozen and root-approved. Backend panel
height has 12 named paired settled-height samples with zero observed geometry
difference; Files tree width has 13 named paired width samples with zero
observed difference. Source heads are Before `084a410604`/build
`bd00d766c4f403c3`, Backend After `c183f4bc3c`/`19aafc29ca5edbc4`, and Files
After `ab650488ed`/`bf128a3fcf7cd316`.

[Backend panel height](../../arch/agentic-linting-refactoring.html#backend-panel-height-film)
is 45.60 seconds (1,140 frames at 25 fps); its packet has 32 PNGs, four full raw
MP4s and 43 ZIP members. The 47 assets are published at immutable Notebook
`a877fcbbdcf4674ad4b36b01c138f234bb377f45`; five critical raw downloads return
HTTP 200 with matching SHA-256 values. Numeric measured ownership, normal
height-only transition and actual reduced-motion transition-property none are
verified. Initial/zero and nested-unmeasured fallback remain unit/CSS coverage.
The pre-existing white DigitalOcean heading on Light+ is retained in the full
raw packet, outside the central film's contrast claim.

[Files tree width](../../arch/agentic-linting-refactoring.html#files-tree-width-film)
is 59.92 seconds (1,498 frames at 25 fps); its packet has 28 PNGs, four full raw
MP4s and 39 ZIP members. Its 43 assets are published at immutable Notebook
`73d4225fa15ed071a5d06e8bf79a185d1f2bb0c2`; five critical raw downloads return
HTTP 200 with matching full SHA-256 values. Desktop widths 224/324/480/160, reload and restore keep
the actual calc.py preview selected. Phone 224/160, reload/restore and Back are
verified; 480 px phone fit is not claimed. One After phone capture miss and a
2.624-second screenshot delay are disclosed without inferring the missing
interval. The After phone excerpt includes the actual 224 px restoration.

Both films are 1440 × 1120, H.264 limited-range yuv420p/AAC with fast start,
captions, poster previews and very quiet original ambience. No new GIF is
provided. The range metadata repair for Files preserves all 1,498 decoded YUV
frames, AAC elementary bytes and the reviewed RGB gate frames; it changes no
UI content. All complete originals and source/coverage limits are downloadable.

Both PRs remain **draft**, with **no bot review requested**. The actual films and specific feature
anchors are attached while draft. Current code and media-description CI pass:
eight checks passed and six skipped each, none pending or failed. The honest
draft/media Notebook snapshot must be published and its live feature anchors
verified before readiness and initial bot requests. The cohort remains **50: 46 merged, one open non-draft, three drafts**.
All 34 earlier films and 68 download anchors are unchanged; two new sections
bring the page to **36 films and 72 MP4 download anchors**. The exact-main audit
remains 612 warnings and 0 errors at `084a410604`; draft reductions are separate.

Runtime: real Canvas 1.33.0, Agent Server/SDK 1.58.1, automation 1.25.1, Node
24.22.1/npm 11.12.1, identical real --mars-web configuration. No authentication
or model message was submitted, no agent started, and zero ActionEvents were
recorded. All three owned runs stopped, private state was purged, and all five
reused core ports closed. Earlier README text remains an unchanged byte prefix.


## Ready for review · 24 October

The published draft/media snapshot `689a013069ff681b04810839cb67e6d33c29c251`
passed all 15 live Pages HTTP/hash/MIME checks, including both specific film
anchors. #18902 and #18903 are now ready and open at their unchanged recorded
heads, with eight checks passed and six skipped each. Initial all-hands-bot
review requests are verified pending; no approval or merge is claimed.
The cohort is **50: 46 merged, three open non-draft and one draft**. All
**36 films and 72 MP4 download anchors**, media/source bytes, prior history
and the exact-main 612-warning audit remain unchanged.


## Next wave baseline · merged ownership batches

Backend panel height #18902 merged at `2026-10-24T08:23:56Z` as
`7b452520613fdf71771fc10285ed0df1ceef8697`; Files tree width #18903 merged at
`2026-10-24T09:13:15Z` as `fee10e3d2909ebbf9950578575b1ee011492171e`. Exact
bot approvals and merge lifecycle are retained in `progress.json`. The films
keep their original `c183f4bc3c` and `ab650488ed` capture heads.

The cohort is **50: 48 merged, one open non-draft, one draft**. All 36 video
elements, 72 MP4 download anchors, prior proposal/audit objects, recording
identities, media/source bytes, related prerequisites and completed approval
watch are preserved. Earlier README content remains an unchanged byte prefix.

Fresh exact main **`fee10e3d29` passes with 0 errors and 609 warnings** across
1,425 linted files (193 with diagnostics): 519 arbitrary-value, 72 inline-style
and 18 palette findings. The [full public audit](main-lint-audit-2026-10-24-fee10e3d29.json)
records exactly three removed findings and none added from `084a410604`.
SHA-256: `a242caaa2b9ac66d64dd81ba15cd3ad059fa3ffab9e6f89b142f6937495687dc`. Full lint, machine
ESLint, typecheck and formatting pass. The existing exact-lock installation was
reused after identity checks; no install, resolver, network or stack was run.
All nine earlier main and sixteen proposal audits remain unchanged.

Sidebar stacking and desktop overview-drawer width are the next separate
candidate scopes; no new PR IDs, frozen films or live claims are recorded.
Each actual matching film section must be published and its own Notebook
anchor verified live before readiness and the initial bot review request.


## New Sidebar and Overview drafts

Sidebar stacking [#18908](https://github.com/OpenHands/OpenHands/pull/18908),
issue #18906, is a draft at `6654969d173f8df8f17ce3221715e48124f42ab1`.
Two z-[1] spellings become z-1, with the same literal scoped z-index:1 in actual
app/library CSS. All 26 existing tests and type/format checks pass; target
arbitrary-value findings fall 4→2. Its [specific section](../../arch/agentic-linting-refactoring.html#sidebar-stacking-film)
contains pending evidence text only.

Overview drawer sizing [#18909](https://github.com/OpenHands/OpenHands/pull/18909),
issue #18907, is a draft at `a3ddc1b35f39268bc34e4d1ca221e6de93d17a73`.
The unchanged width hook supplies numeric px values to static width/transition
readers. All 24 tests across three files and type/format/app/library checks
pass; two baseline contract tests failed before the change. Independent full
branch lint is 605 warnings/0 errors, removing three inline-style and one
arbitrary-value finding. Static emitted-CSS contracts cover host font 32px and
spacing 3rem; this is not a live Canvas host-override claim.

A genuine baseline 12×0px native grip remains at 420px after drag and a healthy
doctor/retry. [Separate issue #18910](https://github.com/OpenHands/OpenHands/issues/18910)
records this pre-existing hit-area defect; public capture proof is pending.
Real drag, clamps and persistence after drag are blocked. Unit and actual
compiled-CSS contracts cover the hook/transition path. Independent review
found no CSS-refactor regression and no hit-area-fix prerequisite. Existing
phone issue #16792 remains separate; the mobile branch is unchanged. The
[Overview feature section](../../arch/agentic-linting-refactoring.html#overview-drawer-film)
contains pending evidence text only.

Independent code review passes with low risk and no material findings. Both
PRs remain **draft**, with CI started, matching After/final media pending and
**no bot review requested**. No final CI counts, frozen packet or matched live
pass is claimed. The cohort is **52: 48 merged, one open non-draft, three drafts**.
All 50 earlier proposal objects, ten main audits, sixteen prior proposal audits,
36 films and 72 MP4 anchors, media/source bytes and earlier history are retained.
Independent branch reductions are not integrated: exact `fee10e3d29` remains
**609 warnings and 0 errors**. Each actual film section must be published and
its own live anchor verified before readiness and the initial bot request.


## Frozen media/draft checkpoint · publication pending

Both independent source/asset gates pass. The 93 packet assets and exact-main
audit are prepared in local asset commit `aa301cf0f30bdc3e992454ae244989d78538e59d`.
Nothing is published or publicly HTTP-verified at this checkpoint. Both PRs
remain **draft**, with **no bot request**. Last actual CI is **seven passed, one
media-description failure, six skipped each**; final attachment/validation is
pending. Root will publish assets and this draft snapshot together, verify raw
downloads and each own live film anchor, then attach published media and pass
description CI before readiness and initial bot review.

The [Sidebar film](../../arch/agentic-linting-refactoring.html#sidebar-stacking-film)
is 24.76 seconds, 619 frames at 25 fps; 50 assets include 34 PNGs/four raw MP4s
(38 selected originals) and 46 ZIP members. Exact source/build identities are
`fee10e3d29`/`0d613af38d4884d7` and `6654969d17`/`6687c3c31260b0e6`. Its one
paired computed sample has zero stable-field differences. Glyph/background/dot
stacking is preserved; phone evidence is unchanged expanded-path smoke.
One Before desktop capture miss and source timing limits remain disclosed.
Film SHA-256: `da0e447bce16e33506455f4822c0ca6dc2af8edaefdbd31184f0424c9421d4e6`.

The [Overview film](../../arch/agentic-linting-refactoring.html#overview-drawer-film)
is 20.84 seconds, 521 frames at 25 fps; 43 assets include 26 PNGs/four raw MP4s
(30 originals: 16 Before/14 After) and 39 ZIP members. Its proof-pointer correction
and dependent metadata/ZIP hashes passed the refreshed independent gate.
Final ZIP SHA-256: `b5f5224c1ac1167483caaf7d9ac000571a88d3400ae6b3bb6224c172acc2f113`.
Film SHA-256: `d054345e1da07acc8178ca5172c5166a8af30a50e62044bfb4d14dd7d7ab4886`.
Source/build identities are `fee10e3d29`/`0d613af38d4884d7` and
`a3ddc1b35f`/`c67b70a90d8ab8ee`. Nine paired computed samples have zero stable
field/width differences at actual 420 px open/close/reopen/reload/Escape; outer 0 px
and inner 420 px remain when closed. Native resize remains blocked by the
unchanged 12×0 px grip, #18910. Other widths, clamps, isDragging and after-drag
persistence have unit/build coverage only. Phone entry remains blocked by
#16792; no live phone-path pass is claimed. Sanitized proof JSON and actual
Before/After bug screenshots are included in the packet.

Both films have 1440×1120 H.264 limited-range yuv420p/AAC, fast start, poster and
captions; no new GIF. The page is **38 films/76 MP4 anchors**, preserving all 36
earlier video elements/72 download anchors. The cohort is **52: 48 merged, one
open non-draft, three drafts**. Exact-main remains 609 warnings/0 errors at
`fee10e3d29`; independent branch reductions are separate. All three owned runs
are stopped/private-purged, and all five reused core ports are independently
confirmed closed. Full source/operational limits and earlier README history
remain preserved.


## Ready checkpoint · live film anchors verified

Asset commit `aa301cf0f30bdc3e992454ae244989d78538e59d` and media snapshot
`ef5d54c22340ddf6d73921f1c54470257bbd4c33` are published. All 10 critical raw
downloads passed HTTP 200/full SHA; all 15 live Pages files passed HTTP/full
SHA/MIME, including both own film anchors. #18908 and #18909 are ready/open at
unchanged heads, with **eight passed checks/six skipped each**. Initial
all-hands-bot requests are verified pending; no approval or merge is claimed.
The cohort is **52: 48 merged, three open non-draft, one draft**. All 36 earlier
films/72 downloads are retained, with **38 films/76 MP4 anchors total**.
Source/capture heads, all media bytes and audit history remain unchanged.
Independent readiness closure passes. Separate resize issue #18910 has exact
published baseline PNG/geometry proof and is ready-for-dev; native resize and
phone #16792 limits remain unchanged.


## Oct 25 coherent domain draft checkpoint

Sidebar #18908 merged at `2026-10-24T22:32:15Z` as
`51f634fd980b618e348a0fae4ebcee62d5fa52a5`; Overview #18909 merged at
`2026-10-24T22:36:17Z` as `1abbd4b41544dd8a74b19ff3359029537bbaa41b`.
Their original capture heads and films remain unchanged. Current metadata
confirms older #18520 is open/non-draft at
`aef5a5591ded4ebb01d08a05ef3925884581f2e5`; its evidence, prerequisites and
user text are retained. #18533 remains open/non-draft unchanged.

Exact-main `1abbd4b415` passes with **603 warnings, 0 errors**: 516 arbitrary,
69 inline and 18 palette findings. Six findings were removed and none added
versus fee10e3d29. All earlier audit objects remain unchanged; the new public
audit is `main-lint-audit-2026-10-25-1abbd4b415.json`.

Automation aliases #18917 at `e69074d21b86d1aaaa9887fb3dde366d2659add2`
removes 77 branch findings (target 115→38); full branch lint 526/0, 67 tests and
14/14 actual app/library emitted CSS pairs pass. Dropdown controls #18918 at
`92cc0b57fab00cebed9f065999f1255e27bc5255` removes 18 target inline findings;
97 tests pass with six existing todo cases. Compiled sr-only retains real
controls and equivalent hidden geometry, with clip-path rather than literal
old clip identity. Matching live evidence and frozen packets are pending.

Both new PRs remain **draft**; no final green/readiness/bot request is claimed.
The cohort is **54: 50 merged, two open non-draft, two drafts**. All 38 existing
films/76 downloads and their source identities are retained. No new video,
media filename or public/live claim is added. Coherent domain batches have
no arbitrary PR size/count limit. Each own film anchor must be published and
verified live before readiness and the initial bot review. Portal coordinates
remain deferred because distinct owners/body-portal scope require separate
review. Earlier README text remains an unchanged byte prefix.


## Frozen Oct25 media · drafts retained

Both matching packets are complete/frozen, visually approved and copied locally.
Automation is 27.64 seconds/691 frames, 47 assets, 32 PNGs/two raw MP4s and 43 ZIP
members. Dropdown is 24.64 seconds/616 frames, 24 assets, 10 PNGs/two raw MP4s
and 20 ZIP members. Both are 1440×1120 at 25 fps, H.264 yuv420p/AAC with fast start,
posters, VTT and quiet original ambience (mean −52.5 dBFS); no new GIF. All 46
selected originals retain their exact bytes; owned three runs are stopped,
private state purged and independent port checks confirm closure.

[Automation film](../../arch/agentic-linting-refactoring.html#automation-theme-aliases-film):
11 authority observations, but 10 strict screenshot-associated comparisons,
zero stable color/DOM differences; two Solarized relative saved-age-label
widths differ. Nine of 14 class recipes are live, five compiler-only. Visible
phone form limits are retained; no full settled Entrypoint/model/provider or
edit-agent proof. Film SHA-256:
`7a31a63b3184b3945820bde65a0f3e73bf6ea9c3a29f7d4f64b59190c833d853`.

[Dropdown film](../../arch/agentic-linting-refactoring.html#dropdown-hidden-controls-film):
two matched desktop stable samples and intentional sampled clip rect→auto plus
compiled clip-path:inset(50%). Baseline live clipPath was not sampled; literal
CSS identity is not claimed. Phone is unchanged visible-trigger smoke only;
the hidden desktop duplicate query is excluded from phone geometry. Film SHA:
`7f97f508161b717e5c653fa083ae31989918c720ab61f7fce9499b1f9eb80ad3`.

Both PRs remain **draft**, with no initial bot request. Root-reported current CI
is 18917: 7 passed/1 media-description failure/6 skipped; 18918: 6 passed/1 pending/
1 media-description failure/6 skipped. Asset commit/public HTTP/live own-anchor
and final current CI gates remain pending; no green/ready/publication claim.
The cohort stays **54: 50 merged, 2 open non-draft, 2 drafts**. All 38 earlier films
and 76 MP4 anchors are preserved; totals become **40 films/80 MP4 anchors**.
Exact-main remains 603/0; independent branch reductions stay separate.


## Local asset commit checkpoint

Independent frozen-asset gate PASS is bound to local commit
`ef22c28aa21e9fb5796773c78d358ac3a00b553a` (72 new packet/audit files). It is
not published yet; public HTTP and own live film-anchor checks remain pending.
Current CI for **both** drafts is seven passed checks, one expected
media-description failure, six skipped and zero pending code checks. The older
checkpoint above is retained as history. Both PRs remain draft/NoBot until
actual publication, current description and live-anchor receipts are supplied.
All 40 film elements/80 MP4 anchors and source/media identities are unchanged.


## Final READY checkpoint · verification pinned to media snapshot C

Asset B `ef22c28aa21e9fb5796773c78d358ac3a00b553a` and media docs C
`a914cb127d13cf720e4d483ec481212876532d53` are published. All 11 critical raw
files pass HTTP 200/full SHA; all 15 live Pages files pass HTTP/full SHA and
expected MIME, including both own film anchors. Existing designated Chrome
shows readable After playback at 0:17/0:27 for automation and 0:18/0:24 for
dropdown, with visible Slack links. Files were verified by HTTP, not browser
download clicks. These checks apply to C; root verifies final READY docs D
after its later publication.

Both #18917/#18918 are **ready/open at unchanged heads**, with effective CI
**8 passed/6 skipped/0 pending/0 failed**, including fresh ready-event
description validation. Initial all-hands-bot requests were verified pending
after green; no prior review, approval or merge is claimed. HUMAN prefixes were
byte-preserved. The cohort is **54: 50 merged/4 open non-draft/0 draft**.
All 40 film elements/80 MP4 anchors, corrected source/media bytes and stated
coverage limits remain unchanged. Exact-main stays 603/0; independent 77+18
proposal reductions remain separate. The user chooses merging; no merge,
release or watch is performed here.


## 25 October continuation · draft evidence checkpoint

Prior #18917 merged at `2026-10-25T02:20:45Z` as
`74323b544c151669b3cdd88fb950942a29beda55`; #18918 merged at
`2026-10-25T02:21:19Z` as `b185939d3dec3b203b0651c675f175ee5b4ed43e`.
These are 03:20 and 03:21 Stockholm after the DST change; original capture heads
and all 40 whole film elements/80 MP4 anchors remain unchanged.

Exact main `c5612599307c0bc44e21ed25c97e2a542e194b32` now has **508 warnings/0 errors**:
439 arbitrary values, 51 inline styles and 18 palette findings. The
[public audit](main-lint-audit-2026-10-25-c561259930.json) records exactly 95 removed and none
added versus 1abbd4b415; SHA-256 `26aac3a5821323c5277f2f7789863827b6f3ab992b604e0ce856b4d74a822279`.
Full lint, machine ESLint, typecheck and formatting pass using the committed
lock and existing verified install; no dependency resolution/install ran.

New **draft** [#18933](https://github.com/OpenHands/OpenHands/pull/18933) uses
17 existing profile theme aliases across six files at `2c4e9e6bd9533d84245f92a66ab732a2a35b255b`.
All 90 tests, app/library builds and five emitted full-class pairs pass;
independent branch lint is491/0. Known Solarized keyless-note contrast #18546
(2.58:1) and the public embedded AddModels body-portal gap remain inherited.
New **draft** [#18934](https://github.com/OpenHands/OpenHands/pull/18934) gives
twelve preview bindings two compiled owners at `e0eee4cc154875c759d6f346495afce69118a79e`.
All 34 existing tests/full lint/builds pass, independent branch lint496/0;
independent actual twelve-property cascade proof is still ongoing.
These branch reductions remain separate from integrated main508/0.
Matching evidence and current source CI are in progress; no frozen new movie,
public HTTP, readiness or initial bot request is claimed. Own film anchors
`profile-theme-aliases-film` and `file-preview-theme-film` must be published
and verified before readiness and initial review. No arbitrary batch size/count cap.

The cohort is **56: 52 merged/2 open non-draft/2 draft**. Current read-only
#18520 evidence confirms open/non-draft, CLEAN/MERGEABLE, bot-approved at
unchanged `aef5a5591d`, CI8 passed/6 skipped and no review requests. Its latest
bot approval accepts candid fixture-backed appearance evidence: a real-account
empty state plus forty focus measurements across five themes/two viewports.
The earlier static-only record and original source identities remain history.
Fixture proof does not establish DigitalOcean authentication, billing or
resource lifecycle; issue18517 still requests authenticated affected states
and is not ready-for-dev. No duplicate DO source work is needed.
SDK5603 and budget18533 are explicitly **parked by the user**; their records,
prerequisites and user text remain unchanged, with no new SDK status work.


## 25 October continuation · frozen MEDIA/DRAFT checkpoint

The [profile theme film](../../arch/agentic-linting-refactoring.html#profile-theme-aliases-film)
and [Markdown preview film](../../arch/agentic-linting-refactoring.html#file-preview-theme-film)
are complete locally. Both native players have posters/captions, visible Slack
downloads, complete-original ZIPs and relative source/comparison links. All forty
earlier whole players/eighty MP4 anchors retain their bytes; totals are
**42 films/84 MP4 downloads**. No new GIF.

Local-only asset B `11dd5ab4dd01504b1f0fd881377d9551539ff6c1` contains
123 packet assets plus the exact-main audit. It is not yet published. Frozen
profile packet: 48.64 seconds, 59 PNGs/four native clips, 72 ZIP members; film
SHA `a2808a9dec0c43e0238fa9947214b7952f81026e978a277281d7b4092aeed277`.
Frozen Files packet: 38.4 seconds, 32 PNGs/two native clips, 43 ZIP members; film
SHA `a431e990bf5c7946adfb0e9760696991f67b6e20c354df617c8cb2a8eda971d1`.
Both are H.264/yuv420p/AAC, 25 fps with fast start, and quiet original ambience
averaging −52.5 dB. Independent code/live/frozen-asset gates and root visual
review pass; no public HTTP or live-anchor verification is claimed yet.

Source/builds are c561259930/dfd39a7c2f6aec0a before, profile
2c4e9e6bd9/b38c7801a740f06a and Files e0eee4cc15/b5f49973c55d0d72 after.
All 23 profile computed states and eleven desktop Files states match. Five
themes and representative 390 px phone originals are included. Files phone
uses native Hide file tree on both revisions; three matching Before stills
come from a supplemental same-baseline/build run. Phone Rich/table visual
smoke lacks paired baseline hidden-tree computed measurements. Host overrides,
embedded hosts and absent sanitized caption/kbd/lead descendants retain
compiled-contract coverage; Files actual twelve-property proof passes across
32 scenarios. Genuine filesystem reads use the existing adapter, with zero
agent prompts/model calls/turns. Solarized keyless-note issue #18546 (2.58:1),
Cloud/older-backend/bound-provider and embedded AddModels limits remain. Four
existing profile warnings remain outside the color-only batch; no claim that
all four lack aliases. No pixel identity, contrast or phone-layout fix claimed.

Both #18933/#18934 remain **draft/NoBot**. Actual 11:05 UTC source-CI receipt
records **7 passed/1 media-description failure/6 skipped/0 pending** each.
Root publishes B plus media docs C, verifies immutable raw and own live film
anchors, attaches media and closes required checks before readiness/initial
bot review. Cohort remains **56: 52 merged/2 open non-draft/2 drafts**.
Main remains **508/0**; independent17+12 branch reductions and branch491/496
counts are separate. All 97 originals and old source identities are retained;
owned runs are stopped/private-purged and core ports independently closed.
SDK5603 and budget18533 remain user-parked, with their records unchanged.


## 25 October continuation · READY, initial bot reviews pending

Asset B `11dd5ab4dd01504b1f0fd881377d9551539ff6c1` and media docs C
`6a55643db7a6fcdf29fedc962c0f945fd52c00a2` are published. Eleven immutable
raw files pass HTTP/full SHA; fifteen live Pages files pass HTTP/full SHA and
expected MIME, including both own film anchors. Existing designated Chrome
shows readable native profile Before at 0:18/0:48 and After at 0:25/0:48, plus
Files After at 0:28/0:38, with visible Slack download links. Downloads were
verified by HTTP/full SHA; no browser download click is claimed. These checks
apply to media snapshot C, not the later READY-docs D deployment.

Both #18933/#18934 are **ready/open at unchanged exact heads**, with fresh
ready-event description validation successful and effective required CI
**8 passed/6 skipped/0 failed/0 pending**. Initial all-hands-bot requests were
verified pending after green; reviews are empty. HUMAN prefixes were byte
preserved. Independent final readiness is PASS; no bot approval or merge is
claimed. Cohort: **56: 52 merged/4 open non-draft/0 drafts**. All 42 complete
players/84 MP4 anchors, source/capture identities and coverage limits are
unchanged. Main stays 508/0; branch 491/496 and independent 17+12 remain separate.
SDK #5603/budget #18533 remain user-parked with their old records unchanged. The
user chooses merging; no merges, releases or watch actions are performed here.


## 25 October evening continuation · draft checkpoint

[#18933](https://github.com/OpenHands/OpenHands/pull/18933) merged
`2026-10-25T19:53:58Z` as `ddbcd525d0f3259ffddf1ea5fff366ecdc4a171a`;
[#18934](https://github.com/OpenHands/OpenHands/pull/18934) merged
`2026-10-25T20:57:16Z` as `044ec59e12e5070406378ba24d568cfbb3a10bf0`.
These are 20:53 and 21:57 Stockholm (ZoneInfo, UTC+1 after DST). Original
capture heads 2c4e9e6bd9/e0eee4cc15 and all 42 whole players/84 MP4 download
anchors retain their bytes. There are 88 total MP4 href anchors; download
counts require the download attribute.

Exact main `044ec59e12e5070406378ba24d568cfbb3a10bf0` passes **479 warnings/0 errors**:
410 arbitrary values, 51 inline styles and 18 palette findings, 1,425 files
linted/186 with diagnostics. The [public audit](main-lint-audit-2026-10-25-044ec59e12.json)
records exactly 29 removed/0 added versus c561259930 (settings 17/Files 12);
SHA-256 `65295d88364b60da49c5e8f2f7ae26bc79f7ed375b702a420a92c75f2d7af1a6`.
Full lint, machine ESLint, typecheck and formatting pass; independent draft
branch counts are not combined into this integrated-main total.

Three new **drafts** have independent code/CSS PASS/LOW, with final live
evidence, media and final-head CI still pending:

- [Home #18946](https://github.com/OpenHands/OpenHands/pull/18946), issue #18943,
  final `0cc2b720c16a1c498ed6ca387b66045a69470833` / product `988aab3510`: six
  aliases/findings removed, branch 473/0. Original 25-test Home and targeted
  37-test Home/theme runs overlap; do not add them. One new actual consumer
  CSS case covers five themes; isolated-runtime notice/static test-mode pill
  remain compiler/test-only pending genuine live proof.
- [Automation #18947](https://github.com/OpenHands/OpenHands/pull/18947), issue #18944,
  `4506f4ff98958f68283e7121f1763367f96a8ab1`: four substitutions remove only
  two diagnosed warnings, branch 477/0; seven suites/40 tests. Draft map recipes
  are outside the current class-site scanner; genuine DRAFT differs from
  paused/inactive. Matching script/status evidence remains pending.
- [Extensions #18948](https://github.com/OpenHands/OpenHands/pull/18948), issue #18945,
  final `510f00ebc3c7b236e76e6ace4b541f62e8cb71b2` / product `50b5f7e6a8`: six
  frames/twelve classes/findings, branch 467/0. Seven suites/101 tests plus two
  additional build/viewport suites/16 tests pass. The scoped 90vw/85vh library
  build contract retains the preexisting embedded body-portal limitation.

Final Home/Extensions commits are test-only and preserve reviewed product
bytes. Initial CI snapshots are superseded; final required checks/media
description outcomes remain pending. No frozen new film paths, public HTTP,
readiness or initial bot request is claimed. Future own anchors are
`home-launcher-theme-film`, `automation-detail-theme-film` and
`extension-dialog-viewport-film`; matching films must be published/live-verified
before readiness and initial review. Coherent batches have no arbitrary
count/size cap. Cohort: **59 = 54 merged/2 open non-draft/3 drafts**.
Read-only reconciliation confirms #18520/#18533 remain open/non-draft at their
unchanged heads (approved/review-required respectively). Their old objects
and user text remain unchanged. SDK #5603/budget #18533 stay explicitly parked;
no new SDK work, source/media edits, merges, release or watch is performed.


## 25 October evening continuation · frozen MEDIA/DRAFT checkpoint

Three own film sections are complete locally: [Home](../../arch/agentic-linting-refactoring.html#home-launcher-theme-film),
[Automation detail](../../arch/agentic-linting-refactoring.html#automation-detail-theme-film), and
[Extension dialogs](../../arch/agentic-linting-refactoring.html#extension-dialog-viewport-film).
They use native same-origin controls, posters/captions, visible Slack downloads
and complete-original ZIP/source/comparison links. All 42 older whole players
and 84 download anchors retain their bytes; totals are **45 films/90 MP4
download anchors** (94 total MP4 href anchors). No new GIF.

Local-only asset B `bec344f8284745a92ce0c10c9a4e4a1a2779926a` contains 252 packet assets
plus the main audit; it is not yet published. Independent frozen-asset gate
passes 69 checks and root decoded visual review passes. Final movies:

- Home 43.24 seconds, 80 PNGs/four native clips, 94 ZIP members; film SHA
  `1b3b3f64f1bcb71f820cd68fd54b63dff1ea18e848e8db781f8f3d7590f599c6`.
- Automation 31.88 seconds, 42 PNGs/six clips, 57 ZIP members; film SHA
  `04c48deff3f6d74c25909c2491ab2bb552b5b5e336467446d71f328ba485731c`.
- Extensions 77.88 seconds, 76 PNGs/four clips, 89 ZIP members; film SHA
  `25fba58c5f22d8269f747754c507eaa7c0e6b4d47e6cb6c4627a96c1445c6745`.

All are 25 fps H.264/yuv420p/AAC, fast-start, with original quiet ambience
averaging −52.5 dB. The 212 selected originals are retained; all six owned runs
are stopped/private-purged and all owned ports are conclusively closed.
No model prompt, completion or agent turn was run.

Home has 40 corrected matched mounted-branch samples across five themes, both
Code/Automate modes, desktop/phone and normal/reduced motion, settled 750 ms.
Earlier preference-only captures are excluded. Clock activation is one 700 ms
animation, not continuous rotation. Isolated-runtime notice remains compiler/
mocked-test-only. Automation has 20 matched genuine detail Draft/script states;
compact Draft cards/rows remain compiler-only. One fixed credential-free printf
Test per phase exited 0 in Bash; service remained RUNNING/Starting without its
callback. Exact runs were cancelled and owned objects deleted; no completed
Test lifecycle, expand/copy controls or enabled schedule is claimed. Extensions
has 38 matched samples across six real frames, desktop/phone/short-phone, with
five-theme stills on one representative dialog. Long API-discovered content
exercises real scrolling/footer owners; nothing was installed or executed.
Inherited embedded body-portal scope remains; no live embedded/Cloud/ACP
coverage, global pixel identity, layout or performance improvement is claimed.

Actual build/cache identities are distinct from final checkout heads: Before
044ec59e12/build 8e365d1fa30953c3; Home checkout 0cc2b720c1/build cdf6895f5874b3f2
reuses actual app/library source 988aab3510 by exact input equality. Automation
4506f4ff98/build d75a8350ef7e384f is built from that source. Extensions checkout/
app source 510f00ebc3/build 086cdbb325a81428 retains library source 50b5f7e6a8.
No older bytes are relabelled as newly built source.

Cohort remains **59: 54 merged/2 open non-draft/3 drafts**. All three new PRs
remain **draft/NoBot**, with actual code CI 7 passed/1 expected media-description
failure/6 skipped/0 pending. Raw HTTP, own live anchors, publication and final
readiness gates await root B+C publication and media attachment. Exact-main
stays 479/0; independent 473/477/467 branches and 6/2/12 reductions stay separate.
SDK #5603/budget #18533 remain user-parked and unchanged.


## 25 October evening continuation · READY, initial bot reviews pending

Asset B `bec344f8284745a92ce0c10c9a4e4a1a2779926a` and media docs C
`355eafa23e4a722d7b913c800dbfec6a7c265420` are published. Sixteen immutable raw files
and twenty live Pages files pass HTTP/full SHA and expected MIME, including
all three own film anchors. Designated Chrome verifies readable native
playback and visible Slack download links. Downloads were verified by HTTP
and full body SHA; no browser download click is claimed. Proof belongs to
media C, not the later READY-docs D deployment.

All three #18946/#18947/#18948 are **ready/open at unchanged heads**. Fresh
ready-event description validation succeeds; required CI is **8 passed /
6 skipped / 0 failed / 0 pending** each. Initial all-hands-bot requests are
verified pending after green, with empty reviews and preserved HUMAN prefixes.
Independent final readiness passes; no bot approval or merge is claimed.
Cohort: **59 = 54 merged / 5 open non-draft / 0 drafts**. All 45 whole players
and 90 MP4 download anchors, source/build/cache identities, originals and
coverage limits remain unchanged. Main stays 479/0; branches 473/477/467 and
reductions 6/2/12 remain separate. SDK #5603/budget #18533 remain user-parked
with their records unchanged. The user chooses merging; no merge, release
or watch action is performed here.


## 26 October continuation · one combined setup draft

Prior #18946/#18947/#18948 merged at 23:02:08/23:02:30/23:03:22 UTC on
25 October: Stockholm 26 October 00:02/00:02/00:03. Merge commits are
`9b43513590b6e3eaa90b0c363f7b75a9c2360fcd`,
`f5f3e412d44e7ba90e535c5e345c5a176f1eaa3a`, and
`7a41641c6d8bcf3e2e3c19c08b778781bcf954c2`. Original capture/build/cache
identities remain unchanged, as do all 45 complete players/90 MP4 download
anchors/94 total MP4 href anchors.

Exact main `7a41641c6d8bcf3e2e3c19c08b778781bcf954c2` passes **459 warnings/0 errors**:
390 arbitrary values, 51 inline styles, 18 palette findings; 1,425 linted files/
179 diagnostic files. [Public audit](main-lint-audit-2026-10-26-7a41641c6d.json)
SHA-256 `c57a3d0d1d4f5b2484df483f0c91d0b752ee4219517763c83f03985989e47afe` records 20 removed/0 added
versus 044ec59e12. Full lint/typecheck/format and machine ESLint pass. Active
Node 24.22.1/npm 11.12.1 differ from the repository Volta Node pin recorded
separately in that audit; no matching-pin claim.

One meaningful [combined Automation setup PR #18950](https://github.com/OpenHands/OpenHands/pull/18950),
issue #18949, groups 42 findings: panel 17, prompt stack 17, new route 4 and
ConversationMain dock 4. Final head `eef335c07dcb4f013c7722e107c49d720bb507d5`
preserves product `ceb04025621644dc9d672af4d9b4c1796d029fc7`; branch 417/0
removes 42 findings/0 added, independently of main 459/0. Typography/palette, APIs, state
and dynamic layout logic remain untouched. 94 focused tests across six suites
and 15 Vite/scope tests across two files overlap; do not claim 109 disjoint
tests. Permanent actual library output covers 14 recipe roles/four width refs.
An erased PostCSS annotation fix reproduced then resolved the full typecheck
error; generated test JavaScript and all product files remain byte-identical.
Independent source/CSS/acceptance/type-fix reviews pass.

Captured After checkout/app source is `7569edff89e328d1bdfd0cbda6edd8df327c0bcb`,
actual library source is `ceb04025621644dc9d672af4d9b4c1796d029fc7`; never
relabel these pixels as final PR head eef335c07d. Private evidence has 42 named
states, 84 PNGs/six native clips and 16,276 matching sampled computed properties.
No-message/autotitle-off/tools-empty idle fixtures have zero model turns/events;
inactive bundles have zero runs/dispatches. Owned runs are stopped/private-
purged with actual errno 61 port-closure checks. Root Before review passes;
final After/film/source packaging and public media gates remain pending. The
unrelated Getting started counter differs with fixture order, outside the
selected setup comparisons; no whole-page pixel/synchronized-video identity.

#18950 remains **draft/NoBot**: actual CI 6 passed/1 pending Ubuntu/1 expected
media-description failure/6 skipped. Cohort: **60 = 57 merged/2 old open
non-draft/1 draft**. No new movie path, asset B, public HTTP verification,
readiness or bot success is claimed. Own anchor `automation-setup-layout-film`
is reserved; the matching film must be published/live-verified before readiness
and initial bot review. User preference is one coherent combined owner batch,
rather than tiny PRs. SDK #5603/budget #18533 and all older user records,
history/audits/watch remain unchanged. No Git/source/assets/external actions.


## 26 October · frozen MEDIA/DRAFT checkpoint

The [combined Automation setup film](../../arch/agentic-linting-refactoring.html#automation-setup-layout-film)
is complete locally: 82 seconds, 84 PNGs/six full native clips, 105 ZIP members,
109 packet assets plus the audit. Local-only asset B
`025d108708a9f26698afe3dee6330313ff09fdab` is not yet published. Independent frozen-asset
review passes 28 checks; root Before/After source and decoded-film review pass.
Film SHA `65785af3bf6430053e20bd185202fd18304da0b6f28a0ddd5ba57a5eafea6bb2`;
ZIP SHA `ea40b853661ee3b18502af1a8fd6000950404ca990bb5cc200fe5398662d8475`.
Native same-origin playback/poster/captions and Slack download are accompanied
by immutable B MP4/ZIP/source/comparison/compiled-contract/source-binding links.
No public availability or HTTP success is claimed. All 45 previous players/
90 download anchors/94 MP4 href anchors retain their bytes; totals become
**46 players/92 download anchors/96 MP4 href anchors**. No GIF.

Captured/app After remains 7569edff89, library source ceb0402562 and final PR
head eef335c07d; exact source equality and erased test syntax never relabel the
original pixels. All 42 named states/16,276 sampled computed properties match.
The sidebar Getting started counter 2→3 reflects fixture order, outside selected
roles. Benign QA labels/UUIDs, relative clocks and existing narrow overflow
remain. Standalone Local Neutral/Light+ is live evidence; embedded scope is
compiled proof. No model/provider turn, Automation run/dispatch, appearance
improvement or whole-page/synchronized-video identity claim. The inactive
bundle and zero-message/events idle conversation remain execution-free.
Local Node 24.22.1 differs from repository Volta Node 24.21.0; npm 11.12.1 is
repository-pinned. Original ambience averages −52.5 dB, with 25 fps H.264/AAC,
fast start and unaltered selected-original bytes/timing. Owned runs/fixtures
are stopped/deleted and private state purged, with actual errno 61 port checks.

#18950 remains **draft/NoBot**. Actual current final-head CI is **7 passed/
1 expected missing-media-description failure/6 skipped/0 pending**, with Ubuntu
and Windows green. Cohort remains **60 = 57 merged/2 old open non-draft/1 draft**.
Root publishes B+C, verifies raw/live own anchors and attaches media before
final required green CI, readiness and initial bot review. Main 459/0 and
independent branch 417/0 remain separate. SDK #5603/budget #18533, older user
records, audit/history/watch and source identities remain unchanged.


## 26 October · READY, initial bot review pending

Asset B `025d108708a9f26698afe3dee6330313ff09fdab` and media docs C
`7ebad1d4289e78810fc3abc6eebb95e0b2453607` are published. Six immutable raw files
and ten live Pages files pass HTTP/full body SHA; live MP4 is video/mp4.
The own film anchor is verified. Existing designated Chrome shows native
Before playback at 0:29, After at 0:48, paused at 0:52/1:22, with the visible
same-origin Slack download link. No browser download/save was clicked or
claimed. These checks belong to media C, not future READY docs D deployment.

#18950 is **ready/open at unchanged eef335c07d**, with actual final ready-event
CI **8 passed / 6 skipped / 0 pending / 0 failed**. Fresh description job
[121334708278](https://github.com/OpenHands/OpenHands/actions/runs/40248376873/job/121334708278) succeeds.
Initial all-hands-bot review was requested and verified pending after green;
reviews were empty, HUMAN prefix preserved, no prior approval/re-review claim.
Independent final closure is PASS/readyAllowed; no merge is authorized here.
Cohort: **60 = 57 merged / 3 open non-draft / 0 drafts**. All 46 complete
players, 92 download anchors and 96 MP4 href anchors, exact originals and
source/build/cache/runtime limits remain unchanged. Captured/app 7569 and
library ceb remain distinct from final eef; main 459 and branch 417 remain
separate. SDK #5603/budget #18533 and older user/audit/history/watch records
are unchanged. The user chooses merging; no merge, release or watch action.
