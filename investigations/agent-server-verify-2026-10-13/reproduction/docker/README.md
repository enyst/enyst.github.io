# Frozen-source verification runtime

These local images support the Docker capability probes; they do not certify production Docker/PyInstaller packaging.
Build the frozen checkout first with `make build`. Use that checkout as the source context and its built `.venv` as named context `qa_venv`. The initial image assumes the interpreter at `/usr/bin/python3.13`; verify copied-venv interpreter compatibility on your host. Supply your own trusted CA bundle via the `system_ca` build secret; no trust bundle or credential is published here.

Build order and image tags used:

1. `Dockerfile-runtime` → `qa-agent-server:acca181a` (named context `qa_venv` and CA secret required).
2. `local-pricing.Dockerfile` → `qa-agent-server:acca181a-local-pricing`.
3. `runtime-layout.Dockerfile` → `qa-agent-server:acca181a-local-layout`.
4. `runtime-uid.Dockerfile` → `qa-agent-server:acca181a-local-uid`.
5. `nohealth-uid.Dockerfile` → `qa-agent-server:acca181a-local-uid-nohealth` for the controlled never-health startup branch.

The final layout moves editable public source outside the mounted conversation workspace and permits UID1000 traversal/read/execute. The bundled-price setting avoids a remote price-table lookup at import time. Before driving probes, repeat the UID1000 empty-workspace import proof and verify all four package versions and `OPENHANDS_BUILD_GIT_SHA`. The saved proof JSON records the image used in this audit. The first two layouts were invalid runtime arrangements, not product failures.
