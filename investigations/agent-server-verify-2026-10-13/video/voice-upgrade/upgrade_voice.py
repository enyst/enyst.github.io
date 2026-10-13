#!/usr/bin/env python3
"""Replace narration and remix the score without changing recorded video packets."""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
from pathlib import Path

from record import ROOT, duration, make_mix, run, write_captions

UP=ROOT/'voice-upgrade'
GENERATED=UP/'generated'
OUT=UP/'remix'


def video_hash(path):
    # Container metadata and audio change; the compressed video stream must not.
    result=run(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-c','copy',
                '-f','hash','-hash','sha256','-'])
    return result.stdout.strip()


def mix_video(source,mix,captions,target):
    run(['ffmpeg','-y','-v','error','-i',str(source),'-i',str(mix),'-i',str(captions),
         '-map','0:v:0','-map','1:a:0','-map','2:0','-c:v','copy','-c:a','aac',
         '-b:a','160k','-c:s','mov_text','-metadata:s:s:0','language=eng',
         '-metadata','comment=Neural narration update; original recorded video stream preserved',
         '-t',str(duration(source)),'-movflags','+faststart',str(target)])
    assert video_hash(source)==video_hash(target),f'Video stream changed: {target}'
    run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'])


def main():
    spec=json.loads((ROOT/'final-highlights.json').read_text())
    chapters=json.loads((ROOT/'final-highlights/chapters.json').read_text())
    OUT.mkdir(parents=True,exist_ok=True)
    report={'voice_provenance':json.loads((UP/'voice-manifest.json').read_text()),
            'video_stream_preserved':True,'clips':[],'speech_adjustments':[],
            'main_events':[],'captions':'Sentence timing is proportional within each complete spoken segment.'}
    main_events=[]
    for i,(entry,chapter) in enumerate(zip(spec['clips'],chapters)):
        source_dir=Path(entry['directory']);slug=source_dir.name
        target_dir=OUT/'uncut'/slug;target_dir.mkdir(parents=True,exist_ok=True)
        source=source_dir/'agent-server-verification.mp4'
        length=duration(source)
        timeline=json.loads((source_dir/'timeline.json').read_text())
        cutoff=json.loads((source_dir/'recording-metadata.json').read_text())['summary_at']
        ranges=[]
        offset=chapter['at_seconds']
        for j,(beg,end) in enumerate(entry['keep_ranges']):
            end=cutoff if end=='summary' else float(end)
            piece=ROOT/'final-highlights'/f'{i+1:02d}-{j+1:02d}-recorded-highlight.mp4'
            ranges.append({'beg':float(beg),'end':end,'offset':offset})
            offset+=duration(piece)
        events=[]
        for k,event in enumerate(timeline):
            updated=dict(event)
            keep=next((r for r in ranges if r['beg']<=event['at']<r['end']),None)
            if event['type']=='speech':
                name=Path(event['path']).name
                generated=GENERATED/slug/name
                assert generated.exists(),generated
                text=generated.with_suffix('.txt').read_text()
                natural=duration(generated)
                following=[e['at'] for e in timeline[k+1:] if e['type']=='speech']
                bound=(following[0] if following else length)-event['at']-.2
                if keep:bound=min(bound,keep['end']-event['at']-.2)
                tempo=max(1,natural/bound)
                assert tempo<=1.20,('Narration needs a shorter natural delivery',slug,name,natural,bound,tempo)
                voice=target_dir/name
                run(['ffmpeg','-y','-v','error','-i',str(generated),
                     '-af',f'atempo={tempo:.8f},loudnorm=I=-18:TP=-3:LRA=8',
                     '-ar','48000','-ac','1',str(voice)])
                voice.with_suffix('.txt').write_text(text)
                assert duration(voice)<=bound+.05
                updated['path']=str(voice)
                report['speech_adjustments'].append({'clip':slug,'file':name,
                    'natural_duration':natural,'available_seconds':bound,'tempo':tempo,
                    'rendered_duration':duration(voice),'voice_loudness_target_lufs':-18})
            events.append(updated)
            if keep:
                main_event={**updated,'at':keep['offset']+event['at']-keep['beg']}
                main_events.append(main_event)
        captions=target_dir/'narration.srt';write_captions(events,captions)
        mix=target_dir/'neural-narration-and-score.wav';make_mix(events,length,mix)
        target=target_dir/'agent-server-verification.mp4';mix_video(source,mix,captions,target)
        (target_dir/'timeline.json').write_text(json.dumps(events,indent=2)+'\n')
        report['clips'].append({'slug':slug,'duration_seconds':length,
                               'video_stream_hash':video_hash(target),
                               'audio_and_video_decode':'pass','output':str(target)})
    main_dir=OUT/'final-highlights';main_dir.mkdir(exist_ok=True)
    source=ROOT/'final-highlights/agent-server-bug-highlights.mp4';length=duration(source)
    counts=GENERATED/'final-highlights/full-report-counts.wav'
    start=chapters[-1]['at_seconds']+.6
    natural=duration(counts);bound=length-start-.4;tempo=max(1,natural/bound)
    assert tempo<=1.20,('Count narration needs a shorter natural delivery',natural,bound)
    voice=main_dir/'full-report-counts.wav'
    run(['ffmpeg','-y','-v','error','-i',str(counts),
         '-af',f'atempo={tempo:.8f},loudnorm=I=-18:TP=-3:LRA=8',
         '-ar','48000','-ac','1',str(voice)])
    voice.with_suffix('.txt').write_text(counts.with_suffix('.txt').read_text())
    main_events.append({'type':'speech','at':start,'path':str(voice)})
    main_events.sort(key=lambda e:e['at'])
    captions=main_dir/'narration.srt';write_captions(main_events,captions)
    mix=main_dir/'neural-narration-and-score.wav';make_mix(main_events,length,mix)
    target=main_dir/'agent-server-bug-highlights.mp4';mix_video(source,mix,captions,target)
    report['main']={'duration_seconds':length,'video_stream_hash':video_hash(target),
                    'output':str(target),'audio_and_video_decode':'pass',
                    'ending_tempo':tempo,'ending_natural_duration':natural}
    report['main_events']=main_events
    (main_dir/'timeline.json').write_text(json.dumps(main_events,indent=2)+'\n')
    screenplay=['Agent Server verification · neural narrated screenplay',
                'Actual recorded reproductions. Setup/cleanup edits are labeled.','']
    for i,chapter in enumerate(chapters):
        end=chapters[i+1]['at_seconds'] if i+1<len(chapters) else length
        spoken=[Path(e['path']).with_suffix('.txt').read_text() for e in main_events
                if e['type']=='speech' and chapter['at_seconds']<=e['at']<end]
        screenplay.extend([f"[{chapter['at_seconds']:.3f} sec · {chapter['title']}]",
                           'NARRATOR: '+' '.join(spoken),''])
    (main_dir/'screenplay.txt').write_text('\n'.join(screenplay))
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'output':str(target),'duration_seconds':length,
                      'uncut_films':len(report['clips']),'video_streams_unchanged':True,
                      'max_tempo':max([a['tempo'] for a in report['speech_adjustments']]+[tempo])}))


if __name__=='__main__':main()
