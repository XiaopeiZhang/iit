/**
 * Employee stores name, number and hire data.
 * 
 * @author xiaopei
 *
 */
public class Employee{

	private String name;
	private String number;
	private String hireDate;
	
	public Employee(String name, String num, int year, int month, int day) {
		this.name = name;
		setNumber(num);
		this.hireDate = String.valueOf(month) + "/" + String.valueOf(day) + "/" + String.valueOf(year);
	}
	
	public Employee(String name, String num, String date) {
		this.name = name;
		setNumber(num);
		this.hireDate = date;
	}
	
	public Employee(Employee emp) {
		this.name = emp.name;
		setNumber(emp.number);
		this.hireDate = emp.hireDate;
	}
	
	public String getName() {
		return this.name;
	}
	
	public void setName(String newName) {
		this.name = newName;
	}
	
	public String getNumber() {
		return this.number;
	}
	
	/**
	 * setNumber sets the emplyee's number to be newNum.
	 * If length of newNum is not 5, or the first three
	 * characters are not digits, or the fourth character
	 * is not '-', or the last character is not an upper case
	 * letter, it throws an InvalidEmployeeNumber exception.
	 * 
	 * @param newNum
	 * @throws InvalidEmployeeNumber
	 */
	public void setNumber(String newNum) throws InvalidEmployeeNumber {
		if(newNum.length() != 5 || !Character.isDigit(newNum.charAt(0)) || !Character.isDigit(newNum.charAt(1)) || !Character.isDigit(newNum.charAt(2)) || newNum.charAt(3) != '-' || !Character.isLetter(newNum.charAt(4)) || Character.isLowerCase(newNum.charAt(4))) {
			throw new InvalidEmployeeNumber();
		}
		else {
			this.number = newNum;
		}
	}
	
	public String getHireDate() {
		return this.hireDate;
	}
	
	public void setHireDate(String date) {
		this.hireDate = date;
	}
	
	public void setHireDate(int newYear, int newMonth, int newDay) {
		this.hireDate = String.valueOf(newMonth) + "/" + String.valueOf(newDay) + "/" + String.valueOf(newYear);
	}
	
	public boolean equals(Employee emp) {
		return this.name.equals(emp.name) && this.number.equals(emp.number) && this.hireDate.equals(emp.hireDate);
	}
	
	public String toString() {
		return this.name + " " + this.number + " " + this.hireDate;
	}
	
}
