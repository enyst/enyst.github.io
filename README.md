# enyst.github.io

Architecture-page maintenance follow-ups: [`OPENHANDS_DOC_STATUS.md`](OPENHANDS_DOC_STATUS.md).

The [OpenHands feature map](openhands-features/index.html) is a static snapshot
of the maintained upstream recipes. Regenerate it from a clean, selected
OpenHands revision with `python scripts/build-openhands-features.py --checkout ../playground`.
The generator preserves every behavior ID and checks literal command fidelity.
Reviewed CLI screenshots and their provenance live in `assets/openhands-features/`;
the `capture-*.json` manifests attach media beneath the corresponding recipes.
New captures must match the selected source revision. The delimited OpenHands
features section in the homepage is generated; other homepage content is retained.
