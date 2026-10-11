#!/usr/bin/env python3
"""Render three separate maintainer reports from checked GitHub snapshots.

Input: assets/openhands-maintainer-reports/{created-week,triage}.json
This renderer does not fetch GitHub or rerun any OpenHands fix branch.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import csv
import html
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets/openhands-maintainer-reports'
OUT = ROOT / 'investigations'
cohort = json.loads((ASSETS / 'created-week.json').read_text())
triage = json.loads((ASSETS / 'triage.json').read_text())
triage['observed_at'] = triage.get('observed_at') or triage['metadata_observed_until']
esc = lambda v: html.escape(str(v), quote=True)


def stamp(value):
    date = datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)
    return f'<time datetime="{esc(value)}">{date.day} {date.strftime("%B %Y, %H:%M:%S UTC")}</time>'


def author(login):
    return f'<a href="https://github.com/{esc(login)}">{esc(login)}</a>'


def prs_list(prs, merged=False):
    parts = []
    for pr in sorted(prs, key=lambda r: -r['number']):
        status = 'Merged' if merged else 'Draft · open' if pr.get('draft') else 'Open'
        color = 'merged' if merged else 'draft' if pr.get('draft') else 'open'
        date = f'<p class="byline">Merged {stamp(pr["merged_at"])}</p>' if merged else ''
        note = f'<p class="scope-note">{esc(pr["scope"])}</p>' if pr.get('scope') else ''
        raw_evidence = pr.get('evidence')
        evidence_text = 'GitHub identifies this merged PR as the issue’s closer.' if merged else ''
        if isinstance(raw_evidence, str):
            evidence_text = raw_evidence
        evidence = f'<p class="audit-note">{esc(evidence_text)}</p>' if evidence_text else ''
        parts.append(f'''<li class="pr-row"><div class="pr-top"><a class="number" href="{esc(pr['url'])}">PR #{pr['number']}</a><span class="status {color}">{status}</span><span class="byline">by {author(pr['author'])}</span></div><a class="pr-title" href="{esc(pr['url'])}">{esc(pr['title'])}</a>{date}{note}{evidence}</li>''')
    return '<ul class="pr-list">' + '\n'.join(parts) + '</ul>'


PATHS = {
    'closed': 'openhands-last-week-merged-issues.html',
    'open': 'openhands-last-week-open-issues.html',
    'triage': 'openhands-pr-keep-close.html',
}


def base(kind, title, description, body):
    links = []
    for k, label in [('closed', 'Posted last week · closed by merged PRs'), ('open', 'Posted last week · still open'), ('triage', 'PRs · Keep / Close')]:
        if k != kind:
            links.append(f'<a href="{PATHS[k]}">{label}</a>')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Engel's Code Design Notebook</title>
<meta name="description" content="{esc(description)}"><link rel="canonical" href="https://enyst.github.io/investigations/{PATHS[kind]}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="article"><meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&amp;family=DM+Sans:wght@400;500;700&amp;family=JetBrains+Mono:wght@400;600&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="../brand.css"><link rel="stylesheet" href="../assets/openhands-issue-pr-report/report.css"><link rel="stylesheet" href="../assets/openhands-maintainer-reports/reports.css"><script src="../assets/openhands-maintainer-reports/reports.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to report</a><main class="shell report-shell" id="main"><a class="back" href="../index.html">← Engel's Code Design Notebook</a>
{body}
<nav class="report-nav" aria-label="Related maintainer reports">{''.join(links)}</nav>
<p class="cohort-note">OpenHands/OpenHands · checked report snapshots.</p></main></body></html>
'''


def filters(target, noun, choices=None):
    select = ''
    if choices:
        select = f'<div><label for="{target}-group">Show</label><select id="{target}-group">' + ''.join(f'<option value="{esc(value)}">{esc(label)}</option>' for value, label in choices) + '</select></div>'
    return f'''<form class="filters" data-report-filter="{target}" data-result="{target}-result" data-noun="{noun}" role="search" hidden><div class="search-field"><label for="{target}-search">Search {noun}, titles and authors</label><input id="{target}-search" type="search" placeholder="Issue, PR, title or author"></div>{select}<button type="reset">Clear filters</button></form><p class="result-count" id="{target}-result" role="status" aria-live="polite" hidden></p>'''


def issue_card(issue, merged=False):
    prs = issue['merged_prs'] if merged else issue['open_prs']
    search = ' '.join([str(issue['number']), issue['title'], issue['author']] + [f'{p["number"]} {p["title"]} {p["author"]}' for p in prs]).lower()
    group = ('own' if all(p['author'] in ('enyst', 'smolpaws') for p in prs) else 'other') if merged else 'with-pr' if prs else 'no-pr'
    label = 'Closed by merged PR' if merged else 'Still open'
    color = 'merged' if merged else 'open'
    closed_date = f' · Closed {stamp(issue["closed_at"])}' if merged else ''
    pr_heading = 'Merged closing PR' + ('s' if len(prs) != 1 else '') if merged else f'{len(prs)} open PR' + ('s' if len(prs) != 1 else '')
    pr_content = prs_list(prs, merged) if prs else '<p class="no-match">No open implementation PR identified.</p>'
    note = f'<p class="audit-note">{esc(issue["note"])}</p>' if issue.get('note') else ''
    return f'''<article class="issue-card" id="issue-{issue['number']}" data-search="{esc(search)}" data-group="{group}"><div class="issue-heading"><a class="number" href="{esc(issue['url'])}">Issue #{issue['number']}</a><span class="status {color}">{label}</span></div><h3><a href="{esc(issue['url'])}">{esc(issue['title'])}</a></h3><p class="byline">Posted by {author(issue['author'])} · Created {stamp(issue['created_at'])}{closed_date}</p><div class="issue-prs"><h4>{pr_heading}</h4>{pr_content}{note}</div></article>'''


records = cohort['records']
assert len(records) == len({r['number'] for r in records})
assert all(r['author'] in ('enyst', 'smolpaws') for r in records)
assert all(cohort['window']['start'] <= r['created_at'] < cohort['window']['end'] for r in records)
closed = sorted([r for r in records if r['classification'] == 'closed_merged_pr'], key=lambda r: -r['number'])
opened = sorted([r for r in records if r['classification'] == 'open'], key=lambda r: -r['number'])
other = sorted([r for r in records if r['classification'] == 'closed_other'], key=lambda r: -r['number'])
assert len(closed) + len(opened) + len(other) == len(records)
assert all(r['state'] == 'closed' and r['merged_prs'] for r in closed)
assert all(r['state'] == 'open' for r in opened)
assert all(p['state'] == 'open' for r in opened for p in r['open_prs'])
own = sum(all(p['author'] in ('enyst', 'smolpaws') for p in r['merged_prs']) for r in closed)
external = len(closed) - own
active = sum(bool(r['open_prs']) for r in opened)
pr_matches = sum(len(r['open_prs']) for r in opened)
unique_open_prs = len({p['number'] for r in opened for p in r['open_prs']})
window = f"{stamp(cohort['window']['start'])} to {stamp(cohort['window']['end'])}"
observed = stamp(cohort['observed_at'])
reconciliation = f'{len(records)} issues posted: {len(closed)} closed by merged PRs + {len(opened)} still open' + (f' + {len(other)} other closures.' if other else '.')
downloads = '<p><a href="../assets/openhands-maintainer-reports/created-week.json">Checked issue/PR dataset (JSON)</a> · <a href="../assets/openhands-maintainer-reports/created-week.csv">Issue/PR list (CSV)</a></p>'
issue_method = f'''<section class="method" id="method"><h2 class="section-heading">Counting rules</h2><p>The cohort is issues in OpenHands/OpenHands authored by enyst or smolpaws and created from {window}; the end is exclusive. Issue creation determines membership. Status and PR metadata were checked through {observed}.</p><p>An issue counts as closed by a merged PR when it is closed and GitHub’s closure event names a merged PR as the closer. This counts issue closures. A tracker closed by a partial PR is included and clearly labeled; closure alone does not establish that every requirement was fixed.</p><p>For open issues, implementation PRs are matched using paginated issue timelines, linked PRs and explicit fixing references checked in context. Incidental mentions and QA-only references are excluded. Every issue counts once. Open PR counts include drafts and all authors; the same PR can address more than one issue.</p><p>{reconciliation}</p>{downloads}</section>'''

other_section = ''
if other:
    entries = []
    for issue in other:
        detail = esc(issue.get('note') or 'No full merged fixing PR established.')
        references = prs_list(issue.get('merged_prs', []), True) if issue.get('merged_prs') else ''
        entries.append(f'<li><a href="{esc(issue["url"])}">#{issue["number"]} — {esc(issue["title"])}</a><span class="byline">Posted by {author(issue["author"])} · {detail}</span>{references}</li>')
    other_section = f'<section><h2 class="section-heading">{len(other)} other closure' + ('s' if len(other) != 1 else '') + f'</h2><p>Shown to reconcile the cohort; excluded from the completed-fix count.</p><ul class="archive-list">{"".join(entries)}</ul></section>'

partials = [r for r in closed if r.get('fix_scope') == 'partial']
partial_note = ''
if partials:
    partial_links = ', '.join(f'<a href="#issue-{r["number"]}">#{r["number"]}</a>' for r in partials)
    partial_note = f'<p class="callout">The {len(closed)} closures include {len(partials)} partial tracker closure: {partial_links}. It is included because a merged PR directly closed it; its remaining scope is stated in the row.</p>'
body = f'''<header class="report-header"><p class="eyebrow">OpenHands / OpenHands · Issues posted in the last seven days</p><h1 class="page">Closed by merged PRs</h1><p class="lede"><strong class="headline-count">{len(closed)} issues</strong> posted by enyst or smolpaws during the week are now closed by a merged PR. Each issue below names the closing PR’s author.</p><p class="snapshot">Posted {window}. Status checked through {observed}.</p></header>
<div class="stats two"><div><strong>{own}</strong><span>issues closed by enyst / smolpaws PRs</span></div><div><strong>{external}</strong><span>issues closed by other authors’ PRs</span></div></div>{partial_note}
{filters('closed-list','issues',[('all',f'All {len(closed)} issues'),('own',f'PRs by enyst / smolpaws · {own}'),('other',f'PRs involving other authors · {external}')])}<section id="closed-list" aria-label="Issues closed by merged PRs" class="issue-list">{'\n'.join(issue_card(i,True) for i in closed)}<p class="empty-filter" hidden>No matching issues.</p></section>{other_section}{issue_method}'''
(OUT / PATHS['closed']).write_text(base('closed', 'OpenHands · last week’s issues closed by merged PRs', f'{len(closed)} issues posted by enyst/smolpaws in the last seven days are closed by merged PRs, with every PR author.', body))

body = f'''<header class="report-header"><p class="eyebrow">OpenHands / OpenHands · Issues posted in the last seven days</p><h1 class="page">Still open</h1><p class="lede"><strong class="headline-count">{len(opened)} issues</strong> posted by enyst or smolpaws during the week remain open. Every issue below gives its open PR count, with links and authors.</p><p class="snapshot">Posted {window}. Status checked through {observed}.</p></header>
<div class="stats"><div><strong>{active}</strong><span>issues with an open PR</span></div><div><strong>{len(opened)-active}</strong><span>issues without an open PR</span></div><div><strong>{unique_open_prs}</strong><span>distinct open PRs · drafts included</span></div></div>
<p class="section-intro">All PR authors are included. There are {pr_matches} issue–PR links across {unique_open_prs} distinct open PRs. Counts refer to proposed implementation work; an open PR does not establish that the issue is fully solved.</p>
{filters('open-list','issues',[('all',f'All {len(opened)} issues'),('with-pr',f'With an open PR · {active}'),('no-pr',f'No open PR · {len(opened)-active}')])}<section id="open-list" aria-label="Still-open issues and their PR counts" class="issue-list">{'\n'.join(issue_card(i) for i in opened)}<p class="empty-filter" hidden>No matching issues.</p></section>{issue_method}'''
(OUT / PATHS['open']).write_text(base('open', 'OpenHands · last week’s issues still open', f'{len(opened)} issues posted by enyst/smolpaws in the last seven days remain open; open PR counts and authors for each.', body))


def triage_card(row):
    keep = row['decision'] == 'keep'
    decision = 'Keep' if keep else 'Close without merge'
    label = 'Why keep' if keep else 'Closure reason'
    color = 'keep' if keep else 'close'
    title = row['pr_title']
    search = f'{row["pr"]} {title} {row["pr_author"]} {row["issue"]} {row["reason"]}'.lower()
    state = 'Draft · open' if row.get('draft') else 'Open'
    issue_state = row.get('issue_state', 'unknown').capitalize()
    evidence = ''.join(f'<li><a href="{esc(url)}">{esc(url)}</a></li>' for url in dict.fromkeys(row.get('evidence_urls', [])))
    caveats = ''.join(f'<li>{esc(c)}</li>' for c in row.get('audit_caveats', row.get('original_audit_remaining_checks', [])))
    note = f'<p class="audit-note">{esc(row["refresh_note"])}</p>' if row.get('refresh_note') else ''
    head_note = 'The current head matches the earlier code audit.' if row['head_matches_original_audit'] else 'The head has changed since the earlier code audit; see the refreshed assessment.'
    return f'''<article class="issue-card" id="pr-{row['pr']}" data-group="{row['decision']}" data-search="{esc(search)}"><div class="pr-top"><a class="number" href="{esc(row['pr_url'])}">PR #{row['pr']}</a><span class="status {color}">{decision}</span><span class="status {'draft' if row.get('draft') else 'open'}">{state}</span><span class="byline">by {author(row['pr_author'])}</span></div><h3><a href="{esc(row['pr_url'])}">{esc(title)}</a></h3><p class="byline"><a href="{esc(row['issue_url'])}">Issue #{row['issue']}</a> · {issue_state}</p><p class="reason"><strong class="reason-label">{label}</strong>{esc(row['reason'])}</p>{note}<details class="evidence"><summary>Evidence and review limits</summary><ul>{evidence}</ul><p>Reviewed code head: <code>{esc(row['head_sha'])}</code>. {head_note}</p>{'<ul>' + caveats + '</ul>' if caveats else ''}</details></article>'''


all_triage = triage['records']
keep = [r for r in all_triage if r['state'] == 'open' and r['decision'] == 'keep']
close = [r for r in all_triage if r['state'] == 'open' and r['decision'] == 'close']
archived = [r for r in all_triage if r['state'] != 'open']
assert len(all_triage) == len({r['pr'] for r in all_triage})
assert len(keep) + len(close) + len(archived) == len(all_triage)
close_groups = {g: [r for r in close if r['group'] == g] for g in ['closure-defect-or-duplicate','closure-unready']}
assert sum(map(len,close_groups.values())) == len(close)
archive = []
for row in sorted(archived, key=lambda r: -r['pr']):
    status = 'Merged' if row.get('merged_at') else 'Already closed without merge'
    archive.append(f'<li><a href="{esc(row["pr_url"])}">PR #{row["pr"]} — {esc(row["pr_title"])}</a><span class="byline">{status} · by {author(row["pr_author"])}</span></li>')
close_html = ''
for group, heading in [('closure-defect-or-duplicate','Defect or redundant fix'),('closure-unready','Incomplete work or evidence')]:
    rows = close_groups[group]
    close_html += f'<section data-filter-subgroup><h3 class="subgroup-heading">{heading} · {len(rows)} PRs</h3><div class="issue-list">{"".join(triage_card(r) for r in rows)}</div></section>'
updates_html = ''.join(f'<p class="snapshot">Update {stamp(u["at"])}: {esc(u["text"])}</p>' for u in triage.get('updates', []))
body = f'''<header class="report-header"><p class="eyebrow">OpenHands / OpenHands · Maintainer review queue</p><h1 class="page">PRs to keep or close</h1><p class="lede"><strong>{len(keep)} Keep</strong> candidates and <strong>{len(close)} Close without merge</strong> candidates from the previously reviewed other-author PR queue. Each PR has its author and a specific reason.</p><p class="snapshot">Issue, PR and reference states checked through {stamp(triage['observed_at'])}. Code assessment dates from the original audit on 10 October 2026; refreshed heads are compared with that audit.</p>{updates_html}</header>
<nav class="report-nav" aria-label="Queue sections"><a href="#keep">Keep · {len(keep)}</a><a href="#close">Close without merge · {len(close)}</a><a href="#done">Already merged / closed · {len(archived)}</a><a href="#method">Review scope</a></nav>
<p class="callout">These are review recommendations. “Keep” retains a useful candidate for review. Closure reasons apply the maintainer’s policy that partial drafts and incomplete functional evidence can be closed. No PR closures or reviews are submitted by this report.</p>
{filters('triage-list','PRs',[('all',f'All {len(keep)+len(close)} active PRs'),('keep',f'Keep · {len(keep)}'),('close',f'Close without merge · {len(close)}')])}
<div id="triage-list"><section id="keep" data-filter-subgroup><h2 class="section-heading">Keep · {len(keep)} PRs</h2><div class="issue-list">{"".join(triage_card(r) for r in keep)}</div></section><section id="close" data-filter-subgroup><h2 class="section-heading">Close without merge · {len(close)} PRs</h2>{close_html}</section><p class="empty-filter" hidden>No matching PRs.</p></div>
<section id="done"><h2 class="section-heading">Already merged or closed · {len(archived)} PRs</h2><p>Removed from the active recommendations.</p><ul class="archive-list">{''.join(archive)}</ul></section>
<section class="method" id="method"><h2 class="section-heading">Review scope</h2><p>This page follows the original {len(all_triage)} open or draft other-author PRs reviewed for issues filed by enyst or smolpaws. It is a separate queue from the two creation-date cohort reports: issues here may be older than a week.</p><p>Reasons come from the earlier current-head production/test diff reviews, issue requirements, CI and available functional evidence. Fresh metadata confirms PR and issue states and whether the reviewed code head has changed. Existing links to reviews or contributor recordings are evidence, not a claim that this auditor reran every branch.</p><p>The earlier audit independently ran focused tests and a fail-before mutation check for PR #18151, and a minimal Chromium geometry reproduction for PR #18242. Those checks were not full OpenHands UI runs. No new branch runtime verification was performed for this refresh.</p><p><a href="../assets/openhands-maintainer-reports/triage.json">Checked triage dataset (JSON)</a> · <a href="../assets/openhands-maintainer-reports/triage.csv">Active recommendations (CSV)</a></p></section>'''
(OUT / PATHS['triage']).write_text(base('triage','OpenHands PRs · Keep / Close without merge',f'{len(keep)} Keep and {len(close)} Close without merge candidates, with titles, authors and individual reasons.',body))


def write_csv(filename, fields, rows):
    with (ASSETS / filename).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


csv_rows = []
for issue in records:
    prs = issue['open_prs'] if issue['classification'] == 'open' else issue['merged_prs']
    for pr in prs or [{}]:
        csv_rows.append({
            'issue':issue['number'], 'issue_title':issue['title'], 'issue_author':issue['author'],
            'issue_url':issue['url'], 'created_at':issue['created_at'], 'state':issue['state'],
            'outcome':issue['classification'], 'open_pr_count':len(issue['open_prs']),
            'issue_fix_scope':issue.get('fix_scope',''), 'issue_note':issue.get('note',''),
            'pr':pr.get('number',''), 'pr_title':pr.get('title',''), 'pr_author':pr.get('author',''),
            'pr_url':pr.get('url',''), 'pr_draft':pr.get('draft',''), 'merged_at':pr.get('merged_at',''),
            'pr_scope':pr.get('scope',''),
        })
write_csv('created-week.csv', ['issue','issue_title','issue_author','issue_url','created_at','state','outcome','open_pr_count','issue_fix_scope','issue_note','pr','pr_title','pr_author','pr_url','pr_draft','merged_at','pr_scope'], csv_rows)
write_csv('triage.csv',['recommendation','category','pr','pr_title','pr_author','pr_url','draft','issue','issue_url','issue_state','reason','head_sha'], [{
    'recommendation':r['decision'], 'category':r['group'], 'pr':r['pr'], 'pr_title':r['pr_title'],
    'pr_author':r['pr_author'], 'pr_url':r['pr_url'], 'draft':r.get('draft',False),
    'issue':r['issue'], 'issue_url':r['issue_url'], 'issue_state':r.get('issue_state',''),
    'reason':r['reason'], 'head_sha':r['head_sha'],
} for r in keep+close])
print(json.dumps({'cohort':len(records),'closed_by_merged_pr':len(closed),'own_pr_closures':own,'other_author_pr_closures':external,'partial_tracker_closures':len(partials),'open_issues':len(opened),'issues_with_open_pr':active,'distinct_open_prs':unique_open_prs,'open_pr_matches':pr_matches,'other_closures':len(other),'keep':len(keep),'close':len(close),'archived':len(archived)}, indent=2))
