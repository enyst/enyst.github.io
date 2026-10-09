#!/usr/bin/env python3
"""Render the checked issue inventory and original evidence as static HTML.

Edit assets/verify-openhands/issues.json, then run this script. It never queries
GitHub or changes the dated research snapshot. No third-party packages needed.
"""
import html

def render_gallery(rows, icon, repo_order, repo_slugs, themes, cohort_labels):
    if not all('visual' in r for r in rows):return ''
    esc=lambda x:html.escape(str(x),quote=True)
    chunks=['<section class="walkthrough" id="walkthrough" aria-labelledby="walkthrough-title"><header class="walkthrough-intro"><p class="eyebrow">The findings, up close</p><h2 id="walkthrough-title">What the issues looked like.</h2><p>One short walkthrough for each issue. Original before/after pairs are selected from the PRs where available; single issue captures, recordings and terminal evidence are labeled. API reproduction cards condense the linked reports; they are not new test runs. Open and closed-unmerged proposals show what was tested on that branch, not a shipped fix.</p><p class="small-muted">Select an image to inspect the full-size original. <a href="#issues">Return to the issue list ↑</a></p></header>']
    for repo in repo_order:
        slug=repo_slugs[repo]
        group=[r for r in rows if r['repo']==repo]
        chunks.append(f'<section class="detail-repo" aria-labelledby="detail-{slug}-heading"><header class="repo-heading"><h3 id="detail-{slug}-heading">{esc(repo)}</h3><span class="count">{len(group)} issues</span></header>')
        for theme in themes:
            items=[r for r in group if r['theme_slug']==theme['theme_slug']]
            if not items:continue
            chunks.append(f'<section class="detail-theme"><header class="theme-heading"><h4>{esc(theme["theme"])}</h4><span class="count">{len(items)} issues</span></header>')
            for row in sorted(items,key=lambda x:x['number']):
                v=row['visual'];article_id=f'detail-{slug}-{row["number"]}'
                title=row['title'].removeprefix('[Bug]: ').removeprefix('[Bug] ')
                chunks.append(f'<article class="issue-detail" id="{article_id}" aria-labelledby="{article_id}-title"><div class="detail-kicker"><a href="{esc(row["url"])}">{esc(repo.split("/")[-1])} #{row["number"]}</a><a href="#issue-{slug}-{row["number"]}">Back to list ↑</a></div><h5 id="{article_id}-title">{esc(title)}</h5><p class="detail-description">{esc(v["summary"])}</p>')
                chunks.append(f'<p class="run-label">{esc(cohort_labels[row["cohort"]])}</p>')
                reproduction=v.get('reproduction')
                if reproduction:
                    chunks.append('<dl class="reproduction">')
                    after_label='After' if (v.get('primary_pr') or {}).get('state')=='MERGED' else 'After · PR branch'
                    for key,label in [('action','Action'),('before','Before'),('after',after_label),('observed','Observed'),('expected','Expected')]:
                        if reproduction.get(key):chunks.append(f'<div class="{key}"><dt>{label}</dt><dd>{esc(reproduction[key])}</dd></div>')
                    chunks.append('</dl>')
                    if reproduction.get('note') and reproduction.get('before'):chunks.append(f'<p class="evidence-note">{esc(reproduction["note"])}</p>')
                images=v.get('images',[])
                if images:
                    pair=len(images)==2 and {x['role'] for x in images}=={'before','after'}
                    mode='image-pair' if pair else 'single-evidence'
                    chunks.append(f'<div class="visual-evidence {mode}">')
                    for i in images:
                        label={'before':'Before','after':'After','evidence':'Evidence'}.get(i['role'],'Evidence')
                        primary=v.get('primary_pr') or {}
                        if label=='After' and primary.get('state')!='MERGED':label='Proposed change' if primary.get('state')=='CLOSED' else 'After · PR branch'
                        if i.get('media_type')=='video':
                            chunks.append(f'<figure><span class="image-label {esc(i["role"])}">{label} · recording</span><video class="evidence-video" data-preview-time="1" controls preload="metadata" playsinline width="{i["width"]}" height="{i["height"]}" aria-label="{esc(i["alt"])}"><source src="{esc(i["src"])}" type="video/webm"><a href="{esc(i["src"])}">Open the original recording</a></video><figcaption>{esc(i["caption"])} <a href="{esc(i["src"])}">Full recording</a></figcaption></figure>')
                        else:
                            chunks.append(f'<figure><span class="image-label {esc(i["role"])}">{label}</span><a class="evidence-image" href="{esc(i["src"])}" target="_blank" rel="noopener" aria-label="Open full-size image: {esc(i["alt"])}"><img src="{esc(i["src"])}" width="{i["width"]}" height="{i["height"]}" alt="{esc(i["alt"])}" loading="lazy" decoding="async"></a><figcaption>{esc(i["caption"])}</figcaption></figure>')
                    chunks.append('</div>')
                if v.get('evidence_note'):chunks.append(f'<p class="evidence-note">{esc(v["evidence_note"])}</p>')
                if v.get('recordings'):
                    links=' · '.join(f'<a href="{esc(recording["url"])}">{esc(recording["label"])}</a>' for recording in v['recordings'])
                    chunks.append(f'<p class="evidence-note">Original recordings: {links}</p>')
                primary=v.get('primary_pr')
                if primary:
                    kind='merged' if primary['state']=='MERGED' else 'closed' if primary['state']=='CLOSED' else 'draft' if primary.get('is_draft',primary.get('isDraft')) else 'open'
                    label={'merged':'Merged','closed':'Closed unmerged','draft':'Draft PR','open':'Open PR'}[kind]
                    chunks.append(f'<p class="more-pr">More in the PR: <a href="{esc(primary["url"])}">{esc(primary["title"])}</a> <span class="inline-state {kind}">{icon(kind)}{label}</span></p>')
                else:chunks.append(f'<p class="more-pr">No fixing PR identified at the snapshot time. <a href="{esc(row["url"])}">More in the issue.</a></p>')
                chunks.append('</article>')
            chunks.append('</section>')
        chunks.append('</section>')
    chunks.append('</section>')
    return ''.join(chunks)

import json,html
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'assets/verify-openhands/issues.json').read_text())
esc=lambda x:html.escape(str(x),quote=True)
rows=data['issues']
total=len(rows)
assert len({(r['repo'],r['number']) for r in rows})==total
cohorts=data['cohorts']
cohort_labels={c['id']:c['label'] for c in cohorts}
api_count=sum(r['cohort']=='agent-server' for r in rows)
mapped_ids=data['feature_map_snapshot']['mapped_ids']
repo_order=['OpenHands/OpenHands','OpenHands/software-agent-sdk','OpenHands/automation']
repo_slugs={'OpenHands/OpenHands':'canvas','OpenHands/software-agent-sdk':'sdk','OpenHands/automation':'automation'}
repo_labels={'OpenHands/OpenHands':'Agent Canvas','OpenHands/software-agent-sdk':'Software Agent SDK','OpenHands/automation':'Automation'}
themes=data['theme_order']
checked=datetime.fromisoformat(data['checked_at'].replace('Z','+00:00')).astimezone(ZoneInfo('UTC'))
checked_label=f'{checked.day} {checked:%B %Y}, {checked:%H:%M} {checked:%Z}'
icon=lambda name:f'<svg class="icon" aria-hidden="true" viewBox="0 0 24 24"><use href="#icon-{name}"></use></svg>'
prs={f"{p['repo']}#{p['number']}":p for r in rows for p in r['prs']}
merged=sum(p['state']=='MERGED' for p in prs.values());opened=sum(p['state']=='OPEN' for p in prs.values());failed=sum(p['state']=='OPEN' and p.get('ci',{}).get('state')=='FAILURE' for p in prs.values())

def statuses(row):
 output=[];categories=set()
 for p in row['prs']:
  if p['state']=='MERGED':kind='merged';label='Merged'
  elif p['state']=='CLOSED':kind='closed';label='Closed unmerged'
  elif p.get('is_draft'):kind='draft';label='Draft PR';categories.add('open')
  else:kind='open';label='Open PR'
  categories.add(kind)
  relation={'related':'Related alternative','partial':'Partial fix'}.get(p.get('relation'),'')
  prefix=f'{p["repo"].split("/")[-1]} ' if p['repo']!=row['repo'] else ''
  output.append(f'<div class="pr-item"><div class="status-line {kind}">{icon(kind)}<span><strong>{label}</strong> · {esc(prefix)}#{p["number"]}</span></div>')
  if relation:output.append(f'<p class="status-detail">{relation}</p>')
  ci=p.get('ci',{});state=ci.get('state')
  if p['state']=='OPEN':
   if state=='FAILURE':
    categories.add('failed');count=len(ci.get('failed',[]));label='Checks failing'+(f' · {count} '+('check' if count==1 else 'checks') if count else '')
    title='; '.join(ci.get('failed',[]))
    output.append(f'<p class="status-detail failed" title="{esc(title)}">{icon("failed")}{label}</p>')
   elif state=='PENDING':output.append(f'<p class="status-detail pending">{icon("pending")}Checks pending</p>')
   elif state=='SUCCESS':output.append(f'<p class="status-detail '+('open' if not ci.get('metadata_only') else '')+f'">{icon("check")}{"Metadata checks only" if ci.get("metadata_only") else "Checks passing"}</p>')
   elif state=='CANCELLED':output.append(f'<p class="status-detail">{icon("closed")}Checks cancelled</p>')
   else:output.append('<p class="status-detail">No check result available</p>')
   if ci.get('detail'):output.append(f'<p class="status-detail">{esc(ci["detail"])}</p>')
  output.append('</div>')
 if not row['prs']:
  categories.add('none');output.append(f'<div class="status-line none">{icon("none")}<span>No fix PR found</span></div>')
 if row.get('note'):output.append(f'<p class="issue-note">{esc(row["note"])}</p>')
 return ''.join(output),' '.join(sorted(categories))

gallery_html=render_gallery(rows,icon,repo_order,repo_slugs,themes,cohort_labels)
cohort_options=''.join(f'<option value="{esc(c["id"])}">{esc(c["label"])}</option>' for c in cohorts)
cohort_summary=''.join(f'<li><strong>{sum(r["cohort"]==c["id"] for r in rows)}</strong><span>{esc(c["label"])}</span></li>' for c in cohorts)
sections=[]
for repo in repo_order:
 group=[r for r in rows if r['repo']==repo];slug=repo_slugs[repo]
 sections.append(f'<section class="repo-section" id="{slug}" aria-labelledby="{slug}-heading"><header class="repo-heading"><h2 id="{slug}-heading">{esc(repo)}</h2><span class="count">{len(group)} issues</span></header>')
 for theme in themes:
  rr=[r for r in group if r['theme_slug']==theme['theme_slug']]
  if not rr:continue
  themeid=f'{slug}-{theme["theme_slug"]}'
  sections.append(f'<section class="theme-group" aria-labelledby="{themeid}"><header class="theme-heading"><h3 id="{themeid}">{esc(theme["theme"])}</h3><span class="count">{len(rr)} '+('issue' if len(rr)==1 else 'issues')+'</span></header><ul class="issue-list">')
  for r in sorted(rr,key=lambda x:x['number']):
   status,categories=statuses(r)
   jump=f'<a class="evidence-jump" href="#detail-{slug}-{r["number"]}">See walkthrough ↓</a>' if 'visual' in r else ''
   reason=r.get('state_reason')
   issue_label='Issue open' if r['issue_state']=='OPEN' else 'Issue closed'+(' · not planned' if reason=='NOT_PLANNED' else '')
   search=' '.join([repo,repo_labels[repo],r['theme'],str(r['number']),r['title'],cohort_labels[r['cohort']]]+[str(p['number']) for p in r['prs']])
   sections.append(f'<li class="issue-row" id="issue-{slug}-{r["number"]}" data-cohort="{esc(r["cohort"])}" data-states="{categories}" data-search="{esc(search)}"><div class="issue-main"><span class="issue-key">#{r["number"]} · {issue_label}</span><a class="issue-title" href="{esc(r["url"])}">{esc(r["title"])}</a><span class="run-label">{esc(cohort_labels[r["cohort"]])}</span>{jump}</div><div class="issue-status" aria-label="Pull request status">{status}</div></li>')
  sections.append('</ul></section>')
 sections.append('</section>')
nav=''.join(f'<li><a href="#{repo_slugs[repo]}" data-repo="{repo_slugs[repo]}">{repo_labels[repo]} <span class="count">{sum(r["repo"]==repo for r in rows)}</span></a></li>' for repo in repo_order)
legend=''.join(f'<span class="legend-item {kind}">{icon(kind)}{label}</span>' for kind,label in [('merged','Merged'),('open','Open PR'),('draft','Draft PR'),('closed','Closed unmerged'),('failed','Checks failing'),('none','No fix PR found')])
page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#10110f">
<title>{total} findings: the issues and their fixes — OpenHands verification</title>
<meta name="description" content="Issues filed by OpenHands feature-map verification runs, grouped by repository and theme, with the checked status of their fixing pull requests.">
<meta property="og:title" content="{total} findings. Follow the fixes."><meta property="og:description" content="The full issue list behind OpenHands’ agent-driven verification effort, with pull request status."><meta property="og:type" content="article"><meta property="og:url" content="https://enyst.github.io/arch/verify-openhands-issues.html">
<link rel="canonical" href="https://enyst.github.io/arch/verify-openhands-issues.html">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/verify-openhands/issues.css"><script src="../assets/verify-openhands/issues.js" defer></script>
</head>
<body>
<a class="skip-link" href="#issues">Skip to issue list</a>
<svg class="symbol-defs" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs>
<symbol id="icon-merged" viewBox="0 0 24 24"><circle cx="6" cy="4" r="2.5"/><circle cx="6" cy="20" r="2.5"/><circle cx="18" cy="4" r="2.5"/><path d="M6 6.5v11M18 6.5c0 8-12 3-12 11"/></symbol>
<symbol id="icon-open" viewBox="0 0 24 24"><circle cx="6" cy="4" r="2.5"/><circle cx="6" cy="20" r="2.5"/><circle cx="18" cy="20" r="2.5"/><path d="M6 6.5v11M18 17.5V9a5 5 0 0 0-5-5h-1m3-3-3 3 3 3"/></symbol>
<symbol id="icon-draft" viewBox="0 0 24 24"><circle cx="6" cy="4" r="2.5"/><circle cx="6" cy="20" r="2.5"/><circle cx="18" cy="20" r="2.5"/><path d="M6 6.5v11M18 6v2m0 4v2"/></symbol>
<symbol id="icon-closed" viewBox="0 0 24 24"><circle cx="6" cy="4" r="2.5"/><circle cx="6" cy="20" r="2.5"/><path d="M6 6.5v11m8-12 6 6m0-6-6 6m4 4v5"/></symbol>
<symbol id="icon-failed" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m9 9 6 6m0-6-6 6"/></symbol>
<symbol id="icon-pending" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
<symbol id="icon-check" viewBox="0 0 24 24"><path d="m5 12 4 4L19 6"/></symbol>
<symbol id="icon-none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" stroke-dasharray="3 3"/><path d="M9 12h6"/></symbol>
</defs></svg>
<header class="masthead"><a class="brand" href="../index.html">EN <span>/ field notes</span></a><a href="../openhands-features/index.html">Feature recipes</a><a href="verify-openhands.html#evolution">← Back to the presentation</a></header>
<main class="shell">
<header>
<p class="eyebrow">OpenHands / the verification findings</p>
<div class="intro-grid"><h1>{total} findings.<br><em>Follow the fixes.</em></h1><div><p class="lede">The original 68 findings, followed by new reports from later feature-map runs. Grouped by repository and theme, with the status of the associated fixing PRs on the right.</p><p class="collaboration-note">The fixes include both community and agent-authored PRs. Existing contributor work was reviewed rather than duplicated.</p><p class="snapshot">Status snapshot checked <time datetime="{esc(data['checked_at'])}">{checked_label}</time>.<br>Open an issue for its discussion, linked PRs and latest updates.</p></div></div>
<dl class="summary"><div><dt>issues in this list</dt><dd>{total}</dd></div><div class="merged"><dt>associated PRs merged</dt><dd>{merged}</dd></div><div class="open"><dt>associated PRs open</dt><dd>{opened}</dd></div><div class="failed"><dt>open PRs with failing checks</dt><dd>{failed}</dd></div></dl>
<p class="summary-note">PR totals count distinct PRs, including identified alternatives. An issue can have several PRs, and a merged partial fix can leave an issue open.</p>
<ul class="run-summary" aria-label="Findings by verification run">{cohort_summary}</ul>
<p class="summary-note">The follow-ups include Canvas runs and bugs found while verifying earlier fixes. The {api_count} Agent Server API reports come from a <a href="https://github.com/OpenHands/software-agent-sdk/pull/5621">separate, still-draft feature map</a>; they are not added to Canvas’s {mapped_ids} mapped behaviors.</p>
</header>
<nav class="page-tabs" aria-label="Page sections"><a href="#issues">Issue list</a><a href="#walkthrough">Visual walkthrough</a><a href="#reading-statuses">About the statuses</a></nav>
<div class="legend" aria-label="Status icon legend">{legend}</div>
<div class="filters" role="search" aria-label="Filter verification issues"><div class="search-field"><label for="issue-search">Search issues</label><input id="issue-search" type="search" placeholder="Title, issue number, PR number, or theme…" autocomplete="off"></div><div class="run-field"><label for="run-filter">Verification run</label><select id="run-filter"><option value="all">All runs</option>{cohort_options}</select></div><div><label for="status-filter">PR status</label><select id="status-filter"><option value="all">All statuses</option><option value="merged">Has a merged PR</option><option value="open">Has an open PR</option><option value="failed">Checks failing</option><option value="draft">Has a draft PR</option><option value="closed">Has a closed, unmerged PR</option><option value="none">No fix PR found</option></select></div><button type="button" id="clear-filters">Clear</button></div>
<div class="filter-note"><p id="result-count" role="status" aria-live="polite">Showing {total} of {total} issues</p><p>Filter matches any associated PR.</p></div>
<div class="ledger-layout" id="issues"><nav class="repo-nav" aria-label="Repositories"><h2>By repository</h2><ul>{nav}</ul><a class="back-link" href="#reading-statuses">How to read statuses</a></nav><div>
{''.join(sections)}
<div class="empty-state" id="no-results" hidden><strong>No matching issues</strong><p>Try another term or clear the filters.</p></div>
</div></div>
{gallery_html}
<section class="method" id="reading-statuses"><h2>How to read this list</h2><p>The first 68 come from <a href="https://github.com/OpenHands/OpenHands/pull/17961">#17961’s “Issues filed” inventory</a>: 62 in Agent Canvas, five in the SDK, and one in automation. Later Canvas findings are included when their issue bodies or run reports tie them to a feature-map verification run. Each distinct issue is counted once, including follow-up reports of a recurring symptom; existing issues rechecked by later runs keep their original group. Themes are editorial groupings.</p><p>The separate <a href="https://github.com/OpenHands/software-agent-sdk/pull/5621">verify-agent-server draft PR #5621</a> reports {api_count} new API bugs, catalogued in <a href="https://github.com/OpenHands/software-agent-sdk/issues/5653">its umbrella issue</a>. Those {api_count} have their own run label. The umbrella and requests to build the maps are not counted as additional bugs. Older issues merely reproduced by later runs are not added again.</p><p>Issue titles and states were read from GitHub. Fixing PRs were checked through closure events, explicit closing references, PR descriptions and issue discussions. General mentions and the feature-map PR itself are excluded. Related alternatives and partial fixes are labeled. “No fix PR found” means no fixing PR was identified in those sources at the check time.</p><p>PR state and issue state are separate. “Merged” describes the PR; it does not claim that every part of an issue was fixed. Check indicators use the newest run of each app, workflow and job on an open PR’s latest head. Older failed runs superseded by a successful run do not count as current failures; the original GitHub rollup remains in the downloadable data. A red indicator records a failing check, not a judgment about its cause. Closed PRs are not treated as merged.</p><p>The <a href="control-openhands-cli.html#fleet">fix-fleet report</a> records how work already claimed by contributors was left to them. This page tracks the fixes together, without attributing every PR to that fleet.</p><p>This is a dated snapshot, with no automatic refresh. <a href="../assets/verify-openhands/issues.json">Download the checked issue and PR data</a>, or return to <a href="verify-openhands.html">the verification presentation</a>.</p></section>
<footer class="footer">Engel’s Code Design Notebook · Source-linked product verification.</footer>
</main></body></html>'''
(ROOT/'arch/verify-openhands-issues.html').write_text(page+'\n')
print('Rendered',len(rows),'issues;',len(prs),'unique associated PRs;',merged,'merged;',opened,'open;',failed,'CI failing')
