"""Mix the narration, the score (ducked under the voice) and the reaction sounds.

Reads scene_times.json, voice/<scene>.wav, score.wav and sfx.wav; writes mix.wav.
"""

import json
import subprocess

marks = json.load(open("scene_times.json"))[:-1]
LEAD = 0.25  # the narrator starts just after each cut

inputs = ["-i", "score.wav", "-i", "sfx.wav"]
delays = []
for i, (name, start) in enumerate(marks):
    inputs += ["-i", f"voice/{name}.wav"]
    ms = int((start + LEAD) * 1000)
    delays.append(f"[{i + 2}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]")

k = len(marks)
graph = ";".join(delays + [
    f"{''.join(f'[v{i}]' for i in range(k))}amix=inputs={k}:normalize=0,volume=1.5,asplit=2[voice][key]",
    "[0:a]volume=0.75[music]",
    "[music][key]sidechaincompress=threshold=0.03:ratio=5:attack=40:release=500[ducked]",
    "[1:a]volume=0.55[fx]",
    "[voice][ducked][fx]amix=inputs=3:normalize=0,alimiter=limit=0.9,loudnorm=I=-16:TP=-1.5:LRA=11[out]",
])
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph,
                "-map", "[out]", "-ar", "44100", "mix.wav"], check=True)
print("wrote mix.wav")
