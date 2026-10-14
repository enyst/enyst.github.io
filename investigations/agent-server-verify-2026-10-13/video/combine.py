#!/usr/bin/env python3
"""Join recorded excerpts and append a final, explicitly defined count card."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from record import HTML, ROOT, duration, make_mix, run, speech, write_captions


def srt_entries(path):
    def seconds(s):
        h, m, rest = s.split(':')
        secs, ms = rest.split(',')
        return int(h) * 3600 + int(m) * 60 + int(secs) + int(ms) / 1000
    for block in path.read_text().strip().split('\n\n'):
        lines = block.splitlines()
        if len(lines) < 3:
            continue
        start, end = lines[1].split(' --> ')
        yield seconds(start), seconds(end), '\n'.join(lines[2:])


def stamp(seconds):
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manifest', type=Path)
    args = ap.parse_args()
    spec = json.loads(args.manifest.read_text())
    if spec.get('requires_final_counts') and not spec.get('final_counts_confirmed'):
        raise SystemExit('Final full-report counts are required before composing the publication film.')
    out = ROOT / spec.get('slug', 'final-highlights')
    out.mkdir(exist_ok=True)
    os.environ['PLAYWRIGHT_BROWSERS_PATH'] = str(ROOT / 'playwright-runtime')
    ending_audio = out / 'full-report-counts.wav'
    spoken_length = speech(spec['ending_narration'], ending_audio)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                              args=['--no-sandbox', '--disable-dev-shm-usage'])
        c = b.new_context(viewport={'width': 1280, 'height': 720},
                          record_video_dir=str(out / 'summary-raw'),
                          record_video_size={'width': 1280, 'height': 720})
        page = c.new_page()
        page.set_content(HTML)
        page.evaluate('summary', {'title': spec['ending_title'],
                                  'closing': spec['ending_caption'],
                                  'eyebrow': spec['ending_eyebrow'],
                                  'counts': spec['all_finding_counts']})
        page.wait_for_timeout(int((spoken_length + 2.3) * 1000))
        page.screenshot(path=str(out / 'full-report-counts.png'))
        raw = Path(page.video.path())
        c.close(); b.close()
    summary_length = min(duration(raw), spoken_length + 2.8)
    events = [{'type': 'speech', 'at': .6, 'path': str(ending_audio)}]
    mix = out / 'summary-mix.wav'
    make_mix(events, summary_length, mix)
    summary = out / 'summary.mp4'
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(raw), '-i', str(mix),
         '-map', '0:v', '-map', '1:a', '-r', '25', '-c:v', 'libx264', '-crf', '22',
         '-preset', 'veryfast', '-threads', '2', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k',
         '-t', str(summary_length), str(summary)])
    summary_captions = out / 'summary.srt'
    write_captions(events, summary_captions)
    pieces, captions, chapters = [], [], []
    offset = 0.0
    for i, entry in enumerate(spec['clips']):
        source = Path(entry['directory'])
        meta = json.loads((source / 'recording-metadata.json').read_text())
        cutoff = float(meta['summary_at'])
        chapters.append({'at_seconds': offset, 'title': entry['title'],
                         'feature': entry['feature'], 'source': str(source),
                         'editing_note': entry.get('editing_note'),
                         'retained_source_ranges': entry.get('keep_ranges', [[0, cutoff]])})
        ranges = entry.get('keep_ranges', [[0, cutoff]])
        for j, (beg, end) in enumerate(ranges):
            end = cutoff if end == 'summary' else float(end)
            beg = float(beg)
            if end <= beg or end > cutoff + .05:
                raise ValueError('Invalid retained recording range')
            trim = out / f'{i + 1:02d}-{j + 1:02d}-recorded-highlight.mp4'
            video_filters = []
            if j and entry.get('editing_note'):
                # Caption is a production note, not part of the API evidence.
                note_file = out / f'{i + 1:02d}-editing-note.txt'
                note_file.write_text(entry['editing_note'])
                video_filters.append(f'drawtext=textfile={note_file}:fontcolor=white:fontsize=15:x=28:y=697:box=1:boxcolor=black@0.8:enable=lt(t\\,2.5)')
            timer = entry.get('probe_timer')
            if timer and beg <= timer['start_at'] < end:
                # Original recorder clock covers the entire reproduction. This
                # supporting clock isolates the actual probe operation, using
                # recorded stdout timestamps. Exact HTTP latency stays in view.
                local_start = timer['start_at'] - beg
                local_end = timer['end_at'] - beg
                timer_file = out / f'{i + 1:02d}-probe-timer.txt'
                timer_file.write_text(f'Probe operation: %{{eif:min(t,{local_end})-{local_start}:d}} sec')
                enable = f'gte(t\\,{local_start})'
                video_filters.extend([
                    f'drawbox=x=475:y=668:w=440:h=34:color=0x080b14:t=fill:enable={enable}',
                    f'drawtext=textfile={timer_file}:fontcolor=0x83c9ff:fontsize=15:x=518:y=679:enable={enable}'
                ])
            equation = entry.get('equation')
            if equation and end > equation['after_at']:
                reveal = max(0, equation['after_at'] - beg)
                eq_file = out / f'{i + 1:02d}-equation.txt'
                cap_file = out / f'{i + 1:02d}-equation-caption.txt'
                eq_file.write_text(equation['text'])
                cap_file.write_text(equation['caption'])
                video_filters.extend([
                    f'drawtext=textfile={eq_file}:fontcolor=0xffe389:fontsize=34:x=76:y=540:enable=gte(t\\,{reveal})',
                    f'drawtext=textfile={cap_file}:fontcolor=0xb8cce3:fontsize=12:x=76:y=587:enable=gte(t\\,{reveal})'
                ])
            vf = ['-vf', ','.join(video_filters)] if video_filters else []
            run(['ffmpeg', '-y', '-v', 'error', '-ss', str(beg),
                 '-i', str(source / 'agent-server-verification.mp4'),
                 '-map', '0:v', '-map', '0:a', '-t', str(end - beg), '-r', '25',
                 *vf, '-af', f'afade=t=in:st=0:d=0.025,afade=t=out:st={max(0, end-beg-.025)}:d=0.025',
                 '-c:v', 'libx264', '-crf', '22', '-preset', 'veryfast', '-threads', '2',
                 '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', str(trim)])
            length = duration(trim)
            for a, z, text in srt_entries(source / 'narration.srt'):
                if a < end and z > beg:
                    captions.append((offset + max(a, beg) - beg,
                                     offset + min(z, end) - beg, text))
            pieces.append(trim)
            offset += length
    chapters.append({'at_seconds': offset, 'title': 'Complete report counts'})
    for a, z, text in srt_entries(summary_captions):
        captions.append((offset + a, offset + z, text))
    pieces.append(summary)
    srt = out / 'narration.srt'
    subtitle_text = '\n\n'.join(f'{i + 1}\n{stamp(a)} --> {stamp(z)}\n{text}'
                                for i, (a, z, text) in enumerate(captions)) + '\n'
    srt.write_text(subtitle_text)
    srt.with_suffix('.vtt').write_text('WEBVTT\n\n' + re.sub(
        r'(\d{2}:\d{2}:\d{2}),(\d{3})', r'\1.\2', subtitle_text))
    concat = out / 'concat.txt'
    concat.write_text(''.join(f"file '{path}'\n" for path in pieces))
    target = out / 'agent-server-bug-highlights.mp4'
    run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(concat),
         '-i', str(srt), '-map', '0:v', '-map', '0:a', '-map', '1:0',
         '-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text',
         '-metadata:s:s:0', 'language=eng', '-movflags', '+faststart', str(target)])
    (out / 'chapters.json').write_text(json.dumps(chapters, indent=2))
    screenplay = ['Agent Server verification · original narrated screenplay',
                  'Actual recorded reproductions. Setup/cleanup edits are labeled.', '']
    for i, chapter in enumerate(chapters):
        end = chapters[i + 1]['at_seconds'] if i + 1 < len(chapters) else float('inf')
        spoken = [text.replace('\n', ' ') for a, z, text in captions
                  if chapter['at_seconds'] <= a < end]
        screenplay.extend([f"[{stamp(chapter['at_seconds']).replace(',', '.')} · {chapter['title']}]",
                           'NARRATOR: ' + ' '.join(spoken), ''])
    (out / 'screenplay.txt').write_text('\n'.join(screenplay))
    (out / 'counting-convention.json').write_text(json.dumps({
        'counts': spec['all_finding_counts'], 'caption': spec['ending_caption'],
        'narration': spec['ending_narration']}, indent=2))
    print(json.dumps({'video': str(target), 'duration_seconds': duration(target),
                      'chapters': len(chapters), 'bytes': target.stat().st_size}))


if __name__ == '__main__':
    main()
