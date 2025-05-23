from PIL import Image
import numpy as np
import librosa
import argparse
import sys

audioModified = "N/A.wav"
audioBase = "N/A.wav"

# Create the parser with 3 args
parser = argparse.ArgumentParser(description="Parse up to 3 optional string arguments")
parser.add_argument('str2', type=str, nargs='?', help='Input Audio')
parser.add_argument('str3', type=str, nargs='?', help='Base Audio')

args = parser.parse_args()

args_dict = vars(args)
provided_count = sum(1 for v in args_dict.values() if v is not None)

if provided_count < 2:
    print(f"Error: at least 3 arguments required, but only {provided_count} provided.\nCommand should provide args for the following in order, Input Text, Input Audio, Output Name")
    sys.exit(1)

audioModified = args.str2
audioBase = args.str3

# Making array of bits
bits = []

# Creating base audio
y_base, sr_base = librosa.load(audioBase, sr=None)
y_mod, sr_mod = librosa.load(audioModified, sr=None)

# Segment duration in seconds
segment_duration = 10
samples_per_segment = int(sr_base * segment_duration)

# Number of segments
num_segments = int(np.ceil(len(y_base) / samples_per_segment))

# Pad if needed
if len(y_base) % samples_per_segment != 0:
    padding = samples_per_segment * num_segments - len(y_base)
    y_base = np.pad(y_base, (0, padding), mode='constant')
if len(y_mod) % samples_per_segment != 0:
    padding = samples_per_segment * num_segments - len(y_mod)
    y_mod = np.pad(y_mod, (0, padding), mode='constant')

# Split into segments
segments_base = y_base.reshape((num_segments, samples_per_segment))
segments_mod = y_mod.reshape((num_segments, samples_per_segment))

# Convert audio to spectrogram (Short-Time Fourier Transform)
n_fft = 2048   
hop_length = 512 
win_length = n_fft
window = 'hann'

D_base = librosa.stft(y_base, n_fft=n_fft, hop_length=hop_length)
D_mod = librosa.stft(y_mod, n_fft=n_fft, hop_length=hop_length)

for i in range(num_segments):
    # Form into spectrogram
    D_base = librosa.stft(segments_base[i], n_fft=n_fft, hop_length=hop_length)
    D_mod = librosa.stft(segments_mod[i], n_fft=n_fft, hop_length=hop_length)
    # Get phase and magnitude
    mag_base, phase_base = np.abs(D_base), np.angle(D_base)
    mag_mod, phase_mod = np.abs(D_mod), np.angle(D_mod)
    # Only consider strong magnitude bins
    magnitude_threshold = 0.5
    mask = (mag_base > magnitude_threshold) & (mag_mod > magnitude_threshold)
    # Compute difference only where magnitude is high
    phase_diff = (phase_mod - phase_base)[mask]
    # Normalize difference to [-π, π] (unwrap)
    phase_diff = (phase_diff + np.pi) % (2 * np.pi) - np.pi
    # Count how many are near ±π/2
    bit_value = 0 if np.mean(phase_diff) > 0 else 1
    print("For segment " + str(i) + " difference is " + str(bit_value) + " phase diff is " + str(np.mean(phase_diff)))