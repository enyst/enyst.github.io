"""Fit each section's recorded clips to its narration, add a title, mix voice + a quiet score."""
import json, subprocess, sys, os
E = "/tmp/openhands-verify/2026-11-10T1733-206791/evidence/"
SEC = {
 "s1": ("Turn Projects on", [(E+"S1/turn-on2.mp4", 0, 11.2), (E+"B3/profiles.mp4", 0, 23.6)]),
 "s2": ("Project 1: an SDK bug bash", [(E+"P1/create-and-brief.mp4", 0, 47.4), (E+"P1/finale.mp4", 0, 9.5), (E+"P1/follow-up.mp4", 0, 28.6), (E+"B9/banner-reopen.mp4", 0, 9.9)]),
 "s3": ("Project 2: scoped secrets", [(E+"P2/create-and-brief.mp4", 0, 43.7), (E+"P2/wait-actually.mp4", 0, 8), (E+"P2/wait-actually.mp4", 30, 60.8), (E+"P2/finale.mp4", 0, 35.7)]),
 "s4": ("Project 3: Insider", [(E+"P3/install-insider.mp4", 0, 48), (E+"P3/install-insider.mp4", 140, 207), (E+"P3/board.mp4", 0, 5.3), (E+"P3/finale.mp4", 0, 38.5)]),
 "s5": ("Project files and memory", [(E+"B12/upload-and-read.mp4", 0, 26.2)]),
 "s6": ("Agent Server restarts", [(E+"B15/restart.mp4", 0, 30), (E+"B15/restart-14b3f7c.mp4", 0, 51.5)]),
 "s7": ("Turn Projects off", [(E+"B16/flag-off-on.mp4", 0, 18.6)]),
}
dur = json.load(open("voice/durations.json"))
BG = "0xF4EFE6"; FIT = f"scale=-2:1080,pad=1920:1080:(ow-iw)/2:0:color={BG},setsar=1,fps=30"
FONT_B = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"; FONT = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
def run(a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
os.makedirs("out", exist_ok=True)
for key in (sys.argv[1:] or SEC):
    title, segs = SEC[key]
    D = round(dur[key] + 1.6, 2)
    L0 = sum(b - a for _, a, b in segs); sp = max(1.0, L0 / D)
    ins, fl = [], []
    for j, (f, a, b) in enumerate(segs):
        ins += ["-i", f]; fl.append(f"[{j}:v]trim={a}:{b},setpts=PTS-STARTPTS,{FIT}[c{j}]")
    n = len(segs)
    t = title.replace(":", "\\:")
    TITLE = (f",drawbox=x=0:y=900:w=1920:h=180:color={BG}@0.93:t=fill:enable='lt(t,4)',"
             f"drawtext=fontfile={FONT_B}:text='{t}':fontsize=60:fontcolor=0x2b2722:x=(w-tw)/2:y=930:enable='lt(t,4)',"
             f"drawtext=fontfile={FONT}:text='A live OpenHands Projects run, sped up {sp:.1f}x where the agents work':fontsize=28:fontcolor=0x6b625a:x=(w-tw)/2:y=1010:enable='lt(t,4)'")
    fc = ";".join(fl) + ";" + "".join(f"[c{j}]" for j in range(n)) + f"concat=n={n}:v=1:a=0,setpts=PTS/{sp},tpad=stop_mode=clone:stop_duration={D}{TITLE}[v]"
    run([*ins, "-filter_complex", fc, "-map", "[v]", "-t", str(D), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "22", f"out/{key}-picture.mp4"])
    subprocess.run([sys.executable, "src/score.py", str(D + 0.5)], check=True)
    ms = 600
    fca = f"[0:a]aresample=48000,adelay={ms}|{ms},pan=stereo|c0=c0|c1=c0[v];[1:a]volume=0.12[s];[v][s]amix=inputs=2:normalize=0,alimiter=limit=0.95[out]"
    run(["-i", f"voice/{key}.wav", "-i", "score.wav", "-filter_complex", fca, "-map", "[out]", "-t", str(D), "-c:a", "pcm_s16le", f"out/{key}-mix.wav"])
    run(["-i", f"out/{key}-picture.mp4", "-i", f"out/{key}-mix.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", f"out/{key}.mp4"])
    run(["-ss", "5", "-i", f"out/{key}-picture.mp4", "-frames:v", "1", "-vf", "scale=960:-1", f"out/{key}-poster.jpg"])
    print(key, D, "speed", round(sp, 2), flush=True)
