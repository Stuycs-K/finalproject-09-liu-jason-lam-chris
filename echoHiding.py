import wave
import numpy as np
import sys
import scipy.signal

def data_to_bits(msg):
    bits = []
    for c in msg:
        b = ord(c)
        bits += [(b >> i) & 1 for i in range(7, -1, -1)]
    return np.array(bits, dtype=np.uint8)

def bits_to_string(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8: break
        val = sum(bit << (7-j) for j, bit in enumerate(byte))
        chars.append(chr(val))
    return ''.join(chars)

def encode(input_wav, message, output_wav):
    bits = data_to_bits(message)
    with wave.open(input_wav,'rb') as wf:
        params = wf.getparams()
        fs = wf.getframerate()
        data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int32)

    # Parameters
    d0 = int(fs * 0.03)   # 10ms
    d1 = int(fs * 0.06)   # 20ms
    pilot_len = 256       # samples
    pilot_gain = 1.0      # full-strength pilot
    echo_gain  = 0.6      # echo of pilot only
    block = pilot_len + max(d0, d1) + pilot_len

    out = data.copy()
    for i, bit in enumerate(bits):
        start = i * block
        if start + block >= len(data): break
        pilot = data[start:start+pilot_len]

        # 1) Inject pilot (strong)
        out[start:start+pilot_len] += (pilot_gain * pilot).astype(np.int16)

        # 2) Echo pilot at delay
        delay = d0 if bit==0 else d1
        pos = start + delay
        out[pos:pos+pilot_len] += (echo_gain * pilot).astype(np.int16)

    out = np.clip(out, -32768, 32767).astype(np.int16)
    with wave.open(output_wav,'wb') as wf:
        wf.setparams(params)
        wf.writeframes(out.tobytes())
    print("Encoded.")

def decode(input_wav, msg_len):
    with wave.open(input_wav,'rb') as wf:
        fs = wf.getframerate()
        data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int32)

    d0 = int(fs * 0.03)
    d1 = int(fs * 0.06)
    pilot_len = 256
    block = pilot_len + max(d0, d1) + pilot_len

    bits = []
    for i in range(msg_len * 8):
        start = i * block
        if start + block >= len(data): break
        pilot = data[start:start+pilot_len]
        seg0  = data[start+d0 : start+d0+pilot_len]
        seg1  = data[start+d1 : start+d1+pilot_len]

        e0 = np.dot(pilot, seg0)
        e1 = np.dot(pilot, seg1)
        bits.append(0 if e0 > e1 else 1)
        print(f"Block {i}: e0={e0}, e1={e1}")
    msg = bits_to_string(bits)
    print("Decoded:", msg)
    return msg

if __name__ == "__main__":
    if sys.argv[1]=="encode":
        encode(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1]=="decode":
        decode(sys.argv[2], int(sys.argv[3]))
    else:
        print("Usage: encode <in.wav> <msg> <out.wav> | decode <in.wav> <len>")