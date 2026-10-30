"""Build dual-judge title evidence without changing either prior study."""

import html
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SITE = ROOT.parents[1]
P = json.loads((ROOT / "protocol.json").read_text())
D = {n: json.loads((ROOT / f"{n}.json").read_text()) for n in P["models"]}
ITEMS = json.loads((ROOT / "blinded-items.json").read_text())
M = json.loads((ROOT / "mapping.json").read_text())
CODEX = json.loads((ROOT / "codex.json").read_text())
JEV = json.loads((ROOT / "jev.json").read_text())
C = {r["id"]: r["answers"] for r in CODEX["items"]}
V = {r["id"]: r for r in JEV["records"]}
T = {(r["case_id"], r["title"]): r["id"] for r in ITEMS["titles"]}
APPLICABLE = {r["id"]: r["criteria"] for r in ITEMS["titles"] + ITEMS["groups"]}
E = lambda x: html.escape(str(x), quote=True)
ARMS = {"default": "SDK default", "fixed": "Topic — action"}
MODELS = {"haiku": "Haiku 4.5", "gemini": "Gemini 3 Flash Preview", "luna": "GPT-6 Luna · low"}
RULES = {"clarity": "Clear task", "frontload": "Topic first", "connotation": "Connotation", "fidelity": "Requested-work fidelity", "collection": "Consistent, meaningful collection"}


def label(judge, id, criterion):
    if judge == "codex":
        return C.get(id, {}).get(criterion)
    record = V.get(id, {}).get("response")
    return record.get("answers", {}).get(criterion, {}).get("choice") if record else None


def counts(judge, criterion, arm, model="all"):
    if criterion == "collection":
        ids = [id for id, m in M.items() if id.startswith("g") and m["arm"] == arm and (model == "all" or m["model"] == model)]
    else:
        ids = [T[(r["case_id"], r["title"])] for n, d in D.items() if model in ("all", n) for r in d["records"] if r["arm"] == arm and r["title"] and criterion in APPLICABLE[T[(r["case_id"], r["title"])]]]
    result = Counter(label(judge, id, criterion) or "missing" for id in ids)
    return result


def meter(c):
    total = sum(c.values())
    if not total:
        return "Not applicable"
    pieces = "".join(f'<i class="{k}" style="width:{100*c[k]/total:.3f}%"></i>' for k in ("pass", "partial", "fail", "missing") if c[k])
    caption = " · ".join(f"{c[k]} {k}" for k in ("pass", "partial", "fail", "missing") if c[k])
    return f'<div class="bar" role="img" aria-label="{E(caption)}">{pieces}</div><small>{E(caption)} · n={total}</small>'


def scorecard(model="all"):
    rows = []
    for key, name in RULES.items():
        cells = "".join('<td>' + meter(counts(judge, key, arm, model)) + '</td>' for judge in ("codex", "jev") for arm in ARMS)
        unit = "collection groups" if key == "collection" else "title occurrences, applicable cases only"
        rows.append(f'<tr><th>{name}<small>{unit}</small></th>{cells}</tr>')
    return '<div class="scroll"><table><thead><tr><th>Criterion</th><th colspan="2">Codex / gpt-6-astra</th><th colspan="2">Jev / jev-1.14.0</th></tr><tr><th></th>' + ''.join(f'<th>{a}</th>' for _ in range(2) for a in ARMS.values()) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'


agreement = []
disagreements = []
for row in ITEMS["titles"] + ITEMS["groups"]:
    for key in row["criteria"]:
        c, v = label("codex", row["id"], key), label("jev", row["id"], key)
        agreement.append({"id": row["id"], "criterion": key, "codex": c, "jev": v, "agreement": c == v if c and v else None})
        if c and v and c != v:
            probabilities = V[row["id"]]["response"]["answers"][key]
            content = f'<pre>{E(json.dumps(row.get("items", {k: row[k] for k in ("request", "title", "first_two_words") if k in row}), ensure_ascii=False, indent=2))}</pre>'
            disagreements.append(f'<details class="disagreement" data-rule="{key}"><summary>{row["id"]} · {RULES[key]} · Codex {c} / Jev {v} · confidence {probabilities.get("confidence", 0):.3f}</summary>{content}<pre>{E(json.dumps(probabilities, ensure_ascii=False, indent=2))}</pre></details>')
summary = {"generation_attempts": sum(len(d["records"]) for d in D.values()), "displayed_titles": sum(bool(r["title"]) for d in D.values() for r in d["records"]), "unique_titles": len(ITEMS["titles"]), "groups": len(ITEMS["groups"]), "scores": {j: {k: {a: dict(counts(j, k, a)) for a in ARMS} for k in RULES} for j in ("codex", "jev")}, "agreement": {k: {"compared": sum(r["criterion"] == k and r["agreement"] is not None for r in agreement), "agreed": sum(r["criterion"] == k and r["agreement"] is True for r in agreement)} for k in RULES}, "disagreements": len(disagreements)}
(ROOT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
(ROOT / "agreement.json").write_text(json.dumps(agreement, indent=2) + "\n")
agreement_rows = ''.join(f'<tr><th>{RULES[k]}</th><td>{s["agreed"]}/{s["compared"]}</td><td>{s["compared"]-s["agreed"]}</td></tr>' for k, s in summary["agreement"].items())
comparisons = []
for model, data in D.items():
    for repeat in (1, 2):
        for case in P["cases"]:
            cards = []
            for arm in ARMS:
                r = next(r for r in data["records"] if r["case_id"] == case["id"] and r["arm"] == arm and r["repeat"] == repeat)
                if r["title"]:
                    id = T[(r["case_id"], r["title"])]
                    badges = ''.join(f'<div class="judge"><b>{name}</b> ' + ' '.join(f'<span class="badge {label(j, id, k) or "missing"}">{k}: {label(j, id, k) or "missing"}</span>' for k in ("clarity", "frontload", "fidelity")) + '</div>' for j, name in (("codex", "Codex"), ("jev", "Jev")))
                else:
                    badges = '<span class="badge fail">Generation failure</span>'
                format_ok = bool(r["title"] and re.search(r"\S\s+—\s+\S", r["title"]))
                cards.append(f'<div class="card {arm}"><div class="kicker">{ARMS[arm]}</div><p class="generated">{E(r["title"] or "No title")}</p>{badges}<small>{r["characters"]} Python characters · em-dash layout {"yes" if format_ok else "no"}</small></div>')
            comparisons.append(f'<article class="pair" data-model="{model}"><div class="kicker">{MODELS[model]} · run {repeat} · {case["id"]}</div><div class="two">{"".join(cards)}</div><details><summary>Original synthetic request</summary><pre>{E(case["input"])}</pre></details></article>')
models = ''.join(f'<details><summary>{name} · all five evaluation dimensions</summary>{scorecard(n)}</details>' for n, name in MODELS.items())
criteria = ''.join(f'<details><summary>{RULES[k]}</summary><p>{E(r["instructions"])}</p><pre>{E(json.dumps(r["criteria"], ensure_ascii=False, indent=2))}</pre></details>' for k, r in P["rubric"].items())
format_counts = {a: sum(bool(r["title"] and re.search(r"\S\s+—\s+\S", r["title"])) for d in D.values() for r in d["records"] if r["arm"] == a) for a in ARMS}
embedded = json.dumps({"protocol": P, "models": D, "items": ITEMS, "mapping": M, "codex": CODEX, "jev": JEV, "summary": summary, "agreement": agreement, "codex_instructions": json.loads((ROOT / "codex-instructions.json").read_text()), "reproduction_notes": (ROOT / "reproduce.txt").read_text()}, ensure_ascii=False).replace('</', '<\\/')
page = r'''<!doctype html>
<!-- notebook-attribution: {"version":1,"contributions":[{"agent":"SmolPaws","llm":null,"date":"2026-10-30","role":"author"}]} -->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Two judges, four title rules — Engel’s Notebook</title><style>
:root{--bg:#f6f3eb;--paper:#fffdf8;--ink:#272b28;--muted:#62665e;--line:#d8d7ca;--teal:#286854;--gold:#916a2a;--pass:#337d67;--partial:#8b5f1e;--fail:#b34c40;--mono:ui-monospace,SFMono-Regular,Menlo,monospace;--sans:"Avenir Next","Segoe UI",sans-serif}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 var(--sans)}a{color:var(--teal);text-underline-offset:3px}.wrap{display:grid;grid-template-columns:165px minmax(0,1fr);gap:45px;max-width:1320px;margin:auto;padding:42px 26px 90px}nav{position:sticky;top:24px;align-self:start;font:12px/2 var(--mono)}nav ol{padding-left:18px}main{min-width:0}header{border-bottom:1px solid var(--line);padding:10px 0 28px}h1{font:normal clamp(42px,5.5vw,75px)/1.04 Georgia,serif;letter-spacing:-.04em;margin:20px 0}h2{font:normal 33px/1.2 Georgia,serif;margin:45px 0 18px}.lead{font-size:20px;max-width:70ch}.kicker{font:11px/1.8 var(--mono);text-transform:uppercase;letter-spacing:.07em;color:var(--gold)}.muted,small{color:var(--muted)}.note{background:#e9e6d9;border-left:3px solid var(--gold);padding:15px 21px;margin:24px 0}.scroll{overflow:auto}table{width:100%;border-collapse:collapse}th,td{text-align:left;vertical-align:middle;border-bottom:1px solid var(--line);padding:14px 11px;min-width:145px}th small{display:block;font-size:11px;font-weight:normal}thead th{font:11px var(--mono);color:var(--muted)}tbody th{font-size:13px}.bar{display:flex;height:11px;border-radius:2px;overflow:hidden;margin:0 0 7px}.bar i{height:100%;display:block}td small{font:10px/1.7 var(--mono)}.pass{background:var(--pass)}.partial{background:var(--partial)}.fail{background:var(--fail)}.missing{background:#62665e}.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}.pair{padding:22px 0;border-top:1px solid var(--line)}.pair>.kicker{margin-bottom:12px}.card{background:var(--paper);border:1px solid var(--line);border-top:3px solid #a9ad9d;padding:19px;min-width:0}.card.fixed{border-top-color:var(--teal)}.generated{font-size:18px;line-height:1.5;font-weight:600;overflow-wrap:anywhere}.badge{display:inline-block;padding:0 5px;color:white;font:10px/2 var(--mono);border-radius:2px;margin:0 1px 2px 0}.judge{font-size:11px;margin:8px 0}.judge b{display:inline-block;width:46px}.card small{font:10px var(--mono)}details{border:1px solid var(--line);margin:12px 0}summary{padding:12px 15px;cursor:pointer;font-size:13px}details>p{margin:15px 18px}pre{margin:0;background:#eae8df;padding:18px;white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.7 var(--mono);max-height:450px;overflow:auto}code{background:#eae8df;font:12px var(--mono);padding:2px 5px}select{padding:8px;background:var(--paper);border:1px solid var(--line);font:14px var(--sans)}.filters{display:flex;gap:15px;margin:20px 0;align-items:center}footer{border-top:1px solid var(--line);margin-top:45px;padding-top:22px;font-size:12px;color:var(--muted)}[hidden]{display:none!important}:focus-visible{outline:3px solid var(--gold);outline-offset:3px}@media(max-width:850px){.wrap{display:block;padding:24px 16px 60px}nav{position:static}nav ol{display:flex;gap:20px;flex-wrap:wrap}.two{grid-template-columns:1fr}h1{font-size:48px}}
</style></head><body><div class="wrap"><nav aria-label="Contents"><a href="../">← Notebook</a><ol><li><a href="#rules">Four rules</a></li><li><a href="#scores">Two scorecards</a></li><li><a href="#agreement">Judge agreement</a></li><li><a href="#outputs">Every title</a></li><li><a href="#method">Method & evidence</a></li></ol></nav><main><header><div class="kicker">Title experiment three · 30 October 2026</div><h1>One title format.<br>Two independent judges.</h1><p class="lead">A fixed “Topic — action” prompt combines consistent structure with meaningful differences. Codex and Jev independently classify the same displayed titles and sibling collections. Their disagreements remain visible; neither is treated as ground truth.</p><p>@@TOTAL@@ generations · @@UNIQUE@@ unique title texts for judging · 48 collections</p><p><a href="readable-title-evaluation.html">First experiment</a> · <a href="topic-first-title-evaluation.html">Topic-first follow-up</a> — both unchanged.</p></header><section id="rules"><h2>Four instructions, plus a fidelity gate.</h2><ol><li>Make the task clear.</li><li>Put distinguishing topic words first.</li><li>Keep parallel structure and meaningful distinctions together.</li><li>Preserve connotation when sentiment matters.</li></ol><p>“Make variation meaningful” is merged with collection consistency. It remains part of the evaluation. Requested-work fidelity is a separate requirement: a polished title still fails if it changes the task.</p><details><summary>Exact fixed-format prompt</summary><pre>@@PROMPT@@</pre></details><details><summary>Exact shared scoring rubric</summary>@@CRITERIA@@</details><p class="muted">Format is measured in code, not by either judge: the em-dash layout occurred in @@FIXED_FORMAT@@/144 fixed-prompt titles and @@DEFAULT_FORMAT@@/144 default titles. This check does not prove that the topic or action is correct.</p></section><section id="scores"><h2>Both judges favor topic-first. Collections divide them.</h2><div class="note"><p><strong>Shared finding:</strong> the fixed format improved front-loading: Codex 107/144 → 144/144; Jev 102/144 → 141/144. Both gave all 144 fixed-format titles a fidelity pass. These are classifier judgments on the tuned set, not proof of correctness.</p><p><strong>Unsettled:</strong> collection passes moved in opposite directions. Codex: 15/24 → 13/24. Jev: 17/24 → 19/24. The judges agreed on only 30/48 collection grades. I would inspect those disagreements before changing the SDK default.</p></div><p>Green means pass, amber partial, red fail, gray missing judge result. Per-title scores count every generated occurrence, even when identical text is judged once. Collection scores use their own denominators. No manual grade adjustments are applied.</p>@@SCORECARD@@<p class="muted">The four writing principles appear as clarity, topic-first, collection, and applicable connotation. Fidelity is separate. Model-specific results:</p>@@MODELS@@</section><section id="agreement"><h2>Agreement is a measurement of judges, not truth.</h2><p>The table compares one label for each unique request/title/criterion, plus the separate collection judgments. It does not overweight repeated identical outputs. No human gold labels were supplied.</p><div class="scroll"><table><thead><tr><th>Criterion</th><th>Agreed / compared</th><th>Disagreed</th></tr></thead><tbody>@@AGREEMENT@@</tbody></table></div><div class="note"><p>Jev’s confidence is calculated from its answer-probability distribution. High confidence is not proof of correctness. All raw probabilities remain available. Codex returns labels, not comparable probabilities. There is no combined “best judge” or averaged quality score.</p></div><h3>All @@DISAGREEMENT_COUNT@@ disagreements</h3><div class="filters"><label>Criterion <select id="rule"><option value="all">All</option><option value="clarity">Clear task</option><option value="frontload">Topic first</option><option value="fidelity">Fidelity</option><option value="connotation">Connotation</option><option value="collection">Collections</option></select></label></div><div id="disagreements">@@DISAGREEMENTS@@</div></section><section id="outputs"><h2>All 144 matched title pairs.</h2><p>Default and fixed-format outputs were freshly generated, not copied from earlier studies. Expand a request before deciding which judge you agree with.</p><div class="filters"><label>Model <select id="model"><option value="all">All three</option><option value="haiku">Haiku 4.5</option><option value="gemini">Gemini 3 Flash</option><option value="luna">GPT-6 Luna · low</option></select></label><span id="count" role="status" aria-live="polite">144 pairs</span></div><div id="pairs">@@PAIRS@@</div></section><section id="method"><h2>A diagnostic set, not a new benchmark.</h2><p>All 24 synthetic requests appeared in experiment two. They informed the prompt and rubric, so none is held-out validation here. Three generators × two prompts × two repeats produce 288 planned attempts. The protocol was committed before generation.</p><ul><li><strong>Generation:</strong> real SDK helper at <code>01bb167</code>; full input and the same 50-character display cap in both arms. Haiku and Gemini use the eval-proxy route with temperature 0 requested, 256 output tokens, reasoning none. Luna uses ChatGPT subscription, low reasoning requested, with no temperature/output-token control.</li><li><strong>Codex judge:</strong> gpt-6-astra, medium reasoning, three blinded title batches and one collection batch. Labels only; no explanations were requested.</li><li><strong>Jev judge:</strong> pinned jev-1.14.0 through TypeSafe’s API. One minimal request/title state with applicable Choice questions, or one sibling group with the collection question. Raw selected choices, probabilities, confidence, usage and errors are retained.</li><li><strong>Blinding:</strong> neither judge receives generator names, prompt arm labels, generation instructions or the other judge’s answers. Both receive the same semantic questions, criteria, original request and displayed title. Jev option order is deterministically shuffled; Codex reads the rubric in its saved order. This interface difference is a limitation.</li><li><strong>Deterministic checks:</strong> code computes title length, em-dash compliance and the first two Unicode lexical words. Both judges see those first two words. This parser is an operational definition, not a universal linguistic boundary.</li><li><strong>Calibration:</strong> none established on human-labeled title data. This study compares judge outputs; agreement alone cannot validate either judge.</li></ul><p>The generation cap retains ordinary Python string-length semantics. An observed “...” ending is not an independently recorded raw-model truncation event. No private conversations, memory, auth files or credentials were sent as classification state.</p><h3>Evidence and reproduction</h3><ul><li><a href="../experiments/dual-judge-titles/protocol.json">Frozen protocol and rubric</a> · <a href="../experiments/dual-judge-titles/run.py">Generation harness</a> · <a href="../experiments/dual-judge-titles/score.py">Jev request construction and raw scoring harness</a></li><li><a href="../experiments/dual-judge-titles/haiku.json">Haiku results</a> · <a href="../experiments/dual-judge-titles/gemini.json">Gemini results</a> · <a href="../experiments/dual-judge-titles/luna.json">Subscription Luna results</a></li><li><a href="../experiments/dual-judge-titles/blinded-items.json">Both judges’ input states</a> · <a href="../experiments/dual-judge-titles/mapping.json">Revealed mappings</a> · <a href="../experiments/dual-judge-titles/codex.json">Codex labels</a> · <a href="../experiments/dual-judge-titles/jev.json">Jev raw answers</a></li><li><a href="../experiments/dual-judge-titles/codex-instructions.json">Exact Codex instructions</a> · <a href="../experiments/dual-judge-titles/reproduce.txt">Reproduction notes</a> · <a href="../experiments/dual-judge-titles/agreement.json">Per-decision agreement</a> · <a href="../experiments/dual-judge-titles/summary.json">Computed summary</a> · <a href="../experiments/dual-judge-titles/build_report.py">Offline page generator</a></li><li><a href="https://docs.typesafe.ai/primitives/choice">TypeSafe Choice documentation</a> · <a href="https://docs.typesafe.ai/confidence">What confidence means</a></li></ul></section><footer>Generated by AI agent SmolPaws on behalf of Engel Nyst. Independent AI classifiers: Codex and Jev. Original unadjudicated grades are shown. All inputs are synthetic public examples.</footer></main></div><script type="application/json" id="evidence">@@EVIDENCE@@</script><script>document.getElementById('model').addEventListener('change',e=>{let n=0;document.querySelectorAll('#pairs .pair').forEach(p=>{p.hidden=e.target.value!=='all'&&p.dataset.model!==e.target.value;if(!p.hidden)n++});document.getElementById('count').textContent=n+' pairs'});document.getElementById('rule').addEventListener('change',e=>document.querySelectorAll('#disagreements .disagreement').forEach(p=>p.hidden=e.target.value!=='all'&&p.dataset.rule!==e.target.value));</script></body></html>'''
for key, value in {"TOTAL": summary["generation_attempts"], "UNIQUE": summary["unique_titles"], "PROMPT": E(P["prompts"]["fixed"]), "CRITERIA": criteria, "FIXED_FORMAT": format_counts["fixed"], "DEFAULT_FORMAT": format_counts["default"], "SCORECARD": scorecard(), "MODELS": models, "AGREEMENT": agreement_rows, "DISAGREEMENT_COUNT": len(disagreements), "DISAGREEMENTS": ''.join(disagreements), "PAIRS": ''.join(comparisons), "EVIDENCE": embedded}.items():
    page = page.replace('@@' + key + '@@', str(value))
assert '@@' not in page
out = SITE / 'arch/dual-judge-title-evaluation.html'
out.write_text(page)
print(out, len(page))
