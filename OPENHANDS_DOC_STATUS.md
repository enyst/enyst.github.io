# OpenHands architecture-page status

This file is an explicit maintenance follow-up for published OpenHands/SmolPaws architecture pages. The repository has GitHub Issues disabled, so documentation drift is recorded here until the pages themselves are revised.

## Current sources of truth

- SDK transpilation policy: [`enyst/openhands-agent/docs/TRANSPILE_CONTRACT.md`](https://github.com/enyst/openhands-agent/blob/main/docs/TRANSPILE_CONTRACT.md)
- Drift control plane and oracle design: [`enyst/openhands-agent/docs/DRIFT_TOOLING.md`](https://github.com/enyst/openhands-agent/blob/main/docs/DRIFT_TOOLING.md)
- Canonical upstream manifest: [`enyst/openhands-agent/transpile/upstream.json`](https://github.com/enyst/openhands-agent/blob/main/transpile/upstream.json)
- Agent-server transpilation policy: [`enyst/smolpaws/packages/openhands-agent-server/TRANSPILE_RULES.md`](https://github.com/enyst/smolpaws/blob/main/packages/openhands-agent-server/TRANSPILE_RULES.md)
- Agent-server package: [`enyst/smolpaws/packages/openhands-agent-server/README.md`](https://github.com/enyst/smolpaws/blob/main/packages/openhands-agent-server/README.md)
- Durable Message Relay: [`enyst/smolpaws/src/coordinator/DESIGN.md`](https://github.com/enyst/smolpaws/blob/main/src/coordinator/DESIGN.md)
- Slack Message Relay operations: [`enyst/smolpaws/docs/slack/instructions.md`](https://github.com/enyst/smolpaws/blob/main/docs/slack/instructions.md)

Public pages are explanatory snapshots. They must not become a hand-maintained live parity ledger.

## Maintenance machinery now implemented

The SDK fork owns one canonical upstream manifest, deterministic `scan` / `prepare` / `check` tooling, synthetic-git tests, CI coverage, and a weekly drift workflow. The server fork consumes the same manifest from its vendored SDK and validates that provenance before running package CI.

Generated Python OpenAPI evidence, SDK wire-oracle infrastructure, and deterministic Python/TypeScript server checks now exist. Mutable drift and parity counts remain generated evidence rather than prose on this site.

## Message Relay rollout now implemented

The durable external-message subsystem is no longer intake-only scaffolding:

- `MessageRelay` owns lane binding, durable intake, agent-server integration, and `syncDeliveryOutbox()`;
- `OutboundRelay` catches agent events up into the durable delivery outbox and coordinates bounded dispatch;
- `DeliveryDispatcher` owns claim → send fence → delivery target → settlement;
- Slack has a greenfield `SlackBridge`, `SlackRelayRuntime`, and `SlackDeliveryTarget`, with no legacy `/turns` fallback;
- deterministic tests cover SQLite durability, the real TypeScript agent-server, the real agent loop with a deterministic LLM, outbox synchronization, dispatch settlement, and Slack-target routing.

An isolated, self-expiring live canary also completed the full Liberty Labs Socket Mode path on 2026-08-16 at fork commit `a69456fc6f818f23ecb6e2e064f3e03fceeafaf4`. The exact observed reply was `RELAY-LIVE-a69456fc6f81`, produced after Slack ingress, durable Message Relay intake, the real TypeScript agent-server/agent loop, terminal `finish`, `syncDeliveryOutbox()`, `DeliveryDispatcher`, and `SlackDeliveryTarget`.

That proves the real Slack transport and complete durable architecture with a deterministic test LLM. The remaining operational boundary is narrower: restart the normal host so it releases the obsolete Slack Socket Mode connection, then soak standalone `paws` on port 8790 with the configured real LLM profile. A response containing the legacy `Done — nothing to report back` fallback still proves that an older `/turns` process handled that particular event.

## Known pages needing status treatment

### `arch/sdk-swap-surface.html`

Historical pre-swap symbol inventory. It still presents early package versions, missing symbols, and undecided differences as current work.

Action: retain the analysis, but add a prominent **historical / superseded** banner linking to the current SDK contract, server contract, canonical manifest, and drift tooling.

### `arch/smolpaws-sdk-swap.html`

Historical migration plan. It still says the new SDK has no TypeScript server and frames `/turns` versus `/events + /run` as an unresolved architecture question.

Action: mark superseded by the implemented TypeScript agent-server package and external durable Message Relay. Preserve it as migration history.

### `arch/smolpaws-message-work-adr.html`

The decision remains current, but the wording and diagram still use the overloaded term `projector` and its header understates the implementation status.

Action: update status to **accepted / isolated Slack live proof complete / production soak pending**. Replace the user-facing component vocabulary with:

- **delivery outbox sync** / `syncDeliveryOutbox()` for agent EventLog → durable delivery work;
- **Message Relay** for the complete durable external-message subsystem;
- **Outbound Relay** for EventLog catch-up and bounded outbound orchestration;
- **Delivery Dispatcher** for durable delivery work → platform side effect.

Preserve `delivery_unknown` and the existing crash analysis; those semantics remain current.

### Slack architecture page

Action: ensure the Slack page describes Socket Mode → Message Relay → TypeScript agent-server → `syncDeliveryOutbox()` → Delivery Dispatcher → Slack, records the isolated Liberty Labs proof, and clearly distinguishes it from the still-pending normal-process real-provider soak.

### `index.html`

Action: update card descriptions/status labels for the pages above so the home page does not present historical plans as current implementation state.

## Completion rule

After the page banners/status labels and Slack/ADR terminology are updated, delete this file or replace it with a terse pointer explaining that historical banners are intentional. Do not copy weekly drift counts or current parity totals into the public site.
