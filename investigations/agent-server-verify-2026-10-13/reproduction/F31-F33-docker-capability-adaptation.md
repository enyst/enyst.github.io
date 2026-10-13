# F31/F33 Docker capability adaptation

The frozen map marks F31.storage-retention and F33.workspace-runtime-lifecycle blocked solely because its original verification machines lacked Docker. This session has an isolated local Docker daemon. The copy enables those two markers and drives the same frozen source SHA using a source verification image; it does not change server/SDK source or claim canonical published image packaging verification.

The original image under /workspace failed when a conversation workspace mount hid editable source. The first image under /agent-server imported successfully as root, but runtime UID1000 could not execute its Python interpreter. These are source-image preparation failures, retained as environment/harness evidence, not product failures. A permission-compatible image must pass an empty workspace mount and UID1000 import validation before the capability probes run.

The F33 probe uses the real SDK RemoteWorkspace with a scoped runtime conversation ID, retrieves a nonempty worker key distinct from the server key without printing it, calls release_runtime(), and verifies that execution resources stop while history and event count stay readable. The returned key is registered as OPENHANDS_API_KEY within the probe before any later activity.

The F31 probe creates two private Docker servers: one with short storage retention and one with a 1% filesystem disk budget. It runs the real 300-second maintenance loop, verifies the archive marker and deleted runtime directory, preserved events, 410 for run/message/reprovision, and disk-budget removal of gitignored node_modules and .venv directories while tracked and untracked files remain. All paths belong to the freshly launched private runs. A finally block stops only those owned servers. No sleeps alter product timing and no maintenance method is mocked or invoked directly.

Probe source: scripts/f29-f34-docker-probe.py. Original primary outputs and blocked marker remain in F31.json/F33.json; supplemental reports record the actual adapted checks.

The validated image used for probes is qa-agent-server:acca181a-local-uid (0741efd9d276). UID1000 validation with empty /workspace is saved in docker/runtime-uid-imports-proof.json. It grants traversal/read access to public source/dependencies in the local verification image; frozen product source remains unchanged.

Final storage probe passes. A separate observation before owned-server cleanup also verifies archived conversation-scoped bash/start_bash_command and file/download both return the same 410 read-only detail: F31-archived-proxy-routes.json. The real SDK lifecycle probe passes and its owned server is stopped.
