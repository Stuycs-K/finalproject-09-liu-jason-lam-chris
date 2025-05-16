from PIL import Image
import numpy as np
import librosa

# Load the image
image = Image.open("500px-Leonardo_da_Vinci_-_Last_Supper_(copy)_-_WGA12732.jpg")
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

# Save the grayscale image
gray_image.save("output.png")
print("Image saved as output.png")

# Create normalized magnitude array
normalized_magnitudes = np.zeros((height, width))

for i in range(height):
    for j in range(width):
        r, _, _ = gray_pixels[j, i]
        normalized_magnitudes[i][j] = r / 255.0

# Flip the image vertically to match spectrogram orientation
normalized_magnitudes = np.flipud(normalized_magnitudes)

# Creating base audio
y, sr = librosa.load("1-min-silence.wav", sr=None)

# Convert audio to spectrogram (Short-Time Fourier Transform)
n_fft = 20480      # default is 2048, increase for better freq resolution
hop_length = 26  # smaller means better time resolution
D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
magnitude, phase = np.abs(D), np.angle(D)

# Resize the image magnitudes to match the spectrogram shape
image_resized = np.array(Image.fromarray((normalized_magnitudes * 255).astype(np.uint8)).resize(magnitude.shape[::-1]))
image_resized = image_resized.astype(np.float32) / 255.0  # Normalize again

# Optionally invert image if you want darker = louder
image_resized = 1.0 - image_resized

# Scale image magnitudes to match the energy range of the original spectrogram
image_scaled = image_resized * np.max(magnitude)

# Combine image magnitudes with original phase
D_modified = image_scaled * np.exp(1j * phase)

# Convert back to time domain
y_modified = librosa.istft(D_modified)

# Save or play the modified audio
import soundfile as sf
sf.write("image_embedded_audio.wav", y_modified, sr)

