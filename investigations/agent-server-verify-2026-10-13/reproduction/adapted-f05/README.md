# F05 crash-recovery recipe adaptation

The repository CLI and product code remain unchanged. `run-adapted-f05.py`
loads the original CLI module and points only `FEATURE_MAP_DIR` at this copied
recipe. The copy is preserved beside the original map for review.

The execution container's PID 1 does not promptly reap killed server processes.
The lease's `owner_pid` therefore remains a zombie, and the product's
`os.kill(pid, 0)` check considers it alive. The original immediate restart
assertion cannot reach normal recovery before the lease expires.

After SIGKILL the copied recipe records the lease owner status, its expiry, and
remaining TTL; it refuses to wait if the owner is actually live. It waits for
that recorded expiry and restarts again before the unchanged recovery and
`# bug` pause assertions. Ordinary running recovery passes under that condition,
and the accepted mid-call pause is lost on both fresh attempts: GET reports
`error` while both PauseEvents remain persisted. This does not certify immediate
dead-owner takeover.

```sh
.venv/bin/python /workspace/verification-artifacts/adapted-f05/run-adapted-f05.py map run --file F05 --only F05.restart-running-graceful,F05.restart-hard-running,F05.pause-running-crash --fresh --repeat 2 --record --keep-going --timeout 420
```

The unrelated later supplemental bullets in this copy were not selected in the
crash run. Minimal F05 secondary proofs are under `../adapted-f05-secondary`.

