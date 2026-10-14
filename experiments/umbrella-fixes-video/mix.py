"""Mix narration and music onto the rendered video.

Reads scene_times.json (from the render), voice/<scene>.wav (from narration.py)
and music.wav (from music.py). Each narration clip starts with its scene; the
music ducks under the voice. Writes umbrella-fixes.mp4.

    python mix.py media/videos/umbrella_fixes/1080p30/UmbrellaFixes.mp4
"""

import json
import subprocess
import sys

video = sys.argv[1]
marks = json.load(open("scene_times.json"))[:-1]

inputs = ["-i", video, "-i", "music.wav"]
delays = []
for i, (name, start) in enumerate(marks):
    inputs += ["-i", f"voice/{name}.wav"]
    ms = int(start * 1000)
    delays.append(f"[{i + 2}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]")

n = len(marks)
voice_mix = "".join(f"[v{i}]" for i in range(n))
graph = ";".join(delays + [
    f"{voice_mix}amix=inputs={n}:normalize=0,volume=1.4,asplit=2[voice][key]",
    "[1:a]volume=0.7[music]",
    "[music][key]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600[ducked]",
    "[voice][ducked]amix=inputs=2:normalize=0,alimiter=limit=0.9[aout]",
])

subprocess.run(
    ["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph,
     "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-crf", "22", "-preset", "slow",
     "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
     "-shortest", "umbrella-fixes.mp4"],
    check=True,
)
print("wrote umbrella-fixes.mp4")
