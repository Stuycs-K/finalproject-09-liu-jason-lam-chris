import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.awt.Color;
import java.io.File;
import java.io.IOException;


public class test {
    public static void main(String[] args) throws Exception {
        // Initial Image Opening
        BufferedImage image = ImageIO.read(new File("0085.jpg"));
        int width = image.getWidth();
        int height = image.getHeight();
        // New Image Creation
        BufferedImage creation = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        // Color[][] grayscale = new Color[width][height];
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
        
        try {
            ImageIO.write(creation, "png", new File("output.png"));
            System.out.println("Image saved as output.png");
        } catch (IOException e) {
            e.printStackTrace();
        }
        // Color color = new Color(image.getRGB(0, 0)); // Pixel at (0,0)

        // System.out.println("Red: " + color.getRed());
        // System.out.sprintln("Green: " + color.getGreen());
        // System.out.println("Blue: " + color.getBlue());
    }
}