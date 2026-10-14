#!/usr/bin/env bash
set -euo pipefail
export PATH=/workspace/agent-sdk-verify/.agents/skills/verify-agent-server/scripts:/workspace/.tools/tmux/usr/bin:/workspace/.tools/node-v24.21.0-linux-x64/bin:$PATH
export AGENT_SERVER_VERIFY_HOME=/workspace/verification-artifacts/runs
cd /workspace/agent-sdk-verify
export AGENT_SERVER_VERIFY_RUN=$(control-agent-server launch --new --name video-git-space --print-run)
trap 'control-agent-server stop >/dev/null' EXIT
control-agent-server doctor > "$AGENT_SERVER_VERIFY_RUN/evidence/video-doctor.json"
export GIT_CONFIG_GLOBAL="$AGENT_SERVER_VERIFY_RUN/home/.gitconfig"
REPO=$(control-agent-server fixture git-repo --name video-git --print-path)
NAMES="$AGENT_SERVER_VERIFY_RUN/fixtures/video-names"
mkdir -p "$NAMES"
git -C "$NAMES" init -q -b main
printf 'Original notes\n' > "$NAMES/my notes.md"
git -C "$NAMES" add -A
git -C "$NAMES" commit -qm 'Human readable filename'
control-agent-server api GET /api/git/changes --query path="$NAMES" --expect 200 --check . len-eq 0 --save video.git-space/clean > "$AGENT_SERVER_VERIFY_RUN/evidence/video-clean.json"
printf 'Positive control: clean repository -> HTTP 200, no changes.\n'
printf 'Human: edits "my notes.md". A space. A harmless little space.\n'
printf 'Updated notes\n' > "$NAMES/my notes.md"
control-agent-server api GET /api/git/changes --query path="$NAMES" --expect 400 --check detail contains 'Unexpected git diff output format' --save video.git-space/bug > "$AGENT_SERVER_VERIFY_RUN/evidence/video-bug.json"
printf 'Expected: UPDATED "my notes.md"; actual: HTTP 400.\n'
jq -r '.response.body.detail' "$AGENT_SERVER_VERIFY_RUN/evidence/video-bug.json"
printf 'Changes API: no changed-file list is returned for this repo.\n'
printf 'BUG_CONFIRMED: a tracked filename with a space breaks the Git Changes API.\n'
