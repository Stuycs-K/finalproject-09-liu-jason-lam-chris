from PIL import Image
import numpy as np
import librosa
import argparse
import sys

# Load the image and gets size
image = Image.open("0085.jpg")
image = image.convert("RGB")
width, height = image.size

# Convert to grayscale
gray_image = Image.new("RGB", (width, height))
pixels = image.load()
gray_pixels = gray_image.load()

for i in range(height):
    for j in range(width):
        r, g, b = pixels[j, i]
        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        gray_pixels[j, i] = (gray, gray, gray)

# Store pixels as int array
image_array = np.zeros((height, width))
for i in range(height):
    for j in range(width):
        r, _, _ = gray_pixels[j, i]
        image_array[i][j] = r

# Flip the image to match orientation
image_array = np.flipud(image_array)

# Creating base audio
y, sr = librosa.load("pepes-theme.wav", sr=None)

# Convert audio to spectrogram (Short-Time Fourier Transform)
n_fft = 2048      # default is 2048, increase for better freq resolution
hop_length = 512  # smaller means better time resolution
win_length = n_fft
window = 'hann'

D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window)
magnitude, phase = np.abs(D), np.angle(D)

# Convert back to time domain
y_modified = librosa.istft(D, hop_length=hop_length, win_length=win_length, window=window)

# Save the modified audio
import soundfile as sf
sf.write("Clone.wav", y_modified, sr)
