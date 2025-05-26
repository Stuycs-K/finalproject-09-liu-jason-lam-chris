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

        delay0 = int(frameRate / 100)   # 10ms delay for bit 0
        delay1 = int(frameRate / 50)    # 20ms delay for bit 1
        blockSize = delay1 * 2
        attenuation = 0.6               # strength of echo
        pilot_len = 100                 # small impulse to help detection

        if channels != 1:
            raise ValueError("Only mono audio supported.")

        for i, bit in enumerate(bits):
            start = i * blockSize
            end = start + blockSize
            if end + delay1 >= len(copyData):  # ensure bounds
                break

            segment = audioData[start:end]

            # 1. Inject pilot impulse (optional but improves detection)
            for j in range(min(pilot_len, len(segment))):
                copyData[start + j] += int(0.8 * segment[j])

            # 2. Inject echo
            delay = delay0 if bit == 0 else delay1
            for j in range(len(segment)):
                dst = start + delay + j
                if dst < len(copyData):
                    copyData[dst] += int(attenuation * segment[j])

        # Clip to valid range
        copyData = np.clip(copyData, -32768, 32767)

        # Write the output WAV
        with wave.open(outputFile, 'wb') as writeFile:
            writeFile.setparams(wavDescriptor.getparams())
            writeFile.writeframes(copyData.astype(np.int16).tobytes())

def decode(pathToFile, messageLength):
    messageLength = int(messageLength
    bits = []
    with wave.open(pathToFile, 'rb') as w:
        fr = w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)

    delay0 = int(fr/100)    # 10ms
    delay1 = int(fr/50)     # 20ms
    blockSize = delay1*2

    for i in range(messageLength*8):
        start = i*blockSize
        end = start+blockSize
        if end > len(data): break
        seg = data[start:end]
        L = blockSize - delay1

        # compute cross-energies
        e0 = np.dot(seg[:L],    seg[delay0:delay0+L])
        e1 = np.dot(seg[:L],    seg[delay1:delay1+L])

        bits.append(0 if e0 > e1 else 1)

    # bits → string
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8: break
        val = sum([b << (7-j) for j,b in enumerate(byte)])
        chars.append(chr(val))
    msg = ''.join(chars)
    print("Decoded Message:", msg)
    return msg
        
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