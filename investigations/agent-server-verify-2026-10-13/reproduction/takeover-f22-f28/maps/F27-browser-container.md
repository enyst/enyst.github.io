# F27 Playwright override in a Chromium-free container

## Driving it with control-agent-server
Preconditions:
```sh
control-agent-server doctor
QA_CONTAINER=$(cat "$AGENT_SERVER_VERIFY_RUN/fixtures/container-name.txt")
control-agent-server exec --expect-output QA_BROWSER_PATH_EXISTS --save F27.browser-playwright-path/layout -- docker --host=unix:///var/run/docker.sock exec "$QA_CONTAINER" /agent-server/.venv/bin/python -c 'import os; from pathlib import Path; p=Path(os.environ["PLAYWRIGHT_BROWSERS_PATH"]); assert (p/"chromium-qa/chrome-linux64/chrome").exists(); assert not Path("/usr/bin/chromium").exists(); print("QA_BROWSER_PATH_EXISTS")'
```
- **Home-cache positive control (`F27.browser-probe`).**
  ```sh
  control-agent-server api GET /api/tools/catalog --quiet --check tools contains '{"name": "browser_tool_set", "user_selectable": true, "usable": false' --save F27.browser-probe/before
  control-agent-server exec --expect-output QA_HOME_CACHE_LINKED -- docker --host=unix:///var/run/docker.sock exec "$QA_CONTAINER" /agent-server/.venv/bin/python -c 'from pathlib import Path; p=Path("/tmp/qa-browser-home/.cache"); p.mkdir(parents=True,exist_ok=True); (p/"ms-playwright").symlink_to("/qa-playwright"); print("QA_HOME_CACHE_LINKED")'
  control-agent-server exec --timeout 90 --expect-output "$QA_CONTAINER" -- docker --host=unix:///var/run/docker.sock restart "$QA_CONTAINER"
  for _ in $(seq 90); do if control-agent-server api GET /alive --expect 200 --quiet >/dev/null; then break; fi; sleep 1; done
  control-agent-server api GET /alive --expect 200 --quiet
  control-agent-server api GET /api/tools/catalog --quiet --check tools contains '{"name": "browser_tool_set", "user_selectable": true, "usable": true' --save F27.browser-probe/home-control
  ```
- **Playwright override (`F27.browser-playwright-path`), known bug.**
  ```sh
  control-agent-server exec --expect-output QA_HOME_CACHE_REMOVED -- docker --host=unix:///var/run/docker.sock exec "$QA_CONTAINER" /agent-server/.venv/bin/python -c 'from pathlib import Path; Path("/tmp/qa-browser-home/.cache/ms-playwright").unlink(); print("QA_HOME_CACHE_REMOVED")'
  control-agent-server exec --timeout 90 --expect-output "$QA_CONTAINER" -- docker --host=unix:///var/run/docker.sock restart "$QA_CONTAINER"
  for _ in $(seq 90); do if control-agent-server api GET /alive --expect 200 --quiet >/dev/null; then break; fi; sleep 1; done
  control-agent-server api GET /alive --expect 200 --quiet
  control-agent-server api GET /api/tools/catalog --quiet --check tools contains '{"name": "terminal", "user_selectable": true, "usable": true'
  control-agent-server api GET /api/tools/catalog --quiet --check tools contains '{"name": "browser_tool_set", "user_selectable": true, "usable": true' --save F27.browser-playwright-path/catalog  # bug
  ```
