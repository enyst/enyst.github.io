#!/usr/bin/env bash
set -euo pipefail
export PATH=/workspace/agent-sdk-verify/.agents/skills/verify-agent-server/scripts:/workspace/.tools/tmux/usr/bin:/workspace/.tools/node-v24.21.0-linux-x64/bin:$PATH
export UV_CACHE_DIR=/workspace/.cache/uv
export npm_config_cache=/workspace/.cache/npm
export AGENT_SERVER_VERIFY_HOME=/workspace/verification-artifacts/runs
OUT=/workspace/verification-artifacts/family-results
for attempt in 1 2; do
  RUN=$(control-agent-server launch --new --name "f22-lock-confirm-$attempt" --print-run)
  printf '%s\n' "$RUN" > "$OUT/F22-lock-confirm-$attempt.run"
  trap 'control-agent-server stop --run "$RUN" >/dev/null || true' EXIT
  if ! control-agent-server doctor --run "$RUN" > "$OUT/F22-lock-confirm-$attempt-doctor-before.json"; then
    control-agent-server doctor --run "$RUN" > "$OUT/F22-lock-confirm-$attempt-doctor-before-retry.json"
  fi
  control-agent-server map run --file F22 --only F22.save-classes,F22.store-busy-responsive --run "$RUN" --record --keep-going > "$OUT/F22-lock-confirm-$attempt.json"
  control-agent-server doctor --run "$RUN" > "$OUT/F22-lock-confirm-$attempt-doctor-after.json" || true
  control-agent-server stop --run "$RUN" > "$OUT/F22-lock-confirm-$attempt-stop.json"
  trap - EXIT
done
