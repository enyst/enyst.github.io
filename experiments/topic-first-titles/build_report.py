"""Build the separately labeled follow-up report, without changing study one."""

import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT.parents[1]
P = json.loads((ROOT / "protocol.json").read_text())
D = {n: json.loads((ROOT / f"{n}.json").read_text()) for n in P["models"]}
J = json.loads((ROOT / "judgments.json").read_text())
A = {"default": "Default", "previous": "Previous override", "topic_first": "Topic-first override"}
N = {"haiku": "Haiku 4.5", "gemini": "Gemini 3 Flash Preview", "luna": "GPT-6 Luna · low"}
E = lambda x: html.escape(str(x), quote=True)
CASES = {c["id"]: c for c in P["cases"]}
LOOKUP = {(r["case_id"], r["title"]): r for r in J["titles"]}


def rows(split="all", model="all"):
    result = []
    for n, data in D.items():
        if model != "all" and n != model:
            continue
        for r in data["records"]:
            if split != "all" and r["split"] != split:
                continue
            if not r["title"]:
                continue
            result.append({**LOOKUP[(r["case_id"], r["title"])], "arm": r["arm"], "model": n})
    return result


def meter(counts):
    total = sum(counts.values())
    if not total:
        return "—"
    parts = "".join(f'<i class="{k}" style="width:{100*v/total:.3f}%"></i>' for k, v in counts.items() if k != "not_applicable")
    text = " · ".join(f"{counts[k]} {k}" for k in ("pass", "partial", "fail") if counts[k])
    return f'<div class="bar" role="img" aria-label="{E(text)}">{parts}</div><small>{E(text)} / {total}</small>'


def table(split="all", model="all"):
    title_rows = rows(split, model)
    criteria = [(r["id"], r["name"]) for r in P["rubric"]["rules"] if r["id"] not in ("consistent", "variation")] + [("fidelity", "Requested-work fidelity")]
    output = []
    for key, label in criteria:
        cells = []
        for arm in A:
            counts = Counter(r[key] for r in title_rows if r["arm"] == arm and r[key] != "not_applicable")
            cells.append("<td>" + meter(counts) + "</td>")
        output.append(f"<tr><th>{E(label)}</th>{''.join(cells)}</tr>")
    return '<div class="scroll"><table><thead><tr><th>Per-title criterion</th>' + "".join(f"<th>{a}</th>" for a in A.values()) + '</tr></thead><tbody>' + "".join(output) + '</tbody></table></div>'


def group_table():
    output = []
    for key, label in (("consistent", "Consistent structure"), ("variation", "Meaningful variation")):
        cells = []
        for arm in A:
            counts = Counter(g[key] for g in J["groups"] if g["arm"] == arm and g[key] != "not_applicable")
            cells.append('<td>' + meter(counts) + '</td>')
        output.append(f'<tr><th>{label}</th>{"".join(cells)}</tr>')
    return '<div class="scroll"><table><thead><tr><th>Family-level criterion</th>' + "".join(f'<th>{a}</th>' for a in A.values()) + '</tr></thead><tbody>' + "".join(output) + '</tbody></table></div>'


triplets = []
for model, data in D.items():
    for repeat in (1, 2):
        for case in P["cases"]:
            cells = []
            for arm in A:
                r = next(r for r in data["records"] if r["case_id"] == case["id"] and r["repeat"] == repeat and r["arm"] == arm)
                if r["title"]:
                    j = LOOKUP[(r["case_id"], r["title"])]
                    reason = j["reason"]
                    badges = " ".join(f'<span class="badge {j[k]}">{k}: {j[k]}</span>' for k in ("frontload", "fidelity"))
                else:
                    reason = "No usable displayed title." + (" Error: " + ", ".join(r["errors"]) if r["errors"] else " The helper returned None without an exception callback.")
                    badges = '<span class="badge fail">Failed generation</span>'
                cells.append(f'<div class="title {arm}"><div class="kicker">{A[arm]}</div><p class="generated">{E(r["title"] or "No title")}</p><div>{badges}</div><p class="reason">{E(reason)}</p><small>{r["characters"]} characters · {r["latency_seconds"]:.2f}s</small></div>')
            triplets.append(f'<article class="triplet" data-model="{model}" data-split="{case["split"]}" data-case="{case["id"]}"><div class="kicker">{N[model]} · run {repeat} · {case["id"]} · {case["split"]}</div><div class="three">{"".join(cells)}</div><details><summary>Original synthetic request</summary><pre>{E(case["input"])}</pre></details></article>')

all_rows = rows()
summary = {}
for arm in A:
    rr = [r for r in all_rows if r["arm"] == arm]
    summary[arm] = {"fidelity_fail": sum(r["fidelity"] == "fail" for r in rr), "frontload_pass": sum(r["frontload"] == "pass" for r in rr), "n": len(rr), "attempts": sum(r["arm"] == arm for d in D.values() for r in d["records"]), "ellipsis": sum(r["title"].endswith("...") for d in D.values() for r in d["records"] if r["arm"] == arm and r["title"])}
(ROOT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
summary_cards = "".join(f'<div><div class="kicker">{A[arm]}</div><strong>{s["frontload_pass"]}/{s["n"]}</strong><span>front-loading passes</span><p>{s["fidelity_fail"]} fidelity failures · {s["ellipsis"]} ellipsis endings · {s["attempts"]-s["n"]} missing titles</p></div>' for arm, s in summary.items())
model_tables = "".join(f'<details><summary>{name} · all cases</summary>{table(model=n)}</details>' for n, name in N.items())
prompts = "".join(f'<details><summary>{A[arm]} · {len(p) if p else 0} custom-prompt characters</summary><pre>{E(p or "No override: the unchanged SDK default user prompt applies.")}</pre></details>' for arm, p in P["prompts"].items())
groups = "".join(f'<details><summary>{N[g["model"]]} · {A[g["arm"]]} · run {g["repeat"]} · {g["family"]}</summary><p>Consistency: {g["consistent"]} · variation: {g["variation"]}</p><p>{E(g["reason"])}</p></details>' for g in J["groups"])
evidence = json.dumps({"protocol": P, "models": D, "judgments": J, "original_judgments": json.loads((ROOT / "judgments-original.json").read_text()), "adjudication": json.loads((ROOT / "adjudication.json").read_text()), "scoring_titles": (ROOT / "scoring-titles.txt").read_text(), "scoring_groups": (ROOT / "scoring-groups.txt").read_text(), "reproduction_notes": (ROOT / "reproduce.txt").read_text()}, ensure_ascii=False).replace("</", "<\\/")
page = r'''<!doctype html>
<!-- notebook-attribution: {"version":1,"contributions":[{"agent":"SmolPaws","llm":null,"date":"2026-10-30","role":"author"}]} -->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Topic-first titles: the follow-up — Engel’s Notebook</title>
<style>
:root{--bg:#f6f3eb;--paper:#fffdf8;--ink:#272b28;--muted:#62665e;--line:#d8d7ca;--teal:#286854;--gold:#916a2a;--pass:#337d67;--partial:#8b5f1e;--fail:#b34c40;--mono:ui-monospace,SFMono-Regular,Menlo,monospace;--sans:"Avenir Next","Segoe UI",sans-serif}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 var(--sans)}a{color:var(--teal);text-underline-offset:3px}.wrap{max-width:1400px;padding:42px 28px 90px;margin:auto;display:grid;grid-template-columns:160px minmax(0,1fr);gap:44px}nav{position:sticky;top:30px;align-self:start;font:12px/2 var(--mono)}nav ol{padding-left:18px}nav a{text-decoration:none}main{min-width:0}header{border-bottom:1px solid var(--line);padding:16px 0 30px}h1{font:normal clamp(45px,5.5vw,76px)/1.03 Georgia,serif;letter-spacing:-.04em;margin:18px 0 24px}h2{font:normal 34px/1.2 Georgia,serif;margin:46px 0 20px}h3{font-size:18px}.kicker{font:11px/1.8 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--gold)}.lead{font-size:20px;max-width:75ch}.muted,small{color:var(--muted)}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin:30px 0}.stats>div{border-top:3px solid var(--teal);padding:17px;background:var(--paper)}.stats strong{display:block;font:36px Georgia,serif;margin:10px 0}.stats span{font-size:13px}.stats p{font:11px/1.8 var(--mono)}.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.triplet{border-top:1px solid var(--line);padding:20px 0}.triplet>.kicker{margin-bottom:10px}.title{background:var(--paper);border:1px solid var(--line);border-top:3px solid #a9ad9d;padding:17px;min-width:0}.title.topic_first{border-top-color:var(--teal)}.generated{font-size:17px;font-weight:600;overflow-wrap:anywhere;line-height:1.5;min-height:55px}.reason{font-size:12px;color:var(--muted)}.badge{font:10px/2 var(--mono);display:inline-block;padding:0 5px;color:#fff;border-radius:2px}.pass{background:var(--pass)}.partial{background:var(--partial)}.fail{background:var(--fail)}details{border:1px solid var(--line);margin:12px 0}summary{padding:12px 15px;cursor:pointer;font-size:13px}details>p{margin:14px 18px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eae8df;padding:18px;font:12px/1.7 var(--mono);max-height:480px;overflow:auto;margin:0}.scroll{overflow:auto}table{width:100%;border-collapse:collapse}th,td{text-align:left;vertical-align:middle;padding:14px 12px;border-bottom:1px solid var(--line);min-width:160px}th{font-size:13px}thead th{font:11px var(--mono);color:var(--muted)}.bar{display:flex;height:11px;border-radius:2px;overflow:hidden;margin:0 0 6px}.bar i{display:block;height:100%}td small{font:10px/1.7 var(--mono)}.note{padding:15px 22px;background:#ece8d9;border-left:3px solid var(--gold);margin:23px 0}.filters{display:flex;gap:14px;flex-wrap:wrap;margin:20px 0}.filters label{font:12px var(--mono)}select{padding:8px;background:var(--paper);border:1px solid var(--line);font:14px var(--sans);margin-left:4px}code{font:12px var(--mono);background:#eae8df;padding:2px 5px}footer{border-top:1px solid var(--line);margin-top:45px;padding-top:25px;font-size:12px;color:var(--muted)}[hidden]{display:none!important}:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
@media(max-width:850px){.wrap{display:block;padding:22px 16px 60px}nav{position:static}nav ol{display:flex;gap:18px;flex-wrap:wrap}.three,.stats{grid-template-columns:1fr}h1{font-size:48px}.generated{min-height:0}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
</style></head><body><div class="wrap"><nav aria-label="Contents"><a href="../">← Engel’s Notebook</a><ol><li><a href="#results">Results</a></li><li><a href="#fresh">Fresh cases</a></li><li><a href="#collections">Collections</a></li><li><a href="#all">Every title</a></li><li><a href="#method">Method & evidence</a></li></ol></nav><main><header><div class="kicker">Follow-up experiment · 30 October 2026</div><h1>Put the topic first.<br>Then check the meaning.</h1><p class="lead">The shorter topic-first prompt improved front-loading in this sample, with fewer observed ellipsis endings. It still produced one missing title and did not make every collection consistent. Three models, three prompts, 24 requests. This follow-up tests a shorter topic-first override against both the SDK default and the previous action-first override. GPT-6 Luna joins through a ChatGPT subscription with low reasoning requested.</p><p><a href="readable-title-evaluation.html">Read the unchanged first experiment ↗</a></p></header><section id="results"><h2>Front-loading improves. Collection structure still varies.</h2><p>432 generation attempts: 24 cases × three prompts × two repeats × three models. 431 returned a displayed title. Gemini returned no usable title once for the topic-first long-input case; that missing title remains visible below. The quality charts exclude it and show their actual successful-title denominators. No combined “quality score” hides the differences.</p><div class="stats">@@CARDS@@</div><p>Green: pass. Amber: partial. Red: fail. Connotation applies only to feedback and the neutral database comparison. Fidelity checks whether the title still describes the requested work.</p>@@TABLE@@<p><strong>Scoring audit:</strong> deduplicating identical text did not prevent inconsistent treatment of equivalent wording across AI batches. Before publication, nine unique grades were adjudicated under the fixed rubric: six inspect/test fidelity grades and three clipped-detail parse grades. The tables use those corrected grades. <a href="../experiments/topic-first-titles/judgments-original.json">Original blind judgments</a> · <a href="../experiments/topic-first-titles/adjudication.json">Every correction</a>.</p><p class="muted">Pooled descriptive counts only. The models use different transports and sampling controls; inspect each model before generalizing.</p>@@MODEL_TABLES@@</section><section id="fresh"><h2>Separate familiar examples from fresh ones.</h2><p>The 16 reused requests informed the prompt revision. Eight fresh requests have no outputs in the first study. They were still designed by the same researcher after seeing that study, so they are not an independent external benchmark.</p><h3>Reused cases</h3>@@REUSED@@<h3>Fresh cases</h3>@@FRESH@@</section><section id="collections"><h2>Collections have their own denominators.</h2><p><strong>Important tradeoff:</strong> full consistency passes fell from 10/12 default groups to 4/12 topic-first groups; the previous override passed 9/12. Topic-first subjects did not produce a shared grammatical pattern reliably. Consistency is scored across auth and upgrade siblings. Meaningful variation also includes feedback and backup-operation groups. Each group belongs to one model, prompt, and repeat. Do not add these counts to the per-title scores.</p>@@GROUP_TABLE@@<details><summary>Every family judgment</summary>@@GROUPS@@</details></section><section id="all"><h2>All 144 matched comparisons.</h2><p>Each row contains three actual displayed SDK outputs for the same synthetic request. Exact duplicate request/title pairs share one blind judgment, even when different models produced them.</p><div class="filters"><label>Model <select id="model"><option value="all">All models</option><option value="haiku">Haiku 4.5</option><option value="gemini">Gemini 3 Flash</option><option value="luna">GPT-6 Luna · low</option></select></label><label>Cases <select id="split"><option value="all">All cases</option><option value="fresh">Fresh</option><option value="reused">Reused</option></select></label><span id="count" role="status" aria-live="polite">144 comparisons</span></div><div id="triplets">@@TRIPLETS@@</div></section><section id="method"><h2>Fixed prompts. Visible limits.</h2><p>The protocol was committed as <a href="https://github.com/enyst/enyst.github.io/commit/159f1b9">159f1b9</a> before the main run. One successful subscription smoke call preceded it and is excluded from the 432 attempts. The real SDK <code>generate_title_with_llm</code> helper receives the same full input and retains the same 50-character output cap in every arm. This compares bundled prompt changes, not the isolated causal effect of a skill.</p>@@PROMPTS@@<div class="note"><p><strong>Subscription detail:</strong> Luna uses <code>openai/gpt-6-luna</code>, confirmed by Engel instead of the initially requested “6.1 Luna.” Low reasoning is passed explicitly in the request’s extra body and checked in normalized SDK options. The subscription endpoint does not accept the temperature or output-token cap used by the other two models. Its server-side interpretation is not independently verified.</p><p><strong>Scoring:</strong> one AI judge model, blinded to model names, prompt labels, and generation instructions. Exact request/title duplicates are deduplicated before grading, then mapped back to every occurrence. Family groups are judged separately. This avoids the first experiment’s inconsistent duplicate grades; it does not turn AI judgments into human reading-speed measurements.</p><p><strong>Limits:</strong> a small synthetic convenience sample, two repeats, prompt tuning informed by study one, provider aliases rather than independently attested model builds. There is no human usability study, significance claim, or general guarantee. Ellipsis endings are observed text, not instrumented proof of SDK truncation.</p></div><h3>Audit and reproduction</h3><ul><li><a href="../experiments/topic-first-titles/protocol.json">Frozen protocol, exact prompts, cases, and rubric</a> · <a href="../experiments/topic-first-titles/run.py">Real SDK generation harness</a></li><li><a href="../experiments/topic-first-titles/haiku.json">All Haiku outputs</a> · <a href="../experiments/topic-first-titles/gemini.json">All Gemini outputs</a> · <a href="../experiments/topic-first-titles/luna.json">All Luna outputs</a></li><li><a href="../experiments/topic-first-titles/judgments.json">All mapped judgments</a> · <a href="../experiments/topic-first-titles/summary.json">Computed descriptive counts</a> · <a href="../experiments/topic-first-titles/build_report.py">Page generator</a> · <a href="../experiments/topic-first-titles/reproduce.txt">Reproduction notes</a> · <a href="../experiments/topic-first-titles/scoring-titles.txt">Title scoring prompt</a> · <a href="../experiments/topic-first-titles/scoring-groups.txt">Group scoring prompt</a></li><li><a href="https://github.com/OpenHands/software-agent-sdk/pull/6337">Input-cap SDK change #6337</a> · <a href="https://github.com/OpenHands/extensions/pull/871">Readable-text skill #871</a> · <a href="https://fsdatalab.github.io/blog/agent-text-at-scale/">Source writing principles</a></li></ul></section><footer>Generated by AI agent SmolPaws on behalf of Engel Nyst. Blind rubric judgments: Codex. All requests are synthetic. The first experiment remains unchanged.</footer></main></div><script id="evidence" type="application/json">@@EVIDENCE@@</script><script>const model=document.getElementById('model'),split=document.getElementById('split');function filter(){let n=0;document.querySelectorAll('#triplets .triplet').forEach(p=>{p.hidden=(model.value!=='all'&&p.dataset.model!==model.value)||(split.value!=='all'&&p.dataset.split!==split.value);if(!p.hidden)n++});document.getElementById('count').textContent=n+' comparisons'}model.addEventListener('change',filter);split.addEventListener('change',filter);</script></body></html>'''
for key, value in {"CARDS": summary_cards, "TABLE": table(), "MODEL_TABLES": model_tables, "REUSED": table("reused"), "FRESH": table("fresh"), "GROUP_TABLE": group_table(), "GROUPS": groups, "TRIPLETS": "".join(triplets), "PROMPTS": prompts, "EVIDENCE": evidence}.items():
    page = page.replace("@@" + key + "@@", value)
assert "@@" not in page
output = SITE / "arch/topic-first-title-evaluation.html"
output.write_text(page)
print(output, len(page))
