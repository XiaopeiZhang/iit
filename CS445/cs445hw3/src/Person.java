
public class Person {
	
	private String lastName;
	private String firstName;
	private Address home;

	public Person(String last, String first, Address home) {
		this.lastName = last;
		this.firstName = first;
		this.home = new Address(home);
	}
	
	public Person(Person p) {
		this.lastName = p.lastName;
		this.firstName = p.firstName;
		this.home = new Address(p.home);
	}

	public String toString() {
		return this.lastName + " " + this.firstName + ", " + home.toString();
	}
	
}
