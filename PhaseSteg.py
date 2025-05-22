from PIL import Image
import numpy as np
import librosa
import argparse
import sys

# Text used
text = "PiepiePiepie"

# Making array of bits
zeros_array = []

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

# Convert back to time domain
D_modified = magnitude * np.exp(1j * phase)
y_modified = librosa.istft(D_modified, hop_length=hop_length, win_length=win_length, window=window)

# Save the modified audio
import soundfile as sf
sf.write("test.wav", y_modified, sr)