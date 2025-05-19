import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;


//First arguement file, second arguement message

public class lsb {
  public static void main(String[] args) {
    if(args.length == 0){
      System.out.println("No arguements detected!  Use 'make' for syntax");
    }else{
	  if(args[0].equals("encode")){
      String audioFilePath = args[1];
	  String message = args[2];
	  String nameOfFile = args[3];
      byte[] audioBytes = getBytesFromAudioFile(audioFilePath);
	  int[] messageArray = messageToArray(message);
	  modifyWav(messageArray, audioBytes, nameOfFile);
	  
	  /*for(int i = 0; i < messageArray.length; i++){
		System.out.println(messageArray[i]);
	  }*/
      if (audioBytes != null) {
          System.out.println("Number of bytes changed: " + messageArray.length);
      } else {
          System.out.println("Failed to read audio file.");
		}
	  }else if(args[0].equals("decode")){
		String audioFilePath = args[1];
		int numOfBytes = Integer.parseInt(args[2]);
		byte[] audioBytes = getBytesFromAudioFile(audioFilePath);
		for(int i = 0; i< 10; i++){
			System.out.println(audioBytes[i + 96]);
		}
		decode(audioBytes, numOfBytes);
	  }else{
		System.out.println("Invalid arguements! Use 'make' for syntax");
	  }
  }
}

    public static byte[] getBytesFromAudioFile(String filePath) {
        File audioFile = new File(filePath);
        byte[] audioBytes = new byte[(int) audioFile.length()];

        try (FileInputStream fileInputStream = new FileInputStream(audioFile)) {
            fileInputStream.read(audioBytes);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
        /*for(int i = 0; i < 100; i++){ //audioBytes.length
          System.out.println(audioBytes[i]);
        }*/
        return audioBytes;
    }

//This should be done with bitwise operations but I originally did it with exponents
public static int[] messageToArray(String s) {
  int[]parts = new int[s.length() * 4]; //optionally include the terminating character here.
  //calculate the array
  for(int i = 0; i < s.length(); i++){
    int num = s.charAt(i);
     //print(num + " ");
    int indexcount = 0;
    for(int j = 7; j > -1; j--){
        //System.out.print(j + " da ");
        int count = 0;
        if(num >= Math.pow(2, j)){
          count += 2;
          num -= Math.pow(2, j);
        }
        j--;
        if(num >= Math.pow(2, j)){
          count++;
          num -= Math.pow(2, j);
        }
        //print(count);
        parts[i * 4 + indexcount] = count;
        indexcount++;
    }
  }

  /**Verify the contents of the array before you do more.
   'T' -> 01010100 -> 01 01 01 00 -> 1, 1, 1, 0
   'h' -> 01101000 -> 01 10 10 00 -> 1, 2, 2, 0
   'i' -> 01101001 -> 01 10 10 01 -> 1, 2, 2, 1
   's' -> 01110011 -> 01 11 00 11 -> 1, 3, 0, 3
   ...etc.
   So your data array would look like this:
   { 1, 1, 1, 0, 1, 2, 2, 0, 1, 2, 2, 1, 1, 3, 0, 3...}
   */
  //ln(Arrays.toString(parts));
  return parts;
}

public static void modifyWav(int[] messageArray, byte[]fileArray, String fileName){
	byte[] modifiedArray = fileArray.clone();
	
	for(int i = 0; i < messageArray.length; i++){
		modifiedArray[i + 96] = (byte)((fileArray[i] & 252) | messageArray[i]);
	} 
	try(FileOutputStream out = new FileOutputStream(fileName)){
		out.write(modifiedArray);
	}catch (IOException e) {
		e.printStackTrace();
    }
}

public static void decode(byte[] audioBytes, int numOfBytes){
	for(int i = 96; i < (numOfBytes / 4) + 96; i = i + 4){
		System.out.println("daha");
		int temp = audioBytes[i] & 3;
		int temp2 = audioBytes[i + 1] & 3;
		int temp3 = audioBytes[i + 2] & 3;
		int temp4 = audioBytes[i + 3] & 3;
		char temp5 = (char)(temp << 6 + temp2 << 4 + temp3 << 2 + temp4);
		System.out.println(temp5);
	}
}
	
}
