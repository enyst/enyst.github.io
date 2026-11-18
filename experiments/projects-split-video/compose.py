"""Hold each slide for its narration (slow push-in), add a title, mix voice + low score."""
import json, subprocess, sys
SC = ["intro", "test", "guard", "ask", "tags", "check", "keep", "close"]
PY = sys.executable
dur = json.load(open("voice/durations.json"))
def run(a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
parts = []; t = 0; times = {}
for i, name in enumerate(SC):
    D = round(dur[name] + 1.2, 2); out = f"seg{i}.mp4"; times[name] = (t, D)
    vf = (f"scale=1920:1080,setsar=1,zoompan=z='1+0.0002*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":d={int(D*30)}:s=1920x1080:fps=30,fade=t=in:st=0:d=0.4,fade=t=out:st={D-0.4}:d=0.4")
    run(["-loop", "1", "-i", f"slide-{name}.png", "-t", str(D), "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", out])
    parts.append(out); t += D
open("list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
run(["-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "picture.mp4"])
total = t; json.dump(times, open("scene_times.json", "w"), indent=1)
subprocess.run([PY, "score.py", str(total + 1)], check=True)
ins = []; flt = []
for j, name in enumerate(SC):
    ins += ["-i", f"voice/{name}.wav"]; ms = int((times[name][0] + 0.5) * 1000)
    flt.append(f"[{j}:a]aresample=48000,adelay={ms}|{ms},pan=stereo|c0=c0|c1=c0[a{j}]")
n = len(SC)
fc = ";".join(flt) + ";" + "".join(f"[a{j}]" for j in range(n)) + f"amix=inputs={n}:normalize=0[v];[{n}:a]volume=0.11[s];[v][s]amix=inputs=2:normalize=0,alimiter=limit=0.95[out]"
run([*ins, "-i", "score.wav", "-filter_complex", fc, "-map", "[out]", "-t", str(total), "-c:a", "pcm_s16le", "mix.wav"])
run(["-i", "picture.mp4", "-i", "mix.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", "../projects-split.mp4"])
print("total", round(total, 1))
# After compose.py: ffmpeg -i ../projects-split.mp4 -c:v libx264 -crf 30 -preset slow -tune stillimage -c:a copy -movflags +faststart projects-split.mp4
