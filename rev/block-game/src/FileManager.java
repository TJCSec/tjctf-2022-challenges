import java.io.FileOutputStream;

public class FileManager {
    public static void saveData(byte[] data) {
        try {
            FileOutputStream fos = new FileOutputStream("data.dat");
            fos.write(data);
            fos.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
