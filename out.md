![](img/Audio%20Steg_0.png)

![](img/Audio%20Steg_1.png)

![](img/Audio%20Steg_2.png)

<span style="color:#ffffff">INTRODUCTION TO </span>

<span style="color:#ffffff">AUDIO STEGANOGRAPHY</span>

<span style="color:#ffffff">Chris Lam\, Jason Liu</span>

![](img/Audio%20Steg_3.png)

![](img/Audio%20Steg_4.png)

![](img/Audio%20Steg_5.png)

Waveform Audio File \(WAV\)

Stores raw audio samples

Usually uncompressed

Easily able to be converted to other forms but also bigger file sizes

Structure:

44 Bytes Header

Audio Data

MPEG Audio Layer 3 \(MP3\)

Highly compressed audio by using lossy compression \(trades worse audio quality for smaller file sizes\)

Lossy compression gets rid of audio that is inaudible to the human ear

MPEG\-4 Part 14 \(MP4\)

Multimedia container \- can hold audio\, video\, images\, and other forms of data

![](img/Audio%20Steg_6.png)

![](img/Audio%20Steg_7.png)

![](img/Audio%20Steg_8.jpg)

![](img/Audio%20Steg_9.png)

![](img/Audio%20Steg_10.png)

![](img/Audio%20Steg_11.png)

![](img/Audio%20Steg_12.png)

![](img/Audio%20Steg_13.png)

![](img/Audio%20Steg_14.png)

<span style="color:#ffffff">Sampling Rate \- Samples per one second \(Hz\)</span>

<span style="color:#ffffff">Sample \- Amplitude of waveform at a given time \(Higher amplitude = louder sounds\)</span>

<span style="color:#ffffff">Channels \- Audio steam </span>

<span style="color:#ffffff">Mono \- 1 channel</span>

<span style="color:#ffffff">Stereo \- 2 channel</span>

<span style="color:#ffffff">Frame \- Set of samples at a given time</span>

<span style="color:#ffffff">Nyquist–Shannon sampling theorem \- smart person said that to accurately recreate a WAV\, sampling rate should be at least twice the highest frequency </span>

![](img/Audio%20Steg_15.png)

Old white dude with glasses so it's probably Nyquist idk I didn’t double check

![](img/Audio%20Steg_16.png)

![](img/Audio%20Steg_17.png)

![](img/Audio%20Steg_18.png)

![](img/Audio%20Steg_19.png)

<span style="color:#ffffff">In NUMPY we trust</span>

<span style="color:#ffffff">y = A sin\(ωt \+ φ\)</span>

<span style="color:#ffffff">A: amplitude </span>

<span style="color:#ffffff">ω: angular frequency \(2π\* frequency\)</span>

<span style="color:#ffffff">t: time</span>

<span style="color:#ffffff">φ: phase </span>

<span style="color:#ffffff">samples = \(amplitude \* np\.sin\(2 \* np\.pi \* freq \* t\)\)</span>

![](img/Audio%20Steg_20.png)

![](img/Audio%20Steg_21.png)

![](img/Audio%20Steg_22.png)

<span style="color:#ffffff">Least Significant Bit \(LSB\)</span>

![](img/Audio%20Steg_23.jpg)



* If you recall from visual steganography\, we changed the color of some pixels in the image by encoding some bits into their least significant value\.
* The bytes in a WAV file are the samples of the audio file\, meaning\, if we encode with LSB we will change the loudness of certain parts of the audio\. WAV files are little endian\, meaning we will have to change the first bit\.


![](img/Audio%20Steg_24.png)

![](img/Audio%20Steg_25.jpg)

![](img/Audio%20Steg_26.jpg)

![](img/Audio%20Steg_27.png)



* <span style="color:#ffffff">Literal witchcraft</span>
* <span style="color:#ffffff">I hate it so much it made me bilingual: “我讨厌 echo hiding”</span>
  * <span style="color:#ffffff">Translation: “I hate echo hiding” </span>
* <span style="color:#ffffff">Take </span>  <span style="color:#ffffff">segments</span>  <span style="color:#ffffff"> of the original audio\, delay the </span>  <span style="color:#ffffff">segments using one of two predefined delays\, </span>  <span style="color:#ffffff">and then add the </span>  <span style="color:#ffffff">segments</span>  <span style="color:#ffffff"> back into the original audio</span>
  * <span style="color:#ffffff">The distinct time intervals correspond to what bits will be turned on when decoding</span>


![](img/Audio%20Steg_28.png)

__What if I don’t have the original audio?__

__You cry__

__Autocorrelation__

![](img/Audio%20Steg_29.png)

![](img/Audio%20Steg_30.png)

<span style="color:#ffffff">Echo Hiding Pt 2</span>

<span style="color:#ffffff">Phase changes are harder for human ears to perceive </span>

<span style="color:#ffffff">Remember Ohm? Ohm’s Acoustic Law \(we analyze sounds through frequency\)</span>

<span style="color:#ffffff">Temporal masking \(loud sound masks quiet sound\)</span>

<span style="color:#ffffff">Decode:</span>

<span style="color:#ffffff">	Loop through the segments</span>

<span style="color:#ffffff">	Dot product of two signals shows how similar the two signals are to one another</span>

<span style="color:#ffffff">	Compare dot products between corresponding delay times</span>

![](img/Audio%20Steg_31.jpg)

![](img/Audio%20Steg_32.png)

![](img/Audio%20Steg_33.png)

![](img/Audio%20Steg_34.png)

![](img/Audio%20Steg_35.png)

![](img/Audio%20Steg_36.png)

<span style="color:#ffffff">Image\-Audio Conversion</span>



* <span style="color:#ffffff">Images can be converted into an audio file and be hidden in the spectrogram</span>
* <span style="color:#ffffff">What is a spectrogram?</span>
* <span style="color:#ffffff">A Spectrogram consists of a set of 2D arrays</span>
  * <span style="color:#ffffff">Time Buckets: X\-Axis</span>
  * <span style="color:#ffffff">Frequency Buckets: Y\-Axis</span>
  * <span style="color:#ffffff">Magnitude: Variable 1</span>
  * <span style="color:#ffffff">Phase: Variable 2</span>


![](img/Audio%20Steg_37.png)

![](img/Audio%20Steg_38.png)

![](img/Audio%20Steg_39.png)

![](img/Audio%20Steg_40.png)

<span style="color:#ffffff">Image Preparation</span>

![](img/Audio%20Steg_41.png)

![](img/Audio%20Steg_42.png)

<span style="color:#ffffff">Convert Image into Array of Pixels\.</span>

<span style="color:#ffffff">Create Array of Normalized Values Grayscale for the Pixels</span>

<span style="color:#ffffff">Flip Image as STFT and Image treat 2D arrays differently</span>

![](img/Audio%20Steg_43.png)

![](img/Audio%20Steg_44.png)

![](img/Audio%20Steg_45.png)

![](img/Audio%20Steg_46.png)

<span style="color:#ffffff">Audio</span>  <span style="color:#ffffff"> Preparation</span>

![](img/Audio%20Steg_47.png)

![](img/Audio%20Steg_48.png)

<span style="color:#ffffff">Load an audio file</span>

<span style="color:#ffffff">Perform Short\-Time Fourier Transformation to get Spectrogram Information</span>

<span style="color:#ffffff">Acquire Array of Magnitude and Phase values</span>

![](img/Audio%20Steg_49.png)

![](img/Audio%20Steg_50.png)

![](img/Audio%20Steg_51.png)

![](img/Audio%20Steg_52.png)

<span style="color:#ffffff">Creating Magnitudes</span>

![](img/Audio%20Steg_53.png)

![](img/Audio%20Steg_54.png)

<span style="color:#ffffff">Resize Image to be size of STFT Magnitude Array</span>

<span style="color:#ffffff">Optionally change mode so that white or black is the main color</span>

<span style="color:#ffffff">Change the strength of the values for visibility</span>

<span style="color:#ffffff">Scale values to maximum magnitude</span>

![](img/Audio%20Steg_55.png)

![](img/Audio%20Steg_56.png)

![](img/Audio%20Steg_57.png)

![](img/Audio%20Steg_58.png)

![](img/Audio%20Steg_59.png)

![](img/Audio%20Steg_60.png)

<span style="color:#ffffff">Combine new Magnitude with original phase</span>

<span style="color:#ffffff">Use Inverse Short\-Time Fourier Transformation</span>  <span style="color:#ffffff">Save Audio</span>

![](img/Audio%20Steg_61.png)

![](img/Audio%20Steg_62.png)

![](img/Audio%20Steg_63.png)

![](img/Audio%20Steg_64.png)

![](img/Audio%20Steg_65.png)

<span style="color:#ffffff">Image\-Audio Embedding</span>

<span style="color:#ffffff">Images can also be embedded within the spectrogram of an audio file\.</span>

<span style="color:#ffffff">Well Known Example:</span>

<span style="color:#ffffff">Doom </span>  <span style="color:#ffffff">Soundtrack</span>

![](img/Audio%20Steg_66.png)

![](img/Audio%20Steg_67.png)

![](img/Audio%20Steg_68.png)

![](img/Audio%20Steg_69.png)

<span style="color:#ffffff">Applying Magnitudes</span>

![](img/Audio%20Steg_70.png)

<span style="color:#ffffff">Add normalized values to the already existing audio array</span>

<span style="color:#ffffff">Modifications done to visibility </span>

![](img/Audio%20Steg_71.png)

![](img/Audio%20Steg_72.png)

![](img/Audio%20Steg_73.png)

![](img/Audio%20Steg_74.png)

<span style="color:#ffffff">Can be very subtle when applied correctly</span>

<span style="color:#ffffff">Not viewable on first glance as spectrogram has to be contorted</span>

<span style="color:#ffffff">Very Documented Method leading to it being </span>  <span style="color:#ffffff">easier</span>  <span style="color:#ffffff"> to detect</span>

<span style="color:#ffffff">Image Quality and Visibility </span>  <span style="color:#ffffff">Degradation</span>  <span style="color:#ffffff"> with high quality resulting in louder </span>  <span style="color:#ffffff">disturbances</span>

![](img/Audio%20Steg_75.png)

![](img/Audio%20Steg_76.png)

![](img/Audio%20Steg_77.png)

![](img/Audio%20Steg_78.jpg)



  * <span style="color:#ffffff">Color Priority Mode</span>  <span style="color:#ffffff"> \(Dark\, Light\)</span>
* <span style="color:#ffffff">Whether the image should be drawn based on dark sections or light sections of images</span>
  * <span style="color:#ffffff">Visibility Percentage</span>
* <span style="color:#ffffff">How bright should the entire image be on the spectrogram</span>
* <span style="color:#ffffff">Time Resolution Multiplier & Frequency Resolution Multiplier </span>
* <span style="color:#ffffff">Multipliers on Image Quality</span>
* <span style="color:#ffffff">Increases Run Time</span>


![](img/Audio%20Steg_79.png)

![](img/Audio%20Steg_80.png)

![](img/Audio%20Steg_81.png)

![](img/Audio%20Steg_82.png)

![](img/Audio%20Steg_83.png)



  * <span style="color:#ffffff">Color Priority Mode \(Dark\, Light\)</span>
* <span style="color:#ffffff">Whether the image should be drawn based on dark sections or light sections of images</span>
  * <span style="color:#ffffff">Visibility Percentage</span>
* <span style="color:#ffffff">How bright should the entire image be on the spectrogram</span>
* <span style="color:#ffffff">Time Resolution Multiplier & Frequency Resolution Multiplier </span>
* <span style="color:#ffffff">Multipliers on Image Quality</span>
* <span style="color:#ffffff">Increases Run Time</span>


![](img/Audio%20Steg_84.png)

![](img/Audio%20Steg_85.png)

![](img/Audio%20Steg_86.png)

![](img/Audio%20Steg_87.png)



  * <span style="color:#ffffff">Color Priority Mode \(Dark\, Light\)</span>
* <span style="color:#ffffff">Whether the image should be drawn based on dark sections or light sections of images</span>
  * <span style="color:#ffffff">Visibility Percentage</span>
* <span style="color:#ffffff">How bright should the entire image be on the spectrogram</span>
* <span style="color:#ffffff">Time Resolution Multiplier & Frequency Resolution Multiplier </span>
* <span style="color:#ffffff">Multipliers on Image Quality</span>
* <span style="color:#ffffff">Increases Run Time</span>


![](img/Audio%20Steg_88.png)

![](img/Audio%20Steg_89.png)

![](img/Audio%20Steg_90.png)

![](img/Audio%20Steg_91.png)

![](img/Audio%20Steg_92.png)

<span style="color:#ffffff">Bytes can be encrypted with an audio file by modifying the phases found to indicate 0s and 1s</span>

<span style="color:#ffffff">How is this done?</span>

<span style="color:#ffffff">Phases are modified into a new audio file</span>

<span style="color:#ffffff">New audio file is compared to old to find a difference</span>

<span style="color:#ffffff">Phase changes are hard for the human ear to perceive</span>

![](img/Audio%20Steg_93.png)

![](img/Audio%20Steg_94.png)

