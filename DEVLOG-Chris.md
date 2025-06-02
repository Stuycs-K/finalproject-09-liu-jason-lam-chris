# Dev Log:

This document must be updated daily every time you finish a work session.

## Chris Lam

### 2025-05-15 - Wrote pseduocode for LSB + Completed Proposal

Out for a visa interview during class but caught up with Jason afterwards.

Updated README briefly
Wrote up the proposal and planned what we'll be doing for the next two weeks - 1 hour
Wrote pseduocode for LSB using the previous visual LSB lab for refrence - 30 mins

### 2025-05-16 - Started Least Significant Byte and continued to research WAV headers
Started LSB code:
	- Transfered image steganography LSB to audio LSB - 20 mins
	- Learnt what the 44 bytes in a WAV header meant - 30 mins
	- Successfully wrote and debugged a byte reading function for a WAV (need to figure out how to get rid of the header) - 30 mins

### 2025-05-17 + 18 - Finished LSB Encoder + Decoder
LSB Encoder:
	Tried to incorporate all 44 bytes and failed - 1 hour
	Wrote a message to array function which mimicked the function of the lsb used in visual steganography - 30 mins
	Debugged a syntax error that would make my message to array change endianness - 30 mins
	Wrote modify array and write to a file - 2 hours
LSB Decoder:
	Wrote decode through bitwise functions much like the previous lab - 1 hour
	Decoded a bug where the order of bitwise functions messed with recombination - 30 mins

### 2025-05-19 - Researched + Started implementing Echo Hiding
Fixed LSB and PROPOSAL formatting - 15 mins
Researched WAV files and echo hiding - 1 hour
Finished code to open a WAV file and extract its channel, sample width, frame rate, and num of frames - 30 mins

### 05-20 - Text to Bit array + Echo encoding for MONO only (1 channel)
Made a function to convert ascii characters into a specific bit array that I need - 40 mins

Echo encoding (2 hours):

	- Learnt what signals were and decided and currently debating on whether or not to use them
	- Used extracted information from WAV file to have an echo and two delays, matched each delay to their corresponding bit array
	- Wrote write to a WAV file

### 05-21 - Debugging Echo encode
Fixed like 30 syntax bugs, cleaned up the code, made every parameter in a WAV file print, still need to test if it works by creating a working decode - 1 hour

### 05-22 - Started Echo decode

Finished debugging echo encode (hopefully) - 15 mins
Wrote starter working code for echo decode (need to test more extensively) - 1 hour
Replaced compare bits function with correlate from numpy - 15 mins

### 05-23 - Finished Echo Decode

Basically rewrote my previous decode by basically breaking audio to segments
Read more on this report on signals

### 05-24 + 05-25 - I am in so much pain (Echo Decode and maybe encode don't work at all)

why why why why why why why - 5 hours (ongoing)


### 05-26 Rewrote basically EVERYTHING from scratch

After yesterday, I spent like 4 hours rewriting and testing my new Echo encode and decode and on how to create a sinusoid WAV file. (This time I used dot products w/ the amplitudes of each segment)

### 05-27 Created Slides
Fixed formatting error on LSB
Created and worked on the slideshow, done with explaining different types of audio files

### 05-28 Updated slides

Finished slides and spent ~1 hour recording, though I need to redo my recording tomorrow because I keep blanking out.

### 05-29 - Wrote a script for the slides, finished recording.

In title.

### 05-30 - FIXED ECHOHIDING YES

Finally fixed a bug where I did not amplify the original segment with the 0 bit amplitude.

### 05-31 + 06-1 - Improved echo hiding
Made echoHiding work with particularly noisy audio, need a way to clip amplitudes though.