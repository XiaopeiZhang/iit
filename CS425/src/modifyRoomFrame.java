import java.awt.Container;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;


public class modifyRoomFrame extends JFrame{
	
	static JTextField jt16 = new JTextField("");//capacity
	static String roomnum = null;
	private JLabel jl5=new JLabel("                                        "
			+ "CAPACITY");
	

	public modifyRoomFrame(String rnum)
	{
		JFrame jf=new JFrame("modifyRoom   Room Number: "+rnum);
		jf.setLayout(null);
		Container c1=jf.getContentPane();
		jf.setBounds(10, 10, 900, 700);
		jf.setVisible(true);
		JButton jb8=new JButton("ModifyB10");
		jb8.setBounds(580, 50, 100, 30);
		jt16.setBounds(160, 10, 100, 30);
		jl5.setBounds(10, 50, 900, 30);
		roomnum=rnum;
		
		c1.add(jt16);
		c1.add(jb8);
		c1.add(jl5);
		
		jb8.addActionListener(new pressB10());
		
		
	}
	
class pressB10 implements ActionListener{
		
		
		DBConnection c = new DBConnection();
		Connection conn;
		
		public void actionPerformed(ActionEvent arg0){
			try
			{
				String n1 = modifyRoomFrame.jt16.getText();//cap
				String rnum = roomnum;
				System.out.println(n1+"input,"+rnum);
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           
		   		String query="update room set capacity="+n1+" where room_number="+rnum;
		   		stat.executeUpdate(query);
	            	
				
			}catch (SQLException e)
			{
				e.printStackTrace();
			}
			//new staffTypeIn();
		}
	}
	
}
