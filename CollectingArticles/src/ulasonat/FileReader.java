package ulasonat;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

public class FileReader {

    private ArrayList<String> urls;

    public FileReader(String fileName) throws IOException {
        urls = new ArrayList<>();
        addURLs(fileName);
    }

    public void addURLs(String fileName) throws IOException {
        File file = new File(fileName);
        Scanner scanner = new Scanner(file);

        while (scanner.hasNextLine())
            urls.add(scanner.nextLine());
    }

    public ArrayList<String> getURLs() {
        return urls;
    }
}

