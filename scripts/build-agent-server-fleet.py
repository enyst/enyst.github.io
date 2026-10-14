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
STAMP = datetime.fromisoformat(DATA['observed_at']).strftime('%d October %Y, %H:%M UTC')
SLUGS = {c: c.lower().replace(' and ', '-').replace(' ', '-') for c in CATEGORIES}


def esc(text):
    return escape(str(text), quote=True)


sections = []
for category in CATEGORIES:
    rows = []
    for p in sorted((p for p in PRS if p['category'] == category), key=lambda p: -p['number']):
        search = ' '.join(str(p[k]) for k in ['number', 'category', 'heading', 'summary', 'title']).lower()
        rows.append(f'''<article class="pr" id="pr-{p['number']}" data-category="{esc(category)}" data-search="{esc(search)}">
<a class="pr-number" href="{esc(p['url'])}" aria-label="Read pull request {p['number']} on GitHub">#{p['number']} <span aria-hidden="true">↗</span></a>
<div><h3><a href="{esc(p['url'])}">{esc(p['heading'])}</a></h3><p>{esc(p['summary'])}</p>
<details><summary>Original PR title</summary><p>{esc(p['title'])}</p></details></div></article>''')
    sections.append(f'''<section class="topic" id="{SLUGS[category]}" aria-labelledby="heading-{SLUGS[category]}"><h2 id="heading-{SLUGS[category]}">{esc(category)} <span>{COUNTS[category]}</span></h2>{''.join(rows)}</section>''')
nav = ''.join(f'<a href="#{SLUGS[c]}">{esc(c)} <span>{COUNTS[c]}</span></a>' for c in CATEGORIES)
options = ''.join(f'<option value="{esc(c)}">{esc(c)} ({COUNTS[c]})</option>' for c in CATEGORIES)
page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>The repair queue — OpenHands Agent Server</title>
<meta name="description" content="Short, plain-English summaries of {len(PRS)} proposed OpenHands Agent Server and SDK fixes, with a link to every pull request. Snapshot from 14 October 2026.">
<link rel="canonical" href="https://enyst.github.io/arch/agent-server-fleet.html">
<meta property="og:title" content="The repair queue — OpenHands Agent Server"><meta property="og:description" content="{len(PRS)} proposed fixes. One short summary and source link for each."><meta property="og:type" content="article"><meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&amp;family=DM+Sans:wght@400;500;700&amp;family=JetBrains+Mono:wght@400;600&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="../brand.css"><link rel="stylesheet" href="../assets/agent-server-fleet/report.css"><script src="../assets/agent-server-fleet/report.js" defer></script></head>
<body><a class="skip" href="#main">Skip to summaries</a><main id="main" class="shell fleet-shell">
<a class="back" href="../index.html">← Engel’s Code Design Notebook</a>
<header><p class="eyebrow">OpenHands / verification field notes</p><h1 class="hero">The repair queue.</h1>
<p class="lead">What each fix changes.<br>A short summary. A link to the code.</p>
<div class="snapshot"><strong>{len(PRS)}</strong><div>proposed fixes · open at capture<br><time datetime="{esc(DATA['observed_at'])}">{STAMP}</time></div></div>
<p>The <a href="verify-agent-server.html">verify-agent-server feature map</a> let agents use the real API and record unexpected behavior. This page lists the fleet’s proposed fixes for those findings.</p>
<p class="notice">These PRs are <strong>not merged in this snapshot</strong>. Each summary describes a proposed change, not a released feature. Follow the GitHub link for its current status.</p></header>
<nav class="topics" aria-label="Jump to a topic">{nav}</nav>
<div class="controls" hidden><form id="filters" role="search"><div><label for="query">Find a fix</label><input id="query" type="search" placeholder="PR number, feature or API name"></div><div><label for="category">Topic</label><select id="category"><option value="">All topics ({len(PRS)})</option>{options}</select></div><button type="reset">Clear</button></form><p id="count" role="status" aria-live="polite">Showing {len(PRS)} of {len(PRS)} proposed fixes.</p></div>
<div id="summaries">{''.join(sections)}</div><p id="empty" hidden>No fixes match. Try another word or clear the filters.</p>
<footer><h2>How to read this page</h2><p>I used short sentences, active voice and consistent terms, inspired by ASD-STE100 Simplified Technical English. This page is not certified ASD-STE100. API names keep their exact spelling.</p>
<p>I summarized the public PR descriptions. I did not rerun their tests or independently review every diff. The list includes open PRs authored by enyst whose branch starts with <code>claude/umbrella-bug-fixes-</code>. It excludes other open work.</p>
<p>The morning Slack update counted 108 PRs. This later snapshot contains {len(PRS)}. The count can change as agents open fixes and maintainers merge or close them.</p>
<p class="source-links"><a href="https://github.com/OpenHands/software-agent-sdk/issues/5653">Original findings</a><a href="https://github.com/OpenHands/software-agent-sdk/pulls?q=is%3Apr+is%3Aopen+author%3Aenyst">Current open PRs</a><a href="../assets/agent-server-fleet/snapshot.json">Snapshot data</a><a href="https://github.com/enyst/enyst.github.io/blob/main/scripts/build-agent-server-fleet.py">Page source</a></p>
<p class="endnote">Summaries by SmolPaws 🐾 · {STAMP}</p></footer>
</main></body></html>'''
(ROOT / 'arch/agent-server-fleet.html').write_text(page)
print(f'Rendered {len(PRS)} PRs in {len(CATEGORIES)} topics.')
