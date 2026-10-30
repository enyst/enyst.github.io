"""Run the fixed follow-up protocol through the real SDK title helper."""

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
from openhands.sdk.llm.auth.openai import OpenAISubscriptionAuth
from openhands.sdk.llm.options.responses_options import select_responses_options
from openhands.sdk.workspace import LocalWorkspace


ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=["haiku", "gemini", "luna"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = (ROOT / "protocol.json").read_bytes()
    protocol = json.loads(raw)
    settings = protocol["models"][args.model]
    prompts = protocol["prompts"]
    for prompt in prompts.values():
        assert (
            ConversationConfig(
                workspace=LocalWorkspace(working_dir=str(ROOT)), prompt=prompt
            ).prompt
            == prompt
        )
    kwargs = dict(
        reasoning_effort=settings["reasoning_effort"], timeout=60, num_retries=1
    )
    if args.model == "luna":
        llm = OpenAISubscriptionAuth().create_llm(
            model="gpt-6-luna",
            litellm_extra_body={"reasoning": {"effort": "low"}},
            **kwargs,
        )
        options = select_responses_options(llm, {}, include=None, store=False)
        assert options["extra_body"]["reasoning"] == {"effort": "low"}
    else:
        llm = LLM(
            model=settings["model"],
            base_url=os.environ["LLM_BASE_URL"],
            api_key=SecretStr(os.environ["LLM_API_KEY"]),
            temperature=0,
            extended_thinking_budget=None,
            max_output_tokens=256,
            **kwargs,
        )
    records = []
    result = {
        "schema_version": 1,
        "protocol_sha256": hashlib.sha256(raw).hexdigest(),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "model_key": args.model,
        "settings": settings,
        "source_sdk": protocol["source_sdk"],
        "records": records,
    }
    failures = 0
    arms = list(prompts)
    for repeat in range(protocol["repeats"]):
        for index, case in enumerate(protocol["cases"]):
            rotation = (index + repeat) % len(arms)
            order = arms[rotation:] + arms[:rotation]
            if repeat % 2:
                order = list(reversed(order))
            for arm in order:
                errors = []
                started = time.monotonic()
                title = generate_title_with_llm(
                    case["input"],
                    llm,
                    max_length=50,
                    prompt=prompts[arm],
                    on_error=lambda exc: errors.append(type(exc).__name__),
                )
                record = {
                    "case_id": case["id"],
                    "split": case["split"],
                    "family": case["family"],
                    "repeat": repeat + 1,
                    "arm": arm,
                    "title": title,
                    "characters": len(title) if title else 0,
                    "latency_seconds": round(time.monotonic() - started, 3),
                    "errors": errors,
                }
                records.append(record)
                failures = failures + 1 if not title else 0
                args.output.write_text(
                    json.dumps(result, ensure_ascii=False, indent=2) + "\n"
                )
                print(json.dumps(record, ensure_ascii=False), flush=True)
                if failures >= 3:
                    result["stopped_early"] = "Three consecutive failures"
                    result["finished_at"] = datetime.now(timezone.utc).isoformat()
                    args.output.write_text(
                        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
                    )
                    raise SystemExit("Investigate setup before more calls")
    result["finished_at"] = datetime.now(timezone.utc).isoformat()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
