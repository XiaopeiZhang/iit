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

	public class modifyShowFrame extends JFrame {
		static JTextField jt15 = new JTextField("");//room no
		static JTextField jt16 = new JTextField("");//capacity
		static JTextField jt21 = new JTextField("");//room no
		
		static JTextField jt17 = new JTextField("");//room no
		static JTextField jt18 = new JTextField("");//showtime
		static JTextField jt19 = new JTextField("");//title
		static JTextField jt20 = new JTextField("");//mid
		static JTextField jt22 = new JTextField("");//room no
		static JTextField jt23 = new JTextField("");//showtime
		
		private JLabel jl5=new JLabel("ROOM NO.                                        "
									+ "CAPACITY");
		private JLabel jl6=new JLabel("ROOM NO.                             "
									+ "SHOWTIME(yyyy-mm-dd hh:mi:ss)                            "
									+ "MOVIE TITLE                             "
									+ "MID");
		
		public modifyShowFrame(){
			
		JFrame jf=new JFrame("modifyShow");
		jf.setLayout(null);
		Container c1=jf.getContentPane();
		jf.setBounds(10, 10, 900, 700);
		jf.setVisible(true);
		
		JButton jb6=new JButton("AddB6");
		JButton jb7=new JButton("AddB7");
		JButton jb8=new JButton("ModifyB8");
		JButton jb9=new JButton("ModifyB9");
		
		jb6.setBounds(580, 10, 100, 30);
		jb7.setBounds(580, 200, 100, 30);
		jb8.setBounds(580, 80, 100, 30);
		jb9.setBounds(580, 270, 100, 30);
		jl5.setBounds(10, 50, 900, 30);
		jl6.setBounds(10, 240, 900, 30);
		
		jt15.setBounds(10, 10, 100, 30);
		jt16.setBounds(160, 10, 100, 30);
		
		jt17.setBounds(10, 200, 100, 30);
		jt18.setBounds(160, 200, 100, 30);
		jt19.setBounds(310, 200, 100, 30);
		jt20.setBounds(460, 200, 100, 30);
		
		jt21.setBounds(10, 80, 100, 30);
		jt22.setBounds(10, 270, 100, 30);
		jt23.setBounds(160, 270, 100, 30);
		
		c1.add(jt15);
		c1.add(jt16);
		c1.add(jt17);
		c1.add(jt18);
		c1.add(jt19);
		c1.add(jt20);
		c1.add(jt21);
		c1.add(jt22);
		c1.add(jt23);
		
		c1.add(jb6);
		c1.add(jb7);
		c1.add(jb8);
		c1.add(jb9);
		c1.add(jl5);
		c1.add(jl6);
		
		jb6.addActionListener(new pressB6());
		jb7.addActionListener(new pressB7());
		jb8.addActionListener(new pressB8());
		jb9.addActionListener(new pressB9());
		//jf.setDefaultCloseOperation();
		}	
	
	
	class pressB6 implements ActionListener{//add room
		
		
		DBConnection c = new DBConnection();
		Connection conn;
		
		public void actionPerformed(ActionEvent arg0){
			try
			{
				String n1 = modifyShowFrame.jt15.getText();//room no
				String n2 = modifyShowFrame.jt16.getText();//capacity
				
				
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           ResultSet rset = stat.executeQuery("select * from room");
		           boolean flag = false;
		           
		           
		           
		           while (rset.next()) {
		            	if(n1.equals(rset.getString("room_number"))){	
		            		flag=true;
		            		
		           
		            		break;
		            	}
		            	}
		            
		         
		            if(flag==false)
		            {
		            	String query=new String();
		            	if(n2.equals(""))
		            	{
		            		query="insert into room values ("+n1+", null)";
		            	}
		            	else
		            		query="insert into room values ("+n1+", "+n2+")";
		            	
		            	stat.executeUpdate(query);
		            	

		            }
	            	
				
			}catch (SQLException e)
			{
				e.printStackTrace();
			}
			//new staffTypeIn();
		}
	}
	
	
	
	class pressB7 implements ActionListener{
		
		
		DBConnection c = new DBConnection();
		Connection conn;
		
		public void actionPerformed(ActionEvent arg0){
			try
			{
				String n1 = modifyShowFrame.jt17.getText();
				String n2 = modifyShowFrame.jt18.getText();
				String n3 = modifyShowFrame.jt19.getText();
				String n4 = modifyShowFrame.jt20.getText();
				
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           ResultSet rset = stat.executeQuery("select * from room");
		           boolean flag = false;
		          
		           while (rset.next()) {
		            	if(n1.equals(rset.getString("room_number"))){	
		            		flag=true;
		            		break;
		            	}
		            	}
		           ResultSet rset2 = stat.executeQuery("select * from movie");
		           
			          
		           while (rset2.next()) {
		            	if(n4.equals(rset2.getString("MID"))){	
		            		flag=true;	            		
		            		break;
		            	}
		            	}
		           
		           ResultSet rset1 = stat.executeQuery("select * from showing");
		           
		          
		           while (rset1.next()) {
		        	   System.out.println(rset1.getString("showtime"));
		            	if(n1.equals(rset1.getString("room_number")) && n2.equals(rset1.getString("showtime"))){	
		            		flag=false;	            		
		            		break;
		            	}
		            	}
		         
		           
		           
		            if(flag==true)
		            {
		            	String query=new String();
		            	if(n3.equals(""))
		            	{
		            		query="insert into showing values ("+n1+",to_timestamp('"+n2+"','yyyy/mm/dd hh24:mi:ss'),null,"+n4+")";
		            	}
		            	else
		            		query="insert into showing values ("+n1+",to_timestamp('"+n2+"','yyyy/mm/dd hh24:mi:ss'),'"+n3+"',"+n4+")";
		            	stat.executeUpdate(query);
		            	
		           

		            }
	            	
				
			}catch (SQLException e)
			{
				e.printStackTrace();
			}
			//new staffTypeIn();
		}
	}
	
	
	class pressB8 implements ActionListener{
		
		
		
		
		public void actionPerformed(ActionEvent arg0){
			try
			{
				DBConnection c = new DBConnection();
				Connection conn;
				String n1 = modifyShowFrame.jt21.getText();//room no
				
				
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           ResultSet rset = stat.executeQuery("select * from room");
		           boolean flag=false;
		           
		           
		           
		           while (rset.next()) {
		            	if(n1.equals(rset.getString("room_number"))){	
		            		flag=true;
		            		
		            		break;
		            	}
		            	}
		           
		           System.out.println(flag+","+n1);
		           if(flag==true)
		        	   new modifyRoomFrame(n1);
	
	            	
				
			}catch (SQLException e)
			{
				e.printStackTrace();
			}
			//new staffTypeIn();
		}
	}
	
	
	class pressB9 implements ActionListener{
		
		
		DBConnection c = new DBConnection();
		Connection conn;
		
		public void actionPerformed(ActionEvent arg0){
			try
			{
				String n1 = modifyShowFrame.jt22.getText();//room no
				String n2 = modifyShowFrame.jt23.getText();
				boolean flag=false;
				
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           ResultSet rset = stat.executeQuery("select * from showing");

		           while (rset.next()) {
		        	   System.out.println(rset.getString("room_number")+","+rset.getString("showtime"));
		            	if(n1.equals(rset.getString("room_number"))&&n2.equals(rset.getString("showtime"))){	
		            		flag=true;
		            		break;
		            	}
		            	}
		           System.out.println("input"+n1+","+n2+" "+flag);
		           if(flag==true)
		        	   new modifyShowingFrame(n1, n2);

	            	
				
			}catch (SQLException e)
			{
				e.printStackTrace();
			}
			//new staffTypeIn();
		}
	}
	
	}