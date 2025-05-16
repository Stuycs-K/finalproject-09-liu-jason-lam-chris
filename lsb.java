import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

public class lsb {
  public static void main(String[] args) {
    if(args.length == 0){
      System.out.println("No arguements detected!");
    }else{
      String audioFilePath = args[0];
      byte[] audioBytes = getBytesFromAudioFile(audioFilePath);
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
        for(int i = 0; i < audioBytes.length; i++){
          System.out.println(audioBytes[i]);
        }
        return audioBytes;
    }


}
