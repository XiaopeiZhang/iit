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

	public class modifyMovieFrame extends JFrame {
		
		
		
		static JTextField jt15 = new JTextField("");
		static JTextField jt16 = new JTextField("");
		static JTextField jt17 = new JTextField("");
		static JTextField jt18 = new JTextField("");
		static JTextField jt19 = new JTextField("");
		
		private JLabel jl4=new JLabel( "TITLE                                  "
									 + "RELEASE YEAR                           "
									 + "LENGTH                                 "
									 + "PG RATING");
		
		public modifyMovieFrame(String id){
			
		JFrame jf=new JFrame("modifyMovie "+id);
		jf.setLayout(null);
		Container c1=jf.getContentPane();
		jf.setBounds(10, 10, 900, 700);
		jf.setVisible(true);
		jt19 = new JTextField(id);
		
		JButton jb6=new JButton("OKB6");
		
		jb6.setBounds(580, 10, 100, 30);
		jl4.setBounds(10, 50, 900, 30);
		

		
		jt15.setBounds(10, 10, 100, 30);
		jt16.setBounds(160, 10, 100, 30);
		jt17.setBounds(310, 10, 100, 30);
		jt18.setBounds(460, 10, 100, 30);
		
		c1.add(jt15);
		c1.add(jt16);
		c1.add(jt17);
		c1.add(jt18);
		c1.add(jb6);
		c1.add(jl4);
		
		jb6.addActionListener(new pressB6());
		
		//jf.setDefaultCloseOperation();
		}	
	
	
	class pressB6 implements ActionListener{
		
		
		DBConnection c = new DBConnection();
		Connection conn;

		
		public void actionPerformed(ActionEvent arg0){
			try
			{
					String n1 = modifyMovieFrame.jt15.getText();//title
					String n2 = modifyMovieFrame.jt16.getText();//year
					String n3 = modifyMovieFrame.jt17.getText();//length
					String n4 = modifyMovieFrame.jt18.getText();//rating
					String mid = modifyMovieFrame.jt19.getText();

				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           ResultSet rset = stat.executeQuery("select * from movie");
		           boolean flag = false;
		           String ntitle = new String();
		           String nyear = new String();
		           String nlength = new String();
		           String npg = new String();
		           boolean check1=false;
		           boolean check2=false;
		           boolean check3=false;
		           boolean check4=false;
		           while (rset.next()) {
		            	if(mid.equals(rset.getString("MID"))){	
		            		flag=true;
		            		
		            		if(!n1.equals("")){
		            			ntitle=n1;
		            			check1=true;
		            		}
		            		
		            		if(!n2.equals("")){
		            			nyear=n2;
			            		check2=true;
		            		}
			            		
		            		
		            		if(!n3.equals("")){
		            			nlength=n3;
		            			check3=true;
		            		}
		            		
		            		if(!n4.equals("")){
		            			npg=n4;
		            			check4=true;
		            		}
		            		
		            		break;
		            	}
		            	}
		            
		            if(flag==true)
		            {
		            	if(check1==true)
		            	{
		            		String query="update movie set title='"+ntitle+"' where MID="+mid;
		            		stat.executeUpdate(query);
		            	}
		            	
		            	if(check2==true)
		            	{
		            		String query="update movie set release_year="+nyear+" where MID="+mid;
		            		stat.executeUpdate(query);
		            	}
		            	
		            	if(check3==true)
		            	{
		            		String query="update movie set length="+nlength+" where MID="+mid;
		            		stat.executeUpdate(query);
		            	}
		            	
		            	if(check4==true)
		            	{
		            		String query="update movie set pg_rating='"+npg+"' where MID="+mid;
		            		stat.executeUpdate(query);
		            	}
		            }

	            	
		            
	            		
	            	
				
			}catch (SQLException e)
			{
				e.printStackTrace();
			}
			//new staffTypeIn();
		}
	}
	}