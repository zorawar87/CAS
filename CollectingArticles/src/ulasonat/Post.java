package ulasonat;

public class Post {

    private static int counter = 0;

    private int id;
    private String text;
    private String url;
    private String website;
    private String date;


    public Post(String text, String url, String website, String date) {
        this.text = text;
        this.url = url;
        this.website = website;
        this.date = date;
        this.id = ++counter;
    }

    @Override
    public String toString() {

        return id + "~en~" + (url != null ? url : "")
                + "~" + (text != null ? text : "")
                + "~~~" + (website != null ? website : "")
                + "~" + (date != null ? date : "");
    }
}
