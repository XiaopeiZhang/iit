
public class Money implements Comparable<Money> {

	private long dollars;
	private long cents;
	
	public Money(double amount) {
		dollars = (long) amount;
		cents = (long) Math.round((amount - dollars) * 100);
	}
	
	public Money(Money otherObject) {
		this.dollars = otherObject.dollars;
		this.cents = otherObject.cents;
	}
	
	public Money add(Money otherAmount) {
		Money m = new Money(this);
		m.cents += otherAmount.cents;
		m.dollars += otherAmount.dollars + m.cents / 100;
		m.cents %= 100;
		return m;
	}
	
	public Money subtract(Money otherAmount) {
		Money m = new Money(this);
		if(m.cents >= otherAmount.cents) {
			m.cents -= otherAmount.cents;
			m.dollars -= otherAmount.dollars;
		}
		else {
			m.cents += 100 - otherAmount.cents;
			m.dollars += - 1 - otherAmount.dollars;
		}
		return m;
	}
	
	@ Override
	public int compareTo(Money otherObject) {
		if (this.dollars > otherObject.dollars || (this.dollars == otherObject.dollars && this.cents > otherObject.cents))
			return 1;
		else if (this.dollars < otherObject.dollars || (this.dollars == otherObject.dollars && this.cents < otherObject.cents))
			return -1;
		else
			return 0;
	}
	
	public boolean equals(Money otherObject) {
		if(this.compareTo(otherObject) == 0) {
			return true;
		}
		else {
			return false;
		}
	}
	
	public String toString() {
		if(cents < 10) {
			return "$" + String.valueOf(dollars) + ".0" + String.valueOf(cents);
		}
		else {
			return "$" + String.valueOf(dollars) + "." + String.valueOf(cents);
		}
	}
}
