
public class MoneyDriver {

	public static void main(String[] args) {
//		The current amount is $500.00
//		Adding $10.02 gives $510.02
//		Subtracting $10.88 gives $499.14
//		$10.02 equals $10.02
//		$10.88 does not equal $10.02
		Money m = new Money(500);
		System.out.println("The current amount is " + m);
		Money add = new Money(10.02);
		m = m.add(add);
		System.out.println("Adding " + add + " gives " + m);
		Money subtract = new Money(10.88);
		m = m.subtract(subtract);
		System.out.println("Subtracting " + subtract + " gives " + m);
		Money eq = new Money(10.02);
		Money ineq = new Money(10.88);
		if(add.equals(eq)) {
			System.out.println(eq + " equals " + add);
		}
		if(!add.equals(ineq)) {
			System.out.println(ineq + " does not equal " + add);
		}
	}

}
