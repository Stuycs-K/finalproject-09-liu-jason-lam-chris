# Dev Log:

This document must be updated daily every time you finish a work session.

## Jason Liu

### 2024-05-15 - Researching Audio Steganography
Did research on different methods of steganography,
- Least Significant Bit
- Phase Coding
- Echo Hiding
- Spread Spectrum
- Frequency Masking
- Spectrogram Image Imbedding

Chris has to do something today so wasn't able to discuss what we will do for project in class but likely,,
- Least Significant Bit
- Spectrogram Image Imbedding
- and one other method

Did some research on how to make an image into a spectrogram.

Made a function to take in an image, grayscale it, and then normalize the values into an array. However to make it a spectrogram I think I have to use python.

### 2024-05-16 - Worked on Spectrogram Image Imbedding

Started preliminary code in turning an image into a wav file with message hidden in spectrogram.

### 2024-05-17 - Deepened understanding of Spectrogram Image Imbedding, Started making program more usable.

Did more research into what functions do as well as code behaviors.

### 2024-05-19 - Made Spectrogram Image have arguements. Finished preliminary program to hide in audio file.

Added commands for different factors of image in the spectrogram. 
Finished coding a method to add image to an existing spectrogram.
Need to add command line args.

### 2024-05-20 - Added arguements to program to instead hide image within existing audio.

Added commands for different factors of image in the spectrogram. 
Will start researching other methods.
Researched Phase Encoding

- https://medium.com/@achyuta.katta/audio-steganography-using-phase-encoding-d13f100380f2

made a basic plan of how to intiate it.

### 2024-05-21 - AP Macroeconomics Test + Research

Did research on how stft allows me to change phases and then made a pseudo code type plan.
Didn't end up doing much bc AP Macro today and AP Calc BC tmrw.
So I did end up doing work I made the code for phase encoding need to make decoding tmrw.

### 2024-05-22 - Worked on Phase Encoding

Did like basics for phase encoding
Will work on decoder tomorrow

### 2024-05-23 - Worked on Phase Encoding

Made decoder and realized encoder does not work so I need to switch approaches as my current one doesn't work
Did research on other method using DFT so imma try that tmrw

### 2024-05-26 - Testing on Phase Encoding

Did some testing to little to no sucess so no commits