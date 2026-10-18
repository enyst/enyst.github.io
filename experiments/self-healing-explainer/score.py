"""A quiet, low ambient score: slow pad chords, a sub bass, sparse soft bell notes, reverb."""
import sys, numpy as np, soundfile as sf
from scipy.signal import fftconvolve, butter, sosfilt
SR = 44100
dur = float(sys.argv[1]); N = int(dur * SR); t = np.arange(N) / SR
rng = np.random.default_rng(7)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
# A minor: Am(add9) - Fmaj7 - C(add9) - G6, 10 s each
chords = [[45, 57, 60, 64, 71], [41, 57, 60, 64, 65], [48, 55, 60, 62, 64], [43, 55, 59, 62, 64]]
CH = 10.0
out = np.zeros(N)
def env(n, a, r):
    e = np.ones(n); A = int(a * SR); R = int(r * SR)
    e[:A] = np.sin(np.linspace(0, np.pi / 2, A)) ** 2; e[-R:] *= np.cos(np.linspace(0, np.pi / 2, R)) ** 2
    return e
k = 0; start = 0.0
while start < dur:
    notes = chords[k % 4]; L = min(CH + 3.0, dur - start + 0.01); n = int(L * SR); s0 = int(start * SR)
    tt = np.arange(n) / SR; seg = np.zeros(n)
    for j, m in enumerate(notes):
        f = hz(m)
        if j == 0:   # sub bass, pure
            v = 0.5 * np.sin(2 * np.pi * (f / 2) * tt) + 0.25 * np.sin(2 * np.pi * f * tt)
        else:        # pad: detuned soft harmonics
            v = sum((0.6 / h) * np.sin(2 * np.pi * f * h * tt * (1 + d) + rng.uniform(0, 6))
                    for h in (1, 2, 3) for d in (-0.003, 0.003)) * 0.22
        seg += v
    seg *= env(n, 3.0, 3.0) * (1 + 0.08 * np.sin(2 * np.pi * 0.11 * tt))
    e = min(N, s0 + n); out[s0:e] += seg[: e - s0]
    # sparse bell notes from the chord, high but soft
    for b in range(3):
        bt = start + 1.5 + b * 3.2 + rng.uniform(-0.3, 0.3)
        if bt + 4 > dur: break
        m = rng.choice(notes[1:]) + 12; f = hz(m); bn = int(4 * SR); bb = np.arange(bn) / SR
        bell = (np.sin(2 * np.pi * f * bb) + 0.3 * np.sin(2 * np.pi * 2 * f * bb)) * np.exp(-bb * 1.3) * 0.12
        bell[:200] *= np.linspace(0, 1, 200)
        i0 = int(bt * SR); out[i0:i0 + bn] += bell[: N - i0]
    start += CH; k += 1
out = sosfilt(butter(4, 2200, 'low', fs=SR, output='sos'), out)
ir_n = int(3.0 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 2.2); ir[0] = 6
ir = sosfilt(butter(2, 3000, 'low', fs=SR, output='sos'), ir)
wet = fftconvolve(out, ir)[:N]; wet /= np.abs(wet).max()
mix = 0.65 * out / np.abs(out).max() + 0.35 * wet
fade = np.ones(N); fi = int(4 * SR); fo = int(6 * SR)
fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
mix = mix * fade; mix = 0.5 * mix / np.abs(mix).max()
sf.write(sys.argv[2], np.stack([mix, np.roll(mix, 300)], 1), SR)
print("ok")
