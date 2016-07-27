import java.util.Date;
import java.text.Format;
import java.text.SimpleDateFormat;

/**
 * This is a simulation of a post.
 * 
 * @author xiaopei
 *
 */
public class Post {

	private String username;
	private long timestamp;
	
	/**
	 * Class constructor specifying user who posts.
	 * 
	 * @param postname the string that represents username.
	 */
	public Post(String postname) {
		username = postname;
		timestamp = System.currentTimeMillis();
	}
	
	/**
	 * A copy constructor.
	 * 
	 * @param another the post that is being copied.
	 */
	public Post(Post another) {
		username = another.username;
		timestamp = another.timestamp;
	}
	
	/**
	 * Get the username of this post.
	 * 
	 * @return the string that represents the username.
	 */
	public String getUsername() {
		return username;
	}
	
	/**
	 * Change the username of this post.
	 * 
	 * @param name the string that represents the to-be username.
	 */
	public void setUsername(String name) {
		username = name;
	}
	
	/**
	 * Get the timestamp when this post is created.
	 * 
	 * @return the string that shows when this post is created.
	 */
	public String getTimestamp() {
		String time;
		long current = System.currentTimeMillis();
		if(current - timestamp <= 1000) {
			time = "1 second ago";
		}
		else if(current - timestamp < 60000) {
			time = Long.toString((current - timestamp) / 1000) + " seconds ago";
		}
		else if(current - timestamp < 60000 * 2) {
			time = "1 minute ago";
		}
		else if(current - timestamp < 60000 * 60) {
			time = Long.toString((current - timestamp) / 60000) + " minutes ago";
		}
		else if(current - timestamp < 60000 * 60 * 2) {
			time = "1 hour ago";
		}
		else if(current - timestamp < 60000 * 60 * 24) {
			time = Long.toString((current - timestamp) / (60000 * 60)) + " hours ago";
		}
		else {
			Format ft = new SimpleDateFormat("EEE, MMM dd yyyy, HH:mm");
			time = ft.format(new Date(timestamp));
		}
		return time;
	}
	
	/**
	 * Change the timestamp this post is created.
	 * 
	 * @param t the long parameter that represents a timestamp.
	 */
	public void setTimestamp(long t) {
		timestamp = t;
	}
	
	/**
	 * Check whether the two posts are the same.
	 * 
	 * @param p the post that is used for comparison.
	 * @return whether the posts are the same.
	 */
	public boolean equals(Post p) {
		return username.equals(p.username) && timestamp == p.timestamp;
	}
	
	/**
	 * Display this post.
	 */
	public String toString() {
		String result = "Username: " + username + "\n";
		return result + getTimestamp() + "\n";
	}
	
}
