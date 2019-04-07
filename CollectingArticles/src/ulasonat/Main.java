package ulasonat;

import org.json.*;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class Main {


    private static ArrayList<String> urls;
    private static ArrayList<Post> posts = new ArrayList<>();
    private static int postsPerUrl = 100;

    public static void main(String[] args) throws IOException, JSONException {
        FileReader readFile = new FileReader("urls.txt");
        urls = readFile.getURLs();
        addPosts();
        writeToFile("output.csv");
    }

    private static void addPosts() throws IOException, JSONException {
        int cnt = 0;
        int total = urls.size();
        for(int i=0; i<urls.size(); i++) {
            System.out.println("Reading (" + (++cnt) + "/" + total + ")");
            JSONObject jsonObject = ReadJSON.readJsonFromUrl(urls.get(i));
            JSONArray jsonArray = ParseJSON.getPosts(jsonObject);
            for(int j=0; j<postsPerUrl; j++) {
                String text = (String) jsonArray.getJSONObject(j).get("text");
                String url = (String) jsonArray.getJSONObject(j).get("url");
                JSONObject thread = (JSONObject) jsonArray.getJSONObject(j).get("thread");
                String website = (String) thread.get("site");
                String date = (String) jsonArray.getJSONObject(j).get("published");

                posts.add(new Post(text, url, website, date));
            }
        }
    }

    private static void writeToFile(String fileName) throws IOException {
        String fileContent = "";
        int cnt = 0;
        int total = urls.size() * 100;
        for(Post p : posts) {
            cnt++;
            if(cnt % 100 == 0)
                System.out.println("Writing (" + cnt + "/" + total + ")");
            fileContent += p + "\n";
        }

        BufferedWriter writer = new BufferedWriter(new FileWriter(fileName));
        writer.write("Id⁓language⁓Link⁓Text⁓Keywords⁓Sentiment⁓Website⁓Date\n");
        writer.write(fileContent);
        writer.close();
    }
}
