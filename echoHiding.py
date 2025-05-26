
import wave
import numpy as np
import sys
import scipy.signal

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

        frames = wavDescriptor.readframes(numFrames)
        audioData = np.frombuffer(frames, dtype=np.int16)
        copyData = np.copy(audioData)

        delay0 = int(frameRate / 100)   # 10ms
        delay1 = int(frameRate / 50)    # 20ms
        attenuation = 0.5               # echo strength

        if channels == 1:
            blockSize = delay1 * 2
            for i in range(len(bits)):
                start = i * blockSize
                end = start + blockSize
                if end + delay1 >= len(copyData):  # ensure we don't go out of bounds
                    break
                segment = audioData[start:end]

                # Inject echo at the correct delay
                if bits[i] == 0:
                    for j in range(len(segment)):
                        if start + delay0 + j < len(copyData):
                            copyData[start + delay0 + j] += int(attenuation * segment[j])
                else:
                    for j in range(len(segment)):
                        if start + delay1 + j < len(copyData):
                            copyData[start + delay1 + j] += int(attenuation * segment[j])

        copyData = np.clip(copyData, -32768, 32767)

        with wave.open(outputFile, 'wb') as writeFile:
            writeFile.setparams(wavDescriptor.getparams())
            writeFile.writeframes(copyData.astype(np.int16).tobytes())

def decode(pathToFile, messageLength):
    messageLength = int(messageLength)
    bits = []

    with wave.open(pathToFile, 'rb') as wavDescriptor:
        channels = wavDescriptor.getnchannels()
        sampleWidth = wavDescriptor.getsampwidth()
        frameRate = wavDescriptor.getframerate()
        numFrames = wavDescriptor.getnframes()

        frames = wavDescriptor.readframes(numFrames)
        audioData = np.frombuffer(frames, dtype=np.int16)

        delay0 = int(frameRate / 100)   # 10ms
        delay1 = int(frameRate / 50)    # 20ms
        blockSize = delay1 * 2

        for i in range(messageLength * 8):
            start = i * blockSize
            end = start + blockSize
            if end > len(audioData):
                break

            segment = audioData[start:end]
            if np.max(np.abs(segment)) < 500:  # optional: skip silent segments
                bits.append(0)
                continue

            corr = scipy.signal.correlate(segment, segment, mode='full')
            mid = len(corr) // 2

            corr_at_delay0 = corr[mid + delay0]
            corr_at_delay1 = corr[mid + delay1]

            if corr_at_delay0 > corr_at_delay1:
                bits.append(0)
            else:
                bits.append(1)

    decodedMessage = bitsToString(bits)
    print("Decoded Message:", decodedMessage)
        
def bitsToString(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        val = sum([(bit << (7 - j)) for j, bit in enumerate(byte)])
        chars.append(chr(val))
    return ''.join(chars)

if __name__ == "__main__":
    if(sys.argv[1] == "encodeDelay"):
        encodeDelay(sys.argv[2], sys.argv[3], sys.argv[4])
    elif(sys.argv[1] == "decode"):
        decode(sys.argv[2], sys.argv[3])