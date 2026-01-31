from audio_capture import AudioStream, get_loudness
import signal_processor
import chord_matcher
from collections import deque
import numpy as np
import time

# Initialize persistent stream
audio_device = AudioStream()
STABILITY_WINDOW = 3
history = deque(maxlen=STABILITY_WINDOW)
last_chord = None

print("Calibrating... Stay quiet.")
# Measure noise floor
noise_floor = np.mean([get_loudness(audio_device.read()) for _ in range(10)])
THRESHOLD = max(noise_floor * 4, 1500)
print(f"Calibration Complete. Threshold: {THRESHOLD:.2f}\n")

try:
    while True:
        audio_data = audio_device.read()

        if get_loudness(audio_data) > THRESHOLD:
            current_notes = signal_processor.detect_notes(audio_data)

            if current_notes:
                history.append(tuple(current_notes))

                # Check if all samples in history are identical (Stability Gate)
                if len(history) == STABILITY_WINDOW and len(set(history)) == 1:
                    chord = chord_matcher.match_chord(list(history[0]))

                    if chord != last_chord:
                        print(f"🎸 Detected: {chord} | Notes: {history[0]}")
                        last_chord = chord
            else:
                history.clear()
        else:
            # Silence resets the detection
            if last_chord is not None:
                print("Silence... Listening...")
            last_chord = None
            history.clear()

except KeyboardInterrupt:
    print("\nStopping...")
    audio_device.close()