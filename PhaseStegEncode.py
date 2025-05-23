from PIL import Image
import numpy as np
import librosa
import argparse
import sys
import soundfile as sf

text = "N/A"
audio = "N/A.wav"
outputName = "output.wav"

# Create the parser with 3 args
parser = argparse.ArgumentParser(description="Parse up to 3 optional string arguments")
parser.add_argument('str2', type=str, nargs='?', help='Input Text')
parser.add_argument('str3', type=str, nargs='?', help='Input Audio')
parser.add_argument('str4', type=str, nargs='?', help='Output')

args = parser.parse_args()

args_dict = vars(args)
provided_count = sum(1 for v in args_dict.values() if v is not None)

if provided_count < 3:
    print(f"Error: at least 3 arguments required, but only {provided_count} provided.\nCommand should provide args for the following in order, Input Text, Input Audio, Output Name")
    sys.exit(1)

text = args.str2
audio = args.str3
outputName = args.str4

# # Text used
# text = ""

# Making array of bits
bits = []

for char in text:
    binary = format(ord(char), '08b')  # Convert character to 8-bit binary string
    for bit in binary:
        bits.append(bit)

print(bits)

# Creating base audio
y, sr = librosa.load(audio, sr=None)

# Segment duration in seconds
segment_duration = 10
samples_per_segment = int(sr * segment_duration)

# Number of segments
num_segments = int(np.ceil(len(y) / samples_per_segment))

# Pad if needed
if len(y) % samples_per_segment != 0:
    padding = samples_per_segment * num_segments - len(y)
    y = np.pad(y, (0, padding), mode='constant')

# Split into segments
segments = y.reshape((num_segments, samples_per_segment))

# # Optionally save segments
# for i, segment in enumerate(segments):
#     sf.write(f'segment_{i}.wav', segment, sr)

# Convert audio to spectrogram (Short-Time Fourier Transform)
n_fft = 2048   
hop_length = 512 
win_length = n_fft
window = 'hann'

modified_segments = []

for i in range(num_segments):
    if i == len(bits):
        break
    # Form into spectrogram
    D = librosa.stft(segments[i], n_fft=n_fft, hop_length=hop_length)
    # Get Magnitude and Phase arrays
    magnitude, phase = np.abs(D), np.angle(D)
    # Phase Modification
    if bits[i] == '0':
        phase = np.pi/2
    else:
        phase = np.pi/2
    # Construction
    D_modified = magnitude * np.exp(1j * phase)
    # Convert back to time domain
    y_modified = librosa.istft(D_modified, hop_length=hop_length, win_length=win_length, window=window)
    # Store the result
    modified_segments.append(y_modified)

# Concatenate all modified segments
final_audio = np.concatenate(modified_segments)

# Save the modified audio
sf.write(outputName, final_audio, sr)