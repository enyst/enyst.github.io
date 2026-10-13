# Reproduce this audit

Target repository: https://github.com/enyst/agent-sdk
Frozen revision: acca181af1f353975965bcf6486e1d0a58f444c0
All four Python packages and the TypeScript client: 1.54.0.

Read the frozen verify-agent-server/SKILL.md and its report/adaptation contracts first.
Run its build and map checks, then `control-agent-server map run --file Fnn --fresh --record --keep-going`.
Use your own provider credentials through environment variables. No credential is included here.
The report's exact reproduction commands use the original workspace paths; adjust these paths to your checkout and evidence root.

This directory includes the copied recipes, adapter scripts and patches used to make environment-dependent prerequisites concrete. Each family batch explains its adaptations. Product source was unchanged.
The nested .agents/skills directories preserve the executable CLI and map exactly as used. Python bytecode, caches, private shell state, runtime keys, and fixtures are excluded.
The frozen-source Docker image is a local verification runtime, not a production packaging certification.

The evidence archive contains request/response observations and transcripts. It does not contain private server persistence. The full attempt table and per-run ledgers preserve earlier setup failures as well as fresh confirmations.
