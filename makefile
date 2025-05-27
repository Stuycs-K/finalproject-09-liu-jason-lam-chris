.PHONY: lsb echo create convert embed clean
usage:
	@echo "There are 5 programs avaliable for different types of audio steganography. Listed below are descriptions and how to use them.\n"
	@echo "First function is lsb (Least Significant Bit) encoding and decoding.\n     make lsb ARGS=\"encode PathtoAudio Message OutputName\"\n     make lsb ARGS=\"decode PathtoAudio NumberofBytes\"\n"
	@echo "Second function is Echo Hiding encoding and decoding.\n     make echo ARGS=\"encode PathtoAudio Message OutputName\"\n     make echo ARGS=\"decode PathtoAudio NumberofBytes\"\n"
	@echo "Third function is Wav Create which is needed to create the input file for echo hiding.\n     make create\n"
	@echo "Fourth function is Image to Audio Conversion.\n     make convert ARGS=\"ImageName OutputName ColorPriorityMode VisibilityPercentage TimeResolutionMultiplier FrequencyResolutionMultiplier\"\n"
	@echo "Fifth function is Image embedding into Audio.\n     make embed ARGS=\"ImageName AudioName OutputName ImageHeight ImageLength ImageStartX ImageStartY ColorPriorityMode VisibilityPercentage TimeResolutionMultiplier FrequencyResolutionMultiplier\"\n"
compile:
	javac lsb.java
lsb:
	@java lsb $(ARGS)
echo:
	@python3 echoHiding.py $(ARGS)
create:
	@python3 wavCreate.py $(ARGS)
convert:
	@python3 SpectImg.py $(ARGS)
embed:
	@python3 SpecImgEmb.py $(ARGS)
clean:
	@rm -f lsb.class
	@echo "Cleaned up files!"
