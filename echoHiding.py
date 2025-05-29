import wave
import numpy as np
import sys

def encode(inWav, message, outWav, delay=500, amp0=0.05, amp1=0.25):
    with wave.open(inWav, 'rb') as wf:
        params = wf.getparams()
        audio = np.frombuffer(wf.readframes(params.nframes), dtype=np.int16).astype(np.float32)

    bits = [int(b) for c in message for b in f"{ord(c):08b}"]
    print("Encoding bits:", bits)

    block = 2 * delay
    for i, bit in enumerate(bits):
        start = i * block
        if start + block >= len(audio):
            print(f"Block {i} truncated, skipping")
            break
        amp = amp1 if bit else amp0
        for j in range(delay):
            audio[start + delay + j] += amp * audio[start + j]

    audio = np.clip(audio, -32768, 32767).astype(np.int16)
    with wave.open(outWav, 'wb') as wf:
        wf.setparams(params)
        wf.writeframes(audio.tobytes())
    print("Encoding done.")

def decode(inWav, num_bytes, delay=500):
    with wave.open(inWav, 'rb') as wf:
        audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32)
    bits = []
    block = 2 * delay
    for i in range(num_bytes * 8):
        start = i * block
        if start + block >= len(audio):
            break
        x = audio[start:start + delay]
        y = audio[start + delay:start+ 2 * delay]
        e0 = np.dot(x, x)
        e1 = np.dot(y, x)
        bit = 1 if abs(e1) > abs(e0) else 0
        print(f"Block {i}: e0={e0:.1f}, e1={e1:.1f} -> bit={bit}")
        bits.append(bit)

    chars = [chr(int("".join(map(str, bits[i:i+8])), 2)) for i in range(0, len(bits), 8)]
    print("Decoded message:", ''.join(chars))

# CLI
if __name__ == "__main__":
    if sys.argv[1] == "encode":
        encode(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "decode":
        decode(sys.argv[2], int(sys.argv[3]))
