import java.text.DateFormat;
import java.util.Date;

/**
 * This is a simulation of a commented post with a photo.
 * 
 * @author xiaopei
 *
 */
public class PhotoPost extends CommentedPost {
	
	private String filename;
	private String caption;

	/**
	 * Class constructor specifying user who posts, the name of photo and the caption of photo.
	 * 
	 * @param postname the string of username.
	 * @param photoName the strong of photo name.
	 * @param photoCaption the string of photo caption.
	 */
	public PhotoPost(String postname, String photoName, String photoCaption) {
		super(postname);
		filename = photoName;
		caption = photoCaption;
	}
	
	/**
	 * A copy constructor.
	 * 
	 * @param another the post that is being copied.
	 */
	public PhotoPost(PhotoPost another) {
		super(another);
		filename = another.filename;
		caption = another.caption;
	}
	
	/**
	 * Get the file name of this post.
	 * 
	 * @return the string of the file name.
	 */
	public String getFilename() {
		return filename;
	}
	
	/**
	 * Set the file name of this post.
	 * 
	 * @param fn the string of the new file name.
	 */
	public void setFilename(String fn) {
		filename = fn;
	}
	
	/**
	 * Get the caption of this post.
	 * 
	 * @return the string of the caption.
	 */
	public String getCaption() {
		return caption;
	}
	
	/**
	 * Set the caption of this post.
	 * 
	 * @param cap the string of the new caption.
	 */
	public void setCaption(String cap) {
		caption = cap;
	}
	
	/**
	 * Check whether the two posts are the same.
	 * 
	 * @param p the post that is used for comparison.
	 * @return whether the posts are the same.
	 */
	public boolean equals(PhotoPost p) {
		return super.equals(p) && filename.equals(p.filename) && caption.equals(p.caption);
	}
	
	/**
	 * Display this post.
	 */
	public String toString() {
		return super.toString() + "Filename: " + filename + "\nCaption: " + caption + "\n";
	}

}
