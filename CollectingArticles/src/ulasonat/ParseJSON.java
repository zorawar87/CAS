package ulasonat;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class ParseJSON {

    public static ArrayList<Post> getNews(JSONArray articles, int nArticles) {
        return null;
    }

    /** @return */
    public static JSONArray getPosts(JSONObject jsonObject) throws JSONException {
        return jsonObject.getJSONArray("posts");
    }
}
