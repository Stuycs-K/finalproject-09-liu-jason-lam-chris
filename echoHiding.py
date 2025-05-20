import wave
import numpy as np
import sys

def dataToBits(dataToHide):
    bits = []
    for char in dataToHide:
        val = ord(char)
        bits.extend([(val >> i) & 1 for i in range(7, -1, -1)])
    return np.array(bits, dtype=np.uint8)


def encode(pathToFile, dataToHide, outputFile):
    bits = dataToBits(dataToHide)
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
        if(channels == 1):
            for i in range(0, len(bits)):
                copyData = np.copy(frames)
                delay = (int)(bits[i] * (frameRate/1000))
                frames[i] = frames[i] + delay


##def decode(inputCiphertextfile, keyfile):


if __name__ == "__main__":
    if(sys.argv[1] == "encode"):
        readFile(sys.argv[2])
#    elif(sys.argv[1] == "encode"):
        ##
