# F22–F28 confirmation and ordinary-branch supplements

Product code and the shared repository CLI are unchanged. `run-map.py` loads the
original CLI module and points only its feature-map directory at these preserved
recipe copies. The final triage and proof index identify the exact fresh run and
marked assertion for every counted feature. A valid fresh primary plus one new
independent fresh confirmation is used where the primary had already reached the
correct marker; this avoids repeating proven model turns unnecessarily.

The copied F22 ACP/corrupt-settings recipes explicitly arrange their undeclared
active-profile prerequisite. The store-timeout supplement retains its 503/error
checks and records HTTP elapsed time, excluding CLI startup from the obsolete
shell upper bound. Its DELETE and post-timeout recovery branches pass.

The F27 browser config supplement uses the real host Chromium installation;
unrelated home-cache symlink requirements are removed. Default tools, disabled
catalog, and Docker-runtime catalog branches pass. Server-info and built-in-agent
catalog disagreements reproduce on the primary and the fresh supplement.

`browser_container.py` drives two independently created containers using the
already built `qa-agent-server:acca181a-local-layout` image. Each `/server_info`
reports the target checkout SHA. The real Chromium binary is mounted read-only
solely under a Playwright path. The probe fails to discover that configured path,
while a HOME cache link to the same binary is a successful control. Explicit
published ports remain stable across restarts. Earlier startup/ephemeral-port
attempts are preserved as harness diagnostics and excluded from confirmations.
Only binary discovery/catalog usability is asserted; browser navigation is not.
Both containers are removed and their attached runs stopped.

The focused F28 core fixture proves restart persistence, retained approval,
start without re-prepare, uninstall, retained backend data, repeated DELETE,
and explicit data removal. It uses its own install count instead of stale global
counts. An earlier directory check incorrectly used `state ls`, which counts
files; that diagnostic is preserved and replaced by the proper directory check.

Known-bug recipes stop at their first failing assertion. The final triage names
material later assertions that were not reached. Human subscription login is
blocked; no account sign-in is completed. Zombie PID/process-group checks are
kept distinct from the two independently confirmed live backend orphans in F28.

```sh
python /workspace/verification-artifacts/finalize-f22-f28-triage.py
```

The final cleanup audit verifies all 19 owned run ports are closed, no owned
server or registered helper is live, and both browser containers are removed.
Evidence is preserved; candidate public evidence is scanned for the configured
DeepSeek and GitHub credential values without printing those values.
