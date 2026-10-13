#!/usr/bin/env bash
set -euo pipefail
export PATH="/workspace/agent-sdk-verify/.agents/skills/verify-agent-server/scripts:/workspace/.tools/tmux/usr/bin:$PATH"
export AGENT_SERVER_VERIFY_HOME=/workspace/verification-artifacts/runs
export AGENT_SERVER_VERIFY_RUN
AGENT_SERVER_VERIFY_RUN=$(control-agent-server launch --new --name video-f14-atomic --checkout /workspace/agent-sdk-verify --print-run)
server_pid=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["pid"])' "$AGENT_SERVER_VERIFY_RUN/run.json")
trap 'prlimit --pid "$server_pid" --fsize=unlimited: >/dev/null 2>&1 || true; control-agent-server stop --run "$AGENT_SERVER_VERIFY_RUN" >/dev/null 2>&1 || true' EXIT
control-agent-server doctor > "$AGENT_SERVER_VERIFY_RUN/evidence/video-doctor-cold.json" || control-agent-server doctor > "$AGENT_SERVER_VERIFY_RUN/evidence/video-doctor-warm.json"
fixture="$AGENT_SERVER_VERIFY_RUN/fixtures/video-atomic"
mkdir -p "$fixture"
printf 'qa-f14 v2\n' > "$fixture/original.txt"
head -c 900000 /dev/zero > "$fixture/new.bin"
control-agent-server api POST /api/file/upload --query path="$fixture/control.bin" --file file="$fixture/new.bin" --expect 200 --save VIDEO.atomic/control-upload >/dev/null
cmp "$fixture/new.bin" "$fixture/control.bin"
control-agent-server api POST /api/file/upload --query path="$fixture/target.txt" --file file="$fixture/original.txt" --expect 200 --save VIDEO.atomic/original-upload >/dev/null
cmp "$fixture/original.txt" "$fixture/target.txt"
printf '%s\n' 'Positive controls: 900000-byte upload succeeds; original 10-byte file is intact.'
printf '%s\n' 'Now overwrite it with 900000 bytes under a 500000-byte write limit.'
prlimit --pid "$server_pid" --fsize=500000:
control-agent-server api POST /api/file/upload --query path="$fixture/target.txt" --file file="$fixture/new.bin" --expect 500 --check exception contains 'File too large' --save VIDEO.atomic/failed-overwrite > "$fixture/response-safe.json"
prlimit --pid "$server_pid" --fsize=unlimited:
control-agent-server api GET /api/file/download --query path="$fixture/target.txt" --expect 200 --raw-out "$fixture/after.bin" --save VIDEO.atomic/after-download >/dev/null
python3 - "$fixture" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1]); response = json.loads((p/'response-safe.json').read_text())
old, new, after = [(p/n).read_bytes() for n in ['original.txt','new.bin','after.bin']]
assert old == b'qa-f14 v2\n' and len(old) == 10
assert len(new) == 900000 and len(after) == 500000
assert response['status'] == 500 and 'File too large' in response['response']['body']['exception']
assert after == new[:500000] and after != old
print('HTTP', response['status'], ':', response['response']['body']['exception'])
print(f'Before: {len(old)} bytes. Attempted: {len(new)} bytes. After failure: {len(after)} partial bytes.')
print('Content comparison: original file lost; partial replacement persisted.')
print('BUG_CONFIRMED: failed upload destroyed the previous file.')
PY
