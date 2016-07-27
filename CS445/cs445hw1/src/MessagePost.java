import java.text.DateFormat;
import java.util.Date;

/**
 * This is a simulation of a commented post with a message.
 * 
 * @author xiaopei
 *
 */
public class MessagePost extends CommentedPost {

	private String message;
	
	/**
	 * Class constructor specifying user who posts and the message.
	 * 
	 * @param postname the string of username.
	 * @param postMessage the string of message.
	 */
	public MessagePost(String postname, String postMessage) {
		super(postname);
		message = postMessage;
	}
	
	/**
	 * A copy constructor.
	 * 
	 * @param another the post that is being copied.
	 */
	public MessagePost(MessagePost another) {
		super(another);
		message = another.message;
	}
	
	/**
	 * Get the message of this post.
	 * 
	 * @return the string of the message.
	 */
	public String getMessage() {
		return message;
	}
	
	/**
	 * Set the new message.
	 * 
	 * @param postMessage the string of the new message.
	 */
	public void setMessage(String postMessage) {
		message = postMessage;
	}
	
	/**
	 * Check whether the two posts are the same.
	 * 
	 * @param p the post that is used for comparison.
	 * @return whether the posts are the same.
	 */
	public boolean equals(MessagePost p) {
		return super.equals(p) && message.equals(p.message);
	}
	
	/**
	 * Display this post.
	 */
	public String toString() {
		return super.toString() + "Message: " + message + "\n";
	}

}
