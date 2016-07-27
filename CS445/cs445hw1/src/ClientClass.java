import java.util.ArrayList;

/**
 * This is a simulation of a collection of posts.
 * 
 * @author xiaopei
 *
 */
public class ClientClass {
	
	ArrayList<Post> posts;
	
	/**
	 * Class constructor.
	 */
	public ClientClass() {
		posts = new ArrayList<Post>();
	}
	
	/**
	 * Add a post.
	 * 
	 * @param p the post to be added.
	 */
	public void addPost(Post p) {
		posts.add(p);
	}
	
	/**
	 * Display all the posts.
	 */
	public String toString() {
		String result = "";
		for(Post p:posts) {
			result += p.toString() + "\n";
		}
		return result;
	}

}
