# Agent Server full verification — 13 October 2026 UTC

Full verify-agent-server audit: 130 confirmed defect groups (12 high, 69 medium, 49 low).

Ran the repository's [verify-agent-server skill](https://github.com/enyst/agent-sdk/blob/acca181af1f353975965bcf6486e1d0a58f444c0/.agents/skills/verify-agent-server/SKILL.md) with Codex against **`acca181af1f353975965bcf6486e1d0a58f444c0`**, server/SDK/tools/workspace **1.54.0**, Python 3.13.5, and the current TypeScript client. The product checkout was frozen throughout. The report covers **34 families, 935 unique mapped IDs: 934 active and one retired**.

[Interactive report](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/) · [Narrated recorded highlights](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/video/highlights.mp4) · [All evidence](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence.zip) · [Artifact checksums](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/manifest.json)

The five recorded cases use fresh real API/client executions, plus two independent confirmation runs per defect. The film includes original mathematical explanations, quiet music, observation cues, narration, and English captions. Setup/restart/cleanup cuts are labeled; the 28-second heartbeat stall stays continuous. Full uncut browser recordings and transcripts are retained.

## Scope, counting, and outcome

Latest recorded unique-feature results: **{"blocked": 3, "fail": 3, "pass": 778, "retired": 1, "xfail": 149, "xpass": 1}**. Recipe assertions and reviewed product defects are separate measures. `xfail` means a mapped failure assertion reproduced; ambiguous semantics and recipe drift are excluded from confirmed defect totals. `xpass` means its known-defect marker passed and needs review. Every counted defect group reproduced at its actual assertion on two fresh runs. Groups merge related recipe branches and proven cross-client duplicates where their notes explain the shared cause; low-severity cases are included in the complete report.

The family batches contain **133 groups**. Three proven cross-family duplicates are merged in this aggregate: the two TypeScript event-history cases join their REST server defects, and the start-time secret visibility case joins runtime secret persistence. The aggregate retains every consumer's commands and evidence. The F20, F21 and F22/F23 store-lock regressions remain separate groups because they drive separate Store/router implementations.

The three remaining raw `fail` labels are coverage limits rather than counted defects: F17.noop-write-readonly stopped at its immutable-filesystem prerequisite; F28.backend-stop and F28.status-exit-hang could not establish process absence on this host because PID 1 leaves exited descendants as zombies. Three raw `blocked` labels cover the default-bind namespace prerequisite, OpenVSCode availability, and human subscription login. Live authenticated GitHub repository pagination and filtering passed; its invalid-token 401 branch remains inconclusive because the same fake token also returns200 in a direct provider control through this environment. Two mapped expected failures have ambiguous contract semantics and are excluded; the Node 24 reconnect `xpass` is map/runtime drift. F12/F14 primary JSON output was interrupted by ENOSPC, but their fresh recovery/supplement ledgers cover all mapped IDs.

The full mapped replay and recovery/supplements are documented below, with explicit blocked, ambiguous, and client entry-point limits. Production Docker/PyInstaller packaging, other operating systems, and human OAuth login are outside the completed proof. A frozen-source Docker verification image exercised local runtime paths; it does not certify the production image build.

The map integrity check passed **34 files / 935 IDs**. Route coverage passed **204 routes, 194 owned and driven**, with ten intentional exclusions and no unowned or undriven owned routes.

## DeepSeek and spend

Real DeepSeek Flash conversations exercised tools, profiles, switching, skills, MCP, SDK and gateway consumers. DeepSeek Pro was exercised by real routing/profile checks. Claude Code ACP used **DeepSeek's Anthropic-compatible endpoint with the supplied DeepSeek key**; `haiku` and `sonnet` in ACP statistics are adapter labels, not evidence of Anthropic credentials or Anthropic billing.

Recorded SDK cost estimates are `{"deepseek/deepseek-flash": 0.136002828, "deepseek/deepseek-v4-pro": 0.014378672000000002, "haiku": 0.016939800000000005, "sonnet": 0.323544}` USD. These are incomplete estimates: profile validation, deleted conversations and standalone clients can be absent, and ACP label pricing can differ from the actual provider price. Duplicated fork/state copies were deduplicated. The provider bill was not queried. [Usage scope and data](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/usage.json).

## Environment and harness recovery

The standard multi-stage Docker build filled the 32 GB VFS filesystem at approximately 02:38 UTC. Its 37 task-owned build-cache records reported only 88 MB while physical snapshots consumed about 28 GB. Those exact cache records were removed; existing images and volumes were preserved. Interrupted attempts remain evidence and were excluded from product conclusions. Fresh recovery checks supply their replacement observations.

Cold OpenAPI generation, concurrent imports, PID-1 zombies and brittle shell deadlines caused other setup failures. Copied recipe adaptations record warmup, zombie-aware/subreaper supervision, explicit dependencies, observation windows, and current contract differences. They preserve product expectations and source. The original CLI suite reported **36 passed / 3 failed**; the three process-lifecycle tests passed under a child-reaping supervisor, with the zombie limitation recorded. [Original test output](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/skill-tests.log) · [Supervisor check](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/skill-tests-subreaper.log).

Private run state, keys, shell state files and fixtures are excluded from publication. Public exchanges are reviewed, real configured credentials are scrubbed, and transient session/device codes and cookie values are additionally redacted.

## Feature coverage

| Family | Latest unique-ID results |
|---|---|
| F01 | pass: 11 |
| F02 | blocked: 1, pass: 18, xfail: 2 |
| F03 | pass: 22, retired: 1, xfail: 1 |
| F04 | pass: 25, xfail: 7 |
| F05 | pass: 27, xfail: 4 |
| F06 | pass: 23, xfail: 5 |
| F07 | pass: 22, xfail: 2 |
| F08 | pass: 20, xfail: 3 |
| F09 | pass: 19, xfail: 9 |
| F10 | pass: 19, xfail: 6 |
| F11 | pass: 23, xfail: 2 |
| F12 | pass: 27, xfail: 3 |
| F13 | pass: 24, xfail: 5 |
| F14 | pass: 23, xfail: 7 |
| F15 | pass: 23, xfail: 5 |
| F16 | blocked: 1, pass: 22, xfail: 3 |
| F17 | fail: 1, pass: 21, xfail: 2 |
| F18 | pass: 25, xfail: 4 |
| F19 | pass: 25, xfail: 3 |
| F20 | pass: 29, xfail: 6 |
| F21 | pass: 28, xfail: 4 |
| F22 | pass: 19, xfail: 5 |
| F23 | pass: 22, xfail: 5 |
| F24 | blocked: 1, pass: 17, xfail: 2 |
| F25 | pass: 26, xfail: 7 |
| F26 | pass: 21, xfail: 4 |
| F27 | pass: 26, xfail: 5 |
| F28 | fail: 2, pass: 23, xfail: 4 |
| F29 | pass: 23, xfail: 6 |
| F30 | pass: 22, xfail: 4 |
| F31 | pass: 19, xfail: 4 |
| F32 | pass: 24, xfail: 6 |
| F33 | pass: 37, xfail: 6 |
| F34 | pass: 23, xfail: 8, xpass: 1 |

## Confirmed product defects

### High — Rich exception rendering stalls the entire agent server

Features: `F05.run-error-responsive`.

**Expected:** Health and event-count probes remain below 1.5 seconds while a model-provider failure is handled.

**Observed:** A positive-control /alive request took 67 ms; a failure-time probe took 4,512 ms. The second fresh attempt recorded 10,909 ms, while the request before the failure met the 1.5-second threshold.

```sh
control-agent-server map run --file F05 --only F05.run-error,F05.run-error-responsive,F05.unknown-id-pause,F05.run-conflict,F05.pause-running,F05.pause-running-get,F05.pause-running-release,F05.restart-running-graceful,F05.restart-hard-running,F05.pause-running-crash --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-024519-40d0-map-f05`, `20261013-024951-9459-map-f05`.

Evidence: [after.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024519-40d0-map-f05/evidence/F05.run-error-responsive/after.json) · [alive-before.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024519-40d0-map-f05/evidence/F05.run-error-responsive/alive-before.json) · [F05-run-pause-interrupt-02-responsive-while-a-run-fails-f05-run-err.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024519-40d0-map-f05/evidence/map-run/F05-run-pause-interrupt-02-responsive-while-a-run-fails-f05-run-err.json) · [after.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024951-9459-map-f05/evidence/F05.run-error-responsive/after.json) · [alive-before.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024951-9459-map-f05/evidence/F05.run-error-responsive/alive-before.json) · [F05-run-pause-interrupt-02-responsive-while-a-run-fails-f05-run-err.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024951-9459-map-f05/evidence/map-run/F05-run-pause-interrupt-02-responsive-while-a-run-fails-f05-run-err.json).

Default console logger.exception renders a large Rich traceback synchronously on the event loop. LOG_JSON=true or LOG_RICH_TRACEBACKS=false is the documented workaround; production Docker uses JSON logging.

### High — Out-of-order durable frames can make a session cursor lose a message

Features: `F07.live-order`.

**Expected:** The first user message yields durable seq 0,1,2 in order, matching persisted log order.

**Observed:** The live socket emits 0,2,1: last_user_message_id is published before the user message at seq 1.

```sh
control-agent-server map run --file F07 --only F07.live-order,F07.deleted-close --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-025721-700e-map-f07`, `20261013-025834-053c-map-f07`.

Evidence: [order-4b477523-fc4b-41e1-bd20-141a666eb5ce.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025721-700e-map-f07/evidence/F07.live-order/order-4b477523-fc4b-41e1-bd20-141a666eb5ce.json) · [F07-session-socket-01-live-frames-in-seq-order-f07-live-order-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025721-700e-map-f07/evidence/map-run/F07-session-socket-01-live-frames-in-seq-order-f07-live-order-.json) · [order-d06266ef-6639-4e3d-82e9-708fd2dd8bc7.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025834-053c-map-f07/evidence/F07.live-order/order-d06266ef-6639-4e3d-82e9-708fd2dd8bc7.json) · [F07-session-socket-01-live-frames-in-seq-order-f07-live-order-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025834-053c-map-f07/evidence/map-run/F07-session-socket-01-live-frames-in-seq-order-f07-live-order-.json).

A client saving the highest sequence and disconnecting after 2 resumes past the missing message. Replay itself is ordered; the message remains on disk.

### High — Runtime secret updates are not saved

Features: `F08.secrets-visible, F08.secrets-unsaved-restart, F04.create-secrets-get`.

**Expected:** GET immediately reflects an updated runtime secret and the secret survives restart.

**Observed:** GET omits the new secret until another state save; restart before that save loses the credential.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F08 --only F08.secrets-visible,F08.secrets-unsaved-restart --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024737-a894-map-f08`, `20261013-025113-2057-map-f08`, `20261013-024143-6004-map-f04`, `20261013-024259-9a86-map-f04`.

Evidence: [F08-confirmation-security-secrets-01-runtime-secret-visible-to-get-f08-secret.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024737-a894-map-f08/evidence/map-run/F08-confirmation-security-secrets-01-runtime-secret-visible-to-get-f08-secret.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024737-a894-map-f08/evidence/F08.secrets-visible/get.json) · [F08-confirmation-security-secrets-05-unsaved-secret-restart-f08-secrets-unsav.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024737-a894-map-f08/evidence/map-run/F08-confirmation-security-secrets-05-unsaved-secret-restart-f08-secrets-unsav.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024737-a894-map-f08/evidence/F08.secrets-unsaved-restart/get.json) · [F08-confirmation-security-secrets-01-runtime-secret-visible-to-get-f08-secret.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025113-2057-map-f08/evidence/map-run/F08-confirmation-security-secrets-01-runtime-secret-visible-to-get-f08-secret.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025113-2057-map-f08/evidence/F08.secrets-visible/get.json).

Merged: both observations originate from updating the secret registry without triggering a conversation state save. Not filed by this worker: external reporting and publication remain parent-owned. Aggregate merge: F04.create-secrets-get. Constructor and runtime secret updates mutate LocalConversation.update_secrets without triggering a state save.

#### Additional consumer proof: Medium — Start-time secrets disappear from the immediate conversation GET

Features: `F04.create-secrets-get`.

**Expected:** GET immediately lists the start-time StaticSecret that the create response lists, masked.

**Observed:** Create lists QA_F 04_TOKEN; the immediate GET returns an empty secret_sources map.

```sh
control-agent-server map run --file F04 --only F04.create-initial-message-run-false,F04.create-secrets-get,F04.create-secrets-plain,F04.batch-get-limit,F04.patch-whitespace-title,F04.patch-unknown-id,F04.delete-unknown-id --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-024143-6004-map-f04`, `20261013-024259-9a86-map-f04`.

Evidence: [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/F04.create-secrets-get/get.json) · [F04-conversation-lifecycle-06-start-time-secret-visible-to-get-f04-cre.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/map-run/F04-conversation-lifecycle-06-start-time-secret-visible-to-get-f04-cre.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/F04.create-secrets-get/get.json) · [F04-conversation-lifecycle-06-start-time-secret-visible-to-get-f04-cre.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/map-run/F04-conversation-lifecycle-06-start-time-secret-visible-to-get-f04-cre.json).

The secret exists in live memory but is absent from the autosaved base_state snapshot until a later state save.


### High — Fork drops model credentials and cannot continue

Features: `F10.fork-keeps-credentials, F10.fork-run-memory`.

**Expected:** The fork retains encrypted agent and condenser keys and can run with source history.

**Observed:** Fork base_state has no API key; continuing a DeepSeek fork fails authentication.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F10 --only F10.fork-keeps-credentials,F10.fork-run-memory --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024131-0603-map-f10`, `20261013-024315-4f15-map-f10`.

Evidence: [F10-fork-navigate-condense-ask-06-the-fork-keeps-the-model-keys-f10-fork-k.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024131-0603-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-06-the-fork-keeps-the-model-keys-f10-fork-k.json) · [F10-fork-navigate-condense-ask-07-a-fork-runs-with-the-source-s-memory-f10.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024131-0603-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-07-a-fork-runs-with-the-source-s-memory-f10.json) · [auth-errors.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024131-0603-map-f10/evidence/F10.fork-run-memory/auth-errors.json) · [F10-fork-navigate-condense-ask-06-the-fork-keeps-the-model-keys-f10-fork-k.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024315-4f15-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-06-the-fork-keeps-the-model-keys-f10-fork-k.json) · [F10-fork-navigate-condense-ask-07-a-fork-runs-with-the-source-s-memory-f10.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024315-4f15-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-07-a-fork-runs-with-the-source-s-memory-f10.json) · [auth-errors.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024315-4f15-map-f10/evidence/F10.fork-run-memory/auth-errors.json).

Merged: failed continuation follows from the same missing cipher when fork state is saved. Not filed by this worker: external reporting and publication remain parent-owned.

### High — Idle eviction kills a running scoped bash command

Features: `F13.scoped-idle-eviction`.

**Expected:** Running scoped commands keep their conversation loaded and can be stopped normally.

**Observed:** Idle eviction kills the active scoped command and leaves the retained stream without any terminal BashOutput through shutdown 19–20 seconds after eviction. Consumers expecting an exit code may wait until their own timeout.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F13 --only F13.scoped-idle-eviction --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031029-c530-map-f13`, `20261013-031229-ccc9-map-f13`.

Evidence: [F13-bash-06-idle-eviction-kills-a-running-command-f1.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/map-run/F13-bash-06-idle-eviction-kills-a-running-command-f1.json) · [F13-bash-06-idle-eviction-kills-a-running-command-f1.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/map-run/F13-bash-06-idle-eviction-kills-a-running-command-f1.json) · [f13-idle-eviction-terminal-evidence.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/reproduction/f13-idle-eviction-terminal-evidence.json).

Not filed by this worker: external reporting and publication remain parent-owned. The independent terminal-event evidence checks both retained owned BashCommand streams. No actual client poller wait, rehydration, or later stop API was exercised. See f13-idle-eviction-terminal-evidence.json.

### High — Failed overwrite destroys the previous file

Features: `F14.upload-atomic`.

**Expected:** Mid-write EFBIG failure leaves the previous uploaded file intact.

**Observed:** The existing target is truncated and replaced by 500000 partial bytes despite 500.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F14 --only F14.upload-atomic --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024217-af4c-map-f14`, `20261013-024649-c36e-map-f14`.

Evidence: [F14-files-04-failed-overwrite-f14-upload-atomic-known.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/map-run/F14-files-04-failed-overwrite-f14-upload-atomic-known.json) · [F14-files-04-failed-overwrite-f14-upload-atomic-known.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/map-run/F14-files-04-failed-overwrite-f14-upload-atomic-known.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### High — An unrelated secret write after cipher rotation destroys existing secret ciphertext

Features: `F18.secret-key-rotation`.

**Expected:** When ciphertext cannot be decrypted with the current cipher key, a write must reject the operation or preserve the old ciphertext so restoring the old key recovers the existing values.

**Observed:** In both runs rotating the cipher key and restoring it without a write recovered the original secret and LLM key. After another rotation, PUT of an unrelated secret returned 200 and an unrelated misc-settings PATCH also returned 200. Once the original key was restored, the saved state assertion showed custom_secrets.QA_F18_TOKEN.secret=null instead of its previous Fernet ciphertext.

```sh
control-agent-server map run --file F18 --only F18.secret-key-rotation --fresh --repeat 2 --record --checkout /workspace/agent-sdk-verify
```

Fresh confirmation runs: `20261013-024700-3f62-map-f18`, `20261013-025117-43f0-map-f18`.

Evidence: [read-under-new-key.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.secret-key-rotation/read-under-new-key.json) · [settings-under-new-key.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.secret-key-rotation/settings-under-new-key.json) · [control-rotated-back.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.secret-key-rotation/control-rotated-back.json) · [put-under-new-key.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.secret-key-rotation/put-under-new-key.json) · [patch-under-new-key.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.secret-key-rotation/patch-under-new-key.json) · [F18-settings-and-secrets-07-cipher-key-rotation-f18-secret-key-rotat.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/map-run/F18-settings-and-secrets-07-cipher-key-rotation-f18-secret-key-rotat.json).

The decisive post-restore persisted-null assertion is inside the map-run transcript, not a separate HTTP exchange. Each recipe stops at that first failing secrets.json assertion. The later settings.json ciphertext assertion and final post-restore GET checks were not executed, so permanent LLM-key loss and final HTTP reads are not claimed as independently confirmed here. Not filed: this task is read-only saved-evidence extraction; no issue lookup or external action was performed. Both fresh runs used checkout SHA acca181af1f353975965bcf6486e1d0a58f444c0. Reproduction commands are provided for review and were not rerun during extraction.

### High — Waiting for the LLM profile store lock stalls unrelated server requests

Features: `F20.store-busy-responsive`.

**Expected:** GET /alive must answer within 3000ms while a profile save waits for the store lock, as it does with no lock.

**Observed:** GET /alive returned 200 only after 25,771ms in the initial run and 23,523ms in the clean run. In both runs the waiting save returned 503 after approximately 30 seconds, no profile was created, and the exact timing assertion failed.

```sh
control-agent-server map run --file F20 --only F20.store-busy-responsive --fresh --repeat 2 --record --keep-going --checkout /workspace/agent-sdk-verify
```

Fresh confirmation runs: `20261013-021919-4f6c-map-f20`, `20261013-024525-b13b-map-f20`.

Evidence: [alive.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021919-4f6c-map-f20/evidence/F20.store-busy-responsive/alive.json) · [busy-save.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021919-4f6c-map-f20/fixtures/qa-f20/busy-save.json) · [F20-llm-profiles-11-lock-wait-blocks-the-server-f20-store-bu.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021919-4f6c-map-f20/evidence/map-run/F20-llm-profiles-11-lock-wait-blocks-the-server-f20-store-bu.json) · [alive.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024525-b13b-map-f20/evidence/F20.store-busy-responsive/alive.json) · [busy-save.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024525-b13b-map-f20/fixtures/qa-f20/busy-save.json) · [F20-llm-profiles-11-lock-wait-blocks-the-server-f20-store-bu.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024525-b13b-map-f20/evidence/map-run/F20-llm-profiles-11-lock-wait-blocks-the-server-f20-store-bu.json).

Already independently confirmed twice and present in triage-f15-f21.json. Initial evidence occurred before the later ENOSPC interruption and has matching saved controls and failed assertion. Related F21 busy-lock case is listed separately pending its own repeated confirmation. No rerun or shared triage mutation was performed during extraction.

### High — Waiting for the agent-profile store lock stalls unrelated server requests

Features: `F21.busy-blocks-server`.

**Expected:** GET /alive must answer within 2000ms while an agent-profile request waits for the store lock.

**Observed:** No-lock /alive controls pass, but while the profile request waits for its store lock, /alive returns 200 only after 25,097ms and 25,063ms in the two fresh targeted runs.

```sh
control-agent-server map run --file F21 --only F21.save-create,F21.acp-kind,F21.busy-blocks-server --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-030758-8dc4-map-f21`, `20261013-030902-92d4-map-f21`.

Evidence: [F21-agent-profiles-03-lock-wait-stalls-the-server-f21-busy-blo.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030758-8dc4-map-f21/evidence/map-run/F21-agent-profiles-03-lock-wait-stalls-the-server-f21-busy-blo.json) · [alive.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030758-8dc4-map-f21/evidence/F21.busy-blocks-server/alive.json) · [F21-agent-profiles-03-lock-wait-stalls-the-server-f21-busy-blo.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030902-92d4-map-f21/evidence/map-run/F21-agent-profiles-03-lock-wait-stalls-the-server-f21-busy-blo.json) · [alive.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030902-92d4-map-f21/evidence/F21.busy-blocks-server/alive.json).

This matches the already-confirmed F20 LLM-profile-store stall family, but this agent-profile variant currently has only one clean-run proof. The recipe stops at the timing assertion; shell exit releases the held lock. Two further fresh targeted confirmations now reproduce the exact marked failures. Not filed: read-only evidence extraction performed no issue lookup or external action.

### High — Synchronous profile-store locks freeze the server

Features: `F22.store-busy-responsive, F23.store-busy-responsive`.

**Expected:** GET /alive responds within 3000 ms while a meta-profile save waits on the store lock.

**Observed:** F22 meta-profile save lock waits stall /alive for 29,087 and 27,731 ms; F23 provider-connection list lock waits also stall /alive while idle controls remain fast.

```sh
control-agent-server map run --file F22 --only F22.save-classes,F22.store-busy-responsive --fresh --repeat 2 --record --keep-going
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F23-llm-catalog-and-connections.md --only F23.models-no-bedrock,F23.conn-create,F23.conn-create-blank-key,F23.conn-patch-blank-key,F23.validate-linked-draft,F23.store-busy-responsive --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-022801-881f-f22-lock-confirm-1`, `20261013-023058-b5d0-f22-lock-confirm-2`, `20261013-024155-0956-map-f23`, `20261013-034323-e6ea-map-f23`.

Evidence: [F22-lock-confirm-1-doctor-after.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/family-results/F22-lock-confirm-1-doctor-after.json) · [F22-lock-confirm-1-doctor-before.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/family-results/F22-lock-confirm-1-doctor-before.json) · [F22-lock-confirm-2-doctor-after.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/family-results/F22-lock-confirm-2-doctor-after.json) · [F22-lock-confirm-2-doctor-before-retry.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/family-results/F22-lock-confirm-2-doctor-before-retry.json) · [alive-idle.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022801-881f-f22-lock-confirm-1/evidence/F22.store-busy-responsive/alive-idle.json) · [alive.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022801-881f-f22-lock-confirm-1/evidence/F22.store-busy-responsive/alive.json).

The async meta-profile router calls the synchronous file-locked MetaProfileStore on the event loop. The same root cause may be grouped with F20/F23 store lock stalls, if each endpoint's proof and counting convention are retained. Both clean confirmations use explicit fresh launch, successful doctor before map driving, doctor after recovery, and targeted stop. Second run required an initial OpenAPI warmup retry before driving. F22.save-classes supplies the undeclared store-directory prerequisite. No model inference occurs in the selected recipe. Grouped F22/F23 synchronous store operations on async request paths. Each endpoint has its own two fresh proofs. Root may group the separately verified F20 route with this mechanism, preserving every endpoint proof.

### High — A live backend survives the server crash while status says stopped

Features: `F28.hard-restart-orphan`.

**Expected:** No backend process of the dead server survives its hard restart.

**Observed:** Both fresh runs report stopped with null pid after restart while pgrep of the run-private artifact path still finds the live backend.

```sh
control-agent-server map run --file F28 --only F28.hard-restart-orphan --fresh --repeat 2 --record
```

Fresh confirmation runs: `20261013-025047-4da6-map-f28`, `20261013-025217-c43a-map-f28`.

Evidence: [status-after-crash.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025047-4da6-map-f28/evidence/F28.hard-restart-orphan/status-after-crash.json) · [F28-canvas-extensions-04-backend-outlives-a-crash-f28-hard-restar.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025047-4da6-map-f28/evidence/map-run/F28-canvas-extensions-04-backend-outlives-a-crash-f28-hard-restar.json) · [status-after-crash.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025217-c43a-map-f28/evidence/F28.hard-restart-orphan/status-after-crash.json) · [F28-canvas-extensions-04-backend-outlives-a-crash-f28-hard-restar.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025217-c43a-map-f28/evidence/map-run/F28-canvas-extensions-04-backend-outlives-a-crash-f28-hard-restar.json).

The backend starts a new session and survives SIGKILL with parent pid 1. Matching the artifact command path excludes an empty-cmdline zombie; this is separate from the unreaped-child observation limit in backend-stop/status-exit-hang. Automatic targeted CLI stop reaps owned orphans.

### High — Second-server takeover overwrites newer conversation metadata

Features: `F31.takeover-keeps-metadata`.

**Expected:** The title last persisted by the first owner should survive takeover.

**Observed:** The second server rewrites meta.json with its startup catalog's older title, losing the owner's later rename.

```sh
/workspace/verification-artifacts/harness-f29-f34/.agents/skills/verify-agent-server/scripts/control-agent-server map run --file F31 --only F31.takeover-keeps-metadata --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024316-e532-map-f31`, `20261013-025937-a7eb-map-f31`.

Evidence: [F31-persistence-and-limits-01-takeover-keeps-newer-metadata-f31-takeov.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024316-e532-map-f31/evidence/map-run/F31-persistence-and-limits-01-takeover-keeps-newer-metadata-f31-takeov.json) · [F31-persistence-and-limits-01-takeover-keeps-newer-metadata-f31-takeov.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025937-a7eb-map-f31/evidence/map-run/F31-persistence-and-limits-01-takeover-keeps-newer-metadata-f31-takeov.json).

[
  "Isolated copied recipe adjusts only exited-zombie setup observation; frozen product source and bug assertion unchanged. See F31-zombie-adaptation.md."
]

### Medium — Workspace session cookie drops the server URL prefix

Features: `F02.workspace-cookie-root-path`.

**Expected:** A cookie minted through a prefixed server URL authenticates the prefixed workspace file URL.

**Observed:** Cookie Path is <redacted:session-cookie> regardless of root_path. The browser-like cookie jar gets 401 at /qa-f02-prefix<redacted:session-cookie>/{id}/workspace/qa-f02.html; the same valid cookie gets 200 at the unprefixed URL.

```sh
control-agent-server map run --file F02 --only F02.workspace-cookie-root-path,F02.workspace-session-ipv6-loopback --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-022326-2081-map-f02`, `20261013-022650-a777-map-f02`.

Evidence: [mint.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022430-59fc-f02-prefix/evidence/F02.workspace-cookie-root-path/mint.json) · [file-with-cookie.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022430-59fc-f02-prefix/evidence/F02.workspace-cookie-root-path/file-with-cookie.json) · [mint.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022749-a380-f02-prefix/evidence/F02.workspace-cookie-root-path/mint.json) · [file-with-cookie.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022749-a380-f02-prefix/evidence/F02.workspace-cookie-root-path/file-with-cookie.json).

Known map bug reproduced at the marked assertion in both fresh attempts. Header-authenticated prefixed URL and cookie-authenticated unprefixed URL are successful controls. No model needed. Source: auth_router.py cookie Path ignores root_path.

### Medium — IPv6 loopback workspace cookies omit Secure and Partitioned

Features: `F02.workspace-session-ipv6-loopback`.

**Expected:** Host [::1]:8000 receives SameSite=none; Secure; Partitioned, matching localhost and 127.0.0.1.

**Observed:** The IPv6 Host request returns 204 with SameSite=none but omits Secure and Partitioned, so browsers reject the cookie. The two IPv4/localhost controls include both flags.

```sh
control-agent-server map run --file F02 --only F02.workspace-cookie-root-path,F02.workspace-session-ipv6-loopback --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-022326-2081-map-f02`, `20261013-022650-a777-map-f02`.

Evidence: [ipv6-host.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022326-2081-map-f02/evidence/F02.workspace-session-ipv6-loopback/ipv6-host.json) · [ipv6-host.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022650-a777-map-f02/evidence/F02.workspace-session-ipv6-loopback/ipv6-host.json).

Known map bug reproduced twice. The test changes the HTTP Host header to IPv6 loopback while reaching the same loopback server; it does not claim an IPv6 network bind test. Source: auth_router.py:42-65 splits request.url.hostname on ':' before loopback matching.

### Medium — Deferred init accepts CORS origins but leaves the boot allowlist unchanged

Features: `F03.init-delivered-cors-origins`.

**Expected:** The allow_cors_origins delivered by successful POST /api/init authorizes that origin on a CORS preflight.

**Observed:** The delivered https://qa-f03.example gets 400 Disallowed CORS origin and no Access-Control-Allow-Origin. Localhost control gets200; an undelivered origin also gets400.

```sh
control-agent-server map run --file F03 --only F03.init-success,F03.init-delivered-cors-origins --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-023017-4c4d-map-f03`, `20261013-023328-d486-map-f03`.

Evidence: [preflight.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-023017-4c4d-map-f03/evidence/F03.init-delivered-cors-origins/preflight.json) · [preflight.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-023328-d486-map-f03/evidence/F03.init-delivered-cors-origins/preflight.json).

Known map bug at marked assertion in both fresh attempts. CORSDispatcher captures config.allow_cors_origins when create_app runs; successful init updates the config but does not rebuild middleware.

### Medium — Conversation create executes an initial message with run=false

Features: `F04.create-initial-message-run-false`.

**Expected:** Persist the initial message and remain idle with no model run when initial_message.run is false.

**Observed:** The false request runs to finished on the controlled provider just like the true control.

```sh
control-agent-server map run --file F04 --only F04.create-initial-message-run-false,F04.create-secrets-get,F04.create-secrets-plain,F04.batch-get-limit,F04.patch-whitespace-title,F04.patch-unknown-id,F04.delete-unknown-id --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-024143-6004-map-f04`, `20261013-024259-9a86-map-f04`.

Evidence: [start.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/F04.create-initial-message-run-false/start.json) · [F04-conversation-lifecycle-02-initial-message-run-false-f04-create-ini.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/map-run/F04-conversation-lifecycle-02-initial-message-run-false-f04-create-ini.json) · [start.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/F04.create-initial-message-run-false/start.json) · [F04-conversation-lifecycle-02-initial-message-run-false-f04-create-ini.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/map-run/F04-conversation-lifecycle-02-initial-message-run-false-f04-create-ini.json) · [observed-actions.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032709-376d-map-f04/evidence/F04.create-initial-message-run-false/observed-actions.json) · [observed-status.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032709-376d-map-f04/evidence/F04.create-initial-message-run-false/observed-status.json).

The live recipe checks the persisted user message, then observes execution starting/finishing. The create schema advertises run=false, but _start_conversation unconditionally calls run(). Supplemental GET reports finished and exactly one ActionEvent on both fresh attempts.

### Medium — A mid-call pause is invisible to GET and lost on crash recovery

Features: `F05.pause-running-get, F05.pause-running-crash`.

**Expected:** GET agrees with the accepted paused state; after SIGKILL/restart the accepted pause remains paused.

**Observed:** During an accepted mid-call pause, status search and PauseEvent say paused, but GET and base_state.json say running. After SIGKILL, lease expiry, and restart, both PauseEvents remain but GET reports error.

```sh
control-agent-server map run --file F05 --only F05.run-error,F05.run-error-responsive,F05.unknown-id-pause,F05.run-conflict,F05.pause-running,F05.pause-running-get,F05.pause-running-release,F05.restart-running-graceful,F05.restart-hard-running,F05.pause-running-crash --fresh --repeat 2 --record --keep-going --timeout 420
.venv/bin/python /workspace/verification-artifacts/adapted-f05/run-adapted-f05.py map run --file F05 --only F05.restart-running-graceful,F05.restart-hard-running,F05.pause-running-crash --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-024519-40d0-map-f05`, `20261013-024951-9459-map-f05`, `20261013-032311-dcf8-map-f05`, `20261013-032700-5284-map-f05`.

Evidence: [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024519-40d0-map-f05/evidence/F05.pause-running-get/get.json) · [F05-run-pause-interrupt-06-get-after-a-mid-call-pause-f05-pause-run.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024519-40d0-map-f05/evidence/map-run/F05-run-pause-interrupt-06-get-after-a-mid-call-pause-f05-pause-run.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024951-9459-map-f05/evidence/F05.pause-running-get/get.json) · [F05-run-pause-interrupt-06-get-after-a-mid-call-pause-f05-pause-run.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024951-9459-map-f05/evidence/map-run/F05-run-pause-interrupt-06-get-after-a-mid-call-pause-f05-pause-run.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032311-dcf8-map-f05/evidence/F05.pause-running-crash/get.json) · [lease-expiry.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032311-dcf8-map-f05/evidence/F05.pause-running-crash/lease-expiry.json).

One root cause across GET, disk snapshot, and crash recovery: autosave is deferred while model I/O holds save_depth open. In this PID-1 container the killed owner remains a zombie; the adaptation verifies that state, records the remaining owner-lease TTL, waits for expiry, and restarts before the target assertion. Instantaneous dead-owner recovery is not certified.

### Medium — Documented short event kinds silently return empty results

Features: `F06.search-kind-short, F34.events-search-kind`.

**Expected:** kind=MessageEvent returns the two user messages, matching their wire kind and the TypeScript client contract.

**Observed:** The fully qualified MessageEvent filter finds two messages; the documented short kind returns an empty search and count 0. Both routes independently reproduce twice.

```sh
control-agent-server map run --file F06 --only F06.send-no-run,F06.search-kind-short,F06.get-one,F06.unknown-event,F06.send-non-user-role,F06.ws-delete-close,F06.search-timestamp-order --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-025406-9fbb-map-f06`, `20261013-025528-20b8-map-f06`, `20261013-024756-c705-map-f34`, `20261013-025335-6a42-map-f34`.

Evidence: [short-name.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025406-9fbb-map-f06/evidence/F06.search-kind-short/short-name.json) · [F06-conversation-events-02-short-kind-names-f06-search-kind-short-k.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025406-9fbb-map-f06/evidence/map-run/F06-conversation-events-02-short-kind-names-f06-search-kind-short-k.json) · [short-name.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025528-20b8-map-f06/evidence/F06.search-kind-short/short-name.json) · [F06-conversation-events-02-short-kind-names-f06-search-kind-short-k.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025528-20b8-map-f06/evidence/map-run/F06-conversation-events-02-short-kind-names-f06-search-kind-short-k.json) · [fqn-control.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032934-9891-map-f06/evidence/F06.search-kind-short-count/fqn-control.json) · [short-count.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032934-9891-map-f06/evidence/F06.search-kind-short-count/short-count.json).

The service compares module.ClassName rather than the documented wire kind; TypeScript clients following the documentation silently lose history. Aggregate merge: F34.events-search-kind. The TypeScript search drives the same server short-kind versus module.ClassName comparison.

#### Additional consumer proof: Medium — TypeScript documented short event kinds find no events

Features: `F34.events-search-kind`.

**Expected:** MessageEvent should find the same queued user message as the fully qualified kind.

**Observed:** The qualified kind finds one; the short name returns no items and count zero. Same server root cause as F06.search-kind-short.

```sh
control-agent-server map run --file F34 --only F34.events-search-kind --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024756-c705-map-f34`, `20261013-025335-6a42-map-f34`.

Evidence: [F34-typescript-client-04-short-event-kinds-f34-events-search-kind.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024756-c705-map-f34/evidence/map-run/F34-typescript-client-04-short-event-kinds-f34-events-search-kind.json) · [F34-typescript-client-04-short-event-kinds-f34-events-search-kind.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025335-6a42-map-f34/evidence/map-run/F34-typescript-client-04-short-event-kinds-f34-events-search-kind.json).

[
  "Same server defect as F06.search-kind-short; cross-family aggregate must deduplicate."
]


### Medium — Timestamp-based event resume skips delayed stats updates

Features: `F06.search-timestamp-order`.

**Expected:** A timestamp cut at an observation keeps that observation and every later-listed event in REST and WebSocket replay.

**Observed:** The marked REST count is lower than the number of events listed from the observation onward.

```sh
control-agent-server map run --file F06 --only F06.send-no-run,F06.search-kind-short,F06.get-one,F06.unknown-event,F06.send-non-user-role,F06.ws-delete-close,F06.search-timestamp-order --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-025406-9fbb-map-f06`, `20261013-025528-20b8-map-f06`.

Evidence: [count-since-observation.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025406-9fbb-map-f06/evidence/F06.search-timestamp-order/count-since-observation.json) · [F06-conversation-events-08-log-order-is-timestamp-order-f06-search-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025406-9fbb-map-f06/evidence/map-run/F06-conversation-events-08-log-order-is-timestamp-order-f06-search-.json) · [count-since-observation.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025528-20b8-map-f06/evidence/F06.search-timestamp-order/count-since-observation.json) · [F06-conversation-events-08-log-order-is-timestamp-order-f06-search-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025528-20b8-map-f06/evidence/map-run/F06-conversation-events-08-log-order-is-timestamp-order-f06-search-.json) · [all.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032934-9891-map-f06/evidence/F06.search-timestamp-order-sorted/all.json) · [socket.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032934-9891-map-f06/evidence/F06.search-timestamp-replay/socket.json).

Stats updates are timestamped at model response time, then appended after tool observations; both REST count and legacy socket replay skip a subsequently appended stats event. Replay and unsorted-timestamp assertions separately reproduced twice using real DeepSeek file-editor turns.

### Medium — One absent event crashes get-one and batch history reads

Features: `F06.unknown-event, F34.events-unknown-id`.

**Expected:** Get-one returns 404 for a missing ID; a mixed batch preserves known events and returns null for the missing slot.

**Observed:** Get-one returns 500 for an absent event ID; a batch containing one valid event and one absent event also returns 500 instead of [event, null]. Both branches reproduce twice.

```sh
control-agent-server map run --file F06 --only F06.send-no-run,F06.search-kind-short,F06.get-one,F06.unknown-event,F06.send-non-user-role,F06.ws-delete-close,F06.search-timestamp-order --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-025406-9fbb-map-f06`, `20261013-025528-20b8-map-f06`, `20261013-024756-c705-map-f34`, `20261013-025335-6a42-map-f34`.

Evidence: [get-one.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025406-9fbb-map-f06/evidence/F06.unknown-event/get-one.json) · [F06-conversation-events-04-unknown-event-id-f06-unknown-event-known.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025406-9fbb-map-f06/evidence/map-run/F06-conversation-events-04-unknown-event-id-f06-unknown-event-known.json) · [get-one.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025528-20b8-map-f06/evidence/F06.unknown-event/get-one.json) · [F06-conversation-events-04-unknown-event-id-f06-unknown-event-known.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025528-20b8-map-f06/evidence/map-run/F06-conversation-events-04-unknown-event-id-f06-unknown-event-known.json) · [known-control.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032934-9891-map-f06/evidence/F06.unknown-event-batch/known-control.json) · [mixed.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032934-9891-map-f06/evidence/F06.unknown-event-batch/mixed.json).

EventLog.get_index raises KeyError before the router can return 404/null; an absent item aborts the whole batch. Aggregate merge: F34.events-unknown-id. The TypeScript lookup drives the same EventLog.get_index missing-ID failure as the REST consumer.

#### Additional consumer proof: Low — TypeScript event lookup receives 500 for a missing event

Features: `F34.events-unknown-id`.

**Expected:** A missing event should reject with 404 and batch lookup should return null in that slot.

**Observed:** Single and batch calls both reject with 500 Unknown event_id. This is the server defect also exercised by F06.unknown-event.

```sh
control-agent-server map run --file F34 --only F34.events-unknown-id --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024756-c705-map-f34`, `20261013-025335-6a42-map-f34`.

Evidence: [F34-typescript-client-03-unknown-event-id-f34-events-unknown-id-k.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024756-c705-map-f34/evidence/map-run/F34-typescript-client-03-unknown-event-id-f34-events-unknown-id-k.json) · [F34-typescript-client-03-unknown-event-id-f34-events-unknown-id-k.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025335-6a42-map-f34/evidence/map-run/F34-typescript-client-03-unknown-event-id-f34-events-unknown-id-k.json).

[
  "Same server defect as F06.unknown-event; cross-family aggregate must deduplicate."
]


### Medium — Deleting a conversation leaves its event/session sockets open

Features: `F06.ws-delete-close, F07.deleted-close`.

**Expected:** DELETE closes already subscribed sockets before answering; subsequent reads are 404 and new sockets 4004.

**Observed:** DELETE succeeds, REST returns 404 and a new socket 4004, but the existing capture remains open with close=null.

```sh
control-agent-server map run --file F06 --only F06.send-no-run,F06.search-kind-short,F06.get-one,F06.unknown-event,F06.send-non-user-role,F06.ws-delete-close,F06.search-timestamp-order --fresh --repeat 2 --record --keep-going --timeout 420
control-agent-server map run --file F07 --only F07.live-order,F07.deleted-close --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-025406-9fbb-map-f06`, `20261013-025528-20b8-map-f06`, `20261013-025721-700e-map-f07`, `20261013-025834-053c-map-f07`.

Evidence: [delete.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025406-9fbb-map-f06/evidence/F06.ws-delete-close/delete.json) · [socket.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025406-9fbb-map-f06/evidence/F06.ws-delete-close/socket.json) · [F06-conversation-events-06-deleting-a-conversation-closes-its-socke.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025406-9fbb-map-f06/evidence/map-run/F06-conversation-events-06-deleting-a-conversation-closes-its-socke.json) · [delete.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025528-20b8-map-f06/evidence/F06.ws-delete-close/delete.json) · [socket.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025528-20b8-map-f06/evidence/F06.ws-delete-close/socket.json) · [F06-conversation-events-06-deleting-a-conversation-closes-its-socke.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025528-20b8-map-f06/evidence/map-run/F06-conversation-events-06-deleting-a-conversation-closes-its-socke.json).

The legacy events and session protocols reproduce independently twice. Subscriber.close does not close the WebSocket, leaving connected clients waiting after successful DELETE. This is a socket/task leak; no OS process orphan is claimed.

### Medium — Loading a plugin twice duplicates hook side effects

Features: `F09.load-plugin-twice`.

**Expected:** Repeated plugin loading keeps one copy of its hooks.

**Observed:** Skills stay deduplicated but identical user_prompt_submit hooks are appended twice.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F09 --only F09.load-plugin-twice --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025803-aa01-map-f09`, `20261013-030236-b017-map-f09`.

Evidence: [F09-model-switching-plugins-14-load-the-same-plugin-twice-f09-load-plug.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/map-run/F09-model-switching-plugins-14-load-the-same-plugin-twice-f09-load-plug.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.load-plugin-twice/get.json) · [second-load.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.load-plugin-twice/second-load.json) · [F09-model-switching-plugins-14-load-the-same-plugin-twice-f09-load-plug.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/map-run/F09-model-switching-plugins-14-load-the-same-plugin-twice-f09-load-plug.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/F09.load-plugin-twice/get.json) · [second-load.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/F09.load-plugin-twice/second-load.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Medium — Native model switch endpoints alter ACP placeholder LLM

Features: `F09.switch-llm-acp-refused`.

**Expected:** switch_llm and switch_profile reject ACP conversations and retain acp-managed config.

**Observed:** The endpoints accept and replace the ACP agent placeholder LLM.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F09 --only F09.switch-llm-acp-refused --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025803-aa01-map-f09`, `20261013-030236-b017-map-f09`.

Evidence: [F09-model-switching-plugins-08-llm-switches-on-an-acp-conversation-f09-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/map-run/F09-model-switching-plugins-08-llm-switches-on-an-acp-conversation-f09-.json) · [switch-llm.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.switch-llm-acp-refused/switch-llm.json) · [switch-profile.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.switch-llm-acp-refused/switch-profile.json) · [F09-model-switching-plugins-08-llm-switches-on-an-acp-conversation-f09-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/map-run/F09-model-switching-plugins-08-llm-switches-on-an-acp-conversation-f09-.json) · [switch-llm.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/F09.switch-llm-acp-refused/switch-llm.json) · [switch-profile.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/F09.switch-llm-acp-refused/switch-profile.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Medium — GET omits an acknowledged mid-run model switch

Features: `F09.switch-llm-mid-run-get`.

**Expected:** GET and persisted state reflect the acknowledged LLM switch.

**Observed:** The acknowledged switch appears immediately on the WebSocket, but GET still reports the previous default usage_id while the tool step is running, in both fresh repeats.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F09 --only F09.switch-llm-mid-run-get --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025803-aa01-map-f09`, `20261013-030236-b017-map-f09`.

Evidence: [F09-model-switching-plugins-05-get-right-after-a-mid-run-switch-f09-swi.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/map-run/F09-model-switching-plugins-05-get-right-after-a-mid-run-switch-f09-swi.json) · [frames.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.switch-llm-mid-run-get/frames.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.switch-llm-mid-run-get/get.json) · [switch.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.switch-llm-mid-run-get/switch.json) · [F09-model-switching-plugins-05-get-right-after-a-mid-run-switch-f09-swi.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/map-run/F09-model-switching-plugins-05-get-right-after-a-mid-run-switch-f09-swi.json) · [frames.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/F09.switch-llm-mid-run-get/frames.json).

Not filed by this worker: external reporting and publication remain parent-owned. The following contemporaneous base_state assertion was not reached; persisted-state loss and loss on crash are not claimed.

### Medium — Switch requests reuse stale registered LLM configuration

Features: `F09.switch-profile-edited, F09.switch-llm-registered-usage-id`.

**Expected:** A switch installs posted or current profile configuration, or rejects the request.

**Observed:** A 200 success silently retains an older LLM when its usage_id was registered earlier; editing a saved profile is ignored on later switch.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F09 --only F09.switch-profile-edited,F09.switch-llm-registered-usage-id --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025803-aa01-map-f09`, `20261013-030236-b017-map-f09`.

Evidence: [F09-model-switching-plugins-01-switch-to-an-edited-profile-f09-switch-p.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/map-run/F09-model-switching-plugins-01-switch-to-an-edited-profile-f09-switch-p.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.switch-profile-edited/get.json) · [switch-again.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.switch-profile-edited/switch-again.json) · [F09-model-switching-plugins-02-switch-onto-a-registered-usage-id-f09-sw.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/map-run/F09-model-switching-plugins-02-switch-onto-a-registered-usage-id-f09-sw.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.switch-llm-registered-usage-id/get.json) · [switch.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.switch-llm-registered-usage-id/switch.json).

Merged: both variants use the first-write-wins LLM registry and silently reuse the previous registration. Not filed by this worker: external reporting and publication remain parent-owned.

### Medium — Final-response endpoint returns abandoned branch answer

Features: `F10.navigate-final-response`.

**Expected:** Navigating HEAD before the answer makes the active-branch final response empty.

**Observed:** agent_final_response still returns the abandoned answer.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F10 --only F10.navigate-final-response --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024131-0603-map-f10`, `20261013-024315-4f15-map-f10`.

Evidence: [F10-fork-navigate-condense-ask-09-final-response-after-navigating-back-f10.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024131-0603-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-09-final-response-after-navigating-back-f10.json) · [after-navigate.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024131-0603-map-f10/evidence/F10.navigate-final-response/after-navigate.json) · [F10-fork-navigate-condense-ask-09-final-response-after-navigating-back-f10.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024315-4f15-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-09-final-response-after-navigating-back-f10.json) · [after-navigate.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024315-4f15-map-f10/evidence/F10.navigate-final-response/after-navigate.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Medium — Goal resume runs beyond max_iterations

Features: `F11.goal-cap-overrun`.

**Expected:** No goal status reports iteration above max_iterations.

**Observed:** Resuming after failed last judge reports capped 2 of 1 and performs another round.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F11 --only F11.goal-cap-overrun --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031634-2620-map-f11`, `20261013-031830-28b2-map-f11`.

Evidence: [F11-goals-02-a-resume-after-a-failed-last-audit-overr.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031634-2620-map-f11/evidence/map-run/F11-goals-02-a-resume-after-a-failed-last-audit-overr.json) · [goal-events.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031634-2620-map-f11/evidence/F11.goal-cap-overrun/goal-events.json) · [resume.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031634-2620-map-f11/evidence/F11.goal-cap-overrun/resume.json) · [F11-goals-02-a-resume-after-a-failed-last-audit-overr.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031830-28b2-map-f11/evidence/map-run/F11-goals-02-a-resume-after-a-failed-last-audit-overr.json) · [goal-events.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031830-28b2-map-f11/evidence/F11.goal-cap-overrun/goal-events.json) · [resume.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031830-28b2-map-f11/evidence/F11.goal-cap-overrun/resume.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Medium — Restart leaves an inactive goal marked running

Features: `F11.goal-restart-active`.

**Expected:** A loop cancelled by restart is reported interrupted and inactive.

**Observed:** Conversation restores paused but its latest goal status remains active/running.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F11 --only F11.goal-restart-active --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031634-2620-map-f11`, `20261013-031830-28b2-map-f11`.

Evidence: [F11-goals-03-a-loop-active-at-a-restart-stays-running.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031634-2620-map-f11/evidence/map-run/F11-goals-03-a-loop-active-at-a-restart-stays-running.json) · [after-restart.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031634-2620-map-f11/evidence/F11.goal-restart-active/after-restart.json) · [goal-events.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031634-2620-map-f11/evidence/F11.goal-restart-active/goal-events.json) · [F11-goals-03-a-loop-active-at-a-restart-stays-running.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031830-28b2-map-f11/evidence/map-run/F11-goals-03-a-loop-active-at-a-restart-stays-running.json) · [after-restart.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031830-28b2-map-f11/evidence/F11.goal-restart-active/after-restart.json) · [goal-events.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031830-28b2-map-f11/evidence/F11.goal-restart-active/goal-events.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Medium — Pending file-credential binding poisons a native conversation

Features: `F12.binding-native-cold`.

**Expected:** A cold native conversation never acquires an ACP credential-binding requirement.

**Observed:** Binding while native conversation is unloaded creates a persistent requirement that blocks later loading after pause.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F12 --only F12.binding-native-cold --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025756-a01d-map-f12`, `20261013-030529-8df8-map-f12`.

Evidence: [F12-runtime-and-credentials-02-regular-conversation-not-loaded-f12-bind.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025756-a01d-map-f12/evidence/map-run/F12-runtime-and-credentials-02-regular-conversation-not-loaded-f12-bind.json) · [events-after-pause.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025756-a01d-map-f12/evidence/F12.binding-native-cold/events-after-pause.json) · [put.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025756-a01d-map-f12/evidence/F12.binding-native-cold/put.json) · [F12-runtime-and-credentials-02-regular-conversation-not-loaded-f12-bind.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030529-8df8-map-f12/evidence/map-run/F12-runtime-and-credentials-02-regular-conversation-not-loaded-f12-bind.json) · [events-after-pause.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030529-8df8-map-f12/evidence/F12.binding-native-cold/events-after-pause.json) · [put.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030529-8df8-map-f12/evidence/F12.binding-native-cold/put.json).

Not filed by this worker: external reporting and publication remain parent-owned. The post-pause API loading failure is proved; the later meta.json length assertion was not reached.

### Medium — Model switch loses managed API key refresh hook

Features: `F12.managed-key-switch`.

**Expected:** An in-scope switched LLM retries a 401 after fetching managed key.

**Observed:** First run refreshes; after switch the 401 surfaces, no second fetch or retry, conversation errors.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F12 --only F12.managed-key-switch --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025756-a01d-map-f12`, `20261013-030529-8df8-map-f12`.

Evidence: [F12-runtime-and-credentials-05-refresh-after-a-model-switch-f12-managed.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025756-a01d-map-f12/evidence/map-run/F12-runtime-and-credentials-05-refresh-after-a-model-switch-f12-managed.json) · [key-fetch.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025756-a01d-map-f12/evidence/F12.managed-key-switch/key-fetch.json) · [F12-runtime-and-credentials-05-refresh-after-a-model-switch-f12-managed.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030529-8df8-map-f12/evidence/map-run/F12-runtime-and-credentials-05-refresh-after-a-model-switch-f12-managed.json) · [key-fetch.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030529-8df8-map-f12/evidence/F12.managed-key-switch/key-fetch.json).

Not filed by this worker: external reporting and publication remain parent-owned. The pre-assertion wait prints error after the switch in both repeats, while the source sink count stays 1; the final finished-state GET assertion was not reached.

### Medium — Sandbox pause leaves open conversation sockets silent

Features: `F12.sandbox-pause-websocket`.

**Expected:** Existing sockets close or continue delivering rehydrated conversation events.

**Observed:** An open socket remains bound to the unloaded service and receives no later new events.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F12 --only F12.sandbox-pause-websocket --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025756-a01d-map-f12`, `20261013-030529-8df8-map-f12`.

Evidence: [F12-runtime-and-credentials-01-open-sockets-across-a-pause-f12-sandbox-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025756-a01d-map-f12/evidence/map-run/F12-runtime-and-credentials-01-open-sockets-across-a-pause-f12-sandbox-.json) · [fresh-session-socket.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025756-a01d-map-f12/evidence/F12.sandbox-pause-websocket/fresh-session-socket.json) · [fresh-socket.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025756-a01d-map-f12/evidence/F12.sandbox-pause-websocket/fresh-socket.json) · [old-session-socket.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025756-a01d-map-f12/evidence/F12.sandbox-pause-websocket/old-session-socket.json) · [old-socket.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025756-a01d-map-f12/evidence/F12.sandbox-pause-websocket/old-socket.json) · [F12-runtime-and-credentials-01-open-sockets-across-a-pause-f12-sandbox-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030529-8df8-map-f12/evidence/map-run/F12-runtime-and-credentials-01-open-sockets-across-a-pause-f12-sandbox-.json).

Not filed by this worker: external reporting and publication remain parent-owned. Both old events/session captures and their fresh controls were saved before the first failed assertion; both old streams lack the post-pause message and remote-close frame.

### Medium — Synchronous bash execution truncates output above 1 MiB

Features: `F13.execute-large-output`.

**Expected:** execute_bash_command returns all 1100012 stdout characters.

**Observed:** It returns only the final chunk, losing the first 1048576 characters.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F13 --only F13.execute-large-output --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031029-c530-map-f13`, `20261013-031229-ccc9-map-f13`.

Evidence: [F13-bash-04-large-output-through-execute-f13-execute.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/map-run/F13-bash-04-large-output-through-execute-f13-execute.json) · [execute.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/F13.execute-large-output/execute.json) · [F13-bash-04-large-output-through-execute-f13-execute.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/map-run/F13-bash-04-large-output-through-execute-f13-execute.json) · [execute.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/F13.execute-large-output/execute.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Medium — Bash output paging filters order after page limit

Features: `F13.order-gt-paging`.

**Expected:** limit=1 with order__gt=0 returns the next output chunk.

**Observed:** The result is empty with a next_page_id; SDK pollers can miss later chunks and time out.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F13 --only F13.order-gt-paging --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031029-c530-map-f13`, `20261013-031229-ccc9-map-f13`.

Evidence: [F13-bash-03-order-filter-and-paging-f13-order-gt-pag.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/map-run/F13-bash-03-order-filter-and-paging-f13-order-gt-pag.json) · [limit-1.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/F13.order-gt-paging/limit-1.json) · [limit-2.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/F13.order-gt-paging/limit-2.json) · [F13-bash-03-order-filter-and-paging-f13-order-gt-pag.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/map-run/F13-bash-03-order-filter-and-paging-f13-order-gt-pag.json) · [limit-1.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/F13.order-gt-paging/limit-1.json) · [limit-2.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/F13.order-gt-paging/limit-2.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Medium — Bash timestamp filters compare local spelling rather than instant

Features: `F13.timestamp-offset`.

**Expected:** Equivalent UTC and non-UTC offset timestamps select the same events.

**Observed:** UTC selects the command while equivalent +02:00 timestamp selects none.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F13 --only F13.timestamp-offset --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031029-c530-map-f13`, `20261013-031229-ccc9-map-f13`.

Evidence: [F13-bash-01-offset-timestamps-f13-timestamp-offset-k.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/map-run/F13-bash-01-offset-timestamps-f13-timestamp-offset-k.json) · [plus-two.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/F13.timestamp-offset/plus-two.json) · [utc.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/F13.timestamp-offset/utc.json) · [F13-bash-01-offset-timestamps-f13-timestamp-offset-k.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/map-run/F13-bash-01-offset-timestamps-f13-timestamp-offset-k.json) · [plus-two.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/F13.timestamp-offset/plus-two.json) · [utc.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/F13.timestamp-offset/utc.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Medium — Case-only sibling directory names loop pagination

Features: `F14.subdirs-case-pagination`.

**Expected:** Pagination over Foo and foo reaches both directories.

**Observed:** The lowercased cursor repeats the first page indefinitely.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F14 --only F14.subdirs-case-pagination --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024217-af4c-map-f14`, `20261013-024649-c36e-map-f14`.

Evidence: [F14-files-05-paging-past-a-case-only-twin-f14-subdirs.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/map-run/F14-files-05-paging-past-a-case-only-twin-f14-subdirs.json) · [page-2.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/F14.subdirs-case-pagination/page-2.json) · [F14-files-05-paging-past-a-case-only-twin-f14-subdirs.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/map-run/F14-files-05-paging-past-a-case-only-twin-f14-subdirs.json) · [page-2.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/F14.subdirs-case-pagination/page-2.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Medium — Concurrent trajectory exports share and corrupt one temporary ZIP

Features: `F14.trajectory-concurrent`.

**Expected:** All concurrent downloads return 200 and valid ZIP bytes.

**Observed:** Shared temporary path is overwritten/unlinked across handlers, causing broken downloads and 500s.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F14 --only F14.trajectory-concurrent --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024217-af4c-map-f14`, `20261013-024649-c36e-map-f14`.

Evidence: [F14-files-08-concurrent-trajectory-downloads-f14-traj.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/map-run/F14-files-08-concurrent-trajectory-downloads-f14-traj.json) · [burst.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/F14.trajectory-concurrent/burst.json) · [F14-files-08-concurrent-trajectory-downloads-f14-traj.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/map-run/F14-files-08-concurrent-trajectory-downloads-f14-traj.json) · [burst.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/F14.trajectory-concurrent/burst.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Medium — Trajectory export ignores init-time conversations_path

Features: `F14.trajectory-init-path`.

**Expected:** Both trajectory routes export the conversation stored at the initialized path.

**Observed:** GET finds the conversation but trajectory export reads the launch-time default and returns 404.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F14 --only F14.trajectory-init-path --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024217-af4c-map-f14`, `20261013-024649-c36e-map-f14`.

Evidence: [F14-files-11-init-time-conversations-path-f14-traject.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/map-run/F14-files-11-init-time-conversations-path-f14-traject.json) · [F14-files-11-init-time-conversations-path-f14-traject.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/map-run/F14-files-11-init-time-conversations-path-f14-traject.json) · [F14-files-02-init-time-conversations-path-f14-traject.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034147-e66e-map-f14/evidence/map-run/F14-files-02-init-time-conversations-path-f14-traject.json) · [global.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034241-a692-f14-init/evidence/F14.trajectory-init-path/global.json) · [scoped.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034241-a692-f14-init/evidence/F14.trajectory-init-path/scoped.json) · [F14-files-02-init-time-conversations-path-f14-traject.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034324-233c-map-f14/evidence/map-run/F14-files-02-init-time-conversations-path-f14-traject.json).

Not filed by this worker: external reporting and publication remain parent-owned. Two additional fresh sibling runs save 404 responses from both the global and scoped export routes after custom init-time conversation storage was configured.

### Medium — Changes misses a repository below the requested workspace directory

Features: `F15.changes-repo-below-path`.

**Expected:** A plain workspace directory containing one repository returns its two changes prefixed with proj/.

**Observed:** HTTP 200 [] although GET for the nested repository returns UPDATED README.md and ADDED notes.txt.

```sh
control-agent-server map run --file F15 --only F15.changes-repo-below-path --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-022138-1cb7-map-f15`, `20261013-022337-0fbc-map-f15`.

Evidence: [ws.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022138-1cb7-map-f15/evidence/F15.changes-repo-below-path/ws.json) · [ws.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022337-0fbc-map-f15/evidence/F15.changes-repo-below-path/ws.json).

Known map bug, independently reproduced twice. Typical repository-backed workspace layout.

### Medium — Changes rejects tracked filenames with spaces and mangles non-ASCII filenames

Features: `F15.changes-special-names`.

**Expected:** HTTP 200 [{status: UPDATED, path: my notes.md}] with the real filename.

**Observed:** A modified tracked my notes.md makes the entire Changes response HTTP400: Unexpected git diff output format: M\tmy notes.md. In both supplemental fresh runs a modified café.txt is returned as the quoted/mangled path "caf/303/251.txt" instead of its real filename.

```sh
control-agent-server map run --file F15 --only F15.changes-special-names --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-022138-1cb7-map-f15`, `20261013-022337-0fbc-map-f15`.

Evidence: [space.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022138-1cb7-map-f15/evidence/F15.changes-special-names/space.json) · [space.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022337-0fbc-map-f15/evidence/F15.changes-special-names/space.json) · [non-ascii.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031006-7188-map-f15/evidence/F15.changes-special-names/non-ascii.json) · [non-ascii.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031237-2ccf-map-f15/evidence/F15.changes-special-names/non-ascii.json).

The original space case is confirmed twice. Copied recipes preserve the same assertions while continuing through sibling cases, and two further fresh runs independently prove the non-ASCII branch. Supplemental command and adaptations: F15-recipe-adaptation.md; family-results/F15-supplemental.json.

### Medium — Changes returns tracked and untracked paths on inconsistent bases when querying a repository subdirectory

Features: `F15.changes-subdir-paths`.

**Expected:** Every returned path resolves against one consistent base (requested src directory or repository root).

**Observed:** HTTP 200 [UPDATED README.md, ADDED new.py, UPDATED src/app.py]; no single base resolves all returned paths, and README.md is outside the requested src directory.

```sh
control-agent-server map run --file F15 --only F15.changes-subdir-paths --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-022138-1cb7-map-f15`, `20261013-022337-0fbc-map-f15`.

Evidence: [src.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022138-1cb7-map-f15/evidence/F15.changes-subdir-paths/src.json) · [src.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022337-0fbc-map-f15/evidence/F15.changes-subdir-paths/src.json).

Known map bug. Fixture repository-root positive control returns all four changes with consistent paths.

### Medium — Diff cannot read a working-tree file that Changes correctly lists as deleted

Features: `F15.diff-deleted-file`.

**Expected:** HTTP 200 original from HEAD and modified empty string for a tracked deleted file.

**Observed:** Changes lists DELETED src/util.py, but Diff answers HTTP 400 'File does not exist: .../src/util.py'.

```sh
control-agent-server map run --file F15 --only F15.diff-deleted-file --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-022138-1cb7-map-f15`, `20261013-022337-0fbc-map-f15`.

Evidence: [diff.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022138-1cb7-map-f15/evidence/F15.diff-deleted-file/diff.json) · [diff.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022337-0fbc-map-f15/evidence/F15.diff-deleted-file/diff.json).

Known map bug. Deletion-list positive control reaches the file before diff failure.

### Medium — An unchanged indented file has a phantom diff because original text loses indentation

Features: `F15.diff-whitespace`.

**Expected:** An unchanged file has identical original and modified text.

**Observed:** An unchanged indented file returns original indented line\nbody without its two leading spaces, while modified retains them. Both supplemental fresh runs also return original body and modified body followed by two newlines for the unchanged trailing-blank-line file. Changes lists neither unchanged file.

```sh
control-agent-server map run --file F15 --only F15.diff-whitespace --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-022138-1cb7-map-f15`, `20261013-022337-0fbc-map-f15`.

Evidence: [lead.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022138-1cb7-map-f15/evidence/F15.diff-whitespace/lead.json) · [lead.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022337-0fbc-map-f15/evidence/F15.diff-whitespace/lead.json) · [trail.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031006-7188-map-f15/evidence/F15.diff-whitespace/trail.json) · [trail.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031237-2ccf-map-f15/evidence/F15.diff-whitespace/trail.json).

Leading-indentation failure confirmed twice in the original recipe. CRLF positive controls pass. Copied recipe continues after the indentation assertion and independently proves trailing-blank-line loss in two further fresh runs.

### Medium — Cookie authentication fails on the slashless Docker workspace root

Features: `F16.docker-root-cookie`.

**Expected:** With the workspace-session cookie, slash and slashless routes both reach the conversation lookup (404 for the chosen unknown UUID).

**Observed:** In both fresh Docker-mode subprocesses the slashed route returns 404 with the cookie, but the slashless route returns 401 Unauthorized. Header-auth controls reach the conversation lookup for both forms.

```sh
control-agent-server map run --file F16 --only F16.docker-root-cookie --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025955-5a37-map-f16`, `20261013-030422-3050-map-f16`.

Evidence: [F16-workspace-serving-and-vscode-07-docker-mode-root-and-the-cookie-f16-dock.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025955-5a37-map-f16/evidence/map-run/F16-workspace-serving-and-vscode-07-docker-mode-root-and-the-cookie-f16-dock.json) · [slash.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030329-0721-f16-docker/evidence/F16.docker-root-cookie/slash.json) · [slashless.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030329-0721-f16-docker/evidence/F16.docker-root-cookie/slashless.json) · [F16-workspace-serving-and-vscode-07-docker-mode-root-and-the-cookie-f16-dock.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030422-3050-map-f16/evidence/map-run/F16-workspace-serving-and-vscode-07-docker-mode-root-and-the-cookie-f16-dock.json) · [slash.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030655-92b6-f16-docker/evidence/F16.docker-root-cookie/slash.json) · [slashless.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030655-92b6-f16-docker/evidence/F16.docker-root-cookie/slashless.json).

This proves startup route/auth dispatch with OH_CONVERSATION_RUNTIME=docker; a Docker conversation/container is not used. The fresh parent map runs each launch and stop their own isolated Docker-mode server. Not filed: parent owns external reporting; no issue was filed by this worker.

### Medium — VS Code URLs do not encode folder names containing ampersand or hash

Features: `F16.vscode-folder-encoding`.

**Expected:** Parsing the URL yields exactly the requested folder and no fragment.

**Observed:** The saved scoped URL pastes qa f16&x=1#frag literally: a URL parser reads a truncated folder, an extra x parameter, and a fragment. The normal-folder control passes in both runs.

```sh
control-agent-server map run --file F16 --only F16.vscode-enabled-status,F16.vscode-url-shape,F16.vscode-folder-encoding --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025955-5a37-map-f16`, `20261013-030422-3050-map-f16`.

Evidence: [F16-workspace-serving-and-vscode-04-folder-with-and-f16-vscode-folder-encodi.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025955-5a37-map-f16/evidence/map-run/F16-workspace-serving-and-vscode-04-folder-with-and-f16-vscode-folder-encodi.json) · [odd-folder.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025955-5a37-map-f16/evidence/F16.vscode-folder-encoding/odd-folder.json) · [F16-workspace-serving-and-vscode-04-folder-with-and-f16-vscode-folder-encodi.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030422-3050-map-f16/evidence/map-run/F16-workspace-serving-and-vscode-04-folder-with-and-f16-vscode-folder-encodi.json) · [odd-folder.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030422-3050-map-f16/evidence/F16.vscode-folder-encoding/odd-folder.json).

No editor binary is installed. This confirms the URL returned by the real API and its browser parsing, not opening the editor. The URL is observable through the separately confirmed stopped-editor advertisement defect. Not filed: parent owns external reporting; no issue was filed by this worker.

### Medium — Settings PATCH accepts nonexistent agent and meta profile targets

Features: `F18.dangling-pointers`.

**Expected:** PATCH /api/settings must reject nonexistent active_agent_profile_id and active_meta_profile targets with 404, as their dedicated activate routes do, without enabling a switch tool for a nonexistent meta-profile.

**Observed:** In both runs each dedicated activate route returned 404, but PATCH returned 200 with the nonexistent agent UUID or meta-profile name in the active pointer. The meta-profile PATCH also returned enable_classify_and_switch_llm_tool=true.

```sh
control-agent-server map run --file F18 --only F18.dangling-pointers --fresh --repeat 2 --record --checkout /workspace/agent-sdk-verify
```

Fresh confirmation runs: `20261013-024700-3f62-map-f18`, `20261013-025117-43f0-map-f18`.

Evidence: [activate-agent-profile.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.dangling-pointers/activate-agent-profile.json) · [agent-profile-id.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.dangling-pointers/agent-profile-id.json) · [activate-meta-profile.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.dangling-pointers/activate-meta-profile.json) · [meta-profile.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.dangling-pointers/meta-profile.json) · [F18-settings-and-secrets-02-dangling-agent-profile-pointer-f18-dangl.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/map-run/F18-settings-and-secrets-02-dangling-agent-profile-pointer-f18-dangl.json) · [F18-settings-and-secrets-03-dangling-meta-profile-pointer-f18-dangli.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/map-run/F18-settings-and-secrets-03-dangling-meta-profile-pointer-f18-dangli.json).

Grouped the agent and meta variants under the same feature ID and missing-target validation symptom. The saved response confirms acceptance and returned state; the map-described lazy default-profile suppression was not separately exercised in these focused repeats. Not filed: this task is read-only saved-evidence extraction; no issue lookup or external action was performed. Both fresh runs used checkout SHA acca181af1f353975965bcf6486e1d0a58f444c0. Reproduction commands are provided for review and were not rerun during extraction.

### Medium — Scoped secret listing returns unhandled 500 for agent profile store errors

Features: `F18.secret-scope-profile-errors`.

**Expected:** GET /api/settings/secrets?agent_profile_id= must map malformed agent-profile data to 400 and a busy profile-store lock to 503, matching the agent-profile routes.

**Observed:** In both runs the malformed profile control returned 400, while scoped secret listing returned 500 with the validation exception. With the lock held, the profile route returned 503 after about 30 seconds, while scoped secret listing returned 500 with Agent profile store lock acquisition timed out after 30.0s (about 32.6 seconds).

```sh
control-agent-server map run --file F18 --only F18.secret-scope-profile-errors --fresh --repeat 2 --record --checkout /workspace/agent-sdk-verify
```

Fresh confirmation runs: `20261013-024700-3f62-map-f18`, `20261013-025117-43f0-map-f18`.

Evidence: [agent-profile-route.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.secret-scope-profile-errors/agent-profile-route.json) · [unloadable.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.secret-scope-profile-errors/unloadable.json) · [agent-profile-busy.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.secret-scope-profile-errors/agent-profile-busy.json) · [secrets-busy.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.secret-scope-profile-errors/secrets-busy.json) · [F18-settings-and-secrets-04-agent-profile-that-no-longer-loads-f18-s.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/map-run/F18-settings-and-secrets-04-agent-profile-that-no-longer-loads-f18-s.json) · [F18-settings-and-secrets-05-agent-profile-store-busy-f18-secret-scop.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/map-run/F18-settings-and-secrets-05-agent-profile-store-busy-f18-secret-scop.json).

Grouped malformed-data and busy-lock cases because they exercise the same scoped-list entry point and absent profile-store error mapping, with both control/target pairs independently saved in each run. Not filed: this task is read-only saved-evidence extraction; no issue lookup or external action was performed. Both fresh runs used checkout SHA acca181af1f353975965bcf6486e1d0a58f444c0. Reproduction commands are provided for review and were not rerun during extraction.

### Medium — Deleting an LLM profile through its .json alias bypasses the reference guard

Features: `F20.json-alias-guard`.

**Expected:** Deleting the .json alias of a referenced profile must return 409 and preserve the profile, as deleting the plain name does.

**Observed:** The plain-name DELETE returned 409 naming the agent referrer and GET through the alias read the profile. Alias DELETE returned 200; the following plain-name GET returned 404 while the referencing agent profile still existed. Cleanup completed before the saved 409 assertion failed. Both cited fresh targeted repeats reproduce this outcome; the exact per-attempt values are in the saved exchanges/transcripts.

```sh
control-agent-server map run --file F20 --only F20.json-alias-guard --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-030609-7ab0-map-f20`, `20261013-030955-5180-map-f20`.

Evidence: [F20-llm-profiles-04-delete-through-the-json-alias-f20-json-a.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/map-run/F20-llm-profiles-04-delete-through-the-json-alias-f20-json-a.json) · [delete.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/F20.json-alias-guard/delete.json) · [after.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/F20.json-alias-guard/after.json) · [F20-llm-profiles-04-delete-through-the-json-alias-f20-json-a.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030955-5180-map-f20/evidence/map-run/F20-llm-profiles-04-delete-through-the-json-alias-f20-json-a.json) · [delete.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030955-5180-map-f20/evidence/F20.json-alias-guard/delete.json) · [after.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030955-5180-map-f20/evidence/F20.json-alias-guard/after.json).

Alias rename and active-profile pointer aftermath mentioned in frozen prose were not independently driven by this recipe and are excluded. Two further fresh targeted confirmations now reproduce the exact marked failures. Not filed: read-only evidence extraction performed no issue lookup or external action.

### Medium — Profile activation accepts an undecryptable stored key after cipher rotation

Features: `F20.secret-key-rotation`.

**Expected:** Activation must refuse a profile whose encrypted key cannot be decrypted, preserving the previous active profile and settings ciphertext.

**Observed:** After rotation the profile file retained Fernet ciphertext, profile detail returned config.api_key=null/api_key_set=false, while the list reported api_key_set=true. Activation returned 200 and llm_applied=true instead of 4xx, failing the exact activation assertion. Both cited fresh targeted repeats reproduce this outcome; the exact per-attempt values are in the saved exchanges/transcripts.

```sh
control-agent-server map run --file F20 --only F20.secret-key-rotation --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-030609-7ab0-map-f20`, `20261013-030955-5180-map-f20`.

Evidence: [F20-llm-profiles-05-secret-key-rotation-f20-secret-key-rotat.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/map-run/F20-llm-profiles-05-secret-key-rotation-f20-secret-key-rotat.json) · [detail.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/F20.secret-key-rotation/detail.json) · [list.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/F20.secret-key-rotation/list.json) · [activate.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/F20.secret-key-rotation/activate.json) · [F20-llm-profiles-05-secret-key-rotation-f20-secret-key-rotat.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030955-5180-map-f20/evidence/map-run/F20-llm-profiles-05-secret-key-rotation-f20-secret-key-rotat.json) · [detail.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030955-5180-map-f20/evidence/F20.secret-key-rotation/detail.json).

The recipe stops at activation. Later GET /api/settings and settings.json ciphertext checks were not reached; persisted settings destruction, a changed active pointer, and a subsequent conversation failure are not independently confirmed by this saved attempt. Two further fresh targeted confirmations now reproduce the exact marked failures. Not filed: read-only evidence extraction performed no issue lookup or external action.

### Medium — Profile validation with default retries and timeout exceeds its 30-second bound

Features: `F20.validate-unreachable-bounded, F20.validate-hang-bounded`.

**Expected:** Validation should return a verdict within 30 seconds for a refused connection or a provider that never responds, with the default retry and timeout settings.

**Observed:** A refused localhost connection returned valid=false/LLMServiceUnavailableError after 120,553ms and 120,482ms. In both fresh runs the hanging fixture received the provider request, the CLI reached its30-second ReadTimeout, /alive stayed responsive, and a hard restart cancelled the in-flight validation. The exact marked bound assertions failed.

```sh
control-agent-server map run --file F20 --only F20.validate-unreachable-bounded,F20.validate-hang-bounded --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-030609-7ab0-map-f20`, `20261013-030955-5180-map-f20`.

Evidence: [F20-llm-profiles-02-unreachable-endpoint-is-slow-f20-validat.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/map-run/F20-llm-profiles-02-unreachable-endpoint-is-slow-f20-validat.json) · [default-retries.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/F20.validate-unreachable-bounded/default-retries.json) · [F20-llm-profiles-03-hanging-provider-is-slower-f20-validate-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/map-run/F20-llm-profiles-03-hanging-provider-is-slower-f20-validate-.json) · [stub-request.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/F20.validate-hang-bounded/stub-request.json) · [F20-llm-profiles-02-unreachable-endpoint-is-slow-f20-validat.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030955-5180-map-f20/evidence/map-run/F20-llm-profiles-02-unreachable-endpoint-is-slow-f20-validat.json) · [default-retries.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030955-5180-map-f20/evidence/F20.validate-unreachable-bounded/default-retries.json).

Grouped the two variants because profile validation inherits the LLM default retry/timeout policy without a bounded preflight budget. No 27-minute terminal duration or eventual hanging-provider verdict is claimed: the focused recipe intentionally cancels it after proving the 30-second timeout. Two further fresh targeted confirmations now reproduce the exact marked failures. Not filed: read-only evidence extraction performed no issue lookup or external action.

### Medium — Overwriting an agent profile whose name ends in .json changes its identity

Features: `F21.json-suffix-identity`.

**Expected:** A repeated save of the same accepted name must retain the original profile id and increment revision to 1, or the .json-suffixed name must be rejected with 422 and nothing stored.

**Observed:** The accepted profile was activated under id 25f93991-4f33-4a2d-a179-bcff203c003b. A second save updated the LLM reference to deepseek-pro but returned a profile with different id be7b87d6-80df-4dd7-9f2c-62d429d7224e and revision 0. The saved identity/revision assertion failed. Both cited fresh targeted repeats reproduce this outcome; the exact per-attempt values are in the saved exchanges/transcripts.

```sh
control-agent-server map run --file F21 --only F21.save-create,F21.acp-kind,F21.json-suffix-identity --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-030758-8dc4-map-f21`, `20261013-030902-92d4-map-f21`.

Evidence: [F21-agent-profiles-05-json-names-lose-their-identity-f21-json-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030758-8dc4-map-f21/evidence/map-run/F21-agent-profiles-05-json-names-lose-their-identity-f21-json-.json) · [after-overwrite.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030758-8dc4-map-f21/evidence/F21.json-suffix-identity/after-overwrite.json) · [F21-agent-profiles-05-json-names-lose-their-identity-f21-json-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030902-92d4-map-f21/evidence/map-run/F21-agent-profiles-05-json-names-lose-their-identity-f21-json-.json) · [after-overwrite.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030902-92d4-map-f21/evidence/F21.json-suffix-identity/after-overwrite.json).

The recipe stops at its first identity/revision failure. The later DELETE and GET /api/settings pointer-clear assertion were not reached, so delete behavior and the final active pointer are not independently claimed. The original id is proven by the saved activation exchange inside the transcript. Two further fresh targeted confirmations now reproduce the exact marked failures. Not filed: read-only evidence extraction performed no issue lookup or external action.

### Medium — Exported TypeScript agent-profile types reject live server payload fields

Features: `F21.ts-payload-types`.

**Expected:** The exported OpenHandsAgentProfile, ACPAgentProfile, and AgentProfileDiagnostics types must accept all fields of live payloads accepted by the generated server contract.

**Observed:** The generated-contract shape file type-checked. The exported shape file failed tsc with TS2353 for disabled_skills on OpenHandsAgentProfile, acp_startup_timeout on ACPAgentProfile, and resolved_mcp_config_keys on AgentProfileDiagnostics; the summary type produced no error. Both cited fresh targeted repeats reproduce this outcome; the exact per-attempt values are in the saved exchanges/transcripts.

```sh
control-agent-server map run --file F21 --only F21.save-create,F21.acp-kind,F21.ts-payload-types --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-030758-8dc4-map-f21`, `20261013-030902-92d4-map-f21`.

Evidence: [F21-agent-profiles-04-typescript-payload-types-f21-ts-payload-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030758-8dc4-map-f21/evidence/map-run/F21-agent-profiles-04-typescript-payload-types-f21-ts-payload-.json) · [F21-agent-profiles-04-typescript-payload-types-f21-ts-payload-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030902-92d4-map-f21/evidence/map-run/F21-agent-profiles-04-typescript-payload-types-f21-ts-payload-.json).

Use the full-family command to ensure qa-f21-coder and qa-f21-acp fixture profiles exist; the selected recipe has no Requires declarations for those arrange steps. The compiler errors and payload snapshots are local saved evidence; no rebuild or network operation was performed during extraction. Two further fresh targeted confirmations now reproduce the exact marked failures. Not filed: read-only evidence extraction performed no issue lookup or external action.

### Medium — Meta-profile activation reports success while ACP drops it

Features: `F22.activate-acp`.

**Expected:** Refuse activation or explicitly report that it was not applied.

**Observed:** Activation returns 200 activated while both settings and the list retain active_meta_profile=null on an ACP agent.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F22-meta-profiles.md --only F22.save-classes,F22.save-direct,F22.empty-router,F22.activate-acp,F22.corrupt-settings,F22.persistence-dir --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-021742-7d44-map-f22`, `20261013-034317-5724-map-f22`.

Evidence: [activate.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021742-7d44-map-f22/evidence/F22.activate-acp/activate.json) · [list.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021742-7d44-map-f22/evidence/F22.activate-acp/list.json) · [F22-meta-profiles-17-activation-on-acp-settings-f22-activate-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021742-7d44-map-f22/evidence/map-run/F22-meta-profiles-17-activation-on-acp-settings-f22-activate-.json) · [activate.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034317-5724-map-f22/evidence/F22.activate-acp/activate.json) · [list.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034317-5724-map-f22/evidence/F22.activate-acp/list.json) · [F22-meta-profiles-04-activation-on-acp-settings-f22-activate-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034317-5724-map-f22/evidence/map-run/F22-meta-profiles-04-activation-on-acp-settings-f22-activate-.json).

Both runs verify the ACP state and restore OpenHands settings afterwards; the copied recipe arranges the previously undeclared qa-direct activation.

### Medium — Meta-profile persistence does not expand the configured tilde path

Features: `F22.persistence-dir`.

**Expected:** Write meta-profiles under the expanded OH_PERSISTENCE_DIR beside settings.json.

**Observed:** The configured home/qa-f22-tilde/settings.json exists, but its adjacent meta-profile is absent; the meta-profile uses the unexpanded path.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F22-meta-profiles.md --only F22.save-classes,F22.save-direct,F22.empty-router,F22.activate-acp,F22.corrupt-settings,F22.persistence-dir --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-021742-7d44-map-f22`, `20261013-034317-5724-map-f22`.

Evidence: [F22-meta-profiles-24-persistence-directory-with-f22-persisten.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021742-7d44-map-f22/evidence/map-run/F22-meta-profiles-24-persistence-directory-with-f22-persisten.json) · [save.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-022816-f88c-f22-tilde/evidence/F22.persistence-dir/save.json) · [F22-meta-profiles-06-persistence-directory-with-f22-persisten.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034317-5724-map-f22/evidence/map-run/F22-meta-profiles-06-persistence-directory-with-f22-persisten.json) · [save.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034339-4b8d-f22-tilde/evidence/F22.persistence-dir/save.json).

Nested isolated servers are stopped by the recipe; saved response and state-location transcript prove both fresh attempts.

### Medium — Blank and redacted provider keys are accepted on creation and update

Features: `F23.conn-create-blank-key, F23.conn-patch-blank-key`.

**Expected:** Reject blank, whitespace-only, and redacted placeholder keys and retain the previous shared key.

**Observed:** Whitespace and placeholder creates return 201 with api_key_set=false. PATCH accepts empty, whitespace, and placeholder values; subsequent linked-profile activation applies null, null, and the literal placeholder.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F23-llm-catalog-and-connections.md --only F23.models-no-bedrock,F23.conn-create,F23.conn-create-blank-key,F23.conn-patch-blank-key,F23.validate-linked-draft,F23.store-busy-responsive --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-024155-0956-map-f23`, `20261013-034323-e6ea-map-f23`.

Evidence: [list.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024155-0956-map-f23/evidence/F23.conn-create-blank-key/list.json) · [placeholder.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024155-0956-map-f23/evidence/F23.conn-create-blank-key/placeholder.json) · [space.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024155-0956-map-f23/evidence/F23.conn-create-blank-key/space.json) · [patch-1.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024155-0956-map-f23/evidence/F23.conn-patch-blank-key/patch-1.json) · [patch-2.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024155-0956-map-f23/evidence/F23.conn-patch-blank-key/patch-2.json) · [patch-3.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024155-0956-map-f23/evidence/F23.conn-patch-blank-key/patch-3.json).

One grouped validation defect across create/update; both endpoint branches independently reproduced twice. All negative-test keys are synthetic.

### Medium — Draft validation does not resolve its provider connection key

Features: `F23.validate-linked-draft`.

**Expected:** The same DeepSeek draft validates whether its key is inline or linked through provider_connection_id.

**Observed:** The inline-key positive control validates successfully; the linked draft returns valid=false with LLMAuthenticationError.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F23-llm-catalog-and-connections.md --only F23.models-no-bedrock,F23.conn-create,F23.conn-create-blank-key,F23.conn-patch-blank-key,F23.validate-linked-draft,F23.store-busy-responsive --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-024155-0956-map-f23`, `20261013-034323-e6ea-map-f23`.

Evidence: [linked.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024155-0956-map-f23/evidence/F23.validate-linked-draft/linked.json) · [F23-llm-catalog-and-connections-18-validate-a-linked-draft-f23-validate-lin.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024155-0956-map-f23/evidence/map-run/F23-llm-catalog-and-connections-18-validate-a-linked-draft-f23-validate-lin.json) · [linked.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034323-e6ea-map-f23/evidence/F23.validate-linked-draft/linked.json) · [F23-llm-catalog-and-connections-05-validate-a-linked-draft-f23-validate-lin.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034323-e6ea-map-f23/evidence/map-run/F23-llm-catalog-and-connections-05-validate-a-linked-draft-f23-validate-lin.json).

Tiny real DeepSeek calls distinguish credential resolution from provider/network availability.

### Medium — Expired subscription status crashes when token refresh is offline

Features: `F24.status-offline`.

**Expected:** Status returns connected=false after an unreachable token refresh, as it does for a rejected refresh.

**Observed:** An unexpired synthetic login reports connected=true; after expiry with the same unreachable proxy, status returns 500 All connection attempts failed.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F24-openai-subscription.md --only F24.status-offline,F24.device-start-offline --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-025101-09f6-map-f24`, `20261013-034748-623a-map-f24`.

Evidence: [F24-openai-subscription-18-status-with-an-expired-login-offline-f24.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025101-09f6-map-f24/evidence/map-run/F24-openai-subscription-18-status-with-an-expired-login-offline-f24.json) · [status.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025510-6f5e-f24-offline/evidence/F24.status-offline/status.json) · [F24-openai-subscription-01-status-with-an-expired-login-offline-f24.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034748-623a-map-f24/evidence/map-run/F24-openai-subscription-01-status-with-an-expired-login-offline-f24.json) · [status.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034812-81fc-f24-offline/evidence/F24.status-offline/status.json).

No human login or real account is completed; fixtures contain only explicitly fake access/refresh tokens.

### Medium — Documented skill and plugin source examples cannot be parsed

Features: `F25.install-documented-sources, F26.install-documented-source`.

**Expected:** The source syntax advertised by the current OpenAPI descriptions installs successfully.

**Observed:** The supported repository plus repo_path forms install from GitHub, while the advertised github:owner/repo/subdirectory forms return 400 Failed to fetch source.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F25-skills.md --only F25.marketplace-public,F25.install-bad-frontmatter,F25.install-documented-sources,F25.install-unknown-ref,F25.refresh-unfetchable,F25.sync-offline,F25.marketplace-stale-cache --fresh --record --keep-going --timeout 360
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F26-plugins.md --only F26.install-repo-root-name,F26.install-documented-source,F26.refresh-unfetchable,F26.conversation-resume-disabled --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-025747-be38-map-f25`, `20261013-030021-e114-map-f26`, `20261013-034422-49fa-map-f25`, `20261013-034505-0581-map-f26`.

Evidence: [documented.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/F25.install-documented-sources/documented.json) · [F25-skills-16-documented-install-sources-f25-install-d.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/map-run/F25-skills-16-documented-install-sources-f25-install-d.json) · [documented.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030021-e114-map-f26/evidence/F26.install-documented-source/documented.json) · [working-form.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030021-e114-map-f26/evidence/F26.install-documented-source/working-form.json) · [F26-plugins-11-documented-install-source-f26-install-do.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030021-e114-map-f26/evidence/map-run/F26-plugins-11-documented-install-source-f26-install-do.json) · [documented.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034422-49fa-map-f25/evidence/F25.install-documented-sources/documented.json).

Grouped documentation/parser contract across skills and plugins. Working GitHub installs are live positive controls. The later skill /tree/main URL variant is not reached.

### Medium — Cached installs silently accept a nonexistent git ref

Features: `F25.install-unknown-ref, F28.install-ref-cached`.

**Expected:** An unknown ref returns HTTP 400 and leaves the existing pinned install untouched.

**Observed:** Both Canvas and skill endpoints accept the nonexistent ref with 200 when the source is cached and install the cached checkout.

```sh
control-agent-server map run --file F28 --only F28.install-ref-cached --fresh --repeat 2 --record
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F25-skills.md --only F25.marketplace-public,F25.install-bad-frontmatter,F25.install-documented-sources,F25.install-unknown-ref,F25.refresh-unfetchable,F25.sync-offline,F25.marketplace-stale-cache --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-025047-4da6-map-f28`, `20261013-025217-c43a-map-f28`, `20261013-025747-be38-map-f25`, `20261013-034422-49fa-map-f25`.

Evidence: [unknown-ref.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025047-4da6-map-f28/evidence/F28.install-ref-cached/unknown-ref.json) · [F28-canvas-extensions-02-unknown-ref-on-a-cached-source-f28-insta.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025047-4da6-map-f28/evidence/map-run/F28-canvas-extensions-02-unknown-ref-on-a-cached-source-f28-insta.json) · [unknown-ref.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025217-c43a-map-f28/evidence/F28.install-ref-cached/unknown-ref.json) · [F28-canvas-extensions-02-unknown-ref-on-a-cached-source-f28-insta.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025217-c43a-map-f28/evidence/map-run/F28-canvas-extensions-02-unknown-ref-on-a-cached-source-f28-insta.json) · [cached.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/F25.install-unknown-ref/cached.json) · [first-clone.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/F25.install-unknown-ref/first-clone.json).

The first pinned install is the positive control; the cache falls back after checkout failure. This shares a generic cached-repository cause with F25 but each driving bullet is counted separately unless grouping is explained. Grouped F25/F28 shared cached-repository fallback defect; each endpoint has two fresh proofs. No duplicate bug count.

### Medium — The public skills marketplace misses the current extensions manifest

Features: `F25.marketplace-public`.

**Expected:** Return the skills from the actual public extensions manifest.

**Observed:** A real extensions checkout is available, but GET /api/skills/marketplace returns 200 with skills=[].

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F25-skills.md --only F25.marketplace-public,F25.install-bad-frontmatter,F25.install-documented-sources,F25.install-unknown-ref,F25.refresh-unfetchable,F25.sync-offline,F25.marketplace-stale-cache --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-025747-be38-map-f25`, `20261013-034422-49fa-map-f25`.

Evidence: [catalog.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/F25.marketplace-public/catalog.json) · [F25-skills-03-public-marketplace-catalog-f25-marketpla.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/map-run/F25-skills-03-public-marketplace-catalog-f25-marketpla.json) · [catalog.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034422-49fa-map-f25/evidence/F25.marketplace-public/catalog.json) · [F25-skills-02-public-marketplace-catalog-f25-marketpla.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034422-49fa-map-f25/evidence/map-run/F25-skills-02-public-marketplace-catalog-f25-marketpla.json).

The current repository uses .plugin/marketplace.json while the service default expects marketplaces/default.json.

### Medium — Skills sync does not refresh the marketplace catalog cache

Features: `F25.marketplace-stale-cache`.

**Expected:** After sync brings a newly listed skill into the clone, marketplace catalog lists that entry.

**Observed:** Sync succeeds and the cloned skill and manifest entry exist, but the catalog still omits qa-f25-pub-extra; one warmed catalog retains its prior entry, and the second retains a cached empty result.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F25-skills.md --only F25.marketplace-public,F25.install-bad-frontmatter,F25.install-documented-sources,F25.install-unknown-ref,F25.refresh-unfetchable,F25.sync-offline,F25.marketplace-stale-cache --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-025747-be38-map-f25`, `20261013-034422-49fa-map-f25`.

Evidence: [after-sync.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/F25.marketplace-stale-cache/after-sync.json) · [F25-skills-32-catalog-after-a-sync-f25-marketplace-sta.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/map-run/F25-skills-32-catalog-after-a-sync-f25-marketplace-sta.json) · [after-sync.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034422-49fa-map-f25/evidence/F25.marketplace-stale-cache/after-sync.json) · [F25-skills-11-catalog-after-a-sync-f25-marketplace-sta.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034422-49fa-map-f25/evidence/map-run/F25-skills-11-catalog-after-a-sync-f25-marketplace-sta.json).

Independent from the public manifest-path issue: the local stand-in has a valid marketplaces/default.json. Sync invalidates only public-skills cache, leaving the catalog TTL cache.

### Medium — A resumed conversation still activates a disabled plugin skill

Features: `F26.conversation-resume-disabled`.

**Expected:** A resumed turn follows the plugin enabled state on disk.

**Observed:** After disabling the plugin and restarting, its hook no longer runs, but its first slash command still has activated_skills=[qa-f26-inst:qa-hello] on the user message.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F26-plugins.md --only F26.install-repo-root-name,F26.install-documented-source,F26.refresh-unfetchable,F26.conversation-resume-disabled --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-030021-e114-map-f26`, `20261013-034505-0581-map-f26`.

Evidence: [frames.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030021-e114-map-f26/evidence/F26.conversation-resume-disabled/frames.json) · [F26-plugins-20-resume-after-disabling-f26-conversation-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030021-e114-map-f26/evidence/map-run/F26-plugins-20-resume-after-disabling-f26-conversation-.json) · [frames.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034505-0581-map-f26/evidence/F26.conversation-resume-disabled/frames.json) · [F26-plugins-04-resume-after-disabling-f26-conversation-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034505-0581-map-f26/evidence/map-run/F26-plugins-04-resume-after-disabling-f26-conversation-.json).

Two real DeepSeek turns per proof. The later include_skills GET assertion is not reached; the live socket activation itself is proven twice.

### Medium — The browser availability probe ignores PLAYWRIGHT_BROWSERS_PATH

Features: `F27.browser-playwright-path`.

**Expected:** Find the real Chromium binary installed solely under PLAYWRIGHT_BROWSERS_PATH.

**Observed:** Two fresh Chromium-free layout-image containers report the browser unusable with the configured Playwright path. Linking the same binary into HOME/.cache/ms-playwright makes the catalog usable; removing that link reproduces the failure.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/browser_container.py
```

Fresh confirmation runs: `20261013-040445-9999-qa-f27-browser-path-1`, `20261013-040554-b24c-qa-f27-browser-path-2`.

Evidence: [catalog.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-040445-9999-qa-f27-browser-path-1/evidence/F27.browser-playwright-path/catalog.json) · [layout.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-040445-9999-qa-f27-browser-path-1/evidence/F27.browser-playwright-path/layout.json) · [before.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-040445-9999-qa-f27-browser-path-1/evidence/F27.browser-probe/before.json) · [home-control.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-040445-9999-qa-f27-browser-path-1/evidence/F27.browser-probe/home-control.json) · [F27-browser-container-00-preconditions.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-040445-9999-qa-f27-browser-path-1/evidence/map-run/F27-browser-container-00-preconditions.json) · [F27-browser-container-01-home-cache-positive-control-f27-browser-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-040445-9999-qa-f27-browser-path-1/evidence/map-run/F27-browser-container-01-home-cache-positive-control-f27-browser-.json).

The real host Chromium binary is mounted read-only; only probe/catalog usability is asserted, not a navigation test. Each container is removed after its attached-run proof.

### Medium — One slow health probe permanently latches a recovered backend unhealthy

Features: `F28.status-probe-latch`.

**Expected:** After direct health returns ok again, backend status returns ready without manual stop/start.

**Observed:** Both fresh runs keep reporting unhealthy during the five-second recovery poll, despite direct health ok and a live serving process.

```sh
control-agent-server map run --file F28 --only F28.status-probe-latch --fresh --repeat 2 --record
```

Fresh confirmation runs: `20261013-025047-4da6-map-f28`, `20261013-025217-c43a-map-f28`.

Evidence: [after-recovery.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025047-4da6-map-f28/evidence/F28.status-probe-latch/after-recovery.json) · [F28-canvas-extensions-03-health-probe-latch-f28-status-probe-latc.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025047-4da6-map-f28/evidence/map-run/F28-canvas-extensions-03-health-probe-latch-f28-status-probe-latc.json) · [after-recovery.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025217-c43a-map-f28/evidence/F28.status-probe-latch/after-recovery.json) · [F28-canvas-extensions-03-health-probe-latch-f28-status-probe-latc.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025217-c43a-map-f28/evidence/map-run/F28-canvas-extensions-03-health-probe-latch-f28-status-probe-latc.json).

The slow probe has a one-second timeout. Once unhealthy, later status calls do not probe again. No timing-only model assertions are involved.

### Medium — Canvas WebSocket bridge loses requested subprotocol

Features: `F29.ws-subprotocol`.

**Expected:** The bridge should negotiate qa.v1 exactly as the directly contacted backend does.

**Observed:** The direct socket selects qa.v1; the proxied socket selects no protocol and reports protocol none, breaking browser clients that require a subprotocol.

```sh
control-agent-server map run --file F29 --only F29.ws-subprotocol --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031857-df62-map-f29`, `20261013-031947-956c-map-f29`.

Evidence: [F29-app-backend-bridge-05-subprotocol-f29-ws-subprotocol-known-bug.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031857-df62-map-f29/evidence/map-run/F29-app-backend-bridge-05-subprotocol-f29-ws-subprotocol-known-bug.json) · [F29-app-backend-bridge-05-subprotocol-f29-ws-subprotocol-known-bug.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031947-956c-map-f29/evidence/map-run/F29-app-backend-bridge-05-subprotocol-f29-ws-subprotocol-known-bug.json).

### Medium — Overlapping OpenAI requests receive the later turn's answer

Features: `F30.chat-reuse-concurrent`.

**Expected:** Request X should receive its stored QA_F30_RACE_B answer; request Y should receive QA_F30_RACE_C.

**Observed:** Both requests receive QA_F30_RACE_C although the server stores the correct separate B and C agent messages.

```sh
control-agent-server map run --file F30 --only F30.chat-reuse-concurrent --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-032042-3ef3-map-f30`, `20261013-032720-3de9-map-f30`.

Evidence: [F30-openai-gateway-04-overlapping-turns-on-one-conversation-f3.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032042-3ef3-map-f30/evidence/map-run/F30-openai-gateway-04-overlapping-turns-on-one-conversation-f3.json) · [F30-openai-gateway-04-overlapping-turns-on-one-conversation-f3.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032720-3de9-map-f30/evidence/map-run/F30-openai-gateway-04-overlapping-turns-on-one-conversation-f3.json).

### Medium — OpenAI continuation waits 120 seconds at confirmation

Features: `F30.chat-reuse-confirmation`.

**Expected:** A continued conversation awaiting confirmation should return 409 promptly, like a new one.

**Observed:** It remains waiting_for_confirmation with the proposed command unrun, then returns 504 after the fixed 120-second gateway timeout.

```sh
control-agent-server map run --file F30 --only F30.chat-reuse-confirmation --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-032042-3ef3-map-f30`, `20261013-032720-3de9-map-f30`.

Evidence: [F30-openai-gateway-05-confirmation-on-a-continued-conversation.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032042-3ef3-map-f30/evidence/map-run/F30-openai-gateway-05-confirmation-on-a-continued-conversation.json) · [F30-openai-gateway-05-confirmation-on-a-continued-conversation.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032720-3de9-map-f30/evidence/map-run/F30-openai-gateway-05-confirmation-on-a-continued-conversation.json).

### Medium — Rejected OpenAI continuations persist duplicate user turns

Features: `F30.chat-reuse-run-limit-429`.

**Expected:** A 429 should leave the conversation unchanged so an OpenAI retry is safe.

**Observed:** Each refused request appends the user message; two 429 responses leave two copies.

```sh
control-agent-server map run --file F30 --only F30.chat-reuse-run-limit-429 --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-032042-3ef3-map-f30`, `20261013-032720-3de9-map-f30`.

Evidence: [F30-openai-gateway-06-run-limit-on-a-continued-conversation-f3.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032042-3ef3-map-f30/evidence/map-run/F30-openai-gateway-06-run-limit-on-a-continued-conversation-f3.json) · [F30-openai-gateway-06-run-limit-on-a-continued-conversation-f3.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032720-3de9-map-f30/evidence/map-run/F30-openai-gateway-06-run-limit-on-a-continued-conversation-f3.json).

### Medium — OpenAI continuation usage includes previous turns

Features: `F30.chat-usage-per-request`.

**Expected:** The second request should report its own 3 prompt, 2 completion and 5 total tokens.

**Observed:** It reports accumulated 13 prompt, 7 completion and 20 total tokens although per-call usage is available.

```sh
control-agent-server map run --file F30 --only F30.chat-usage-per-request --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-032042-3ef3-map-f30`, `20261013-032720-3de9-map-f30`.

Evidence: [F30-openai-gateway-03-usage-per-request-f30-chat-usage-per-req.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032042-3ef3-map-f30/evidence/map-run/F30-openai-gateway-03-usage-per-request-f30-chat-usage-per-req.json) · [F30-openai-gateway-03-usage-per-request-f30-chat-usage-per-req.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032720-3de9-map-f30/evidence/map-run/F30-openai-gateway-03-usage-per-request-f30-chat-usage-per-req.json).

### Medium — Explicit environment null cannot clear a configured value

Features: `F31.config-null-override`.

**Expected:** OH_APP_BACKEND_PUBLIC_URL_IS_NONE=1 should clear the URL and capability even when the config file sets it.

**Observed:** The file's URL remains advertised because merge keeps an earlier value when the environment supplies None. The same behavior prevents environment-based disabling of a configured idle TTL.

```sh
control-agent-server map run --file F31 --only F31.config-null-override --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024316-e532-map-f31`, `20261013-025937-a7eb-map-f31`.

Evidence: [F31-persistence-and-limits-09-null-from-the-environment-f31-config-nul.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024316-e532-map-f31/evidence/map-run/F31-persistence-and-limits-09-null-from-the-environment-f31-config-nul.json) · [F31-persistence-and-limits-09-null-from-the-environment-f31-config-nul.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025937-a7eb-map-f31/evidence/map-run/F31-persistence-and-limits-09-null-from-the-environment-f31-config-nul.json).

### Medium — Rejected stale-owner write changes its GET state and returns 500

Features: `F31.fenced-write-no-trace`.

**Expected:** A lost-ownership PATCH should give a client error and leave visible state unchanged.

**Observed:** The guarded save refuses the write and disk remains correct, but the stale owner's GET reports the refused title; PATCH returns 500.

```sh
control-agent-server map run --file F31 --only F31.fenced-write-no-trace --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024316-e532-map-f31`, `20261013-025937-a7eb-map-f31`.

Evidence: [F31-persistence-and-limits-03-refused-write-leaves-no-trace-f31-fenced.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024316-e532-map-f31/evidence/map-run/F31-persistence-and-limits-03-refused-write-leaves-no-trace-f31-fenced.json) · [F31-persistence-and-limits-03-refused-write-leaves-no-trace-f31-fenced.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025937-a7eb-map-f31/evidence/map-run/F31-persistence-and-limits-03-refused-write-leaves-no-trace-f31-fenced.json).

### Medium — Slow webhook causes 409 after the conversation reports finished

Features: `F32.slow-receiver`.

**Expected:** A finished conversation should accept a new run regardless of receiver latency.

**Observed:** A fast receiver permits POST /run; a 15-second receiver makes it return 409 Conversation already running while GET says finished.

```sh
control-agent-server map run --file F32 --only F32.slow-receiver --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031700-aa28-map-f32`, `20261013-032530-35b4-map-f32`.

Evidence: [F32-webhooks-and-telemetry-05-a-slow-receiver-blocks-the-next-run-f32-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031700-aa28-map-f32/evidence/map-run/F32-webhooks-and-telemetry-05-a-slow-receiver-blocks-the-next-run-f32-.json) · [F32-webhooks-and-telemetry-05-a-slow-receiver-blocks-the-next-run-f32-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032530-35b4-map-f32/evidence/map-run/F32-webhooks-and-telemetry-05-a-slow-receiver-blocks-the-next-run-f32-.json).

### Medium — Python reconnect reconciles history but skips missed callbacks

Features: `F33.conversation-reconnect-callbacks`.

**Expected:** A user message recorded during the socket outage should reach callbacks after reconnection.

**Observed:** Both messages appear in server history and state.events; only the connected message reaches the callback.

```sh
control-agent-server map run --file F33 --only F33.conversation-reconnect-callbacks --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-033440-1239-map-f33`, `20261013-034709-4e02-map-f33`.

Evidence: [F33-sdk-remote-client-23-callbacks-after-a-reconnect-f33-conversa.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-033440-1239-map-f33/evidence/map-run/F33-sdk-remote-client-23-callbacks-after-a-reconnect-f33-conversa.json) · [F33-sdk-remote-client-23-callbacks-after-a-reconnect-f33-conversa.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034709-4e02-map-f33/evidence/map-run/F33-sdk-remote-client-23-callbacks-after-a-reconnect-f33-conversa.json).

### Medium — Python run join times out during a healthy long tool call

Features: `F33.conversation-run-join-long-tool`.

**Expected:** A second run() should join the 45-second tool call and return finished.

**Observed:** It raises ConversationRunError wrapping ReadTimeout after 30 seconds while the original run continues, writes its file and finishes.

```sh
control-agent-server map run --file F33 --only F33.conversation-run-join-long-tool --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-033440-1239-map-f33`, `20261013-034709-4e02-map-f33`.

Evidence: [F33-sdk-remote-client-17-join-a-run-during-a-long-tool-call-f33-c.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-033440-1239-map-f33/evidence/map-run/F33-sdk-remote-client-17-join-a-run-during-a-long-tool-call-f33-c.json) · [F33-sdk-remote-client-17-join-a-run-during-a-long-tool-call-f33-c.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034709-4e02-map-f33/evidence/map-run/F33-sdk-remote-client-17-join-a-run-during-a-long-tool-call-f33-c.json).

### Medium — Reading Python remote state twice corrupts its cached values

Features: `F33.conversation-state-reread`.

**Expected:** Repeated reads of confirmation policy, analyzer, agent and confirmation-mode flag should remain stable.

**Observed:** First reads are correct; second policy/agent reads raise ValidationError, analyzer becomes None and confirmation mode changes true to false.

```sh
control-agent-server map run --file F33 --only F33.conversation-state-reread --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-033440-1239-map-f33`, `20261013-034709-4e02-map-f33`.

Evidence: [F33-sdk-remote-client-08-read-the-state-twice-f33-conversation-st.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-033440-1239-map-f33/evidence/map-run/F33-sdk-remote-client-08-read-the-state-twice-f33-conversation-st.json) · [F33-sdk-remote-client-08-read-the-state-twice-f33-conversation-st.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034709-4e02-map-f33/evidence/map-run/F33-sdk-remote-client-08-read-the-state-twice-f33-conversation-st.json).

### Medium — Python remote state stores transient token deltas

Features: `F33.conversation-streaming-state`.

**Expected:** state.events should exclude transient StreamingDeltaEvent frames and match stored server history.

**Observed:** The client adds streamed deltas to state.events although the server persists none.

```sh
control-agent-server map run --file F33 --only F33.conversation-streaming-state --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-033440-1239-map-f33`, `20261013-034709-4e02-map-f33`.

Evidence: [F33-sdk-remote-client-04-deltas-kept-out-of-state-events-f33-conv.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-033440-1239-map-f33/evidence/map-run/F33-sdk-remote-client-04-deltas-kept-out-of-state-events-f33-conv.json) · [F33-sdk-remote-client-04-deltas-kept-out-of-state-events-f33-conv.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034709-4e02-map-f33/evidence/map-run/F33-sdk-remote-client-04-deltas-kept-out-of-state-events-f33-conv.json).

### Medium — Python remote conversations ignore token callbacks

Features: `F33.conversation-token-callbacks`.

**Expected:** Token callbacks should receive streamed deltas supplied to the remote conversation.

**Observed:** Event callbacks see deltas, but the token callback is never called.

```sh
control-agent-server map run --file F33 --only F33.conversation-token-callbacks --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-033440-1239-map-f33`, `20261013-034709-4e02-map-f33`.

Evidence: [F33-sdk-remote-client-03-token-callbacks-on-a-remote-conversation.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-033440-1239-map-f33/evidence/map-run/F33-sdk-remote-client-03-token-callbacks-on-a-remote-conversation.json) · [F33-sdk-remote-client-03-token-callbacks-on-a-remote-conversation.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034709-4e02-map-f33/evidence/map-run/F33-sdk-remote-client-03-token-callbacks-on-a-remote-conversation.json).

### Medium — TypeScript BashWebSocketClient cannot open a Node socket

Features: `F34.bash-websocket, F34.ws-callback-client`.

**Expected:** The Node callback should receive the BashOutput that the CLI replays on the same socket.

**Observed:** No frames arrive and onError says WebSocket implementation not available because the ESM module attempts require('ws').

```sh
control-agent-server map run --file F34 --only F34.bash-websocket,F34.ws-callback-client --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024756-c705-map-f34`, `20261013-025335-6a42-map-f34`.

Evidence: [F34-typescript-client-02-bash-events-socket-from-node-f34-bash-we.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024756-c705-map-f34/evidence/map-run/F34-typescript-client-02-bash-events-socket-from-node-f34-bash-we.json) · [F34-typescript-client-02-bash-events-socket-from-node-f34-bash-we.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025335-6a42-map-f34/evidence/map-run/F34-typescript-client-02-bash-events-socket-from-node-f34-bash-we.json) · [F34-typescript-client-05-conversation-callback-socket-from-node-f.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024756-c705-map-f34/evidence/map-run/F34-typescript-client-05-conversation-callback-socket-from-node-f.json) · [F34-typescript-client-05-conversation-callback-socket-from-node-f.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025335-6a42-map-f34/evidence/map-run/F34-typescript-client-05-conversation-callback-socket-from-node-f.json).

[
  "Two driving bullets share the ESM WebSocket constructor discovery failure and are counted as one defect."
]

### Medium — TypeScript manager ignores conversation execution options

Features: `F34.manager-create-options`.

**Expected:** maxIterations 7 and stuckDetection false should be preserved, like direct RemoteConversation.start.

**Observed:** The manager-created conversation has max_iterations 500 and stuck_detection true.

```sh
control-agent-server map run --file F34 --only F34.manager-create-options --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024756-c705-map-f34`, `20261013-025335-6a42-map-f34`.

Evidence: [F34-typescript-client-07-create-options-f34-manager-create-option.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024756-c705-map-f34/evidence/map-run/F34-typescript-client-07-create-options-f34-manager-create-option.json) · [F34-typescript-client-07-create-options-f34-manager-create-option.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025335-6a42-map-f34/evidence/map-run/F34-typescript-client-07-create-options-f34-manager-create-option.json).

### Medium — TypeScript updateConversation return type promises missing fields

Features: `F34.manager-update-result`.

**Expected:** The declared ConversationInfo result should include the conversation id and stored new title.

**Observed:** The title is stored, but the promise resolves with success:true and its id/title are undefined.

```sh
control-agent-server map run --file F34 --only F34.manager-update-result --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024756-c705-map-f34`, `20261013-025335-6a42-map-f34`.

Evidence: [F34-typescript-client-06-update-result-f34-manager-update-result-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024756-c705-map-f34/evidence/map-run/F34-typescript-client-06-update-result-f34-manager-update-result-.json) · [F34-typescript-client-06-update-result-f34-manager-update-result-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025335-6a42-map-f34/evidence/map-run/F34-typescript-client-06-update-result-f34-manager-update-result-.json).

### Medium — TypeScript RemoteWorkspace corrupts binary downloads

Features: `F34.workspace-binary-download`.

**Expected:** The five-byte file ff 00 80 fe 41 should download byte for byte with file_size 5.

**Observed:** FileClient returns the exact bytes; RemoteWorkspace produces eleven bytes ef bf bd 00 ef bf bd ef bf bd 41 and file_size 11.

```sh
control-agent-server map run --file F34 --only F34.workspace-binary-download --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024310-2602-map-f34`, `20261013-024359-a3ff-map-f34`.

Evidence: [F34-typescript-client-01-binary-download-through-remoteworkspace-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024310-2602-map-f34/evidence/map-run/F34-typescript-client-01-binary-download-through-remoteworkspace-.json) · [F34-typescript-client-01-binary-download-through-remoteworkspace-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024359-a3ff-map-f34/evidence/map-run/F34-typescript-client-01-binary-download-through-remoteworkspace-.json).

### Medium — TypeScript GitChange status type disagrees with server values

Features: `F34.workspace-git-types`.

**Expected:** Statuses returned by gitChanges should type-check against exported GitChange.status.

**Observed:** The server values UPDATED and ADDED type-check against generated GitChangeStatus but fail against the exported lowercase union.

```sh
control-agent-server map run --file F34 --only F34.workspace-git-types --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024756-c705-map-f34`, `20261013-025335-6a42-map-f34`.

Evidence: [F34-typescript-client-01-git-status-type-f34-workspace-git-types-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024756-c705-map-f34/evidence/map-run/F34-typescript-client-01-git-status-type-f34-workspace-git-types-.json) · [F34-typescript-client-01-git-status-type-f34-workspace-git-types-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025335-6a42-map-f34/evidence/map-run/F34-typescript-client-01-git-status-type-f34-workspace-git-types-.json).

### Low — A conversation batch of 100 IDs returns 500 instead of a client error

Features: `F04.batch-get-limit`.

**Expected:** Refuse 100 IDs with 400/422 naming the limit.

**Observed:** A batch of 100 well-formed UUIDs returns 500 with an empty exception string.

```sh
control-agent-server map run --file F04 --only F04.create-initial-message-run-false,F04.create-secrets-get,F04.create-secrets-plain,F04.batch-get-limit,F04.patch-whitespace-title,F04.patch-unknown-id,F04.delete-unknown-id --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-024143-6004-map-f04`, `20261013-024259-9a86-map-f04`.

Evidence: [hundred.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/F04.batch-get-limit/hundred.json) · [F04-conversation-lifecycle-08-100-ids-in-one-batch-f04-batch-get-limit.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/map-run/F04-conversation-lifecycle-08-100-ids-in-one-batch-f04-batch-get-limit.json) · [hundred.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/F04.batch-get-limit/hundred.json) · [F04-conversation-lifecycle-08-100-ids-in-one-batch-f04-batch-get-limit.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/map-run/F04-conversation-lifecycle-08-100-ids-in-one-batch-f04-batch-get-limit.json).

batch_get_conversations uses assert len(ids)<100 instead of request validation; the ordinary 99-ID control is covered by the primary full family.

### Low — Plain-string create secrets cause an unhandled server error

Features: `F04.create-secrets-plain`.

**Expected:** Accept the plain-string secret like the secrets update route, or reject it with 422.

**Observed:** POST <redacted:session-cookie> returns 500: 'str' object has no attribute 'pop'.

```sh
control-agent-server map run --file F04 --only F04.create-initial-message-run-false,F04.create-secrets-get,F04.create-secrets-plain,F04.batch-get-limit,F04.patch-whitespace-title,F04.patch-unknown-id,F04.delete-unknown-id --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-024143-6004-map-f04`, `20261013-024259-9a86-map-f04`.

Evidence: [start.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/F04.create-secrets-plain/start.json) · [F04-conversation-lifecycle-07-plain-string-secret-value-f04-create-sec.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/map-run/F04-conversation-lifecycle-07-plain-string-secret-value-f04-create-sec.json) · [start.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/F04.create-secrets-plain/start.json) · [F04-conversation-lifecycle-07-plain-string-secret-value-f04-create-sec.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/map-run/F04-conversation-lifecycle-07-plain-string-secret-value-f04-create-sec.json).

This is a malformed-input/status-only defect. Synthetic QA values are used; no real secret is posted in the negative test.

### Low — DELETE on a missing conversation contradicts its documented 404

Features: `F04.delete-unknown-id`.

**Expected:** DELETE returns 404 for a missing or already-deleted conversation.

**Observed:** DELETE on an absent ID returns 400, and a second DELETE after successful deletion also returns 400, despite the documented 404.

```sh
control-agent-server map run --file F04 --only F04.create-initial-message-run-false,F04.create-secrets-get,F04.create-secrets-plain,F04.batch-get-limit,F04.patch-whitespace-title,F04.patch-unknown-id,F04.delete-unknown-id --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-024143-6004-map-f04`, `20261013-024259-9a86-map-f04`.

Evidence: [unknown.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/F04.delete-unknown-id/unknown.json) · [F04-conversation-lifecycle-12-delete-on-an-unknown-id-f04-delete-unkno.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/map-run/F04-conversation-lifecycle-12-delete-on-an-unknown-id-f04-delete-unkno.json) · [unknown.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/F04.delete-unknown-id/unknown.json) · [F04-conversation-lifecycle-12-delete-on-an-unknown-id-f04-delete-unkno.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/map-run/F04-conversation-lifecycle-12-delete-on-an-unknown-id-f04-delete-unkno.json) · [first-delete.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032709-376d-map-f04/evidence/F04.delete-unknown-id/first-delete.json) · [get-deleted.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032709-376d-map-f04/evidence/F04.delete-unknown-id/get-deleted.json).

Both the never-created and already-deleted branches reproduced twice.

### Low — PATCH on a missing conversation contradicts its documented 404

Features: `F04.patch-unknown-id`.

**Expected:** PATCH returns 404 for the same missing ID that GET returns 404 for.

**Observed:** PATCH returns 200 with success=false despite the OpenAPI 404 response declaration.

```sh
control-agent-server map run --file F04 --only F04.create-initial-message-run-false,F04.create-secrets-get,F04.create-secrets-plain,F04.batch-get-limit,F04.patch-whitespace-title,F04.patch-unknown-id,F04.delete-unknown-id --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-024143-6004-map-f04`, `20261013-024259-9a86-map-f04`.

Evidence: [unknown.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/F04.patch-unknown-id/unknown.json) · [F04-conversation-lifecycle-10-patch-on-an-unknown-id-f04-patch-unknown.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/map-run/F04-conversation-lifecycle-10-patch-on-an-unknown-id-f04-patch-unknown.json) · [unknown.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/F04.patch-unknown-id/unknown.json) · [F04-conversation-lifecycle-10-patch-on-an-unknown-id-f04-patch-unknown.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/map-run/F04-conversation-lifecycle-10-patch-on-an-unknown-id-f04-patch-unknown.json).

Status-contract defect; the source test currently locks the 200 behavior.

### Low — Whitespace title passes validation and erases the title

Features: `F04.patch-whitespace-title`.

**Expected:** Reject a whitespace-only title with 422 and retain the existing title.

**Observed:** PATCH with a whitespace-only title returns 200; a subsequent GET reports title="" on two fresh supplemental runs.

```sh
control-agent-server map run --file F04 --only F04.create-initial-message-run-false,F04.create-secrets-get,F04.create-secrets-plain,F04.batch-get-limit,F04.patch-whitespace-title,F04.patch-unknown-id,F04.delete-unknown-id --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-024143-6004-map-f04`, `20261013-024259-9a86-map-f04`.

Evidence: [patch.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/F04.patch-whitespace-title/patch.json) · [F04-conversation-lifecycle-09-whitespace-only-title-f04-patch-whitespa.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024143-6004-map-f04/evidence/map-run/F04-conversation-lifecycle-09-whitespace-only-title-f04-patch-whitespa.json) · [patch.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/F04.patch-whitespace-title/patch.json) · [F04-conversation-lifecycle-09-whitespace-only-title-f04-patch-whitespa.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024259-9a86-map-f04/evidence/map-run/F04-conversation-lifecycle-09-whitespace-only-title-f04-patch-whitespa.json) · [accepted-whitespace.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032709-376d-map-f04/evidence/F04.patch-whitespace-title/accepted-whitespace.json) · [before.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032709-376d-map-f04/evidence/F04.patch-whitespace-title/before.json).

Metadata defect: validation checks min_length before stripping. Acceptance and persisted title erasure are both independently proven twice.

### Low — Pause/interrupt on an unknown conversation use undocumented 400

Features: `F05.unknown-id-pause`.

**Expected:** Both pause and interrupt return their documented 404 for a missing conversation.

**Observed:** Both pause and interrupt return 400 for an absent valid UUID, despite GET returning 404 and both OpenAPI routes documenting 404.

```sh
control-agent-server map run --file F05 --only F05.run-error,F05.run-error-responsive,F05.unknown-id-pause,F05.run-conflict,F05.pause-running,F05.pause-running-get,F05.pause-running-release,F05.restart-running-graceful,F05.restart-hard-running,F05.pause-running-crash --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-024519-40d0-map-f05`, `20261013-024951-9459-map-f05`.

Evidence: [pause.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024519-40d0-map-f05/evidence/F05.unknown-id-pause/pause.json) · [F05-run-pause-interrupt-03-pause-or-interrupt-an-unknown-id-f05-unk.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024519-40d0-map-f05/evidence/map-run/F05-run-pause-interrupt-03-pause-or-interrupt-an-unknown-id-f05-unk.json) · [pause.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024951-9459-map-f05/evidence/F05.unknown-id-pause/pause.json) · [F05-run-pause-interrupt-03-pause-or-interrupt-an-unknown-id-f05-unk.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024951-9459-map-f05/evidence/map-run/F05-run-pause-interrupt-03-pause-or-interrupt-an-unknown-id-f05-unk.json) · [get-control.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-033533-16b0-map-f05/evidence/F05.unknown-id-interrupt/get-control.json) · [interrupt.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-033533-16b0-map-f05/evidence/F05.unknown-id-interrupt/interrupt.json).

Each method reproduced twice. Status-only defect.

### Low — A schema-valid non-user message causes 500

Features: `F06.send-non-user-role`.

**Expected:** Reject assistant-role input with 4xx and append no events, including on an empty log.

**Observed:** An assistant-role POST returns 500 on both initialized and empty logs. The rejected POST to an empty log also persists a SystemPromptEvent, leaving count 1 instead of 0.

```sh
control-agent-server map run --file F06 --only F06.send-no-run,F06.search-kind-short,F06.get-one,F06.unknown-event,F06.send-non-user-role,F06.ws-delete-close,F06.search-timestamp-order --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-025406-9fbb-map-f06`, `20261013-025528-20b8-map-f06`.

Evidence: [assistant.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025406-9fbb-map-f06/evidence/F06.send-non-user-role/assistant.json) · [F06-conversation-events-05-non-user-role-f06-send-non-user-role-kno.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025406-9fbb-map-f06/evidence/map-run/F06-conversation-events-05-non-user-role-f06-send-non-user-role-kno.json) · [assistant.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025528-20b8-map-f06/evidence/F06.send-non-user-role/assistant.json) · [F06-conversation-events-05-non-user-role-f06-send-non-user-role-kno.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025528-20b8-map-f06/evidence/map-run/F06-conversation-events-05-non-user-role-f06-send-non-user-role-kno.json) · [after.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032934-9891-map-f06/evidence/F06.send-non-user-role-empty-mutation/after.json) · [before.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032934-9891-map-f06/evidence/F06.send-non-user-role-empty-mutation/before.json).

Role is schema-valid but LocalConversation asserts user. Both response and empty-log mutation branches reproduced twice. Count remains one low-severity malformed-input bug.

### Low — Non-string secret values return 500

Features: `F08.secrets-bad-value`.

**Expected:** Numbers, null and booleans are rejected with 422.

**Observed:** Number, null, and boolean secret values all return 500 instead of 422 in both additional fresh sibling runs.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F08 --only F08.secrets-bad-value --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024737-a894-map-f08`, `20261013-025113-2057-map-f08`.

Evidence: [F08-confirmation-security-secrets-02-non-string-secret-value-f08-secrets-bad-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024737-a894-map-f08/evidence/map-run/F08-confirmation-security-secrets-02-non-string-secret-value-f08-secrets-bad-.json) · [number.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024737-a894-map-f08/evidence/F08.secrets-bad-value/number.json) · [F08-confirmation-security-secrets-02-non-string-secret-value-f08-secrets-bad-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025113-2057-map-f08/evidence/map-run/F08-confirmation-security-secrets-02-non-string-secret-value-f08-secrets-bad-.json) · [number.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025113-2057-map-f08/evidence/F08.secrets-bad-value/number.json) · [F08-confirmation-security-secrets-01-non-string-secret-value-f08-secrets-bad-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034151-6d5f-map-f08/evidence/map-run/F08-confirmation-security-secrets-01-non-string-secret-value-f08-secrets-bad-.json) · [number.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034151-6d5f-map-f08/evidence/F08.secrets-bad-value/number.json).

Not filed by this worker: external reporting and publication remain parent-owned. Number-only original confirmations are supplemented with separate saved exchanges for all three input shapes; no extra defect group is counted.

### Low — Pre-run ACP model switch accepts whitespace

Features: `F09.acp-model-blank`.

**Expected:** Blank model ids are rejected and the prior model remains.

**Observed:** Whitespace is accepted with 200 before the ACP session exists.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F09 --only F09.acp-model-blank --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025803-aa01-map-f09`, `20261013-030236-b017-map-f09`.

Evidence: [F09-model-switching-plugins-07-blank-acp-model-f09-acp-model-blank-know.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/map-run/F09-model-switching-plugins-07-blank-acp-model-f09-acp-model-blank-know.json) · [blank.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.acp-model-blank/blank.json) · [F09-model-switching-plugins-07-blank-acp-model-f09-acp-model-blank-know.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/map-run/F09-model-switching-plugins-07-blank-acp-model-f09-acp-model-blank-know.json) · [blank.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/F09.acp-model-blank/blank.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Low — Unsupported ACP model id returns 500

Features: `F09.acp-model-live-unknown`.

**Expected:** A model id absent from available_models is rejected with a client error.

**Observed:** The Claude ACP adapter model switch surfaces an internal 500.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F09 --only F09.acp-model-live-unknown --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025803-aa01-map-f09`, `20261013-030236-b017-map-f09`.

Evidence: [F09-model-switching-plugins-10-unknown-model-on-a-live-session-f09-acp-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/map-run/F09-model-switching-plugins-10-unknown-model-on-a-live-session-f09-acp-.json) · [switch.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.acp-model-live-unknown/switch.json) · [F09-model-switching-plugins-10-unknown-model-on-a-live-session-f09-acp-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/map-run/F09-model-switching-plugins-10-unknown-model-on-a-live-session-f09-acp-.json) · [switch.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/F09.acp-model-live-unknown/switch.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Low — Switching before first run loses usage accounting

Features: `F09.switch-llm-before-first-run`.

**Expected:** The successful switched model call appears under its usage_id in stats.

**Observed:** The run finishes but switched usage has no token or cost entry.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F09 --only F09.switch-llm-before-first-run --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025803-aa01-map-f09`, `20261013-030236-b017-map-f09`.

Evidence: [F09-model-switching-plugins-03-switch-before-the-first-run-f09-switch-l.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/map-run/F09-model-switching-plugins-03-switch-before-the-first-run-f09-switch-l.json) · [stats.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.switch-llm-before-first-run/stats.json) · [switch.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/F09.switch-llm-before-first-run/switch.json) · [F09-model-switching-plugins-03-switch-before-the-first-run-f09-switch-l.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/map-run/F09-model-switching-plugins-03-switch-before-the-first-run-f09-switch-l.json) · [stats.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/F09.switch-llm-before-first-run/stats.json) · [switch.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/F09.switch-llm-before-first-run/switch.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Low — TypeScript ACP switch docs promise an absent 409

Features: `F09.ts-client-acp-docs`.

**Expected:** Docs explain that a pre-run switch is stored and returns 200.

**Observed:** Both switchAcpModel docstrings promise 409 before first message.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F09 --only F09.ts-client-acp-docs --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025803-aa01-map-f09`, `20261013-030236-b017-map-f09`.

Evidence: [F09-model-switching-plugins-11-typescript-docstrings-for-a-pre-run-acp-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025803-aa01-map-f09/evidence/map-run/F09-model-switching-plugins-11-typescript-docstrings-for-a-pre-run-acp-.json) · [F09-model-switching-plugins-11-typescript-docstrings-for-a-pre-run-acp-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030236-b017-map-f09/evidence/map-run/F09-model-switching-plugins-11-typescript-docstrings-for-a-pre-run-acp-.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Low — Side question on unknown conversation returns 500

Features: `F10.ask-agent-unknown`.

**Expected:** Unknown conversation is documented 404.

**Observed:** ask_agent returns internal 500.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F10 --only F10.ask-agent-unknown --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024131-0603-map-f10`, `20261013-024315-4f15-map-f10`.

Evidence: [F10-fork-navigate-condense-ask-11-unknown-conversation-f10-ask-agent-unkno.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024131-0603-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-11-unknown-conversation-f10-ask-agent-unkno.json) · [unknown.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024131-0603-map-f10/evidence/F10.ask-agent-unknown/unknown.json) · [F10-fork-navigate-condense-ask-11-unknown-conversation-f10-ask-agent-unkno.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024315-4f15-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-11-unknown-conversation-f10-ask-agent-unkno.json) · [unknown.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024315-4f15-map-f10/evidence/F10.ask-agent-unknown/unknown.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Low — Disabled condenser is reported as an internal server error

Features: `F10.condense-status`.

**Expected:** Missing or no-op condenser is a client configuration error.

**Observed:** The disabled condenser path returns an unhandled 500 with traceback in both fresh repeats.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F10 --only F10.condense-status --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024131-0603-map-f10`, `20261013-024315-4f15-map-f10`.

Evidence: [F10-fork-navigate-condense-ask-10-refusal-status-f10-condense-status-known.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024131-0603-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-10-refusal-status-f10-condense-status-known.json) · [disabled.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024131-0603-map-f10/evidence/F10.condense-status/disabled.json) · [F10-fork-navigate-condense-ask-10-refusal-status-f10-condense-status-known.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024315-4f15-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-10-refusal-status-f10-condense-status-known.json) · [disabled.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024315-4f15-map-f10/evidence/F10.condense-status/disabled.json).

Not filed by this worker: external reporting and publication remain parent-owned. The separate no-op condenser assertion was not reached after the disabled-case failure.

### Low — Fork tags differ between state and stored metadata

Features: `F10.fork-tags-consistent`.

**Expected:** GET and meta.json agree on inherited tags.

**Observed:** GET drops source qa=src while meta.json retains it.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F10 --only F10.fork-tags-consistent --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024131-0603-map-f10`, `20261013-024315-4f15-map-f10`.

Evidence: [F10-fork-navigate-condense-ask-05-fork-tags-agree-with-the-stored-metadata.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024131-0603-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-05-fork-tags-agree-with-the-stored-metadata.json) · [fork.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024131-0603-map-f10/evidence/F10.fork-tags-consistent/fork.json) · [F10-fork-navigate-condense-ask-05-fork-tags-agree-with-the-stored-metadata.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024315-4f15-map-f10/evidence/map-run/F10-fork-navigate-condense-ask-05-fork-tags-agree-with-the-stored-metadata.json) · [fork.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024315-4f15-map-f10/evidence/F10.fork-tags-consistent/fork.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Low — Malformed scoped bash conversation id produces 500

Features: `F13.scoped-bad-id`.

**Expected:** A non-UUID conversation id is rejected with 422.

**Observed:** The dependency reads unset runtime_event_service and produces 500.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F13 --only F13.scoped-bad-id --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031029-c530-map-f13`, `20261013-031229-ccc9-map-f13`.

Evidence: [F13-bash-05-malformed-conversation-id-f13-scoped-bad.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/map-run/F13-bash-05-malformed-conversation-id-f13-scoped-bad.json) · [execute.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/F13.scoped-bad-id/execute.json) · [search.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031029-c530-map-f13/evidence/F13.scoped-bad-id/search.json) · [F13-bash-05-malformed-conversation-id-f13-scoped-bad.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/map-run/F13-bash-05-malformed-conversation-id-f13-scoped-bad.json) · [execute.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/F13.scoped-bad-id/execute.json) · [search.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031229-ccc9-map-f13/evidence/F13.scoped-bad-id/search.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Low — Archive format description omits nested-repository selection

Features: `F14.archive-format-doc`.

**Expected:** The OpenAPI format description matches archive contents.

**Observed:** It promises the entire directory but a single nested repository excludes adjacent top.txt.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F14 --only F14.archive-format-doc --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024217-af4c-map-f14`, `20261013-024649-c36e-map-f14`.

Evidence: [F14-files-06-what-format-promises-f14-archive-format-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/map-run/F14-files-06-what-format-promises-f14-archive-format-.json) · [tar.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/F14.archive-format-doc/tar.json) · [F14-files-06-what-format-promises-f14-archive-format-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/map-run/F14-files-06-what-format-promises-f14-archive-format-.json) · [tar.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/F14.archive-format-doc/tar.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Low — Invalid upload target is reported as server failure

Features: `F14.upload-onto-directory`.

**Expected:** Directory target or parent-file collision yields 4xx.

**Observed:** Upload maps both collisions to a masked 500.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F14 --only F14.upload-onto-directory --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024217-af4c-map-f14`, `20261013-024649-c36e-map-f14`.

Evidence: [F14-files-02-upload-onto-a-directory-f14-upload-onto-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/map-run/F14-files-02-upload-onto-a-directory-f14-upload-onto-.json) · [upload.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/F14.upload-onto-directory/upload.json) · [F14-files-02-upload-onto-a-directory-f14-upload-onto-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/map-run/F14-files-02-upload-onto-a-directory-f14-upload-onto-.json) · [upload.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/F14.upload-onto-directory/upload.json) · [F14-files-01-upload-onto-a-directory-f14-upload-onto-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034147-e66e-map-f14/evidence/map-run/F14-files-01-upload-onto-a-directory-f14-upload-onto-.json) · [upload.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034147-e66e-map-f14/evidence/F14.upload-onto-directory/upload.json).

Not filed by this worker: external reporting and publication remain parent-owned. Two additional fresh sibling runs save 500 responses for both existing-directory and parent-is-file collisions.

### Low — Remote upload results omit file_size in Python and TypeScript

Features: `F14.upload-size`.

**Expected:** Both remote clients report the 70000-byte upload size, as LocalWorkspace does.

**Observed:** Bytes upload intact; Python returns None and TypeScript returns undefined for file_size.

```sh
PATH=/workspace/verification-artifacts/f08-f14-harness/.agents/skills/verify-agent-server/scripts:$PATH control-agent-server map run --file F14 --only F14.upload-size --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-024217-af4c-map-f14`, `20261013-024649-c36e-map-f14`.

Evidence: [F14-files-03-upload-size-in-the-consumers-result-f14-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/map-run/F14-files-03-upload-size-in-the-consumers-result-f14-.json) · [rest.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/F14.upload-size/rest.json) · [sdk.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/F14.upload-size/sdk.json) · [ts.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024217-af4c-map-f14/evidence/F14.upload-size/ts.json) · [F14-files-03-upload-size-in-the-consumers-result-f14-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/map-run/F14-files-03-upload-size-in-the-consumers-result-f14-.json) · [rest.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024649-c36e-map-f14/evidence/F14.upload-size/rest.json).

Not filed by this worker: external reporting and publication remain parent-owned.

### Low — A stopped VS Code editor is still advertised with a usable-looking URL

Features: `F16.vscode-url-not-running`.

**Expected:** With enabled=true and running=false, both URL routes return url=null.

**Observed:** Both fresh keyed servers report running=false but the global URL returns a localhost editor URL carrying the redacted session token. The scoped URL-shape controls also return editor URLs.

```sh
control-agent-server map run --file F16 --only F16.vscode-enabled-status,F16.vscode-url-shape,F16.vscode-url-not-running --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-025955-5a37-map-f16`, `20261013-030422-3050-map-f16`.

Evidence: [F16-workspace-serving-and-vscode-03-not-running-still-advertised-f16-vscode-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025955-5a37-map-f16/evidence/map-run/F16-workspace-serving-and-vscode-03-not-running-still-advertised-f16-vscode-.json) · [global.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025955-5a37-map-f16/evidence/F16.vscode-url-not-running/global.json) · [F16-workspace-serving-and-vscode-03-not-running-still-advertised-f16-vscode-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030422-3050-map-f16/evidence/map-run/F16-workspace-serving-and-vscode-03-not-running-still-advertised-f16-vscode-.json) · [global.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030422-3050-map-f16/evidence/F16.vscode-url-not-running/global.json).

The keyless and deferred-init controls return null in both fresh runs. This is a dead-link/metadata defect; the caller already holds the token. The dedicated scoped null assertion follows the failed global assertion and is not reached. Not filed: parent owns external reporting; no issue was filed by this worker.

### Low — Workspace registry no-op mutations unnecessarily create or rewrite the persistence file

Features: `F17.noop-delete-no-file, F17.noop-write-untouched`.

**Expected:** A refused DELETE on a fresh directory must leave workspaces.json absent; re-posting identical registered workspaces must preserve the existing file inode and modification time, as GET does.

**Observed:** Both runs begin with no workspaces.json, return 404 for the two unknown-path deletes, keep both lists empty, then find a newly created file. Later an identical re-add returns 200 with the same registry body as before, but the inode/modification-time equality assertion fails; the preceding GET leaves that equality intact.

```sh
control-agent-server map run --file F17 --only F17.noop-delete-no-file,F17.add-workspaces,F17.wire-format,F17.idempotent-add,F17.delete-workspace,F17.noop-write-untouched --fresh --repeat 2 --record --keep-going --checkout /workspace/agent-sdk-verify
```

Fresh confirmation runs: `20261013-025957-13e4-map-f17`, `20261013-030107-4090-map-f17`.

Evidence: [delete.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025957-13e4-map-f17/evidence/F17.noop-delete-no-file/delete.json) · [F17-workspaces-registry-01-a-refused-delete-on-a-fresh-directory-f1.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025957-13e4-map-f17/evidence/map-run/F17-workspaces-registry-01-a-refused-delete-on-a-fresh-directory-f1.json) · [get.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025957-13e4-map-f17/evidence/F17.delete-workspace/get.json) · [readd.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025957-13e4-map-f17/evidence/F17.noop-write-untouched/readd.json) · [F17-workspaces-registry-06-no-op-writes-leave-the-file-alone-f17-no.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025957-13e4-map-f17/evidence/map-run/F17-workspaces-registry-06-no-op-writes-leave-the-file-alone-f17-no.json) · [delete.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030107-4090-map-f17/evidence/F17.noop-delete-no-file/delete.json).

Grouped file creation and identical-content replacement as one persistence no-op defect. The re-add branch stops at its first failed stamp comparison; subsequent unknown workspace/parent DELETE stamp checks are not reached. F17.noop-write-readonly is blocked by missing chattr and is not included as a verified symptom. Explicit arrange IDs are included because F17 recipes lack Requires declarations. Confirmed on two fresh runs at checkout SHA acca181af1f353975965bcf6486e1d0a58f444c0. Not filed: read-only saved-evidence extraction performed no issue lookup, rerun, or external action.

### Low — Secret GET OpenAPI promises the wrong invalid-name status

Features: `F18.secret-name-contract`.

**Expected:** The published GET /api/settings/secrets/{name} invalid-name status must match the live route response (422), or the route must return its published 400.

**Observed:** Both saved OpenAPI documents say 400 if name format is invalid for GET; GET /api/settings/secrets/1bad returned 422 in both runs, failing the assertion derived from that published description.

```sh
control-agent-server map run --file F18 --only F18.secret-name-contract --fresh --repeat 2 --record --checkout /workspace/agent-sdk-verify
```

Fresh confirmation runs: `20261013-024700-3f62-map-f18`, `20261013-025117-43f0-map-f18`.

Evidence: [openapi.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/fixtures/qa-f18/openapi.json) · [invalid-name.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/F18.secret-name-contract/invalid-name.json) · [F18-settings-and-secrets-06-documented-status-for-an-invalid-name-f1.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024700-3f62-map-f18/evidence/map-run/F18-settings-and-secrets-06-documented-status-for-an-invalid-name-f1.json) · [openapi.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025117-43f0-map-f18/fixtures/qa-f18/openapi.json) · [invalid-name.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025117-43f0-map-f18/evidence/F18.secret-name-contract/invalid-name.json) · [F18-settings-and-secrets-06-documented-status-for-an-invalid-name-f1.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025117-43f0-map-f18/evidence/map-run/F18-settings-and-secrets-06-documented-status-for-an-invalid-name-f1.json).

The saved DELETE description also says 400, but DELETE was not driven by these focused repeats. PUT already documents 422 in both saved OpenAPI documents; the frozen recipe prose claiming PUT also says 400 is stale and is excluded from this confirmed bug. Not filed: this task is read-only saved-evidence extraction; no issue lookup or external action was performed. Both fresh runs used checkout SHA acca181af1f353975965bcf6486e1d0a58f444c0. Reproduction commands are provided for review and were not rerun during extraction.

### Low — An out-of-range OAuth callback port returns 500 instead of a validation error

Features: `F19.oauth-callback-bad-port`.

**Expected:** A callback URL with port 99999 must return 400, as an incorrect in-range port does.

**Observed:** Both runs arrange a local OAuth job awaiting consent, accept the ready-state check, and return 400 Unexpected OAuth callback URL for port 1. Posting port 99999 returns 500 with exception Port out of range 0-65535.

```sh
control-agent-server map run --file F19 --only F19.oauth-callback-bad-port --fresh --repeat 2 --record --keep-going --checkout /workspace/agent-sdk-verify
```

Fresh confirmation runs: `20261013-030153-d95d-map-f19`, `20261013-030348-f557-map-f19`.

Evidence: [port-99999.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030153-d95d-map-f19/evidence/F19.oauth-callback-bad-port/port-99999.json) · [F19-mcp-05-port-out-of-range-f19-oauth-callback-bad.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030153-d95d-map-f19/evidence/map-run/F19-mcp-05-port-out-of-range-f19-oauth-callback-bad.json) · [port-99999.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030348-f557-map-f19/evidence/F19.oauth-callback-bad-port/port-99999.json) · [F19-mcp-05-port-out-of-range-f19-oauth-callback-bad.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030348-f557-map-f19/evidence/map-run/F19-mcp-05-port-out-of-range-f19-oauth-callback-bad.json).

The recipe stops at the port-99999 failure. The subsequent nonnumeric port abc and final still-authorizing check are not reached, so neither is claimed as confirmed. Confirmed on two fresh runs at checkout SHA acca181af1f353975965bcf6486e1d0a58f444c0. Not filed: read-only saved-evidence extraction performed no issue lookup, rerun, or external action.

### Low — Replaying a completed MCP OAuth callback returns an unhandled server error

Features: `F19.oauth-callback-replay`.

**Expected:** Submitting the callback again for a succeeded local OAuth job must return a handled result (200 or a 4xx such as 409).

**Observed:** Both runs complete the local OAuth flow and show the job succeeded/callback_ready=true immediately before replay. The repeated callback POST returns 500 with exception All connection attempts failed.

```sh
control-agent-server map run --file F19 --only F19.oauth-callback-replay --fresh --repeat 2 --record --keep-going --checkout /workspace/agent-sdk-verify
```

Fresh confirmation runs: `20261013-030153-d95d-map-f19`, `20261013-030348-f557-map-f19`.

Evidence: [succeeded.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030153-d95d-map-f19/evidence/F19.oauth-flow/succeeded.json) · [replay.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030153-d95d-map-f19/evidence/F19.oauth-callback-replay/replay.json) · [F19-mcp-04-replayed-callback-f19-oauth-callback-rep.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030153-d95d-map-f19/evidence/map-run/F19-mcp-04-replayed-callback-f19-oauth-callback-rep.json) · [succeeded.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030348-f557-map-f19/evidence/F19.oauth-flow/succeeded.json) · [replay.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030348-f557-map-f19/evidence/F19.oauth-callback-replay/replay.json) · [F19-mcp-04-replayed-callback-f19-oauth-callback-rep.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030348-f557-map-f19/evidence/map-run/F19-mcp-04-replayed-callback-f19-oauth-callback-rep.json).

The assertion stops at the replay response; the later status-unchanged GET is not reached. The frozen map claim about callbacks after consent timeout is not independently exercised. Only the local saved OAuth fixture was involved. Confirmed on two fresh runs at checkout SHA acca181af1f353975965bcf6486e1d0a58f444c0. Not filed: read-only saved-evidence extraction performed no issue lookup, rerun, or external action.

### Low — MCP settings accept a server with neither command nor URL

Features: `F19.settings-empty-server`.

**Expected:** POST /api/settings/mcp/qa-empty with {} must return 422 and leave no stored server.

**Observed:** Both fresh runs confirm the key is initially absent, then POST {} returns 201 with qa-empty={enabled:true} in the returned MCP settings. The recipe removes the accepted entry and fails its explicit false guard.

```sh
control-agent-server map run --file F19 --only F19.settings-empty-server --fresh --repeat 2 --record --keep-going --checkout /workspace/agent-sdk-verify
```

Fresh confirmation runs: `20261013-030153-d95d-map-f19`, `20261013-030348-f557-map-f19`.

Evidence: [create.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030153-d95d-map-f19/evidence/F19.settings-empty-server/create.json) · [F19-mcp-01-server-with-neither-command-nor-url-f19-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030153-d95d-map-f19/evidence/map-run/F19-mcp-01-server-with-neither-command-nor-url-f19-.json) · [create.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030348-f557-map-f19/evidence/F19.settings-empty-server/create.json) · [F19-mcp-01-server-with-neither-command-nor-url-f19-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030348-f557-map-f19/evidence/map-run/F19-mcp-01-server-with-neither-command-nor-url-f19-.json).

Only malformed configuration acceptance is proved. The frozen prose claims this can remove all MCP tools from future conversations, but these focused repeats do not independently drive that downstream behavior; no tool-loss severity claim is made. Confirmed on two fresh runs at checkout SHA acca181af1f353975965bcf6486e1d0a58f444c0. Not filed: read-only saved-evidence extraction performed no issue lookup, rerun, or external action.

### Low — DeepSeek authentication failure is classified as a bad request

Features: `F20.validate-bad-key-type`.

**Expected:** A provider authentication_error should be reported as LLMAuthenticationError.

**Observed:** POST /api/profiles/qa-draft/validate returned 200 valid=false with error.type=LLMBadRequestError, although its redacted provider message contains authentication_error. The saved jq assertion expecting LLMAuthenticationError failed. Both cited fresh targeted repeats reproduce this outcome; the exact per-attempt values are in the saved exchanges/transcripts.

```sh
control-agent-server map run --file F20 --only F20.validate-bad-key-type --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going --timeout 420
```

Fresh confirmation runs: `20261013-030609-7ab0-map-f20`, `20261013-030955-5180-map-f20`.

Evidence: [F20-llm-profiles-01-deepseek-401-type-f20-validate-bad-key-t.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/map-run/F20-llm-profiles-01-deepseek-401-type-f20-validate-bad-key-t.json) · [deepseek-401.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030609-7ab0-map-f20/evidence/F20.validate-bad-key-type/deepseek-401.json) · [F20-llm-profiles-01-deepseek-401-type-f20-validate-bad-key-t.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030955-5180-map-f20/evidence/map-run/F20-llm-profiles-01-deepseek-401-type-f20-validate-bad-key-t.json) · [deepseek-401.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030955-5180-map-f20/evidence/F20.validate-bad-key-type/deepseek-401.json).

The observed failure is error classification; validation honestly returns valid=false and the posted credential is absent from the provider message. The saved exchange does not include a separate upstream HTTP-status capture. Two further fresh targeted confirmations now reproduce the exact marked failures. Not filed: read-only evidence extraction performed no issue lookup or external action.

### Low — Corrupted settings produce an unmapped meta-profile activation error

Features: `F22.corrupt-settings`.

**Expected:** Return 409 like LLM-profile activation and retain the corrupted file.

**Observed:** The LLM-profile control returns 409; meta-profile activation returns 500 for the same corrupted file. The file remains unchanged and is restored.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F22-meta-profiles.md --only F22.save-classes,F22.save-direct,F22.empty-router,F22.activate-acp,F22.corrupt-settings,F22.persistence-dir --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-021742-7d44-map-f22`, `20261013-034317-5724-map-f22`.

Evidence: [activate.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021742-7d44-map-f22/evidence/F22.corrupt-settings/activate.json) · [llm-profile-activate.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021742-7d44-map-f22/evidence/F22.corrupt-settings/llm-profile-activate.json) · [F22-meta-profiles-19-unreadable-settings-f22-corrupt-settings.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021742-7d44-map-f22/evidence/map-run/F22-meta-profiles-19-unreadable-settings-f22-corrupt-settings.json) · [activate.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034317-5724-map-f22/evidence/F22.corrupt-settings/activate.json) · [llm-profile-activate.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034317-5724-map-f22/evidence/F22.corrupt-settings/llm-profile-activate.json) · [F22-meta-profiles-05-unreadable-settings-f22-corrupt-settings.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034317-5724-map-f22/evidence/map-run/F22-meta-profiles-05-unreadable-settings-f22-corrupt-settings.json).

Status/error mapping only; no additional data loss is claimed.

### Low — A meta-profile with no routing mode is accepted

Features: `F22.empty-router`.

**Expected:** Reject a router with neither classes nor direct prompt with 422.

**Observed:** POST with only classifier_model returns 201 and persists an unusable routing configuration.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F22-meta-profiles.md --only F22.save-classes,F22.save-direct,F22.empty-router,F22.activate-acp,F22.corrupt-settings,F22.persistence-dir --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-021742-7d44-map-f22`, `20261013-034317-5724-map-f22`.

Evidence: [save.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021742-7d44-map-f22/evidence/F22.empty-router/save.json) · [F22-meta-profiles-05-router-with-no-route-f22-empty-router-kn.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-021742-7d44-map-f22/evidence/map-run/F22-meta-profiles-05-router-with-no-route-f22-empty-router-kn.json) · [save.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034317-5724-map-f22/evidence/F22.empty-router/save.json) · [F22-meta-profiles-03-router-with-no-route-f22-empty-router-kn.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034317-5724-map-f22/evidence/map-run/F22-meta-profiles-03-router-with-no-route-f22-empty-router-kn.json).

Validation defect; the model validator documents requiring one routing mode. Trap removes the test profile.

### Low — Provider model lists include identifiers from Bedrock

Features: `F23.models-no-bedrock`.

**Expected:** A DeepSeek provider list excludes Bedrock-only deepseek.* identifiers.

**Observed:** Both provider lists contain deepseek.r1-v1:0, deepseek.v3-v1:0, and deepseek.v3.2.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F23-llm-catalog-and-connections.md --only F23.models-no-bedrock,F23.conn-create,F23.conn-create-blank-key,F23.conn-patch-blank-key,F23.validate-linked-draft,F23.store-busy-responsive --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-024155-0956-map-f23`, `20261013-034323-e6ea-map-f23`.

Evidence: [anthropic.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024155-0956-map-f23/evidence/F23.models-no-bedrock/anthropic.json) · [deepseek.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024155-0956-map-f23/evidence/F23.models-no-bedrock/deepseek.json) · [F23-llm-catalog-and-connections-05-no-bedrock-ids-under-a-provider-f23-mode.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-024155-0956-map-f23/evidence/map-run/F23-llm-catalog-and-connections-05-no-bedrock-ids-under-a-provider-f23-mode.json) · [anthropic.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034323-e6ea-map-f23/evidence/F23.models-no-bedrock/anthropic.json) · [deepseek.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034323-e6ea-map-f23/evidence/F23.models-no-bedrock/deepseek.json) · [F23-llm-catalog-and-connections-01-no-bedrock-ids-under-a-provider-f23-mode.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034323-e6ea-map-f23/evidence/map-run/F23-llm-catalog-and-connections-01-no-bedrock-ids-under-a-provider-f23-mode.json).

The same recipe fetches Anthropic as a control, but its later negative assertion is not reached after the DeepSeek failure.

### Low — Offline device-login start returns an unhandled 500

Features: `F24.device-start-offline`.

**Expected:** Return a gateway failure such as 502/503/504 when OpenAI is unreachable.

**Observed:** A real throwaway device code is created and confirmed pending; after its loopback CONNECT relay stops, another device/start returns 500 All connection attempts failed.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F24-openai-subscription.md --only F24.status-offline,F24.device-start-offline --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-025101-09f6-map-f24`, `20261013-034748-623a-map-f24`.

Evidence: [F24-openai-subscription-19-start-and-poll-a-login-offline-f24-devic.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025101-09f6-map-f24/evidence/map-run/F24-openai-subscription-19-start-and-poll-a-login-offline-f24-devic.json) · [start.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025551-44ef-f24-outage/evidence/F24.device-start-offline/start.json) · [F24-openai-subscription-02-start-and-poll-a-login-offline-f24-devic.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034748-623a-map-f24/evidence/map-run/F24-openai-subscription-02-start-and-poll-a-login-offline-f24-devic.json) · [start.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034843-3ace-f24-outage/evidence/F24.device-start-offline/start.json).

No account login was completed. The later offline poll assertion is not reached and is listed as not-run.

### Low — Malformed skill frontmatter produces an unhandled server error

Features: `F25.install-bad-frontmatter`.

**Expected:** Reject malformed YAML frontmatter with a client error.

**Observed:** Skill install returns 500 with the YAML parser exception instead of 422.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F25-skills.md --only F25.marketplace-public,F25.install-bad-frontmatter,F25.install-documented-sources,F25.install-unknown-ref,F25.refresh-unfetchable,F25.sync-offline,F25.marketplace-stale-cache --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-025747-be38-map-f25`, `20261013-034422-49fa-map-f25`.

Evidence: [install.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/F25.install-bad-frontmatter/install.json) · [F25-skills-12-malformed-frontmatter-f25-install-bad-fr.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/map-run/F25-skills-12-malformed-frontmatter-f25-install-bad-fr.json) · [install.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034422-49fa-map-f25/evidence/F25.install-bad-frontmatter/install.json) · [F25-skills-03-malformed-frontmatter-f25-install-bad-fr.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034422-49fa-map-f25/evidence/map-run/F25-skills-03-malformed-frontmatter-f25-install-bad-fr.json).

Synthetic local package; bad-input error mapping only.

### Low — Refreshing a vanished skill or plugin source returns an unmapped 500

Features: `F25.refresh-unfetchable, F26.refresh-unfetchable`.

**Expected:** Refuse an unfetchable source with 400/422 and retain the prior install.

**Observed:** After a local installed source is moved away, both refresh endpoints return 500 with ExtensionFetchError.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F25-skills.md --only F25.marketplace-public,F25.install-bad-frontmatter,F25.install-documented-sources,F25.install-unknown-ref,F25.refresh-unfetchable,F25.sync-offline,F25.marketplace-stale-cache --fresh --record --keep-going --timeout 360
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F26-plugins.md --only F26.install-repo-root-name,F26.install-documented-source,F26.refresh-unfetchable,F26.conversation-resume-disabled --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-025747-be38-map-f25`, `20261013-030021-e114-map-f26`, `20261013-034422-49fa-map-f25`, `20261013-034505-0581-map-f26`.

Evidence: [refresh.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/F25.refresh-unfetchable/refresh.json) · [F25-skills-20-refresh-of-a-vanished-source-f25-refresh.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/map-run/F25-skills-20-refresh-of-a-vanished-source-f25-refresh.json) · [vanished.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030021-e114-map-f26/evidence/F26.refresh-unfetchable/vanished.json) · [F26-plugins-16-unfetchable-refresh-f26-refresh-unfetcha.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030021-e114-map-f26/evidence/map-run/F26-plugins-16-unfetchable-refresh-f26-refresh-unfetcha.json) · [refresh.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034422-49fa-map-f25/evidence/F25.refresh-unfetchable/refresh.json) · [F25-skills-08-refresh-of-a-vanished-source-f25-refresh.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034422-49fa-map-f25/evidence/map-run/F25-skills-08-refresh-of-a-vanished-source-f25-refresh.json).

Grouped shared fetch-error mapping; each endpoint independently reproduced twice. Later preservation assertions are not reached after the status failure.

### Low — Skills sync reports success after its git fetch fails

Features: `F25.sync-offline`.

**Expected:** Report an unsuccessful forced refresh when its origin cannot be fetched.

**Observed:** A direct git fetch proves the configured origin is unreachable, but POST /api/skills/sync returns status=success and Skills repository synced successfully.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F25-skills.md --only F25.marketplace-public,F25.install-bad-frontmatter,F25.install-documented-sources,F25.install-unknown-ref,F25.refresh-unfetchable,F25.sync-offline,F25.marketplace-stale-cache --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-025747-be38-map-f25`, `20261013-034422-49fa-map-f25`.

Evidence: [sync.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/F25.sync-offline/sync.json) · [F25-skills-24-sync-without-a-reachable-origin-f25-sync.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025747-be38-map-f25/evidence/map-run/F25-skills-24-sync-without-a-reachable-origin-f25-sync.json) · [sync.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034422-49fa-map-f25/evidence/F25.sync-offline/sync.json) · [F25-skills-10-sync-without-a-reachable-origin-f25-sync.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034422-49fa-map-f25/evidence/map-run/F25-skills-10-sync-without-a-reachable-origin-f25-sync.json).

Response metadata defect; retaining the cached clone is permissible, but the forced sync result is inaccurate.

### Low — Manifestless repository plugins inherit the cache hash in their name

Features: `F26.install-repo-root-name`.

**Expected:** A manifestless repository installs under its repository directory name.

**Observed:** The source qa-f26-src installs as qa-f26-src-<16 hex>, derived from its URL-hashed cache directory.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F26-plugins.md --only F26.install-repo-root-name,F26.install-documented-source,F26.refresh-unfetchable,F26.conversation-resume-disabled --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-030021-e114-map-f26`, `20261013-034505-0581-map-f26`.

Evidence: [install.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030021-e114-map-f26/evidence/F26.install-repo-root-name/install.json) · [F26-plugins-07-repository-root-name-f26-install-repo-ro.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030021-e114-map-f26/evidence/map-run/F26-plugins-07-repository-root-name-f26-install-repo-ro.json) · [install.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034505-0581-map-f26/evidence/F26.install-repo-root-name/install.json) · [F26-plugins-01-repository-root-name-f26-install-repo-ro.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034505-0581-map-f26/evidence/map-run/F26-plugins-01-repository-root-name-f26-install-repo-ro.json).

Metadata/naming defect; fixture is removed before the assertion.

### Low — Resuming without the registered custom tool module returns an unhandled 500

Features: `F27.custom-tool-missing-on-resume`.

**Expected:** Report a missing custom-module prerequisite with a controlled client error.

**Observed:** After the real custom-tool turn persists its observation, restart without its module makes message POST return 500 because the observation discriminator is not registered.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F27-hooks-subagents-tools.md --only F27.subagents-bad-skill,F27.custom-tool-modules,F27.custom-tool-missing-on-resume --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-030559-0256-map-f27`, `20261013-034502-5a13-map-f27`.

Evidence: [send.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030559-0256-map-f27/evidence/F27.custom-tool-missing-on-resume/send.json) · [F27-hooks-subagents-tools-24-tool-module-gone-on-resume-f27-custom-to.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030559-0256-map-f27/evidence/map-run/F27-hooks-subagents-tools-24-tool-module-gone-on-resume-f27-custom-to.json) · [send.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034502-5a13-map-f27/evidence/F27.custom-tool-missing-on-resume/send.json) · [F27-hooks-subagents-tools-03-tool-module-gone-on-resume-f27-custom-to.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034502-5a13-map-f27/evidence/map-run/F27-hooks-subagents-tools-03-tool-module-gone-on-resume-f27-custom-to.json).

The initial custom tool executes successfully on real DeepSeek in both proofs; missing-module errors are not claimed as successful restores.

### Low — Server info advertises the browser despite enable_browser=false

Features: `F27.server-info-browser-disabled`.

**Expected:** The server-info usable_tools agrees with the config-aware catalog.

**Observed:** Catalog browser usability is false on the disabled server, but server_info still includes browser_tool_set.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F27-browser-config.md --fresh --record --keep-going --timeout 240
```

Fresh confirmation runs: `20261013-030559-0256-map-f27`, `20261013-035121-8592-map-f27`.

Evidence: [server-info.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030559-0256-map-f27/evidence/F27.server-info-browser-disabled/server-info.json) · [F27-hooks-subagents-tools-29-usable-tools-with-the-browser-disabled-f.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030559-0256-map-f27/evidence/map-run/F27-hooks-subagents-tools-29-usable-tools-with-the-browser-disabled-f.json) · [server-info.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-035121-8592-map-f27/evidence/F27.server-info-browser-disabled/server-info.json) · [F27-browser-config-02-server-info-browser-disabled-f27-server-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-035121-8592-map-f27/evidence/map-run/F27-browser-config-02-server-info-browser-disabled-f27-server-.json).

Metadata inconsistency. The fresh supplement retains the real host Chromium rather than requiring an unnecessary cache symlink.

### Low — A sub-agent with an absent configured skill causes message POST 500

Features: `F27.subagents-bad-skill`.

**Expected:** Reject invalid agent configuration or return a client error when it is used.

**Observed:** The conversation is created, but appending a user message returns 500 Skill ... not found but was given to agent ...

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F27-hooks-subagents-tools.md --only F27.subagents-bad-skill,F27.custom-tool-modules,F27.custom-tool-missing-on-resume --fresh --record --keep-going --timeout 360
```

Fresh confirmation runs: `20261013-030559-0256-map-f27`, `20261013-034502-5a13-map-f27`.

Evidence: [send-control.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030559-0256-map-f27/evidence/F27.subagents-bad-skill/send-control.json) · [send.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030559-0256-map-f27/evidence/F27.subagents-bad-skill/send.json) · [F27-hooks-subagents-tools-15-agent-with-a-missing-skill-f27-subagents.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030559-0256-map-f27/evidence/map-run/F27-hooks-subagents-tools-15-agent-with-a-missing-skill-f27-subagents.json) · [send-control.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034502-5a13-map-f27/evidence/F27.subagents-bad-skill/send-control.json) · [send.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034502-5a13-map-f27/evidence/F27.subagents-bad-skill/send.json) · [F27-hooks-subagents-tools-01-agent-with-a-missing-skill-f27-subagents.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034502-5a13-map-f27/evidence/map-run/F27-hooks-subagents-tools-01-agent-with-a-missing-skill-f27-subagents.json).

Bad configuration/error-mapping defect, not a model failure.

### Low — Disabled-browser servers still list the browser-only built-in agent

Features: `F27.subagents-browser-disabled`.

**Expected:** Exclude the browser-only web-researcher when enable_browser=false.

**Observed:** The catalog marks browser_tool_set unusable, but built-in discovery still returns web-researcher.

```sh
.venv/bin/python /workspace/verification-artifacts/takeover-f22-f28/run-map.py map run --file F27-browser-config.md --fresh --record --keep-going --timeout 240
```

Fresh confirmation runs: `20261013-030559-0256-map-f27`, `20261013-035121-8592-map-f27`.

Evidence: [builtins.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030559-0256-map-f27/evidence/F27.subagents-browser-disabled/builtins.json) · [F27-hooks-subagents-tools-30-browser-only-sub-agent-with-the-browser-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-030559-0256-map-f27/evidence/map-run/F27-hooks-subagents-tools-30-browser-only-sub-agent-with-the-browser-.json) · [builtins.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-035121-8592-map-f27/evidence/F27.subagents-browser-disabled/builtins.json) · [F27-browser-config-03-subagents-browser-disabled-f27-subagents.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-035121-8592-map-f27/evidence/map-run/F27-browser-config-03-subagents-browser-disabled-f27-subagents.json).

Only discovery was driven; no browser delegation or configuration bypass is claimed.

### Low — Matching-checksum non-gzip backend archive returns unhandled 500

Features: `F28.prepare-corrupt-archive`.

**Expected:** POST backend/prepare rejects invalid archive format with HTTP 409 and records no approval.

**Observed:** Both fresh runs return HTTP 500 with exception not a gzip file after checksum validation.

```sh
control-agent-server map run --file F28 --only F28.prepare-corrupt-archive --fresh --repeat 2 --record
```

Fresh confirmation runs: `20261013-025047-4da6-map-f28`, `20261013-025217-c43a-map-f28`.

Evidence: [prepare.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025047-4da6-map-f28/evidence/F28.prepare-corrupt-archive/prepare.json) · [F28-canvas-extensions-01-non-gzip-artifact-f28-prepare-corrupt-ar.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025047-4da6-map-f28/evidence/map-run/F28-canvas-extensions-01-non-gzip-artifact-f28-prepare-corrupt-ar.json) · [prepare.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025217-c43a-map-f28/evidence/F28.prepare-corrupt-archive/prepare.json) · [F28-canvas-extensions-01-non-gzip-artifact-f28-prepare-corrupt-ar.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-025217-c43a-map-f28/evidence/map-run/F28-canvas-extensions-01-non-gzip-artifact-f28-prepare-corrupt-ar.json).

tarfile.ReadError escapes the router ValueError mapping. The case stops at this invalid-format assertion; later no-write checks in the recipe are not reached.

### Low — Canvas bridge keeps crashed backend ready until status polling

Features: `F29.backend-crash-detected`.

**Expected:** After the backend process exits, requests should return 503 backend not ready.

**Observed:** Without a status poll, requests return 502 Conversation container unreachable for the entire 15-second observation.

```sh
control-agent-server map run --file F29 --only F29.backend-crash-detected --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031857-df62-map-f29`, `20261013-031947-956c-map-f29`.

Evidence: [F29-app-backend-bridge-06-crash-seen-by-the-bridge-f29-backend-cra.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031857-df62-map-f29/evidence/map-run/F29-app-backend-bridge-06-crash-seen-by-the-bridge-f29-backend-cra.json) · [F29-app-backend-bridge-06-crash-seen-by-the-bridge-f29-backend-cra.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031947-956c-map-f29/evidence/map-run/F29-app-backend-bridge-06-crash-seen-by-the-bridge-f29-backend-cra.json).

### Low — Canvas proxy sends duplicate Date and Server headers

Features: `F29.proxy-response-headers`.

**Expected:** A proxied response should contain one Date and one Server header.

**Observed:** Uvicorn adds its headers alongside copied backend headers, producing comma-joined duplicate values.

```sh
control-agent-server map run --file F29 --only F29.proxy-response-headers --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031857-df62-map-f29`, `20261013-031947-956c-map-f29`.

Evidence: [F29-app-backend-bridge-04-one-date-and-server-header-f29-proxy-res.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031857-df62-map-f29/evidence/map-run/F29-app-backend-bridge-04-one-date-and-server-header-f29-proxy-res.json) · [F29-app-backend-bridge-04-one-date-and-server-header-f29-proxy-res.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031947-956c-map-f29/evidence/map-run/F29-app-backend-bridge-04-one-date-and-server-header-f29-proxy-res.json).

### Low — Canvas bare-root query parameter changes the proxied path

Features: `F29.proxy-root-path-query`.

**Expected:** ?path=echo on the bare app root should reach the root with the query unchanged.

**Observed:** The proxy sends the request to /echo, whereas the trailing-slash root preserves /.

```sh
control-agent-server map run --file F29 --only F29.proxy-root-path-query --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031857-df62-map-f29`, `20261013-031947-956c-map-f29`.

Evidence: [F29-app-backend-bridge-02-root-path-parameter-f29-proxy-root-path-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031857-df62-map-f29/evidence/map-run/F29-app-backend-bridge-02-root-path-parameter-f29-proxy-root-path-.json) · [F29-app-backend-bridge-02-root-path-parameter-f29-proxy-root-path-.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031947-956c-map-f29/evidence/map-run/F29-app-backend-bridge-02-root-path-parameter-f29-proxy-root-path-.json).

### Low — Canvas bridge trusts a forwarded scheme despite its setting

Features: `F29.session-forwarded-proto`.

**Expected:** With trust_forwarded_headers disabled, X-Forwarded-Proto should not alter an otherwise valid request.

**Observed:** The same session bootstrap succeeds without the header and returns 421 when X-Forwarded-Proto: https is supplied.

```sh
control-agent-server map run --file F29 --only F29.session-forwarded-proto --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031857-df62-map-f29`, `20261013-031947-956c-map-f29`.

Evidence: [F29-app-backend-bridge-01-forwarded-proto-f29-session-forwarded-pr.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031857-df62-map-f29/evidence/map-run/F29-app-backend-bridge-01-forwarded-proto-f29-session-forwarded-pr.json) · [F29-app-backend-bridge-01-forwarded-proto-f29-session-forwarded-pr.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031947-956c-map-f29/evidence/map-run/F29-app-backend-bridge-01-forwarded-proto-f29-session-forwarded-pr.json).

### Low — Server-selected per-process tmux directory survives shutdown

Features: `F31.tmux-dir-cleanup`.

**Expected:** The per-process TMUX_TMPDIR selected by the server should disappear after graceful stop.

**Observed:** The directory remains; the recipe's cleanup trap removes it after recording the failed assertion.

```sh
/workspace/verification-artifacts/harness-f29-f34/.agents/skills/verify-agent-server/scripts/control-agent-server map run --file F31 --only F31.tmux-dir-cleanup --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031657-8509-map-f31`, `20261013-031758-c007-map-f31`.

Evidence: [F31-persistence-and-limits-01-per-process-tmux-directory-removed-on-st.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031657-8509-map-f31/evidence/map-run/F31-persistence-and-limits-01-per-process-tmux-directory-removed-on-st.json) · [F31-persistence-and-limits-01-per-process-tmux-directory-removed-on-st.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031758-c007-map-f31/evidence/map-run/F31-persistence-and-limits-01-per-process-tmux-directory-removed-on-st.json).

[
  "Isolated copied recipe adjusts only exited-zombie setup observation; frozen product source and bug assertion unchanged. See F31-zombie-adaptation.md."
]

### Low — Full webhook buffer waits behind an in-flight batch

Features: `F32.buffer-stranded`.

**Expected:** The queued user message should reach the sink within ten seconds once the buffer fills.

**Observed:** The first batch is posted, while a second full buffer waits for the long flush timer or a later close.

```sh
control-agent-server map run --file F32 --only F32.buffer-stranded --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031700-aa28-map-f32`, `20261013-032530-35b4-map-f32`.

Evidence: [F32-webhooks-and-telemetry-02-events-stranded-behind-an-in-flight-batc.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031700-aa28-map-f32/evidence/map-run/F32-webhooks-and-telemetry-02-events-stranded-behind-an-in-flight-batc.json) · [F32-webhooks-and-telemetry-02-events-stranded-behind-an-in-flight-batc.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032530-35b4-map-f32/evidence/map-run/F32-webhooks-and-telemetry-02-events-stranded-behind-an-in-flight-batc.json).

### Low — Telemetry schema promises a random fallback instead of secret key

Features: `F32.telemetry-salt-docs`.

**Expected:** The salt description should state that the configured secret key is the first fallback.

**Observed:** It promises per-process random salt and unlinkability across runs although the secret-key-derived reference remains stable across restarts.

```sh
control-agent-server map run --file F32 --only F32.telemetry-salt-docs --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031700-aa28-map-f32`, `20261013-032530-35b4-map-f32`.

Evidence: [F32-webhooks-and-telemetry-16-salt-description-f32-telemetry-salt-docs.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031700-aa28-map-f32/evidence/map-run/F32-webhooks-and-telemetry-16-salt-description-f32-telemetry-salt-docs.json) · [F32-webhooks-and-telemetry-16-salt-description-f32-telemetry-salt-docs.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032530-35b4-map-f32/evidence/map-run/F32-webhooks-and-telemetry-16-salt-description-f32-telemetry-salt-docs.json).

### Low — Conversation outcome telemetry misses real token and cost usage

Features: `F32.telemetry-usage-buckets`.

**Expected:** A real model run's outcome should contain measured usage buckets.

**Observed:** The conversation has positive token usage but outcome total_tokens_bucket and cost_bucket are unknown.

```sh
control-agent-server map run --file F32 --only F32.telemetry-usage-buckets --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031700-aa28-map-f32`, `20261013-032530-35b4-map-f32`.

Evidence: [F32-webhooks-and-telemetry-10-token-and-cost-buckets-from-real-usage-f.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031700-aa28-map-f32/evidence/map-run/F32-webhooks-and-telemetry-10-token-and-cost-buckets-from-real-usage-f.json) · [F32-webhooks-and-telemetry-10-token-and-cost-buckets-from-real-usage-f.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032530-35b4-map-f32/evidence/map-run/F32-webhooks-and-telemetry-10-token-and-cost-buckets-from-real-usage-f.json).

### Low — Webhook schema documents the wrong event path and timer

Features: `F32.webhook-spec-docs`.

**Expected:** OpenAPI should describe the per-conversation event path and a timer started by the first event.

**Observed:** It says events go to /events and the timer resets with every new event; live behavior differs.

```sh
control-agent-server map run --file F32 --only F32.webhook-spec-docs --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-031700-aa28-map-f32`, `20261013-032530-35b4-map-f32`.

Evidence: [F32-webhooks-and-telemetry-04-webhook-field-descriptions-f32-webhook-s.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-031700-aa28-map-f32/evidence/map-run/F32-webhooks-and-telemetry-04-webhook-field-descriptions-f32-webhook-s.json) · [F32-webhooks-and-telemetry-04-webhook-field-descriptions-f32-webhook-s.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-032530-35b4-map-f32/evidence/map-run/F32-webhooks-and-telemetry-04-webhook-field-descriptions-f32-webhook-s.json).

### Low — Unimportable custom tool produces an unhandled server error

Features: `F33.custom-tool-module-unimportable`.

**Expected:** A client tool the server cannot import should result in a 4xx or a recorded conversation error.

**Observed:** Creation succeeds with 201, then sending the message fails with 500 for the unregistered tool.

```sh
control-agent-server map run --file F33 --only F33.custom-tool-module-unimportable --checkout /workspace/agent-sdk-verify --fresh --repeat 2 --record --keep-going
```

Fresh confirmation runs: `20261013-033440-1239-map-f33`, `20261013-034709-4e02-map-f33`.

Evidence: [F33-sdk-remote-client-26-an-agent-tool-the-server-cannot-import-f.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-033440-1239-map-f33/evidence/map-run/F33-sdk-remote-client-26-an-agent-tool-the-server-cannot-import-f.json) · [F33-sdk-remote-client-26-an-agent-tool-the-server-cannot-import-f.json](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/evidence/20261013-034709-4e02-map-f33/evidence/map-run/F33-sdk-remote-client-26-an-agent-tool-the-server-cannot-import-f.json).
## Harness and map corrections / drift

```json
{
  "title": "Some F05/F06 isolated recipe selections omit state prerequisites",
  "actual": "Requires clauses omit earlier recipes whose variables or conversation state are consumed. Repro selections explicitly include the prerequisite IDs; shared files were not changed."
}
```

```json
{
  "title": "Cold OpenAPI generation exceeded doctor timeout under concurrent load",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F02-repro-doctor.json",
    "/workspace/verification-artifacts/family-results/F02-repro-doctor-retry.json"
  ],
  "actual": "The first doctor had only the OpenAPI check fail with ReadTimeout. After cache warmup the identical doctor was clean, with health/auth/build checks and no log tracebacks. Treat as transient timing; not counted as a product bug."
}
```

```json
{
  "title": "Shared overlay filled during verification",
  "actual": "ENOSPC interrupted first primary F02 and first F04 repro save_evidence; empty F04-F07 repro summaries followed. Existing F01, F02-repro and F03-repro summaries were valid. After space restoration the incomplete families were restarted, preserving prior evidence. No bug conclusion uses ENOSPC attempts.",
  "runs": [
    "/workspace/verification-artifacts/runs/20261013-022642-a649-map-f02",
    "/workspace/verification-artifacts/runs/20261013-023639-adff-map-f04"
  ]
}
```

```json
{
  "title": "Hard-restart lease checks encounter unreaped PID-1 zombies",
  "feature_ids": [
    "F05.restart-hard-running",
    "F05.pause-running-crash"
  ],
  "actual": "Original crash recipes fail before the target pause assertion because os.kill(owner_pid, 0) still succeeds for the killed zombie process. The recipe copy waits the recorded lease TTL and restarts; ordinary running recovery then passes and pause-loss reproduces.",
  "adaptation": "/workspace/verification-artifacts/adapted-f05/feature-map/F05-run-pause-interrupt.md",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F05-lease-adapted-repro.json"
  ]
}
```

```json
{
  "id": "cold-doctor-timeout",
  "title": "Cold OpenAPI doctor probe times out under CPU contention",
  "actual": "F08.secrets-restart, F10.restart-persist and F14 upload-atomic/restart stop at the required OpenAPI read while health/auth/SHA/socket checks pass.",
  "adaptation": "Isolated map copies retry doctor once; original timeout evidence is preserved.",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F08-doctor-after-surprises.json"
  ],
  "notes": "Original doctor probes use http_client(10); no product code changed."
}
```

```json
{
  "id": "F09-subscription-race",
  "title": "Mid-run recipes start before socket subscription",
  "feature_ids": [
    "F09.switch-llm-mid-run",
    "F09.switch-llm-mid-run-get"
  ],
  "actual": "Primary capture contains the sleep observation but misses its earlier ActionEvent.",
  "adaptation": "Create with --no-run, wait for socket full_state, then POST /run; same real DeepSeek prompt and assertions."
}
```

```json
{
  "id": "missing-selected-dependencies",
  "title": "Selected restart recipes omit state-arranging dependencies",
  "feature_ids": [
    "F10.restart-persist",
    "F14.restart"
  ],
  "adaptation": "Added F10.fork-independent/navigate-empty and F14.upload-download/scoped-transfer in isolated copies."
}
```

```json
{
  "id": "F12-blocked-label",
  "title": "Docker recipe remains unconditionally blocked on a capable host",
  "feature_ids": [
    "F12.docker-runtime"
  ],
  "adaptation": "Removed blocked label only in isolated copy, selected frozen-source image, added own-container safe inspection and missing lifecycle assertions."
}
```

```json
{
  "id": "F12-no-daemon-precondition",
  "title": "Docker error-path recipe assumes no daemon without arranging it",
  "feature_ids": [
    "F12.docker-runtime-contract"
  ],
  "adaptation": "Explicit missing DOCKER_HOST Unix socket ensures intended no-daemon path."
}
```

```json
{
  "id": "unknown-runtime-credential-redaction",
  "severity": "high",
  "confirmed": true,
  "title": "Harness does not automatically redact newly issued container session credentials",
  "actual": "Redactor recognizes run keys and selected env values, rather than the session_api_key response field.",
  "adaptation": "Capture raw output directly, reveal only boolean presence proof, register key via recognized OPENHANDS_API_KEY env before recording exchanges.",
  "notes": "Two fresh compatible-image observations safely printed only the boolean marker for an unmasked newly issued runtime key. The captured key was registered under OPENHANDS_API_KEY before evidence/attach. No credential value was printed or published. This is a harness gap, excluded from product-defect counts.",
  "runs": [
    "/workspace/verification-artifacts/runs/20261013-035149-9cf7-map-f12",
    "/workspace/verification-artifacts/runs/20261013-035150-c7fa-map-f12"
  ],
  "evidence": [
    "/workspace/verification-artifacts/runs/20261013-035149-9cf7-map-f12/evidence/map-run/F12-runtime-and-credentials-01-docker-runtime-with-a-daemon-f12-docker-.json",
    "/workspace/verification-artifacts/runs/20261013-035150-c7fa-map-f12/evidence/map-run/F12-runtime-and-credentials-01-docker-runtime-with-a-daemon-f12-docker-.json"
  ]
}
```

```json
{
  "id": "disk-exhaustion",
  "title": "Docker build filled 32GB overlay and aborted evidence writes",
  "feature_ids": [
    "F12.managed-key-refresh",
    "F12.managed-key-scope",
    "F12.managed-key-switch",
    "F12.docker-runtime-contract",
    "F14.trajectory-init-path"
  ],
  "actual": "ENOSPC left primary F12.json/F14.json empty, with 27/29 feature ledger rows intact.",
  "recovery": "Root removed only owned disposable Docker build caches; 26GB free; affected tails replayed separately.",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F12-primary-aborted.json",
    "/workspace/verification-artifacts/family-results/F14-primary-aborted.json"
  ]
}
```

```json
{
  "id": "Docker-layout-and-owner-permissions",
  "feature_ids": [
    "F12.docker-runtime"
  ],
  "classification": "harness image setup",
  "detail": "Earlier image stored source/venv under the runtime-mounted /workspace. Relocation fixed the vanished entrypoint, then copied mode 700 root-owned virtualenv bin blocked UID 1000. Both failure variants are preserved as harness evidence. Local-uid artifact relocates public source/deps and grants read/traverse permissions; actual UID 1000 plus empty-/workspace import proof passes.",
  "evidence": [
    "/workspace/verification-artifacts/docker/runtime-layout-permissions.txt",
    "/workspace/verification-artifacts/docker/runtime-uid-imports-proof.json"
  ]
}
```

```json
{
  "id": "Docker-vfs-transport-deadline",
  "feature_ids": [
    "F12.docker-runtime"
  ],
  "classification": "environment/harness timing",
  "detail": "Two compatible-image creates returned 201 in 86,055 ms and 82,971 ms. CLI default 30-second transport deadline interrupted earlier local vfs provisioning. Create/reprovision now allow 180 seconds. The configured child health deadline remains unchanged."
}
```

```json
{
  "id": "Docker-persisted-history-route",
  "feature_ids": [
    "F12.docker-runtime"
  ],
  "classification": "map drift",
  "detail": "Frozen registry deliberately mounts outer persisted event reads before the runtime proxy. Events/search with X-Expose-Secrets returns 200; the refusal guard belongs to proxy_http. Copied recipe records persisted-history200 and tests 422 on an actual proxied scoped bash read."
}
```

```json
{
  "feature_ids": [
    "F15.commits"
  ],
  "classification": "map drift",
  "detail": "Copied recipe now accepts valid ISO 8601 UTC Z timestamps and declares Requires: F15.changes-base for the feature-branch fixture. The first supplemental selective history attempt lacked that fixture and is discarded as a harness failure. Two further fresh corrected history attempts pass every assertion. Product checkout unchanged."
}
```

```json
{
  "feature_ids": [
    "F15.ts-client",
    "F17"
  ],
  "classification": "environment and shared build race",
  "detail": "Initial npm cache/build race attempts discarded. Parent centrally rebuilt TypeScript. F15.ts-client passes in both fresh bug-reproduction runs; clean F17 full map has22 passes,2 expected failures and one chattr environment failure."
}
```

```json
{
  "feature_ids": [
    "F15.repo-search-unreachable",
    "F16.vscode-enabled-status"
  ],
  "classification": "load transient/harness cascading state",
  "detail": "Initial cold OpenAPI doctor exceeded its fixed10-second timeout under shared load. Fresh F16 enabled-status/doctor and dependent URL-shape/no-key/deferred-init controls pass twice. F15 recovery warms OpenAPI before the unchanged doctor in a copied recipe."
}
```

```json
{
  "feature_ids": [
    "F17.noop-write-untouched"
  ],
  "classification": "missing Requires",
  "detail": "Selective reproduction must explicitly include add-workspaces, wire-format, idempotent-add, delete-workspace prerequisites because family contains no Requires declarations."
}
```

```json
{
  "feature_ids": [
    "F20.sdk-get-llm-linked",
    "F20.no-cipher",
    "F21.ts-client"
  ],
  "classification": "environment ENOSPC",
  "detail": "ENOSPC interrupted initial runs at02:39. Evidence preserved. Fresh complete replacement F20 has30 pass/6 xfail and F21 has29 pass/4 xfail. No disk-incident failure is counted as a product defect."
}
```

```json
{
  "feature_ids": [
    "F21.dangling-llm-report"
  ],
  "classification": "source/map documentation drift",
  "status": "excluded-from-product-bugs",
  "expected": "The private seed-helper prose should describe materialize diagnostics using the publicly declared llm_profile_ref and llm_profile_resolved fields.",
  "actual": "The saved materialize body conforms to the public response model: valid=false, llm_profile_ref=qa-f21-missing, llm_profile_resolved=false, and an errors entry naming the missing profile. It has no dangling_llm_profile_ref field, and the public AgentProfileDiagnostics model and generated schema do not declare that field. The private seed helper docstring alone promises it; the recipe conditionally asserts it after grepping that docstring.",
  "runs": [
    "/workspace/verification-artifacts/runs/20261013-024523-a1a8-map-f21"
  ],
  "evidence": [
    "/workspace/verification-artifacts/runs/20261013-024523-a1a8-map-f21/evidence/F21.dangling-llm-report/materialize.json",
    "/workspace/verification-artifacts/runs/20261013-024523-a1a8-map-f21/evidence/map-run/F21-agent-profiles-30-how-a-dangling-llm-reference-is-reported.json"
  ],
  "source_references": [
    "/workspace/agent-sdk-verify/openhands-agent-server/openhands/agent_server/agent_profiles_router.py:181",
    "/workspace/agent-sdk-verify/openhands-agent-server/openhands/agent_server/agent_profiles_router.py:545",
    "/workspace/agent-sdk-verify/openhands-sdk/openhands/sdk/profiles/resolver.py:86",
    "/workspace/agent-sdk-verify/clients/typescript/src/generated/agent-server-schema.ts:1975"
  ],
  "notes": "No missing public-contract field or dishonest diagnostics response is established. Fix the seed docstring/map expectation rather than require a new redundant response field; no shared source or map was changed during extraction."
}
```

```json
{
  "feature_ids": [
    "F18.secret-name-contract"
  ],
  "classification": "map drift",
  "detail": "Frozen prose says PUT documents400, but saved OpenAPI already documents422 for PUT. Only GET documentation/status mismatch is confirmed; DELETE branch was not reached."
}
```

```json
{
  "feature_ids": [
    "F15.repo-search-github"
  ],
  "classification": "Old capability blocker removed; live positive checks verified; negative control limited by environment",
  "detail": "An isolated frozen skill copy removes only the predeclared blocked marker. QA_GITHUB_TOKEN is privately assigned from the supplied credential and registered as OPENHANDS_API_KEY for CLI redaction. Product source remains unchanged. Only the public target identity should remain in exported repository names and URLs.",
  "evidence": [
    "/workspace/verification-artifacts/F15-github-live-adaptation.md",
    "/workspace/verification-artifacts/F15-github-live-adaptation.patch"
  ],
  "harness_copy": "/workspace/verification-artifacts/github-live-harness"
}
```

```json
{
  "feature_ids": [
    "F23",
    "F28"
  ],
  "kind": "environment_disk_exhaustion",
  "actual": "The 32 GB overlay filled during unrelated Docker VFS verification. F23/F28 replay aborted with ENOSPC while saving evidence and arranging fixtures; these attempts are excluded from product confirmations and are being rerun after 26 GB was freed.",
  "runs": [
    "/workspace/verification-artifacts/runs/20261013-022431-19cb-map-f23",
    "/workspace/verification-artifacts/runs/20261013-023125-701d-map-f28",
    "/workspace/verification-artifacts/runs/20261013-023753-d1da-map-f22"
  ],
  "notes": "All three affected run process groups were stopped through their explicit CLI --run selection. Partial ledgers are preserved. The last F22 directory was an unstarted confirmation attempt with zero evidence files."
}
```

```json
{
  "feature_ids": [
    "F22.store-busy"
  ],
  "kind": "harness_timing_fragility",
  "actual": "Full replay failed shell elapsed <=33s, while the saved HTTP exchange correctly returned 503 after 30360 ms. CLI startup overhead under concurrent load is included in shell SECONDS.",
  "evidence": [
    "/workspace/verification-artifacts/runs/20261013-021742-7d44-map-f22/evidence/map-run/F22-meta-profiles-20-store-busy-f22-store-busy.json",
    "/workspace/verification-artifacts/runs/20261013-021742-7d44-map-f22/evidence/F22.store-busy/save.json"
  ],
  "notes": "The subsequent DELETE timeout step was not reached in this raw bullet. This failure does not count as a product bug."
}
```

```json
{
  "feature_ids": [
    "F22.activate-acp",
    "F22.corrupt-settings",
    "F22.store-busy-responsive"
  ],
  "kind": "undeclared_state_prerequisites",
  "actual": "Several --only recipes depend on earlier state without declaring Requires. Activation and corrupted-settings need qa-direct active; responsive lock needs an existing meta-profile store directory.",
  "notes": "Explicit prerequisite IDs or CLI setup restore reviewable reproduction. A discarded exploratory lock subset used save-direct alone, which saved the needed directory but failed its list-count assertion; neither exploratory attempt is used in the confirmed-bug count."
}
```

```json
{
  "feature_ids": [
    "F28.restart-persistence",
    "F28.uninstall"
  ],
  "kind": "map_count_drift",
  "expected": "Unrelated installed-app counts 6 before uninstall and5 after.",
  "actual": "New early qa-f28-flaky fixture installed by backend-stop makes counts7 and6; behavior checks after the obsolete count assert were skipped.",
  "runs": [
    "/workspace/verification-artifacts/runs/20261013-024207-5ac2-map-f28"
  ],
  "notes": "Fresh independent core persistence/uninstall supplement planned; no shared recipe edit."
}
```

```json
{
  "feature_ids": [
    "F24.status-offline",
    "F24.device-start-offline"
  ],
  "kind": "discarded_arrangement_attempt",
  "actual": "The first copied precondition had incorrect indentation and did not carry its fixture variables into selected bullets. No bug assertion was reached; the corrected fresh replay reaches both markers.",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F24-repro-arrangement-invalid.json",
    "/workspace/verification-artifacts/family-results/F24-repro.json"
  ]
}
```

```json
{
  "feature_ids": [
    "F27.browser-disabled-launch",
    "F27.browser-disabled",
    "F27.catalog-docker-runtime"
  ],
  "kind": "host_chromium_layout_assumption",
  "actual": "The host already has standard Chromium. Primary negative-probe checks and cache-symlink assertions fail as preconditions, not product behavior. The focused config/catalog supplement uses the actual host layout and proves the remaining ordinary branches.",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F27-browser-config-repro.json"
  ]
}
```

```json
{
  "feature_ids": [
    "F28.backend-stop",
    "F28.status-exit-hang"
  ],
  "kind": "pid1_zombie_observation_limit",
  "actual": "The parent/child stop APIs and status transitions return their expected values, but kill -0 continues to see unreaped zombies. A group-stop timing bound also exceeds seven seconds in this environment. No additional live orphan is inferred from those PID checks; the separately confirmed hard-restart orphan has a nonempty artifact command line.",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F28.json"
  ]
}
```

```json
{
  "feature_ids": [
    "F28.restart-persistence",
    "F28.uninstall"
  ],
  "kind": "focused_core_replay",
  "actual": "The focused fresh fixture proves persistence, restart with an existing approval, uninstall, retained data/approval, repeated DELETE, and data removal without unrelated global install counts.",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F28-core-supplement.json"
  ]
}
```

```json
{
  "id": "ENOSPC",
  "reason": "Task-owned Docker build exhausted shared filesystem during original F30–F34 pass; all original ledgers preserved; root removed only task build caches and npm download cache. Recovery supplements replace environment failures.",
  "evidence": "/workspace/verification-artifacts/F29-F34-enospc-incident.json"
}
```

```json
{
  "id": "PID1-zombies",
  "reason": "PID1 does not reap exited server children; kill(pid,0) and CLI alive/stop status report zombies alive. Original instant takeover checks pass twice under own-scope subreaper with unchanged assertions,16 adopted exited children reaped,0 remain,0signals.",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F31-takeover-supervised-repro.json",
    "/workspace/verification-artifacts/F31-takeover-supervisor-report.json",
    "/workspace/verification-artifacts/F31-zombie-adaptation.md"
  ]
}
```

```json
{
  "id": "F32-shell-timer",
  "reason": "Separate CLI imports crossed6s window under load. One-process real HTTP probe observes flush6.106s and6.269s twice. First own adaptation omitted workspace and correctly422; those failures preserved.",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F32-timer-corrected-repro.json",
    "/workspace/verification-artifacts/F32-timer-adaptation.md"
  ]
}
```

```json
{
  "id": "F34-reconnect-window",
  "reason": "Original60s watcher window overlaps15sstop+~25sstartup+backoff;120s observation passes twice on ws-backed client and native Node24. Native knownmarker xpass is runtime drift.",
  "evidence": "/workspace/verification-artifacts/family-results/F34-reconnect-adapted-repro.json"
}
```

```json
{
  "id": "F30-missing-Requires",
  "reason": "Reuse-run-limit recipe consumes QA_F30_SECOND created by reuse-header but declares chat-basic only. Supplement explicitly includes reuse-header; limit recovery passes twice."
}
```

```json
{
  "id": "source-verification-image",
  "reason": "Docker became available, so static capability blockers are adapted. Published canonical image packaging remains outside this proof; exact frozen source image requires relocated source/UID1000 traversal permissions.",
  "evidence": "/workspace/verification-artifacts/F31-F33-docker-capability-adaptation.md"
}
```

```json
{
  "id": "F33-provider-refusal",
  "reason": "Unmodified real DeepSeek prompt refused hashing synthetic QA strings and produced no ObservationEvent. Explicit local synthetic fixture purpose passes real DeepSeek and unchanged assertions.",
  "evidence": "/workspace/verification-artifacts/family-results/F33-secrets-synthetic-prompt.json"
}
```
## Blocked prerequisites and coverage limits

```json
{
  "feature_ids": [
    "F02.default-bind"
  ],
  "prerequisite": "Writable /proc/self/uid_map and unprivileged user/network namespaces for unshare -rn",
  "attempted": "python -m openhands.agent_server default host inside a private namespace",
  "actual": "unshare: cannot open /proc/self/uid_map: Read-only file system. It failed before launching the server.",
  "evidence": [
    "/workspace/verification-artifacts/runs/20261013-024124-a231-map-f02/evidence/F02.default-bind/no-key.json"
  ],
  "notes": "This is blocked by the execution environment, not an agent-server bug. The primary JSON retains the raw fail; the evidence ledger has a later blocked judgment."
}
```

```json
{
  "feature_ids": [
    "F05.restart-hard-running"
  ],
  "prerequisite": "A host that reaps the killed server PID before the immediate recovery assertion",
  "attempted": "Original immediate SIGKILL/restart dead-owner takeover recipe",
  "actual": "The container leaves the owner PID as a zombie and os.kill(pid, 0) treats it as alive. Recovery after recorded lease expiry and a further restart is proven twice; instantaneous takeover is not proven.",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F05-repro.json",
    "/workspace/verification-artifacts/family-results/F05-lease-adapted-repro.json"
  ]
}
```

```json
{
  "title": "Running Codex ACP credential write-back",
  "prerequisite": "Codex ACP binary plus OpenAI login not provided",
  "route": "External credential source PUT with expected_version/value",
  "notes": "F12 activation, scrubbing, binding scope and reload guard are driven; provider-driven credential refresh synchronization is not reached.",
  "reason": "Codex ACP binary plus OpenAI login not provided",
  "feature_ids": [
    "F12.binding-live-acp"
  ]
}
```

```json
{
  "id": "canonical-docker-packaging",
  "feature_ids": [
    "F12.docker-runtime"
  ],
  "route": "Canonical Dockerfile-built runtime image",
  "reason": "Canonical build exhausted the 32 GB overlay and was aborted. The compatible local image uses frozen source plus the locked host virtualenv; local lifecycle coverage does not verify canonical packaging."
}
```

```json
{
  "feature_ids": [
    "F16.vscode-running"
  ],
  "reason": "No installed OpenVSCode Server binary; map hardcoded blocked."
}
```

```json
{
  "feature_ids": [
    "F17.noop-write-readonly"
  ],
  "reason": "chattr executable missing (exit127); immutable-attribute capability and filesystem support also unproven. API assertions were not reached."
}
```

```json
{
  "feature_ids": [
    "F15.repo-search-github"
  ],
  "route": "Invalid-token 401 branch only",
  "reason": "Live GitHub listing returned 200; pagination and case-insensitive AGENT-SDK search passed. The 401 negative control branch is inconclusive because api.github.com/user/repos itself returns 200 for the same fake token through the inherited egress/proxy environment. The local persisted token equals the fake fixture, so no backend token-selection/cache defect is established.",
  "evidence": [
    "/workspace/verification-artifacts/runs/20261013-041559-37e6-map-f15/evidence/F15.repo-search-github/bad-token.json",
    "/workspace/verification-artifacts/runs/20261013-041559-37e6-map-f15/evidence/F15.repo-search-github/direct-negative-control.json"
  ],
  "positive_branch_evidence": [
    "/workspace/verification-artifacts/runs/20261013-041559-37e6-map-f15/evidence/F15.repo-search-github/page-1.json",
    "/workspace/verification-artifacts/runs/20261013-041559-37e6-map-f15/evidence/F15.repo-search-github/page-2.json",
    "/workspace/verification-artifacts/runs/20261013-041559-37e6-map-f15/evidence/map-run/F15-git-01-live-github-listing-f15-repo-search-gith.json"
  ],
  "harness_copy": "/workspace/verification-artifacts/github-live-harness/.agents/skills/verify-agent-server/references/feature-map/F15-git.md"
}
```

```json
{
  "feature_ids": [
    "F24.login-complete"
  ],
  "prerequisite": "A human completing a real ChatGPT account login",
  "actual": "Not attempted; throwaway device codes and fake persisted tokens test the credential-free branches without signing anyone in."
}
```

```json
{
  "feature_ids": [
    "F28.backend-stop",
    "F28.status-exit-hang"
  ],
  "prerequisite": "A host that reaps terminated descendant PIDs before kill -0 process-absence checks",
  "actual": "Ordinary stop/status APIs succeeded, but the final process-absence/timing bounds are inconclusive for unreaped zombies. No extra product bug counted.",
  "evidence": [
    "/workspace/verification-artifacts/family-results/F28.json"
  ]
}
```
## Inconclusive or ambiguous expectations

```json
{
  "feature_ids": [
    "F15.repo-search-github"
  ],
  "expectation": "A deliberately invalid GitHub token should produce401.",
  "actual": "Both the Agent Server route and direct api.github.com negative control return 200. The local store contains the fake fixture token. Egress authentication or response handling prevents an unauthenticated upstream control.",
  "classification": "Environment negative control limitation; no product bug",
  "evidence": [
    "/workspace/verification-artifacts/runs/20261013-041559-37e6-map-f15/evidence/F15.repo-search-github/bad-token.json",
    "/workspace/verification-artifacts/runs/20261013-041559-37e6-map-f15/evidence/F15.repo-search-github/direct-negative-control.json"
  ]
}
```

```json
{
  "id": "F29.proxy-request-framing",
  "reason": "Valid HTTP rechunking changes Transfer-Encoding; GETbody/status correct and adjacent POST exact-byte control passes. No supported backend failure shown; exclude productbug count."
}
```

```json
{
  "id": "F32.deferred-init-flag",
  "reason": "Effective deferred_init false after /api/init is intentional and asserted by unit tests. Map assumes booted-deferred semantics without documentedcontract. Exclude productbug count."
}
```
## Client entry points not independently driven

```json
{
  "family": "F08",
  "entrypoints": [
    "RemoteConversation.set_confirmation_policy",
    "RemoteConversation.set_security_analyzer",
    "RemoteConversation.update_secrets (including callable and SecretSource serialization)",
    "RemoteConversation.reject_pending_actions",
    "RemoteConversation.run as the SDK confirmation-accept entry point",
    "ConversationClient.setConfirmationPolicy",
    "ConversationClient.setSecurityAnalyzer",
    "ConversationClient.updateSecrets",
    "ConversationClient.respondToConfirmation",
    "RemoteConversation.setConfirmationPolicy",
    "RemoteConversation.setSecurityAnalyzer",
    "RemoteConversation.updateSecrets (including callable conversion to StaticSecret)",
    "RemoteConversation.sendConfirmationResponse"
  ],
  "reason": "F08-confirmation-security-secrets.md:75-97 lists client surfaces and says recipes use direct REST/socket drivers; no Python or TypeScript client program appears in this family.",
  "notes": "Direct REST/socket observations do not verify the uncalled wrappers."
}
```

```json
{
  "family": "F09",
  "entrypoints": [
    "RemoteConversation.switchProfile",
    "RemoteConversation.switchLlm",
    "RemoteConversation.switchAcpModel"
  ],
  "reason": "F09-model-switching-plugins.md:80-86 and dynamic program at 553-596 name only ConversationClient and ConversationManager. Python plugin program is at 726-744.",
  "notes": "Direct REST/socket observations do not verify the uncalled wrappers."
}
```

```json
{
  "family": "F10",
  "entrypoints": [
    "RemoteConversation.fork",
    "RemoteConversation.navigate_to (including cached-state refresh)",
    "RemoteConversation.condense",
    "RemoteConversation.ask_agent",
    "ConversationClient.forkConversation",
    "ConversationClient.navigateConversation",
    "ConversationClient.condenseConversation",
    "ConversationClient.askAgent",
    "RemoteConversation.fork",
    "RemoteConversation.navigateTo",
    "RemoteConversation.condense",
    "RemoteConversation.askAgent"
  ],
  "reason": "F10-fork-navigate-condense-ask.md:71-85 explicitly states every recipe drives REST directly.",
  "notes": "Direct REST/socket observations do not verify the uncalled wrappers."
}
```

```json
{
  "family": "F11",
  "entrypoints": [
    "run_goal standalone synchronous driver",
    "ConversationClient.startGoal",
    "ConversationClient.stopGoal",
    "ConversationClient.resumeGoal",
    "RemoteConversation.startGoal",
    "RemoteConversation.stopGoal",
    "RemoteConversation.resumeGoal"
  ],
  "reason": "F11-goals.md:87-107 documents TypeScript goal wrappers and the separate synchronous Python run_goal driver; recipes drive REST and sockets directly.",
  "notes": "Direct REST/socket observations do not verify the uncalled wrappers."
}
```

```json
{
  "family": "F12",
  "entrypoints": [
    "AsyncRemoteWorkspace.get_runtime_session_key",
    "AsyncRemoteWorkspace.release_runtime"
  ],
  "reason": "F12-runtime-and-credentials.md:109-115 documents local TypeScript runtime methods and Python Docker lifecycle methods; the Node program at 243-266 checks local available state only.",
  "notes": "The named covered-elsewhere methods were driven in the F33 Docker SDK supplement or F34 exact-byte positive control. The remaining listed methods were not independently driven; route coverage does not prove every wrapper.",
  "covered_elsewhere_in_this_audit": [
    "RemoteWorkspace.get_runtime_session_key",
    "RemoteWorkspace.release_runtime"
  ]
}
```

```json
{
  "family": "F13",
  "entrypoints": [
    "RemoteWorkspace.start_command as a standalone entry point",
    "RemoteWorkspace.get_command_output as a standalone entry point",
    "RemoteWorkspace.stop_command",
    "AsyncRemoteWorkspace.execute_command",
    "AsyncRemoteWorkspace.start_command",
    "AsyncRemoteWorkspace.get_command_output",
    "AsyncRemoteWorkspace.stop_command",
    "BashClient.searchEvents",
    "BashClient.getEvent",
    "BashClient.getEvents",
    "BashClient.batchGetEvents",
    "BashClient.startCommand",
    "BashClient.executeCommand",
    "BashClient.clearEvents",
    "BashClient.stopCommand",
    "BashWebSocketClient (including query-key auth, replay, and reconnect)",
    "RemoteWorkspace.executeCommand"
  ],
  "reason": "F13-bash.md:78-98 documents all wrapper surfaces but describes only two sync execute_command SDK programs plus raw REST/WebSocket drivers.",
  "notes": "Direct REST/socket observations do not verify the uncalled wrappers."
}
```

```json
{
  "family": "F14",
  "entrypoints": [
    "AsyncRemoteWorkspace.file_upload (global and scoped)",
    "AsyncRemoteWorkspace.file_download (global and scoped)",
    "FileClient.uploadFile",
    "FileClient.uploadTextFile",
    "FileClient.downloadTextFile",
    "FileClient.downloadTrajectory",
    "FileClient.getHome",
    "FileClient.searchSubdirectories",
    "RemoteConversation.downloadTrajectory",
    "RemoteWorkspace.fileDownload",
    "RemoteWorkspace.fileUpload string/File input branches",
    "write_file tool consuming fileUpload.file_size"
  ],
  "reason": "F14-files.md:77-89 documents wrapper surfaces; upload-size at 210-261 exercises only TypeScript global Blob upload, and sdk-workspace at 776-809 exercises sync Python transfers in both scopes.",
  "notes": "The named covered-elsewhere methods were driven in the F33 Docker SDK supplement or F34 exact-byte positive control. The remaining listed methods were not independently driven; route coverage does not prove every wrapper.",
  "covered_elsewhere_in_this_audit": [
    "FileClient.downloadFile"
  ]
}
```

```json
{
  "family": "F16",
  "entrypoints": [
    "RemoteWorkspace.startWorkspaceSession/deleteWorkspaceSession",
    "VSCodeClient.getUrl/getStatus"
  ],
  "reason": "Map describes the wrappers but executes no TypeScript program for them; REST cookie/status/URL proof does not verify these wrappers."
}
```

```json
{
  "family": "F19",
  "entrypoints": [
    "MCPClient.testServer/startOAuth/getOAuthStatus/submitOAuthCallback",
    "SettingsClient.createMcpServer/patchMcpServer/deleteMcpServer"
  ],
  "reason": "Map explicitly states these TypeScript calls are not driven; only REST lane and Python get_mcp_config are driven."
}
```
## Secondary assertions and environment-specific scenarios not independently driven

- Immediate dead-owner lease takeover on a host that reaps SIGKILLed children

- F02.default-bind unprivileged network namespace recipe; environment refuses uid_map writes

```json
{
  "feature_id": "F24.device-start-offline",
  "branch": "Offline poll assertion after the first failing device/start assertion"
}
```

```json
{
  "feature_id": "F25.install-documented-sources",
  "branch": "The second advertised /tree/main URL variant after the first failing github shorthand"
}
```

```json
{
  "feature_id": "F26.conversation-resume-disabled",
  "branch": "include_skills GET after the failing live socket assertion"
}
```

```json
{
  "feature_id": "F28.prepare-corrupt-archive",
  "branch": "Later no-write assertions after the invalid-format failure"
}
```
## Full attempt ledger

[Every recorded attempt, preserving each run](https://enyst.github.io/investigations/agent-server-verify-2026-10-13/all-attempts.md).

