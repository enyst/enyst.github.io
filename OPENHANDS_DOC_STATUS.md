# OpenHands architecture-page status

Audited 2026-09-14 against SmolPaws #170 (`c344f79`) and SDK #28 (`369b9c5`).
LLM accounting notes updated 2026-09-15 after SDK #35 (`a983e4c`) and server #184 (`28106cd`)
merged and were verified on the shared and canary product hosts. Earlier unrecorded usage remains unknown.
Beads owns task status; the site explains dated architecture, decisions and plans. It is not runtime telemetry.

## Current explanations

- [Agent-triggered condensation](arch/agent-triggered-condensation.html): September 20 proposal update: staged warnings, typed condense Action/Observation payloads, voluntary reset and an explicitly configured Python-style hard-reset fallback with an environment notice before its summary. Not implemented; `smolpaws-te15` and its seven dependent tasks own status. Manual-command behavior and exact metadata/configuration remain design decisions.
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

`arch/whatsapp-as-bridge.html`, `arch/openhands-agent-server-parity.html`,
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
