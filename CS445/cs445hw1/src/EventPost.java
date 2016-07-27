import java.text.DateFormat;
import java.util.Date;

/**
 * This is a simulation of an event post.
 * 
 * @author xiaopei
 *
 */
public class EventPost extends Post {

	private String eventType;
	
	/**
	 * Class constructor specifying user who posts and the type of the event.
	 * 
	 * @param postname the string of username.
	 * @param type the string of event type.
	 */
	public EventPost(String postname, String type) {
		super(postname);
		eventType = type;
	}
	
	/**
	 * A copy constructor.
	 * 
	 * @param another the post that is being copied.
	 */
	public EventPost(EventPost another) {
		super(another);
		eventType = another.eventType;
	}
	
	/**
	 * Get the event type.
	 * 
	 * @return the string of event type.
	 */
	public String getEventType() {
		return eventType;
	}
	
	/**
	 * Set the event type.
	 * 
	 * @param et the string of new event type.
	 */
	public void setEventType(String et) {
		eventType = et;
	}
	
	/**
	 * Check whether the two posts are the same.
	 * 
	 * @param p the post that is used for comparison.
	 * @return whether the posts are the same.
	 */
	public boolean equals(EventPost p) {
		return super.equals(p) && eventType.equals(p.eventType);
	}
	
	/**
	 * Display this post.
	 */
	public String toString() {
		return super.toString() + "Event Type: " + eventType + "\n";
	}

}
