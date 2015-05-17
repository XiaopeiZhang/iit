import java.awt.*;

import javax.swing.*;


public class buyTicketFrame {

	public buyTicketFrame(String ticketinfo)
	{
		JFrame jf=new JFrame();
		Container c=jf.getContentPane();
		jf.setLayout(null);
		
		jf.setBounds(10, 10, 900, 700);
		JButton jb1=new JButton("BUY");
		System.out.println(ticketinfo+"\nPlease type in your ID number again ");
		JLabel jl1=new JLabel(ticketinfo+"\nPlease type in your ID number again ");
		JTextField jt1=new JTextField("");
		
		jb1.setBounds(10, 10, 100, 30);
		jl1.setBounds(10, 70, 500, 200);
		jt1.setBounds(200, 10, 100, 30);
		
		c.add(jl1);
		c.add(jb1);
		c.add(jt1);
		jf.setVisible(true);
	}
}
