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
