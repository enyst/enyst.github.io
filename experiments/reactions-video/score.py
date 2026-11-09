"""A low, light score and the reaction sounds, synthesized with numpy (no samples).

Reads scene_times.json and marks.json (written by the render) and writes
score.wav (music) and sfx.wav (the crisp pop of each reaction, and the click
of the switch). mix.py lays them under the narration.
"""

import json
import wave

import numpy as np

SR = 44100
marks = json.load(open("scene_times.json"))
moments = json.load(open("marks.json"))
total = marks[-1][1] + 0.3
n = int(total * SR)
t = np.arange(n) / SR


def hz(note):
    names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7,
             "G#": 8, "A": 9, "A#": 10, "B": 11}
    name, octave = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((names[name] + 12 * (octave + 1) - 69) / 12)


# one chord per scene, in F major; the "wait, actually" turn leans on the IV,
# the heart lands on the tonic
CHORDS = {
    "hook": ["F2", "C3", "A3", "E4"],
    "flag": ["D2", "A2", "F3", "C4"],
    "setup": ["A#1", "F2", "D3", "A3"],
    "ask": ["F2", "C3", "A3", "E4"],
    "thumbs": ["A#1", "F2", "D3", "A3"],
    "done": ["C2", "G2", "E3", "A#3"],
    "restore": ["D2", "A2", "F3", "C4"],
    "closing": ["F2", "C3", "A3", "G4"],
}


def env(start, end, fade=1.2, length=n):
    e = np.zeros(length)
    a, b = int(start * SR), min(int(end * SR), length)
    seg = np.ones(b - a)
    f = min(int(fade * SR), len(seg) // 2)
    seg[:f] = np.linspace(0, 1, f)
    seg[-f:] = np.minimum(seg[-f:], np.linspace(1, 0, f))
    e[a:b] = seg
    return e


def pluck(buf, at, freq, amp, decay=0.6, bright=0.3):
    a = int(at * SR)
    if a >= len(buf):
        return
    m = min(int(decay * 4 * SR), len(buf) - a)
    tt = np.arange(m) / SR
    tone = np.sin(2 * np.pi * freq * tt) + bright * np.sin(2 * np.pi * 2 * freq * tt) \
        + 0.12 * np.sin(2 * np.pi * 3 * freq * tt)
    buf[a:a + m] += amp * tone * np.exp(-tt / decay * 3) * np.minimum(1, tt * 400)


music = np.zeros(n)
spans = list(zip(marks[:-1], marks[1:]))
for (name, start), (_, end) in spans:
    e = env(max(0, start - 0.6), end + 0.6)
    vib = 1 + 0.0025 * np.sin(2 * np.pi * 0.25 * t)
    for note in CHORDS[name]:
        f = hz(note)
        music += 0.07 * e * (np.sin(2 * np.pi * f * vib * t) + 0.5 * np.sin(2 * np.pi * f * 1.004 * t))

# a light marimba-like ostinato at 100 bpm, eighth notes, following the chords
beat = 60 / 100 / 2
pattern = [0, 2, 1, 3, 2, 1, 3, 2]
for (name, start), (_, end) in spans:
    if name == "closing":
        continue
    tones = [hz(x) * 4 for x in CHORDS[name][1:]] + [hz(CHORDS[name][0]) * 8]
    k = 0
    at = start + 0.2
    while at < end - 0.1:
        pluck(music, at, tones[pattern[k % 8]], 0.05 if k % 2 else 0.075, decay=0.35)
        at += beat
        k += 1

# closing: a slow rising arpeggio that resolves
c0 = dict(marks)["closing"]
for i, note in enumerate(["F4", "A4", "C5", "E5", "F5"]):
    pluck(music, c0 + 0.4 + i * 0.45, hz(note), 0.12, decay=1.6)

fade = np.ones(n)
fade[-int(2.5 * SR):] = np.linspace(1, 0, int(2.5 * SR))
music *= fade * np.minimum(1, t / 1.0)

# soften: one-pole low-pass
y = np.empty_like(music)
acc = 0.0
alpha = 0.18
for i in range(n):
    acc += alpha * (music[i] - acc)
    y[i] = acc
music = y / np.max(np.abs(y)) * 10 ** (-20 / 20)

# ---------------------------------------------------------------- sound effects
sfx = np.zeros(n)
rng = np.random.default_rng(7)


def pop(at, base=1250, amp=0.5):
    """Crisp: a quick upward chirp, a bright click and a tiny bell."""
    a = int(at * SR)
    m = int(0.35 * SR)
    tt = np.arange(m) / SR
    freq = base + 700 * (1 - np.exp(-tt / 0.012))  # a quick upward flick
    chirp = np.sin(2 * np.pi * np.cumsum(freq) / SR)
    body = chirp * np.exp(-tt * 45)
    click = rng.standard_normal(m) * np.exp(-tt * 900)
    click = np.diff(click, prepend=0)  # high-passed: crisp, not thumpy
    bell = (np.sin(2 * np.pi * base * 2 * tt) + 0.4 * np.sin(2 * np.pi * base * 3.01 * tt)) * np.exp(-tt * 14)
    sfx[a:a + m] += amp * (0.8 * body + 0.35 * click + 0.25 * bell)


def tick(at, amp=0.3):
    a = int(at * SR)
    m = int(0.05 * SR)
    tt = np.arange(m) / SR
    sfx[a:a + m] += amp * (np.sin(2 * np.pi * 2200 * tt) + 0.5 * rng.standard_normal(m)) * np.exp(-tt * 160)


pop(moments["hook_pop"], 1250, 0.55)
tick(moments["flag_switch"])
pop(moments["thumbs_pop"], 1250, 0.6)
pop(moments["heart_pop"], 880, 0.5)
sfx = sfx / np.max(np.abs(sfx)) * 10 ** (-6 / 20)


def write(name, mono, delay=0.0):
    st = np.stack([mono, np.roll(mono, int(delay * SR))], axis=1)
    with wave.open(name, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


write("score.wav", music, 0.012)
write("sfx.wav", sfx)
print("wrote score.wav and sfx.wav", round(total, 1), "s")
