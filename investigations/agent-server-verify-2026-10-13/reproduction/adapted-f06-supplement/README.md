# F06 secondary branches

The original multi-assertion known-bug recipes stop at their first failure.
This copy adds independent selected bullets for short-kind count, mixed event
batch, empty-log role rejection and mutation, timestamp socket replay, and
timestamp ordering. Expected results remain unchanged at the marked assertions.
Each branch reproduces in two fresh independent runs and strengthens one
existing bug block, with no added bug count or primary feature total.

The wrapper loads the unchanged repository CLI and points its feature-map
directory at this copy. Each fresh run is checked with `doctor`. The tiny
file-editor turn runs on real `deepseek/deepseek-flash`, preserving the skill's
happy-path requirement. No product responses are mocked.

```sh
.venv/bin/python /workspace/verification-artifacts/adapted-f06-supplement/run-adapted-f06.py map run --file F06 --only F06.send-no-run,F06.get-one,F06.send-run,F06.search-kind-short-count,F06.unknown-event-batch,F06.send-non-user-role-empty,F06.send-non-user-role-empty-mutation,F06.search-timestamp-replay,F06.search-timestamp-order-sorted --fresh --repeat 2 --record --keep-going --timeout 420
```

