# enyst.github.io

Architecture-page maintenance follow-ups: [`OPENHANDS_DOC_STATUS.md`](OPENHANDS_DOC_STATUS.md).

The [Agentic linting refactoring page](arch/agentic-linting-refactoring.html)
tracks the staged Canvas lint rollout and its next steps. Its Before/After
video, direct MP4 download, captions, and provenance are stored in
`experiments/agentic-linting-refactoring/`. Rule scopes and PR statuses are
a dated snapshot; update the source revision and `progress.json` together
with the page when refreshing them.

The [OpenHands feature map](openhands-features/index.html) is a static snapshot
of the maintained upstream recipes. Regenerate it from a clean, selected
OpenHands revision with `python scripts/build-openhands-features.py --checkout ../playground`.
The generator preserves every behavior ID and checks literal command fidelity.
Reviewed CLI screenshots and their provenance live in `assets/openhands-features/`;
the `capture-*.json` manifests attach media beneath the corresponding recipes.
New captures must match the selected source revision. The delimited OpenHands
features section in [`verify/index.html`](verify/index.html), the verification
table of contents, is generated; the rest of that page is retained. The homepage
links to it with a single card.

The [verification table of contents](verify/index.html) gathers the OpenHands
agent-sdk verification work: the explainer video in
`experiments/verify-agent-sdk-explainer/` (Manim scene, music and stills), the
Agent Server map and its bug tracker, the core SDK map in progress, and the
OpenHands app map.

The [verification findings](arch/verify-openhands-issues.html) are a dated GitHub
status and evidence snapshot. Update `assets/verify-openhands/issues.json`, then
run `python scripts/build-verification-findings.py` to rebuild the page. Keep the
original 68, follow-up findings, and draft Agent Server API map findings labeled
separately; retain image provenance and distinguish reported evidence from fresh
verification. The renderer does not fetch statuses or advance the snapshot date.

The [maintainer PR queue](investigations/openhands-pr-keep-close.html) and
[Monday issue inventory](investigations/openhands-issues-since-monday.html)
follow frozen cohorts. Refresh GitHub metadata with
`python scripts/refresh-maintainer-triage.py` and
`python scripts/refresh-monday-issue-inventory.py --refresh-weekly`, then render
with `python scripts/build-maintainer-reports.py` and
`python scripts/build-monday-issue-inventory.py`. The collectors use the inherited
proxy and `GITHUB_TOKEN_ENYST` or `GITHUB_TOKEN` and perform no GitHub writes.
They retain the original 53 reviewed PRs, 118 Monday-inventory issues, and
106 issues created in the October 4–11 window. Review newly discovered fixing
references and the ambiguous-reference audit before publishing; preserve
classified exclusions and original review evidence. A changed PR head does not
inherit a fresh code or runtime verdict. Update the homepage counts together
with the rendered reports.

The [earlier issue/PR survey](investigations/openhands-issue-pr-report.html)
keeps its original October 4–11 closure tally. Refresh current statuses in
`assets/openhands-issue-pr-report/data.json`, retaining removed open-list entries
in its refresh audit, then run `python scripts/build-issue-pr-report.py`.
