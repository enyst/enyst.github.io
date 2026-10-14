# F04 supplemental conversation lifecycle branches

Source: `openhands-agent-server/openhands/agent_server/conversation_router.py`, `openhands-agent-server/openhands/agent_server/conversation_service.py`
Routes: none

## Sub-features

- `F04.supplement-arrange`: arrange the secondary branches of three existing bugs.
- `F04.patch-whitespace-title-persisted`: observe the title after accepting whitespace.
- `F04.delete-unknown-id-repeat`: repeat a successful conversation deletion.
- `F04.create-initial-message-run-false-status`: read the completed run=false conversation.
- `F04.create-initial-message-run-false-actions`: count actions after run=false creation.

## How to get to it (agent POV)

Use the REST conversation create, GET, PATCH, DELETE and event routes through the
unchanged CLI. These are supplementary observations for existing F04 bugs.

## Driving it with control-agent-server

Preconditions:

```sh
mkdir -p "$AGENT_SERVER_VERIFY_RUN/evidence/F04.supplement"
if ! control-agent-server doctor > "$AGENT_SERVER_VERIFY_RUN/evidence/F04.supplement/doctor.json"; then
  control-agent-server doctor > "$AGENT_SERVER_VERIFY_RUN/evidence/F04.supplement/doctor-retry.json"
fi
W="$AGENT_SERVER_VERIFY_RUN/fixtures/qa-f04-supplement-ws"
mkdir -p "$W"
OFFLINE_AGENT='{"llm":{"model":"openai/qa-offline","api_key":"<redacted:api_key>","base_url":"http://127.0.0.1:9/v1","num_retries":0},"tools":[]}'
STUB=$(control-agent-server fixture llm-stub --name qa-f04-supplement-stub --step 'tool:finish:{"message":"QA_F04_SUPPLEMENT_DONE"}' --print-path)
STUB_AGENT="{\"llm\":{\"model\":\"openai/qa-stub\",\"api_key\":\"<redacted:api_key>\",\"base_url\":\"$STUB/v1\",\"num_retries\":0},\"tools\":[]}"
```

- **Arrange the original bug's remaining branches (`F04.supplement-arrange`).**
  Accept the previously confirmed whitespace PATCH200 only to reach its GET.
  Create/delete an independent idle conversation to reach repeated deletion.
  Persist the run=false message and wait for the already confirmed execution.

  ```sh
  TITLEID=$(control-agent-server api POST <redacted:session-cookie> --json "{\"workspace\":{\"working_dir\":\"$W\"},\"agent\":$OFFLINE_AGENT,\"autotitle\":false}" --expect 201 --field id)
  control-agent-server api PATCH "<redacted:session-cookie>/$TITLEID" --json '{"title":"QA F04 preserved title"}' --expect 200 --check success eq true
  control-agent-server api GET "<redacted:session-cookie>/$TITLEID" --expect 200 --check title eq 'QA F04 preserved title' --save F04.patch-whitespace-title/before
  control-agent-server api PATCH "<redacted:session-cookie>/$TITLEID" --json '{"title":"   "}' --expect 200 --check success eq true --save F04.patch-whitespace-title/accepted-whitespace
  DEL=$(control-agent-server api POST <redacted:session-cookie> --json "{\"workspace\":{\"working_dir\":\"$W\"},\"agent\":$OFFLINE_AGENT,\"autotitle\":false}" --expect 201 --field id)
  control-agent-server api DELETE "<redacted:session-cookie>/$DEL" --expect 200 --check success eq true --save F04.delete-unknown-id/first-delete
  control-agent-server api GET "<redacted:session-cookie>/$DEL" --expect 404 --save F04.delete-unknown-id/get-deleted
  NR=$(control-agent-server api POST <redacted:session-cookie> --json "{\"workspace\":{\"working_dir\":\"$W\"},\"agent\":$STUB_AGENT,\"autotitle\":false,\"initial_message\":{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"QA F04 supplement run false.\"}],\"run\":false}}" --expect 201 --save F04.create-initial-message-run-false/supplement-start --field id)
  control-agent-server conversation events "$NR" --kinds MessageEvent --contains 'QA F04 supplement run false.' --expect-count 1 --save F04.create-initial-message-run-false/supplement-message
  control-agent-server conversation wait "$NR" --until finished --timeout 30
  control-agent-server api GET "<redacted:session-cookie>/$NR" --expect 200 --save F04.create-initial-message-run-false/observed-status
  control-agent-server conversation events "$NR" --kinds ActionEvent --expect-min 1 --save F04.create-initial-message-run-false/observed-actions
  ```

- **Whitespace title persisted GET (`F04.patch-whitespace-title-persisted`), known bug.**

  Requires: `F04.supplement-arrange`
  ```sh
  control-agent-server api GET "<redacted:session-cookie>/$TITLEID" --expect 200 --check title eq 'QA F04 preserved title' --save F04.patch-whitespace-title/get-after-whitespace  # bug
  ```

- **Repeated DELETE (`F04.delete-unknown-id-repeat`), known bug.**

  Requires: `F04.supplement-arrange`
  ```sh
  control-agent-server api GET /openapi.json --check 'paths.<redacted:session-cookie>/{conversation_id}.delete.responses.404' exists --quiet
  control-agent-server api DELETE "<redacted:session-cookie>/$DEL" --expect 404 --save F04.delete-unknown-id/repeat  # bug
  ```

- **Run=false final status (`F04.create-initial-message-run-false-status`), known bug.**

  Requires: `F04.supplement-arrange`
  ```sh
  control-agent-server api GET "<redacted:session-cookie>/$NR" --expect 200 --check execution_status eq idle --save F04.create-initial-message-run-false/supplement-get  # bug
  ```

- **Run=false action count (`F04.create-initial-message-run-false-actions`), known bug.**

  Requires: `F04.supplement-arrange`
  ```sh
  control-agent-server conversation events "$NR" --kinds ActionEvent --expect-count 0 --save F04.create-initial-message-run-false/supplement-actions  # bug
  ```

## Gotchas

The arrange recipe accepts existing wrong behavior to observe its downstream
effects. This does not change the contract expectations or create new bug counts.
