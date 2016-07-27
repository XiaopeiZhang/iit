import java.awt.Graphics;
import javax.swing.JApplet;
import java.applet.AudioClip;

/**
 * This is an JApplet to simulate a color-changing tortoise with
 * a walking ground, a background sound effect and a question to 
 * viewers.
 * 
 * Oh yeah, I know this looks and sounds weird.
 * 
 * Thanks to creeper-ciller78 for this free background sound.
 * 
 * Thanks to CS445 course for code to build upon.
 * 
 * @author xiaopei
 *
 */
public class TortoiseRacerClient extends JApplet {

	private TortoiseRacer t;
	
	/**
	 * Initialize with a tortoise racer and a background sound.
	 */
	public void init() {
		t = new TortoiseRacer("Tortoise", 1, 50);
		// add background sound effects
		AudioClip sound = getAudioClip(getDocumentBase(), "346895__creeper-ciller78__electronic-loop-1.wav");
		sound.play();
	}
	
	/**
	 * Paints a tortoise moving from left to right with
	 * 0.3 second delay.
	 * 
	 * @param g the graph to display.
	 */
	public void paint(Graphics g) {
		for(int i = 0; i < getWidth(); i++) {
			t.move();
			t.draw(g);
			
			try {
				Thread.sleep(300);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			
			g.clearRect(0, 0, getWidth(), getHeight());
		}
	}

}
