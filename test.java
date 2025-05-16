import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.awt.Color;
import java.io.File;

public class test {
    public static void main(String[] args) throws Exception {
        BufferedImage image = ImageIO.read(new File("0085.jpg"));

        Color color = new Color(image.getRGB(0, 0)); // Pixel at (0,0)

        System.out.println("Red: " + color.getRed());
        System.out.println("Green: " + color.getGreen());
        System.out.println("Blue: " + color.getBlue());
    }
}