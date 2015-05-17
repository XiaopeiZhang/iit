
import java.awt.Container;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.WindowConstants;


public class incorrectMsg extends JFrame  {
	
	//public static void main(String args[]){
	//	memberFrame mF=new memberFrame();
	//	mF.incorrectID();
	//}
	
	public void incorrectID() {
			JLabel jl = new JLabel("incorrect ID");
			setTitle("incorrectPassword");
			setLayout(null);
			setBounds(500,300,300,100);
			Container c = getContentPane();
			jl.setBounds(30, 20, 100, 20);
			c.add(jl);
			setVisible(true);
			setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
			JButton b1=new JButton("Return");
			b1.setBounds(10, 60, 90, 30);
			c.add(b1);
			b1.addActionListener(new pressB1());
			//dispose();
		}
	
	public void incorrectID2(){
		JLabel jl = new JLabel("incorrect ID");
		setTitle("incorrectPassword");
		setLayout(null);
		setBounds(500,300,300,100);
		Container c = getContentPane();
		jl.setBounds(30, 20, 100, 20);
		c.add(jl);
		setVisible(true);
		setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
		JButton b1=new JButton("Return");
		b1.setBounds(10, 60, 90, 30);
		c.add(b1);
		b1.addActionListener(new pressB2());
		//dispose();
	}
	class pressB1 implements ActionListener{
		public void actionPerformed(ActionEvent arg0){
			dispose();
			dispose();
			new staffTypeIn();
		}
	}
	class pressB2 implements ActionListener{
		public void actionPerformed(ActionEvent arg0){
			dispose();
			dispose();
			new memberTypeIn();
		}
	}

}
