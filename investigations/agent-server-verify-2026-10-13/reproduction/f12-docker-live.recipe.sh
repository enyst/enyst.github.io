DK=$(control-agent-server launch --new --name f12-docker-live --env DOCKER_HOST=unix:///var/run/docker.sock --print-run \
  --config-json '{"conversation_runtime":"docker","conversation_image":"qa-agent-server:acca181a-local-uid","conversation_container_memory":"1g","conversation_container_cpus":1,"conversation_container_pids_limit":256,"conversation_storage_retention_days":0.00002}')
trap 'control-agent-server stop --run "$DK" >/dev/null 2>&1 || true; if test -n "${INNER:-}"; then control-agent-server stop --run "$INNER" >/dev/null 2>&1 || true; fi; if test -n "${DEAD:-}"; then control-agent-server stop --run "$DEAD" >/dev/null 2>&1 || true; fi' EXIT
control-agent-server doctor --run "$DK" || control-agent-server doctor --run "$DK"
control-agent-server api POST /api/profiles/qa-f12-docker-llm --run "$DK" --json '{"llm":{"model":"openai/qa-stub","api_key":"qa","base_url":"http://127.0.0.1:9/v1","num_retries":0}}' --expect 200,201 --save F12.docker-runtime/llm-profile
control-agent-server api POST /api/agent-profiles/qa-f12-docker-live --run "$DK" --json '{"agent_kind":"openhands","llm_profile_ref":"qa-f12-docker-llm","tools":[],"secret_refs":[]}' --expect 201 --save F12.docker-runtime/agent-profile
DPID=$(control-agent-server api GET /api/agent-profiles/qa-f12-docker-live --run "$DK" --expect 200 --field profile.id)
CID=$(control-agent-server api POST <redacted:session-cookie> --run "$DK" \
  --json "{\"agent_profile_id\":\"$DPID\",\"autotitle\":false}" --timeout 180 --expect 200,201 --save F12.docker-runtime/create --field id)
cat > "$AGENT_SERVER_VERIFY_RUN/fixtures/docker-safe-inspect.py" <<'PY'
import hashlib, json, subprocess, sys
from pathlib import Path
dk, cid, profile = sys.argv[1:]
owner = hashlib.sha256((str((Path(dk)/'server/workspace/conversations').resolve())+'\0'+str((Path(dk)/'home/.openhands').resolve())).encode()).hexdigest()[:24]
ids = subprocess.check_output(['docker','--host=unix:///var/run/docker.sock','ps','-q','--filter','label=ai.openhands.runtime-owner='+owner],text=True).split()
records = json.loads(subprocess.check_output(['docker','--host=unix:///var/run/docker.sock','inspect',*ids],text=True)) if ids else []
source = str(Path(dk)/'server/workspace/conversations'/cid.replace('-',''))
selected = [r for r in records if any(m['Source']==source for m in r['Mounts'])]
assert len(selected)==1, 'expected exactly the container owned by this conversation'
r = selected[0]; h = r['HostConfig']; e = dict(v.split('=',1) for v in r['Config']['Env'])
assert [h['Memory'],h['NanoCpus'],h['PidsLimit']]==[1073741824,1000000000,256], 'limits mismatch'
assert h['CapDrop']==['ALL'], 'capabilities not dropped'
assert 'no-new-privileges' in h['SecurityOpt'], 'no-new-privileges missing'
assert e['OH_CONVERSATION_RUNTIME']=='local', 'inner runtime not local'
p = json.loads(e['OH_RUNTIME_LAUNCHED_PROFILE'])
assert p['agent_profile_id']==profile and p['secret_refs']==[], 'launched profile mismatch'
port = r['NetworkSettings']['Ports']['8000/tcp'][0]
assert port['HostIp']=='127.0.0.1', 'port binding not local'
print(json.dumps({'container_id':r['Id'],'inner_url':'http://127.0.0.1:'+port['HostPort'],'memory':h['Memory'],'nano_cpus':h['NanoCpus'],'pids_limit':h['PidsLimit'],'cap_drop':h['CapDrop'],'launched_profile':p}))
PY
INSPECT=$(python3 "$AGENT_SERVER_VERIFY_RUN/fixtures/docker-safe-inspect.py" "$DK" "$CID" "$DPID")
printf '%s\n' "$INSPECT"
IURL=$(printf '%s' "$INSPECT" | python3 -c 'import json,sys;print(json.load(sys.stdin)["inner_url"])')
control-agent-server api GET "<redacted:session-cookie>/$CID/runtime" --run "$DK" --expect 200 --check runtime_status eq available --check can_resume eq true --save F12.docker-runtime/available
CREDS_RAW=$(control-agent-server api POST "<redacted:session-cookie>/$CID/runtime/credentials" --run "$DK" --expect 200 --check session_api_key exists)
CKEY=$(printf '%s' "$CREDS_RAW" | python3 -c 'import json,sys;print(json.load(sys.stdin)["response"]["body"]["session_api_key"])')
case "$CREDS_RAW" in *"$CKEY"*) printf '%s\n' 'QA_F12_UNKNOWN_CONTAINER_KEY_PRESENT_IN_NORMAL_MODE';; *) false;; esac
test "${CKEY#<redacted:}" = "$CKEY"
export OPENHANDS_API_KEY="$CKEY"
control-agent-server api POST "<redacted:session-cookie>/$CID/runtime/credentials" --run "$DK" --expect 200 --check session_api_key exists --save F12.docker-runtime/credentials-masked
INNER=$(control-agent-server attach --url "$IURL" --key-env OPENHANDS_API_KEY --print-run)
control-agent-server api GET "<redacted:session-cookie>/$CID" --run "$INNER" --expect 200 --check id eq "$CID" --save F12.docker-runtime/inner-authenticated
control-agent-server api GET /server_info --run "$INNER" --expect 200 --check build_git_sha eq acca181af1f353975965bcf6486e1d0a58f444c0 --save F12.docker-runtime/inner-target-sha
control-agent-server api GET "<redacted:session-cookie>/$CID" --run "$DK" --expect 200 --check launched_agent_profile.agent_profile_id eq "$DPID" --save F12.docker-runtime/launched-profile
control-agent-server api GET "<redacted:session-cookie>/$CID/events/search" --run "$DK" --header 'X-Expose-Secrets: plaintext' --expect 200 --save F12.docker-runtime/persisted-history
control-agent-server api GET "<redacted:session-cookie>/$CID/bash/bash_events/search" --run "$DK" --header 'X-Expose-Secrets: plaintext' --expect 422 --check detail eq 'Runtime secret exposure is unsupported' --save F12.docker-runtime/exposure-refused
control-agent-server api DELETE "<redacted:session-cookie>/$CID/runtime" --run "$DK" --expect 204 --save F12.docker-runtime/release
control-agent-server api GET "<redacted:session-cookie>/$CID/runtime" --run "$DK" --expect 200 --check runtime_status eq missing --check can_resume eq true
control-agent-server api GET "<redacted:session-cookie>/$CID" --run "$DK" --expect 200
control-agent-server api POST "<redacted:session-cookie>/$CID/runtime/reprovision" --run "$DK" --timeout 180 --expect 200 --check runtime_status eq available --save F12.docker-runtime/reprovision
control-agent-server api DELETE "<redacted:session-cookie>/$CID/runtime" --run "$DK" --expect 204
T0=$SECONDS
until control-agent-server state ls --run "$DK" "home/.openhands/runtime-control/${CID//-/}.archived.json" --expect-count 1 >/dev/null; do
  test $((SECONDS-T0)) -le 360
  sleep 2
done
control-agent-server api POST "<redacted:session-cookie>/$CID/runtime/reprovision" --run "$DK" --expect 410 --check detail eq 'Conversation runtime was archived; its history is read-only' --save F12.docker-runtime/archived
control-agent-server api GET "<redacted:session-cookie>/$CID" --run "$DK" --expect 200 --save F12.docker-runtime/archive-history
control-agent-server stop --run "$INNER"
control-agent-server stop --run "$DK"
DF="$AGENT_SERVER_VERIFY_RUN/fixtures/no-health-image"
mkdir -p "$DF"
cat > "$DF/Dockerfile" <<'EOF'
FROM qa-agent-server:acca181a-local-uid
ENTRYPOINT ["python", "-c", "import time; time.sleep(600)"]
EOF
DOCKER_BUILDKIT=0 docker --host=unix:///var/run/docker.sock build --network=none -t qa-agent-server:nohealth-uid-acca181a "$DF"
DEAD=$(control-agent-server launch --new --name f12-docker-timeout --env DOCKER_HOST=unix:///var/run/docker.sock --print-run --config-json '{"conversation_runtime":"docker","conversation_image":"qa-agent-server:nohealth-uid-acca181a","conversation_container_startup_timeout":2}')
control-agent-server doctor --run "$DEAD" || control-agent-server doctor --run "$DEAD"
control-agent-server api POST <redacted:session-cookie> --run "$DEAD" --json '{"agent":{"llm":{"model":"openai/qa-stub","api_key":"qa"},"tools":[]},"autotitle":false}' --timeout 180 --expect 502 --expect-max-ms 120000 --save F12.docker-runtime/startup-bound
control-agent-server logs --run "$DEAD" --grep 'healthy in time' --expect-min 1
control-agent-server stop --run "$DEAD"
