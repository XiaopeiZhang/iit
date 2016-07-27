import java.text.DateFormat;
import java.util.ArrayList;
import java.util.Date;

/**
 * This is a simulation of a post with coomments and likes.
 * 
 * @author xiaopei
 *
 */
public class CommentedPost extends Post {

	private int likes;
	private ArrayList<String> comments;
	
	/**
	 * Class constructor specifying user who posts.
	 * 
	 * @param postname the string that represents username.
	 */
	public CommentedPost(String postname) {
		super(postname);
		likes = 0;
		comments = new ArrayList<String>();
	}
	
	/**
	 * A copy constructor.
	 * 
	 * @param another the post that is being copied.
	 */
	public CommentedPost(CommentedPost another) {
		super(another);
		likes = another.likes;
		comments = another.comments;
	}
	
	/**
	 * Get the number of likes this post has.
	 * 
	 * @return the integer that represents the number of likes.
	 */
	public int getLikes() {
		return likes;
	}
	
	/**
	 * Add 1 to the number of likes.
	 */
	public void like() {
		likes++;
	}
	
	/**
	 * Deduct 1 from the number of likes.
	 */
	public void dislike() {
		likes--;
	}
	
	/**
	 * Get all the comments of this post.
	 * 
	 * @return the string of all the comments.
	 */
	public String getComments() {
		String allComments = "";
		for(String comment: comments) {
			allComments += comment + "\n";
		}
		return allComments;
	}
	
	/**
	 * Add a comment to the post.
	 * 
	 * @param comment the string represents the comment to be added.
	 */
	public void addComment(String comment) {
		comments.add(comment);
	}
	
	/**
	 * Delete a comment from the post.
	 * 
	 * @param comment the string represents the comment to be deleted.
	 */
	public void deleteComment(String comment) {
		comments.remove(comment);
	}
	
	/**
	 * Check whether the two posts are the same.
	 * 
	 * @param p the post that is used for comparison.
	 * @return whether the posts are the same.
	 */
	public boolean equals(CommentedPost p) {
		boolean sameComments = true;
		for(int i = 0; i < comments.size(); i++) {
			if(!comments.get(i).equals(p.comments.get(i))) {
				return false;
			}
		}
		return super.equals(p) && likes == p.likes && sameComments;
	}
	
	/**
	 * Display this post.
	 */
	public String toString() {
		return super.toString() + Integer.toString(likes) + " likes\nComments: " + getComments();
	}

}
