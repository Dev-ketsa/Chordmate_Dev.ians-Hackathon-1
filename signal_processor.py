import numpy as np
from scipy.fft import fft, fftfreq

RATE = 44100
CHUNK = 4096


def detect_notes(audio_data):
    window = np.hanning(len(audio_data))
    audio_float = audio_data.astype(float) * window

    fft_result = fft(audio_float)
    magnitudes = np.abs(fft_result[:CHUNK // 2])
    frequencies = fftfreq(CHUNK, 1 / RATE)[:CHUNK // 2]

    # NEW: Higher threshold to kill noise
    # Only keep peaks that are at least 60% as loud as the loudest sound
    max_mag = np.max(magnitudes)
    if max_mag == 0: return []

    peak_indices = np.where(magnitudes > max_mag * 0.6)[0]

    notes_list = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    detected = []

    for i in peak_indices:
        f = frequencies[i]
        if 75 < f < 1000:  # Stay within guitar frequency range
            semitones = 12 * np.log2(f / 440.0)
            note_name = notes_list[int(round(semitones)) % 12]
            detected.append(note_name)

    return sorted(list(set(detected)))