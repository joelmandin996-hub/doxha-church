import numpy as np
import wave

SR = 44100
DUR = 62.0  # slightly longer than the video, trimmed at mix time
N = int(SR * DUR)
t = np.linspace(0, DUR, N, endpoint=False)

def note_freq(semitones_from_a4):
    return 440.0 * (2 ** (semitones_from_a4 / 12.0))

def one_pole_lowpass(x, cutoff_hz, sr):
    a = np.exp(-2 * np.pi * cutoff_hz / sr)
    y = np.zeros_like(x)
    prev = 0.0
    for i in range(len(x)):
        prev = (1 - a) * x[i] + a * prev
        y[i] = prev
    return y

def one_pole_lowpass_vec(x, cutoff_hz, sr, chunk=4096):
    # chunked approximation of a slow-moving lowpass using cumulative smoothing
    a = np.exp(-2 * np.pi * cutoff_hz / sr)
    y = np.empty_like(x)
    prev = 0.0
    out = []
    kernel_len = min(len(x), int(sr / max(cutoff_hz, 1) * 8))
    kernel_len = max(kernel_len, 8)
    kernel = a ** np.arange(kernel_len)
    kernel = kernel / kernel.sum()
    y = np.convolve(x, kernel, mode='same')
    return y

# ---- warm pad: soft sine/triangle-ish partials, very slow chord movement ----
NOTE = {
    'F3': -21, 'A3': -18, 'C4': -14, 'E4': -9,
    'C3': -26, 'E3': -22, 'G3': -19,
    'A2': -30, 'C4b': -14, 'E4b': -9, 'G4': -7,
    'G2': -31, 'B3': -16, 'D4': -12,
}
chords = [
    ['F3', 'A3', 'C4', 'E4'],
    ['C3', 'E3', 'G3', 'C4b'],
    ['A2', 'C4', 'E4b', 'G4'],
    ['G2', 'B3', 'D4', 'G4'],
    ['F3', 'A3', 'C4', 'E4'],
    ['C3', 'E3', 'G3', 'C4b'],
]
chord_dur = DUR / len(chords)
pad = np.zeros(N)
for i, chord in enumerate(chords):
    start = int(i * chord_dur * SR)
    end = int((i + 1) * chord_dur * SR) + int(1.2 * SR)
    end = min(end, N)
    seg_n = end - start
    if seg_n <= 0:
        continue
    seg_t = t[start:end]
    seg = np.zeros(seg_n)
    for note in chord:
        f = note_freq(NOTE[note])
        # soft triangle-like timbre via a couple of odd harmonics at low amplitude (gentler than raw sine stack)
        seg += 0.42 * np.sin(2 * np.pi * f * seg_t)
        seg += 0.42 * np.sin(2 * np.pi * (f * 1.004) * seg_t)  # gentle chorus detune
        seg += 0.10 * np.sin(2 * np.pi * (f * 3) * seg_t) / 3.0  # soft 3rd harmonic, rounds the tone
        seg += 0.18 * np.sin(2 * np.pi * (f * 2) * seg_t)  # airy octave shimmer
    seg /= len(chord)
    # slow attack/release envelope, long and smooth (ambient, not percussive)
    a_n = int(1.8 * SR)
    r_n = int(1.8 * SR)
    env = np.ones(seg_n)
    if a_n < seg_n:
        env[:a_n] = np.linspace(0, 1, a_n) ** 1.6
    if r_n < seg_n:
        env[-r_n:] *= (np.linspace(1, 0, r_n) ** 1.6)
    pad[start:end] += seg * env

# slow amplitude LFO (breathing) for a living, non-static pad
lfo = 0.85 + 0.15 * np.sin(2 * np.pi * 0.065 * t)
pad *= lfo

# overall dynamic arc: soft intro -> gentle build -> airy climax at device showcase -> settle for outro
arc = np.ones(N) * 0.16
def ramp(a, b, t0, t1):
    i0, i1 = int(t0 * SR), int(t1 * SR)
    i1 = min(i1, N)
    if i1 > i0:
        arc[i0:i1] = np.linspace(a, b, i1 - i0)
    arc[i1:] = b if i1 < N else (arc[i1 - 1] if i1 > 0 else b)

ramp(0.09, 0.13, 0.0, 7.0)      # hook
ramp(0.13, 0.11, 7.0, 16.0)     # problem, slightly recede
ramp(0.11, 0.20, 16.0, 20.0)    # the turn — building
ramp(0.20, 0.24, 20.0, 23.0)    # brand reveal
ramp(0.24, 0.30, 23.0, 47.0)    # feature run, steady build
ramp(0.30, 0.34, 47.0, 52.0)    # emotional payoff, warm
ramp(0.34, 0.40, 52.0, 57.0)    # CTA climax
ramp(0.40, 0.16, 57.0, 62.0)    # resolve / fade
pad *= arc

# ---- soft low sub-bass "breath" swells instead of a clicky pulse (ambient, felt not heard) ----
breath = np.zeros(N)
swell_period = 4.8  # seconds between soft swells
n_swells = int(DUR / swell_period) + 1
for i in range(n_swells):
    st = i * swell_period
    if st < 3.0:
        continue
    idx0 = int(st * SR)
    dur = 3.6
    idxn = min(int(dur * SR), N - idx0)
    if idxn <= 0:
        continue
    seg_t = np.linspace(0, dur, idxn)
    f = 48.0
    env = np.sin(np.pi * np.clip(seg_t / dur, 0, 1)) ** 1.4  # smooth rise & fall, no attack transient
    tone = np.sin(2 * np.pi * f * seg_t) * env
    amp = np.interp(st, [3, 16, 23, 47, 52, 62], [0.05, 0.06, 0.10, 0.13, 0.16, 0.09])
    breath[idx0:idx0 + idxn] += tone * amp

# ---- sparse, soft bell-like accents at scene-change moments (ascending, airy, not sharp) ----
chime_times = [0.3, 7.2, 16.2, 20.2, 23.2, 29.2, 35.2, 41.2, 46.4, 46.6, 46.8, 47.2, 52.2]
motif = [0, 2, 4, 7, 9, 11, 14, 16, 12, 14, 16, 19, 21, 24]
chimes = np.zeros(N)
base = -14
for i, ct in enumerate(chime_times):
    idx0 = int(ct * SR)
    dur = 1.6
    idxn = min(int(dur * SR), N - idx0)
    if idxn <= 0:
        continue
    seg_t = np.linspace(0, dur, idxn)
    semis = base + motif[i % len(motif)]
    f = note_freq(semis)
    env = np.exp(-seg_t * 2.0)
    tone = (np.sin(2 * np.pi * f * seg_t) + 0.35 * np.sin(2 * np.pi * f * 2.01 * seg_t)) * env
    chimes[idx0:idx0 + idxn] += tone * 0.065

mix = pad + breath + chimes

# ---- simple algorithmic reverb: convolve with a short synthetic exponential-decay noise impulse ----
rng = np.random.default_rng(7)
ir_dur = 1.8
ir_n = int(ir_dur * SR)
ir_t = np.arange(ir_n) / SR
ir_noise = rng.standard_normal(ir_n)
ir = ir_noise * np.exp(-ir_t * 3.2)
ir = one_pole_lowpass_vec(ir, 2200, SR)
ir /= np.max(np.abs(ir)) + 1e-9
wet = np.convolve(mix, ir, mode='full')[:N] * 0.22
mix = mix * 0.9 + wet

# gentle overall smoothing to remove any digital harshness
kernel_size = 5
kernel = np.ones(kernel_size) / kernel_size
mix = np.convolve(mix, kernel, mode='same')

# fade in / fade out
fade_in = int(0.6 * SR)
fade_out = int(2.0 * SR)
mix[:fade_in] *= np.linspace(0, 1, fade_in)
mix[-fade_out:] *= np.linspace(1, 0, fade_out)

peak = np.max(np.abs(mix))
if peak > 0:
    mix = mix / peak * 0.8

pcm = np.int16(np.clip(mix, -1, 1) * 32767)

with wave.open('music.wav', 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(pcm.tobytes())

print('music.wav written', DUR, 's')
