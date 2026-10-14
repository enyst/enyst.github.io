#!/usr/bin/env bash
set -euo pipefail
export PATH=/workspace/agent-sdk-verify/.agents/skills/verify-agent-server/scripts:/workspace/.tools/tmux/usr/bin:/workspace/.tools/node-v24.21.0-linux-x64/bin:$PATH
export AGENT_SERVER_VERIFY_HOME=/workspace/verification-artifacts/runs
cd /workspace/agent-sdk-verify
export AGENT_SERVER_VERIFY_RUN=$(control-agent-server launch --new --name video-secret-loss --print-run)
trap 'control-agent-server stop >/dev/null' EXIT
control-agent-server doctor > "$AGENT_SERVER_VERIFY_RUN/evidence/video-doctor.json"
control-agent-server api PUT /api/settings/secrets --json '{"name":"HERO_TOKEN","value":"qa-video-fake-credential"}' --expect 200 --quiet
control-agent-server api GET /api/settings/secrets/HERO_TOKEN --expect 200 --check . eq qa-video-fake-credential --save video.secret-loss/original > "$AGENT_SERVER_VERIFY_RUN/evidence/video-original.json"
printf 'A fake credential is saved and readable. No real account is involved.\n'
control-agent-server restart --rotate-secret-key > "$AGENT_SERVER_VERIFY_RUN/evidence/video-rotate-control.json"
control-agent-server restart --restore-secret-key > "$AGENT_SERVER_VERIFY_RUN/evidence/video-restore-control.json"
control-agent-server api GET /api/settings/secrets/HERO_TOKEN --expect 200 --check . eq qa-video-fake-credential --save video.secret-loss/control > "$AGENT_SERVER_VERIFY_RUN/evidence/video-control.json"
printf 'Positive control: rotate away, rotate back, original credential survives.\n'
control-agent-server restart --rotate-secret-key > "$AGENT_SERVER_VERIFY_RUN/evidence/video-rotate-bug.json"
control-agent-server api PUT /api/settings/secrets --json '{"name":"SIDE_TOKEN","value":"qa-video-unrelated-value"}' --expect 200 --save video.secret-loss/unrelated-write > "$AGENT_SERVER_VERIFY_RUN/evidence/video-unrelated.json"
printf 'Rotate away again. Save one unrelated fake credential: HTTP 200.\n'
control-agent-server restart --restore-secret-key > "$AGENT_SERVER_VERIFY_RUN/evidence/video-restore-bug.json"
control-agent-server api GET /api/settings/secrets/HERO_TOKEN --expect 404 --check detail eq 'Secret not found' --save video.secret-loss/bug > "$AGENT_SERVER_VERIFY_RUN/evidence/video-lost.json"
control-agent-server state cat home/.openhands/secrets.json --check custom_secrets.HERO_TOKEN.secret eq null > "$AGENT_SERVER_VERIFY_RUN/evidence/video-null.json"
printf 'Expected: original credential survives. Actual after rotating back: HTTP 404.\n'
printf 'Persisted HERO_TOKEN.secret = null. The old ciphertext was overwritten.\n'
printf 'BUG_CONFIRMED: an unrelated write under another cipher key destroys a saved credential.\n'
