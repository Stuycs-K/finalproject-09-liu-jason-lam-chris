import wave
import numpy as np
import sys

def readFile(filename):
    with wave.open(filename, 'rb') as wavDescriptor:
        channels = wavDescriptor.getnchannels() #mono = 1 audio stream, stereo = 2 audio streams
        sample_width = wavDescriptor.getsampwidth() #Width refers to how many bytes are used to store one audio sample (sample = amplitude/noise at one stream, frame = full set of samples in one time instance) 
        frame_rate = wavDescriptor.getframerate() #Frequency: Number of cycles a wave completes in one cycle
        num_frames = wavDescriptor.getnframes() #Returns the number of frames in the audio
        
def encode(inputTextfile, keyfile, outputCiphertextfile):

def decode(inputCiphertextfile, keyfile):


if __name__ == "__main__":
    if(sys.argv[1] == "encode"):
        ##
    elif(sys.argv[1] == "encode"):
        ##