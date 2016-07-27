import java.awt.Graphics;
import java.awt.Color;

/**
 * This is a tortoise racer class to draw a tortoise.
 * 
 * Thanks to CS445 course for code to build upon.
 * 
 * @author xiaopei
 *
 */
public class TortoiseRacer extends Animal implements Movable {

	public TortoiseRacer() {
		super();
	}

	public TortoiseRacer(String rID, int rX, int rY) {
		super(rID, rX, rY);
	}
	
	/**
	 * Draw a tortoise with color depending on its X position.
	 * Draw a walking ground right below the tortoise.
	 * Display a string moving with the tortoise below the walking ground.
	 * 
	 * @param g the graph to display.
	 */
	public void draw(Graphics g) {
		int startX = getX();
		int startY = getY();
		g.drawString("Tortoise or Chameleon?", startX, startY + 50);
		g.drawLine(0, 65, 200, 65);
		g.setColor(new Color((24 + startX * 10) % 255, (129 + startX * 10) % 255, (24 + startX * 10) % 255));	// dark green
		// body
		g.fillOval(startX, startY, 25, 15);
		// head
		g.fillOval(startX + 20, startY + 5, 15, 10);
		// flatten bottom
		g.clearRect(startX, startY + 11, 35, 4);
		// feet
		g.setColor(new Color(102, 51, 0));	// brown
		g.fillOval(startX + 3, startY + 10, 5, 5);
		g.fillOval(startX + 17, startY + 10, 5, 5);
	}
	
	public void move() {
		setX(getX() + SLOW);
	}
	
}
