import java.util.ArrayList;

/**
 * This is a test class for testing all the other classes.
 * 
 * You can delete this test class and create your own.
 * 
 * @author xiaopei
 *
 */
public class Test {

	public static void main(String[] args) {
		ClientClass posts = new ClientClass();
		
		// test methods in Post
		System.out.println("Test p1");
		Post p1 = new Post("xiaopei");
		System.out.println(p1.getUsername());
		System.out.println(p1.getTimestamp());
		p1.setUsername("xp");
		System.out.println(p1.getUsername());
		p1.setTimestamp(System.currentTimeMillis() - 60000);
		System.out.println(p1.getTimestamp());
		posts.addPost(p1);
		Post p10 = new Post(p1);
		System.out.println(p1.equals(p10));
		posts.addPost(p10);
		
		// test methods in CommentedPost
		System.out.println();
		System.out.println("Test p2");
		CommentedPost p2 = new CommentedPost("xiaopei");
		p2.like();
		p2.like();
		System.out.println(p2.getLikes());
		p2.addComment("Whose post?");
		p2.addComment("I like it!");
		System.out.print(p2.getComments());
		p2.dislike();
		System.out.println(p2.getLikes());
		p2.deleteComment("Whose post?");
		System.out.print(p2.getComments());
		p2.setTimestamp(System.currentTimeMillis() - 23000);
		posts.addPost(p2);
		CommentedPost p20 = new CommentedPost(p2);
		System.out.println(p2.equals(p20));
		posts.addPost(p20);
		
		// test methods in EventPost
		System.out.println();
		System.out.println("Test p3");
		EventPost p3 = new EventPost("xiaopei", "meeting");
		System.out.println(p3.getEventType());
		p3.setEventType("party");
		System.out.println(p3.getEventType());
		p3.setTimestamp(System.currentTimeMillis() - 60000 * 35);
		posts.addPost(p3);
		EventPost p30 = new EventPost(p3);
		System.out.println(p3.equals(p30));
		posts.addPost(p30);
		
		// test methods in MessagePost
		System.out.println();
		System.out.println("Test p4");
		MessagePost p4 = new MessagePost("xiaopei", "House warming!");
		System.out.println(p4.getMessage());
		p4.setMessage("Party is over!");
		System.out.println(p4.getMessage());
		p4.addComment("I am attending!");
		p4.like();
		p4.setTimestamp(System.currentTimeMillis() - 60000 * 60 * 3);
		posts.addPost(p4);
		MessagePost p40 = new MessagePost(p4);
		System.out.println(p4.equals(p40));
		posts.addPost(p40);
		
		// test methods in PhotoPost
		System.out.println();
		System.out.println("Test p5");
		PhotoPost p5 = new PhotoPost("xiaopei", "summer travel", "Willis Tower");
		System.out.println(p5.getFilename());
		p5.setFilename("travel with mk");
		System.out.println(p5.getFilename());
		System.out.println(p5.getCaption());
		p5.setCaption("Sears Tower");
		System.out.println(p5.getCaption());
		p5.addComment("Beautiful scene!");
		p5.addComment("Nice weather!");
		p5.like();
		p5.setTimestamp(System.currentTimeMillis() - 60000 * 60 * 28);
		posts.addPost(p5);
		PhotoPost p50 = new PhotoPost(p5);
		System.out.println(p5.equals(p50));
		posts.addPost(p50);
		
		// test methods in ClientClass
		System.out.println();
		System.out.println("Print out all the posts below.");
		System.out.println(posts);
	}

}
