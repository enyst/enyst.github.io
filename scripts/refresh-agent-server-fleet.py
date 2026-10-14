#!/usr/bin/env python3
"""Refresh fleet PR metadata from GitHub without dropping merged or closed fixes.

Hand-written summaries live in snapshot.json. If a new fleet PR needs a summary,
stop without writing the snapshot and list its number for the editor.
"""
from datetime import datetime, timezone
import json
import re
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'assets/agent-server-fleet/snapshot.json'


def has_decision_section(body):
    # Only a Markdown heading counts, not prose mentioning another section.
    body = re.sub(r"^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*$", "", body, flags=re.M | re.S)
    return bool(re.search(r"^ {0,3}#{1,6}[ \t]+(?:\*\*)?Decision needed(?:\*\*)?[ \t]*(?:[:—–-][^\n]*)?(?:[ \t]+#+)?[ \t]*$", body, flags=re.M | re.I))


def refresh(snapshot, fetched, observed_at):
    known = {pr['number'] for pr in snapshot['prs']}
    by_number = {pr['number']: pr for pr in fetched}
    fleet = {pr['number'] for pr in fetched if pr['headRefName'].startswith('claude/umbrella-bug-fixes-')}
    if missing := known - by_number.keys():
        raise ValueError(f'Incomplete GitHub results; missing PRs: {sorted(missing)}')
    if new := fleet - known:
        raise ValueError(f'Add summaries for new fleet PRs before refreshing: {sorted(new)}')
    for pr in snapshot['prs']:
        live = by_number[pr['number']]
        pr.update(title=live['title'], url=live['url'], state=live['state'],
                  is_draft=live['isDraft'], review_decision=live['reviewDecision'],
                  merged_at=live['mergedAt'], closed_at=live['closedAt'], updated_at=live['updatedAt'],
                  decision_needed=has_decision_section(live['body']))
    snapshot['observed_at'] = observed_at
    snapshot['scope'] = ('PRs authored by enyst with a head branch starting '
                         'claude/umbrella-bug-fixes-, including merged and closed PRs.')
    return snapshot


def main():
    fetched = json.loads(subprocess.check_output([
        'gh', 'pr', 'list', '--repo', 'OpenHands/software-agent-sdk', '--author', 'enyst',
        '--state', 'all', '--limit', '1000', '--json',
        'number,title,url,headRefName,state,isDraft,reviewDecision,mergedAt,closedAt,updatedAt,body',
    ], text=True))
    if len(fetched) >= 1000:
        raise SystemExit('GitHub result limit reached; increase the limit before refreshing.')
    try:
        snapshot = refresh(json.loads(SNAPSHOT.read_text()), fetched,
                           datetime.now(timezone.utc).isoformat())
    except ValueError as error:
        raise SystemExit(str(error)) from error
    SNAPSHOT.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + '\n')
    print(f'Refreshed {len(snapshot["prs"])} PRs. Run scripts/build-agent-server-fleet.py next.')


if __name__ == '__main__':
    main()
