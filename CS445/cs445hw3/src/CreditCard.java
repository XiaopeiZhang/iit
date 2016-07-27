
public class CreditCard {

	private Money balance;
	private Money creditLimit;
	private Person owner;
	
	public CreditCard(Money balance, Money limit, Person owner) {
		this.balance = new Money(balance);
		this.creditLimit = new Money(limit);
		this.owner = new Person(owner);
	}
	
	public CreditCard(Person newCardHolder, Money limit) {
		this.balance = new Money(0);
		this.creditLimit = new Money(limit);
		this.owner = new Person(newCardHolder);
	}
	
	public Money getBalance() {
		return new Money(balance);
	}
	
	public Money getCreditLimit() {
		return new Money(creditLimit);
	}
	
	public String getPersonals() {
		return this.owner.toString();
	}
	
	public void charge(Money amount) {
		System.out.println("Attempt to charge " + amount);
		if(this.creditLimit.compareTo(this.balance.add(amount)) < 0) {
			System.out.println("Exceeds credit limit.");
		}
		else {
			System.out.println("Charge: " + amount);
			this.balance = this.balance.add(amount);
			System.out.println("Balance: " + this.balance);
		}
	}
	
	public void payment(Money amount) {
		System.out.println("Attempt to pay " + amount);
		System.out.println("Payment: " + amount);
		this.balance = this.balance.subtract(amount);
		System.out.println("Balance: " + this.balance);
	}
}
