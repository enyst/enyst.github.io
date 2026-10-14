#!/usr/bin/env bash
set -euo pipefail
export PATH=/workspace/agent-sdk-verify/.agents/skills/verify-agent-server/scripts:/workspace/.tools/tmux/usr/bin:/workspace/.tools/node-v24.21.0-linux-x64/bin:$PATH
export AGENT_SERVER_VERIFY_HOME=/workspace/verification-artifacts/runs
cd /workspace/agent-sdk-verify
export AGENT_SERVER_VERIFY_RUN=$(control-agent-server launch --new --name video-profile-heartbeat --print-run)
trap 'flock -u 9 2>/dev/null || true; control-agent-server stop >/dev/null' EXIT
control-agent-server doctor > "$AGENT_SERVER_VERIFY_RUN/evidence/video-doctor.json"
control-agent-server api POST /api/profiles/video-lock --json '{"llm":{"model":"openai/qa-video-no-provider-call"}}' --expect 201 --quiet
control-agent-server api GET /alive --auth none --expect 200 --expect-max-ms 3000 --save video.profile-heartbeat/control > "$AGENT_SERVER_VERIFY_RUN/evidence/video-alive-control.json"
printf 'Positive control: /alive responds promptly, server is healthy.\n'
LOCK="$AGENT_SERVER_VERIFY_RUN/home/.openhands/profiles/.profiles.lock"
exec 9>>"$LOCK"
flock -w 5 9
(exec 9>&-; control-agent-server api GET /api/profiles/video-lock --timeout 60 --expect 503 --save video.profile-heartbeat/profile-lock > "$AGENT_SERVER_VERIFY_RUN/evidence/video-profile-locked.json") &
WAITER=$!
sleep 5
printf 'Another process holds the profile file lock. A profile read waits.\n'
printf 'Meanwhile: GET /alive ... waiting for the heartbeat ...\n'
control-agent-server api GET /alive --auth none --timeout 60 --expect 200 --save video.profile-heartbeat/bug > "$AGENT_SERVER_VERIFY_RUN/evidence/video-alive-bug.json"
wait "$WAITER"
flock -u 9
ELAPSED=$(jq -r .elapsed_ms "$AGENT_SERVER_VERIFY_RUN/evidence/video-alive-bug.json")
jq -e '.elapsed_ms > 20000' "$AGENT_SERVER_VERIFY_RUN/evidence/video-alive-bug.json" >/dev/null
printf 'Expected: heartbeat within 3 seconds. Actual: HTTP 200 after %s ms.\n' "$ELAPSED"
printf 'One locked profile stalls unrelated requests on the server event loop.\n'
printf 'BUG_CONFIRMED: profile-store lock blocks the server heartbeat.\n'
