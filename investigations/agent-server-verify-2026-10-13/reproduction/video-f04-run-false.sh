#!/usr/bin/env bash
set -euo pipefail
cd /workspace/agent-sdk-verify
export PATH=/workspace/agent-sdk-verify/.agents/skills/verify-agent-server/scripts:/workspace/.tools/tmux/usr/bin:/workspace/.tools/node-v24.21.0-linux-x64/bin:$PATH
export UV_CACHE_DIR=/workspace/.cache/uv
export PRE_COMMIT_HOME=/workspace/.cache/pre-commit
export AGENT_SERVER_VERIFY_HOME=/workspace/verification-artifacts/runs
export AGENT_SERVER_VERIFY_RUN=$(control-agent-server launch --new --name video-f04-run-false --print-run)
trap 'control-agent-server stop --run "$AGENT_SERVER_VERIFY_RUN" >/dev/null' EXIT
control-agent-server api GET /openapi.json --timeout 120 --quiet >/dev/null
control-agent-server doctor >/dev/null
WORKSPACE="$AGENT_SERVER_VERIFY_RUN/fixtures/video-workspace"
mkdir -p "$WORKSPACE"
STUB=$(control-agent-server fixture llm-stub --name video-f04-provider --step 'tool:finish:{"message":"QA_VIDEO_FINISHED"}' --print-path)
AGENT="{\"llm\":{\"model\":\"openai/qa-video\",\"api_key\":\"<redacted:api_key>\",\"base_url\":\"$STUB/v1\",\"num_retries\":0},\"tools\":[]}"
CONTROL=$(control-agent-server api POST <redacted:session-cookie> --json "{\"workspace\":{\"working_dir\":\"$WORKSPACE\"},\"agent\":$AGENT,\"autotitle\":false,\"initial_message\":{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"Control: finish now.\"}],\"run\":true}}" --expect 201 --field id --save F04.create-initial-message-run-false/video-control)
control-agent-server conversation wait "$CONTROL" --until finished --timeout 30 >/dev/null
CONTROL_STATUS=$(control-agent-server api GET "<redacted:session-cookie>/$CONTROL" --field execution_status)
test "$CONTROL_STATUS" = finished
printf 'CONTROL: initial_message.run=true  -> %s\n' "$CONTROL_STATUS"
TEST=$(control-agent-server api POST <redacted:session-cookie> --json "{\"workspace\":{\"working_dir\":\"$WORKSPACE\"},\"agent\":$AGENT,\"autotitle\":false,\"initial_message\":{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"Test: do not run yet.\"}],\"run\":false}}" --expect 201 --field id --save F04.create-initial-message-run-false/video-false-request)
control-agent-server conversation wait "$TEST" --until finished --timeout 30 >/dev/null
TEST_STATUS=$(control-agent-server api GET "<redacted:session-cookie>/$TEST" --field execution_status --save F04.create-initial-message-run-false/video-false-after)
test "$TEST_STATUS" = finished
printf 'TEST:    initial_message.run=false -> %s\n' "$TEST_STATUS"
CALLS=$(control-agent-server sink read --name video-f04-provider --path /v1/chat/completions --expect-min 2 --expect-max 2 --save F04.create-initial-message-run-false/video-provider-calls | jq -r .requests)
test "$CALLS" = 2
printf 'Provider calls recorded: %s\n' "$CALLS"
printf 'BUG_CONFIRMED: run=false still scheduled an agent run.\n'
