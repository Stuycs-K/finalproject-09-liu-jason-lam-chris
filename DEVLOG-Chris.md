# Dev Log:

This document must be updated daily every time you finish a work session.

## Chris Lam

### 2024-05-15 - Wrote pseduocode for LSB + Completed Proposal

Out for a visa interview during class but caught up with Jason afterwards.
 
Updated README briefly
Wrote up the proposal and planned what we'll be doing for the next two weeks - 1 hour 
Wrote pseduocode for LSB using the previous visual LSB lab for refrence - 30 mins

### 2024-05-16 - Started Least Significant Byte and continued to research WAV headers
Started LSB code:
	- Transfered image steganography LSB to audio LSB - 20 mins
	- Learnt what the 44 bytes in a WAV header meant - 30 mins
	- Successfully wrote and debugged a byte reading function for a WAV (need to figure out how to get rid of the header) - 30 mins

### 2024-05-17 + 18 - Finished LSB Encoder + Decoder
LSB Encoder:
	Tried to incorporate all 44 bytes and failed - 1 hour
	Wrote a message to array function which mimicked the function of the lsb used in visual steganography - 30 mins
	Debugged a syntax error that would make my message to array change endianness - 30 mins
	Wrote modify array and write to a file - 2 hours
LSB Decoder:
	Wrote decode through bitwise functions much like the previous lab - 1 hour
	Decoded a bug where the order of bitwise functions messed with recombination - 30 mins
