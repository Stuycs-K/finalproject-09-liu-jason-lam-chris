from PIL import Image
import numpy as np
import librosa
import argparse
import sys

# Base Settings
imageName = "N/A.txt"
audioName = "Silent.wav"
outputName = "Output.wav"
mode = "Dark"
visibility = 100
time_resolution = 1
frequency_resolution = 1

# Create the parser with 3 args
parser = argparse.ArgumentParser(description="Parse up to 4 optional string arguments")
parser.add_argument('str1', type=str, nargs='?', help='First string')
parser.add_argument('str2', type=str, nargs='?', help='Second string')
parser.add_argument('str3', type=str, nargs='?', help='Third string')
parser.add_argument('str4', type=int, nargs='?', help='Fourth string')
parser.add_argument('str5', type=int, nargs='?', help='Fifth string')
parser.add_argument('str6', type=int, nargs='?', help='Sixth string')

args = parser.parse_args()

args_dict = vars(args)
provided_count = sum(1 for v in args_dict.values() if v is not None)

if provided_count < 2:
    print(f"Error: at least 2 arguments required, but only {provided_count} provided.\nCommand should provide args for the following in order, Image Name, Output Name, Dark/Light Priority Mode, Visibility Percentage, Time Resolution of Image Multiplier, Frequency Resolution of Image Multiplier")
    sys.exit(1)

imageName = args.str1
outputName = args.str2
if args.str3 is not None:
    mode = args.str3
if args.str4 is not None:
    visibility = args.str4
if args.str5 is not None:
    time_resolution = args.str5
if args.str5 is not None:
    frequency_resolution = args.str6

# print(f"{provided_count} arguments provided. Continuing...")

# Load the image and accquires its size
image = Image.open(imageName)
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

# # Save the grayscale image
# gray_image.save("output.png")
# print("Image saved as output.png")

# Create normalized magnitude array
normalized_magnitudes = np.zeros((height, width))

for i in range(height):
    for j in range(width):
        r, _, _ = gray_pixels[j, i]
        normalized_magnitudes[i][j] = r / 255.0

# Flip the image vertically to match spectrogram orientation
normalized_magnitudes = np.flipud(normalized_magnitudes)

# Creating base audio
y, sr = librosa.load(audioName, sr=None)

# Convert audio to spectrogram (Short-Time Fourier Transform)
n_fft = 2048 * frequency_resolution      # default is 2048, increase for better freq resolution
hop_length = (int)(512 / (time_resolution*1.0)) # smaller means better image resolution but image sounds a lot worse, also audio is a lot longer
D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
magnitude, phase = np.abs(D), np.angle(D)

# Resize the image magnitudes to match the spectrogram shape
image_resized = np.array(Image.fromarray((normalized_magnitudes * 255).astype(np.uint8)).resize(magnitude.shape[::-1]))
image_resized = image_resized.astype(np.float32) / 255.0  # Normalize again

# Optionally invert image if you want darker = louder
if(mode == "Dark"):
    image_resized = 1.0 - image_resized

# Weaken the brightness of the image
image_resized = image_resized.astype(np.float32) / (100.0/visibility)

# Scale image magnitudes to match the energy range of the original spectrogram
image_scaled = image_resized * np.max(magnitude)

# Combine image magnitudes with original phase
D_modified = image_scaled * np.exp(1j * phase)

# Convert back to time domain
y_modified = librosa.istft(D_modified)

# Save the modified audio
import soundfile as sf
sf.write(outputName, y_modified, sr)

