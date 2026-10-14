#!/usr/bin/env python3
"""Render a dated fleet PR snapshot. Does not fetch GitHub or run fix branches."""
from collections import Counter
from datetime import datetime
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'assets/agent-server-fleet/snapshot.json').read_text())
PRS = DATA['prs']
COUNTS = Counter(p['category'] for p in PRS)
CATEGORIES = sorted(COUNTS)
STAMP = datetime.fromisoformat(DATA['observed_at']).strftime('%d %B %Y, %H:%M UTC')
SLUGS = {c: c.lower().replace(' and ', '-').replace(' ', '-') for c in CATEGORIES}


def esc(text):
    return escape(str(text), quote=True)


STATUSES = {
    'merged': ('Merged', '<path d="M6 3v10a4 4 0 0 0 4 4h5M11 7l4 4 4-4M15 11V3"/><circle cx="6" cy="3" r="2"/><circle cx="17" cy="17" r="2"/>'),
    'approved': ('Approved', '<path d="m4 12 5 5L20 6"/>'),
    'open': ('Open (not approved)', '<circle cx="6" cy="5" r="2"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="19" r="2"/><path d="M6 7v10M18 17V9a4 4 0 0 0-4-4h-2"/>'),
    'changes-requested': ('Changes requested', '<path d="M4 4h16v12H9l-5 4V4Z"/><path d="M12 7v4m0 2v1"/>'),
    'draft': ('Draft', '<path stroke-dasharray="3 3" d="M6 7v10M18 17V9a4 4 0 0 0-4-4h-2"/><circle cx="6" cy="5" r="2"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="19" r="2"/>'),
    'closed': ('Closed', '<path d="m6 6 12 12M18 6 6 18"/>'),
}


def status_key(pr):
    if pr['state'] == 'MERGED':
        return 'merged'
    if pr['state'] == 'CLOSED':
        return 'closed'
    if pr['is_draft']:
        return 'draft'
    if pr['review_decision'] == 'CHANGES_REQUESTED':
        return 'changes-requested'
    if pr['review_decision'] == 'APPROVED':
        return 'approved'
    return 'open'


def badge(key, count=None):
    label, paths = STATUSES[key]
    suffix = f' <span class="status-count">{count}</span>' if count is not None else ''
    return (f'<span class="status status-{key}"><svg viewBox="0 0 24 24" '
            f'width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'
            f'<span>{label}</span>{suffix}</span>')


STATUS_COUNTS = Counter(status_key(pr) for pr in PRS)
legend = ''.join(badge(key, STATUS_COUNTS[key]) for key in STATUSES)
status_options = ''.join(f'<option value="{key}">{label} ({STATUS_COUNTS[key]})</option>'
                         for key, (label, _) in STATUSES.items())

def render_row(p):
    status = status_key(p)
    decision = p.get('decision_needed', False)
    search = ('decision needed ' if decision else '') + STATUSES[status][0].lower() + ' ' + ' '.join(str(p[k]) for k in ['number', 'category', 'heading', 'summary', 'title']).lower()
    flag = '<p class="decision-flag">◆ Decision needed · PR description</p>' if decision else ''
    return f'''<article class="pr{' pr-decision' if decision else ''}" id="pr-{p['number']}" data-category="{esc(p['category'])}" data-status="{status}" data-search="{esc(search)}">
<a class="pr-number" href="{esc(p['url'])}" target="_blank" rel="noopener noreferrer" aria-label="Read pull request {p['number']} on GitHub (opens in a new tab)">#{p['number']} <span aria-hidden="true">↗</span></a>
<div>{flag}<div class="pr-heading"><h3><a href="{esc(p['url'])}" target="_blank" rel="noopener noreferrer" aria-label="{esc(p['heading'])} (opens in a new tab)">{esc(p['heading'])}</a></h3>{badge(status)}</div><p>{esc(p['summary'])}</p>
<details><summary>Original PR title</summary><p>{esc(p['title'])}</p></details></div></article>'''


decisions = sorted((p for p in PRS if p.get('decision_needed')), key=lambda p: (p['state'] != 'OPEN', -p['number']))
open_decisions = sum(p['state'] == 'OPEN' for p in decisions)
sections = []
if decisions:
    sections.append(f'''<section class="topic decision-topic" id="decisions" aria-labelledby="heading-decisions"><h2 id="heading-decisions">Decision needed <span>{len(decisions)}</span></h2>
<p class="decision-note">These PR descriptions contain a “Decision needed” section. Open PRs come first: {open_decisions} open, {len(decisions) - open_decisions} merged or closed. The label records the section’s presence; it does not mean a decision is still unresolved after merge.</p>
{''.join(render_row(p) for p in decisions)}</section>''')
nav = f'<a class="decision-jump" href="#decisions">◆ Decision needed <span>{len(decisions)}</span></a>' if decisions else ''
for category in CATEGORIES:
    remaining = sorted((p for p in PRS if p['category'] == category and not p.get('decision_needed')), key=lambda p: -p['number'])
    if not remaining:
        continue
    sections.append(f'''<section class="topic" id="{SLUGS[category]}" aria-labelledby="heading-{SLUGS[category]}"><h2 id="heading-{SLUGS[category]}">{esc(category)} <span>{len(remaining)}</span></h2>{''.join(render_row(p) for p in remaining)}</section>''')
    nav += f'<a href="#{SLUGS[category]}">{esc(category)} <span>{len(remaining)}</span></a>'
options = ''.join(f'<option value="{esc(c)}">{esc(c)} ({COUNTS[c]})</option>' for c in CATEGORIES)
page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>The repair queue — OpenHands Agent Server</title>
<meta name="description" content="Short, plain-English summaries of {len(PRS)} proposed OpenHands Agent Server and SDK fixes, with a link to every pull request. Snapshot from {STAMP}.">
<link rel="canonical" href="https://enyst.github.io/arch/agent-server-fleet.html">
<meta property="og:title" content="The repair queue — OpenHands Agent Server"><meta property="og:description" content="{len(PRS)} proposed fixes. One short summary and source link for each."><meta property="og:type" content="article"><meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&amp;family=DM+Sans:wght@400;500;700&amp;family=JetBrains+Mono:wght@400;600&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="../brand.css"><link rel="stylesheet" href="../assets/agent-server-fleet/report.css"><script src="../assets/agent-server-fleet/report.js" defer></script></head>
<body><a class="skip" href="#main">Skip to summaries</a><main id="main" class="shell fleet-shell">
<a class="back" href="../index.html">← Engel’s Code Design Notebook</a>
<header><p class="eyebrow">OpenHands / verification field notes</p><h1 class="hero">The repair queue.</h1>
<p class="lead">What each fix changes.<br>A short summary. A link to the code.</p>
<div class="snapshot"><strong>{len(PRS)}</strong><div>fix PRs · {STATUS_COUNTS["open"] + STATUS_COUNTS["approved"] + STATUS_COUNTS["changes-requested"] + STATUS_COUNTS["draft"]} open · {STATUS_COUNTS["merged"]} merged · {STATUS_COUNTS["closed"]} closed<br><time datetime="{esc(DATA['observed_at'])}">{STAMP}</time></div></div>
<p>The <a href="verify-agent-server.html">verify-agent-server feature map</a> let agents use the real API and record unexpected behavior. This page tracks the fleet’s fixes for those findings, including merged and closed PRs.</p>
<p class="notice">Status checked at the time above. <strong>Approved does not mean merged.</strong> Approval reflects GitHub’s review decision and may come from a bot. Merged changes may not be released yet. PRs with a “Decision needed” section appear first. PR links open in a new tab.</p></header>
<div class="status-legend" aria-label="PR status counts">{legend}</div>
<nav class="topics" aria-label="Jump to a topic">{nav}</nav>
<div class="controls" hidden><form id="filters" role="search"><div><label for="query">Find a fix</label><input id="query" type="search" placeholder="PR number, feature or API name"></div><div><label for="category">Topic</label><select id="category"><option value="">All topics ({len(PRS)})</option>{options}</select></div><div><label for="status">Status</label><select id="status"><option value="">All statuses ({len(PRS)})</option>{status_options}</select></div><button type="reset">Clear</button></form><p id="count" role="status" aria-live="polite">Showing {len(PRS)} of {len(PRS)} fix PRs.</p></div>
<div id="summaries">{''.join(sections)}</div><p id="empty" hidden>No fixes match. Try another word or clear the filters.</p>
<footer><h2>How to read this page</h2><p>I used short sentences, active voice and consistent terms, inspired by ASD-STE100 Simplified Technical English. This page is not certified ASD-STE100. API names keep their exact spelling.</p>
<p>I summarized the public PR descriptions. I did not rerun their tests or independently review every diff. The list includes PRs authored by enyst whose branch starts with <code>claude/umbrella-bug-fixes-</code>. It keeps merged and closed PRs and excludes other work.</p>
<p>Icons identify merged, approved, open without approval, changes requested, draft and closed PRs. Merged and closed states take priority over reviews. Draft takes priority for an open draft PR.</p>
<p class="source-links"><a href="https://github.com/OpenHands/software-agent-sdk/issues/5653">Original findings</a><a href="https://github.com/OpenHands/software-agent-sdk/pulls?q=is%3Apr+is%3Aopen+author%3Aenyst">Current open PRs</a><a href="../assets/agent-server-fleet/snapshot.json">Snapshot data</a><a href="https://github.com/enyst/enyst.github.io/blob/main/scripts/build-agent-server-fleet.py">Page source</a><a href="https://github.com/enyst/enyst.github.io/blob/main/scripts/refresh-agent-server-fleet.py">Refresh script</a></p>
<p class="endnote">Summaries by SmolPaws 🐾 · {STAMP}</p></footer>
</main></body></html>'''
(ROOT / 'arch/agent-server-fleet.html').write_text(page)
print(f'Rendered {len(PRS)} PRs in {len(CATEGORIES)} topics.')
