import numpy as np
import librosa
import soundfile as sf
import argparse
import sys

mode = "encode"

# Create the parser with 1 args
parser = argparse.ArgumentParser(description="Parse up to 1 optional string arguments")
parser.add_argument('str1', type=str, nargs='?', help='Mode')

args = parser.parse_args()

args_dict = vars(args)
provided_count = sum(1 for v in args_dict.values() if v is not None)

if provided_count < 1:
    print(f"Error: at least 5 arguments required, but only {provided_count} provided.\nCommand should provide args for the following in order, Image Name, Audio Name, Output Name, Image Height, Image Length, Image start X, Image start Y, Dark/Light Priority Mode, Visibility Percentage, Time Resolution of Image Multiplier, Frequency Resolution of Image Multiplier")
    sys.exit(1)

mode = args.str1

# STFT parameters
n_fft = 2048
hop_length = 512
win_length = n_fft
window = 'hann'

if mode == "encode":
    string = " \x00\x7f\x80\xff"
    bits = [int(bit) for char in string for bit in format(ord(char), '08b')]

    print(bits)
    print(len(bits))

    y, sr = librosa.load("clean.wav", sr=None)

    D_orig = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window)
    magnitude_orig, phase_orig = np.abs(D_orig), np.angle(D_orig)

    phase_mod = phase_orig.copy()

    buckets_per_bit = 5
    for i, bit in enumerate(bits):
        start = i * buckets_per_bit
        end = start + buckets_per_bit
        if end > phase_orig.shape[1]:
            break
        if bit == 1:
            phase_mod[:, start:end] += np.pi  # Apply π shift to 5 frames

    D_mod = magnitude_orig * np.exp(1j * phase_mod)
    y_mod = librosa.istft(D_mod, hop_length=hop_length, win_length=win_length, window=window)

    sf.write("output.wav", y_mod, sr)

if mode == "decode":
    y, sr = librosa.load("clean.wav", sr=None)
    D_orig = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window)
    _, phase_orig = np.abs(D_orig), np.angle(D_orig)

    y_reloaded, sr = librosa.load("output.wav", sr=None)
    D_reloaded = librosa.stft(y_reloaded, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window)
    _, phase_reloaded = np.abs(D_reloaded), np.angle(D_reloaded)

    reconstructedBits = []

    buckets_per_bit = 5
    total_time_buckets = phase_orig.shape[1]
    total_bits = total_time_buckets // buckets_per_bit

    for i in range(total_bits):
        start = i * buckets_per_bit
        end = start + buckets_per_bit
        if end > total_time_buckets:
            break
        diff = (phase_reloaded[:, start:end] - phase_orig[:, start:end] + np.pi) % (2 * np.pi) - np.pi
        mean_diff = np.mean(np.abs(diff))
        if mean_diff > 1.4:
            reconstructedBits.append(1)
            print(f"Bit {i}: Mean phase difference = {mean_diff:.3f}")
        else:
            reconstructedBits.append(0)
            print(f"Bit {i}: Mean phase difference = {mean_diff:.3f}")

    print(reconstructedBits)
    string = ""
    for i in range(0, len(reconstructedBits), 8):
        byte = reconstructedBits[i:i+8]
        if len(byte) < 8:
            break
        ascii_val = int("".join(map(str, byte)), 2)
        print(chr(ascii_val), ascii_val)
        string += chr(ascii_val)

    print(string)
