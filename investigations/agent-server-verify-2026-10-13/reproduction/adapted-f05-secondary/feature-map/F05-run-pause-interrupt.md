# F05 suppressed secondary branches

Launch: `--config-json '{"max_concurrent_runs":1}'`

## Sub-features

- `F05.pause-base-setup`: arrange an accepted mid-call pause through real API calls.
- `F05.unknown-id-interrupt`: missing-ID interrupt follows its documented status.
- `F05.pause-running-base-state`: paused disk state agrees with the accepted pause.

## Driving it with control-agent-server

Preconditions:
```sh
control-agent-server doctor
NOPE=$(python3 -c 'import uuid; print(uuid.uuid4())')
PAUSE_KIND=openhands.sdk.event.user_action.PauseEvent
HANG=$(control-agent-server fixture llm-stub --name qa-f05-secondary-hang --step hang:300 --print-path)
HANG_AGENT="{\"llm\":{\"model\":\"openai/qa-stub\",\"api_key\":\"<redacted:api_key>\",\"base_url\":\"$HANG/v1\",\"num_retries\":0},\"tools\":[]}"
P=$(control-agent-server conversation start --body-json "{\"agent\":$HANG_AGENT}" --no-autotitle --print-id)
```
- **Unknown interrupt (`F05.unknown-id-interrupt`), known bug.**
  ```sh
  control-agent-server api GET /openapi.json --check 'paths.<redacted:session-cookie>/{conversation_id}/interrupt.post.responses.404' exists --quiet --save F05.unknown-id-interrupt/openapi
  control-agent-server api GET "<redacted:session-cookie>/$NOPE" --expect 404 --save F05.unknown-id-interrupt/get-control
  control-agent-server api POST "<redacted:session-cookie>/$NOPE/interrupt" --expect 404 --save F05.unknown-id-interrupt/interrupt  # bug
  ```
- **Paused snapshot setup (`F05.pause-base-setup`).**
  ```sh
  control-agent-server conversation send "$P" --text 'hi' --no-run
  control-agent-server api POST "<redacted:session-cookie>/$P/run" --expect 200 --check success eq true
  control-agent-server conversation wait "$P" --until running --timeout 30
  control-agent-server sink read --name qa-f05-secondary-hang --expect-min 1 --wait 30
  control-agent-server api POST "<redacted:session-cookie>/$P/pause" --expect 200 --check success eq true --save F05.pause-running-base-state/accepted
  control-agent-server api GET <redacted:session-cookie>/search --query status=paused --check items contains "$P" --quiet --save F05.pause-running-base-state/search-control
  control-agent-server api GET "<redacted:session-cookie>/$P/events/count" --query kind="$PAUSE_KIND" --check . eq 1 --save F05.pause-running-base-state/pause-count
  ```
- **Paused base snapshot (`F05.pause-running-base-state`), known bug.**
  Requires: `F05.pause-base-setup`
  ```sh
  control-agent-server state cat "server/workspace/conversations/${P//-/}/base_state.json" --check execution_status eq paused  # bug
  ```
