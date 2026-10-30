"""Run synthetic title comparisons through the SDK's real title helper.

Set PYTHONPATH to the SDK checkout under test. Supply LLM_MODEL, LLM_BASE_URL,
and LLM_API_KEY through the environment (LLM_BASE_URL is optional). No credentials are written to output.
"""

import argparse
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import SecretStr

from openhands.sdk.conversation.request import ConversationConfig
from openhands.sdk.conversation.title_utils import generate_title_with_llm
from openhands.sdk.llm import LLM
from openhands.sdk.workspace import LocalWorkspace


CASES = [
    {
        "id": "auth-login",
        "family": "auth",
        "input": "Investigate why login fails after a password reset. No cause is confirmed yet.",
        "focus": "login",
        "risks": ["invented resolution", "lost uncertainty"],
    },
    {
        "id": "auth-session",
        "family": "auth",
        "input": "Investigate why sessions expire after five minutes. No cause is confirmed yet.",
        "focus": "session expiry",
        "risks": ["invented resolution", "lost uncertainty"],
    },
    {
        "id": "auth-oauth",
        "family": "auth",
        "input": "Investigate why OAuth callbacks return HTTP 400. No cause is confirmed yet.",
        "focus": "OAuth callbacks",
        "risks": ["invented resolution", "lost uncertainty"],
    },
    {
        "id": "upgrade-urllib3",
        "family": "upgrade",
        "input": "Upgrade urllib3 to the latest compatible patch release and run its regression tests.",
        "focus": "urllib3",
        "risks": ["invented completion"],
    },
    {
        "id": "upgrade-pydantic",
        "family": "upgrade",
        "input": "Upgrade Pydantic to the latest compatible patch release and run its regression tests.",
        "focus": "Pydantic",
        "risks": ["invented completion"],
    },
    {
        "id": "upgrade-pillow",
        "family": "upgrade",
        "input": "Upgrade Pillow to the latest compatible patch release and run its regression tests.",
        "focus": "Pillow",
        "risks": ["invented completion"],
    },
    {
        "id": "filler-cache",
        "family": "frontloading",
        "input": "I was hoping you could help me with a task today. What I need is an explanation of Redis cache eviction, especially the allkeys-lru policy.",
        "focus": "Redis cache eviction",
        "risks": ["generic opening"],
    },
    {
        "id": "filler-build",
        "family": "frontloading",
        "input": "I was hoping you could help me with a task today. What I need is an explanation of Rust incremental compilation and why cache misses slow builds.",
        "focus": "Rust incremental compilation",
        "risks": ["generic opening"],
    },
    {
        "id": "feedback-complaint",
        "family": "feedback",
        "input": "Summarize customer complaints: users say the lesson energy limit interrupts practice and forces them to wait. Do not turn this into praise.",
        "focus": "energy-limit complaints",
        "risks": ["wrong sentiment"],
    },
    {
        "id": "feedback-praise",
        "family": "feedback",
        "input": "Summarize customer praise: users love the offline lessons because they can practice on the train. Do not invent a complaint.",
        "focus": "offline-lesson praise",
        "risks": ["wrong sentiment"],
    },
    {
        "id": "feedback-mixed",
        "family": "feedback",
        "input": "Summarize mixed feedback about chess lessons: users enjoy the puzzles but complain that the checkmate rule sometimes rejects valid moves.",
        "focus": "mixed chess-lesson feedback",
        "risks": ["flattened mixed sentiment"],
    },
    {
        "id": "neutral-compare",
        "family": "fidelity",
        "input": "Compare SQLite and PostgreSQL for a small offline-first app. I have not selected either database.",
        "focus": "SQLite and PostgreSQL comparison",
        "risks": ["invented decision", "invented sentiment"],
    },
    {
        "id": "negation",
        "family": "fidelity",
        "input": "Explain how to inspect Docker disk usage. Do not delete containers, images, or volumes.",
        "focus": "Docker disk inspection",
        "risks": ["opposite action", "invented cleanup"],
    },
    {
        "id": "uncertainty",
        "family": "fidelity",
        "input": "Check whether TLS certificate rotation might explain the intermittent webhook failures. This is a hypothesis, not a confirmed cause.",
        "focus": "possible TLS-related webhook failures",
        "risks": ["hypothesis stated as fact", "invented resolution"],
    },
    {
        "id": "completed",
        "family": "status",
        "input": "The login fix has already merged and all regression tests passed. Write a short release note about the completed fix.",
        "focus": "release note for completed login fix",
        "risks": ["confusing requested writing with completed engineering"],
    },
    {
        "id": "long-tail",
        "family": "input-cap",
        "input": "Reference background only; the actual request follows at the end.\n"
        + "The project uses a small command-line interface and stores its examples in a dedicated folder. "
        * 20
        + "\nACTUAL REQUEST: Investigate Zephyr's Unicode CSV parser crash. Do not work on the CLI examples.",
        "focus": "Zephyr Unicode CSV parser crash",
        "risks": ["missing decisive text beyond character 1000"],
    },
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    skill = args.skill.read_text()
    if skill.startswith("---\n"):
        skill = skill.split("---\n", 2)[2]
    override = (
        "Generate one conversation title for the user request below. "
        "Apply the following readable-text skill to a sidebar of task titles. "
        "Use one relevant emoji followed by an action in the continuous form "
        "and the specific task subject. Keep the distinguishing topic near the start. "
        "Describe the user's requested work, not an assumed result. "
        "Use the same vocabulary for the same concepts across titles. "
        "Preserve negation, uncertainty, and meaningful sentiment where relevant. "
        "Return only a title of at most {max_length} characters.\n\n"
        + skill
        + "\n\nUSER REQUEST:\n{conversation_content}"
    )
    config = ConversationConfig(
        workspace=LocalWorkspace(working_dir=str(Path.cwd())), prompt=override
    )
    assert config.prompt == override
    model = os.environ["LLM_MODEL"]
    records = []
    consecutive_failures = 0
    result = {
        "schema_version": 1,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "revision": args.revision,
        "model": model,
        "temperature": 0,
        "reasoning_effort": "none",
        "extended_thinking_budget": None,
        "max_title_characters": 50,
        "repeats": args.repeats,
        "skill_sha256": hashlib.sha256(skill.encode()).hexdigest(),
        "override_characters": len(override),
        "override": override,
        "cases": CASES,
        "records": records,
        "method": "Same uncapped SDK helper and inputs in both arms; only the user prompt differs. Synthetic public inputs only. No fallbacks counted as successful generations.",
    }
    for repeat in range(args.repeats):
        for index, case in enumerate(CASES):
            arms = (
                ["default", "override"]
                if (repeat + index) % 2 == 0
                else ["override", "default"]
            )
            for arm in arms:
                llm = LLM(
                    model=model,
                    base_url=os.environ.get("LLM_BASE_URL"),
                    api_key=SecretStr(os.environ["LLM_API_KEY"]),
                    temperature=0,
                    max_output_tokens=256,
                    reasoning_effort="none",
                    extended_thinking_budget=None,
                    timeout=45,
                    num_retries=1,
                    usage_id="readable-title-evaluation",
                )
                errors = []
                started = time.monotonic()
                title = generate_title_with_llm(
                    case["input"],
                    llm,
                    max_length=50,
                    prompt=override if arm == "override" else None,
                    on_error=lambda exc: errors.append(type(exc).__name__),
                )
                record = {
                    "case_id": case["id"],
                    "repeat": repeat + 1,
                    "arm": arm,
                    "title": title,
                    "characters": len(title) if title else 0,
                    "latency_seconds": round(time.monotonic() - started, 3),
                    "errors": errors,
                }
                records.append(record)
                consecutive_failures = consecutive_failures + 1 if not title else 0
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(
                    json.dumps(result, ensure_ascii=False, indent=2) + "\n"
                )
                print(json.dumps(record, ensure_ascii=False), flush=True)
                if consecutive_failures >= 3:
                    result["stopped_early"] = (
                        "Three consecutive failed generations; investigate before spending more requests."
                    )
                    result["finished_at"] = datetime.now(timezone.utc).isoformat()
                    args.output.write_text(
                        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
                    )
                    raise SystemExit("Stopped after three failed generations")
    result["finished_at"] = datetime.now(timezone.utc).isoformat()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
