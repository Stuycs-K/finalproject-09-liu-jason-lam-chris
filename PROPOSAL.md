# Final Project Proposal

## Group Members:

Chris Lam & Jason Liu

# Intentions:

We plan to create and implement steganographic algorithms to hide and retrieve data in audio files. To the human ear, the modified audio file should be practically indistinguishable from the original audio.


# Intended usage:

This program will prompt the user for an audio file, data to be encrypted, and the method of encryption, and return a modified audio file.

Afterwords, the user may retrieve the hidden data from the modified audio file if applicable (for spectrograms users should just use a third party tool like ``audacity``).

# Technical Details:

The technical design for our programs will be similar to our previous lab of image steganography, only this time, we will not be using processing (because we have audacity to see the spectrograms).

We will be attempting to create three different algorithms to encode messages:

Least Significant Bit - We have already covered this in class, but with audio, each byte represents a tiny frame of the entire recording (almost like a pixel for a photo). By using the binary operations **AND** to zero out the last two bits and **OR** to encode one letter of our message into the last two bits, we are able to encode messages without disorting the original sound too much. Chris will be responsible for this part.

Spectrogram Image Embedding - Spectrograms are a visual representation of an audio's frequency or noisiness vs time. Therefore, by manipulating a sound's loudness at certain intervals, you can hide text, symbols, and even images in a spectrogram. Many video game developers have used this to hide easter eggs in their soundtracks. Jason will be responsible for this part.


# Intended pacing:

5/16 - Most of the setup should be finished (makefile, organizing sample audios into folders, etc).

5/19 - Encode for least significant byte and PNG to WAV should also be finished.

5/21 - Decode for least significant byte should be finished and tested.

5/22 - Spectrogram image embedding should be finished and tested.

5/26 - Frequency masking should be finished and tested.

5/27 - Testing, document all bugs, etc. Slides and video presentation should be done by this point.

5/28 - Final updates on github repo.
