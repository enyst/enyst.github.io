"""A quiet, low score for Feature Map Daily: warm pads, a soft bass and a few bells.

Everything is synthesized here from sine partials (no samples). The chords
change with the film's scenes (see T in video.html), and a soft bell marks
each scene change. The mix stays low so it sits under the picture.

    python3 score.py score.wav
"""

import sys
import wave

import numpy as np

SR = 48000
DUR = 125.0
N = int(SR * DUR)
out = np.zeros((2, N))


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# A minor-ish, open and low: Am, F, C, G, Dm voicings.
CHORDS = {
    "Am": [45, 52, 57, 60, 64],
    "F": [41, 48, 53, 57, 60],
    "C": [48, 55, 60, 64, 67],
    "G": [43, 50, 55, 59, 62],
    "Dm": [38, 50, 53, 57, 62],
    "Fmaj7": [41, 48, 52, 57, 64],
}
# (start, chord); scene starts from video.html: 0 title, 6 map, 20 daily,
# 34 results, 50 zoom, 62 story, 74.5 settings, 90.5 card, 104.5 code, 118.5 end
PROG = [
    (0, "Am"), (6, "F"), (13, "C"), (20, "G"), (27, "Am"), (34, "F"), (42, "C"),
    (50, "Dm"), (56, "Fmaj7"), (62, "Am"), (68, "G"), (74.5, "F"), (82.5, "C"),
    (90.5, "Dm"), (97.5, "G"), (104.5, "Am"), (111.5, "F"), (118.5, "C"), (122, "Am"),
]
CUES = [6, 20, 34, 50, 62, 74.5, 90.5, 104.5, 118.5]

t = np.arange(N) / SR


def env_ad(n, attack, release):
    e = np.ones(n)
    a = min(n, int(attack * SR))
    r = min(n - a, int(release * SR))
    e[:a] = np.linspace(0, 1, a, endpoint=False) ** 2
    if r > 0:
        e[n - r:] *= np.linspace(1, 0, r) ** 2
    return e


# Pads: each chord crossfades into the next over ~2.5 s.
for i, (t0, name) in enumerate(PROG):
    t1 = PROG[i + 1][0] if i + 1 < len(PROG) else DUR
    a, b = int(t0 * SR), min(N, int((t1 + 2.5) * SR))
    seg = np.arange(b - a) / SR
    e = env_ad(b - a, 2.5, 2.5)
    for j, m in enumerate(CHORDS[name]):
        f = hz(m)
        for side, det in ((0, -0.12), (1, 0.12)):
            ph = (j * 1.3 + side) % (2 * np.pi)
            v = np.sin(2 * np.pi * (f + det) * seg + ph)
            v += 0.25 * np.sin(2 * np.pi * 2 * (f + det) * seg + ph)  # a little warmth
            vib = 1 + 0.08 * np.sin(2 * np.pi * (0.07 + 0.01 * j) * seg)
            out[side, a:b] += 0.022 * e * v * vib

# Bass: the chord root an octave down, slow breathing.
for i, (t0, name) in enumerate(PROG):
    t1 = PROG[i + 1][0] if i + 1 < len(PROG) else DUR
    a, b = int(t0 * SR), min(N, int((t1 + 1.5) * SR))
    seg = np.arange(b - a) / SR
    f = hz(CHORDS[name][0] - 12)
    e = env_ad(b - a, 1.2, 1.8) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.12 * seg))
    v = np.sin(2 * np.pi * f * seg) + 0.15 * np.sin(2 * np.pi * 2 * f * seg)
    out[:, a:b] += 0.05 * e * v

# Bells at scene changes: a soft fifth above the chord's top note.
for c in CUES:
    name = [n for t0, n in PROG if t0 <= c][-1]
    f = hz(CHORDS[name][-1] + 7)
    a = int(c * SR)
    n = min(N - a, int(4.5 * SR))
    seg = np.arange(n) / SR
    e = np.exp(-seg * 1.3) * (1 - np.exp(-seg * 120))
    v = np.sin(2 * np.pi * f * seg) + 0.4 * np.sin(2 * np.pi * 2.76 * f * seg) * np.exp(-seg * 2.5)
    out[0, a:a + n] += 0.03 * e * v
    out[1, a:a + n] += 0.026 * e * v

# Gentle low-pass (a short Hann FIR) and a long fade in/out.
kern = np.hanning(25)
kern /= kern.sum()
for ch in range(2):
    out[ch] = np.convolve(out[ch], kern, mode="same")
fade = np.ones(N)
fade[: int(2 * SR)] = np.linspace(0, 1, int(2 * SR)) ** 2
fade[-int(4 * SR):] = np.linspace(1, 0, int(4 * SR)) ** 2
out *= fade
out /= np.max(np.abs(out)) / 0.5  # peak at -6 dBFS; render.mjs lowers it further

pcm = (np.clip(out.T, -1, 1) * 32767).astype("<i2")
with wave.open(sys.argv[1] if len(sys.argv) > 1 else "score.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", sys.argv[1] if len(sys.argv) > 1 else "score.wav", f"{DUR}s")
