from PIL import Image
import numpy as np
import librosa
import argparse
import sys

text = "PiepiePiepie"

zeros_array = []

for char in text:
    binary = format(ord(char), '08b')  # Convert character to 8-bit binary string
    for bit in binary:
        bits.append(bit)
