# F28 persistence and uninstall core supplement

## Driving it with control-agent-server
Preconditions:
```sh
control-agent-server doctor
FX=$(control-agent-server fixture canvas-app --name qa-f28-core --backend ok --print-path)
control-agent-server api POST /api/canvas-extensions/install --json "{\"source\":\"$FX\"}" --check name eq qa-f28-core --save F28.core-setup/install
REV=$(control-agent-server api GET /api/canvas-extensions/installed/qa-f28-core/backend --field revision)
control-agent-server api POST /api/canvas-extensions/installed/qa-f28-core/backend/prepare --json "{\"revision\":\"$REV\"}" --check prepared_revision eq "$REV" --save F28.core-setup/prepare
```
- **Persistence (`F28.restart-persistence`).**
  ```sh
  control-agent-server api PATCH /api/canvas-extensions/installed/qa-f28-core --json '{"enabled":true}' --check enabled eq true
  OLD_PID=$(control-agent-server api POST /api/canvas-extensions/installed/qa-f28-core/backend/start --json "{\"revision\":\"$REV\"}" --check state eq ready --field pid)
  control-agent-server restart
  control-agent-server api GET /api/canvas-extensions/installed --check canvas_extensions len-eq 1 --quiet --save F28.restart-persistence/installed
  control-agent-server api GET /api/canvas-extensions/installed/qa-f28-core --check enabled eq true --save F28.restart-persistence/metadata
  control-agent-server api GET /api/canvas-extensions/installed/qa-f28-core/backend --check state eq stopped --check prepared_revision eq "$REV" --check pid eq null --save F28.restart-persistence/backend
  control-agent-server api POST /api/canvas-extensions/installed/qa-f28-core/backend/start --json "{\"revision\":\"$REV\"}" --check state eq ready --check pid ne "$OLD_PID" --save F28.restart-persistence/start-again
  control-agent-server api POST /api/canvas-extensions/installed/qa-f28-core/backend/stop --check state eq stopped
  ```
- **Uninstall (`F28.uninstall`).**
  ```sh
  control-agent-server api POST /api/canvas-extensions/installed/qa-f28-core/backend/start --json "{\"revision\":\"$REV\"}" --check state eq ready
  control-agent-server api DELETE /api/canvas-extensions/installed/qa-f28-core --check message eq "Canvas extension 'qa-f28-core' uninstalled" --save F28.uninstall/delete
  control-agent-server api GET /api/canvas-extensions/installed/qa-f28-core --expect 404
  control-agent-server api GET /api/canvas-extensions/installed --check canvas_extensions len-eq 0 --save F28.uninstall/installed
  control-agent-server state cat home/.openhands/canvas-extensions/installed/.installed.json --check extensions.qa-f28-core missing --max-chars 100
  control-agent-server api GET /api/canvas-extensions/installed/qa-f28-core/backend --check state eq missing --check prepared_revision eq "$REV" --save F28.uninstall/backend
  test -d "$AGENT_SERVER_VERIFY_RUN/home/.openhands/canvas-extensions/backends/data/qa-f28-core/home"
  control-agent-server state cat home/.openhands/canvas-extensions/backends/approvals/qa-f28-core.json --check revision eq "$REV"
  control-agent-server api DELETE /api/canvas-extensions/installed/qa-f28-core --expect 404
  control-agent-server api DELETE /api/canvas-extensions/installed/qa-f28-core/backend/data --check state eq missing --save F28.uninstall/delete-data
  control-agent-server state ls 'home/.openhands/canvas-extensions/backends/data/qa-f28-core' --expect-count 0
  ```
