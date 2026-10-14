import json,math,re
from pathlib import Path
def rgb(c):
 v=list(map(float,re.findall(r'[-+]?\d*\.?\d+',c)))
 if c.startswith('rgb'): return [n/255 for n in v[:3]]
 if c.startswith('oklch'):
  L,C,h=v;h=math.radians(h);a=C*math.cos(h);b=C*math.sin(h)
  l=(L+.3963377774*a+.2158037573*b)**3;m=(L-.1055613458*a-.0638541728*b)**3;s=(L-.0894841775*a-1.2914855480*b)**3
  linear=[4.0767416621*l-3.3077115913*m+.2309699292*s,-1.2684380046*l+2.6097574011*m-.3413193965*s,-.0041960863*l-.7034186147*m+1.7076147010*s]
  return [max(0,min(1,12.92*x if x<=.0031308 else 1.055*x**(1/2.4)-.055)) for x in linear]
 raise ValueError(c)
def luminance(c):
 x=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb(c)]
 return sum(a*b for a,b in zip(x,[.2126,.7152,.0722]))
def ratio(fg,bg):
 a,b=sorted([luminance(fg),luminance(bg)])
 return (b+.05)/(a+.05)
data={}
for phase in ['before','after']:
 for r in json.load(open('/tmp/odie-theme-errors-'+phase+'-evidence.json')):
  if 'style' not in r:continue
  s=r['style']; fg=s['border' if r['target']=='field-border' else 'color'];bg=s['background'][0]['color']
  data.setdefault((r['theme'],r['target']),{})[phase]={'foreground':fg,'background':bg,'ratio':round(ratio(fg,bg),2)}
rows=['| Theme | Element | Before | After |','| --- | --- | ---: | ---: |']
for (theme,target),p in data.items():rows.append(f"| {theme} | {target} | {p['before']['ratio']:.2f}:1 | {p['after']['ratio']:.2f}:1 |")
text='\n'.join(rows)+'\n'
Path('/tmp/odie-theme-errors-contrast.md').write_text(text)
Path('/tmp/odie-theme-errors-contrast.json').write_text(json.dumps([{'theme':theme,'target':target,**p} for (theme,target),p in data.items()],indent=2))
print(text)
