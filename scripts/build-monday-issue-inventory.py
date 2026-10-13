#!/usr/bin/env python3
"""Render the Monday issue inventory from a checked GitHub data snapshot.

Input: assets/openhands-monday-issue-inventory/data.json
Optional decision labels: assets/openhands-maintainer-reports/triage.json
This script never fetches GitHub, changes an issue, or reuses a proposed fix.
"""
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import csv
import html
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/openhands-monday-issue-inventory"
OUTPUT = ROOT / "investigations/openhands-issues-since-monday.html"
OWN = {"enyst", "smolpaws"}
LOCAL = ZoneInfo("Europe/Stockholm")
esc = lambda value: html.escape(str(value), quote=True)


def parse_date(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def stamp(value, seconds=False):
    date = parse_date(value).astimezone(LOCAL)
    clock = date.strftime("%H:%M:%S" if seconds else "%H:%M")
    text = f"{date.day} {date.strftime('%B %Y')}, {clock} {date.tzname()}"
    return f'<time datetime="{esc(value)}">{text}</time>'


def author(login):
    return f'<a href="https://github.com/{esc(login)}">{esc(login)}</a>'


def merged(pr):
    return bool(pr.get("merged") or pr.get("merged_at") or pr["state"] == "merged")


def active(pr):
    return pr["state"] == "open" and not merged(pr)


def pr_state(pr):
    if merged(pr):
        return "Merged", "merged"
    if active(pr):
        return ("Draft · open", "draft") if pr.get("draft") else ("Open", "open")
    return "Closed without merge", "unmerged"


def bucket(issue):
    if issue["state"] == "closed":
        return "closed"
    return "with-own" if issue["own_prs"] else "without-own"


def pr_list(prs, issue, triage):
    parts = []
    closers = {pr["number"] for pr in issue.get("direct_closing_prs", [])}
    for pr in sorted(prs, key=lambda item: -item["number"]):
        label, color = pr_state(pr)
        decision = triage.get(pr["number"])
        triage_link = ""
        if decision:
            review_decision = decision["decision"] if decision["decision"] in {"keep", "close"} else decision.get("original_decision")
            if review_decision == "close":
                decision_text, decision_color = "Close", "close"
            elif review_decision == "keep":
                decision_text, decision_color = "Keep", "keep"
            else:
                decision_text, decision_color = "Archived", "unmerged"
            prefix = "Prior review" if decision["decision"] == "archive" and review_decision else "PR review"
            triage_link = f'<a class="status {decision_color}" href="openhands-pr-keep-close.html#pr-{pr["number"]}">{prefix}: {decision_text}</a>'
        scope = esc(pr.get("scope") or "")
        if pr.get("fix_scope") == "partial" and not scope:
            scope = "Partial implementation proposal; does not establish a complete fix."
        scope_note = f'<p class="scope-note">{scope}</p>' if scope else ""
        direct = pr.get("direct_closer") or pr["number"] in closers
        closer_note = '<p class="audit-note">GitHub’s issue closure event identifies this PR as the closer.</p>' if direct else ""
        dates = ""
        if merged(pr) and pr.get("merged_at"):
            dates = f'<p class="byline">Merged {stamp(pr["merged_at"])}</p>'
        elif not active(pr) and pr.get("closed_at"):
            dates = f'<p class="byline">Closed {stamp(pr["closed_at"])}</p>'
        evidence = pr.get("evidence") or {}
        evidence_urls = list(dict.fromkeys(evidence.get("urls", []))) if isinstance(evidence, dict) else []
        refs = ""
        if evidence_urls:
            links = "".join(f'<li><a href="{esc(url)}">{esc(url)}</a></li>' for url in evidence_urls)
            refs = f'<details class="evidence"><summary>Issue–PR matching evidence</summary><ul>{links}</ul></details>'
        parts.append(f'''<li class="pr-row"><div class="pr-top"><a class="number" href="{esc(pr['url'])}">PR #{pr['number']}</a><span class="status {color}">{label}</span><span class="byline">by {author(pr['author'])}</span>{triage_link}</div><a class="pr-title" href="{esc(pr['url'])}">{esc(pr['title'])}</a>{dates}{scope_note}{closer_note}{refs}</li>''')
    return '<ul class="pr-list">' + "\n".join(parts) + "</ul>"


def issue_card(issue, triage):
    own_prs, other_prs = issue["own_prs"], issue["other_prs"]
    own_open = sum(active(pr) for pr in own_prs)
    other_open = sum(active(pr) for pr in other_prs)
    group = bucket(issue)
    search = " ".join([str(issue["number"]), issue["title"], issue["author"]] + [f'{pr["number"]} {pr["title"]} {pr["author"]}' for pr in own_prs + other_prs]).lower()
    state_label = "Open issue" if issue["state"] == "open" else "Closed issue"
    issue_color = "open" if issue["state"] == "open" else "unmerged"
    own_label = "Has own PR" if own_prs else "No own PR"
    own_color = "own" if own_prs else "missing"
    closed_at = f' · Closed {stamp(issue["closed_at"])}' if issue.get("closed_at") and issue["state"] == "closed" else ""
    own_content = pr_list(own_prs, issue, triage) if own_prs else '<p class="no-match">No implementation PR by enyst or smolpaws identified, in any state.</p>'
    flags = ""
    if issue["state"] == "open" and own_prs and all(not active(pr) and not merged(pr) for pr in own_prs):
        flags = '<p class="attention-note">The own-author PRs were closed without merge. This open issue has no active own-author PR.</p>'
    elif issue["state"] == "open" and any(merged(pr) for pr in own_prs):
        flags = '<p class="attention-note">An own-author PR was merged, but the issue remains open. Check remaining scope or issue closure before deciding whether a new fix is needed.</p>'
    if other_prs:
        other_content = f'<details class="other-proposals"><summary>Other-author proposals · {len(other_prs)} total · {other_open} open</summary><p class="context-note">Context for the inventory. Proposals marked Close are intended to be superseded by independent maintainer fixes.</p>{pr_list(other_prs, issue, triage)}</details>'
    else:
        other_content = '<p class="context-note no-other">Other-author proposals: none identified.</p>'
    notes = list(dict.fromkeys(issue[key] for key in ["note", "closure_note", "reconciliation_note", "status_drift_note"] if issue.get(key)))
    note = "".join(f'<p class="audit-note">{esc(text)}</p>' for text in notes)
    excluded = issue.get("excluded_references") or []
    excluded_content = ""
    if excluded:
        rows = "".join(f'<li><a href="{esc(pr["url"])}">PR #{pr["number"]}</a> · {esc(pr["title"])} · {esc(pr.get("reason") or "Incidental reference; not an implementation match.")}</li>' for pr in excluded)
        excluded_content = f'<details class="evidence excluded-refs"><summary>{len(excluded)} reference' + ('s' if len(excluded) != 1 else '') + f' excluded from PR counts</summary><ul>{rows}</ul></details>'
    return f'''<article class="issue-card" id="issue-{issue['number']}" data-group="{group}" data-search="{esc(search)}" data-author="{esc(issue['author'].lower())}" data-own-open="{own_open}"><div class="issue-heading"><a class="number" href="{esc(issue['url'])}">Issue #{issue['number']}</a><span class="status {issue_color}">{state_label}</span><span class="status {own_color}">{own_label}</span></div><h3><a href="{esc(issue['url'])}">{esc(issue['title'])}</a></h3><p class="byline">Posted by {author(issue['author'])} · Created {stamp(issue['created_at'])}{closed_at}</p><p class="pr-counts"><strong>{own_open} open own-author PR{'s' if own_open != 1 else ''}</strong><span>{other_open} open other-author PR{'s' if other_open != 1 else ''}</span></p>{flags}<div class="issue-prs"><h4>PRs by enyst / smolpaws · {len(own_prs)} total · all states</h4>{own_content}{note}</div>{other_content}{excluded_content}</article>'''


def write_csv(records):
    columns = ["issue", "issue_title", "issue_author", "issue_url", "issue_state", "issue_created_at", "has_own_pr", "own_open_pr_count", "other_open_pr_count", "pr", "pr_title", "pr_author", "pr_url", "pr_state", "pr_draft", "pr_merged_at", "pr_fix_scope", "pr_is_own", "pr_direct_closer"]
    with (ASSETS / "inventory.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for issue in records:
            base = {"issue": issue["number"], "issue_title": issue["title"], "issue_author": issue["author"], "issue_url": issue["url"], "issue_state": issue["state"], "issue_created_at": issue["created_at"], "has_own_pr": bool(issue["own_prs"]), "own_open_pr_count": sum(active(pr) for pr in issue["own_prs"]), "other_open_pr_count": sum(active(pr) for pr in issue["other_prs"])}
            closers = {pr["number"] for pr in issue.get("direct_closing_prs", [])}
            for pr in issue["own_prs"] + issue["other_prs"] or [None]:
                values = dict(base)
                if pr:
                    values.update({"pr": pr["number"], "pr_title": pr["title"], "pr_author": pr["author"], "pr_url": pr["url"], "pr_state": pr_state(pr)[0], "pr_draft": bool(pr.get("draft")), "pr_merged_at": pr.get("merged_at") or "", "pr_fix_scope": pr.get("fix_scope") or "", "pr_is_own": pr["author"].lower() in OWN, "pr_direct_closer": bool(pr.get("direct_closer") or pr["number"] in closers)})
                writer.writerow(values)


def main():
    data = json.loads((ASSETS / "data.json").read_text())
    records = sorted(data["records"], key=lambda issue: -issue["number"])
    start, end = parse_date(data["window"]["start"]), parse_date(data["window"]["end"])
    assert len(records) == len({issue["number"] for issue in records}), "Duplicate issues"
    assert all(issue["author"].lower() in OWN for issue in records), "Unexpected issue author"
    assert all(start <= parse_date(issue["created_at"]) <= end for issue in records), "Issue outside inclusive frozen window"
    assert all(issue["state"] in {"open", "closed"} for issue in records), "Unknown issue state"
    for issue in records:
        assert all(pr["author"].lower() in OWN for pr in issue["own_prs"])
        assert all(pr["author"].lower() not in OWN for pr in issue["other_prs"])
        assert len(issue["own_prs"] + issue["other_prs"]) == len({pr["number"] for pr in issue["own_prs"] + issue["other_prs"]}), "Duplicate PR match"
        assert issue.get("has_own_pr", bool(issue["own_prs"])) == bool(issue["own_prs"])
        assert all(pr["state"] in {"open", "closed", "merged"} for pr in issue["own_prs"] + issue["other_prs"]), "Unknown PR state"
        if "own_open_pr_count" in issue:
            assert issue["own_open_pr_count"] == sum(active(pr) for pr in issue["own_prs"]), "Own open-PR count mismatch"
        if "other_open_pr_count" in issue:
            assert issue["other_open_pr_count"] == sum(active(pr) for pr in issue["other_prs"]), "Other open-PR count mismatch"
    triage_path = ROOT / "assets/openhands-maintainer-reports/triage.json"
    triage_data = json.loads(triage_path.read_text()) if triage_path.exists() else {"records": []}
    triage = {row["pr"]: row for row in triage_data["records"]}
    groups = {key: [issue for issue in records if bucket(issue) == key] for key in ["without-own", "with-own", "closed"]}
    missing, with_own, closed = (groups[key] for key in ["without-own", "with-own", "closed"])
    closed_own = sum(bool(issue["own_prs"]) for issue in closed)
    own_total = len(with_own) + closed_own
    no_own_total = len(records) - own_total
    open_total = len(missing) + len(with_own)
    own_open_issues = sum(any(active(pr) for pr in issue["own_prs"]) for issue in missing + with_own)
    closed_only = sum(bool(issue["own_prs"]) and all(not active(pr) and not merged(pr) for pr in issue["own_prs"]) for issue in with_own)
    distinct_own = {pr["number"] for issue in records for pr in issue["own_prs"]}
    distinct_other_open = {pr["number"] for issue in records for pr in issue["other_prs"] if active(pr)}
    fetched = data.get("fetch_finished_at")
    fetched_start = data.get("fetch_started_at")
    fetched_note = f' Status checked through {stamp(fetched)}.' if fetched else ""
    metadata_interval = f' Metadata was read from {stamp(fetched_start, True)} through {stamp(fetched, True)}; these reads were not simultaneous.' if fetched and fetched_start else ""
    descriptions = {
        "without-own": ("Open without your PR", "These are the remaining open issues for which no implementation PR by enyst or smolpaws was identified, across open, merged and closed states."),
        "with-own": ("Open with your PR", "At least one implementation PR by enyst or smolpaws exists. The badges distinguish active work, merged partial work and proposals closed without merge."),
        "closed": ("Closed issues · archive", "Retained to account for every issue posted in the window. An issue being closed does not by itself establish that all reported behavior was fixed. Own-author PR matches use the same all-state rule."),
    }
    sections = []
    for key in ["without-own", "with-own", "closed"]:
        title, explanation = descriptions[key]
        rows = groups[key]
        content = "\n".join(issue_card(issue, triage) for issue in rows) if rows else '<p class="no-match">No issues in this group.</p>'
        sections.append(f'<section id="{key}" data-inventory-section><h2 class="section-heading">{title} · {len(rows)}</h2><p class="section-intro">{explanation}</p><div class="issue-list">{content}</div></section>')
    choices = [("without-own", f"Open without own PR · {len(missing)}"), ("no-active-own", f"Open with no active own PR · {open_total-own_open_issues}"), ("with-own", f"Open with own PR · {len(with_own)}"), ("open", f"All open issues · {open_total}"), ("closed", f"Closed archive · {len(closed)}"), ("all", f"All issues · {len(records)}")]
    options = "".join(f'<option value="{key}">{esc(label)}</option>' for key, label in choices)
    authors = "".join(f'<option value="{login}">{login}</option>' for login in sorted(OWN))
    triage_stamp = triage_data.get("observed_at") or triage_data.get("metadata_observed_until")
    triage_note = f' The related review labels were last refreshed {stamp(triage_stamp, True)}.' if triage_stamp else ""
    closed_only_links = ", ".join(f'<a href="#issue-{issue["number"]}">#{issue["number"]}</a>' for issue in with_own if all(not active(pr) and not merged(pr) for pr in issue["own_prs"]))
    closed_only_note = f' These are {closed_only_links}.' if closed_only_links else ""
    body = f'''<header class="report-header"><p class="eyebrow">OpenHands / OpenHands · Maintainer issue inventory</p><h1 class="page">Issues since Monday</h1><p class="lede"><strong class="headline-count">{len(missing)} open issues without your PR.</strong> Of {len(records)} issues posted by enyst or smolpaws since Monday 5 October, {own_total} have an implementation PR by either account and {no_own_total} do not, across all issue states.</p><p class="snapshot">Posted from {stamp(data['window']['start'])} through {stamp(data['window']['end'])}, inclusive.{fetched_note} All times use Stockholm time.</p></header>
<div class="stats"><div><strong>{len(missing)}</strong><span>open · no enyst / smolpaws PR in any state</span></div><div><strong>{len(with_own)}</strong><span>open · an enyst / smolpaws PR exists</span></div><div><strong>{len(closed)}</strong><span>closed · retained in the archive</span></div></div>
<p class="callout"><strong>Inventory for independent maintainer fixes.</strong> PRs marked Close in the <a href="openhands-pr-keep-close.html#close">related review queue</a> are intended to be closed and superseded by new work. Their code will not be reused. This inventory did not begin issue fixes or copy changes from those PRs.</p>
<div class="table-wrap"><table class="summary-table"><caption>Issue counts · an “own PR” is an implementation proposal by enyst or smolpaws in any state</caption><thead><tr><th scope="col">Issue state</th><th scope="col">No own PR</th><th scope="col">Has own PR</th><th scope="col">Total</th></tr></thead><tbody><tr><th scope="row">Still open</th><td>{len(missing)}</td><td>{len(with_own)}</td><td>{open_total}</td></tr><tr><th scope="row">Closed</th><td>{len(closed)-closed_own}</td><td>{closed_own}</td><td>{len(closed)}</td></tr><tr class="total"><th scope="row">All issues</th><td>{no_own_total}</td><td>{own_total}</td><td>{len(records)}</td></tr></tbody></table></div>
<p class="section-intro">{own_open_issues} of the {open_total} open issues currently have an open own-author PR. {closed_only} open issue{'s have' if closed_only != 1 else ' has'} only own-author PRs closed without merge.{closed_only_note} There are {len(distinct_own)} distinct own-author implementation PRs across the cohort; {len(distinct_other_open)} distinct other-author PRs remain open.</p>
<nav class="report-nav inventory-nav" aria-label="Inventory sections"><a href="#without-own" data-show-group="without-own">Open without own PR · {len(missing)}</a><a href="#with-own" data-show-group="with-own">Open with own PR · {len(with_own)}</a><a href="#closed" data-show-group="closed">Closed archive · {len(closed)}</a><a href="#method">Counting and matching</a><a href="openhands-pr-keep-close.html">Related PR review queue →</a></nav>
<form class="filters" id="inventory-filter" role="search" hidden><div class="search-field"><label for="inventory-search">Search issue and PR titles, numbers or authors</label><input type="search" id="inventory-search" placeholder="Issue, PR, title or author"></div><div><label for="inventory-group">Issue group</label><select id="inventory-group">{options}</select></div><div><label for="inventory-author">Issue author</label><select id="inventory-author"><option value="all">Both accounts</option>{authors}</select></div><button type="reset">Clear filters</button></form><p class="result-count" id="inventory-result" role="status" aria-live="polite" hidden></p><noscript><p class="context-note">All issues are shown below. Search and group filtering become available with JavaScript.</p></noscript>
<div id="inventory-list">{''.join(sections)}<p class="empty-filter" id="inventory-empty" hidden>No matching issues. Change the issue group or clear the search.</p></div>
<section class="method" id="method"><h2 class="section-heading">Counting and matching</h2><p>The cohort includes issues in OpenHands/OpenHands posted by enyst or smolpaws, created from Monday 5 October 2026 at 00:00 Europe/Stockholm through the frozen endpoint above. In UTC this is <code>{esc(data['window']['start'])}</code> through <code>{esc(data['window']['end'])}</code>. Monday is inclusive. Only issue creation determines the frozen membership. PR matches and issue/PR states reflect metadata observed during collection, including later updates; openness is not reconstructed at the creation cutoff.{metadata_interval}</p><p>“Has own PR” means at least one actual implementation proposal authored by enyst or smolpaws was matched to the issue. Open PRs, drafts, merged PRs and PRs closed without merge are counted and labeled separately. This is not a completed-fix count. Partial proposals are labeled; a merged partial PR can leave its issue open. The “no active own PR” filter reports current PR state; merged matches can require checking remaining scope or closing the issue rather than writing another fix.</p><p>The collector paginated GitHub’s author-specific issue collections, complete issue timelines and PR records, checked authoritative closure events, and searched PR descriptions for references back to these issues. Because timeline cross-references can be missing, the reverse search includes all own-author PRs in every state and other-author PRs updated since Monday. Exact issue references were checked in context for implementation intent. Incidental mentions, review or QA references, and documentation that merely mentions an issue are excluded from implementation counts; exclusions appear beneath the affected issue.</p><p>“No PR” means none identified through those metadata checks, rather than proof that no unlinked or unreferenced implementation exists. Other-author proposals with no recent update, no issue link and no fixing reference may escape detection. An issue counts once; one PR can address several issues, so PR totals use distinct PR numbers. This inventory inspects metadata and matching intent; it does not verify that a proposed implementation solves the issue.</p><p>Other-author proposals are shown separately for context, with actual PR states and open counts. A Keep or Close label links to the existing review queue; it is not a new code review.{triage_note} No issue fixing, PR reuse, PR closure or review submission was performed for this inventory.</p><p class="downloads-line"><a href="../assets/openhands-monday-issue-inventory/data.json" download>Checked dataset (JSON)</a> · <a href="../assets/openhands-monday-issue-inventory/inventory.csv" download>Issue–PR rows (CSV)</a></p><p class="cohort-note">{len(records)} issues reconcile to {open_total} open + {len(closed)} closed; {own_total} with own PRs + {no_own_total} without. This is a dated snapshot and may change after new PRs, merges or closures. Prepared by Codex, an AI assistant, on enyst’s behalf.</p></section>
<nav class="report-nav" aria-label="Related reports"><a href="openhands-pr-keep-close.html">PRs · Keep / Close</a><a href="openhands-last-week-open-issues.html">Previous weekly open-issue report</a><a href="openhands-last-week-merged-issues.html">Previous weekly merged-issue report</a></nav>'''
    description = f"{len(records)} OpenHands issues filed by enyst or smolpaws since Monday 5 October 2026: {len(missing)} open without their PR, {len(with_own)} open with their PR and {len(closed)} closed."
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>OpenHands issues since Monday — Engel’s Code Design Notebook</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="https://enyst.github.io/investigations/openhands-issues-since-monday.html"><meta property="og:title" content="OpenHands issues since Monday"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="article"><meta name="twitter:card" content="summary"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&amp;family=DM+Sans:wght@400;500;700&amp;family=JetBrains+Mono:wght@400;600&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="../brand.css"><link rel="stylesheet" href="../assets/openhands-issue-pr-report/report.css"><link rel="stylesheet" href="../assets/openhands-maintainer-reports/reports.css"><link rel="stylesheet" href="../assets/openhands-monday-issue-inventory/inventory.css"><script src="../assets/openhands-monday-issue-inventory/inventory.js" defer></script></head><body><a class="skip-link" href="#main">Skip to inventory</a><main class="shell report-shell" id="main"><a class="back" href="../index.html">← Engel’s Code Design Notebook</a>{body}<p class="cohort-note">OpenHands/OpenHands · enyst / smolpaws · checked issue and implementation-PR inventory.</p></main></body></html>
'''
    OUTPUT.write_text(page, encoding="utf-8")
    write_csv(records)
    print(json.dumps({"issues": len(records), "open_without_own": len(missing), "open_with_own": len(with_own), "closed": len(closed), "with_own_any_state": own_total, "without_own_any_state": no_own_total, "output": str(OUTPUT)}))


if __name__ == "__main__":
    main()
