#!/usr/bin/env python3
"""Check fleet snapshot refresh, status precedence, and generated PR links."""
import copy
from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parents[1]
RENDER = runpy.run_path(str(ROOT / 'scripts/build-agent-server-fleet.py'))
spec = importlib.util.spec_from_file_location('refresh', ROOT / 'scripts/refresh-agent-server-fleet.py')
REFRESH = importlib.util.module_from_spec(spec)
spec.loader.exec_module(REFRESH)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pr_links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href', '').startswith('https://github.com/OpenHands/software-agent-sdk/pull/'):
            self.pr_links.append(attrs)


class FleetTests(unittest.TestCase):
    def test_six_statuses_and_precedence(self):
        cases = [
            ('MERGED', True, 'CHANGES_REQUESTED', 'merged'),
            ('CLOSED', True, 'APPROVED', 'closed'),
            ('OPEN', True, 'APPROVED', 'draft'),
            ('OPEN', True, 'CHANGES_REQUESTED', 'draft'),
            ('OPEN', False, 'CHANGES_REQUESTED', 'changes-requested'),
            ('OPEN', False, 'APPROVED', 'approved'),
            ('OPEN', False, 'REVIEW_REQUIRED', 'open'),
            ('OPEN', False, '', 'open'),
        ]
        for state, draft, review, expected in cases:
            with self.subTest(state=state, draft=draft, review=review):
                self.assertEqual(RENDER['status_key'](dict(state=state, is_draft=draft, review_decision=review)), expected)

    def test_every_badge_has_an_icon_and_text(self):
        for key, (label, _) in RENDER['STATUSES'].items():
            badge = RENDER['badge'](key)
            self.assertIn('<svg ', badge)
            self.assertIn('aria-hidden="true"', badge)
            self.assertIn(label, badge)

    def test_all_pr_links_open_safely_in_new_tabs(self):
        parser = Links()
        parser.feed((ROOT / 'arch/agent-server-fleet.html').read_text())
        self.assertEqual(len(parser.pr_links), len(RENDER['PRS']) * 2)
        for attrs in parser.pr_links:
            self.assertEqual(attrs.get('target'), '_blank')
            self.assertEqual(set(attrs['rel'].split()), {'noopener', 'noreferrer'})
            self.assertIn('opens in a new tab', attrs['aria-label'])

    def sample(self):
        return {'prs': [{'number': 1, 'summary': 'Keep this summary.'}]}

    def live(self):
        return dict(number=1, headRefName='claude/umbrella-bug-fixes-test', title='Fix', url='https://example.com',
                    state='MERGED', isDraft=False, reviewDecision='APPROVED', mergedAt='now', closedAt='now', updatedAt='now')

    def test_refresh_retains_merged_and_closed_rows_and_summary(self):
        for state in ['MERGED', 'CLOSED']:
            live = self.live() | {'state': state}
            result = REFRESH.refresh(self.sample(), [live], 'now')
            self.assertEqual(len(result['prs']), 1)
            self.assertEqual(result['prs'][0]['state'], state)
            self.assertEqual(result['prs'][0]['summary'], 'Keep this summary.')
            self.assertEqual(result['observed_at'], 'now')

    def test_missing_or_new_pr_stops_before_snapshot_mutation(self):
        for fetched in [[], [self.live(), self.live() | {'number': 2}]]:
            original = self.sample()
            snapshot = copy.deepcopy(original)
            with self.assertRaises(ValueError):
                REFRESH.refresh(snapshot, fetched, 'now')
            self.assertEqual(snapshot, original)


if __name__ == '__main__':
    unittest.main()
