import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

//First arguement file, second arguement message

public class lsb {
  public static void main(String[] args) {
    if(args.length == 0){
      System.out.println("No arguements detected!");
    }else{
      String audioFilePath = args[0];
	  String message = args[1];
	  String nameOfFile = args[2];
      byte[] audioBytes = getBytesFromAudioFile(audioFilePath);
	  int[] messageArray = messageToArray(message);
	  modifyWav(messageArray, audioBytes, nameOfFile);
	  
	  /*for(int i = 0; i < messageArray.length; i++){
		System.out.println(messageArray[i]);
	  }*/
      if (audioBytes != null) {
          System.out.println("Number of bytes read: " + audioBytes.length);
      } else {
          System.out.println("Failed to read audio file.");
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
        for(int i = 0; i < 100; i++){ //audioBytes.length
          System.out.println(audioBytes[i]);
        }
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
		modifiedArray[i] = (byte)((fileArray[i + 89] & 252) | messageArray[i]);
	}
	try(FileOutputStream out = new FileOutputStream(fileName)){
		out.write(modifiedArray);
	}catch (IOException e) {
		e.printStackTrace();
    }
}
	
}
