from PIL import Image
import numpy as np
import librosa
import argparse
import sys

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

# Text used
# text = "PiepiePiepie"

# Making array of bits
bits = []

for char in text:
    binary = format(ord(char), '08b')  # Convert character to 8-bit binary string
    for bit in binary:
        bits.append(bit)

# End condition
bits.append('2')

print(bits)
# Creating base audio
y, sr = librosa.load(audio, sr=None)

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
            if bits[index] == '2':
                phase[j, i] += np.pi
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
sf.write(outputName, y_modified, sr)