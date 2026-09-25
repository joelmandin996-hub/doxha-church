import numpy as np
import wave

SR = 44100
DUR = 29.6  # slightly longer than video, will be trimmed at mix time
N = int(SR * DUR)
t = np.linspace(0, DUR, N, endpoint=False)

def env_adsr(n, sr, attack, release, sustain_level=1.0):
    e = np.ones(n)
    a = int(attack * sr)
    r = int(release * sr)
    if a > 0:
        e[:a] = np.linspace(0, sustain_level, a)
    if r > 0:
        e[-r:] *= np.linspace(sustain_level, 0, r)
    return e

def note_freq(semitones_from_a4):
    return 440.0 * (2 ** (semitones_from_a4 / 12.0))

# ---- Pad: warm chord progression, cinematic swell ----
# Chord progression (uplifting, Apple-keynote-ish): Fmaj7 -> C/E -> Am7 -> G  (repeated, slow)
# Using semitone offsets from A4=0
NOTE = {
    'F3': -21, 'A3': -18, 'C4': -14, 'E4': -9,
    'C3': -26, 'E3': -22, 'G3': -19,
    'A2': -30, 'C4b': -14, 'E4b': -9, 'G4': -7,
    'G2': -31, 'B3': -16, 'D4': -12,
}
chords = [
    ['F3', 'A3', 'C4', 'E4'],   # Fmaj7
    ['C3', 'E3', 'G3', 'C4b'],  # C/E-ish (C major)
    ['A2', 'C4', 'E4b', 'G4'],  # Am7
    ['G2', 'B3', 'D4', 'G4'],   # G major
]
chord_dur = DUR / len(chords)

pad = np.zeros(N)
for i, chord in enumerate(chords):
    start = int(i * chord_dur * SR)
    end = int((i + 1) * chord_dur * SR) + int(0.6 * SR)
    end = min(end, N)
    seg_n = end - start
    if seg_n <= 0:
        continue
    seg_t = t[start:end]
    seg = np.zeros(seg_n)
    for note in chord:
        f = note_freq(NOTE[note])
        # two slightly detuned sines for a soft chorus effect
        seg += 0.5 * np.sin(2 * np.pi * f * seg_t)
        seg += 0.5 * np.sin(2 * np.pi * (f * 1.003) * seg_t)
        seg += 0.25 * np.sin(2 * np.pi * (f * 2) * seg_t)  # soft octave shimmer
    seg /= len(chord)
    e = env_adsr(seg_n, SR, attack=0.9, release=0.9, sustain_level=1.0)
    pad[start:end] += seg * e

# overall pad amplitude arc: soft intro -> build -> climax around device showcase (21-24s) -> resolve
arc = np.ones(N) * 0.16
def ramp(a, b, t0, t1):
    i0, i1 = int(t0 * SR), int(t1 * SR)
    i1 = min(i1, N)
    if i1 > i0:
        arc[i0:i1] = np.linspace(a, b, i1 - i0)
    arc[i1:] = b if i1 < N else arc[i1 - 1] if i1 > 0 else b

ramp(0.10, 0.16, 0.0, 4.0)
ramp(0.16, 0.22, 4.0, 13.0)
ramp(0.22, 0.34, 13.0, 21.0)
ramp(0.34, 0.40, 21.0, 24.0)
ramp(0.40, 0.20, 24.0, 29.0)
pad *= arc

# ---- Pulse: soft rhythmic heartbeat-like low thump, builds over time ----
pulse = np.zeros(N)
bpm = 100
beat = 60.0 / bpm
n_beats = int(DUR / beat)
for b in range(n_beats):
    bt = b * beat
    if bt < 3.0:
        continue  # silence during pure logo intro
    idx0 = int(bt * SR)
    dur = 0.18
    idxn = min(int(dur * SR), N - idx0)
    if idxn <= 0:
        continue
    seg_t = np.linspace(0, dur, idxn)
    f = 62.0
    click = np.sin(2 * np.pi * f * seg_t) * np.exp(-seg_t * 18)
    amp = np.interp(bt, [3, 13, 21, 29.6], [0.05, 0.12, 0.22, 0.16])
    pulse[idx0:idx0 + idxn] += click * amp

# ---- Sparkle chimes at scene-change moments (ascending motif) ----
chime_times = [0.6, 4.6, 8.0, 9.0, 13.2, 15.1, 17.0, 18.9, 21.1, 24.2, 25.4]
motif = [0, 2, 4, 7, 9, 11, 14, 16, 19, 21, 24]  # semitone offsets from C4-ish, ascending pentatonic-ish
chimes = np.zeros(N)
base = -14  # around C4 relative to A4
for i, ct in enumerate(chime_times):
    idx0 = int(ct * SR)
    dur = 1.1
    idxn = min(int(dur * SR), N - idx0)
    if idxn <= 0:
        continue
    seg_t = np.linspace(0, dur, idxn)
    semis = base + motif[i % len(motif)]
    f = note_freq(semis)
    tone = (np.sin(2 * np.pi * f * seg_t) + 0.5 * np.sin(2 * np.pi * f * 2 * seg_t)) * np.exp(-seg_t * 3.2)
    chimes[idx0:idx0 + idxn] += tone * 0.10

mix = pad + pulse + chimes

# gentle low-pass smoothing (moving average) to soften digital edges
kernel_size = 6
kernel = np.ones(kernel_size) / kernel_size
mix = np.convolve(mix, kernel, mode='same')

# fade in / fade out
fade_in = int(0.4 * SR)
fade_out = int(1.2 * SR)
mix[:fade_in] *= np.linspace(0, 1, fade_in)
mix[-fade_out:] *= np.linspace(1, 0, fade_out)

# normalize to avoid clipping
peak = np.max(np.abs(mix))
if peak > 0:
    mix = mix / peak * 0.85

pcm = np.int16(np.clip(mix, -1, 1) * 32767)

with wave.open('music.wav', 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(pcm.tobytes())

print('music.wav written', DUR, 's')
