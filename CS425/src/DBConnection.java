import java.sql.*; 
import java.sql.*; 
import java.sql.*; 


 public class DBConnection {  
 
  
    private Connection conn;  
    private Statement stat;  
    private String url="jdbc:oracle:thin:@fourier.cs.iit.edu:1521:ORCL"; 
    private String user= "jzhou49";;  
    private String password = "zhoujie2312148JAY*";
    //private String driver = 
  
    // 初始化获得statement对象  
    public Connection getDBConnection()  {  
        try {  
            Class.forName("oracle.jdbc.driver.OracleDriver");//加载驱动 
            //System.out.println("数据库驱动成功"); 
        } catch (ClassNotFoundException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        } 
        try{
            url = "jdbc:oracle:thin:@fourier.cs.iit.edu:1521:ORCL";  
            user = "jzhou49";//数据库用户名  
            password = "zhoujie2312148JAY*";//数据库密码  
            conn = DriverManager.getConnection(url, user, password);//获得连接  
        }catch (SQLException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        }
		return conn;
        
    }  
  
    // 执行插入，修改，删除接口  
    /*public int executeUpdate(String sql) {  
        int flag = 0;  
        try {  
            flag = stat.executeUpdate(sql);//执行sql语句  
        } catch (SQLException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        } finally {  
  
            try {  
                stat.close();//释放资源  
                conn.close();  
            } catch (SQLException e) {  
                // TODO Auto-generated catch block  
                e.printStackTrace();  
            }  
  
        }  
        return flag;  
    }  
  
    // 执行查询的接口  
    public ResultSet executeQuery(String sql) {  
        ResultSet set = null;  
        try {  
            set = stat.executeQuery(sql);  
        } catch (SQLException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        } finally {  
          try {  
              stat.close();  
              conn.close();  
          } catch (SQLException e) {  
              // TODO Auto-generated catch block  
              e.printStackTrace();  
          }  
        }  
        return set;  
    }*/
    //public static void main(String[] args){
    //	DBConnection c =new DBConnection();
    //	c.getDBConnection();
    //}
  
}
