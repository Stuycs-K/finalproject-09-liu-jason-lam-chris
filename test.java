import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.awt.Color;
import java.io.File;
import java.io.IOException;
import java.util.Arrays;

public class test {
    public static void main(String[] args) throws Exception {
        // Initial Image Opening
        BufferedImage image = ImageIO.read(new File("0085.jpg"));
        int width = image.getWidth();
        int height = image.getHeight();
        // New Image Creation
        BufferedImage creation = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        // Looping
        for(int i = 0; i < height; i++){
            for(int j = 0; j < width; j++){
                int pixel = image.getRGB(j, i);
                int red   = (pixel >> 16) & 0xff;
                int green = (pixel >> 8) & 0xff;
                int blue  = pixel & 0xff;
                int greyScale = (int)(0.299 * red + 0.587 * green + 0.114 * blue);
                creation.setRGB(j, i, (greyScale << 16) | (greyScale << 8) | greyScale);
            }
        }
        // Making file
        try {
            ImageIO.write(creation, "png", new File("output.png"));
            System.out.println("Image saved as output.png");
        } catch (IOException e) {
            e.printStackTrace();
        }
        // Making array of normalized variables for the imagexs
        double normalizedMagnitudes[][] = new double[height][width]; 
        for(int i = 0; i < height; i++){
            for(int j = 0; j < width; j++){
                int pixel = creation.getRGB(j, i);
                double red = ((pixel >> 16) & 0xff)/255.0;
                normalizedMagnitudes[i][j] = red;
            }
        }
    }
}