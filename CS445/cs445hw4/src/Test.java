import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Test {

	public static void main(String[] args) {
		ProductionWorker pw1 = new ProductionWorker("John", "111-A", 2016, 1, 1, 1, 20);
		ProductionWorker pw2 = new ProductionWorker("Joan", "121-A", "1/1/2016", 1, 20);
		ProductionWorker pw3 = new ProductionWorker("Doe", "113-Z", "1/1/2016", 1, 20);
		List<ProductionWorker> pwList = new ArrayList<>();
		pwList.add(pw1);
		pwList.add(pw2);
		pwList.add(pw3);
		
		try {
			DataOutputStream output = new DataOutputStream(new FileOutputStream("employees.dat"));
			for(ProductionWorker p: pwList) {
				System.out.println(p);
				output.writeUTF(p.toString());
			}
			output.close();
		}
		catch(IOException e) {
			e.printStackTrace();
		}
		
		for(ProductionWorker p: pwList) {
			System.out.println(p.getName());
			p.setName("Jack");
			System.out.println(p.getNumber());
			p.setNumber("321-Z");
			System.out.println(p.getHireDate());
			p.setHireDate("2/2/2016");
			System.out.println(p.getShift());
			p.setShift(2);
			System.out.println(p.getPayRate());
			p.setPayRate(30);
			System.out.println(p);
		}
		
		try {
			DataInputStream input = new DataInputStream(new FileInputStream("employees.dat"));
	        while (input.available() > 0) {
	            String x = input.readUTF();
	            System.out.println(x);
	        }
	        input.close();
		}
		catch(IOException e) {
			e.printStackTrace();
		}
	
	
	try {
		ProductionWorker pw4 = new ProductionWorker("Doe", "113xZ", "1/1/2016", 3, -1);
	}
	catch(InvalidEmployeeNumber | InvalidShift | InvalidPayRate e) {
		e.printStackTrace();
	}
	
	try {
		ProductionWorker pw4 = new ProductionWorker("Doe", "113-3", "1/1/2016", 3, -1);
	}
	catch(InvalidEmployeeNumber | InvalidShift | InvalidPayRate e) {
		e.printStackTrace();
	}
	
	try {
		ProductionWorker pw4 = new ProductionWorker("Doe", "113-z", "1/1/2016", 3, -1);
	}
	catch(InvalidEmployeeNumber | InvalidShift | InvalidPayRate e) {
		e.printStackTrace();
	}
	
	try {
		ProductionWorker pw4 = new ProductionWorker("Doe", "11a-Z", "1/1/2016", 3, -1);
	}
	catch(InvalidEmployeeNumber | InvalidShift | InvalidPayRate e) {
		e.printStackTrace();
	}
	
	try {
		ProductionWorker pw4 = new ProductionWorker("Doe", "113-Z", "1/1/2016", 3, -1);
	}
	catch(InvalidEmployeeNumber | InvalidShift | InvalidPayRate e) {
		e.printStackTrace();
	}
	
	try {
		ProductionWorker pw4 = new ProductionWorker("Doe", "113-Z", "1/1/2016", 1, -1);
	}
	catch(InvalidEmployeeNumber | InvalidShift | InvalidPayRate e) {
		e.printStackTrace();
	}
	
	
	}

}
