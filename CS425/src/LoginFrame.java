import java.awt.Container;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.SwingConstants;
import javax.swing.WindowConstants;


public class LoginFrame extends JFrame {
	public LoginFrame(){
		setTitle("movieSystem");
		JLabel jl = new JLabel("choose your identity",JLabel.CENTER);
		jl.setHorizontalAlignment(SwingConstants.CENTER);
		setLayout(null);
		setBounds(500,300,230,150);
		Container c = getContentPane();
		JButton b1=new JButton("staff");
		JButton b2=new JButton("member");
		b1.setBounds(10, 60, 90, 30);
		b2.setBounds(110, 60, 90, 30);
		b1.addActionListener(new pressB1());
		b2.addActionListener(new pressB2());
		c.add(b1);
		c.add(b2);
		c.add(jl);
		jl.setOpaque(true);
		jl.setSize(210, 50);
		setVisible(true);
		setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
	}
	
	class pressB1 implements ActionListener{
		public void actionPerformed(ActionEvent arg0){
			dispose();
			new staffTypeIn();
		}
	}
	class pressB2 implements ActionListener{
		public void actionPerformed(ActionEvent arg0){
			dispose();
			new memberTypeIn();
		}
	}
	
}
