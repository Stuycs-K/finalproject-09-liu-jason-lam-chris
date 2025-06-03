import wave
import numpy as np
import sys

def encode(inWav, message, outWAV, delay=200, amp0=0.1, amp1=3):
    with wave.open(inWav, 'rb') as wf:
        params = wf.getparams()
        n_channels, sampwidth, framerate, n_frames, comptype, compname = params
        audio = np.frombuffer(wf.readframes(n_frames), dtype=np.int16).astype(np.float32)

    #if n_channels == 2:
        #audio = audio.reshape(-1, 2)
        #left = audio[:, 0].copy()
        #right = audio[:, 1].copy()
    #else:
        left = audio.copy()
        right = None

    bits = [int(b) for c in message for b in f"{ord(c):08b}"]
    print("Number of bits encoded:", int(len(bits) / 8))

    block = 2 * delay
    for i, bit in enumerate(bits):
        start = i * block
        if start + block >= len(left):
            print(f"Block {i} truncated, skipping")
            break
        amp = amp1 if bit else amp0
        for j in range(delay):
            left[start + delay + j] += amp * left[start + j]

    left = np.clip(left, -32768, 32767).astype(np.int16)

    if right is not None:
        audio = np.stack((left, right), axis=1).flatten()
    else:
        audio = left

    with wave.open(outWAV, 'wb') as wf:
        wf.setparams(params)
        wf.writeframes(audio.tobytes())

    print("Encoding done.")

def decode(inWav, num_bytes, delay=200):
    with wave.open(inWav, 'rb') as wf:
        params = wf.getparams()
        n_channels, sampwidth, framerate, n_frames, comptype, compname = params
        audio = np.frombuffer(wf.readframes(n_frames), dtype=np.int16).astype(np.float32)

    # if n_channels == 2:
    #     audio = audio.reshape(-1, 2)
    #     left = audio[:, 0]
    # else:
        left = audio

    bits = []
    block = 2 * delay
    for i in range(num_bytes * 8):
        start = i * block
        if start + block >= len(left):
            break
        x = left[start:start + delay] * (1.1)
        y = left[start + delay:start + 2 * delay]
        e0 = np.dot(x, x)
        e1 = np.dot(y, x)
        bit = 1 if abs(e1) > abs(e0) else 0
        print(f"Block {i}: e0={e0:.1f}, e1={e1:.1f} -> bit={bit}")
        bits.append(bit)

    chars = [chr(int("".join(map(str, bits[i:i+8])), 2)) for i in range(0, len(bits), 8)]
    print("Decoded message:", ''.join(chars))

if __name__ == "__main__":
    if sys.argv[1] == "encode":
        encode(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "decode":
        decode(sys.argv[2], int(sys.argv[3]))
