
public class Address {

	private String street;
	private String city;
	private String state;
	private String zip;
	
	public Address(String street, String city, String state, String zip) {
		this.street = street;
		this.city = city;
		this.state = state;
		this.zip = zip;
	}
	
	public Address(Address a) {
		this.street = a.street;
		this.city = a.city;
		this.state = a.state;
		this.zip = a.zip;
	}
	
	public String toString() {
		return this.street + ", " + this.city + ", " + this.state + " " + this.zip;
	}
	
}
