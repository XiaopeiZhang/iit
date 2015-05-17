import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.*;
import javax.swing.*;




public class memberTypeIn extends JFrame {
	
	//public static void main(String args[]){
	//	new memberTypeIn();
	//}
	
	static JTextField jt = new JTextField("",20);
	public memberTypeIn(){
		setTitle("member");
		JLabel jl = new JLabel("type in your ID",JLabel.CENTER);
		jl.setHorizontalAlignment(SwingConstants.CENTER);
		setLayout(null);
		setBounds(500,300,230,150);
		Container c = getContentPane();
		JButton b1=new JButton("Login");
		JButton b2=new JButton("Cancel");
		b1.setBounds(10, 60, 90, 30);
		b2.setBounds(110, 60, 90, 30);
		b1.addActionListener(new pressB1());
		b2.addActionListener(new pressB2());
		c.add(b1);
		c.add(b2);
		c.add(jl);
		c.add(jt);
		jl.setOpaque(true);
		jl.setSize(210, 50);
		jt.setBounds(55, 35, 100, 20);
		setVisible(true);
		setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
	}
	
	
	class pressB1 implements ActionListener{
		
		DBConnection c = new DBConnection();
		Connection conn;
		boolean flag=false;
		public void actionPerformed(ActionEvent arg0){
			try
			{
				   String id=memberTypeIn.jt.getText();// read input
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           ResultSet rset = stat.executeQuery("select * from member");
		            while (rset.next()) {
		            	if(id.equals(rset.getString("SID"))){
		            		//rset.
		            		flag=true;
		            		//System.out.println("duil");
		            		dispose();
		            		new memberFrame();
		            		break;
		            	}
		            	}
	            	if(flag==false){
	            		incorrectMsg i=new incorrectMsg();
	            		i.incorrectID2();
	            		dispose();
	            	}
				
			}catch (SQLException e)
			{
				e.printStackTrace();
			}
			//new staffTypeIn();
		}
	}
	class pressB2 implements ActionListener{
		public void actionPerformed(ActionEvent arg0){

				dispose();
				new LoginFrame();
		
		}
	}
}
