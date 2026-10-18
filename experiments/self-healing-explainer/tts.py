import re, json, sys, numpy as np, soundfile as sf
from kokoro import KPipeline
SR=24000
text=open(sys.argv[1]).read()
segs=re.findall(r'^## \d+\. (.+?)\n(.+?)(?=\n## |\Z)', text, re.S|re.M)
fix=lambda s: s.replace('control-openhands','control open hands').replace('OpenHands','Open Hands').replace('known-bug','known bug')
p=KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
out=[]
for i,(title,para) in enumerate(segs,1):
    sents=re.split(r'(?<=[.?!])\s+', para.strip())
    audio=[np.zeros(int(0.3*SR))]; t=0.3; marks=[]
    for s in sents:
        a=np.concatenate([x for _,_,x in p(fix(s), voice='af_heart', speed=0.95)])
        marks.append({'text':s,'start':round(t,3),'end':round(t+len(a)/SR,3)})
        gap=0.55 if s.endswith(('.','?')) else 0.3
        audio += [a, np.zeros(int(gap*SR))]; t+=len(a)/SR+gap
    audio.append(np.zeros(int(0.4*SR)))
    y=np.concatenate(audio); sf.write(f'seg{i:02d}.wav', y, SR)
    out.append({'id':i,'title':title,'dur':round(len(y)/SR,3),'sents':marks})
    print(i, title, round(len(y)/SR,1), flush=True)
json.dump(out, open('timings.json','w'), indent=1)
