[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/am3xLbu5)
# Audio Steganography
 
### Hallucinosis Jammers

Jason Liu
Chris Lam
       
### Project Description:

We implemented 4 different methods for hiding messages or images within audio files.
The methods are as follows:
- Least Significant Bit
- Echo Hiding
- Image to Audio Conversion
- Embedding Image into Audio

### Project Video Link:

https://drive.google.com/file/d/15zl53tLId5RjmunLWLDLJRGcOCXgA6Vr/view?usp=sharing

Zoom scuffed up the recording for some reason so lower portion of screen was a bit cut off.

### Instructions:

All the utility is listed under the make file as default or make usage.

### Resources/ References:

https://svenruppert.com/2024/04/17/audio-steganography-in-more-detail/  - Basic overview of audio steagnography

https://docs.fileformat.com/audio/wav/ - WAV file header

https://docs.python.org/3.13/library/wave.html - Python WAV library

https://arxiv.org/html/2408.13277v2 - Echo hiding explanation and example in Python
http://www.fim.uni-linz.ac.at/lva/Rechtliche_Aspekte/2001SS/Stegano/leseecke/echo%20data%20hiding%20by%20d.%20gruhl%20and%20w.%20bender.pdf - Useful diagrams for echo hiding

https://numpy.org/doc/2.1/reference/generated/numpy.correlate.html - Numpy correlate documentation

https://medium.com/@AungKyawZall/audio-steganography-39f9fb6d9330 - Base ideas that led to Spectrogram work

https://librosa.org/doc/0.11.0/generated/librosa.stft.html - Documentation for stft used in Spectrogram

https://medium.com/@achyuta.katta/audio-steganography-using-phase-encoding-d13f100380f2 - Research about Phase Encoding (Did not end up in final project)

