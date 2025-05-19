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
image_array = np.zeros((height, width))
pixels = image.load()

for i in range(height):
    for j in range(width):
        r, g, b = pixels[j, i]
        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        image_array[i, j] = gray

# Flip the image to match orientation
image_array = np.flipud(image_array)

# Rescaling Image
target_height = 800  # frequency bins max 1025 based on n_fft
target_width = 800   # time frames max 1 + sample length / hop_length

image_resized = np.array(Image.fromarray((image_array).astype(np.uint8)).resize((target_width, target_height))).astype(np.float32) / 255.0

# Dark Priority Mode
image_resized = 1.0 - image_resized

# Starting location
start_row = 0        # frequency bin start
start_col = 200        # time frame start

# Creating base audio
y, sr = librosa.load("pepes-theme.wav", sr=None)

# Convert audio to spectrogram (Short-Time Fourier Transform)
n_fft = 2048      # default is 2048, increase for better freq resolution
hop_length = 512  # smaller means better time resolution
win_length = n_fft
window = 'hann'

D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window)
magnitude, phase = np.abs(D), np.angle(D)

# Quick Check if image will fit
end_row = start_row + target_height
end_col = start_col + target_width
assert end_row <= magnitude.shape[0] and end_col <= magnitude.shape[1], "Image doesn't fit!"

# adding to magnitude
magnitude[start_row:end_row, start_col:end_col] += image_resized * np.max(magnitude) * .005

# Convert back to time domain
D_modified = magnitude * np.exp(1j * np.angle(D))
y_modified = librosa.istft(D_modified, hop_length=hop_length, win_length=win_length, window=window)

# Save the modified audio
import soundfile as sf
sf.write("NewAudio.wav", y_modified, sr)
