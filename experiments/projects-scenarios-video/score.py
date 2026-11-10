"""A cool, quiet lo-fi groove under the narration: electric piano ii-V-I-vi, round bass,
soft swung drums and a little vinyl dust. Synthesized from scratch with numpy."""
import numpy as np, sys, wave
SR = 48000; BPM = 84; BEAT = 60 / BPM; BAR = 4 * BEAT
rng = np.random.default_rng(7)
def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def epiano(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    mod = np.sin(2*np.pi*f*t) * 1.6 * np.exp(-t * 3.0)               # bell-like attack that fades
    body = np.sin(2*np.pi*f*t + mod) + 0.25*np.sin(2*np.pi*2*f*t)
    trem = 1 + 0.12*np.sin(2*np.pi*4.2*t)                            # gentle tremolo, Rhodes style
    env = np.exp(-t * 1.1) * np.minimum(1, t / 0.006)
    return body * env * trem
def bass(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    env = np.minimum(1, t/0.01) * np.exp(-t * 1.6)
    return (np.sin(2*np.pi*f*t) + 0.2*np.sin(2*np.pi*2*f*t)) * env
def kick():
    t = np.arange(int(0.35*SR)) / SR
    f = 48 + 70*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*9)
def lp(x, k):
    return np.convolve(x, np.ones(k)/k, mode="same")
def snare():
    t = np.arange(int(0.22*SR)) / SR
    nz = lp(rng.standard_normal(len(t)), 6) * np.exp(-t*22)
    return 0.6*nz + 0.25*np.sin(2*np.pi*190*t)*np.exp(-t*30)
def hat():
    t = np.arange(int(0.05*SR)) / SR
    nz = rng.standard_normal(len(t)); nz = nz - lp(nz, 4)                 # crude high-pass
    return nz * np.exp(-t*70)
CHORDS = [  # (bass root, voicing) Dm9, G13, Cmaj9, Am9
    (38, [53, 57, 60, 64]), (43, [53, 57, 59, 64]), (36, [52, 55, 59, 62]), (45, [55, 60, 64, 67])]
def add(buf, x, at, g):
    s = int(at * SR)
    if s >= len(buf): return
    e = min(len(buf), s + len(x)); buf[s:e] += x[:e-s] * g
def render(total):
    n = int(total * SR) + SR; keys = np.zeros(n); low = np.zeros(n); drums = np.zeros(n)
    K, S, H = kick(), snare(), hat()
    bar = 0; t0 = 0.0
    while t0 < total:
        root, voicing = CHORDS[bar % 4]
        for j, m in enumerate(voicing): add(keys, epiano(midi(m), BAR*1.1), t0 + 0.012*j, 0.22)   # a little strum
        add(keys, epiano(midi(voicing[-1] + 2), BEAT*1.5), t0 + 2.5*BEAT, 0.10)                 # small melodic answer
        add(low, bass(midi(root), BEAT*1.8), t0, 0.55); add(low, bass(midi(root + 7), BEAT*0.9), t0 + 2.5*BEAT, 0.35)
        if t0 >= BAR * 2:                                                                       # drums come in after two bars
            for b in (0, 2.5): add(drums, K, t0 + b*BEAT, 0.7)
            for b in (1, 3): add(drums, S, t0 + b*BEAT, 0.35)
            for i in range(8):
                sw = (0.62 if i % 2 else 0.0) * BEAT * 0.5 + (i // 2) * BEAT                     # swung eighths
                add(drums, H, t0 + sw, 0.10 if i % 2 else 0.16)
        bar += 1; t0 += BAR
    keys = lp(keys, 10); dust = (rng.random(n) < 0.0004) * rng.standard_normal(n) * 0.15 + rng.standard_normal(n) * 0.004
    mix_l = keys + low + drums*0.9 + lp(dust, 3); mix_r = np.roll(keys, int(0.011*SR)) + low + drums + lp(dust, 3)
    out = np.stack([mix_l, mix_r], 1)[:int(total*SR)]
    fade_in, fade_out = int(1.5*SR), int(4*SR)
    out[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]; out[-fade_out:] *= np.linspace(1, 0, fade_out)[:, None]
    out = np.tanh(out / np.max(np.abs(out)) * 1.4) * 0.85                                       # soft tape-ish saturation
    w = wave.open("score.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out*32767).astype("<i2").tobytes()); w.close()
if __name__ == "__main__": render(float(sys.argv[1]))
