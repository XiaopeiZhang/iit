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

	public class modifyPersonFrame extends JFrame {
		static JTextField jt15 = new JTextField("");
		static JTextField jt16 = new JTextField("");
		static JTextField jt17 = new JTextField("");
		static JTextField jt18 = new JTextField("");
		
		private JLabel jl5=new JLabel("NAME                                        "
									+ "DATE OF BIRTH(yyyymmdd)                       "
									+ "GENDER");
		
		public modifyPersonFrame(String id){
			
		JFrame jf=new JFrame("modifyPerson "+id);
		jf.setLayout(null);
		Container c1=jf.getContentPane();
		jf.setBounds(10, 10, 900, 700);
		jf.setVisible(true);
		jt18 = new JTextField(id);
		
		JButton jb6=new JButton("OKB6");
		
		jb6.setBounds(580, 10, 100, 30);
		jl5.setBounds(10, 50, 900, 30);

		
		jt15.setBounds(10, 10, 100, 30);
		jt16.setBounds(160, 10, 100, 30);
		jt17.setBounds(310, 10, 100, 30);
		
		
		c1.add(jt15);
		c1.add(jt16);
		c1.add(jt17);
		c1.add(jb6);
		c1.add(jl5);
		
		jb6.addActionListener(new pressB6());
		
		//jf.setDefaultCloseOperation();
		}	
	
	
	class pressB6 implements ActionListener{
		
		
		DBConnection c = new DBConnection();
		Connection conn;
		
		public void actionPerformed(ActionEvent arg0){
			try
			{
				String n1 = modifyPersonFrame.jt15.getText();//name
				String n2 = modifyPersonFrame.jt16.getText();//dob
				String n3 = modifyPersonFrame.jt17.getText();//gender
				String pid = modifyPersonFrame.jt18.getText();
				
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           ResultSet rset = stat.executeQuery("select * from person");
		           boolean flag = false;
		           String nname = new String();
		           String ndob = new String();
		           String ngender = new String();
		           boolean check1=false;
		           boolean check2=false;
		           boolean check3=false;
		           while (rset.next()) {
		            	if(pid.equals(rset.getString("PID"))){	
		            		flag=true;
		            		
		            		if(!n1.equals("")){
		            			nname=n1;
		            			check1=true;
		            		}
		            		
		            		if(!n2.equals("")){
		            			ndob=n2;
			            		check2=true;
		            		}
			            		
		            		
		            		if(!n3.equals("")){
		            			ngender=n3;
		            			check3=true;
		            		}
		            		
		            		
		            		break;
		            	}
		            	}
		            
		         
		            if(flag==true)
		            {
		            	
		            	if(check1==true)
		            	{
		            		String query="update person set name='"+nname+"' where PID="+pid;
		            		stat.executeUpdate(query);
		            	}
		            	
		            	if(check2==true)
		            	{
		            		String query="update person set date_of_birth=to_date('"+ndob+"','yyyymmdd') where PID="+pid;
		            		stat.executeUpdate(query);
		            	}
		            	
		            	if(check3==true)
		            	{
		            		String query="update person set gender='"+ngender+"' where PID="+pid;
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