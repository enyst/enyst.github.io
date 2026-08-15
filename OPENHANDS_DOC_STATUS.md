# OpenHands architecture-page status

This file is an explicit maintenance follow-up for published OpenHands/SmolPaws architecture pages. The repository has GitHub Issues disabled, so documentation drift is recorded here until the pages themselves are revised.

## Current sources of truth

- SDK transpilation policy: [`enyst/openhands-agent/docs/TRANSPILE_CONTRACT.md`](https://github.com/enyst/openhands-agent/blob/main/docs/TRANSPILE_CONTRACT.md)
- Drift-tooling design: [`enyst/openhands-agent/docs/DRIFT_TOOLING.md`](https://github.com/enyst/openhands-agent/blob/main/docs/DRIFT_TOOLING.md)
- Agent-server transpilation policy: [`enyst/smolpaws/packages/openhands-agent-server/TRANSPILE_RULES.md`](https://github.com/enyst/smolpaws/blob/main/packages/openhands-agent-server/TRANSPILE_RULES.md)
- Agent-server package: [`enyst/smolpaws/packages/openhands-agent-server/README.md`](https://github.com/enyst/smolpaws/blob/main/packages/openhands-agent-server/README.md)
- Durable coordinator: [`enyst/smolpaws/src/coordinator/DESIGN.md`](https://github.com/enyst/smolpaws/blob/main/src/coordinator/DESIGN.md)

Public pages are explanatory snapshots. They must not become a hand-maintained live parity ledger.

## Known pages needing status treatment

### `arch/sdk-swap-surface.html`

Historical pre-swap symbol inventory. It still presents early package versions, missing symbols, and undecided differences as current work.

Action: retain the analysis, but add a prominent **historical / superseded** banner linking to the current SDK contract, server contract, and drift-tooling design.

### `arch/smolpaws-sdk-swap.html`

Historical migration plan. It still says the new SDK has no TypeScript server and frames `/turns` versus `/events + /run` as an unresolved architecture question.

Action: mark superseded by the implemented TypeScript agent-server package and external durable coordinator. Preserve it as migration history.

### `arch/smolpaws-message-work-adr.html`

The ADR remains useful, but its header says `status: proposed` even though the coordinator core and `EXT-SERVER-001` idempotent event append are implemented.

Action: update status to **accepted / core implemented**, explicitly noting that bridge canary, cutover, and old-runner removal remain rollout work.

### `index.html`

Action: update card descriptions/status labels for the pages above so the home page does not present historical plans as current implementation state.

## Completion rule

After the page banners/status labels are updated, delete this file or replace it with a terse pointer explaining that historical banners are intentional. Do not copy weekly drift counts or current parity totals into the public site.
