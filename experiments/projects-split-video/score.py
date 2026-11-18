"""A tiny, low-tone score: slow sine pads on a four-chord loop, synthesized with numpy."""
import numpy as np, sys, wave
SR = 48000
def tone(f, n):
    t = np.arange(n) / SR
    return (np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*2*f*t+0.3) + 0.12*np.sin(2*np.pi*3*f*t+1.1))
def render(total):
    chords = [[110.0, 164.81, 220.0], [98.0, 146.83, 196.0], [87.31, 130.81, 174.61], [98.0, 146.83, 196.0]]  # A, G, F, G (low)
    bar = 6.0; n = int(total * SR); out = np.zeros(n)
    i = 0; s = 0
    while s < n:
        m = min(int(bar*SR*1.25), n - s)
        env = np.ones(m); a = int(1.5*SR); r = int(2.5*SR)
        env[:min(a,m)] = np.linspace(0, 1, min(a,m)); env[-min(r,m):] *= np.linspace(1, 0, min(r,m))
        for f in chords[i % 4]: out[s:s+m] += tone(f, m) * env / 3
        s += int(bar*SR); i += 1
    # gentle low-pass via moving average, global fades
    k = 64; out = np.convolve(out, np.ones(k)/k, mode="same")
    fade = int(3*SR); out[:fade] *= np.linspace(0,1,fade); out[-fade:] *= np.linspace(1,0,fade)
    out = out / np.max(np.abs(out)) * 0.9
    st = np.stack([out, np.roll(out, int(0.012*SR))], 1)
    w = wave.open("score.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st*32767).astype("<i2").tobytes()); w.close()
if __name__ == "__main__": render(float(sys.argv[1]))
