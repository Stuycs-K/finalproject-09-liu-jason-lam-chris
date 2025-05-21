import wave
import numpy as np
import sys

def dataToBits(dataToHide):
    bits = []
    for char in dataToHide:
        val = ord(char)
        bits.extend([(val >> i) & 1 for i in range(7, -1, -1)])
    return np.array(bits, dtype=np.uint8)


def encodeDelay(pathToFile, dataToHide, outputFile):
    bits = dataToBits(dataToHide)
    with wave.open(pathToFile, 'rb') as wavDescriptor:
        channels = wavDescriptor.getnchannels() #mono = 1 audio stream, stereo = 2 audio streams
        sampleWidth = wavDescriptor.getsampwidth() #Width refers to how many bytes are used to store one audio sample (sample = amplitude/noise at one stream, frame = full set of samples in one time instance)
        frameRate = wavDescriptor.getframerate() #Frequency: Number of cycles a wave completes in one cycle
        numFrames = wavDescriptor.getnframes() #Returns the number of frames in the audio
        frames = wavDescriptor.readframes(numFrames)
        print(channels)
        print(sampleWidth)
        print(frameRate)
        print(numFrames)
        copyData = frames[:]
        #for i in range(0, len(frames)):
        #    print(frames[i])
        #for i in range (0, len(copyData)):
        #    print(copyData[i])
        if(channels == 1):
            for i in range(0, len(bits)):
                delay1 = (int)(frameRate/1000)
                delay2 = (int) (frameRate/500)
                if(bits[i] == 0):
                    copyData[i + delay1] += (frames[i] // 4)#0.4 is the amplitude of the echo
                elif(bits[i] == 1):
                    copyData[i + delay2] += (frames[i] // 4)
                else:
                    print("Error in dataToBits")
        copyData = np.clip(copyData, -32768, 32767)
        with wave.open(outputFile, 'wb') as writeFile:
            writeFile.setparams(wavDescriptor.getparams())
            writeFile.writeframes(copyData.tobytes())

##def encodeAmplitude

##def decode(inputCiphertextfile, keyfile):


if __name__ == "__main__":
    if(sys.argv[1] == "encodeDelay"):
        encodeDelay(sys.argv[2], sys.argv[3], sys.argv[4])
#    elif(sys.argv[1] == "encode"):
        ##
