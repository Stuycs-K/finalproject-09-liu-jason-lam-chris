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

# Convert audio to spectrogram (Short-Time Fourier Transform)
n_fft = 2048   
hop_length = 512 
win_length = n_fft
window = 'hann'

D_base = librosa.stft(y_base, n_fft=n_fft, hop_length=hop_length)
D_mod = librosa.stft(y_mod, n_fft=n_fft, hop_length=hop_length)

# Get Phase Arrays
phase_base, phase_mod = np.angle(D_base), np.angle(D_mod)

done = False

index = 0

for i in range (0, phase_base.shape[1]):
    if done:
        break
    for j in range (38, 513):
        print(phase_base[j, i], phase_mod[j, i])
        difference = (phase_mod[j, i] - phase_base[j, i] + np.pi) % (2 * np.pi) - np.pi
        if difference == np.pi or index == 10000:
            done = True
            break  # Stop bit found — break inner loop
        elif difference == np.pi / 2:
            bits.append('0')
        elif difference == -np.pi / 2:
            bits.append('1')
        index += 1

# Forming into a message
chars = []

for i in range(0, len(bits), 8):
    byte = bits[i:i+8]
    if len(byte) < 8:
        break  # Skip incomplete bytes
    char = chr(int(''.join(byte), 2))
    chars.append(char)

print(bits)
message = ''.join(chars)
print("Decoded message:", message)
