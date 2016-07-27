/**
 * ProductionWorker extends Employee and stores two
 * extra variables, shift and hourly pay rate.
 * 
 * @author xiaopei
 *
 */
public class ProductionWorker extends Employee {

	int shift;
	double payRate;
	
	public ProductionWorker(String name, String num, int year, int month, int day, int shift, double rate) {
		super(name, num, year, month, day);
		setShift(shift);
		setPayRate(rate);
	}
	
	public ProductionWorker(String name, String num, String date, int shift, double rate) {
		super(name, num, date);
		setShift(shift);
		setPayRate(rate);
	}
	
	public ProductionWorker(Employee emp, int shift, double rate) {
		super(emp);
		setShift(shift);
		setPayRate(rate);
	}
	
	public ProductionWorker(ProductionWorker pw) {
		super(pw.getName(), pw.getNumber(), pw.getHireDate());
		setShift(pw.shift);
		setPayRate(pw.payRate);
	}
	
	public int getShift() {
		return this.shift;
	}
	
	/**
	 * setShift sets the production worker's shift
	 * to be newShift. If newShift is not 1 for day shift
	 * or 2 for night shift, it throws an InvalidShift exception.
	 * 
	 * @param newShift
	 * @throws InvalidShift
	 */
	public void setShift(int newShift) throws InvalidShift {
		if(newShift != 1 && newShift != 2) {
			throw new InvalidShift();
		}
		else {
			this.shift = newShift;
		}
	}
	
	public double getPayRate() {
		return this.payRate;
	}
	
	/**
	 * setPayRate sets the production worker's hourly pay rate
	 * to be newRate. If newRate is negative,
	 * it throws an InvalidPayRate exception.
	 * 
	 * @param newRate
	 * @throws InvalidPayRate
	 */
	public void setPayRate(double newRate) throws InvalidPayRate {
		if(newRate < 0) {
			throw new InvalidPayRate();
		}
		else {
			this.payRate = newRate;
		}
	}
	
	public boolean equals(ProductionWorker pw) {
		return super.equals(pw) && this.shift == pw.shift && this.payRate == pw.payRate;
	}
	
	public String toString() {
		return super.toString() + " " + String.valueOf(this.shift) + " " + String.valueOf(this.payRate);
	}

}
