"""Quiet ambient score that follows the scenes of self_healing.py.

Reads scene_times.json (written by the render) and writes music.wav: a soft pad
whose chord changes with each scene, a low root under it, a small bell at each
scene change, and a few plucks where bugs are caught and fixed.
"""

import json
import wave

import numpy as np

SR = 44100
marks = json.load(open("scene_times.json"))
total = marks[-1][1] + 0.5
n = int(total * SR)
t = np.arange(n) / SR
out = np.zeros(n)


def hz(note):
    names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7,
             "G#": 8, "A": 9, "A#": 10, "B": 11}
    name, octave = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((names[name] + 12 * (octave + 1) - 69) / 12)


# One chord per scene, in D major, low and slow; the bug scenes lean minor and
# the closing resolves.
CHORDS = {
    "opening": ["D2", "A2", "F#3", "E4"],        # D add9
    "nets": ["G2", "D3", "B3", "F#4"],           # Gmaj7
    "door": ["E2", "B2", "G3", "D4"],            # Em7
    "promise": ["D2", "A2", "F#3", "E4"],        # D add9
    "walk": ["A1", "E2", "C#3", "B3"],           # A add9
    "goal": ["B1", "F#2", "D3", "A3"],           # Bm7, a bug
    "goal_fix": ["G2", "D3", "B3", "F#4"],       # Gmaj7, the fix
    "proof": ["E2", "B2", "G3", "D4"],           # Em7
    "freeze": ["F#2", "C#3", "A3", "E4"],        # F#m7, a stall
    "freeze_fix": ["A2", "E3", "B3", "D4"],      # Asus
    "secrets": ["B1", "F#2", "D3", "A3"],        # Bm7
    "secrets_fix": ["G2", "D3", "A3", "B3"],     # Gadd9
    "decide": ["E2", "B2", "G3", "D4"],          # Em7
    "closing": ["D2", "A2", "E3", "F#4"],        # D add9, resolve
    "credits": ["D2", "A2", "E3", "F#4"],        # the same chord, held under the credits
}


def envelope(start, end, fade=1.6):
    e = np.zeros(n)
    a, b = int(start * SR), min(int(end * SR), n)
    seg = np.ones(b - a)
    f = int(fade * SR)
    seg[:f] = np.linspace(0, 1, min(f, len(seg)))[: len(seg[:f])]
    seg[-f:] = np.minimum(seg[-f:], np.linspace(1, 0, min(f, len(seg))))
    e[a:b] = seg
    return e


def pad_voice(freq, env):
    # slightly detuned sines with a soft second harmonic, slow vibrato
    vib = 1 + 0.002 * np.sin(2 * np.pi * 0.2 * t)
    v = (np.sin(2 * np.pi * freq * vib * t)
         + 0.6 * np.sin(2 * np.pi * freq * 1.003 * t)
         + 0.15 * np.sin(2 * np.pi * 2 * freq * t))
    return v * env


def pluck(at, freq, amp=0.35, decay=1.8):
    a = int(at * SR)
    if a >= n:
        return
    length = min(int(decay * 3 * SR), n - a)
    tt = np.arange(length) / SR
    tone = (np.sin(2 * np.pi * freq * tt) + 0.3 * np.sin(2 * np.pi * 2 * freq * tt))
    out[a:a + length] += amp * tone * np.exp(-tt / decay * 2.5) * np.minimum(1, tt * 200)


def tick(at, amp=0.12):
    a = int(at * SR)
    length = min(int(0.08 * SR), n - a)
    if length <= 0:
        return
    tt = np.arange(length) / SR
    noise = np.random.default_rng(int(at * 1000)).standard_normal(length)
    body = np.sin(2 * np.pi * 1800 * tt)
    out[a:a + length] += amp * (0.4 * noise + body) * np.exp(-tt * 70)


spans = list(zip(marks[:-1], marks[1:]))
for (name, start), (_, end) in spans:
    env = envelope(max(0, start - 0.8), end + 0.8)
    for note in CHORDS[name]:
        out += 0.09 * pad_voice(hz(note), env)
    # a low root an octave down, for warmth
    out += 0.07 * pad_voice(hz(CHORDS[name][0]) / 2, env)
    # a bell on the root, two octaves up, at each scene change
    if name != "credits":
        pluck(start + 0.05, hz(CHORDS[name][0]) * 4, amp=0.22, decay=2.5)

times = dict(marks)

# beats.json (written by the render) holds the moments the score answers:
# "catch" a bug caught by a net, "tick" a map line checked, "arp" the walk
# ending, "sour" a bug showing itself, "fix" a fix landing.
beats = json.load(open("beats.json"))
notes = ["A4", "B4", "D5", "E5", "F#5", "A5"]
for i, at in enumerate(beats.get("catch", [])):
    pluck(at, hz(notes[i % len(notes)]), amp=0.09, decay=1.2)
for at in beats.get("tick", []):
    tick(at, amp=0.05)
for at in beats.get("arp", []):
    for i, note in enumerate(["A4", "C#5", "E5", "A5"]):
        pluck(at + i * 0.45, hz(note), amp=0.11, decay=1.2)
for at in beats.get("sour", []):
    pluck(at, hz("F2"), amp=0.2, decay=2.5)
for at in beats.get("fix", []):
    pluck(at, hz("F#5"), amp=0.12, decay=2.0)
    pluck(at + 0.45, hz("A5"), amp=0.10, decay=2.0)

# closing: final resolving chime
pluck(times["closing"] + 1.5, hz("D5"), amp=0.18, decay=3.0)
pluck(times["closing"] + 2.5, hz("A5"), amp=0.13, decay=3.0)

fade_out = np.ones(n)
f = int(3.0 * SR)
fade_out[-f:] = np.linspace(1, 0, f)
out *= fade_out
fade_in = np.minimum(1, t / 1.5)
out *= fade_in

# gentle low-pass (one-pole) to soften, then normalise quietly (peak -18 dBFS)
y = np.zeros_like(out)
alpha = 0.12
acc = 0.0
for i in range(0, n, 1):
    acc += alpha * (out[i] - acc)
    y[i] = acc
y = y / np.max(np.abs(y)) * 10 ** (-20 / 20)

stereo = np.stack([y, np.roll(y, int(0.012 * SR))], axis=1)
pcm = (stereo * 32767).astype(np.int16)
with wave.open("music.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote music.wav", round(total, 1), "s")
