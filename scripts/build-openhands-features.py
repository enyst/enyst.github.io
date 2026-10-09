#!/usr/bin/env python3
"""Publish the pinned upstream feature map as static, readable HTML.

Usage: python scripts/build-openhands-features.py --checkout ../playground
No packages, remote API calls, or browser mocks are needed. Capture manifests
in assets/openhands-features/capture-*.json attach independently reviewed media.
"""
import argparse
from collections import Counter
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit

SITE = Path(__file__).resolve().parents[1]
SOURCE_DIR = '.agents/skills/verify-openhands/references/feature-map'
REPO = 'https://github.com/OpenHands/OpenHands'
DATE = '2026-10-09'
GROUPS = [
    ('starting-work', 'Starting work', [1, 2, 3, 4]),
    ('conversation-workspace', 'Conversation & workspace', [5, 6, 7, 8, 27]),
    ('settings', 'Settings & configuration', list(range(9, 17))),
    ('customization', 'Customization', list(range(17, 21))),
    ('automations', 'Automations', list(range(21, 25))),
    ('backends-runtimes', 'Backends & runtimes', [25, 26]),
]


def esc(value):
    return html.escape(str(value), quote=True)


def git(checkout, *args):
    return subprocess.check_output(['git', '-C', str(checkout), *args], text=True).strip()


def slug(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def recipe_title(value):
    """Remove only ID-only parentheses; keep blocked and other qualifiers."""
    def parenthesis(match):
        remainder = re.sub(r'`?F\d{2}\.[\w-]+`?', '', match[1])
        remainder = re.sub(r'[\s,;/]+|\band\b', '', remainder)
        return '' if not remainder else match[0]
    return re.sub(r'\s*\(([^()]*)\)', lambda m: (' '+parenthesis(m)).rstrip(), value).strip().rstrip('.')


class Publisher:
    def __init__(self, checkout):
        self.checkout = checkout
        self.revision = git(checkout, 'rev-parse', 'HEAD')
        self.families = []
        self.id_pages = {}
        self.capture_count = 0
        self.code_expected = []
        self.media = []
        self.source_types = {}
        for path in sorted((SITE / 'assets/openhands-features').glob('capture-*.json')):
            data = json.loads(path.read_text())
            self.media.extend(data if isinstance(data, list) else data.get('captures', []))

    def source_url(self, path, line=None):
        kind = 'tree' if self.source_type(path) == 'tree' else 'blob'
        url = f'{REPO}/{kind}/{self.revision}/{path}'
        return url + (f'#L{line}' if line else '')

    def source_type(self, path):
        if path not in self.source_types:
            result = subprocess.run(['git', '-C', str(self.checkout), 'cat-file', '-t', f'{self.revision}:{path}'], capture_output=True, text=True)
            self.source_types[path] = result.stdout.strip() if result.returncode == 0 else None
        return self.source_types[path]

    def href(self, value):
        if value.startswith(('https://', 'http://', '#', 'mailto:')):
            return value
        if re.fullmatch(r'F\d{2}[^/]*\.md(?:#.*)?', value):
            return value.split('#')[0].replace('.md', '.html') + ('#' + value.split('#', 1)[1] if '#' in value else '')
        if value.startswith(('src/', 'bin/', 'scripts/', 'config/', 'docker/', 'electron/', 'tests/', 'package.')):
            return self.source_url(value)
        # All other relative links in this source are contributor references.
        import posixpath
        return self.source_url(posixpath.normpath(posixpath.join(SOURCE_DIR, value)))

    def tokens(self, text):
        """Keep literal commands atomic, including double-delimited code spans."""
        # One upstream span uses single delimiters around a JSON filter that
        # itself contains backticks. Protect its literal contents, never edit it.
        text = text.replace('== `false` &&', '== \ue000false\ue000 &&')
        result = []
        start = 0
        while start < len(text):
            match = re.search(r'`+|\[[^\]\n]+\]\([^\s)]+\)', text[start:])
            if not match:
                result.append(('text', text[start:]))
                break
            left = start + match.start()
            if left > start:
                result.append(('text', text[start:left]))
            if match.group().startswith('['):
                result.append(('link', match.group()))
                start = start + match.end()
                continue
            delimiter = match.group()
            close = re.search(r'(?<!`)'+re.escape(delimiter)+r'(?!`)', text[left+len(delimiter):])
            if not close:
                result.append(('text', text[left:]))
                break
            right = left + len(delimiter) + close.start()
            value = text[left+len(delimiter):right].replace('\ue000', '`')
            result.append(('code', value))
            start = right + len(delimiter)
        return result

    def prose(self, text):
        # Escape raw markup before interpreting the source's small inline syntax.
        text = esc(text)
        text = re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', lambda m: f'<a href="{esc(self.href(html.unescape(m[2])))}">{m[1]}</a>', text)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
        return text

    def inline_tokens(self, tokens, link_features=True):
        rendered = []
        for kind, value in tokens:
            if kind == 'text':
                rendered.append(self.prose(value))
            elif kind == 'link':
                match = re.fullmatch(r'\[([^\]]+)\]\(([^\s)]+)\)', value)
                rendered.append(f'<a href="{esc(self.href(match[2]))}">{self.inline(match[1], link_features=False)}</a>')
            elif value in self.id_pages and link_features:
                rendered.append(f'<a class="feature-reference" href="{self.id_pages[value]}#{esc(value)}"><code>{esc(value)}</code></a>')
            elif value.startswith(('src/', 'config/', 'bin/', 'scripts/', 'docker/', 'electron/', 'tests/')) and ' ' not in value and self.source_type(value):
                rendered.append(f'<a href="{esc(self.source_url(value))}"><code>{esc(value)}</code></a>')
            else:
                rendered.append(f'<code>{esc(value)}</code>')
        return ''.join(rendered)

    def inline(self, value, link_features=True):
        return self.inline_tokens(self.tokens(value), link_features=link_features)

    @staticmethod
    def blocks(text):
        """Parse paragraphs and list items, preserving continuations and children."""
        result = []
        current = None
        for line in text.strip().splitlines():
            if not line.strip():
                if current:
                    result.append(current)
                    current = None
                continue
            if line.startswith('- '):
                if current:
                    result.append(current)
                current = {'kind': 'bullet', 'text': line[2:], 'children': []}
            elif line.startswith('  - ') and current:
                current['children'].append(line.strip()[2:])
            elif line.startswith('  ') and current:
                current['text'] += ' ' + line.strip()
            elif current and current['kind'] == 'paragraph':
                current['text'] += ' ' + line.strip()
            else:
                if current:
                    result.append(current)
                current = {'kind': 'paragraph', 'text': line.strip(), 'children': []}
        if current:
            result.append(current)
        return result

    def block_html(self, blocks):
        output, listing = [], False
        for block in blocks:
            if block['kind'] == 'bullet':
                if not listing:
                    output.append('<ul>')
                    listing = True
                children = '<ul>' + ''.join(f'<li>{self.inline(x)}</li>' for x in block['children']) + '</ul>' if block['children'] else ''
                output.append(f'<li>{self.inline(block["text"])}{children}</li>')
            else:
                if listing:
                    output.append('</ul>')
                    listing = False
                output.append(f'<p>{self.inline(block["text"])}</p>')
        if listing:
            output.append('</ul>')
        return '\n'.join(output)

    def read(self):
        for file in sorted((self.checkout / SOURCE_DIR).glob('F*.md')):
            raw = file.read_text()
            sections = re.split(r'^## (.+)$', raw, flags=re.M)
            if sections[1::2] != ['Sub-features', 'How to get to it (user POV)', 'Driving it with control-openhands', 'Gotchas']:
                raise ValueError(f'Unexpected feature-map structure: {file}')
            title = raw.splitlines()[0][2:]
            family_id = title.split(' — ')[0]
            overview = sections[0].split('\n', 1)[1].strip()
            overview, source = overview.rsplit('\nSource:', 1)
            behavior_blocks = self.blocks(sections[2])
            behaviors = []
            for block in behavior_blocks:
                if block['kind'] == 'paragraph':
                    continue
                match = re.match(r'`(F\d{2}\.[\w-]+)`:\s*(.*)', block['text'])
                if not match:
                    raise ValueError(f'Unexpected behavior declaration: {block}')
                behaviors.append({'id': match[1], 'description': match[2]})
                self.id_pages[match[1]] = file.with_suffix('.html').name
            drive = self.blocks(sections[6])
            split = next((i for i, b in enumerate(drive) if b['text'].startswith('**')), len(drive))
            # F01's first local-run heading belongs to the recipe section.
            if split and drive[split-1]['kind'] == 'paragraph' and drive[split-1]['text'] != 'Preconditions:':
                split -= 1
            family = {'id': family_id, 'number': int(family_id[1:]), 'title': title.split(' — ', 1)[1],
                      'file': file.name, 'page': file.with_suffix('.html').name,
                      'overview': overview.strip(), 'source': source.strip(), 'behaviors': behaviors, 'behavior_blocks': behavior_blocks,
                      'entry_points': self.blocks(sections[4]), 'preconditions': drive[:split],
                      'drive': drive[split:], 'gotchas': self.blocks(sections[8]),
                      'sha256': hashlib.sha256(raw.encode()).hexdigest(), 'recipes': []}
            recipe_number = 0
            for block in family['drive']:
                if block['kind'] == 'paragraph':
                    continue
                recipe_number += 1
                match = re.match(r'\*\*(.+?)\*\*\s*(.*)', block['text'])
                label, body = (match[1], match[2]) if match else ('After the family', block['text'])
                ids = re.findall(r'F\d{2}\.[\w-]+', label)
                family['recipes'].append({'anchor': f'recipe-{recipe_number:03}', 'label': label,
                                          'body': body, 'ids': ids, 'children': block['children']})
            self.families.append(family)
        declared = [x['id'] for f in self.families for x in f['behaviors']]
        if len(declared) != len(set(declared)):
            raise ValueError('Duplicate declared behavior IDs')

    def head(self, title, description, page):
        return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0f0f0e"><title>{esc(title)} — OpenHands features</title>
<meta name="description" content="{esc(description)}"><meta name="keywords" content="openhands-features, Agent Canvas, control-openhands, feature map">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="article"><meta property="og:url" content="https://enyst.github.io/openhands-features/{page}">
<link rel="canonical" href="https://enyst.github.io/openhands-features/{page}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;family=DM+Sans:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="../brand.css"><link rel="stylesheet" href="../assets/openhands-features/feature-map.css">
<script src="../assets/openhands-features/feature-map.js" defer></script></head><body>
<a class="skip-link" href="#content">Skip to content</a>
<header class="topbar"><a class="brand" href="../index.html">EN <span>/ field notes</span></a>
<a class="category-link" href="index.html">OpenHands feature map</a></header>
<main id="content" class="feature-shell">
'''

    def footer(self):
        return '''<footer>Engel’s Code Design Notebook · <a href="../arch/verify-openhands.html">The verification idea</a> · <a href="../arch/control-openhands-cli.html">The CLI</a> · <a href="../arch/verify-openhands-issues.html">The issues and fixes</a></footer>
</main></body></html>\n'''

    def script(self, text):
        """Split prose sentences and literal CLI actions, never punctuation in code."""
        tokens = self.tokens(text)
        rows, pending = [], []
        parentheses = 0

        def flush():
            if pending:
                value = ''.join(v for _, v in pending).strip()
                if value:
                    rows.append(('prose', pending.copy()))
                pending.clear()

        for kind, value in tokens:
            # Full commands and documented shorthand commands remain separate
            # actions. Selectors, expected values, and placeholders stay in prose.
            command = kind == 'code' and parentheses <= 0 and re.match(r'^(?:control-openhands |git -C |curl |npm |node |docker |export |OH_VERIFY_RUN)', value)
            if command:
                flush()
                rows.append(('command', [('code', value)]))
            elif kind in ('code', 'link'):
                pending.append((kind, value))
            else:
                parentheses += value.count('(') - value.count(')')
                parts = re.split(r'(?<=[.!?])\s+(?=[A-Z])', value)
                for i, part in enumerate(parts):
                    if i:
                        flush()
                    pending.append(('text', part))
        flush()
        rendered = []
        for kind, pieces in rows:
            if kind == 'command':
                cmd = pieces[0][1]
                self.code_expected.append(cmd)
                arrange = bool(re.match(r'^(?:export |OH_VERIFY_RUN|.*(?:fixture |llm preset|llm set|api (?:POST|PATCH|PUT|DELETE)))', cmd))
                check = bool(re.search(r'\b(?:snapshot|testids|text|count|value|attr|bbox|errors|toasts|network|events|enabled|visible|url|clipboard|downloads|GET|show|status|doctor)\b', cmd.split(' >> ')[0]))
                wait = bool(re.search(r'\bwait(?:-url|-text)?\b', cmd))
                badge = 'Arrange' if arrange else 'Wait' if wait else 'Check' if check else 'Do'
                label = 'Copy command'
                content = f'<div class="command-line"><code>{esc(cmd)}</code><button type="button" class="copy-command" aria-label="{label}" hidden>Copy</button></div>'
            else:
                plain = ''.join(v for _, v in pieces).strip()
                # Keep connecting prose in the following command's row, avoiding
                # isolated rows containing only "Run", "then", or punctuation.
                connector = re.sub(r'[\s,;.():-]', '', plain).lower()
                if connector in ('', 'run', 'then', 'and', 'thenrun', 'andthen', 'andthenrun', 'next', 'nextrun', 'afterwards'):
                    continue
                if pieces and pieces[0][0] == 'text':
                    pieces = pieces.copy()
                    pieces[0] = ('text', re.sub(r'^[\s,;.]+', '', pieces[0][1]))
                plain = ''.join(v for _, v in pieces).strip()
                badge = 'Expect' if re.match(r'^(?:The |It |After |You |There |No |Both |A |An |This |Its |Saved |Empty |True|False|Count)', plain) else 'Note'
                content = self.inline_tokens(pieces)
                if rendered and rendered[-1]['command'] and re.match(r'^(?:is |are |reads |shows |returns |counts |lists |has |\()', plain):
                    rendered[-1]['content'] += f'<p class="step-observation">{content}</p>'
                    continue
            rendered.append({'badge': badge, 'content': content, 'command': kind == 'command'})
        return '<ol class="script-steps">\n' + '\n'.join(f'<li class="script-row"><span class="row-kind">{row["badge"]}</span><div class="row-content">{row["content"]}</div></li>' for row in rendered) + '\n</ol>'

    def media_for(self, family, recipe, used):
        result = []
        for i, capture in enumerate(self.media):
            if i in used or capture.get('family') != family['id']:
                continue
            ids = capture.get('feature_ids', capture.get('features', []))
            if isinstance(ids, str):
                ids = [ids]
            if not ids and capture.get('feature_id'):
                ids = [capture['feature_id']]
            match = set(ids) & set(recipe['ids'])
            # An explicitly named recipe can target a cleanup/support action.
            label = capture.get('recipe_label', capture.get('recipe', ''))
            preferred = next((r for r in family['recipes'] if label and slug(label) == slug(recipe_title(r['label']))), None)
            if not preferred:
                preferred = next((r for r in family['recipes'] if label and slug(label) in slug(recipe_title(r['label']))), None)
            if preferred and preferred['anchor'] != recipe['anchor']:
                continue
            if match or (preferred and preferred['anchor'] == recipe['anchor']):
                result.append(capture)
                used.add(i)
        return result

    def evidence(self, captures):
        if not captures:
            return ''
        figures = []
        for c in captures:
            filename = c.get('image', c.get('image_filename', c.get('filename', c.get('file', ''))))
            if filename.startswith('assets/'):
                filename = filename.removeprefix('assets/openhands-features/')
            path = SITE / 'assets/openhands-features' / filename
            if not path.is_file() or c.get('source_revision') != self.revision:
                raise ValueError(f'Missing media or different revision: {c}')
            from struct import unpack
            if path.suffix == '.png':
                width, height = unpack('>II', path.read_bytes()[16:24])
            else:
                width, height = 1440, 1000
            self.capture_count += 1
            viewport = c.get('viewport', f'{width} × {height}')
            if isinstance(viewport, dict):
                viewport = f'{viewport.get("width", width)} × {viewport.get("height", height)}'
            caption = c.get('caption', '')
            observation = c.get('observation', '')
            limit = c.get('scope_limitations', c.get('limitations', c.get('scope', '')))
            if isinstance(limit, list):
                limit = ' '.join(limit)
            command = c.get('capture_command', c.get('command', ''))
            actions = c.get('preceding_cli_actions', c.get('actions', c.get('preceding_actions', c.get('cli_actions', []))))
            if isinstance(actions, str):
                actions = [actions]
            commands = '\n'.join(actions + ([command] if command else []))
            versions = ' · '.join(f'{key.replace("_", " ")}: {value}' for key, value in c.get('backend_versions', {}).items())
            src = '../assets/openhands-features/' + filename
            figures.append(f'''<div class="capture-unit"><figure><a href="{esc(src)}" target="_blank" rel="noopener" aria-label="Open full-size screenshot"><img src="{esc(src)}" width="{width}" height="{height}" alt="{esc(c.get('alt', caption))}" loading="lazy" decoding="async"></a>
<figcaption>{esc(caption)} <span class="capture-meta">CLI capture · {esc(viewport)} · 9 October 2026 · Canvas <a href="{REPO}/commit/{self.revision}">{self.revision[:8]}</a></span></figcaption></figure>
{f'<p class="capture-observation">{esc(observation)}</p>' if observation else ''}
{f'<p class="source-note">{esc(limit)}</p>' if limit else ''}
<details class="capture-commands"><summary>How this screenshot was taken</summary><p>{esc(versions)}</p><pre><code>{esc(commands)}</code></pre></details></div>''')
        return '<div class="recipe-evidence" aria-label="Real CLI captures">' + '\n'.join(figures) + '</div>'

    def family_html(self, f, position):
        self.code_expected = []
        page = self.head(f'{f["id"]} · {f["title"]}', f'Every mapped behavior in {f["title"]}: entry points, readable CLI scripts, expected observations, gotchas and real captures.', f['page'])
        page += f'''<header class="overview"><p class="eyebrow">OpenHands / {f['id']} <a class="category-tag" rel="tag" href="index.html">openhands-features</a></p>
<h1 class="hero-title">{esc(f['title'])}</h1>
<div class="lead">{self.block_html(self.blocks(f['overview']))}</div>
<p class="meta">{len(f['behaviors'])} mapped behaviors · {len(f['recipes'])} recipes and supporting checks · source snapshot 9 October 2026<br>
From upstream main at <a href="{REPO}/commit/{self.revision}"><code>{self.revision[:8]}</code></a>. <a href="{self.source_url(SOURCE_DIR+'/'+f['file'])}">Read the maintained source</a>.</p></header>
<div class="page-layout"><aside class="page-nav"><nav aria-label="On this page"><a href="#entry-points">Entry points</a><a href="#preconditions">Before you start</a><a href="#behaviors">Behavior inventory</a><a href="#recipes">Readable recipes</a><a href="#gotchas">Gotchas</a></nav>
<details class="recipe-toc"><summary>Recipe index</summary><nav aria-label="Recipe index">'''
        for recipe in f['recipes']:
            label = recipe_title(recipe['label'])
            page += f'<a href="#{recipe["anchor"]}">{esc(label.replace("`", ""))}</a>\n'
        page += f'''</nav></details></aside><div class="page-content">
<section id="entry-points" class="entry-points"><h2>How to get to it</h2>{self.block_html(f['entry_points'])}</section>
<section id="preconditions" class="preconditions"><h2>Before you start</h2>
<p>Start with <a href="index.html#baseline">the common launch and health checks</a>, then follow this family’s preconditions in order. Recipes share the fixtures and state named below.</p>
{self.block_html(f['preconditions'])}</section>
<section id="behaviors" class="behaviors"><h2>Behavior inventory</h2><details><summary>{len(f['behaviors'])} stable behavior IDs and their expected behavior</summary><ul class="behavior-list">'''
        behavior_index = 0
        for block in f['behavior_blocks']:
            if block['kind'] == 'paragraph':
                page += f'<li class="inventory-group"><strong>{self.inline(block["text"])}</strong></li>'
                continue
            behavior = f['behaviors'][behavior_index]
            behavior_index += 1
            recipe = next((r for r in f['recipes'] if behavior['id'] in r['ids']), None)
            link = f' <a href="#{recipe["anchor"]}">Read recipe ↓</a>' if recipe else ''
            page += f'<li id="{behavior["id"]}"><a class="behavior-id" href="#{behavior["id"]}"><code>{behavior["id"]}</code></a> {self.inline(behavior["description"])}{link}</li>\n'
        page += '''</ul></details></section>
<section id="recipes" class="recipes"><h2>Readable recipes</h2>
<p>Read each script from top to bottom. Code is copied from the map; prose gives the action, expected observation, and conditions. <code>&lt;id&gt;</code>, <code>&lt;run&gt;</code> and similar placeholders stand for values from your own run. Short forms such as <code>browser count</code> continue the same <code>control-openhands</code> invocation; they are kept as documented.</p>
<p class="source-note">Expected observations describe the recipe’s contract. Captures below selected recipes show representative real states from this snapshot; they do not mark every mapped behavior as passed. Follow cleanup before moving to another family.</p>
<div class="search-box" hidden><label for="recipe-search">Find a recipe or behavior ID</label><input id="recipe-search" type="search" placeholder="Try create, phone, or a behavior ID" aria-controls="recipe-list"><p id="recipe-search-status" role="status" aria-live="polite"></p></div>
<p id="recipe-search-empty" hidden>No recipes match. Try another word or a behavior ID.</p><div id="recipe-list">'''
        index, used = 0, set()
        for block in f['drive']:
            if block['kind'] == 'paragraph':
                page += f'<h3 class="recipe-group">{self.inline(block["text"])}</h3>\n'
                continue
            recipe = f['recipes'][index]
            index += 1
            label = recipe_title(recipe['label'])
            ids = ''.join(f'<a href="{self.id_pages.get(i, f["page"])}#{i}"><code>{i}</code></a>' for i in recipe['ids'])
            status = ' · Blocked prerequisite' if recipe['body'].startswith('Blocked:') else ' · Not run' if recipe['body'].startswith('Not-run:') else ''
            page += f'<article class="recipe" id="{recipe["anchor"]}" data-search="{esc(recipe["label"]+" "+recipe["body"])}"><header class="recipe-header"><h3>{self.inline(label)}{esc(status)} <a class="recipe-permalink" href="#{recipe["anchor"]}" aria-label="Link to this recipe">#</a></h3><div class="behavior-tags">{ids}</div></header>\n'
            page += self.script(recipe['body'])
            if recipe['children']:
                page += '<div class="recipe-alternatives"><p>Alternative paths (repeat the preparation above for each):</p><ul>'
                for child in recipe['children']:
                    page += '<li>' + self.script(child) + '</li>'
                page += '</ul></div>'
            page += self.evidence(self.media_for(f, recipe, used)) + '</article>\n'
        # A capture without an exact title match still has a clear family owner.
        unmatched = [c for i, c in enumerate(self.media) if c.get('family') == f['id'] and i not in used]
        if unmatched:
            page += '<div class="family-captures"><h3>More from this family’s real run</h3>' + self.evidence(unmatched) + '</div>'
        page += f'''</div></section><section id="gotchas" class="gotchas"><h2>Gotchas and known limits</h2>{self.block_html(f['gotchas'])}</section>
<p class="source-note">Source paths: {self.inline(f['source'])}</p>
<nav class="family-nav" aria-label="Previous and next family">'''
        if position:
            previous = self.families[position-1]
            page += f'<a href="{previous["page"]}">← {previous["id"]} · {esc(previous["title"])}</a>'
        if position+1 < len(self.families):
            following = self.families[position+1]
            page += f'<a href="{following["page"]}">{following["id"]} · {esc(following["title"])} →</a>'
        page += '</nav></div></div>' + self.footer()
        self.verify_codes(page, self.code_expected)
        return page

    @staticmethod
    def verify_codes(page, expected):
        class Codes(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.active, self.codes, self.buffer = False, [], []
            def handle_starttag(self, tag, attrs):
                if tag == 'code':
                    self.active, self.buffer = True, []
            def handle_data(self, data):
                if self.active:
                    self.buffer.append(data)
            def handle_endtag(self, tag):
                if tag == 'code' and self.active:
                    self.codes.append(''.join(self.buffer))
                    self.active = False
        parsed = Codes()
        parsed.feed(page)
        missing = Counter(expected) - Counter(parsed.codes)
        if missing:
            raise ValueError(f'Rendered commands differ from source: {missing}')

    def card(self, f, prefix=''):
        summary = re.sub(r'\s+', ' ', f['overview']).split('. ')[0].strip()
        return f'''<a class="family-card" href="{prefix}{f['page']}" data-search="{esc(f['id']+' '+f['title']+' '+f['overview']+' '+' '.join(b['id']+' '+b['description'] for b in f['behaviors']))}">
<span class="family-id">{f['id']}</span><h3>{esc(f['title'])}</h3><p>{esc(summary)}.</p>
<span class="family-meta">{len(f['behaviors'])} behaviors · {len(f['recipes'])} recipes</span><span class="category-tag">openhands-features</span></a>'''

    def index_html(self):
        count = sum(len(f['behaviors']) for f in self.families)
        recipes = sum(len(f['recipes']) for f in self.families)
        page = self.head('The OpenHands feature map, for humans', f'{count} behaviors in {len(self.families)} families. Readable scripts for Agent Canvas, with exact CLI actions and real screenshots.', 'index.html')
        page += f'''<header class="overview"><p class="eyebrow">OpenHands / the product, behavior by behavior <span class="category-tag">openhands-features</span></p>
<h1 class="hero-title">The feature map,<br><em>for humans.</em></h1>
<p class="lead">What a user can do in Agent Canvas, how to take that path, and what should happen next. Each family has its own page: readable scripts, literal commands, expected observations, and real screenshots.</p>
<div class="metrics"><dl><div><dt>families</dt><dd>{len(self.families)}</dd></div><div><dt>behaviors</dt><dd>{count}</dd></div><div><dt>recipes & checks</dt><dd>{recipes}</dd></div></dl></div>
<p class="meta">A snapshot of upstream <code>main</code> at <a href="{REPO}/commit/{self.revision}">{self.revision[:8]}</a> · 9 October 2026.<br>The <a href="{self.source_url(SOURCE_DIR+'/README.md')}">maintained map</a> owns the inventory. The <a href="../arch/verify-openhands.html">verification story</a>, <a href="../arch/control-openhands-cli.html">CLI guide</a> and <a href="../arch/verify-openhands-issues.html">issues list</a> explain how it came about.</p></header>
<nav class="links" aria-label="Feature groups">'''
        page += ''.join(f'<a href="#{key}">{esc(name)}</a>' for key, name, _ in GROUPS)
        page += '''<a href="#baseline">Before you start</a></nav>
<section class="family-groups" id="families"><h2>Choose a family</h2>
<div class="search-box" hidden><label for="family-search">Find a feature, page, or behavior ID</label><input type="search" id="family-search" placeholder="Try secrets, workspace, or F14.create" aria-controls="family-list"><p id="search-status" role="status" aria-live="polite"></p></div>
<p id="search-empty" hidden>No families match. Try another word or a behavior ID.</p><div id="family-list">'''
        for key, name, numbers in GROUPS:
            page += f'<section id="{key}"><h3>{esc(name)}</h3><div class="family-grid">'
            page += '\n'.join(self.card(f) for f in self.families if f['number'] in numbers)
            page += '</div></section>'
        page += f'''</div></section><section id="baseline" class="preconditions"><h2>Before you start</h2>
<p>The CLI drives an installed OpenHands checkout. It launches an isolated real stack, keeps a browser open between actions, and records evidence. Run it from the checkout directory with Node 24 or later, installed npm dependencies, <code>uv</code>/<code>uvx</code>, and a supported Chromium browser. The <a href="{self.source_url('.agents/skills/verify-openhands/SKILL.md')}">skill</a> has the complete setup and run contract.</p>
<pre><code>export PATH="$PWD/.agents/skills/verify-openhands/scripts:$PATH"
export OH_VERIFY_RUN=$(control-openhands launch --new --print-run)
control-openhands doctor
control-openhands onboard --skip
# For model-backed recipes, with your configured DeepSeek key:
control-openhands llm preset deepseek
# When finished:
control-openhands stop</code></pre>
<p>Walk onboarding instead of skipping it when F01 is the subject. Start no-LLM checks before configuring a model. Keep <code>OH_VERIFY_RUN</code> set so every command addresses your own run. Desktop is 1440 × 1000; phone is 390 × 844.</p>
<p>Fixtures, API writes and LLM presets arrange preconditions. The user path is proved through the real UI. After saving or deleting, observe again: reload, reopen, or make a read-only API check. Record each actual result with <code>evidence add</code>: <code>pass</code>, <code>fail</code>, <code>blocked</code>, or <code>not-run</code>.</p>
<p>Use <code>deepseek-flash</code> for small model checks and keep prompts confined to the run workspace. Add <code>Do not run any tools</code> when the check only needs a reply. Cloud, enterprise, microphones, Docker and desktop recipes require the environment named in their preconditions.</p></section>
<section id="reading" class="gotchas"><h2>How to read the scripts</h2><p>Each recipe keeps the maintained map’s order and exact code. Numbered rows separate actions and checks; prose explains the expected result. Short forms and placeholders remain as documented. A known failure or blocked prerequisite stays visible.</p>
<p>Selected recipes have fresh screenshots captured with <code>control-openhands browser screenshot</code> from this pinned checkout. Each caption states its scope, and the capture commands are available below it. A screenshot demonstrates the pictured state; API persistence, downloads, sound and timing still need their stated observations. Mapped behaviors are an inventory, not a fresh all-pass ledger.</p>
<p>This category mirrors a dated source revision. The earlier presentation and issue list retain their original dates and counts. <a href="../assets/openhands-features/feature-map.json">Download the category inventory and provenance</a>.</p></section>
<section id="coverage"><h2>Coverage boundaries from the maintained map</h2>'''
        raw_index = (self.checkout / SOURCE_DIR / 'README.md').read_text()
        page += self.block_html(self.blocks(raw_index.split('## Not mapped\n', 1)[1]))
        page += f'''</section><p class="source-note">The approach adapts Lauren Tan’s (<a href="https://github.com/poteto">@poteto</a>) pstack verification-skill generators. <a href="{self.source_url('.agents/skills/verify-openhands/references/adaptation.md')}">Read the adaptation and attribution</a>.</p>'''
        return page + self.footer()

    def write(self):
        target = SITE / 'openhands-features'
        target.mkdir(exist_ok=True)
        for i, family in enumerate(self.families):
            (target / family['page']).write_text(self.family_html(family, i))
        (target / 'index.html').write_text(self.index_html())
        manifest = {'published_snapshot': DATE, 'source_repository': REPO,
                    'source_revision': self.revision, 'source_directory': SOURCE_DIR,
                    'families': len(self.families), 'behaviors': sum(len(f['behaviors']) for f in self.families),
                    'recipes_and_supporting_checks': sum(len(f['recipes']) for f in self.families),
                    'captures': self.capture_count,
                    'inventory': [{k: f[k] for k in ('id', 'title', 'file', 'page', 'sha256', 'behaviors', 'recipes')} for f in self.families]}
        (SITE / 'assets/openhands-features/feature-map.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n')
        # This delimited block is the only homepage content owned by this script.
        index = SITE / 'index.html'
        text = index.read_text()
        nav = '<a href="#openhands-features">OpenHands features</a>'
        if nav not in text:
            text = text.replace('<a href="#how-things-work">', nav+'\n      <a href="#how-things-work">', 1)
        cards = f'''    <!-- BEGIN OPENHANDS FEATURES -->
    <section aria-labelledby="openhands-features">
    <h2 id="openhands-features">OpenHands features</h2>
    <p class="meta">The feature map, for humans: {manifest['behaviors']} behaviors in 27 families, with readable CLI scripts and real screenshots. Source snapshot: 9 October 2026.</p>
    <div class="cards"><a class="card" href="openhands-features/index.html"><div class="card-title">Explore the OpenHands feature map</div><div class="card-desc">Choose a family or search a behavior ID. Follow the user entry point, the commands, and the expected result.</div><span class="card-tag tag-data">openhands-features · full index</span></a></div>
'''
        for key, name, numbers in GROUPS:
            cards += f'    <h3 style="margin:24px 0 12px">{esc(name)}</h3><div class="cards">\n'
            for f in self.families:
                if f['number'] in numbers:
                    cards += f'''      <a class="card" href="openhands-features/{f['page']}"><div class="card-title">{f['id']} · {esc(f['title'])}</div><div class="card-desc">{len(f['behaviors'])} behaviors · {len(f['recipes'])} readable recipes and supporting checks.</div><span class="card-tag tag-data">openhands-features</span></a>\n'''
            cards += '    </div>\n'
        cards += '    </section>\n    <!-- END OPENHANDS FEATURES -->\n\n'
        if '<!-- BEGIN OPENHANDS FEATURES -->' in text:
            text = re.sub(r'    <!-- BEGIN OPENHANDS FEATURES -->.*?    <!-- END OPENHANDS FEATURES -->\n\n', lambda _: cards, text, flags=re.S)
        else:
            text = text.replace('    <h2 id="investigations">', cards+'    <h2 id="investigations">', 1)
        index.write_text(text)
        print(f'Published {manifest["families"]} families, {manifest["behaviors"]} behaviors, {manifest["recipes_and_supporting_checks"]} recipes/checks, {self.capture_count} captures at {self.revision}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', type=Path, required=True)
    args = parser.parse_args()
    if subprocess.run(['git', '-C', str(args.checkout), 'diff', '--quiet', 'HEAD', '--', SOURCE_DIR]).returncode:
        raise SystemExit('Select a clean feature-map revision before publishing it.')
    publisher = Publisher(args.checkout.resolve())
    publisher.read()
    publisher.write()
