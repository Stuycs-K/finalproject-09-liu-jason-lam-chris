from PIL import Image
import numpy as np
import librosa
import argparse
import sys

# Base Settings
imageName = "N/A.txt"
audioName = "Silent.wav"
outputName = "Output.wav"
# Image Scale
target_height = 600  # frequency bins max 1025 based on n_fft
target_width = 600   # time frames max 1 + sample length / hop_length
# Starting location
start_row = 0        # frequency bin start
start_col = 0        # time frame start
# Custom Settings
mode = "Dark"
visibility = 100
time_resolution = 1
frequency_resolution = 1

# Create the parser with 3 args
parser = argparse.ArgumentParser(description="Parse up to 4 optional string arguments")
parser.add_argument('str1', type=str, nargs='?', help='Image Name')
parser.add_argument('str2', type=str, nargs='?', help='Audio Name')
parser.add_argument('str3', type=str, nargs='?', help='Output Name')
parser.add_argument('str4', type=int, nargs='?', help='Image Height')
parser.add_argument('str5', type=int, nargs='?', help='Image Length')
parser.add_argument('str6', type=int, nargs='?', help='Image Start X')
parser.add_argument('str7', type=int, nargs='?', help='Image Start Y')
parser.add_argument('str8', type=str, nargs='?', help='Color Priority Mode')
parser.add_argument('str9', type=float, nargs='?', help='Visibility')
parser.add_argument('str10', type=float, nargs='?', help='Time Resolution Multiplier')
parser.add_argument('str11', type=float, nargs='?', help='Frequency Resolution Multiplier')

args = parser.parse_args()

args_dict = vars(args)
provided_count = sum(1 for v in args_dict.values() if v is not None)

if provided_count < 5:
    print(f"Error: at least 5 arguments required, but only {provided_count} provided.\nCommand should provide args for the following in order, Image Name, Audio Name, Output Name, Image Height, Image Length, Image start X, Image start Y, Dark/Light Priority Mode, Visibility Percentage, Time Resolution of Image Multiplier, Frequency Resolution of Image Multiplier")
    sys.exit(1)

imageName = args.str1
audioName = args.str2
outputName = args.str3
target_height = args.str4
target_width = args.str5
if args.str6 is not None:
    start_row = args.str6
if args.str7 is not None:
    start_col = args.str7
if args.str8 is not None:
    mode = args.str8
if args.str9 is not None:
    visibility = args.str9
if args.str10 is not None:
    time_resolution = args.str10
if args.str11 is not None:
    frequency_resolution = args.str11

# Load the image and gets size
image = Image.open(imageName)
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

# Resize Image
image_resized = np.array(Image.fromarray((image_array).astype(np.uint8)).resize((target_width, target_height))).astype(np.float32) / 255.0

# Dark Priority Mode
image_resized = 1.0 - image_resized

# Creating base audio
y, sr = librosa.load(audioName, sr=None)

# Convert audio to spectrogram (Short-Time Fourier Transform)
n_fft = (int)(2048 * frequency_resolution)      # default is 2048, increase for better freq resolution
hop_length = (int)(512 / (time_resolution*1.0)) # smaller means better image resolution but image sounds a lot worse, also audio is a lot longer
win_length = n_fft
window = 'hann'

D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window)
magnitude, phase = np.abs(D), np.angle(D)

# Quick Check if image will fit
end_row = start_row + target_height
end_col = start_col + target_width
assert end_row <= magnitude.shape[0] and end_col <= magnitude.shape[1], "Image doesn't fit!"

# adding to magnitude
magnitude[start_row:end_row, start_col:end_col] += image_resized * np.max(magnitude) / (100.0/visibility)

# Convert back to time domain
D_modified = magnitude * np.exp(1j * np.angle(D))
y_modified = librosa.istft(D_modified, hop_length=hop_length, win_length=win_length, window=window)

# Save the modified audio
import soundfile as sf
sf.write(outputName, y_modified, sr)
