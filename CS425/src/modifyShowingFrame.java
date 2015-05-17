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


public class modifyShowingFrame extends JFrame{
	
	static JTextField jt19 = new JTextField("");//title
	static JTextField jt20 = new JTextField("");//mid
	static String roomnum = null;
	static String stime = null;
	private JLabel jl6=new JLabel("                                         "
			+ "                                 "
			+ "MOVIE TITLE                             "
			+ "MID");
	

	public modifyShowingFrame(String rnum, String time)
	{
		JFrame jf=new JFrame("modifyShowing   Room Number: "+rnum+" Showtime: "+time);
		jf.setLayout(null);
		Container c1=jf.getContentPane();
		jf.setBounds(10, 10, 900, 700);
		jf.setVisible(true);
		JButton jb11=new JButton("ModifyB11");
		
		jb11.setBounds(580, 140, 100, 30);
		jt19.setBounds(310, 100, 100, 30);
		jt20.setBounds(460, 100, 100, 30);
		jl6.setBounds(10, 140, 900, 30);
		roomnum=rnum;
		stime=time;
		
		c1.add(jt19);
		c1.add(jt20);
		c1.add(jb11);
		c1.add(jl6);
		
		jb11.addActionListener(new pressB11());
		
		
	}
	
class pressB11 implements ActionListener{
		
		
		DBConnection c = new DBConnection();
		Connection conn;
		
		public void actionPerformed(ActionEvent arg0){
			try
			{
				String n1 = modifyShowingFrame.jt19.getText();
				String n2 = modifyShowingFrame.jt20.getText();
				String rnum = roomnum;
				String time = stime;
				
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           ResultSet rset = stat.executeQuery("select * from movie");
		           boolean flag=false;
		           while(rset.next())
		           {
		        	   if(n2.equals(rset.getString("MID")))
		        	   {
		        		   	flag=true;
		        		   	break;
		        	   }
		        		   
		           }
		           
		         if(!n1.equals("")){
			   		String query="update showing set movie_title="+n1+" where room_number="+rnum+" and showtime=to_timestamp('"+time+"','yyyy/mm/dd hh24:mi:ss')";
			   		stat.executeUpdate(query);
		         }
		         
		         if(!n2.equals("")&&flag==true){
				   		String query="update showing set MID="+n2+" where room_number="+rnum+" and showtime=to_timestamp('"+time+"','yyyy/mm/dd hh24:mi:ss')";
				   		stat.executeUpdate(query);
				         }
	            	
				
			}catch (SQLException e)
			{
				e.printStackTrace();
			}
			//new staffTypeIn();
		}
	}
	
}
