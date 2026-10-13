#!/usr/bin/env python3
"""Record live, confirmed repro commands; compose speech and an original score.

This is a recording script, not a simulation. Every terminal line comes from
the actual child process. Claims must have a matching confirmation signal.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import queue
import re
import shlex
import shutil
import subprocess
import threading
import time
import wave
from pathlib import Path

import numpy as np
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent

HTML = r'''<!doctype html><html><head><meta charset="utf-8"><style>
* { box-sizing:border-box } body { margin:0;background:#080b14;color:#edf2fa;
font-family:"Open Sans",sans-serif;overflow:hidden; }
.grid {position:fixed;inset:0;background-image:linear-gradient(#28314733 1px,transparent 1px),linear-gradient(90deg,#28314733 1px,transparent 1px);background-size:48px 48px;opacity:.3}
.frame {position:relative;width:1280px;height:720px;padding:35px 44px}
.eyebrow {font-size:16px;letter-spacing:2px;color:#83c9ff;text-transform:uppercase}
.top {display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.tag {font-size:14px;background:#1f3145;color:#b6ddff;padding:8px 14px;border-radius:30px}
h1 {font-size:36px;font-weight:600;margin:8px 0 20px;letter-spacing:-.7px;max-width:1100px}
.panels {display:grid;grid-template-columns:410px 1fr;gap:28px;height:465px}
.contract {padding:21px;background:#111927;border-radius:14px;border:1px solid #344258}
.label {font-size:14px;letter-spacing:1.8px;text-transform:uppercase;color:#8397b2}
.claim {font-size:22px;line-height:1.45;margin:12px 0 22px;min-height:78px}
.observed {opacity:.14;transition:opacity 700ms;color:#ffe389}
.observed.active {opacity:1}
.terminal {border:1px solid #3d495b;border-radius:14px;overflow:hidden;background:#070e19}
.termbar {display:flex;gap:8px;background:#172232;padding:14px 18px;font-size:13px;color:#b4c6dc}
.dot {width:10px;height:10px;border-radius:100%;background:#77a9d1;display:inline-block}
#cmd {font-size:13px;line-height:1.4;color:#83c9ff;white-space:pre-wrap;overflow-wrap:anywhere;padding:12px 18px;border-bottom:1px solid #263346;max-height:64px;overflow:hidden}
#out {font:16px/1.48 monospace;white-space:pre-wrap;overflow-wrap:anywhere;padding:15px 18px;margin:0;height:340px;overflow:hidden;color:#e4ebf5}
#out .signal {color:#ffe389;background:#80632055;display:block}
svg {width:100%;height:94px;overflow:visible} .edge {stroke:#83c9ff;stroke-width:3;fill:none;stroke-dasharray:180;stroke-dashoffset:180;animation:edge 3s ease forwards}
@keyframes edge {to {stroke-dashoffset:0}}
.node {fill:#101a2c;stroke:#83c9ff;stroke-width:2}.node.actual {stroke:#ffe389}
.tiny {font-size:12px;fill:#b8cce3}.tiny.actual {fill:#ffe389}
.foot {position:absolute;bottom:25px;left:44px;right:44px;display:flex;justify-content:space-between;font-size:15px;color:#8d9fb8}
#status {color:#83c9ff} #status.confirmed {color:#ffe389}
.summary {display:none;position:absolute;inset:0;padding:88px 100px;background:#080b14}
.summary h1 {font-size:53px;margin:20px 0 40px}
.counts {display:flex;gap:28px;margin:25px 0 40px}.count {padding:28px;border:1px solid #456080;border-radius:16px;min-width:190px}.number {font-size:65px;color:#83c9ff}.count .label {margin-top:4px}
.closing {font-size:25px;max-width:1020px;line-height:1.5;color:#c0d0e7}
</style></head><body><div class="grid"></div><div class="frame">
<div class="top"><div class="eyebrow">Agent Server · verification laboratory</div><div class="tag" id="tag">LIVE REPRODUCTION</div></div>
<h1 id="title"></h1><div class="panels"><div class="contract"><div class="label">Expected contract</div><div class="claim" id="expected"></div>
<svg viewBox="0 0 366 94"><path class="edge" d="M76 46 H280"/><circle class="node" cx="54" cy="46" r="30"/><circle class="node actual" cx="310" cy="46" r="30"/><text class="tiny" x="54" y="51" text-anchor="middle">INPUT</text><text class="tiny actual" x="310" y="51" text-anchor="middle">OUTPUT</text></svg>
<div class="observed" id="observed"><div class="label">Actual observation</div><div class="claim" id="actual"></div></div></div>
<div class="terminal"><div class="termbar"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span style="margin-left:10px">Actual process output · redacted credentials</span></div><div id="cmd"></div><pre id="out"></pre></div></div>
<div class="foot"><span id="chapter"></span><span id="status">Reading the contract…</span><span>Dark canvas. Bright evidence.</span></div>
<div class="summary" id="summary"><div class="eyebrow" id="summaryeyebrow">Verification complete · all confirmed findings counted</div><h1 id="summarytitle"></h1><div class="counts" id="counts"></div><div class="closing" id="closing"></div></div>
</div><script>
window.chapter = c => {document.getElementById('summary').style.display='none';for(const k of ['title','expected','actual'])document.getElementById(k).textContent=c[k];document.getElementById('tag').textContent=c.severity.toUpperCase()+' SEVERITY';document.getElementById('chapter').textContent=c.id+' · '+c.position;document.getElementById('cmd').textContent='$ '+c.command;document.getElementById('out').replaceChildren();document.getElementById('observed').classList.remove('active');document.getElementById('status').className='';document.getElementById('status').textContent='Reading the contract…';};
window.running = label => {clearInterval(window.elapsedTimer);const began=Date.now();const s=document.getElementById('status');const name=label||'Reproduction elapsed';s.textContent=name+' · 0.0 sec';window.elapsedTimer=setInterval(()=>{s.textContent=name+' · '+((Date.now()-began)/1000).toFixed(1)+' sec'},100)};
window.line = obj => {const pre=document.getElementById('out');const span=document.createElement('span');span.textContent=obj.text+'\n';if(obj.signal)span.className='signal';pre.appendChild(span);while(pre.scrollHeight>pre.clientHeight && pre.childElementCount>1)pre.firstChild.remove();if(obj.signal)document.getElementById('observed').classList.add('active');};
window.finish = obj => {clearInterval(window.elapsedTimer);document.getElementById('observed').classList.add('active');const s=document.getElementById('status');s.className=obj.confirmed?'confirmed':'';s.textContent=(obj.confirmed?'CONFIRMED':'UNCONFIRMED')+' · process exit '+obj.code;};
window.summary = obj => {document.getElementById('summary').style.display='block';document.getElementById('summaryeyebrow').textContent=obj.eyebrow||'Verification complete · all confirmed findings counted';document.getElementById('summarytitle').textContent=obj.title;document.getElementById('closing').textContent=obj.closing;const e=document.getElementById('counts');e.replaceChildren();for(const [label,value] of Object.entries(obj.counts)){const d=document.createElement('div');d.className='count';const n=document.createElement('div');n.className='number';n.textContent=value;const l=document.createElement('div');l.className='label';l.textContent=label;d.append(n,l);e.append(d)}};
</script></body></html>'''


def run(args: list[str], **kwargs):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, **kwargs)


def duration(path: Path) -> float:
    return float(run(['ffprobe', '-v', 'error', '-show_entries',
                      'format=duration', '-of', 'default=nw=1:nk=1', str(path)]).stdout)


def speech(text: str, target: Path) -> float:
    txt = target.with_suffix('.txt')
    txt.write_text(text)
    run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i',
         f'flite=textfile={txt}:voice=slt', '-ar', '48000', '-ac', '1', str(target)])
    return duration(target)


def sanitizer():
    secrets = [v for k, v in os.environ.items()
               if re.search(r'(API_KEY|TOKEN|PASSWORD|SECRET)', k) and len(v) > 6]

    def clean(text):
        for v in secrets:
            text = text.replace(v, '[REDACTED]')
        text = re.sub(r'(?i)(bearer\s+)[^\s"\']+', r'\1[REDACTED]', text)
        return re.sub(r'\bsk-[A-Za-z0-9_-]{12,}', '[REDACTED]', text)
    return clean


def put_audio(mix: np.ndarray, path: Path, start: float, gain=1.0):
    result = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f',
                             'f32le', '-ar', '48000', '-ac', '1', '-'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    audio = np.frombuffer(result.stdout, dtype=np.float32)
    at = int(start * 48000)
    length = min(len(audio), len(mix) - at)
    if length > 0:
        mix[at:at + length] += audio[:length] * gain


def tone(mix, start, seconds, hz, amp):
    at = int(start * 48000)
    n = min(int(seconds * 48000), len(mix) - at)
    if n <= 0:
        return
    t = np.arange(n) / 48000
    env = np.minimum(t / .025, 1) * np.exp(-t / (seconds * .3))
    sample = np.sin(2 * math.pi * hz * t) + .25 * np.sin(4 * math.pi * hz * t)
    mix[at:at + n] += (sample * env * amp).astype(np.float32)


def make_mix(events, full_duration, target):
    mix = np.zeros(math.ceil((full_duration + .2) * 48000), dtype=np.float32)
    # Original quiet D minor / suspended score, written for this report.
    progression = [(146.83, 220.00, 293.66), (130.81, 196.00, 261.63),
                   (116.54, 174.61, 233.08), (130.81, 196.00, 293.66)]
    for i, at in enumerate(np.arange(.3, full_duration, 6)):
        chord = progression[i % len(progression)]
        for j, hz in enumerate(chord):
            tone(mix, float(at) + j * .17, 5.8, hz, .015)
    for event in events:
        if event['type'] == 'speech':
            put_audio(mix, Path(event['path']), event['at'], 1.0)
        elif event['type'] == 'cue':
            # A gentle ascending "there it is" motif, distinctive from the score.
            for j, hz in enumerate([587.33, 739.99, 880.00]):
                tone(mix, event['at'] + j * .13, .65, hz, .075)
    peak = np.max(np.abs(mix))
    if peak > .94:
        mix *= .94 / peak
    with wave.open(str(target), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
        w.writeframes((mix * 32767).astype('<i2').tobytes())


def write_captions(events, target):
    def stamp(seconds):
        millis = round(seconds * 1000)
        hours, millis = divmod(millis, 3600000)
        minutes, millis = divmod(millis, 60000)
        secs, millis = divmod(millis, 1000)
        return f'{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}'
    cues = []
    for event in events:
        if event['type'] != 'speech':
            continue
        path = Path(event['path'])
        text = path.with_suffix('.txt').read_text()
        # Short sentences, evenly timed within each synthesized speech segment.
        sentences = re.findall(r'[^.!?]+[.!?]?', text)
        total = sum(len(s) for s in sentences)
        at, length = event['at'], duration(path)
        for sentence in sentences:
            end = at + length * len(sentence) / total
            cues.append(f'{len(cues) + 1}\n{stamp(at)} --> {stamp(end)}\n{sentence.strip()}\n')
            at = end
    contents = '\n'.join(cues)
    target.write_text(contents)
    target.with_suffix('.vtt').write_text('WEBVTT\n\n' + re.sub(
        r'(\d{2}:\d{2}:\d{2}),(\d{3})', r'\1.\2', contents))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifest', type=Path)
    args = ap.parse_args()
    manifest = json.loads(args.manifest.read_text())
    chapters = manifest['chapters']
    if not chapters or any(c.get('confirmed') is not True for c in chapters):
        raise SystemExit('Only independently confirmed findings may be recorded.')
    out = ROOT / manifest.get('slug', 'agent-server-bugs')
    out.mkdir(exist_ok=True)
    runtime = ROOT / 'playwright-runtime' / 'ffmpeg-1011'
    runtime.mkdir(parents=True, exist_ok=True)
    exe = runtime / 'ffmpeg-linux'
    if not exe.exists():
        exe.symlink_to('/usr/bin/ffmpeg')
    os.environ['PLAYWRIGHT_BROWSERS_PATH'] = str(runtime.parent)
    clean = sanitizer()
    for i, c in enumerate(chapters):
        c['speech_files'] = {}
        for key in ['opening', 'observation']:
            path = out / f'{i + 1:02d}-{key}.wav'
            c['speech_files'][key] = {'path': str(path),
                                     'duration': speech(c[key + '_narration'], path)}
    ending = out / 'ending.wav'
    ending_duration = speech(manifest['ending_narration'], ending)
    events, evidence = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                                    args=['--no-sandbox', '--disable-dev-shm-usage'])
        context = browser.new_context(viewport={'width': 1280, 'height': 720},
                                      record_video_dir=str(out / 'raw'),
                                      record_video_size={'width': 1280, 'height': 720})
        page = context.new_page()
        start = time.monotonic()
        page.set_content(HTML)
        page.wait_for_timeout(300)
        for i, c in enumerate(chapters):
            info = {k: c[k] for k in ['id', 'title', 'severity', 'expected', 'actual']}
            info.update(position=f'{i + 1} / {len(chapters)}', command=shlex.join(c['command']))
            page.evaluate('chapter', info)
            opening = c['speech_files']['opening']
            events.append({'type': 'speech', 'at': time.monotonic() - start + .3,
                           'path': opening['path']})
            page.wait_for_timeout(int((opening['duration'] + .7) * 1000))
            page.evaluate('running')
            proc = subprocess.Popen(c['command'], cwd=c.get('cwd', '/workspace/agent-sdk'),
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, bufsize=1)
            q = queue.Queue()
            def reader():
                for line in proc.stdout:
                    q.put(line)
                q.put(None)
            threading.Thread(target=reader, daemon=True).start()
            began = time.monotonic()
            rec = {'id': c['id'], 'command': c['command'], 'started_at': began - start,
                   'lines': []}
            pattern = re.compile(c['bug_signal'])
            found, done = False, False
            while not done:
                if time.monotonic() - began > c.get('timeout', 180):
                    proc.kill()
                    raise RuntimeError(f"{c['id']} reproduction timed out")
                try:
                    line = q.get(timeout=.08)
                except queue.Empty:
                    page.wait_for_timeout(60)
                    continue
                if line is None:
                    done = True
                    break
                line = clean(line.rstrip())
                signal = bool(pattern.search(line))
                if signal and not found:
                    found = True
                    events.append({'type': 'cue', 'at': time.monotonic() - start + .06,
                                   'id': c['id']})
                rec['lines'].append({'at': time.monotonic() - start, 'text': line,
                                     'signal': signal})
                if c.get('timer_signal') and re.search(c['timer_signal'], line):
                    page.evaluate('running', c.get('timer_label', 'Operation elapsed'))
                page.evaluate('line', {'text': line, 'signal': signal})
                page.wait_for_timeout(c.get('line_delay_ms', 100))
            code = proc.wait()
            rec.update(exit_code=code, confirmed_signal=found, ended_at=time.monotonic() - start)
            evidence.append(rec)
            page.evaluate('finish', {'confirmed': found, 'code': code})
            (out / 'live-evidence.json').write_text(json.dumps(evidence, indent=2))
            if not found:
                raise RuntimeError(f"{c['id']} did not produce the documented bug signal")
            obs = c['speech_files']['observation']
            events.append({'type': 'speech', 'at': time.monotonic() - start + .3,
                           'path': obs['path']})
            page.wait_for_timeout(int((obs['duration'] + 1.8) * 1000))
        summary_at = time.monotonic() - start
        page.evaluate('summary', {'title': manifest['ending_title'],
                                  'closing': manifest['ending_caption'],
                                  'eyebrow': manifest.get('ending_eyebrow'),
                                  'counts': manifest['all_finding_counts']})
        events.append({'type': 'speech', 'at': time.monotonic() - start + .3,
                       'path': str(ending)})
        page.wait_for_timeout(int((ending_duration + 2) * 1000))
        content_duration = time.monotonic() - start
        page.screenshot(path=str(out / 'summary.png'))
        video = Path(page.video.path())
        context.close(); browser.close()
    raw = out / 'recorded-reproductions.webm'
    shutil.copy2(video, raw)
    length = min(duration(raw), content_duration + .5)
    (out / 'timeline.json').write_text(json.dumps(events, indent=2))
    (out / 'recording-metadata.json').write_text(json.dumps({
        'manifest': str(args.manifest), 'summary_at': summary_at,
        'content_duration': content_duration, 'final_duration': length,
        'independent_confirmation_runs': manifest.get('independent_confirmation_runs', [])
    }, indent=2))
    captions = out / 'narration.srt'
    write_captions(events, captions)
    mix = out / 'narration-and-score.wav'
    make_mix(events, length, mix)
    target = out / 'agent-server-verification.mp4'
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(raw), '-i', str(mix), '-i', str(captions),
         '-map', '0:v:0', '-map', '1:a:0', '-map', '2:0', '-c:s', 'mov_text',
         '-metadata:s:s:0', 'language=eng', '-c:v', 'libx264', '-preset', 'veryfast', '-threads', '2',
         '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
         '-movflags', '+faststart', '-t', str(length), str(target)])
    print(json.dumps({'video': str(target), 'duration_seconds': length,
                      'chapters': len(chapters), 'evidence': str(out / 'live-evidence.json')}))


if __name__ == '__main__':
    main()
