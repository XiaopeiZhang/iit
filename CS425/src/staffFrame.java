import java.awt.BorderLayout;
import java.awt.Container;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Scanner;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.ListSelectionModel;
import javax.swing.SwingConstants;
import javax.swing.WindowConstants;
import javax.swing.table.DefaultTableModel;




public class staffFrame extends JFrame {
	
	//public static void main(String args[]){
	//	new staffFrame();
	//}
	static String[][] allmovieinfo= null;
	static String[][] allshowinfo = null;
	private JButton b1=new JButton("searchMovieB1");
	private JButton b2=new JButton("checkShowsB2");
	private JButton b3=new JButton("AddB3");
	private JButton b4=new JButton("DeleteB4");
	private JButton b5=new JButton("ModifyB5");
	private JButton b6=new JButton("modifyShowsB6");
	
	static JTextField jt1 = new JTextField("");
	static JTextField jt2 = new JTextField("");
	static JTextField jt3 = new JTextField("");
	static JTextField jt4 = new JTextField("");
	static JTextField jt5 = new JTextField("");
	
	static JTextField jt6 = new JTextField("");
	
	static JTextField jt7 = new JTextField("");
	static JTextField jt8 = new JTextField("");
	
	static JTextField jt9 = new JTextField("");
	static JTextField jt10 = new JTextField("");
	static JTextField jt11 = new JTextField("");
	static JTextField jt12 = new JTextField("");
	
	static JTextField jt13 = new JTextField("");
	static JTextField jt14 = new JTextField("");
	
	static JTextField jt15 = new JTextField("");
	static JTextField jt16 = new JTextField("");	
	static JTextField jt17 = new JTextField("");
	
	static JTextField jt18 = new JTextField("");
	static JTextField jt19 = new JTextField("");
	
	
	private JLabel jl1=new JLabel("TITLE                  "
			+ "              GENRE                   "
			+ "        ACTOR              "
			+ "           DIRECTOR               "
			+ "        WRITER");
	private JLabel jl2=new JLabel("MID                                         "
								+ "PID                                                                            "
								+ "MID                                         "
								+ "PID");
	private JLabel jl3=new JLabel("MID");
	
	private JLabel jl4=new JLabel("MID                                         "
								+ "TITLE                     "
								+ "RELEASE YEAR              "
								+ "LENGTH                    "
								+ "PG RATING");
	private JLabel jl5=new JLabel("PID                                "
								+ "NAME                               "
								+ "DATE OF BIRTH(yyyymmdd)               "
								+ "GENDER");
	
	//JTable jtb1=new JTable();
	//JTable jtb2=new JTable();
	//JScrollPane scrollPane2 = new JScrollPane(jtb2);
	//JPanel panel = new JPanel();
	
	
	public staffFrame(){
		
		JFrame jf = new JFrame();
		Container c = jf.getContentPane();		
		jf.setTitle("staffFrame");
		c.setLayout(null);
				
		jf.setBounds(100,20,900,700);
		
		b1.setBounds(700, 30, 150, 40);
		b2.setBounds(700, 200, 150, 40);
		b3.setBounds(700, 500, 150, 40);
		b4.setBounds(200, 350, 150, 40);
		b5.setBounds(400, 350, 150, 40);
		b6.setBounds(700, 250, 150, 40);
		
		
		
		jt1.setBounds(100, 30, 100, 30);
		jt2.setBounds(220, 30, 100, 30);
		jt3.setBounds(340, 30, 100, 30);
		jt4.setBounds(460, 30, 100, 30);
		jt5.setBounds(580, 30, 100, 30);
		
		jt6.setBounds(400, 200, 100, 30);
		
		jt7.setBounds(100, 400, 100, 30);
		jt8.setBounds(220, 400, 100, 30);
		
		jt9.setBounds(100, 500, 100, 30);
		jt10.setBounds(220, 500, 100, 30);
		jt11.setBounds(100, 600, 100, 30);
		jt12.setBounds(220, 600, 100, 30);
		
		jt13.setBounds(460, 400, 100, 30);
		jt14.setBounds(580, 400, 100, 30);
		
		jt15.setBounds(340, 500, 100, 30);
		jt16.setBounds(460, 500, 100, 30);		
		jt17.setBounds(580, 500, 100, 30);
		
		jt18.setBounds(340, 600, 100, 30);
		jt19.setBounds(460, 600, 100, 30);
		
		
		
		jl1.setBounds(140, 30, 20000, 100);
		jl2.setBounds(100, 450, 900, 40);
		jl3.setBounds(370, 200, 150, 40);
		
		jl4.setBounds(100, 550, 900, 30);
		jl5.setBounds(100, 650, 900, 30);
		
		b1.addActionListener(new pressB1());
		b2.addActionListener(new pressB2());
		b3.addActionListener(new pressB3());
		b4.addActionListener(new pressB4());
		b5.addActionListener(new pressB5());
		b6.addActionListener(new pressB6());
		
		c.add(b1);
		c.add(b2);
		c.add(b3);
		c.add(b4);
		c.add(b5);
		c.add(b6);
		
		c.add(jt1);
		c.add(jt2);
		c.add(jt3);
		c.add(jt4);
		c.add(jt5);
		c.add(jt6);//title
		c.add(jt7);//delete1
		c.add(jt8);//delete2
		
		c.add(jt9);//add1
		c.add(jt10);//add2
		c.add(jt11);//add3
		c.add(jt12);//add4
		
		c.add(jt13);//modify1
		c.add(jt14);//modify2
		
		c.add(jt15);//add year
		c.add(jt16);//add length
		c.add(jt17);//add rating
		c.add(jt18);//add dob
		c.add(jt19);//add gender
		
		c.add(jl1);
		c.add(jl2);
		c.add(jl3);
		c.add(jl4);
		c.add(jl5);

		jf.setVisible(true);
		jf.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
	}
	
	class pressB1 implements ActionListener{//search click
		
		//DBConnection c = new DBConnection();
		//Connection conn;
		//boolean flag=false;
		
		public void actionPerformed(ActionEvent arg0){
			try
			{
					DBConnection c = new DBConnection();
					Connection conn;
					boolean flag=false;
				
				   String input1=staffFrame.jt1.getText().toLowerCase();// read input
				   String input2=staffFrame.jt2.getText().toLowerCase();// read input
				   String input3=staffFrame.jt3.getText().toLowerCase();// read input
				   String input4=staffFrame.jt4.getText().toLowerCase();// read input
				   String input5=staffFrame.jt5.getText().toLowerCase();// read input
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           ArrayList<Integer> mal = new ArrayList<Integer>();
		           
		           if(!input1.equals("")||!input2.equals("")||!input3.equals("")||!input4.equals("")||!input5.equals("")){
		        	   
		        	   
		        	   if(!input1.equals("")||!input2.equals("")){//only search movie and genre
		        		   ResultSet rset1 = stat.executeQuery("select * from movie left outer join genre using (MID)");
		            while (rset1.next()) {
		            	String wholeTitle = rset1.getString("title");
		            	String genre = rset1.getString("genre");
		            	
		            	if(!input1.equals("")){//compare title
		            	Scanner scan = new Scanner(input1);
		            	while(scan.hasNext()){
		            		String partialInput = scan.next();

		            	if(wholeTitle.toLowerCase().contains(partialInput)){
		            		System.out.println(wholeTitle);
		            		
		            		int mid = rset1.getInt("MID");
		            		boolean check1 = false;
		            		for(Integer m: mal)
		            		{
		            			if(mid == m)
		            			{
		            				check1 = true;
		            				break;
		            			}
		            		}
		            		if(check1==false)
		            		{
		            			mal.add(mid);
		            			flag=true;
		            		}

		            	}
		            	
		            	}
		            }//end compare title
		            	
		            if(!input2.equals(""))//compare genre
		            {
		             	if(genre.toLowerCase().contains(input2)){
		            		System.out.println(genre);
		            		
		            		int mid = rset1.getInt("MID");
		            		boolean check2 = false;
		            		for(Integer m: mal)
		            		{
		            			if(mid == m)
		            			{
		            				check2 = true;
		            				break;
		            			}
		            		}
		            		if(check2==false)
		            		{
		            			mal.add(mid);
		            			flag=true;
		            		}
		            		
		            	}
		            }//end compare genre

		            }
		           }//end search
		        	   
		           if(!input3.equals("")||!input4.equals("")||!input5.equals(""))//only search person and occupation
		           { 	
			            	if(!input3.equals(""))//compare actor
			            	{
			            		ResultSet rset2 = stat.executeQuery("select * from person join act using (PID)");
			            		while (rset2.next()) {
					            	String pname = rset2.getString("name");
			            		if(pname.toLowerCase().contains(input3))
			            		{
			            			System.out.println(pname);
				            		
				            		int mid = rset2.getInt("MID");
				            		boolean check3 = false;
				            		for(Integer m: mal)
				            		{
				            			if(mid == m)
				            			{
				            				check3 = true;
				            				break;
				            			}
				            		}
				            		if(check3==false)
				            		{
				            			mal.add(mid);
				            			flag=true;
				            		}
			            		}
			            	}
			            }//end  if rset2
			            
			            
			            	
			            	if(!input4.equals(""))//compare director
			            	{
			            		ResultSet rset3 = stat.executeQuery("select * from person join direct using (PID)");
			            		while (rset3.next()) {	
					            	String pname = rset3.getString("name");
			            		if(pname.toLowerCase().contains(input4))
			            		{
			            			System.out.println(pname);
				            		
			            			int mid = rset3.getInt("MID");
				            		boolean check4 = false;
				            		for(Integer m: mal)
				            		{
				            			if(mid == m)
				            			{
				            				check4 = true;
				            				break;
				            			}
				            		}
				            		if(check4==false)
				            		{
				            			mal.add(mid);
				            			flag=true;
				            		}
			            		}
			            	}
			            }//end if rset3
			            
			            
			            	if(!input5.equals(""))//compare writer
			            	{
			            		ResultSet rset4 = stat.executeQuery("select * from person join write using (PID)");
			            		while (rset4.next()) {	
					            	String pname = rset4.getString("name");
			            		if(pname.toLowerCase().contains(input5))
			            		{
			            			System.out.println(pname);
				            		
			            			int mid = rset4.getInt("MID");
				            		boolean check5 = false;
				            		for(Integer m: mal)
				            		{
				            			if(mid == m)
				            			{
				            				check5 = true;
				            				break;
				            			}
				            		}
				            		if(check5==false)
				            		{
				            			mal.add(mid);
				            			flag=true;
				            		}
			            		}
			            	}		            	
			            }//end if rset4
			            
		           }//end search

		           System.out.println("show movies");
		           for(Integer m: mal)
		        	   System.out.println(m);

		           
	            	if(flag==false){
	            		incorrectMsg i=new incorrectMsg();
	            		i.incorrectID();
	            		dispose();
	            	}
	            	
		        	   
		        	   
		        	   
		        	   int numMovie = mal.size();
		        	   String[] moviearray = new String[numMovie];
		        	   String[] actarray = new String[numMovie];
		        	   String[] directarray = new String[numMovie]; 
		        	   String[] writearray = new String[numMovie];
		        	   
		        		   for(int i = 0; i < numMovie; i++)//find all info for each movie
		        		   {
		        			   int m = mal.get(i);
		        			   String actinfo = "";
				        	   String directinfo = "";
				        	   String writeinfo = "";
				        	   String movieinfo = "Movie ID: "+m+"\n";
				        	   String genreinfo = "Genre: ";
				        	   
				        	   ResultSet rset5 = stat.executeQuery("select * from movie left outer join act using (MID) left outer join person using (PID)");
		        			   while(rset5.next())
		        			   { 
		        				   if(m==rset5.getInt("MID"))
		        				   {
		        					   if(rset5.getString("name")!=null)
		        						   actinfo += rset5.getString("name")+"\t";
		        					   if(rset5.getString("date_of_birth")!=null)
		        						   actinfo += "BOD: "+rset5.getString("date_of_birth")+"\t";
		        					   if(rset5.getString("gender")!=null)
		        						   actinfo += "Gender: "+rset5.getString("gender")+"\t";
		        					   if(rset5.getString("role")!=null)
		        						   actinfo += "Role: "+rset5.getString("role")+"\n";
		        				   }
		        			   }
		        			   
		        			   ResultSet rset6 = stat.executeQuery("select * from movie left outer join direct using (MID) left outer join person using (PID)");
		        			   while(rset6.next())
		        			   {
		        				   if(m==rset6.getInt("MID"))
		        				   {
		        					   if(rset6.getString("name")!=null)
		        						   directinfo += rset6.getString("name")+"\t";
		        					   if(rset6.getString("date_of_birth")!=null)
		        						   directinfo += "BOD: "+rset6.getString("date_of_birth")+"\t";
		        					   if(rset6.getString("gender")!=null)
		        						   directinfo += "Gender: "+rset6.getString("gender")+"\n";
		        				   }
		        			   }
		        			   
		        			   ResultSet rset7 = stat.executeQuery("select * from movie left outer join write using (MID) left outer join person using (PID)");
		        			   while(rset7.next())
		        			   {
		        				   if(m==rset7.getInt("MID"))
		        				   {
		        					   if(rset7.getString("name")!=null)
		        						   writeinfo += rset7.getString("name")+"\t";
		        					   if(rset7.getString("date_of_birth")!=null)
		        						   writeinfo += "BOD: "+rset7.getString("date_of_birth")+"\t";
		        					   if(rset7.getString("gender")!=null)
		        						   writeinfo += "Gender: "+rset7.getString("gender")+"\n";
		        				   }
		        			   }
		        			   
		        			   ResultSet rset8 = stat.executeQuery("select * from movie");
		        			   while(rset8.next())
		        			   { 
		        				   if(m==rset8.getInt("MID"))
		        				   {
		        					   if(rset8.getString("title")!=null)
		        						   movieinfo += rset8.getString("title")+"\t";
		        					   if(rset8.getString("release_year")!=null)
		        						   movieinfo += "Release in: "+rset8.getString("release_year")+"\t";
		        					   if(rset8.getString("length")!=null)
		        						   movieinfo += "Length: "+rset8.getString("length")+"\t";
		        					   if(rset8.getString("pg_rating")!=null)
		        						   movieinfo += "PG-rating: "+rset8.getString("pg_rating")+"\n";
		        				   }
		        			   }
		        			   
		        			   ResultSet rset9 = stat.executeQuery("select * from genre");
		        			   while(rset9.next())
		        			   {
		        				   if(m==rset9.getInt("MID"))
		        				   {
		        					   if(rset9.getString("genre")!=null)
		        						   genreinfo += rset9.getString("genre")+"\t";
		        				   }
		        			   }
		        			   

		        			   
		        			   if(!genreinfo.equals("Genre: "))
		        				   movieinfo += genreinfo+"\n";
		        			   
		        			   System.out.println(movieinfo);
		        			   System.out.println(actinfo);
		        			   System.out.println(directinfo); 
		        			   System.out.println(writeinfo);
		        			   
		        			   moviearray[i] = movieinfo;
		        			   actarray[i] = actinfo;
		        			   directarray[i] = directinfo;
		        			   writearray[i] = writeinfo;
		        		   }//end find all info for one movie

		        	  allmovieinfo = new String[numMovie][4];
		        	  for(int i = 0; i < numMovie; i++)
		        		  for(int j = 0; j < 4; j++)
		        		  {
		        			  if(j==0)
		        				  allmovieinfo[i][j] = moviearray[i];
		        			  if(j==1)
		        				  allmovieinfo[i][j] = actarray[i];
		        			  if(j==2)
		        				  allmovieinfo[i][j] = directarray[i];
		        			  if(j==3)
		        				  allmovieinfo[i][j] = writearray[i];
		        		  }
		        	  new searchFrameB1();
		            			            	
		           }//end if there is any input
			}catch (SQLException e)
			{
				e.printStackTrace();
			}
			//new staffTypeIn();
		}
	}
	
	
	public class searchFrameB1 extends JFrame {
		public searchFrameB1(){
		JFrame jf=new JFrame("result");
		Container c=jf.getContentPane();
		
		String column[]={"MOVIE","CAST","DIRECTOR","WRITER"};
		JTable jtb1=new JTable(allmovieinfo,column);
		JScrollPane jsp1=new JScrollPane(jtb1);
		c.add(jsp1);
		jf.setVisible(true);
		//jf.setDefaultCloseOperation();
		}	
	}
	
	
class pressB2 implements ActionListener{//checkShows
		
		
		
		public void actionPerformed(ActionEvent arg0){
			try
			{		
				
				DBConnection c = new DBConnection();
				Connection conn;
				
				   String mid=staffFrame.jt6.getText().toLowerCase();// read input
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
	
		           ResultSet rset = stat.executeQuery("select * from movie natural join showing where mid="+mid);
		           ArrayList<String[]> showings = new ArrayList<String[]>();
		           //System.out.println(memberFrame.value);
		            while (rset.next()) {
		            	String[] row = new String[4];
		            	row[0]=mid;
		            	
		            	if(rset.getString("movie_title")!=null)
		            		row[1]=rset.getString("movie_title");
		            	else
		            		row[1]="none";
		            	
		            	if(rset.getString("showtime")!=null)
		            		row[2]=rset.getString("showtime");
		            	else
		            		row[2]="none";
		            	
		            	if(rset.getString("room_number")!=null)
		            		row[3]=rset.getString("room_number");
		            	else
		            		row[3]="none";
		            	
		            	showings.add(row);
		            	}
		            
		            int numShow = showings.size();

		            if(numShow!=0)
		            {
		            	allshowinfo = new String[numShow][4];
		            	for(int i = 0; i < numShow; i++)
		            	{
		            		String[] currentrow = showings.get(i);
		            		allshowinfo[i][0] = currentrow[0];
		            		allshowinfo[i][1] = currentrow[1];
		            		allshowinfo[i][2] = currentrow[2];
		            		allshowinfo[i][3] = currentrow[3];
		            	}
		            }
		            else
		            {
		            	allshowinfo = new String[1][1];
		            	allshowinfo[1][1] = "No show for this movie";
		            }
		            new searchFrameB2();
				
			}catch (SQLException e)
			{
				e.printStackTrace();
			}
		}
	}
	
	public class searchFrameB2 extends JFrame {
		public searchFrameB2(){
		JFrame jf=new JFrame("result");
		Container c=jf.getContentPane();
		
		String column[]={"MID","TITLE","TIME","ROOM_NUMBER"};
		final DefaultTableModel tableModel=new DefaultTableModel(allshowinfo,column);
		final JTable jtb1=new JTable(tableModel);
		jtb1.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		jtb1.addMouseListener(new MouseAdapter(){
			public void mouseClicked(MouseEvent e) {
				// 获得被选中行的索引
				int selectedRow = jtb1.getSelectedRow();
				// 从表格模型中获得指定单元格的值
				String oa = (String) tableModel.getValueAt(selectedRow, 0);
				// 从表格模型中获得指定单元格的值
				String ob = (String) tableModel.getValueAt(selectedRow, 1);
				String oc = (String) tableModel.getValueAt(selectedRow, 2);
				String od = (String) tableModel.getValueAt(selectedRow, 3);
				//aTextField.setText(oa.toString());// 将值赋值给文本框
				//bTextField.setText(ob.toString());// 将值赋值给文本框
				System.out.println(oa+" "+ob+" "+oc+" "+od);
				String ticketinfo = oa+" "+ob+" "+oc+" "+od;
				new buyTicketFrame(ticketinfo);
			}
		});
		JScrollPane jsp1=new JScrollPane(jtb1);
		c.add(jsp1);
		jf.setVisible(true);
		int index=jtb1.getSelectedRow();
		//System.out.println(oa);
		}	
	}
	
	class pressB3 implements ActionListener{//add
		

		public void actionPerformed(ActionEvent arg0){
			try
			{
				DBConnection c = new DBConnection();
				Connection conn;
				
				   String mid=staffFrame.jt9.getText();// read input
				   String mtitle=staffFrame.jt10.getText();// read input
				   String myear=staffFrame.jt15.getText();
				   String mlength=staffFrame.jt16.getText();
				   String mpg=staffFrame.jt17.getText();
				   
				   String pid=staffFrame.jt11.getText();// read input
				   String pname=staffFrame.jt12.getText();// read input
				   String pdob=staffFrame.jt18.getText();
				   String pgender=staffFrame.jt19.getText();
				   System.out.println(mid+ " "+mtitle);
				   
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           
		           if(!mid.equals("")&&!mtitle.equals("")){//add movie
		           ResultSet rset1 = stat.executeQuery("select MID from movie");
		           boolean check=false;
		            while (rset1.next()) {
		            	if(rset1.getString("MID").equals(mid))
		            	{
		            		check=true;
		            		break;
		            	}
		            	}
		            if(check==false)
		            {
		            	if(myear.equals(""))
		            		myear="null";
		            	if(mlength.equals(""))
		            		mlength="null";
		            	if(!mpg.equals(""))
		            		mpg="'"+mpg+"'";
		            	else
		            		mpg="null";
		            	String query="insert into movie values ("+mid+",'"+mtitle+"',"+myear+","+mlength+","+mpg+")";
		            	stat.executeUpdate(query);
		            	

		            }
		           }
		            
		           if(!pid.equals("")&&!pname.equals("")){//add person
		            ResultSet rset2 = stat.executeQuery("select PID from person");
			           boolean check=false;
			            while (rset2.next()) {
			            	if(rset2.getString("PID").equals(pid))
			            	{
			            		check=true;
			            		break;
			            	}
			            	}
			            if(check==false)
			            {
			            	if(pdob.equals(""))
			            		pdob="null";
			            	else
			            		pdob="to_date('"+pdob+"','yyyymmdd')";
			            	if(pgender.equals(""))
			            		pgender="null";
			            	else
			            		pgender="'"+pgender+"'";
			            	String query="insert into person values ("+pid+",'"+pname+"',"+pdob+","+pgender+")";
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


class pressB4 implements ActionListener{//delete
	DBConnection c = new DBConnection();
	Connection conn;

	public void actionPerformed(ActionEvent arg0){
		try
		{
			   String mid=staffFrame.jt7.getText();// read input
			   String pid=staffFrame.jt8.getText();// read input
			   conn=c.getDBConnection();
	           //Statement stat = conn.createStatement();
	           System.out.println("mid"+mid);
	           
	           if(!mid.equals("")){//delete movie
	        	   System.out.println("jinlai");
	        	   Statement stat = conn.createStatement();
	           ResultSet rset1 = stat.executeQuery("select MID from movie");
	           boolean check = false;
	           while(rset1.next())
	           {
	        	   System.out.println(rset1.getString("MID"));
	        	   if(rset1.getString("MID").equals(mid))
	        	   {
	        		   check=true;
	        		   break;
	        	   }
	           }
	           System.out.println("chulai");
	           System.out.print("check="+check+"  MID="+mid);
	           if(check==true){
	        	   
	        	   System.out.println("jinlail");
	        	   String query="delete from movie where MID="+mid;
	        	   stat.executeUpdate(query);
	        	   System.out.println("daozhel");
	           }}
	           
	           if(!pid.equals("")){//delete person
	        	   Statement stat = conn.createStatement();
	           ResultSet rset2 = stat.executeQuery("select PID from person");
	           boolean check = false;
	           while(rset2.next())
	           {
	        	   System.out.println(rset2.getString("PID"));
	        	   if(rset2.getString("PID").equals(pid))
	        	   {
	        		   check=true;
	        		   break;
	        	   }
	           }
	           
	           System.out.print("check="+check+"  PID="+pid);
	           if(check==true)
	           {
	        	   String query="delete from person where PID="+pid;
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


class pressB5 implements ActionListener{//modify
	DBConnection c = new DBConnection();
	Connection conn;
	
	public void actionPerformed(ActionEvent arg0){
		try
		{		
			String momid=staffFrame.jt13.getText();// read input
			   String mopid=staffFrame.jt14.getText();// read input
			   conn=c.getDBConnection();
	           Statement stat = conn.createStatement();
	           
	           
			   if(!momid.equals("")){//modify movie
				   ResultSet rset1 = stat.executeQuery("select MID from movie");
				   boolean check= false;
				   while(rset1.next())
				   {
					   if(rset1.getString("MID").equals(momid))
					   {
						   check=true;
						   break;
					   }
				   }
				   if(check==true)
					   new modifyMovieFrame(momid);
			   
			   }
            		
			   if(!mopid.equals("")){//modify movie
				   ResultSet rset2 = stat.executeQuery("select PID from person");
				   boolean check=false;
				   while(rset2.next())
				   {
					   if(rset2.getString("PID").equals(mopid))
					   {
						   check=true;
						   break;
					   }
				   }
				   if(check==true)
					   new modifyPersonFrame(mopid);
			   
			   }
			
		}catch (Exception e)
		{
			e.printStackTrace();
		}
		//new staffTypeIn();
	}
}
	

class pressB6 implements ActionListener{//modify
	
	
	public void actionPerformed(ActionEvent arg0){
		new modifyShowFrame();
	}
}

	
	
}













