# OpenHands feature-map reading editions

`scenarios.html` is the searchable reading edition of the Agent Canvas map.
Each `scenarios-Fxx.html` page contains that family's named scripts, expected
behavior, known issues, exact source recipes and executable bug blocks.
The tag is `openhands-features`, under the Self-Healing Codebase Project.

Regenerate from an explicit, clean OpenHands checkout:

```sh
python3 scripts/build-openhands-scenarios.py \
  --checkout /path/to/OpenHands \
  --date 2026-10-16 \
  --source-label 'PR #18334' \
  --source-pr 18334
node --check assets/openhands-features/scenarios.js
```

The generator pins the checkout's commit and backend versions, preserves all
declared behavior IDs, and checks fragment links and every literal inline code
span and fenced block against its own scenario. It emits `scenarios.json` with
source hashes, inventory, recipes and notes. It does not run verification or
infer passing results. Behavior contracts without a separately named recipe
are explicit rather than given an invented replay.

The mini scripts are reading outlines; the expanded source is the complete
replay contract. Missing prerequisites and not-run checks are distinct from
reproduced failures. Once a fix is verified in the application version under
test, remove obsolete failures from the maintained source map before generating
a new edition. Historical evidence belongs in the dated backfill ledger.

The original family pages and `feature-map.json` retain their October 9 snapshot
and reviewed screenshots. `build-openhands-features.py` owns that older edition.
Update the authored home-page and chapter cards when publishing a new snapshot;
do not silently relabel old screenshots as evidence for a newer revision.
