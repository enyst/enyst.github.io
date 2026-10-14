"""Generate the film's quiet score: warm pads, soft plucked arpeggios, a few bells.

Everything is synthesized here from sine partials (no samples, nothing
borrowed), so the music is as open as the rest of the film. Cues follow the
shot timings in video.html / storyboard.md; the music holds its breath with
the character before the replay and before the twist (anticipation in sound).

    python3 score.py score.wav
"""

import sys
import wave

import numpy as np

SR = 48000
DUR = 149.5
N = int(SR * DUR)
rng = np.random.default_rng(1)
out = np.zeros((2, N))


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


CHORDS = {  # D major, voiced low and open
    "D": [50, 57, 61, 64, 66],
    "Bm": [47, 54, 57, 62, 66],
    "G": [43, 50, 54, 59, 62],
    "A": [45, 52, 57, 59, 64],  # A sus2-ish: a gentle dominant, never harsh
    "Em": [40, 47, 54, 57, 62],
}
# (start time, chord); each lasts until the next.
PROG = [
    (0, "D"), (4.5, "Bm"), (9, "G"), (13, "A"),
    (17.5, "D"), (22, "Bm"), (27, "G"), (31.5, "A"), (36, "D"),
    (40.5, "G"), (45, "Em"), (49.5, "A"),
    (54, "Bm"), (58.5, "A"), (59.8, "D"),
    (65.5, "G"), (69.5, "Em"), (73.5, "A"),
    (77.5, "Bm"), (79.4, "A"), (80.5, "D"), (84.5, "G"), (86.1, "D"),
    (91.5, "Bm"), (96, "G"), (100, "A"),
    (103.5, "Bm"), (106, "Em"), (107.4, "A"), (108.4, "D"), (112, "G"),
    (115.5, "D"), (119.5, "Bm"), (124.5, "G"), (129, "A"),
    (133, "D"), (137.5, "G"), (141, "A"), (143.5, "D"),
]


def chord_at(t):
    name = PROG[0][1]
    for t0, c in PROG:
        if t >= t0:
            name = c
    return CHORDS[name]


def curve(points):
    xs, ys = zip(*points)
    return lambda t: np.interp(t, xs, ys)


# Overall pad level: quiet, swelling a little with the story; ducks to hold its breath.
pad_level = curve([
    (0, 0), (2, .45), (9, .5), (17.5, .55), (27, .6), (54, .62), (65.5, .7), (77.5, .72),
    (79.2, .7), (79.6, .3), (80.4, .3), (81, .8), (91.5, .65), (103.5, .6), (107.2, .6),
    (107.6, .3), (108.3, .3), (108.7, .75), (115.5, .62), (124.5, .55), (133, .6),
    (143.5, .55), (147, .3), (149.5, 0),
])


def add(sig, start, pan=0.0):
    i0 = int(start * SR)
    if i0 >= N:
        return
    if i0 < 0:
        sig, i0 = sig[-i0:], 0
    sig = sig[: N - i0]
    left, right = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    out[0, i0:i0 + len(sig)] += sig * left
    out[1, i0:i0 + len(sig)] += sig * right


def pad():
    bounds = [t for t, _ in PROG] + [DUR]
    for k, (t0, name) in enumerate(PROG):
        t1 = bounds[k + 1]
        att, rel = 1.4, 2.6
        n = int((t1 - t0 + rel) * SR)
        t = np.arange(n) / SR
        env = np.minimum(1, t / att) ** 2 * np.where(t < t1 - t0, 1, np.exp(-(t - (t1 - t0)) / (rel / 4)))
        env *= pad_level(t0 + t)
        env *= np.clip((n / SR - t) / .25, 0, 1)  # no click at the tail
        for j, m in enumerate(CHORDS[name]):
            for det, pan in ((-3, -.6), (3, .6)):  # two voices, slightly detuned, spread wide
                f = hz(m) * 2 ** (det / 1200)
                ph = rng.uniform(0, 2 * np.pi)
                lfo = 1 + .08 * np.sin(2 * np.pi * .13 * t + j)
                s = (np.sin(2 * np.pi * f * t + ph) + .22 * np.sin(4 * np.pi * f * t + ph) + .07 * np.sin(6 * np.pi * f * t))
                add(.05 * s * env * lfo, t0, pan * (.4 + .12 * j))
        # a soft sub under the root
        root = hz(CHORDS[name][0] - 12)
        add(.07 * np.sin(2 * np.pi * root * t) * env, t0, 0)


def pluck(t0, m, vel=1.0, pan=0.0, dur=1.8):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = hz(m)
    env = np.minimum(1, t / .004) * np.exp(-t * 3.2)
    s = np.sin(2 * np.pi * f * t) + .28 * np.sin(4 * np.pi * f * t) * np.exp(-t * 5) + .08 * np.sin(6 * np.pi * f * t) * np.exp(-t * 8)
    add(.06 * vel * s * env, t0, pan)


def bell(t0, m, vel=1.0, pan=0.0):
    n = int(5 * SR)
    t = np.arange(n) / SR
    f = hz(m)
    s = np.zeros(n)
    for ratio, amp, dec in ((1, 1, 2.2), (2, .35, 1.4), (2.76, .25, 1.0), (5.4, .08, .5)):
        s += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t / dec)
    add(.07 * vel * s * np.minimum(1, t / .003), t0, pan)


BEAT = 60 / 72


def arp(t0, t1, step, vel, octave=12, rising=False):
    """Chord tones from the current chord, an octave or two up, cycling upward."""
    t, k = t0, 0
    while t < t1:
        tones = sorted(set(m + octave for m in chord_at(t)[1:]) | set(m + octave + 12 for m in chord_at(t)[1:3]))
        if rising:  # climbs across the span: straight ahead, like the replay columns filling
            p = (t - t0) / (t1 - t0)
            idx = min(len(tones) - 1, int(p * len(tones) * 1.0 + (k % 2)))
            m = tones[idx]
        else:
            m = tones[[0, 2, 1, 3, 2, 4, 1, 3][k % 8] % len(tones)]
        v = vel * (1 if k % 4 == 0 else .72) * (.92 + .16 * rng.random())
        pluck(t, m, v, pan=(-.5 if k % 2 else .5) * .7)
        t += step
        k += 1


pad()
# 1 hook: almost nothing; a low bell under the question
bell(6.4, 62, .7, -.1)
# 2 gap: a few notes, like the scattered spotlights
for i, t in enumerate((9.5, 10.3, 11.1)):
    bell(t, [69, 74, 78][i], .35, [-.6, 0, .6][i])
arp(12.8, 17.2, 2 * BEAT, .45)
# 3 meet the map: the unfold blooms into a strummed chord
for j, m in enumerate([62, 66, 69, 73, 76]):
    pluck(19.5 + j * .045, m + 12, .9, -.6 + .3 * j)
arp(21.0, 27.0, BEAT, .55)
# 4–5 the CLI and the map: steady, like typing
arp(27.0, 54.0, BEAT / 2, .5)
# 6 known bugs: XPASS bursts open
arp(54.0, 59.5, BEAT / 2, .48)
bell(59.8, 81, .8, .4)
arp(60.6, 65.5, BEAT / 2, .5)
# 7 the swarm: busier, overlapping
arp(65.5, 77.4, BEAT / 4, .42)
arp(65.5 + BEAT / 8, 77.4, BEAT, .35, octave=24)
# 8 the reveal: silence while the map holds its breath, then a climb, then two bells for the zeros
arp(77.5, 79.2, BEAT / 2, .38)
arp(80.5, 86.0, BEAT / 4, .55, rising=True)
bell(86.1, 74, .9, -.3)
bell(86.8, 78, .9, .3)
arp(87.2, 91.5, BEAT / 2, .5, octave=24)
# 9 taxonomy: cards landing
arp(91.5, 103.5, BEAT / 2, .46)
# 10 the twist: sparse, a held breath, then the flip
arp(103.5, 107.2, BEAT, .42)
bell(108.4, 86, .85, .2)
for j, m in enumerate([62, 66, 69, 74, 78]):
    pluck(108.45 + j * .05, m + 12, .85, -.6 + .3 * j)
arp(109.5, 115.5, BEAT / 2, .5)
# 11–12 outcome, hardening: calmer
arp(115.5, 124.5, BEAT / 2, .44)
arp(124.5, 133.0, BEAT, .4)
# 13 invitation: an easy pulse; the fold-up gets a soft low note
arp(133.0, 142.0, BEAT, .45)
pluck(142.2, 50, .6, 0, dur=3)
# 14 closing: one last bell, then the pad fades out
bell(144.0, 74, .6, 0)

# room: a short stereo reverb from decaying noise (FFT convolution)
ir_n = int(2.4 * SR)
ti = np.arange(ir_n) / SR
wet = np.zeros_like(out)
size = 1 << int(np.ceil(np.log2(N + ir_n)))
for ch in range(2):
    ir = rng.standard_normal(ir_n) * np.exp(-ti / .55)
    ir[: int(.012 * SR)] = 0  # pre-delay
    ir /= np.sqrt(np.sum(ir ** 2))
    wet[ch] = np.fft.irfft(np.fft.rfft(out[ch], size) * np.fft.rfft(ir, size), size)[:N]
mix = .78 * out + .32 * wet

fade = np.ones(N)
fade[: int(1.0 * SR)] = np.linspace(0, 1, int(1.0 * SR))
mix *= fade
mix /= np.max(np.abs(mix)) / 10 ** (-3 / 20)  # peak at -3 dBFS; loudness is set at mux time

pcm = (np.clip(mix.T, -1, 1) * 32767).astype("<i2")
with wave.open(sys.argv[1] if len(sys.argv) > 1 else "score.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("ok", DUR, "s")
