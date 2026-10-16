#!/usr/bin/env python3
"""Render a pinned Canvas feature map as human-readable mini scripts.

python3 scripts/build-openhands-scenarios.py --checkout /path/to/map-checkout \
    --date 2026-10-16 --source-label 'PR #18334' --source-pr 18334

This publishes a separate reading edition. It does not rewrite the older
October 9 family pages, run a verification, or infer passing results.
"""
import argparse
from collections import Counter
import hashlib
import html
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess

SITE = Path(__file__).resolve().parents[1]
MAP_DIR = '.agents/skills/verify-openhands/references/feature-map'
REPO = 'https://github.com/OpenHands/OpenHands'
FEATURE = r'F\d{2}\.[\w-]+'


def esc(value):
    return html.escape(str(value), quote=True)


def slug(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def git(checkout, *args):
    return subprocess.check_output(['git', '-C', str(checkout), *args], text=True).strip()


def bullets(text):
    """Top-level list items; retain indented prose, child lists, and fences."""
    starts = list(re.finditer(r'^- ', text, flags=re.M))
    return [text[m.end():starts[i+1].start() if i+1 < len(starts) else len(text)].strip()
            for i, m in enumerate(starts)]


def clean_title(label):
    label = re.sub(r'\s*\(([^()]*)\)', lambda m: '' if re.search(FEATURE, m[1])
                   and not re.sub(FEATURE+r'|[`\s,;/]|\band\b', '', m[1]) else m[0], label)
    return label.strip().rstrip('.')


def words(value):
    return value.replace('-', ' ').replace('_', ' ')


NAMES = {
    'backend-selector-settings-link': 'Settings', 'add-secret-button': 'Add secret',
    'add-secret-form': 'Add secret form', 'edit-secret-form': 'Edit secret form',
    'name-input': 'Name', 'value-input': 'Value', 'description-input': 'Description',
    'submit-button': 'Submit', 'cancel-button': 'Cancel', 'confirm-button': 'Confirm',
    'chat-input': 'Message', 'confirmation-modal': 'Confirmation dialog',
    'command-menu-trigger': 'Search commands', 'command-menu': 'Command menu',
    'conversation-name': 'Conversation name', 'ellipsis-button': 'More options',
    'back-to-secrets': 'Back to secrets', 'secret-item': 'Secret row',
}


def selector(value):
    """Readable labels, leaving the exact locator in the original recipe."""
    parts = []
    for part in value.split(' >> '):
        if part.startswith('testid='):
            name = part[7:]
            if name.startswith('sidebar-settings-'):
                label = words(name.split('/')[-1]).capitalize() + ' settings'
            else:
                label = NAMES.get(name, words(re.sub(r'-(button|input|link)$', '', name)).capitalize())
            parts.append('“'+label+'”')
        elif part.startswith('has-text='):
            parts.append('containing “'+part[9:]+'”')
        elif part.startswith(('text=', 'label=')):
            parts.append('“'+part.split('=', 1)[1]+'”')
        elif part.startswith('role='):
            match = re.search(r'name=(?:"([^"]+)"|/([^/]+)/)', part)
            parts.append('“'+(match[1] or match[2])+'”' if match else 'the '+part[5:].split('[')[0])
        elif part.startswith('nth='):
            parts.append('match '+str(int(part[4:])+1) if part[4:].isdigit() else part)
        elif 'xpath=' in part:
            parts.append('its containing control')
        else:
            return 'the element identified in the CLI recipe'
    return ' / '.join(parts)


def describe_command(command):
    """Translate documented verbs; never invent selector-dependent actions."""
    normalized = re.sub(r'^control-openhands\s+', '', command.strip())
    try:
        args = shlex.split(normalized)
    except ValueError:
        return 'Do', 'Follow the quoted command in the exact recipe.'
    if not args:
        return 'Do', 'Follow the exact recipe.'
    verb = args[0]
    if verb == 'browser' and len(args) > 1:
        action = args[1]
        rest = args[2:]
        target = selector(rest[0]) if rest else 'the current page'
        if action == 'goto':
            return 'Do', 'Open '+(rest[0] if rest else 'the URL in the recipe')+'.'
        if action in ('click', 'hover', 'dblclick'):
            return 'Do', {'click':'Choose ', 'hover':'Hover over ', 'dblclick':'Double-click '}[action]+target+'.'
        if action in ('fill', 'type'):
            value = rest[1] if len(rest) > 1 and not rest[1].startswith('--') else 'the value specified in the recipe'
            return 'Do', 'Enter “'+value+'” in '+target+'.'
        if action == 'press':
            return 'Do', 'Press '+(' then '.join(rest) or 'the key in the recipe')+'.'
        if action == 'viewport':
            return 'Setup', 'Use the '+(' '.join(rest) or 'specified')+' viewport.'
        if action in ('reload', 'back', 'forward', 'reset'):
            return 'Do', {'reload':'Reload the page.', 'back':'Go back in browser history.',
                          'forward':'Go forward in browser history.', 'reset':'Start with a fresh browser profile.'}[action]
        if action in ('wait', 'wait-url', 'wait-text', 'wait-tab'):
            suffix = ' to disappear' if any(x in rest for x in ('hidden','detached')) else ' to appear'
            return 'Wait', 'Wait for '+target+suffix+'.'
        if action == 'choose' and len(rest) > 1:
            return 'Do', 'Choose “'+rest[1]+'” in '+target+'.'
        if action == 'screenshot':
            return 'Record', 'Capture the visible state as evidence.'
        if action in ('eval', 'attr', 'bbox'):
            return 'Check', {'eval':'Inspect the live page state described in the recipe.',
                             'attr':'Read the specified attribute of '+target+'.',
                             'bbox':'Check that '+target+' fits its viewport.'}[action]
        if action in ('snapshot', 'testids', 'text', 'count', 'value', 'enabled', 'visible'):
            return 'Check', {'snapshot':'Read the accessible page or dialog.', 'testids':'Find the available UI controls.',
                             'text':'Read the text of '+target+'.', 'count':'Count '+target+'.',
                             'value':'Read the value of '+target+'.', 'enabled':'Check whether '+target+' is enabled.',
                             'visible':'Check whether '+target+' is visible.'}[action]
        if action in ('errors', 'toasts', 'network', 'events', 'downloads', 'clipboard', 'media', 'url'):
            return 'Check', {'errors':'Check the browser errors.', 'toasts':'Read the notifications.',
                             'network':'Inspect the real network requests.', 'events':'Read the browser event log.',
                             'downloads':'Inspect the downloaded file.', 'clipboard':'Read the copied content.',
                             'media':'Check sound or media playback.', 'url':'Check the current URL.'}[action]
        if action in ('upload-via', 'drop-files', 'paste'):
            return 'Do', 'Provide the fixture file or pasted content using '+target+'.'
        if action == 'scroll':
            return 'Do', 'Scroll '+target+' as specified in the recipe.'
        return 'Do', 'Use browser '+words(action)+' as specified in the exact recipe.'
    if verb == 'conversation' and len(args) > 1:
        action = args[1]
        if action in ('start', 'send'):
            prompt = args[args.index('--prompt')+1] if '--prompt' in args and args.index('--prompt')+1 < len(args) else None
            text = 'Start a conversation' if action == 'start' else 'Send a follow-up'
            return 'Do', text+(' with the prompt “'+prompt+'”.' if prompt else ' as specified in the recipe.')
        return ('Wait' if action == 'wait' else 'Check' if action in ('events','status','list') else 'Do',
                {'wait':'Wait for the conversation to finish.', 'events':'Read the actual conversation events.',
                 'status':'Check the conversation status.', 'list':'Read the conversation list.',
                 'pause':'Pause the conversation.'}.get(action, 'Use conversation '+words(action)+' as specified.'))
    if verb == 'fixture':
        return 'Setup', 'Create the disposable '+words(args[1] if len(args)>1 else '')+' fixture specified in the recipe.'
    if verb == 'llm':
        return 'Setup', 'Configure or inspect the model profiles specified in the recipe.'
    if verb == 'api':
        method = args[1] if len(args)>1 else 'GET'
        return ('Check' if method == 'GET' else 'Setup',
                'Read the backend state through the API.' if method == 'GET' else 'Arrange the prerequisite backend state through the API.')
    if verb == 'doctor':
        return 'Check', 'Confirm that the isolated stack is healthy.'
    if verb == 'service':
        return 'Setup', 'Change the run-owned service state: '+' '.join(args[1:])+'.'
    if verb in ('launch','stop','restart','onboard','workspace','assert'):
        return 'Do', {'launch':'Launch an isolated stack.', 'stop':'Stop the run-owned stack.',
                      'restart':'Restart the run-owned stack as specified.', 'onboard':'Follow the onboarding setup in the recipe.',
                      'workspace':'Open the fixture workspace.', 'assert':'Check the stated assertion against live output.'}[verb]
    return 'Setup', 'Follow the environment or fixture command in the exact recipe.'


def states(text):
    result = []
    if re.search(r'known failure', text, re.I):
        result.append('failure')
    if re.search(r'known issue', text, re.I):
        result.append('issue')
    if re.search(r'(?:\bBlocked(?: here| locally)?\s*[:.(]|\(blocked\)|\bblocked without\b|\bblocked here\b|\bLive prerequisite:)', text, re.I):
        result.append('blocked')
    if re.search(r'\bnot-run\b|\bnot run(?: here| locally|:)', text, re.I):
        result.append('not-run')
    return result or ['mapped']


LABELS = {'failure':'Known failure', 'issue':'Known issue', 'blocked':'Blocked',
          'not-run':'Not run', 'mapped':'Mapped behavior', 'contract':'Behavior contract', 'support':'Support step'}


class Edition:
    def __init__(self, checkout, date, label, pr):
        self.checkout, self.date, self.label, self.pr = checkout, date, label, pr
        self.revision = git(checkout, 'rev-parse', 'HEAD')
        spec = importlib.util.spec_from_file_location('feature_publisher', SITE/'scripts/build-openhands-features.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.renderer = module.Publisher(checkout)
        original_href = self.renderer.href
        self.renderer.href = lambda value: ('scenarios-'+value[:3]+'.html#'+value[:3] if re.fullmatch(r'F\d{2}[^/]*\.md(?:#.*)?',value)
                                            else original_href(value))
        self.families, self.features, self.anchors = [], {}, set()
        self.versions = json.loads((checkout/'config/defaults.json').read_text())['versions']

    def source(self, filename, line=None):
        return f'{REPO}/blob/{self.revision}/{MAP_DIR}/{filename}'+(f'#L{line}' if line else '')

    def read(self):
        for path in sorted((self.checkout/MAP_DIR).glob('F*.md')):
            raw = path.read_text()
            split = re.split(r'^## (.+)$', raw, flags=re.M)
            if split[1::2] != ['Sub-features','How to get to it (user POV)','Driving it with control-openhands','Gotchas']:
                raise ValueError(f'Unexpected sections in {path.name}')
            fid, title = raw.splitlines()[0][2:].split(' — ',1)
            overview = split[0].split('\n',1)[1].rsplit('\nSource:',1)[0].strip()
            features = []
            for item in bullets(split[2]):
                match = re.fullmatch(r'`('+FEATURE+r')`:\s*(.*)', item, flags=re.S)
                if not match:
                    raise ValueError(f'Unparsed behavior: {item[:100]}')
                feature = {'id':match[1], 'description':re.sub(r'\s*\n\s*',' ',match[2])}
                if feature['id'] in self.features:
                    raise ValueError('Duplicate feature '+feature['id'])
                features.append(feature)
                self.features[feature['id']] = feature
                self.renderer.id_pages[feature['id']] = 'scenarios-'+fid+'.html'
            first = re.search(r'^- \*\*', split[6], re.M)
            if not first:
                raise ValueError(f'No recipes in {path.name}')
            family = {'id':fid,'title':title,'file':path.name,'sha256':hashlib.sha256(raw.encode()).hexdigest(),
                      'overview':overview,'entry':split[4].strip(),'given':split[6][:first.start()].strip(),
                      'gotchas':split[8].strip(),'features':features,'scenarios':[]}
            for index,item in enumerate(bullets(split[6][first.start():]),1):
                match = re.match(r'\*\*(.+?)\*\*\s*(.*)',item,re.S)
                label,body = (match[1],match[2]) if match else ('After each group',item)
                ids = list(dict.fromkeys(re.findall(FEATURE,label)))
                unknown = set(ids)-set(self.features)
                # Forward references are checked after every family is loaded.
                anchor = fid+'--'+slug(clean_title(label))
                if anchor in self.anchors:
                    anchor += '-'+str(index)
                self.anchors.add(anchor)
                family['scenarios'].append({'name':anchor,'title':clean_title(label),'ids':ids,'body':body,
                                            'raw':item,'source_line':raw[:raw.index('- '+item.splitlines()[0])].count('\n')+1})
            self.families.append(family)
        for family in self.families:
            covered = set()
            for scenario in family['scenarios']:
                if set(scenario['ids'])-set(self.features):
                    raise ValueError('Undeclared recipe IDs in '+scenario['name'])
                covered.update(scenario['ids'])
            for feature in family['features']:
                if feature['id'] not in covered:
                    family['scenarios'].append({'name':family['id']+'--contract-'+slug(feature['id']),
                      'title':words(feature['id'].split('.',1)[1]).capitalize(), 'ids':[feature['id']],
                      'body':'','raw':'','contract_only':True,'source_line':None})
            for scenario in family['scenarios']:
                notes = []
                for note in bullets(family['gotchas']):
                    note_ids = set(re.findall(FEATURE,note))
                    if note_ids.intersection(scenario['ids']) and re.search(r'known (?:issue|failure)',note,re.I):
                        notes.append(note)
                declared = [self.features[i]['description'] for i in scenario['ids']]
                scenario['expected'] = [re.split(r'\bKnown (?:failure|issue)\b',x,flags=re.I)[0].strip() for x in declared]
                scenario['notes'] = notes
                annotations=[]
                for text in [scenario['body']]+declared:
                    text=re.sub(r'(?ms)^\s*```[^\n]*\n.*?^\s*```\s*$','',text)
                    for match in re.finditer(r'\bKnown (?:failure|issue)\b.*?(?=\n\n|$)',text,re.I|re.S):
                        if match[0] not in annotations:annotations.append(match[0].strip())
                scenario['annotations']=annotations
                scenario['states'] = states(scenario['body']+'\n'+'\n'.join(declared+notes))
                if scenario.get('contract_only') and scenario['states']==['mapped']:
                    scenario['states']=['contract']
                elif not scenario['ids'] and scenario['states']==['mapped']:
                    scenario['states']=['support']

    def inline(self,text):
        parts=[]
        for kind,value in self.renderer.tokens(text):
            rendered=self.renderer.inline_tokens([(kind,value)])
            if kind=='text':
                rendered=re.sub(r'(?<![&\w/])#(\d+)\b',lambda m: '<a href="'+REPO+'/issues/'+m[1]+'">'+m[0]+'</a>',rendered)
            parts.append(rendered)
        return ''.join(parts)

    def fragment(self,text):
        """Render a trusted map fragment as escaped prose and literal fences."""
        result=[]
        parts=re.split(r'(?m)^\s*```([^\n]*)\n(.*?)^\s*```\s*$',text,flags=re.S)
        for index,part in enumerate(parts):
            if index%3==1:
                result.append('<p class="code-caption">'+esc(part)+'</p>')
            elif index%3==2:
                result.append('<pre><code>'+esc(part.rstrip('\n'))+'</code></pre>')
            else:
                blocks=[]
                for block in self.renderer.blocks(part):
                    blocks.append(block)
                    # Older publisher drops children attached to a paragraph.
                    # Keep those branch instructions in this reading edition.
                    if block['kind']=='paragraph' and block['children']:
                        blocks.extend({'kind':'bullet','text':child,'children':[]} for child in block['children'])
                result.append(self.renderer.block_html(blocks))
        return '\n'.join(result)

    def steps(self,body):
        body=re.sub(r'(?ms)^\s*```[^\n]*\n.*?^\s*```\s*$','',body)
        tokens=self.renderer.tokens(re.sub(r'\s*\n\s*',' ',body))
        rows=[]
        for kind,value in tokens:
            if kind=='code' and re.match(r'^(?:control-openhands |browser |conversation |api (?:GET|POST|PATCH|PUT|DELETE) |fixture |llm |service |workspace )',value):
                badge,description=describe_command(value)
                # Diagnostics belong to the precise replay. The mini script
                # shows the action path; its Expect block states the contract.
                if badge not in ('Check','Record'):rows.append((badge,esc(description)))
        if not rows:
            rows=[('Do',self.inline(body))]
        return rows

    def badges(self,values):
        return '<span class="markers">'+''.join('<span class="marker marker--'+s+'">'+LABELS[s]+'</span>' for s in values)+'</span>'

    def scenario_html(self,family,scenario,claimed):
        anchors=[]
        for fid in scenario['ids']:
            if fid not in claimed:
                anchors.append('<span class="feature-anchor" id="'+fid+'"></span>')
                claimed.add(fid)
        ids=' · '.join(scenario['ids']) or family['id']+' · setup / cleanup'
        expected=''.join('<p>'+self.inline(t)+'</p>' for t in scenario['expected'] if t)
        if not expected:
            expected='<p>Complete this support step before continuing to the next scenario.</p>'
        source_url=self.source(family['file'],scenario['source_line'])
        raw=scenario['body']+'\n'+'\n'.join(scenario['expected']+scenario['notes'])
        search=' '.join([family['id'],family['title'],scenario['title'],ids,raw])
        search=re.sub(r'\s+',' ',search).strip()
        page=''.join(anchors)+f'''<details class="scenario" id="{esc(scenario['name'])}" data-states="{esc(' '.join(scenario['states']))}" data-search="{esc(search)}">
<summary><span class="scenario-heading"><span class="scenario-title">{esc(scenario['title'])}</span><span class="scenario-ids">{esc(ids)}</span></span>{self.badges(scenario['states'])}</summary>
<div class="scenario-body"><p class="scenario-name">Scenario <code>{esc(scenario['name'])}</code> · <a href="#{esc(scenario['name'])}">Permalink</a> · <a href="{source_url}">Source</a></p>
<div class="script-part"><h4>Given</h4><p>Use <a href="#{family['id']}-setup">{esc(family['id'])}’s prerequisites</a> and the <a href="#before-you-start">common setup</a>. Follow the family’s order when a script uses an earlier fixture or says “as above”.</p></div>'''
        if scenario.get('contract_only'):
            page+='''<div class="script-part"><h4>Do</h4><p>This behavior has no separately named recipe in this snapshot. Use the family’s entry points and the contract below; the page does not invent a replay.</p></div>'''
        else:
            steps=self.steps(scenario['body'])
            page+='<div class="script-part"><h4>Do — reading outline</h4><ol class="human-steps">'
            page+=''.join('<li><span class="step-kind">'+badge+'</span><div>'+content+'</div></li>' for badge,content in steps)
            page+='</ol></div>'
        page+='<div class="script-part expect"><h4>Expect</h4>'+expected+'</div>'
        if scenario['annotations']:
            page+='<div class="script-part known-observation"><h4>Known bug observations</h4>'+''.join('<p>'+self.inline(t)+'</p>' for t in scenario['annotations'])+'</div>'
        if scenario['notes']:
            page+='<div class="script-part issue-notes"><h4>Linked known issues</h4>'+''.join('<p>'+self.inline(t)+'</p>' for t in scenario['notes'])+'</div>'
        if not scenario.get('contract_only'):
            page+='<details class="exact-recipe"><summary>Exact CLI recipe &amp; bug checks</summary><div class="original-recipe">'+self.fragment(scenario['body'])+'</div></details>'
        return page+'</div></details>\n'

    def write(self):
        behavior_count=len(self.features)
        all_scenarios=[s for f in self.families for s in f['scenarios']]
        recipe_count=sum(not s.get('contract_only') for s in all_scenarios)
        date_label=__import__('datetime').date.fromisoformat(self.date).strftime('%-d %B %Y')
        nav=''.join(f'<a href="scenarios.html#{f["id"]}"><span>{f["id"]}</span> {esc(f["title"])}</a>' for f in self.families)
        options=''.join(f'<option value="{f["id"]}">{f["id"]} · {esc(f["title"])}</option>' for f in self.families)
        page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Self-Healing OpenHands: the scenario guide — Engel’s notebook</title>
<meta name="description" content="The Agent Canvas feature map as named mini scripts: {behavior_count} behaviors across {len(self.families)} families, with prerequisites, expected results, known-bug markers and exact CLI recipes.">
<meta name="keywords" content="openhands-features, verification, Agent Canvas, feature map, scenarios">
<link rel="canonical" href="https://enyst.github.io/openhands-features/scenarios.html">
<meta property="og:title" content="OpenHands, one scenario at a time"><meta property="og:type" content="article"><meta property="og:url" content="https://enyst.github.io/openhands-features/scenarios.html">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;family=DM+Sans:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="../brand.css"><link rel="stylesheet" href="../assets/openhands-features/scenarios.css">
<script src="../assets/openhands-features/scenarios.js" defer></script></head><body>
<a class="skip" href="#content">Skip to scenarios</a>
<header class="masthead"><a class="notebook" href="../index.html">Engel’s notebook</a><nav aria-label="Breadcrumb"><a href="../verify/index.html">Self-Healing Codebase Project</a><span>/</span><a href="index.html" rel="tag">openhands-features</a></nav></header>
<main id="content" class="reading-shell"><header class="introduction">
<h1>OpenHands,<br><em>one scenario at a time.</em></h1>
<p class="lead">The OpenHands app map in the Self-Healing Codebase Project. Named mini scripts show what to set up, what to do, and what should happen.</p>
<p class="edition">{behavior_count} behavior IDs · {len(self.families)} families · {recipe_count} named recipes &amp; support steps<br>{date_label} · <a href="{REPO}/pull/{self.pr}">{esc(self.label)}</a> at <a href="{REPO}/commit/{self.revision}"><code>{self.revision[:8]}</code></a><br>Canvas {esc(self.versions['agentCanvas'])} · Agent Server {esc(self.versions['agentServer'])} · automation {esc(self.versions['automation'])}</p>
<p class="scope-note">This is the map at the revision above, including its open bug notes. It does not incorporate later changes on main or claim a fresh verification run. <a href="#before-you-start">Setup &amp; reading guide</a> · <a href="../assets/openhands-features/scenarios.json" download>Download the scenario inventory</a></p>
</header>
<section class="reading-key" aria-labelledby="reading-key"><details><summary id="reading-key">How to read the scripts &amp; bug markers</summary><dl><div><dt>Given</dt><dd>The starting state and prerequisites.</dd></div><div><dt>Do</dt><dd>Actions, followed by observations.</dd></div><div><dt>Expect</dt><dd>The intended application behavior.</dd></div></dl>
<p>Open a scenario to read its script. The reading outline highlights the action path; Expect gives the behavior to check. Open <strong>Exact CLI recipe &amp; bug checks</strong> for every instruction, diagnostic, selector, placeholder and executable <code>known-bug</code> block. Use that original recipe for a complete replay.</p>
<div class="legend"><p>{self.badges(['failure'])} A defect reproduced in the source map.</p><p>{self.badges(['issue','blocked'])} A reported issue or path awaiting its named prerequisites. A blocked check is not a reproduced failure.</p><p>{self.badges(['not-run'])} A check not exercised in the source map.</p><p>{self.badges(['mapped'])} An expected behavior; this marker does not mean it passed.</p></div><p>Markers describe the particular paths and notes inside a script. A script can exercise a local path and also record an issue blocked on Cloud prerequisites.</p></details></section>
<p class="example-link">Start with an example: <a href="scenarios-F14.html#F14--create">Create a secret</a> · <a href="scenarios-F14.html#F14--agent-requests-a-secret">A scenario with a known bug</a>.</p>
<div class="tools" hidden><div class="search-control"><label for="scenario-search">Find a scenario, behavior ID, or bug</label><input id="scenario-search" type="search" placeholder="Try secret, F14.create, or #18432" aria-controls="scenario-families"></div><div class="filter-control"><label for="family-filter">Feature family</label><select id="family-filter"><option value="all">All families</option>{options}</select></div><div class="filter-control"><label for="state-filter">Map marker</label><select id="state-filter"><option value="all">All markers</option><option value="failure">Known failure</option><option value="issue">Known issue</option><option value="blocked">Blocked</option><option value="not-run">Not run</option><option value="contract">Behavior contract only</option></select></div><button id="reset-filters" type="button">Reset</button><p id="result-count" role="status" aria-live="polite"></p></div>
<div class="catalog-layout"><aside class="family-nav"><details open><summary>Browse the map</summary><nav aria-label="Feature families">{nav}</nav></details></aside><div id="scenario-families"><p id="empty-results" hidden>No scenarios match. Try a different word, clear the marker filter, or reset.</p>
'''
        claimed=set()
        family_chunks=[]
        for family in self.families:
            start=len(page)
            note_states=states(family['gotchas'])
            page+=f'''<section class="family" id="{family['id']}" data-family="{family['id']}"><header class="family-header"><h2><span>{family['id']}</span> {esc(family['title'])}</h2><p>{len(family['features'])} behaviors · {len(family['scenarios'])} scripts &amp; contracts · <a href="{self.source(family['file'])}">Maintained source</a></p></header>
<details class="family-setup" id="{family['id']}-setup"><summary>Entry points &amp; prerequisites</summary><div><h3>What this family covers</h3>{self.fragment(family['overview'])}<h3>How a user gets here</h3>{self.fragment(family['entry'])}<h3>Given</h3>{self.fragment(family['given'])}</div></details>
<div class="scenario-list">'''
            for scenario in family['scenarios']:
                page+=self.scenario_html(family,scenario,claimed)
            page+=f'''</div><details class="family-notes" data-states="{esc(' '.join(note_states))}" data-search="{esc(family['gotchas'])}"><summary>Family notes, prerequisites for known issues &amp; limits {self.badges([s for s in note_states if s!='mapped'])}</summary><div>{self.fragment(family['gotchas'])}</div></details></section>\n'''
            family_chunks.append(page[start:])
        if claimed!=set(self.features):
            raise ValueError('Feature anchors missing: '+str(set(self.features)-claimed))
        page+=f'''</div></div><section id="before-you-start" class="run-guide"><h2>Before you start</h2><p>Use an OpenHands checkout at the source revision, with Node 24+, installed npm dependencies, <code>uv</code> / <code>uvx</code>, and a supported Chromium browser. <a href="{REPO}/blob/{self.revision}/.agents/skills/verify-openhands/SKILL.md">The verification skill</a> is the complete setup contract.</p>
<pre><code>export PATH="$PWD/.agents/skills/verify-openhands/scripts:$PATH"
export OH_VERIFY_RUN=$(control-openhands launch --new --print-run)
control-openhands doctor
control-openhands onboard --skip
# Configure a model only for a scenario that needs one:
control-openhands llm preset deepseek
# When the run is complete:
control-openhands stop</code></pre>
<p>F01 walks onboarding instead of skipping it. No-model checks run before model configuration. Keep <code>OH_VERIFY_RUN</code> set so commands address your own run. Desktop is 1440 × 1000; phone is 390 × 844. Model-backed checks need the configured provider key and budget.</p>
<p>Recipes run in source order within each family and can share fixtures. The page preserves that order; “as above” is a dependency on an earlier case. Setup commands and API writes arrange state. They do not prove a UI path. Follow the family cleanup steps.</p>
<p>A known failure preserves the intended expectation beside the observed defect. Executable <code>known-bug</code> blocks use <code>xfail</code> for a reproduced symptom and <code>xpass</code> when it stops reproducing. Cloud accounts, enterprise capabilities and other unavailable prerequisites remain explicit. “Not run” is different from “blocked”.</p>
<p>The maintained map describes application behavior at its pinned revision. Once a fix is verified in the application version under test, remove the obsolete failure note and keep the normal expectation. Dated evidence belongs in the backfill ledger.</p>
<p>Read the <a href="{self.source('README.md')}">full map index and coverage boundaries</a>, the <a href="../arch/control-openhands-cli.html">CLI guide</a>, or the <a href="index.html">earlier illustrated edition</a>. The verification approach adapts Lauren Tan’s (<a href="https://github.com/poteto">@poteto</a>) pstack verification-skill generators; <a href="{REPO}/blob/{self.revision}/.agents/skills/verify-openhands/references/adaptation.md">attribution and adaptation</a>.</p></section>
<footer>Engel’s Code Design Notebook · <a href="../verify/index.html">OpenHands verification</a> · <a href="index.html">openhands-features</a></footer></main></body></html>\n'''
        self.validate(page)
        # Keep all content static, but avoid making a browser mount 85,000 DOM
        # elements just to read one script. The index contains every named case;
        # each family page owns its readable scripts and literal source.
        prefix=page[:page.index('<div class="catalog-layout">')]
        suffix=page[page.index('</div></div><section id="before-you-start"'):]
        layout='<div class="catalog-layout"><aside class="family-nav"><details open><summary>Browse the map</summary><nav aria-label="Feature families">'+nav+'</nav></details></aside><div id="scenario-families"><p id="empty-results" hidden>No scenarios match. Try a different word or reset.</p>'
        index=prefix+layout
        for family in self.families:
            index+=f'<section class="family" id="{family["id"]}" data-family="{family["id"]}"><header class="family-header"><h2><span>{family["id"]}</span> {esc(family["title"])}</h2><p>{len(family["features"])} behaviors · <a href="scenarios-{family["id"]}.html">Read this family’s scripts</a></p></header><ul class="scenario-index">'
            for scenario in family['scenarios']:
                ids=' · '.join(scenario['ids']) or family['id']+' · setup / cleanup'
                search=' '.join([family['id'],family['title'],scenario['title'],ids,scenario['body']]+scenario['expected']+scenario['notes'])
                search=re.sub(r'\s+',' ',search).strip()
                index+=f'<li class="scenario" data-search="{esc(search)}" data-states="{esc(" ".join(scenario["states"]))}"><a href="scenarios-{family["id"]}.html#{scenario["name"]}"><span class="scenario-heading"><span class="scenario-title">{esc(scenario["title"])}</span><span class="scenario-ids">{esc(ids)}</span></span>{self.badges(scenario["states"])}</a></li>'
            note_states=states(family['gotchas'])
            index+=f'</ul><details class="family-notes" data-states="{esc(" ".join(note_states))}" data-search="{esc(family["gotchas"])}"><summary>Family notes &amp; prerequisites for known issues</summary><div>{self.fragment(family["gotchas"])}</div></details></section>'
        index+=suffix
        self.validate(index,[])
        (SITE/'openhands-features/scenarios.html').write_text(index)
        for family,chunk in zip(self.families,family_chunks):
            family_prefix=prefix.replace('<body>','<body data-view-family="'+family['id']+'">')
            family_prefix=family_prefix.replace('OpenHands,<br><em>one scenario at a time.</em>',esc(family['title']))
            family_prefix=family_prefix.replace('The OpenHands app map in the Self-Healing Codebase Project. Named mini scripts show what to set up, what to do, and what should happen.',f'{family["id"]} · {len(family["features"])} mapped behaviors in the Self-Healing Codebase Project. Follow the prerequisites, actions and expected results; expand the original CLI recipe to replay it.')
            family_prefix=family_prefix.replace('Self-Healing OpenHands: the scenario guide — Engel’s notebook',esc(family['id']+' · '+family['title'])+' — Self-Healing OpenHands')
            family_prefix=family_prefix.replace('https://enyst.github.io/openhands-features/scenarios.html','https://enyst.github.io/openhands-features/scenarios-'+family['id']+'.html')
            # The full reading key is on the index; a direct family visit still
            # gets a concise explanation and the complete run guide below.
            key_start=family_prefix.index('<section class="reading-key"')
            key_end=family_prefix.index('<div class="tools"')
            family_prefix=family_prefix[:key_start]+'<p class="family-reading-note"><a href="scenarios.html">All scenarios &amp; marker key</a> · Open a script to read Given / Do / Expect. Expand the exact recipe for replayable commands.</p>'+family_prefix[key_end:]
            family_page=family_prefix+layout+chunk+suffix
            self.validate(family_page,[family])
            (SITE/('openhands-features/scenarios-'+family['id']+'.html')).write_text(family_page)
        data={'published_snapshot':self.date,'source_repository':REPO,'source_revision':self.revision,
              'source_label':self.label,'source_pr':self.pr,'source_directory':MAP_DIR,'versions':self.versions,
              'family_count':len(self.families),'behavior_count':behavior_count,'named_recipe_count':recipe_count,
              'script_and_contract_count':len(all_scenarios),'families':self.families}
        (SITE/'assets/openhands-features/scenarios.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({k:v for k,v in data.items() if k!='families'},indent=2))

    def validate(self,page,families=None):
        class Check(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.ids=[];self.refs=[];self.codes=[];self.active=False;self.buffer=[];self.details=[];self.case_codes={}
            def handle_starttag(self,tag,attrs):
                attrs=dict(attrs)
                if 'id' in attrs:self.ids.append(attrs['id'])
                if attrs.get('href','').startswith('#'):self.refs.append(attrs['href'][1:])
                if tag=='details':self.details.append(attrs.get('id') if 'scenario' in attrs.get('class','').split() else None)
                if tag=='code':self.active=True;self.buffer=[]
            def handle_data(self,data):
                if self.active:self.buffer.append(data)
            def handle_endtag(self,tag):
                if tag=='code' and self.active:
                    value=''.join(self.buffer);self.codes.append(value);self.active=False
                    case=next((x for x in reversed(self.details) if x),None)
                    if case:self.case_codes.setdefault(case,[]).append(value)
                if tag=='details':self.details.pop()
        parser=Check();parser.feed(page)
        duplicates=[k for k,v in Counter(parser.ids).items() if v>1]
        if duplicates:raise ValueError('Duplicate HTML IDs: '+str(duplicates))
        missing=set(parser.refs)-set(parser.ids)
        if missing:raise ValueError('Broken fragment links: '+str(missing))
        for family in self.families if families is None else families:
            for scenario in family['scenarios']:
                expected_codes=[]
                for kind,value in self.renderer.tokens(re.sub(r'(?ms)^\s*```[^\n]*\n.*?^\s*```\s*$','',scenario['body'])):
                    if kind=='code':expected_codes.append(value)
                for block in re.findall(r'(?ms)^\s*```[^\n]*\n(.*?)^\s*```\s*$',scenario['body']):
                    expected_codes.append(block.rstrip('\n'))
                missing=Counter(expected_codes)-Counter(parser.case_codes.get(scenario['name'],[]))
                if missing:raise ValueError('Literal source lost in '+scenario['name']+': '+str(missing))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout',type=Path,required=True)
    parser.add_argument('--date',required=True)
    parser.add_argument('--source-label',required=True)
    parser.add_argument('--source-pr',type=int,required=True)
    args=parser.parse_args()
    checkout=args.checkout.resolve()
    if subprocess.run(['git','-C',str(checkout),'diff','--quiet','HEAD','--',MAP_DIR,'config/defaults.json']).returncode:
        raise SystemExit('The map and version pins must match the committed source revision.')
    edition=Edition(checkout,args.date,args.source_label,args.source_pr)
    edition.read();edition.write()


if __name__=='__main__':
    main()
