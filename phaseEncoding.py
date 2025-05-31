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
# --- First block: create and modify audio ---

    string = "a"

    bits = [int(bit) for char in string for bit in format(ord(char), '08b')]
    
    print(bits)
    print(len(bits))

    y, sr = librosa.load("clean.wav", sr=None)

    # STFT of original
    D_orig = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window)
    magnitude_orig, phase_orig = np.abs(D_orig), np.angle(D_orig)

    # Modify phase
    phase_mod = phase_orig.copy()
    for i, bit in enumerate(bits):
        if bit == 1:
            phase_mod[i, :] += np.pi  # Add pi

    # Rebuild modified complex spectrum
    D_mod = magnitude_orig * np.exp(1j * phase_mod)
    y_mod = librosa.istft(D_mod, hop_length=hop_length, win_length=win_length, window=window)

    # Save modified audio
    sf.write("output.wav", y_mod, sr)

if mode == "decode":
# --- Second block: load modified audio and get new phase ---
    y, sr = librosa.load("clean.wav", sr=None)
    D_orig = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window)
    _, phase_orig = np.abs(D_orig), np.angle(D_orig)

    y_reloaded, sr = librosa.load("output.wav", sr=None)
    D_reloaded = librosa.stft(y_reloaded, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window)
    _, phase_reloaded = np.abs(D_reloaded), np.angle(D_reloaded)

    reconstructedBits = []

    # --- Check phase difference ---
    # We'll compare only the first 8 frequency bins used by the bits
    for i in range(8):
        diff = (phase_reloaded[i, :] - phase_orig[i, :] + np.pi) % (2 * np.pi) - np.pi
        mean_diff = np.mean(np.abs(diff))
        if mean_diff > 0:
            # diff = (phase_reloaded[i, :] - phase_orig[i, :] + np.pi) % (2 * np.pi) - np.pi  # Normalize to [-π, π]
            # mean_diff = np.mean(np.abs(diff))
            print(f"Freq bin {i}: Mean phase difference = {mean_diff:.3f} radians")
            reconstructedBits.append(1)
        else:
            # print(f"Freq bin {i}: Not modified (bit = 0)")
            reconstructedBits.append(0)

    print(reconstructedBits)
    string = ""
    for i in range(0, len(reconstructedBits), 8):
        byte = reconstructedBits[i:i+8]
        if len(byte) < 8:
            break  # Ignore incomplete byte at the end
        ascii_val = int("".join(map(str, byte)), 2)
        string += (chr(ascii_val))

    print(string)