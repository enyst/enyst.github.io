"""Lay the screen recordings under the Manim layer, then add the sound.

    python compose.py media/videos/reactions/1080p30/Reactions.mov

Reads scene_times.json and marks.json (from the render), clips/*.mp4,
voice/*.wav (narration.py) and score.wav (score.py). Writes reactions.mp4.
"""

import json
import os
import subprocess
import sys

from plan import CLIP_SCALE, CLIP_X, CLIP_Y, CLIPS

BG = "0x111318"
FPS = 30
overlay = sys.argv[1]
marks = json.load(open("scene_times.json"))
os.makedirs("build", exist_ok=True)


def run(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


pieces = []
for (name, start), (_, end) in zip(marks[:-1], marks[1:]):
    length = round(end - start, 3)
    out = f"build/{name}.mp4"
    if name in CLIPS:
        c = CLIPS[name]
        parts, labels = [], []
        for i, (a, b, speed) in enumerate(c["segs"]):
            parts.append(f"[1:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{speed},fps={FPS}[s{i}]")
            labels.append(f"[s{i}]")
        w, h = int(1600 * CLIP_SCALE), int(900 * CLIP_SCALE)
        graph = ";".join(parts + [
            f"{''.join(labels)}concat=n={len(labels)}:v=1:a=0,scale={w}:{h}:flags=lanczos,"
            f"tpad=stop_mode=clone:stop_duration={length},setpts=PTS+{c['offset']}/TB[clip]",
            f"[0:v][clip]overlay=x={CLIP_X}:y={CLIP_Y}:eof_action=repeat:enable='gte(t,{c['offset']})'[v]",
        ])
        run("-f", "lavfi", "-i", f"color=c={BG}:s=1920x1080:r={FPS}:d={length}", "-i", c["src"],
            "-filter_complex", graph, "-map", "[v]", "-t", str(length),
            "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", out)
    else:
        run("-f", "lavfi", "-i", f"color=c={BG}:s=1920x1080:r={FPS}:d={length}",
            "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", out)
    pieces.append(out)

with open("build/list.txt", "w") as f:
    f.writelines(f"file '{os.path.basename(p)}'\n" for p in pieces)
run("-f", "concat", "-safe", "0", "-i", "build/list.txt", "-c", "copy", "build/base.mp4")

# picture: base, Manim on top; sound: mix.wav from mix.py
run("-i", "build/base.mp4", "-i", overlay, "-i", "mix.wav",
    "-filter_complex", "[1:v]scale=1920:1080[o];[0:v][o]overlay=0:0:shortest=0[v]",
    "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "20", "-preset", "slow",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
    "-shortest", "reactions.mp4")
print("wrote reactions.mp4")
