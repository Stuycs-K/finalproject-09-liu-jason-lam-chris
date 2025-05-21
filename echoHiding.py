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
        channels = wavDescriptor.getnchannels()
        sampleWidth = wavDescriptor.getsampwidth()
        frameRate = wavDescriptor.getframerate()
        numFrames = wavDescriptor.getnframes()

        print(channels)
        print(sampleWidth)
        print(frameRate)
        print(numFrames)
        
        frames = wavDescriptor.readframes(numFrames)
        
        audioData = np.frombuffer(frames, dtype=np.int16)
        copyData = np.copy(audioData)

        if channels == 1:
            delay1 = int(frameRate / 1000)  # 1ms
            delay2 = int(frameRate / 500)   # 2ms

            for i in range(len(bits)):
                if bits[i] == 0 and i + delay1 < len(copyData):
                    copyData[i + delay1] += int(audioData[i] * 0.25)
                elif bits[i] == 1 and i + delay2 < len(copyData):
                    copyData[i + delay2] += int(audioData[i] * 0.25)
                else:
                    print("Index out of bounds or invalid bit")

        copyData = np.clip(copyData, -32768, 32767)

        with wave.open(outputFile, 'wb') as writeFile:
            writeFile.setparams(wavDescriptor.getparams())
            writeFile.writeframes(copyData.astype(np.int16).tobytes())

##def encodeAmplitude

##def decode(inputCiphertextfile, keyfile):


if __name__ == "__main__":
    if(sys.argv[1] == "encodeDelay"):
        encodeDelay(sys.argv[2], sys.argv[3], sys.argv[4])
#    elif(sys.argv[1] == "encode"):
        ##
