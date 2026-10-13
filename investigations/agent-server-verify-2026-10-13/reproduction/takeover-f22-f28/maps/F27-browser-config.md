# F27 browser configuration supplement

## Driving it with control-agent-server
Preconditions:
```sh
control-agent-server doctor
control-agent-server llm preset deepseek --no-validate
```
- **Browser config ordinary (`F27.browser-disabled-launch`, `F27.browser-disabled`).**
  ```sh
  control-agent-server api GET /api/tools/catalog --check tools contains '{"name": "browser_tool_set", "user_selectable": true, "usable": true' --quiet
  BON=$(control-agent-server conversation start --no-run --no-autotitle --print-id)
  control-agent-server api GET "<redacted:session-cookie>/$BON" --check agent.tools contains browser_tool_set --quiet --save F27.browser-disabled-launch/enabled
  control-agent-server restart --config-json '{"enable_browser":false}'
  BOFF=$(control-agent-server conversation start --no-run --no-autotitle --print-id)
  control-agent-server api GET "<redacted:session-cookie>/$BOFF" --check agent.tools not-contains browser_tool_set --check agent.tools contains terminal --check agent.tools contains file_editor --quiet --save F27.browser-disabled-launch/disabled
  control-agent-server api GET "<redacted:session-cookie>/$BON" --check agent.tools contains browser_tool_set --quiet
  control-agent-server api GET /api/tools/catalog --check tools contains '{"name": "browser_tool_set", "user_selectable": true, "usable": false' --quiet --save F27.browser-disabled/catalog
  ```
- **Server-info browser disabled (`F27.server-info-browser-disabled`), known bug.**
  ```sh
  control-agent-server api GET /api/tools/catalog --check tools contains '{"name": "browser_tool_set", "user_selectable": true, "usable": false' --quiet
  control-agent-server api GET /server_info --auth none --check usable_tools contains terminal --check usable_tools not-contains browser_tool_set --save F27.server-info-browser-disabled/server-info  # bug
  ```
- **Subagents browser disabled (`F27.subagents-browser-disabled`), known bug.**
  ```sh
  control-agent-server api GET /api/tools/catalog --check tools contains '{"name": "browser_tool_set", "user_selectable": true, "usable": false' --quiet
  control-agent-server api POST /api/sub-agents --json '{"load_user":false,"load_project":false}' --check agents contains '"name": "bash-runner"' --check agents not-contains '"name": "web-researcher"' --save F27.subagents-browser-disabled/builtins  # bug
  ```
- **Docker-runtime catalog (`F27.catalog-docker-runtime`).**
  ```sh
  control-agent-server restart --reset-config --config-json '{"conversation_runtime":"docker","conversation_image":"ghcr.io/openhands/agent-server:1.2.3-python-minimal"}'
  control-agent-server api GET /api/tools/catalog --check tools contains '{"name": "browser_tool_set", "user_selectable": true, "usable": false' --quiet --save F27.catalog-docker-runtime/minimal-image
  control-agent-server restart --config-json '{"conversation_image_has_browser":true}'
  control-agent-server api GET /api/tools/catalog --check tools contains '{"name": "browser_tool_set", "user_selectable": true, "usable": true' --quiet --save F27.catalog-docker-runtime/explicit-browser
  ```
