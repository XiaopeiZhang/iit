import java.awt.*;
import java.awt.event.*;
import java.sql.*;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Scanner;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;



public class memberFrame extends JFrame {
	
	//public static final char[][] row = null;

	//public static void main(String args[]){
	//	new memberFrame();
	//}

	static String[][] allmovieinfo= null;
	static String[][] allshowinfo = null;
	static JButton b1=new JButton("searchMovieB1");
	static JButton b2=new JButton("checkShowsB2");
			
	static JTextField jt1 = new JTextField("");//title
	static JTextField jt2 = new JTextField("");//genre
	static JTextField jt3 = new JTextField("");//actor
	static JTextField jt4 = new JTextField("");//director
	static JTextField jt5 = new JTextField("");//writer
	static JTextField jt6 = new JTextField("");//MID
	
	
	static JLabel jl1=new JLabel("TITLE                   "
			+ "           GENRE                   "
			+ "        ACTOR              "
			+ "           DIRECTOR               "
			+ "        WRITER");
	//static JLabel jl2=new JLabel("searchResult");
	static JLabel jl3=new JLabel("MID");
	
	

	
	public memberFrame(){
		
		JFrame jf = new JFrame();
		Container c = jf.getContentPane();
		
		jf.setTitle("memberFrame");
		c.setLayout(null);
				
		jf.setBounds(100,20,900,700);
		
		b1.setBounds(320, 160, 150, 40);
		b2.setBounds(700, 350, 150, 40);
		//b3.setBounds(700, 600, 150, 40);
		
		jt1.setBounds(100, 100, 100, 30);
		jt2.setBounds(220, 100, 100, 30);
		jt3.setBounds(340, 100, 100, 30);
		jt4.setBounds(460, 100, 100, 30);
		jt5.setBounds(580, 100, 100, 30);
		jt6.setBounds(340, 250, 100, 30);
		
		jl1.setBounds(140, 90, 20000, 100);
		//jl2.setBounds(370, 90, 150, 40);
		jl3.setBounds(380, 290, 150, 40);
		
		//jtb1.setBounds(100, 130, 600, 180);
		//jtb2.setBounds(100, 400, 600, 180);
		
		//jsp1.setBounds(100, 130, 600, 180);
		//jsp2.setBounds(100, 400, 600, 180);

		
		b1.addActionListener(new pressB1());
		b2.addActionListener(new pressB2());
		//b3.addActionListener(new pressB3());
		
		c.add(b1);
		c.add(b2);
		//c.add(b3);
		
		c.add(jt1);
		c.add(jt2);
		c.add(jt3);
		c.add(jt4);
		c.add(jt5);
		c.add(jt6);
		
		c.add(jl1);
		//c.add(jl2);
		c.add(jl3);
		
		//c.add(jsp1);
		//c.add(jsp2);
		
		jf.setVisible(true);
		setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
	}
	
	class pressB1 implements ActionListener{//search click
		
		
		DBConnection c = new DBConnection();
		Connection conn;
		boolean flag=false;
		public void actionPerformed(ActionEvent arg0){
			try
			{
					
					
					
				   String input1=memberFrame.jt1.getText().toLowerCase();// read input
				   String input2=memberFrame.jt2.getText().toLowerCase();// read input
				   String input3=memberFrame.jt3.getText().toLowerCase();// read input
				   String input4=memberFrame.jt4.getText().toLowerCase();// read input
				   String input5=memberFrame.jt5.getText().toLowerCase();// read input
				   conn=c.getDBConnection();
		           Statement stat = conn.createStatement();
		           ArrayList<Integer> mal = new ArrayList<Integer>();
		           
		           System.out.println(input1);
		           
		           if(!input1.equals("")||!input2.equals("")||!input3.equals("")||!input4.equals("")||!input5.equals("")){
		        	   //System.out.println("111111111");   
		        	   
		        	   if(!input1.equals("")||!input2.equals("")){//only search movie and genre
		        		   ResultSet rset1 = stat.executeQuery("select * from movie natural join genre");
		        		   //System.out.println("111111111");
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
		        			   String actinfo = "Information of actors and actresses: \n";
				        	   String directinfo = "Information of directors: \n";
				        	   String writeinfo = "Information of writers: \n";
				        	   String movieinfo = "Movie ID: "+m+"\nInformation of the movie: \n";
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
		
		
		DBConnection c = new DBConnection();
		Connection conn;
		
		
		public void actionPerformed(ActionEvent arg0){
			try
			{		
				   String mid=memberFrame.jt6.getText().toLowerCase();// read input
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
	
	
	class pressB3 implements ActionListener{
		public void actionPerformed(ActionEvent arg0){
			//dispose();
			//new memberTypeIn();
		}
	}
}










