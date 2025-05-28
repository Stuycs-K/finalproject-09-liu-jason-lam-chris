import numpy as np
import wave

def generateWav(filename='clean.wav', duration_sec=1, freq=440, sample_rate=44100):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    amplitude = 10  # max 32767 for int16, keep some headroom
    samples = (amplitude * np.sin(2 * np.pi * freq * t)).astype(np.int16)

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)        # mono
        wf.setsampwidth(2)        # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())

    print(f"Generated {filename} ({duration_sec}s, {freq}Hz sine wave)")

generateWav("clean.wav", duration_sec=3)
