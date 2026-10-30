"""Prepare blinded items and collect independent Jev classifications."""

import argparse
import hashlib
import json
import os
import random
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
P = json.loads((ROOT / "protocol.json").read_text())


def words(title):
    return re.findall(r"[^\W_]+(?:[-’'][^\W_]+)*", title, flags=re.UNICODE)[:2]


def prepare():
    items = {}
    models = {}
    for name in P["models"]:
        d = json.loads((ROOT / f"{name}.json").read_text())
        assert d.get("finished_at") and len(d["records"]) == 96
        models[name] = d
        cases = {c["id"]: c for c in P["cases"]}
        for r in d["records"]:
            if not r["title"]:
                continue
            c = cases[r["case_id"]]
            key = (c["id"], r["title"])
            items.setdefault(
                key,
                {
                    "case_id": c["id"],
                    "request": c["input"],
                    "title": r["title"],
                    "first_two_words": words(r["title"]),
                    "criteria": ["clarity", "frontload", "fidelity"]
                    + (
                        ["connotation"]
                        if c["family"] == "feedback" or c["id"] == "neutral-compare"
                        else []
                    ),
                },
            )
    rng = random.Random(1030202603)
    entries = list(items.values())
    rng.shuffle(entries)
    mapping = {}
    lookup = {}
    for i, row in enumerate(entries):
        row["id"] = f"t{i + 1:03}"
        lookup[(row["case_id"], row["title"])] = row["id"]
        mapping[row["id"]] = {"case_id": row["case_id"], "title": row["title"]}
    groups = []
    for name, d in models.items():
        for arm in P["prompts"]:
            for repeat in (1, 2):
                for family in P["scoring_groups"]["collection"]:
                    rows = [
                        r
                        for r in d["records"]
                        if r["arm"] == arm
                        and r["repeat"] == repeat
                        and r["family"] == family
                    ]
                    group_id = f"g{len(groups) + 1:03}"
                    linked = [
                        lookup[(r["case_id"], r["title"])] for r in rows if r["title"]
                    ]
                    state = [
                        {
                            "request": next(
                                c["input"]
                                for c in P["cases"]
                                if c["id"] == r["case_id"]
                            ),
                            "title": r["title"],
                        }
                        for r in rows
                        if r["title"]
                    ]
                    groups.append(
                        {"id": group_id, "items": state, "criteria": ["collection"]}
                    )
                    mapping[group_id] = {
                        "model": name,
                        "arm": arm,
                        "repeat": repeat,
                        "family": family,
                        "title_ids": linked,
                        "missing_titles": len(rows) - len(linked),
                    }
    rng.shuffle(groups)
    (ROOT / "blinded-items.json").write_text(
        json.dumps(
            {"titles": entries, "groups": groups, "rubric": P["rubric"]},
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    (ROOT / "mapping.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2) + "\n"
    )
    print(len(entries), "unique title items;", len(groups), "groups")


def question(row, criterion):
    rule = P["rubric"][criterion]
    options = list(rule["criteria"].items())
    random.Random(row["id"] + criterion).shuffle(options)
    return {
        "type": "choice",
        "instructions": rule["instructions"],
        "criteria": dict(options),
    }


def jev():
    data = json.loads((ROOT / "blinded-items.json").read_text())
    api_key = os.environ["TYPESAFE_API_KEY"]
    results = []
    started = datetime.now(timezone.utc).isoformat()
    target = ROOT / "jev.json"

    def call(row):
        state = {
            k: row[k]
            for k in ("request", "title", "first_two_words", "items")
            if k in row
        }
        questions = {key: question(row, key) for key in row["criteria"]}
        payload = {
            "model": P["judges"]["jev"]["model"],
            "state": state,
            "questions": questions,
        }
        request = urllib.request.Request(
            "https://api.typesafe.ai/v1/systemone",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json",
            },
        )
        failures = []
        for attempt in range(4):
            try:
                with urllib.request.urlopen(request, timeout=45) as r:
                    response = json.load(r)
                answers = response["answers"]
                assert set(answers) == set(questions)
                for key, answer in answers.items():
                    assert answer["choice"] in questions[key]["criteria"]
                return {
                    "id": row["id"],
                    "response": response,
                    "errors_before_success": failures,
                }
            except urllib.error.HTTPError as exc:
                failures.append({"type": "HTTPError", "status": exc.code})
                if exc.code not in (429, 500, 502, 503, 504, 529):
                    break
                time.sleep(min(float(exc.headers.get("Retry-After", 2**attempt)), 30))
            except (OSError, ValueError, KeyError, AssertionError) as exc:
                failures.append({"type": type(exc).__name__})
                time.sleep(2**attempt)
        return {"id": row["id"], "response": None, "errors": failures}

    with ThreadPoolExecutor(max_workers=2) as pool:
        for record in pool.map(call, data["titles"] + data["groups"]):
            results.append(record)
            log = Path.home() / ".smolpaws/jev/calls.jsonl"
            log.parent.mkdir(parents=True, exist_ok=True)
            response = record.get("response") or {}
            with log.open("a") as stream:
                stream.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(),
                    "model": response.get("model"), "usage": response.get("usage"),
                    "tag": "dual-judge-title-study", "item_id": record["id"],
                    "success": bool(record["response"])}) + "\n")
            target.write_text(
                json.dumps(
                    {
                        "judge": P["judges"]["jev"],
                        "started_at": started,
                        "records": results,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n"
            )
            print(record["id"], "ok" if record["response"] else "failed", flush=True)
            recent = results[-3:]
            if len(recent) == 3 and all(not r["response"] for r in recent):
                raise RuntimeError("Three failed judgments; stop and inspect service")
    final = json.loads(target.read_text())
    final["finished_at"] = datetime.now(timezone.utc).isoformat()
    target.write_text(json.dumps(final, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "jev"])
    args = parser.parse_args()
    prepare() if args.action == "prepare" else jev()
