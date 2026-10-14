Isolated harness copy; target checkout remains acca181af1f353975965bcf6486e1d0a58f444c0.

F12.docker-runtime: removed unconditional blocked label; configured target-built image qa-agent-server:acca181a and cleanup trap.
F12.docker-runtime-contract: explicitly selected a missing Unix socket through DOCKER_HOST to prove the no-daemon error path on this Docker-capable host.
F09.switch-llm-mid-run and mid-run-get: create with --no-run, open socket and await full_state before POST /run, because initial recipe starts model before subscription and can lose first ActionEvent. Same real DeepSeek prompt and assertions.
F08/F14 doctor calls: retry once after initial required OpenAPI read timeout, to allow warm-cache verification under CPU contention; other required doctor checks remain unchanged. Original transcripts preserve cold timeout.
F12 Docker live expanded assertions: select only own conversation container; inspect safe limits/capabilities/profile; attach child with safely captured session key and assert frozen SHA; archive via real 300-second retention pass; never-health derived image with 2-second startup timeout. Credentials normal-output redaction gap checked without printing credential, then registered as OPENHANDS_API_KEY for masked evidence.
F10.restart-persist: added missing transitive dependencies F10.fork-independent (QA_F10_ONLY_FORK expected) and F10.navigate-empty (empty HEAD expected); warm doctor retry for initial CPU-contention OpenAPI timeout.
F14.restart: added upload-download and scoped-transfer prerequisites, because standalone replay expects both overwritten global blob and scoped uploaded blob.
Docker live image selected qa-agent-server:acca181a-local-pricing: frozen source + locked host venv, config-only LITELLM_LOCAL_MODEL_COST_MAP=True to avoid child import-time HTTPS without CA mount passthrough. Canonical published Dockerfile packaging remains resource blocked separately.
F09.switch-llm-acp-refused and F13.scoped-bad-id: accumulate marked assertion failures, save each route exchange, and fail at final # bug check; both API cases now execute despite the first expected failure.
All remaining isolated selected replays now begin preconditions with doctor plus one warm retry, since standard map run itself does not automatically run doctor. Current F09/F12 first attempts receive explicit live doctor diagnostics separately.
F08 bad-value and F14 directory-upload/init-path: accumulate marked failures so null/boolean, parent-file and scoped export cases run and save exchanges; final # bug check preserves failure classification. Supplementary fresh runs follow original twice-confirmed results.
Corrected added Docker profile arrangement: POST agent-profile returns no id and needs llm_profile_ref, so save offline LLM profile first and obtain minted profile id from GET profile.id. Prior Docker attempts failed arrangement before starting a container, not product behavior. Also assert normal credential field is unmasked and child key authenticates to a guarded inner route.
Further Docker profile arrangement correction: SaveProfileRequest requires {llm:{...}}, confirmed by saved422 detail and F09 canonical recipe; used that wrapper. Both failed Docker-only attempts remain recorded as harness arrangement failures.

Docker layout recovery: the earlier source/venv image puts its entrypoint under
/workspace, which Docker runtime replaces with its conversation workspace mount.
Both corrected attempts failed OCI exec before a child process started. A local
derivative moves unchanged source/venv to /agent-server and selects all four
source packages through PYTHONPATH. Empty-/workspace import proof is saved under
docker/runtime-layout-imports-proof.json before API lifecycle checks. This is
local frozen-source coverage, not canonical Dockerfile packaging verification.
Only this run's computed runtime-owner label is inspected, so unrelated
containers and their environment are excluded. Legacy Docker builder is selected
for these local, network-free image changes because buildx cannot write its
default cache in this sandbox.

Docker ownership recovery: the first moved-layout image still has a root-owned
mode700 virtualenv bin directory. Its default-root empty-workspace import check
passed, but the real runtime UID1000 could not execute Python. Both API attempts
are preserved as image/harness failures. The local-uid derivative applies
chmod -R a+rX only to the public frozen source and dependency artifact. Its
runtime-uid-imports-proof.json explicitly uses UID1000, an empty /workspace
mount, and the configured memory/CPU/PID/capability restrictions before the
new API attempts. Product files in the shared checkout remain unchanged.

Docker vfs timing recovery: real container provisioning took83–86 seconds on
two fresh successful creates. The default30-second CLI transport deadline was
too short and cleanup interrupted the still-running Docker client. Create and
reprovision requests now allow180 seconds. The never-health request's outer
bound allows120 seconds for vfs copying plus the unchanged configured2-second
health wait; its logged health-deadline failure is checked explicitly.

Docker exposure-route drift: frozen source intentionally registers persisted
event reads on the outer catalog before the runtime proxy. Events/search with
the exposure header therefore returns200 (empty history in both fresh probes).
The copied recipe records that control, then checks422 on a proxied scoped bash
read, which actually reaches proxy_http's explicit header refusal. No product
behavior is changed or silently accepted.
