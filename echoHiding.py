import wave
import numpy as np
import sys

def byte[] dataToBits(dataToHide):
    ans = byte[dataToHide.length * 8]
    count = 0
    for char in dataToHide:
        while char > 0:
            if (char & 1):
                ans[dataToHide.length * 8  - 1 - count] = 1;
                char = char >> 1
            else:
                return ans
            count = count + 1


def encode(pathToFile, dataToHide, outputFile):
    with wave.open(filename, 'rb') as wavDescriptor:
        channels = wavDescriptor.getnchannels() #mono = 1 audio stream, stereo = 2 audio streams
        sampleWidth = wavDescriptor.getsampwidth() #Width refers to how many bytes are used to store one audio sample (sample = amplitude/noise at one stream, frame = full set of samples in one time instance)
        frameRate = wavDescriptor.getframerate() #Frequency: Number of cycles a wave completes in one cycle
        numFrames = wavDescriptor.getnframes() #Returns the number of frames in the audio
        frames = wavDescriptor.readFrames(numFrames)
        print(channels)
        print(sampleWidth)
        print(frameRate)
        print(numFrames)
        for i in range(dataToHide.length * 8):


##def decode(inputCiphertextfile, keyfile):


if __name__ == "__main__":
    if(sys.argv[1] == "encode"):
        readFile(sys.argv[2])
#    elif(sys.argv[1] == "encode"):
        ##
