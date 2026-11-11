# OpenHands architecture-page status

Audited 2026-09-14 against SmolPaws #170 (`c344f79`) and SDK #28 (`369b9c5`).
LLM accounting notes updated 2026-09-15 after SDK #35 (`a983e4c`) and server #184 (`28106cd`)
merged and were verified on the shared and canary product hosts. Earlier unrecorded usage remains unknown.
Beads owns task status; the site explains dated architecture, decisions and plans. It is not runtime telemetry.

## Projects SDK scope walkthrough

[How Projects work](arch/projects-insider-sdk-scope.html) follows the coordinator
and worker roles, then separates their SDK contracts from reactions and Insider
Voice. Source checked 11 November 2026: Projects #6602 (`01f2bf191`), reactions
#6609 (`9dba7b939`), Voice #5180 (`0376532d7`). The Projects snapshot already
includes reactions. The page records role presets, profile-based worker launch,
automatic report delivery, board judgments, artifacts, memory, and public API and
history changes. In particular, human reactions are LLM-convertible at these
heads. These snapshots supersede older descriptions only for the scoped
contracts; this documentation pass makes no new runtime-verification claim.

## Insider Voice integration

The 31 October 2026 source check follows SDK [#5180](https://github.com/OpenHands/software-agent-sdk/pull/5180)
(`e17f4e09b`), Canvas [#17558](https://github.com/OpenHands/OpenHands/pull/17558)
(`b6ff25af6`), and Insider [#2](https://github.com/enyst/insider/pull/2) (`bf99051b`).
All three remain draft PRs; these heads match the 26 October integrated verification record.
[The Insider presentation](arch/insider-cat.html), [user guide](arch/insider-cat-stories.html),
and [Voice guide](arch/insider-cat-codex-voice.html) now describe that implementation,
without the superseded prototypes or speculative interaction designs.

The [26 October report](https://github.com/enyst/insider/blob/bf99051b0c8293c324091c47bac5df3b3d16d45b/.pr/insider-verification-20261026.md)
records 42 passed checks out of 46 scoped UI checks, plus nine SDK API recipes.
Real Codex handoff, saved OpenHands tool work, and returned audio were exercised
with generated microphone input. Remaining checks: physical iPad microphone/speaker,
live OpenAI API Voice, live backend switching, and complete keyboard-only traversal.
The 31 October documentation pass is not another live runtime test.

## Current explanations

- [Keep DigitalOcean connected](arch/keep-digitalocean-connected.html): 20 October
  2026 merge of smolpaws's and Claude Code's 19 October proposals, with Engel's
  decisions: one host bridge, OAuth with PKCE kept in the OS keychain, a cookie
  derived from the session key, DigitalOcean-aware restore, and agents using the
  admin-type session key on the active team. The opening principle is “People log in.
  Agents use keys”; no new key types or permissions. New-browser owner approval
  is a release check. Loopback handling and user-created admin keys have follow-up
  records (smolpaws-hf5n, smolpaws-wmaj). Browser behavior and the agent path
  were driven live with `control-openhands` at 8d39305; connecting a session and a
  real OAuth exchange were not possible in the sandbox. The two earlier URLs
  redirect here.

- [Automation profile launch](arch/automation-profile-launch.html): 19 October 2026
  reading of automation #600's fourth design. Separates reported preset/profile-store
  failures from proposed dispatch-time creation and the enterprise tools/secrets gate.
  Public source contracts checked; no fresh live-run or deployment verification.

- [Checking the Agent SDK from outside](arch/agent-sdk-external-contract.html):
  9 October 2026 snapshot of the merged external verifier, the confirmed manual
  Cloud run, and the controls needed before periodic checks. The Cloud
  automation is disabled. The [testing strategy](arch/openhands-sdk-architecture-testing.html)
  remains the broader plan. The [merged evaluation](https://github.com/enyst/automations/tree/ce3f5e362d73c22bf122bd6c02a9a0048e402027/evaluations/sdk-lifecycle-conformance/2026-10-09-cloud)
  owns the dated evidence; this page does not report live run status.
- [Insider Cat](arch/insider-cat.html): 31 October 2026 presentation of the current
  development App: several saved Cats, one continuing identity across Projects and
  regular chat, normal Agent Profile tools and enabled skills, and direct Codex
  handoff to the saved OpenHands agent. Covers legacy Cat resume, local audio
  Stop/Resume, explicit busy-request rejection, and automatic call teardown before
  `/condense`. The [Voice guide](arch/insider-cat-codex-voice.html) records transport
  configuration, context and ownership boundaries, and the dated verification limits.
- [How SmolPaws resets its context](arch/smolpaws-agent-reset.html): 5 October 2026 implementation guide covering voluntary reset, warnings, the separate emergency summarizer, configuration and durable events. It links checked source revisions; it does not assert a live deployment state. The [September proposal](arch/agent-triggered-condensation.html) is retained as design history.
- [Reviewing the reviewer](arch/openhands-review-auditor.html): September 16 investigation,
  chosen actual Astra model and exasperated robot babysitter voice, event-driven implementation draft,
  a supervised pilot with four reviews published and one withheld after the PR changed,
  and explicitly unresolved Cloud deployment prerequisites.
  Subsequent manual publishing uses `enyst`; the continuous-automation draft stays dry-run and recurring reviews stay off.
  The four `smolpaws` pilot publications remain historical. Continuous Cloud automation remains undeployed.
  Corrected detector replay reopened selection; four new manual reviews are verified as published by `enyst`:
  one approval and three requests for changes. Failed and stale attempts remain historical evidence, without a public verdict.
  September 17: four of eight fresh candidates qualified for a bounded local OpenHands Automation trial.
  The first local Automation trial failed before publication, posted zero reviews and is verified disabled.
  The bounded retry completed with four requests for changes published as `enyst`; both local trial
  definitions are verified disabled, and the Cloud Roasted reviewer stays paused. SDK #4862 received a
  verified editorial correction withdrawing one finding with unproven dependency-path reachability;
  its supported request for changes and all eleven historical scores remain unchanged. Original evidence
  remains immutable. All twelve completed PRs are retired; unattended review quality remains unvalidated.
  Literal-false event filters and absent schedules prevent recurring triggers.
  Its persistent host checkpoints remain separate from the unresolved Cloud KV and native-event prerequisites.
- [OpenHands Automations operations](arch/openhands-automation-operations.html): September 15 deployment snapshot,
  permitted effects, recent results, and pending location/target decisions. Distinguishes live registrations
  from authored definitions, paused history, and future plans.
- [WhatsApp readiness](arch/whatsapp-readiness.html): controlled text-canary gates, permanent-cutover gates,
  source evidence, provider accounting rollout and Beads owners. Companion: `smolpaws/smolpaws/docs/whatsapp/READINESS.md`.
- [Bridge topology](arch/smolpaws-bridges-topology.html): shared relay, lane identity, launch additions,
  startup coordination and current implementation versus dated deployment observations.
- [Transpile maintenance](arch/openhands-transpile-maintenance.html): bounded review, DELEGATED server units,
  re-vendoring, TypeScript-owned provider compatibility, and durable accounting with explicit coverage.
- [Slack](smolpaws-slack.html): current relay ownership and extraction policy; August transport proof is historical.
- [Message Work ADR](arch/smolpaws-message-work-adr.html): accepted decision, original proposal retained with
  a dated implementation note for deterministic event append and final/mid-turn delivery.

## Historical pages retained with current links

`arch/agent-triggered-condensation.html`, `arch/whatsapp-as-bridge.html`, `arch/openhands-agent-server-parity.html`,
`arch/smolpaws-sdk-swap.html`, `arch/smolpaws-sdk-swap-board.html`, `arch/sdk-swap-surface.html`,
`smolpaws-whatsapp.html`, `smolpaws-discord.html`, `smolpaws-github.html`.
Their old proposals, runtime observations and source revisions remain historical evidence. Updating a banner
is not a fresh validation of every old gap. The homepage points to the current readiness plan.

## Sources of truth

- SDK: `smolpaws/openhands-agent`, `docs/TRANSPILE_CONTRACT.md`, `docs/LLM_PROVIDERS.md`,
  `docs/LLM_METRICS.md`, `transpile/llm-metrics.md`, `docs/DRIFT_TOOLING.md`,
  `docs/DRIFT_AUTOMATION.md`, `transpile/upstream.json`.
- Server: `smolpaws/smolpaws/packages/openhands-agent-server`, `TRANSPILE_RULES.md`,
  `docs/REVENDOR_AUTOMATION.md`, generated oracles, tests and review records.
- Relay and bridges: `smolpaws/smolpaws`, `src/coordinator/DESIGN.md`, `docs/bridges.md`,
  `docs/whatsapp/README.md`, `docs/whatsapp/READINESS.md`, `docs/slack/instructions.md`.
- Work: Beads `smolpaws-zlo`, `smolpaws-kxa`, `kxa.2`, `kxa.4`–`kxa.9`, `39y`, `b1r.24`, `via`.

Do not copy weekly drift counts or parity totals into the public site. Automation runbooks do not prove
that external schedules are active. Local paths, credentials, chat content and private state stay private.
