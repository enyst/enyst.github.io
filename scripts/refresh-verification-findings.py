#!/usr/bin/env python3
"""Refresh the existing verification cohort from GitHub without changing evidence.

Uses GITHUB_TOKEN_ENYST or GITHUB_TOKEN through the inherited HTTPS proxy. Reads
every tracked issue and PR, paginates issue references and current-head checks,
and discovers explicit fixing PRs among all open PRs and recently updated closed
PRs in the three tracked repositories. No GitHub writes are performed.
"""
import argparse
import copy
import concurrent.futures
import datetime as dt
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPOSITORIES = ['OpenHands/OpenHands', 'OpenHands/software-agent-sdk', 'OpenHands/automation']
PR_FIELDS = '''number title url body state isDraft mergedAt updatedAt headRefOid
repository{nameWithOwner} commits(last:1){nodes{commit{statusCheckRollup{state
contexts(first:100){pageInfo{hasNextPage endCursor}nodes{__typename
...on CheckRun{name status conclusion startedAt completedAt checkSuite{app{id slug} workflowRun{workflow{databaseId}}}}
...on StatusContext{context state createdAt}}}}}}}'''
SOURCE_FIELDS = 'number title url body state isDraft mergedAt repository{nameWithOwner}'
EVENT_FIELDS = '''__typename ...on ClosedEvent{createdAt closer{__typename ...on PullRequest{%s}}}
...on CrossReferencedEvent{createdAt source{__typename ...on PullRequest{%s}}}''' % (SOURCE_FIELDS, SOURCE_FIELDS)
ISSUE_FIELDS = '''number title url body state stateReason closedAt updatedAt repository{nameWithOwner}
timelineItems(last:100,itemTypes:[CROSS_REFERENCED_EVENT,CLOSED_EVENT]){pageInfo{hasPreviousPage startCursor}nodes{%s}}''' % EVENT_FIELDS


def graphql(query):
    token = os.environ.get('GITHUB_TOKEN_ENYST') or os.environ.get('GITHUB_TOKEN')
    if not token:
        raise RuntimeError('Set GITHUB_TOKEN_ENYST or GITHUB_TOKEN; credentials are never printed.')
    request = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({'query':query}).encode(),
        headers={'Authorization':'Bearer '+token, 'Content-Type':'application/json', 'User-Agent':'verification-findings-refresh'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                result = json.load(response)
            if result.get('errors'):
                raise RuntimeError('GraphQL response errors: '+json.dumps(result['errors']))
            return result['data']
        except (urllib.error.URLError, TimeoutError) as error:
            if attempt == 3:
                raise RuntimeError('GitHub fetch failed: '+str(error)) from error
            time.sleep(2 ** attempt)


def repo_query(repo, selection):
    owner, name = repo.split('/')
    return '{repository(owner:%s,name:%s){%s}}' % (json.dumps(owner),json.dumps(name),selection)


def fetch_objects(keys, kind):
    batches = []
    for repo in REPOSITORIES:
        numbers = sorted(n for r,n in keys if r == repo)
        for start in range(0,len(numbers),8):
            fields = ISSUE_FIELDS if kind == 'issue' else PR_FIELDS
            selection = ' '.join('item%d:%s(number:%d){%s}' % (n,kind,n,fields) for n in numbers[start:start+8])
            batches.append((repo,repo_query(repo,selection)))
    objects = {}
    def fetch(batch):
        repo,query = batch
        response = graphql(query)['repository']
        for alias,value in response.items():
            if value is None:
                raise RuntimeError('%s #%s unavailable' % (repo,alias.removeprefix('item')))
        return repo,response
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for repo,response in executor.map(fetch,batches):
            for value in response.values():
                objects[(repo,value['number'])] = value
    for (repo,number),value in objects.items():
        if kind == 'issue':
            connection = value['timelineItems']
            while connection['pageInfo']['hasPreviousPage']:
                selection = 'issue(number:%d){timelineItems(last:100,before:%s,itemTypes:[CROSS_REFERENCED_EVENT,CLOSED_EVENT]){pageInfo{hasPreviousPage startCursor}nodes{%s}}}' % (number,json.dumps(connection['pageInfo']['startCursor']),EVENT_FIELDS)
                connection = graphql(repo_query(repo,selection))['repository']['issue']['timelineItems']
                value['timelineItems']['nodes'] = connection['nodes'] + value['timelineItems']['nodes']
            value['timelineItems']['pageInfo'] = connection['pageInfo']
        else:
            commits = value['commits']['nodes']
            rollup = commits[0]['commit']['statusCheckRollup'] if commits else None
            if not rollup:
                continue
            connection = rollup['contexts']
            while connection['pageInfo']['hasNextPage']:
                selection = 'pullRequest(number:%d){commits(last:1){nodes{commit{statusCheckRollup{contexts(first:100,after:%s){pageInfo{hasNextPage endCursor}nodes{__typename ...on CheckRun{name status conclusion startedAt completedAt checkSuite{app{id slug} workflowRun{workflow{databaseId}}}} ...on StatusContext{context state createdAt}}}}}}}}}' % (number,json.dumps(connection['pageInfo']['endCursor']))
                connection = graphql(repo_query(repo,selection))['repository']['pullRequest']['commits']['nodes'][0]['commit']['statusCheckRollup']['contexts']
                rollup['contexts']['nodes'].extend(connection['nodes'])
            rollup['contexts']['pageInfo'] = connection['pageInfo']
    return objects


def discover_prs(since, cached_index=None):
    results = {}
    if cached_index:
        cached = json.loads(Path(cached_index).read_text())
        for pr in cached['open_prs'] + cached['recent_closed_prs']:
            if pr['state'] != 'open' and pr['updated_at'] < since:
                continue
            results[('OpenHands/OpenHands',pr['number'])] = {
                'number':pr['number'],'title':pr['title'],'url':pr['html_url'],
                'body':pr['body'] or '', 'state':'MERGED' if pr['merged_at'] else pr['state'].upper(),
                'isDraft':pr['draft'],'mergedAt':pr['merged_at'],'updatedAt':pr['updated_at'],
                'repository':{'nameWithOwner':'OpenHands/OpenHands'}}
    for repo in REPOSITORIES:
        if cached_index and repo == 'OpenHands/OpenHands':
            continue
        for state in ['OPEN','CLOSED','MERGED']:
            cursor = None
            while True:
                after = ',after:'+json.dumps(cursor) if cursor else ''
                query = repo_query(repo,'pullRequests(first:100,states:%s,orderBy:{field:UPDATED_AT,direction:DESC}%s){pageInfo{hasNextPage endCursor}nodes{number title url body state isDraft mergedAt updatedAt repository{nameWithOwner}}}' % (state,after))
                connection = graphql(query)['repository']['pullRequests']
                for pr in connection['nodes']:
                    if state == 'OPEN' or pr['updatedAt'] >= since:
                        results[(repo,pr['number'])] = pr
                if not connection['pageInfo']['hasNextPage']:
                    break
                if state != 'OPEN' and connection['nodes'] and connection['nodes'][-1]['updatedAt'] < since:
                    break
                cursor = connection['pageInfo']['endCursor']
    return results


def explicitly_fixes(pr,repo,number):
    owner,name = repo.split('/')
    references = [re.escape('https://github.com/'+repo+'/issues/'+str(number)),re.escape(repo+'#'+str(number))]
    if pr['repository']['nameWithOwner'] == repo:
        references.append('#'+str(number))
    pattern = r'\b(?:fix(?:es|ed)?|close(?:s|d)?|resolve(?:s|d)?)\s+(?:'+ '|'.join(references)+r')(?!\d)'
    for match in re.finditer(pattern,pr.get('body') or '',re.I):
        prefix = (pr.get('body') or '')[max(0,match.start()-100):match.start()]
        if not re.search(r'(?:does\s+not|do\s+not|not|never|without|won.t)\s*$',prefix,re.I):
            return True
    return False


def checked_ci(pr,checked_at):
    commits = pr['commits']['nodes']
    rollup = commits[0]['commit']['statusCheckRollup'] if commits else None
    latest = {}
    for check in rollup['contexts']['nodes'] if rollup else []:
        if check['__typename'] == 'CheckRun':
            suite = check.get('checkSuite') or {}
            key = ('run',(suite.get('app') or {}).get('id'),((suite.get('workflowRun') or {}).get('workflow') or {}).get('databaseId'),check['name'])
            timestamp = check.get('startedAt') or check.get('completedAt') or ''
        else:
            key = ('context',check['context'])
            timestamp = check.get('createdAt') or ''
        if key not in latest or timestamp >= latest[key][0]:
            latest[key] = (timestamp,check)
    failures, pending, cancelled, names = [],False,False,[]
    for _,check in latest.values():
        name = check.get('name') or check.get('context');names.append(name)
        if check['__typename'] == 'CheckRun':
            if check['status'] != 'COMPLETED':
                pending = True
            elif check['conclusion'] in ['FAILURE','TIMED_OUT','ACTION_REQUIRED','STALE']:
                failures.append(name)
            elif check['conclusion'] == 'CANCELLED':
                cancelled = True
        else:
            if check['state'] in ['FAILURE','ERROR']:
                failures.append(name)
            elif check['state'] in ['PENDING','EXPECTED']:
                pending = True
    state = 'FAILURE' if failures else 'PENDING' if pending else 'CANCELLED' if cancelled else 'SUCCESS' if latest else None
    metadata_names = ['validate pr description','cleanup-on-approval','agentcanvas-status-sync','label','claude','review','copilot']
    metadata_only = bool(names) and all(any(token in name.lower() for token in metadata_names) for name in names)
    result = {'state':state,'github_rollup':rollup['state'] if rollup else None,'head_sha':pr['headRefOid'],'failed':sorted(set(failures)),'checked_at':checked_at,'metadata_only':metadata_only}
    result['latest_checks'] = [
        {'name':check.get('name') or check.get('context'),
         'state':check.get('conclusion') if check['__typename']=='CheckRun' else check['state'],
         'status':check.get('status'), 'time':timestamp,
         'workflow_id':(((check.get('checkSuite') or {}).get('workflowRun') or {}).get('workflow') or {}).get('databaseId'),
         'app':((check.get('checkSuite') or {}).get('app') or {}).get('slug')}
        for timestamp,check in latest.values()]
    if failures and all(name == 'Validate PR description' for name in failures):
        result['detail'] = 'PR-description validation.'
    return result


def refresh_descriptive_states(data):
    """Keep reported behavior and original evidence separate from changing state."""
    edited = []
    summaries = {
        17915:'The Stop and Delete confirmation buttons passed the wrong prop name, so their intended test IDs never reached the DOM. PR #18151 restores those selectors.',
        17926:'Typing and leaving a conversation within 500 ms could restore an older draft and lose the latest text. PR #17968 flushes the pending draft before navigation while keeping conversations’ drafts separate.',
        17938:'Entering an existing LLM or agent profile name silently disabled Save with no explanation. PR #18144 shows a duplicate-name message and marks the field invalid while keeping Save disabled.',
        17957:'Escape behaved incorrectly when the skill detail’s +N tag control had focus. PR #17967 gives the popover its own dismissal step, keeping the detail dialog open until the next Escape.',
        17958:'A malformed MCP authentication header produced an environment-variable error. PR #17966 names the actual field: “Headers must follow KEY=value format.”',
        18060:'Opening an agent profile’s menu from the keyboard left focus on its trigger, and arrow navigation got stuck at a disabled item. PR #18112 focuses the first enabled action and returns focus to the trigger when the menu closes.',
        18061:'Switching an automation through Prompt/Plugin, or choosing Default, could leave its Agent profile field blank. PR #18111 normalizes the empty value so “Default” is shown and checked.',
        18206:'An agent hook carrying both fields displayed prompt instead of the system_prompt it actually used. PR #18215 selects the displayed text by hook type.',
    }
    neutral_notes = {
        17915:'PR #18151 is the selected fix. Earlier PR #17983 closed without merging; #18140 is an alternative fix.',
        17926:'PR #17968 is the selected fix; #18096 is an alternative fix.',
        18061:'PR #18111 is the selected fix; the screenshots are from that PR. #18187 is an alternative fix.',
        18173:'PR #18175 is the selected fix; #18217 is an alternative proposal.',
        18195:'PR #18219 is the selected fix and includes the original real-server before/after captures; #18216 closed without merging and #18220 is an alternative proposal.',
        18193:'A usability finding reproduced through verify-openhands; this is a navigation improvement rather than a regression report.',
    }
    for row in data['issues']:
        visual = row['visual']
        if not visual.get('primary_pr') and row['prs']:
            selected = next((p for p in row['prs'] if p['state']=='MERGED'),row['prs'][0])
            visual['primary_pr'] = {key:selected[key] for key in ['repo','number','title','url','state','is_draft']}
        primary = visual.get('primary_pr')
        if row['repo']=='OpenHands/OpenHands':
            number = row['number']
            if number in summaries:
                visual['summary'] = summaries[number]
            if number in neutral_notes:
                row['note'] = neutral_notes[number]
            if number == 17915:
                visual['evidence_note'] = 'This is a nonvisual DOM-attribute fix. PR #18151 reports five passing component tests; its image attachment returned 404 when the original evidence was collected. Alternative PR #18140 supplied no screenshots. Earlier PR #17983 closed without merging.'
            if number == 17957:
                visual['evidence_note'] = 'Original PR screenshots from a local mock run. These captures remain the original branch evidence.'
            if number == 18061:
                visual['evidence_note'] = 'Original before/after screenshots from PR #18111. Alternative PR #18187 reuses the original issue screenshot.'
            if number == 18178:
                row['note'] = 'The before evidence is a container log; the after screenshot is the original capture from the locally tested PR branch. The current PR state is shown in the ledger.'
        if primary:
            # Avoid repeating a mutable status in the behavior description.
            text = visual.get('summary','')
            patterns = [r'\bThe open community PR\b',r'\bAn open community PR\b',r'\bThe open draft PR\b',r'\bThe open PR\b',r'\bThe draft fix\b',r'\bThe open fix\b',r'\bThe open proposal\b']
            for pattern in patterns:
                text = re.sub(pattern,'PR #'+str(primary['number']),text,flags=re.I)
            visual['summary'] = text
        if row['repo']=='OpenHands/software-agent-sdk':
            if row['number']==5496:
                visual['evidence_note'] = 'PR #5690 is now identified; no before-and-after visual evidence was retained in the original collection. The issue remains open.'
            if row['number']==5497:
                visual['evidence_note'] = 'The related proposals offer read-side resolution or write-side updates. Neither PR includes a before-and-after image pair; their current states are shown in the ledger.'
            if row['cohort']=='agent-server':
                visual['evidence_note'] = visual.get('evidence_note','').replace('The verification map is draft PR #5621.','The verification map is PR #5621; its current state is recorded in the downloadable data.')
        for pr in row['prs']:
            if pr['repo']=='OpenHands/software-agent-sdk' and pr['number']==5694 and row['number']==5643:
                pr['relation'] = 'partial'
                row['note'] = 'PR #5694 rejects new empty MCP configurations, but leaves persisted-settings migration and isolation of valid servers from an invalid sibling unresolved.'
            if pr['repo']=='OpenHands/software-agent-sdk' and pr['number']==5690 and row['number']==5496:
                pr['relation'] = 'partial'
                row['note'] = 'PR #5690 locks metadata updates, but installation still swaps the directory outside that lock; concurrent listing can prune the entry and lose its enabled state.'
        edited.append(row['repo']+'#'+str(row['number']))
    data['scope'] = data['scope'].replace('from draft map PR #5621','from feature map PR #5621')
    return edited


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checked-at',help='Common report snapshot timestamp; actual fetch interval is also recorded.')
    parser.add_argument('--audit-output',default='/workspace/verify-openhands-refresh-summary.json')
    parser.add_argument('--cache-output',default='/workspace/verify-openhands-refresh-api.json')
    parser.add_argument('--pr-discovery-cache',help='Optional complete OpenHands open/recent-closed PR index from the companion report refresh.')
    args = parser.parse_args()
    path = ROOT/'assets/verify-openhands/issues.json'
    before = json.loads(path.read_text());data = copy.deepcopy(before)
    started = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
    checked_at = args.checked_at or started
    issue_keys = {(r['repo'],r['number']) for r in data['issues']}
    pr_keys = {(p['repo'],p['number']) for r in data['issues'] for p in r['prs']}
    map_key = (data['agent_server_map']['repo'],data['agent_server_map']['number'])
    issues = fetch_objects(issue_keys,'issue')
    print('Fetched every tracked issue:',len(issues),flush=True)
    discovered = discover_prs(before['checked_at'],args.pr_discovery_cache)
    added = []
    for row in data['issues']:
        issue = issues[(row['repo'],row['number'])]
        known = {(p['repo'],p['number']) for p in row['prs']}
        candidates = dict(discovered)
        closing = set()
        for event in issue['timelineItems']['nodes']:
            source = event.get('closer') or event.get('source')
            if source and source.get('__typename','PullRequest') == 'PullRequest':
                key = (source['repository']['nameWithOwner'],source['number']);candidates[key] = source
                if event['__typename'] == 'ClosedEvent':
                    closing.add(key)
        for key,pr in candidates.items():
            if key in known or key == map_key or key[0] not in REPOSITORIES:
                continue
            if key not in closing and not explicitly_fixes(pr,row['repo'],row['number']):
                continue
            row['prs'].append({'repo':key[0],'number':key[1],'title':pr['title'],'url':pr['url'],'relation':'fix'})
            known.add(key);pr_keys.add(key)
            added.append({'issue':row['repo']+'#'+str(row['number']),'pr':key[0]+'#'+str(key[1]),'evidence':'closing event' if key in closing else 'explicit closing reference'})
    prs = fetch_objects(pr_keys|{map_key},'pullRequest')
    print('Fetched all current PR states and paginated checks:',len(prs),flush=True)
    issue_changes,pr_changes = [],[]
    for row in data['issues']:
        issue = issues[(row['repo'],row['number'])]
        old_state = row['issue_state']
        row.update(title=issue['title'],url=issue['url'],issue_state=issue['state'],state_reason=issue['stateReason'],checked_at=checked_at,closed_at=issue['closedAt'])
        if old_state != row['issue_state']:
            issue_changes.append({'issue':row['repo']+'#'+str(row['number']),'before':old_state,'after':row['issue_state']})
        for target in row['prs']:
            pr = prs[(target['repo'],target['number'])]
            old_state = target.get('state')
            target.update(title=pr['title'],url=pr['url'],state=pr['state'],is_draft=pr['isDraft'],merged_at=pr['mergedAt'],ci=checked_ci(pr,checked_at))
            if old_state != target['state']:
                pr_changes.append({'pr':target['repo']+'#'+str(target['number']),'before':old_state,'after':target['state']})
        primary = row['visual'].get('primary_pr')
        if primary:
            pr = prs[(primary['repo'],primary['number'])]
            primary.update(title=pr['title'],url=pr['url'],state=pr['state'],is_draft=pr['isDraft'])
    map_pr = prs[map_key]
    data['agent_server_map'].update(title=map_pr['title'],state=map_pr['state'],is_draft=map_pr['isDraft'],merged_at=map_pr['mergedAt'],ci=checked_ci(map_pr,checked_at))
    refresh_descriptive_states(data)
    finished = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
    data['checked_at'] = checked_at
    data['refresh'] = {'metadata_fetch_started_at':started,'metadata_fetch_finished_at':finished,'tracked_cohort_preserved':len(data['issues']),'discovery':'All open PRs and closed/merged PRs updated since the prior snapshot in all three repositories, plus full tracked issue reference and closure timelines. New matches require an explicit fixing/closing reference or closing event. Original evidence retained; no browser verification rerun.'}
    unique = {(p['repo'],p['number']):p for r in data['issues'] for p in r['prs']}
    counts = {'issues':len(data['issues']),'distinct_prs':len(unique),'merged_prs':sum(p['state']=='MERGED' for p in unique.values()),'open_prs':sum(p['state']=='OPEN' for p in unique.values()),'closed_unmerged_prs':sum(p['state']=='CLOSED' for p in unique.values()),'open_prs_failing_checks':sum(p['state']=='OPEN' and p['ci']['state']=='FAILURE' for p in unique.values()),'open_issues':sum(r['issue_state']=='OPEN' for r in data['issues'])}
    summary = {'checked_at':checked_at,'fetch_started_at':started,'fetch_finished_at':finished,'counts':counts,'issue_state_changes':issue_changes,'pr_state_changes':list({x['pr']:x for x in pr_changes}.values()),'new_matches':added,'missing_data':[],'cohort_and_original_evidence_preserved':True,'prose_review_required':True}
    # Public GitHub metadata only; credentials are never stored in either file.
    Path(args.cache_output).write_text(json.dumps({'issues':list(issues.values()),'prs':list(prs.values()),'discovered_prs':list(discovered.values())},indent=2)+'\n')
    Path(args.audit_output).write_text(json.dumps(summary,indent=2)+'\n')
    temporary = path.with_suffix('.json.tmp');temporary.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');temporary.replace(path)
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
