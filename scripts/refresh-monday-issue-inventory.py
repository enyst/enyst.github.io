#!/usr/bin/env python3
"""Refresh the frozen maintainer issue inventory from read-only GitHub metadata.

Preserves issue membership and previously reviewed implementation/exclusion
decisions. Discovers new explicit fixing references and authoritative closers;
ambiguous new references are saved for human inspection outside the repository.
Uses the inherited proxy and GITHUB_TOKEN_ENYST/GITHUB_TOKEN. No GitHub writes.
"""
import argparse
from collections import Counter
import concurrent.futures
import copy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPO = 'OpenHands/OpenHands'
OWN = {'enyst', 'smolpaws'}
DATA_PATH = ROOT / 'assets/openhands-monday-issue-inventory/data.json'
spec = importlib.util.spec_from_file_location('verification_refresh', ROOT / 'scripts/refresh-verification-findings.py')
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)
PR_FIELDS = '''number title url body state isDraft mergedAt closedAt createdAt updatedAt
headRefOid author{login} repository{nameWithOwner}'''
EVENT_FIELDS = '''__typename ...on ClosedEvent{createdAt closer{__typename ...on PullRequest{%s}}}
...on ReopenedEvent{createdAt}
...on CrossReferencedEvent{createdAt source{__typename ...on PullRequest{%s}}}''' % (PR_FIELDS, PR_FIELDS)
ISSUE_FIELDS = '''number title url body state stateReason closedAt createdAt updatedAt author{login}
repository{nameWithOwner} timelineItems(last:100,itemTypes:[CROSS_REFERENCED_EVENT,CLOSED_EVENT,REOPENED_EVENT]){
pageInfo{hasPreviousPage startCursor}nodes{%s}}''' % EVENT_FIELDS


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def key(obj):
    return obj['repository']['nameWithOwner'] + '#' + str(obj['number'])


def url_key(url):
    match = re.search(r'github\.com/([^/]+/[^/]+)/(?:pull|issues)/(\d+)', url or '')
    return match[1] + '#' + match[2] if match else None


def fetch_objects(keys, kind):
    grouped = {}
    for object_key in keys:
        repo, number = object_key.rsplit('#', 1)
        grouped.setdefault(repo, []).append(int(number))
    batches = []
    for repo, numbers in grouped.items():
        numbers = sorted(set(numbers))
        for start in range(0, len(numbers), 8):
            fields = ISSUE_FIELDS if kind == 'issue' else PR_FIELDS
            selection = ' '.join('i%d:%s(number:%d){%s}' % (n, kind, n, fields) for n in numbers[start:start + 8])
            batches.append((repo, api.repo_query(repo, selection)))
    objects = {}
    def fetch(batch):
        repo, query = batch
        result = api.graphql(query)['repository']
        if any(value is None for value in result.values()):
            raise RuntimeError('A tracked %s in %s was unavailable' % (kind, repo))
        return result
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for result in executor.map(fetch, batches):
            objects.update((key(value), value) for value in result.values())
    if kind == 'issue':
        for value in objects.values():
            connection = value['timelineItems']
            while connection['pageInfo']['hasPreviousPage']:
                selection = 'issue(number:%d){timelineItems(last:100,before:%s,itemTypes:[CROSS_REFERENCED_EVENT,CLOSED_EVENT,REOPENED_EVENT]){pageInfo{hasPreviousPage startCursor}nodes{%s}}}' % (value['number'], json.dumps(connection['pageInfo']['startCursor']), EVENT_FIELDS)
                connection = api.graphql(api.repo_query(value['repository']['nameWithOwner'], selection))['repository']['issue']['timelineItems']
                value['timelineItems']['nodes'] = connection['nodes'] + value['timelineItems']['nodes']
            value['timelineItems']['pageInfo'] = connection['pageInfo']
    return objects


def discover_prs(since):
    results, pages = {}, []
    for state in ['OPEN', 'CLOSED', 'MERGED']:
        cursor = None
        while True:
            after = ',after:' + json.dumps(cursor) if cursor else ''
            selection = 'pullRequests(first:100,states:%s,orderBy:{field:UPDATED_AT,direction:DESC}%s){pageInfo{hasNextPage endCursor}nodes{%s}}' % (state, after, PR_FIELDS)
            connection = api.graphql(api.repo_query(REPO, selection))['repository']['pullRequests']
            pages.append({'state': state, 'records': len(connection['nodes']), 'has_next_page': connection['pageInfo']['hasNextPage']})
            for pr in connection['nodes']:
                if state == 'OPEN' or pr['updatedAt'] >= since:
                    results[key(pr)] = pr
            if not connection['pageInfo']['hasNextPage']:
                break
            if state != 'OPEN' and connection['nodes'] and connection['nodes'][-1]['updatedAt'] < since:
                break
            cursor = connection['pageInfo']['endCursor']
    return results, pages


def tracked_keys(data, survey, weekly):
    issues = {REPO + '#' + str(r['number']) for r in data['records']}
    issues.update(REPO + '#' + str(r['number']) for r in survey['openIssues']['issues'])
    issues.update(REPO + '#' + str(r['issue']) for r in survey['weeklyClosures']['rows'])
    issues.update(REPO + '#' + str(r['number']) for r in weekly['records'])
    prs = set()
    def walk(value):
        if isinstance(value, dict):
            for name in ('url', 'pr_url'):
                if '/pull/' in str(value.get(name, '')):
                    object_key = url_key(value[name])
                    if object_key:
                        prs.add(object_key)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    for value in [data, survey, weekly]:
        walk(value)
    return issues, prs


def current_closers(issue):
    if issue['state'] != 'CLOSED':
        return []
    closed = [e for e in issue['timelineItems']['nodes'] if e['__typename'] == 'ClosedEvent']
    if not closed:
        return []
    event = max(closed, key=lambda e: e['createdAt'])
    closer = event.get('closer')
    return [closer] if closer and closer.get('__typename') == 'PullRequest' and closer.get('mergedAt') else []


def normalize_pr(pr, old=None, checked_at=None):
    row = copy.deepcopy(old or {})
    row.update(number=pr['number'], title=pr['title'], url=pr['url'],
               author=(pr.get('author') or {}).get('login', 'ghost'),
               author_url='https://github.com/' + (pr.get('author') or {}).get('login', 'ghost'),
               state='open' if pr['state'] == 'OPEN' else 'closed', draft=pr['isDraft'],
               merged=bool(pr['mergedAt']), merged_at=pr['mergedAt'], closed_at=pr['closedAt'],
               created_at=pr['createdAt'], updated_at=pr['updatedAt'], head_sha=pr['headRefOid'],
               state_observed_at=checked_at)
    return row


def active(pr):
    return pr['state'] == 'open' and not pr.get('merged')


def recalculate_counts(records):
    opened = [r for r in records if r['state'] == 'open']
    closed = [r for r in records if r['state'] == 'closed']
    all_prs = {url_key(p['url']): p for r in records for p in r['proposed_prs']}
    own_any = sum(bool(r['own_prs']) for r in records)
    direct = [r for r in closed if r['direct_closing_prs']]
    own_direct = sum(all(p['author'] in OWN for p in r['direct_closing_prs']) for r in direct)
    active_own = sum(any(active(p) for p in r['own_prs']) for r in opened)
    return {
        'issue_count': len(records), 'issue_authors': dict(Counter(r['author'] for r in records)),
        'with_own_pr': own_any, 'without_own_pr': len(records) - own_any,
        'open': len(opened), 'closed': len(closed),
        'open_with_own_pr': sum(bool(r['own_prs']) for r in opened),
        'open_without_own_pr': sum(not r['own_prs'] for r in opened),
        'open_with_active_own_pr': active_own,
        'open_with_closed_only_own_pr': sum(bool(r['own_prs']) and all(not active(p) and not p['merged'] for p in r['own_prs']) for r in opened),
        'open_with_merged_own_pr': sum(any(p['merged'] for p in r['own_prs']) for r in opened),
        'open_with_inactive_own_history': sum(bool(r['own_prs']) and not any(active(p) for p in r['own_prs']) for r in opened),
        'open_without_active_own_pr': len(opened) - active_own,
        'closed_direct_merged_pr': len(direct), 'closed_direct_merged_pr_own': own_direct,
        'closed_direct_merged_pr_other': len(direct) - own_direct, 'closed_without_direct_pr': len(closed) - len(direct),
        'distinct_proposed_prs': len(all_prs), 'proposed_pr_issue_matches': sum(len(r['proposed_prs']) for r in records),
        'excluded_reference_pairs': sum(len(r['excluded_references']) for r in records),
        'distinct_open_prs': sum(active(p) for p in all_prs.values()),
    }


def refresh_weekly(weekly, cache, inventory):
    """Keep the 106-issue creation cohort while updating current states/PRs."""
    previous = copy.deepcopy(weekly)
    indexed = {r['number']: r for r in inventory['records']}
    checked_at = cache['fetch_finished_at']
    for row in weekly['records']:
        issue = cache['issues'][REPO + '#' + str(row['number'])]
        old_by_url = {p['url']: p for p in row['open_prs'] + row['merged_prs']}
        matches = indexed.get(row['number'], {}).get('proposed_prs', [])
        if not matches:
            matches = [normalize_pr(cache['prs'][url_key(p['url'])], p, checked_at) for p in old_by_url.values()]
            known_urls = {p['url'] for p in matches}
            for pr in cache['prs'].values():
                if pr['url'] not in known_urls and api.explicitly_fixes(pr, REPO, row['number']):
                    matches.append(normalize_pr(pr, {'scope': 'Explicit implementation/fixing reference in the PR description.', 'fix_scope': 'issue_fix'}, checked_at))
        merged_prs = []
        for pr in current_closers(issue):
            old = old_by_url.get(pr['url']) or next((p for p in matches if p['url'] == pr['url']), {})
            merged_prs.append(normalize_pr(cache['prs'][key(pr)], old, checked_at))
        row.update(state=issue['state'].lower(), title=issue['title'], updated_at=issue['updatedAt'], closed_at=issue['closedAt'],
                   merged_prs=merged_prs, open_prs=[p for p in matches if active(p)])
        row['open_pr_count'] = len(row['open_prs'])
        row['classification'] = 'open' if row['state'] == 'open' else 'closed_merged_pr' if merged_prs else 'closed_other'
        if row.get('fix_scope') != 'partial':
            row['note'] = None if merged_prs or row['open_prs'] else 'No current open implementation PR identified.' if row['state'] == 'open' else 'No direct merged-PR closer identified by GitHub.'
    closed = [r for r in weekly['records'] if r['classification'] == 'closed_merged_pr']
    opened = [r for r in weekly['records'] if r['classification'] == 'open']
    other = [r for r in weekly['records'] if r['classification'] == 'closed_other']
    own_closed = sum(all(p['author'] in OWN for p in r['merged_prs']) for r in closed)
    open_prs = {url_key(p['url']): p for r in opened for p in r['open_prs']}
    weekly['counts'] = {'issue_count': len(weekly['records']), 'issue_authors': dict(Counter(r['author'] for r in weekly['records'])),
        'closed_by_merged_pr': len(closed), 'closed_pr_author_groups': {'enyst_smolpaws': own_closed, 'other_authors': len(closed) - own_closed},
        'closed_pr_authors': dict(Counter(p['author'] for r in closed for p in r['merged_prs'])),
        'closed_with_full_issue_fix_scope': sum(r.get('fix_scope') != 'partial' for r in closed),
        'closed_with_partial_scope': sum(r.get('fix_scope') == 'partial' for r in closed),
        'closed_other': len(other), 'open': len(opened), 'open_with_prs': sum(bool(r['open_prs']) for r in opened),
        'open_without_prs': sum(not r['open_prs'] for r in opened), 'open_pr_matches': sum(len(r['open_prs']) for r in opened),
        'distinct_open_prs': len(open_prs), 'open_draft_pr_matches': sum(p['draft'] for r in opened for p in r['open_prs']),
        'distinct_open_draft_prs': sum(p['draft'] for p in open_prs.values())}
    weekly.update(observed_at=checked_at, metadata_fetch_started_at=cache['fetch_started_at'], metadata_fetch_finished_at=checked_at, audit_completed_at=now())
    weekly['refresh'] = {'previous_observed_at': previous['observed_at'], 'observed_at': checked_at, 'frozen_issue_membership': len(weekly['records']),
                         'previous_counts': previous['counts'], 'current_counts': weekly['counts'],
                         'method': 'Frozen October 4–11 creation cohort; current issue and matching PR states refreshed from the same complete GitHub cache as the Monday inventory. Original partial tracker caveat retained. No runtime checks or GitHub writes.'}
    weekly['audit_summary'] = {'frozen_membership_preserved': {r['number'] for r in weekly['records']} == {r['number'] for r in previous['records']},
                              'window_preserved': weekly['window'] == previous['window'], 'classification_reconciles': len(closed) + len(opened) + len(other) == len(weekly['records'])}
    (ROOT / 'assets/openhands-maintainer-reports/created-week.json').write_text(json.dumps(weekly, indent=2, ensure_ascii=False) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-output', default='/workspace/verification-status-api.json')
    parser.add_argument('--audit-output', default='/workspace/verification-status-changes.json')
    parser.add_argument('--from-cache', action='store_true')
    parser.add_argument('--refresh-weekly', action='store_true', help='Also refresh the related frozen weekly creation cohort.')
    args = parser.parse_args()
    previous = json.loads(DATA_PATH.read_text())
    survey = json.loads((ROOT / 'assets/openhands-issue-pr-report/data.json').read_text())
    weekly = json.loads((ROOT / 'assets/openhands-maintainer-reports/created-week.json').read_text())
    issue_keys, pr_keys = tracked_keys(previous, survey, weekly)
    if args.from_cache:
        cache = json.loads(Path(args.cache_output).read_text())
    else:
        started = now()
        print('Fetching %d tracked issues and their complete reference/closure histories.' % len(issue_keys), flush=True)
        issues = fetch_objects(issue_keys, 'issue')
        print('Discovering all open and recently updated closed/merged PRs.', flush=True)
        since = min(previous['observed_at'], survey['observed_at'], weekly['observed_at'])
        discovered, pages = discover_prs(since)
        for issue in issues.values():
            for event in issue['timelineItems']['nodes']:
                pr = event.get('closer') or event.get('source')
                if pr and pr.get('__typename') == 'PullRequest':
                    pr_keys.add(key(pr))
        print('Reading %d tracked/reference PRs; %d discovery records.' % (len(pr_keys), len(discovered)), flush=True)
        prs = dict(discovered)
        prs.update(fetch_objects(pr_keys - prs.keys(), 'pullRequest'))
        cache = {'fetch_started_at': started, 'fetch_finished_at': now(), 'issues': issues, 'prs': prs,
                 'discovery': {'since': since, 'pages': pages, 'records': len(discovered), 'repository': REPO}}
        Path(args.cache_output).write_text(json.dumps(cache, indent=2) + '\n')
        print('API cache ready: ' + args.cache_output, flush=True)
    issues, prs = cache['issues'], cache['prs']
    checked_at = cache['fetch_finished_at']
    result = copy.deepcopy(previous)
    issue_changes, new_matches, pr_changes, ambiguous = [], [], [], []
    for row in result['records']:
        issue = issues[REPO + '#' + str(row['number'])]
        if row['state'] != issue['state'].lower():
            issue_changes.append({'issue': row['number'], 'previous_state': row['state'], 'state': issue['state'].lower(), 'closed_at': issue['closedAt']})
        row.update(state=issue['state'].lower(), state_reason=(issue.get('stateReason') or '').lower(),
                   title=issue['title'], author=(issue.get('author') or {}).get('login', 'ghost'),
                   updated_at=issue['updatedAt'], closed_at=issue['closedAt'], state_observed_at=checked_at,
                   status_drift_note=None, reconciliation_note=None)
        candidates = {url_key(p['url']): p for p in row['proposed_prs']}
        exclusions = {url_key(p['url']): p for p in row['excluded_references']}
        closers = current_closers(issue)
        closer_keys = {key(p) for p in closers}
        for pr in prs.values():
            object_key = key(pr)
            if object_key in candidates or (object_key in exclusions and object_key not in closer_keys):
                continue
            explicit = api.explicitly_fixes(pr, REPO, row['number'])
            if object_key in closer_keys or explicit:
                candidates[object_key] = {
                    'scope': 'GitHub identifies this merged PR as the issue’s closer.' if object_key in closer_keys else 'Explicit implementation/fixing reference in the PR description; completion is not independently verified.',
                    'fix_scope': 'issue_fix',
                    'evidence': {'types': ['github_direct_closed_event' if object_key in closer_keys else 'explicit_fixing_reference_in_pr_body'], 'urls': [pr['url']]},
                }
                exclusions.pop(object_key, None)
                new_matches.append({'issue': row['number'], 'pr': pr['number'], 'author': (pr.get('author') or {}).get('login'), 'url': pr['url'], 'direct_closer': object_key in closer_keys})
            elif pr['repository']['nameWithOwner'] == REPO and re.search(r'#%d(?!\d)' % row['number'], pr.get('body') or ''):
                contexts = [pr['body'][max(0, m.start()-170):m.end()+200] for m in re.finditer(r'#%d(?!\d)' % row['number'], pr['body'])]
                ambiguous.append({'issue': row['number'], 'pr': pr['number'], 'url': pr['url'], 'title': pr['title'], 'author': (pr.get('author') or {}).get('login'), 'contexts': contexts})
        normalized = []
        for object_key, old in candidates.items():
            pr = prs[object_key]
            fresh = normalize_pr(pr, old, checked_at)
            fresh['direct_closer'] = object_key in closer_keys
            if (old.get('state'), bool(old.get('merged'))) != (fresh['state'], fresh['merged']):
                pr_changes.append({'issue': row['number'], 'pr': fresh['number'], 'url': fresh['url'], 'previous_state': old.get('state'), 'previous_merged': bool(old.get('merged')), 'state': fresh['state'], 'merged': fresh['merged'], 'merged_at': fresh['merged_at'], 'closed_at': fresh['closed_at']})
            normalized.append(fresh)
        row['proposed_prs'] = sorted(normalized, key=lambda p: p['number'])
        row['own_prs'] = [p for p in row['proposed_prs'] if p['author'].lower() in OWN]
        row['other_prs'] = [p for p in row['proposed_prs'] if p['author'].lower() not in OWN]
        row['open_prs'] = [p for p in row['proposed_prs'] if active(p)]
        row['merged_prs'] = [p for p in row['proposed_prs'] if p['merged']]
        row['closed_without_merge_prs'] = [p for p in row['proposed_prs'] if not active(p) and not p['merged']]
        row['direct_closing_prs'] = [p for p in row['proposed_prs'] if p['direct_closer']]
        row['excluded_references'] = [normalize_pr(prs[k], old, checked_at) for k, old in exclusions.items()]
        row['has_own_pr'] = bool(row['own_prs'])
        for name, value in [('own_pr_count', len(row['own_prs'])), ('other_pr_count', len(row['other_prs'])), ('open_pr_count', len(row['open_prs'])), ('own_open_pr_count', sum(active(p) for p in row['own_prs'])), ('other_open_pr_count', sum(active(p) for p in row['other_prs'])), ('own_merged_pr_count', sum(p['merged'] for p in row['own_prs'])), ('own_closed_without_merge_pr_count', sum(not active(p) and not p['merged'] for p in row['own_prs']))]:
            if name in row:
                row[name] = value
        if row['state'] == 'open':
            row['closure_note'] = None
        elif row['direct_closing_prs']:
            row['closure_note'] = 'GitHub’s latest issue-closing event names ' + ', '.join('#' + str(p['number']) for p in row['direct_closing_prs']) + '; closure alone does not verify every requirement.'
        else:
            row['closure_note'] = 'Closed without an identified direct merged-PR closer; closure alone does not prove an implementation.'
    result['counts'] = recalculate_counts(result['records'])
    result.update(observed_at=checked_at, fetch_started_at=cache['fetch_started_at'], fetch_finished_at=checked_at, normalized_at=now(), status_drift=[])
    result['refresh_changes'] = {'previous_observed_at': previous['observed_at'], 'current_observed_at': checked_at,
        'previous_counts': previous['counts'], 'current_counts': result['counts'], 'new_issue_numbers': [],
        'issue_state_changes': issue_changes, 'new_implementation_matches': new_matches, 'pr_state_changes': pr_changes,
        'previous_open_without_own_pr_count': previous['counts']['open_without_own_pr'], 'current_open_without_own_pr_count': result['counts']['open_without_own_pr']}
    result['methodology']['latest_status_refresh'] = {'frozen_issue_membership': len(result['records']), 'full_issue_timeline_pages_exhausted': True,
        'discovery': cache['discovery'], 'classification': 'Previously reviewed matches/exclusions retained. New explicit fixing references or direct GitHub closers added; ambiguous new references audited separately. Metadata refresh only; no runtime checks or GitHub mutations.'}
    assert {r['number'] for r in result['records']} == {r['number'] for r in previous['records']}
    assert result['window'] == previous['window']
    DATA_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    if args.refresh_weekly:
        refresh_weekly(weekly, cache, result)
    audit = dict(result['refresh_changes'], ambiguous_new_references=ambiguous)
    Path(args.audit_output).write_text(json.dumps(audit, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'counts': result['counts'], 'issue_changes': issue_changes, 'new_matches': new_matches,
                      'ambiguous_references_to_audit': len(ambiguous), 'audit_output': args.audit_output}, indent=2), flush=True)


if __name__ == '__main__':
    main()
