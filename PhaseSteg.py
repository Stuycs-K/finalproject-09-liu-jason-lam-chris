from PIL import Image
import numpy as np
import librosa
import argparse
import sys

# Text used
text = "PiepiePiepie"

# Making array of bits
bits = []

for char in text:
    binary = format(ord(char), '08b')  # Convert character to 8-bit binary string
    for bit in binary:
        bits.append(bit)

# Creating base audio
y, sr = librosa.load("audio/pepes-theme.wav", sr=None)

# Convert audio to spectrogram (Short-Time Fourier Transform)
n_fft = 2048   
hop_length = 512 
win_length = n_fft
window = 'hann'

D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)

# Get Magnitude and Phase arrays
magnitude, phase = np.abs(D), np.angle(D)

index = 0
done = False

# Adding phase changes
for i in range (0, phase.shape[1]):
    for j in range (38, 513):
        if index == len(bits):
            done = True
            break
        if bits[index] == '0':
            phase[j, i] += np.pi/2
        else:
            phase[j, i] -= np.pi/2
        index += 1
    if done:
        break

# Convert back to time domain
D_modified = magnitude * np.exp(1j * phase)
y_modified = librosa.istft(D_modified, hop_length=hop_length, win_length=win_length, window=window)

# Save the modified audio
import soundfile as sf
sf.write("test.wav", y_modified, sr)