#!/usr/bin/env python3
"""Render the issue/PR survey and CSV downloads from its checked JSON dataset.

Run after refreshing assets/openhands-issue-pr-report/data.json. This renderer
does not query GitHub or imply that original browser evidence was rerun.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import csv
import html
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets/openhands-issue-pr-report'
data = json.loads((ASSETS / 'data.json').read_text())
issues = sorted(data['openIssues']['issues'], key=lambda row: -row['number'])
matches = data['otherAuthorPRs']['matches']
week = data['weeklyClosures']
closures = sorted(week['rows'], key=lambda row: row['closed_at'], reverse=True)
by_issue = defaultdict(list)
for row in matches:
    by_issue[row['issue']].append(row)
esc = lambda value: html.escape(str(value), quote=True)

def stamp(value, full=False):
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(timezone.utc)
    label = f'{dt.day} {dt.strftime("%B %Y, %H:%M:%S UTC")}' if full else f'{dt.day} {dt.strftime("%b · %H:%M UTC")}'
    return f'<time datetime="{esc(value)}">{label}</time>'

def author(login):
    return f'<a href="https://github.com/{esc(login)}">{esc(login)}</a>'

def pr_status(value):
    label = value or 'Unknown'
    kind = {'Open':'open', 'Draft':'draft', 'Merged':'merged', 'Closed unmerged':'unmerged', 'Closed, unmerged':'unmerged', 'Closed without merging':'unmerged', 'Closed':'unmerged'}.get(label, 'unmerged')
    if label in ('Closed', 'Closed, unmerged'):
        label = 'Closed unmerged'
    return f'<span class="status {kind}">{esc(label)}</span>'

def closure_group(row):
    if not row.get('pr'):
        return 'unmatched'
    if row['outcome'] != 'solving PR':
        return 'partial'
    return 'own' if row['author_group'] == 'enyst/smolpaws' else 'other'

def closure_card(row):
    group = closure_group(row)
    search = ' '.join(str(row.get(k, '')) for k in ['issue', 'issue_title', 'issue_author', 'pr', 'pr_title', 'pr_author']).lower()
    pr = '<p class="no-match">No matched merged implementation PR identified.</p>'
    if row.get('pr'):
        pr = f'<div class="pr-top"><a class="number" href="{esc(row["pr_url"])}">PR #{row["pr"]}</a><span class="byline">by {author(row["pr_author"])}</span></div><a class="pr-title" href="{esc(row["pr_url"])}">{esc(row["pr_title"])}</a><p class="byline">Merged {stamp(row["merged_at"])}</p>'
        if group == 'partial':
            pr += f'<p class="scope-note">Partial tracker match; excluded from the solved count. {esc(row["evidence"])}</p>'
    return f'<article class="closure-row filter-row" id="closed-issue-{row["issue"]}" data-group="{group}" data-search="{esc(search)}"><div class="closure-issue"><div class="issue-heading"><a class="number" href="{esc(row["issue_url"])}">Issue #{row["issue"]}</a><span class="status merged">Closed</span></div><h3><a href="{esc(row["issue_url"])}">{esc(row["issue_title"])}</a></h3><p class="byline">Filed by {author(row["issue_author"])} · Closed {stamp(row["closed_at"])}</p></div><div class="closure-pr">{pr}</div></article>'

def issue_card(row):
    prs = by_issue[row['number']]
    coverage = 'active' if any(p['status'] in ('Open', 'Draft') for p in prs) else 'historical' if prs else 'none'
    search = ' '.join([str(row['number']), row['title'], row['author']] + [f'{p["pr"]} {p["title"]} {p["author"]} {p["status"]} {p.get("scope", "")}' for p in prs]).lower()
    parts = []
    for p in sorted(prs, key=lambda p: -p['pr']):
        scope = p.get('scope', '')
        note = f'<p class="scope-note">{esc(scope)}</p>' if scope and scope != 'Addresses issue' else ''
        parts.append(f'<li class="pr-row"><div class="pr-top"><a class="number" href="{esc(p["url"])}">PR #{p["pr"]}</a>{pr_status(p["status"])}<span class="byline">by {author(p["author"])}</span></div><a class="pr-title" href="{esc(p["url"])}">{esc(p["title"])}</a>{note}</li>')
    linked = '<ul class="pr-list">' + ''.join(parts) + '</ul>' if parts else '<p class="no-match">No corresponding implementation PR by another author was identified.</p>'
    incidental = row.get('incidental_prs', row.get('incidental_prs_by_enyst_or_smolpaws', []))
    if isinstance(incidental, str):
        incidental = incidental.split()
    extra = ''
    if incidental:
        refs = ' · '.join(f'<a href="{esc(u)}">PR #{esc(str(u).rstrip("/").split("/")[-1])}</a>' for u in incidental)
        extra = f'<details class="reference-note"><summary>Incidental references by enyst/smolpaws</summary><p>{refs}</p><p>These were classified as documentation, QA, bug-filing or unrelated references rather than implementations.</p></details>'
    return f'<article class="issue-card filter-row" id="open-issue-{row["number"]}" data-author="{esc(row["author"])}" data-coverage="{coverage}" data-search="{esc(search)}"><div class="issue-heading"><a class="number" href="{esc(row["url"])}">Issue #{row["number"]}</a><span class="status open">Open at snapshot</span></div><h3><a href="{esc(row["url"])}">{esc(row["title"])}</a></h3><p class="byline">Filed by {author(row["author"])}</p><div class="issue-prs"><h4>Other-author PRs</h4>{linked}</div>{extra}</article>'

assert len(issues) == len({r['number'] for r in issues})
assert len(closures) == len({r['issue'] for r in closures}) == week['closedIssueCount']
assert all(r['state'] == 'open' for r in issues)
assert all(r['issue'] in {i['number'] for i in issues} for r in matches)
assert len(matches) == len({(p['issue'], p['pr']) for p in matches})
issue_counts = Counter(row['author'] for row in issues)
status_counts = Counter(p['status'] for p in matches)
covered = len(by_issue)
active = sum(any(p['status'] in ('Open', 'Draft') for p in prs) for prs in by_issue.values())
groups = {name: [r for r in closures if closure_group(r) == name] for name in ['own','other','partial','unmatched']}
own_authors = Counter(r['pr_author'] for r in groups['own'])
matched_count = sum(bool(row.get('pr')) for row in closures)
solved_count = len(groups['own']) + len(groups['other'])
assert len(groups['own']) == week['counts']['solved']['enyst/smolpaws']
assert len(groups['other']) == week['counts']['solved']['other author']

def write_csv(name, fields, rows):
    with (ASSETS / name).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, '') for key in fields})

write_csv('open-issues.csv', ['issue','author','state','title','url','reference_status','incidental_prs_by_enyst_or_smolpaws','checked_at'], [{**r, 'issue':r['number'], 'reference_status':r.get('reference_status','No corresponding implementation PR identified'), 'incidental_prs_by_enyst_or_smolpaws':' '.join(r.get('incidental_prs', [])), 'checked_at':data['snapshot']} for r in issues])
issue_by_number = {r['number']:r for r in issues}
write_csv('other-author-prs.csv', ['issue','issue_author','issue_title','issue_url','pr','pr_author','pr_title','pr_url','pr_status','scope','checked_at'], [{
    'issue':r['issue'], 'issue_author':issue_by_number[r['issue']]['author'],
    'issue_title':issue_by_number[r['issue']]['title'], 'issue_url':issue_by_number[r['issue']]['url'],
    'pr':r['pr'], 'pr_author':r['author'], 'pr_title':r['title'], 'pr_url':r['url'],
    'pr_status':r['status'], 'scope':r.get('scope',''), 'checked_at':data['snapshot'],
} for r in matches])
write_csv('weekly-closures.csv', ['issue','issue_title','issue_author','issue_url','closed_at','pr','pr_title','pr_author','pr_url','merged_at','author_group','outcome','evidence'], closures)

description = f'Issues filed by enyst and smolpaws: {len(issues)} open issues without an identified implementation PR by either account, PRs by other contributors, and {len(closures)} closures in the last seven days.'
page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>OpenHands issues &amp; their PRs — Engel's Code Design Notebook</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="https://enyst.github.io/investigations/openhands-issue-pr-report.html">
<meta property="og:title" content="OpenHands issues &amp; their PRs"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="article"><meta property="og:url" content="https://enyst.github.io/investigations/openhands-issue-pr-report.html"><meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&amp;family=DM+Sans:wght@400;500;700&amp;family=JetBrains+Mono:wght@400;600&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="../brand.css"><link rel="stylesheet" href="../assets/openhands-issue-pr-report/report.css"><script src="../assets/openhands-issue-pr-report/report.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to report</a><main class="shell report-shell" id="main"><a class="back" href="../index.html">← Engel's Code Design Notebook</a>
<header class="report-header"><p class="eyebrow">OpenHands / OpenHands · Issue &amp; PR survey</p><h1 class="page">OpenHands issues<br>&amp; their PRs</h1><p class="lede">Issues filed by {author('enyst')} and {author('smolpaws')}: which have work from other contributors, which have no identified implementation PR, and who resolved the issues closed in the last seven days.</p><p class="snapshot">Report snapshot {stamp(data['snapshot'], True)}. GitHub issue and PR metadata refreshed {stamp(data.get('observed_at', data['snapshot']), True)}. These are checked snapshots, not live updates.</p></header>
<nav class="report-nav" aria-label="Report sections"><a href="#last-week">Last seven days</a><a href="#other-closures">Fixes by other authors</a><a href="#open-issues">{len(issues)} open issues</a><a href="#method">Method &amp; downloads</a></nav>
<section id="last-week" aria-labelledby="week-heading"><h2 id="week-heading">Issues closed in the last seven days</h2><p class="section-intro"><strong>{len(closures)} issues closed</strong> between {stamp(week['window']['start'], True)} and {stamp(week['window']['end'], True)}. All were filed by enyst or smolpaws; {matched_count} have a matched merged PR.</p>
<div class="table-wrap"><table class="summary-table"><caption>Issue closures grouped by the author of the matched PR</caption><thead><tr><th scope="col">PR authors</th><th scope="col">Matched closures</th><th scope="col">Solved by PR</th></tr></thead><tbody><tr><th scope="row">enyst / smolpaws</th><td>{week['counts']['matched']['enyst/smolpaws']}</td><td><strong>{len(groups['own'])}</strong></td></tr><tr><th scope="row">Other authors</th><td>{week['counts']['matched']['other author']}</td><td><strong>{len(groups['other'])}</strong></td></tr><tr class="total"><th scope="row">Total</th><td>{matched_count}</td><td><strong>{solved_count}</strong></td></tr></tbody></table></div>
<p class="callout">Counts refer to issues closed and the authors of their matched PRs. Partial tracker closures are shown separately and excluded from “solved”. A merged partial fix can leave another issue open.</p>
<form class="filters" id="week-filters" role="search" hidden><div class="search-field"><label for="week-search">Search closed issues and PRs</label><input id="week-search" type="search" placeholder="Issue, PR, title or author"></div><div><label for="week-group">PR authors / outcome</label><select id="week-group"><option value="all">All {len(closures)} closures</option><option value="other">Solved by other authors · {len(groups['other'])}</option><option value="own">Solved by enyst / smolpaws · {len(groups['own'])}</option><option value="partial">Partial tracker matches · {len(groups['partial'])}</option><option value="unmatched">Unmatched closures · {len(groups['unmatched'])}</option></select></div><button type="reset">Clear filters</button></form><p class="result-count" id="week-result" role="status" aria-live="polite" hidden></p>
<div class="week-group" id="other-closures"><h3 class="group-title">{len(groups['other'])} solved by other authors</h3>{''.join(closure_card(r) for r in groups['other'])}</div>
<details class="week-group own-closures" id="own-closures"><summary>{len(groups['own'])} solving matches by enyst and smolpaws</summary><p class="group-note">{own_authors['enyst']} by enyst and {own_authors['smolpaws']} by smolpaws. Expand to read every issue and PR.</p>{''.join(closure_card(r) for r in groups['own'])}</details>
'''
for name, title in [('partial','Partial tracker matches'),('unmatched','Closures without a matched merged PR')]:
    if groups[name]:
        page += f'<div class="week-group" id="{name}-closures"><h3 class="group-title">{title}</h3>{"".join(closure_card(r) for r in groups[name])}</div>'
page += f'''</section>
<section id="open-issues" aria-labelledby="open-heading"><h2 id="open-heading">Open issues without an identified implementation PR by enyst or smolpaws</h2><p class="section-intro"><strong>{len(issues)} issues</strong> were open at the snapshot: <strong>{issue_counts['enyst']} filed by enyst</strong> and <strong>{issue_counts['smolpaws']} by smolpaws</strong>. Corresponding implementation PRs by either account were not identified. Documentation, QA and incidental references were reviewed separately.</p><div class="stats"><div><strong>{covered}</strong><span>issues with other-author PRs</span></div><div><strong>{len(matches)}</strong><span>other-author issue–PR matches</span></div><div><strong>{len(issues)-covered}</strong><span>issues with no other-author PR found</span></div></div><p class="section-intro">Matched proposals include <strong>{status_counts['Open']} open</strong>, <strong>{status_counts['Draft']} draft</strong>, <strong>{status_counts['Closed unmerged']+status_counts['Closed, unmerged']+status_counts['Closed']} closed without merging</strong>, and <strong>{status_counts['Merged']} merged</strong>. A historical or partial merged fix can belong to an issue that remains open.</p>
<form class="filters" id="open-filters" role="search" hidden><div class="search-field"><label for="open-search">Search issues, PRs and contributors</label><input id="open-search" type="search" placeholder="Issue, PR, title or author"></div><div><label for="open-author">Issue author</label><select id="open-author"><option value="all">Both authors</option><option value="enyst">enyst · {issue_counts['enyst']}</option><option value="smolpaws">smolpaws · {issue_counts['smolpaws']}</option></select></div><div><label for="open-coverage">Other-author work</label><select id="open-coverage"><option value="all">All {len(issues)} issues</option><option value="matched">Any matched PR · {covered}</option><option value="active">Open or draft PR · {active}</option><option value="historical">Only closed / historical · {covered-active}</option><option value="none">No PR identified · {len(issues)-covered}</option></select></div><button type="reset">Clear filters</button></form><p class="result-count" id="open-result" role="status" aria-live="polite" hidden></p><div class="issue-list">{''.join(issue_card(r) for r in issues)}</div></section>
<section class="method" id="method" aria-labelledby="method-heading"><h2 id="method-heading">Method &amp; downloads</h2><p>{esc(data['openIssues']['method'])}</p><p>{esc(data['openIssues']['criterion'])}</p><p>{esc(data['openIssues']['limitations'])}</p><p>GitHub issue and PR metadata were refreshed for this snapshot. A matching reference is checked in context; a merge or issue closure is not a fresh browser verification. Weekly closure totals count issues, not distinct PRs or the account that clicked Merge.</p><ul class="downloads"><li><a href="../assets/openhands-issue-pr-report/open-issues.csv">Open-issue CSV</a></li><li><a href="../assets/openhands-issue-pr-report/other-author-prs.csv">Other-author issue–PR CSV</a></li><li><a href="../assets/openhands-issue-pr-report/weekly-closures.csv">Weekly closures CSV</a></li><li><a href="../assets/openhands-issue-pr-report/data.json">Complete checked dataset</a></li></ul><p>See also <a href="../arch/verify-openhands-issues.html">the verification findings and their fixes</a>.</p></section></main></body></html>'''
(ROOT / 'investigations/openhands-issue-pr-report.html').write_text(page)
print(json.dumps({'open_issues':len(issues), 'other_author_matches':len(matches), 'closed_last_seven_days':len(closures), 'solved_own':len(groups['own']), 'solved_other':len(groups['other']), 'partial':len(groups['partial'])}))
