#!/usr/bin/env bash
set -euo pipefail
export PATH=/workspace/agent-sdk-verify/.agents/skills/verify-agent-server/scripts:/workspace/.tools/tmux/usr/bin:/workspace/.tools/node-v24.21.0-linux-x64/bin:$PATH
export UV_CACHE_DIR=/workspace/.cache/uv
export npm_config_cache=/workspace/.cache/npm
export AGENT_SERVER_VERIFY_HOME=/workspace/verification-artifacts/runs
OUT=/workspace/verification-artifacts/family-results
for attempt in 1 2; do
  RUN=$(control-agent-server launch --new --name "f27-browser-$attempt" --print-run)
  printf '%s\n' "$RUN" > "$OUT/F27-browser-confirm-$attempt.run"
  trap 'control-agent-server stop --run "$RUN" >/dev/null || true' EXIT
  if ! control-agent-server doctor --run "$RUN" > "$OUT/F27-browser-confirm-$attempt-doctor-before.json"; then
    control-agent-server doctor --run "$RUN" > "$OUT/F27-browser-confirm-$attempt-doctor-before-retry.json"
  fi
  # The standard Chromium is present on this host. Keep the recipe's private
  # symlink prerequisite for the enabled/disabled and Docker catalog cases.
  # The target is populated by the tracked F27 preconditions.
  mkdir -p "$RUN/home/.cache"
  ln -s "$RUN/fixtures/qa-f27/playwright" "$RUN/home/.cache/ms-playwright"
  control-agent-server map run --file F27 --only F27.browser-disabled-launch,F27.browser-disabled,F27.server-info-browser-disabled,F27.subagents-browser-disabled,F27.catalog-docker-runtime --run "$RUN" --record --keep-going > "$OUT/F27-browser-confirm-$attempt.json"
  control-agent-server doctor --run "$RUN" > "$OUT/F27-browser-confirm-$attempt-doctor-after.json" || true
  control-agent-server stop --run "$RUN" > "$OUT/F27-browser-confirm-$attempt-stop.json"
  trap - EXIT
done
