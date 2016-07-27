
public class CreditCardDemo {

	public static void main(String[] args) {
//		Diane Christie, 237J Harvey Hall, Menomonie, WI 54751
//		Balance: $0.00
//		Credit Limit: $1000.00
//		Attempt to charge $200.00
//		Charge: $200.00
//		Balance: $200.00
//		Attempt to charge $10.02
//		Charge: $10.02
//		Balance: $210.02
//		Attempt to charge $200.00
//		Charge: $200.00
//		Balance: $200.00
//		Attempt to charge $10.02
//		Charge: $10.02
//		Balance: $210.02
//		Attempt to pay $25.00
//		Payment: $25.00
//		Balance: $185.02
//		Attempt to charge $990.00
//		Exceeds credit limit
//		Balance: $185.02
		Address home = new Address("237J Harvey Hall", "Menomonie", "WI", "54751");
		Person person = new Person("Diane", "Christie", home);
		Money limit = new Money(1000);
		CreditCard card = new CreditCard(person, limit);
		System.out.println(card.getPersonals());
		System.out.println("Balance: " + card.getBalance());
		System.out.println("Credit Limit: " + card.getCreditLimit());
		card.charge(new Money(200));
		card.charge(new Money(10.02));
		CreditCard card1 = new CreditCard(person, limit);
		card1.charge(new Money(200));
		card1.charge(new Money(10.02));
		card1.payment(new Money(25));
		card1.charge(new Money(990));
		System.out.println();
		System.out.println("Balance: " + card1.getBalance());
	}
	
}
