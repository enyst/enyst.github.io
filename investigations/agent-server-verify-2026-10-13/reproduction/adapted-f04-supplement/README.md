# F04 secondary-branch reproduction

This isolated recipe supplements the unchanged repository F04 map. Its known-bug
recipes normally stop at the first failing command, so their later GET, repeated
DELETE, and action-count assertions do not execute. These recipes accept the
already confirmed first failure only to arrange the remaining observation. The
original expectations remain at the new `# bug` assertions.

Each supplemental ID belongs to an existing bug; none is a new bug count:

- `F04.patch-whitespace-title-persisted` → `F04.patch-whitespace-title`
- `F04.delete-unknown-id-repeat` → `F04.delete-unknown-id`
- `F04.create-initial-message-run-false-status` and `F04.create-initial-message-run-false-actions` →
  `F04.create-initial-message-run-false`

The original CLI module is loaded without changing its code. Only its
`FEATURE_MAP_DIR` points to this reviewable recipe. The map command launches two
independent runs and stops each run through the ordinary CLI cleanup path. An
offline inline agent creates the idle title/delete fixtures; an exact finish
provider fixture reproduces the controlled run=false defect. No real model is
required for these secondary branches.

```sh
python3 /workspace/verification-artifacts/adapted-f04-supplement/run-adapted-f04-supplement.py map run --file F04 --fresh --repeat 2 --record --keep-going --timeout 420
```
