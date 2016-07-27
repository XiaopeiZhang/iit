import java.awt.Graphics;

/**
 * Code from CS445 course.
 */

public abstract class Animal {
	private String ID;
	private int x;
	private int y;
	
	public Animal() {
		ID = "";
	}
	
	public Animal(String rID, int rX, int rY) {
		ID = rID;
		x = rX;
		y = rY;
	}
	
	public String getID() {
		return ID;
	}
	
	public int getX() {
		return x;
	}
	
	public int getY() {
		return y;
	}
	
	public void setX(int newX) {
		x = newX;
	}
	
	public void setY(int newY) {
		y = newY;
	}
	
	public abstract void draw(Graphics g);
}
