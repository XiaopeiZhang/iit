import java.util.ArrayList;

public class Status
{
	private int[] jug;
	private Status predecessor = null;
	private int step = -1, size;
	private int[] MAXJUG;

	// constructor for source vertex
	public Status(int[] j, int[] m)
	{
		size = m.length;
		jug = new int[size];
		MAXJUG = new int[size];
		for(int i = 0; i < size; i++)
		{
			if(m[i] < 0)
				throw new IllegalArgumentException();
			MAXJUG[i] = m[i];
			if(j[i] < 0 || j[i] > MAXJUG[i])
				throw new IllegalArgumentException();
			jug[i] = j[i];
		}
		step = 0;
		predecessor = null;
	}
	
	// constructor for vertices generated
	public Status(int[] j, Status p)
	{
		size = p.size;
		jug = new int[size];
		MAXJUG = p.MAXJUG;
		for(int i = 0; i < size; i++)
		{
			if(j[i] < 0 || j[i] > MAXJUG[i])
				throw new IllegalArgumentException();
			jug[i] = j[i];
		}
		predecessor = p;
		step = p.step + 1;
	}
	
	public boolean equals(Status comp)
	{
		int i = 0;
		for(; i < size; i++)
		{
			if(jug[i] != comp.jug[i])
				return false;
		}
		return true;
	}
	
	public String toString()
	{
		String s = new String();
		for(int i = 0; i < size; i++)
			s += jug[i] + "\t";
		s += "Step: " + step;
		return s;
	}
	
	// generate all the descendant vertices that can be obtained by one step from this vertex
	public ArrayList<Status> pour(ArrayList<Status> sal)
	{
		Status temp = null;
		int[] t = new int[size];
		for(int i = 0; i < size; i++)
			t[i] = jug[i];
		
		// get all the statuses by pouring from any jug to jug[i]
		for(int i = 0; i < size; i++)
		{
			int b = this.jug[i];
			int m = this.MAXJUG[i];
			for(int j = 0; j < size; j++)
			{
				if(j != i)
				{
					int a = this.jug[j];
					int can = canPour(a, b, m);
					
					if(can == 1)
					{
						t[i] = a + b;
						t[j] = 0;
						temp = new Status(t, this);
						if(temp.checkRepetition(sal))
							sal.add(temp);
						for(int k = 0; k < size; k++)
							t[k] = jug[k];
					}
					
					if(can == 0)
					{
						t[i] = m;
						t[j] = a - (m - b);
						temp = new Status(t, this);
						if(temp.checkRepetition(sal))
							sal.add(temp);
						for(int k = 0; k < size; k++)
							t[k] = jug[k];
					}
				}
			}
		}
		
		return sal;
	}
	
	// check whether this vertex has already been in the array list
	public boolean checkRepetition(ArrayList<Status> sal)
	{
		int index = 0, s = sal.size();
		for(;index < s; index++)
		{
			if(sal.get(index).equals(this))
				return false;
		}
		return true;
	}
	
	// check whether a amount in one jug can be poured to another jug with b amount and capacity maxb
	private int canPour(int a, int b, int maxb)
	{
		if(b < maxb && a > 0)
		{
			if (a <= maxb - b)
				return 1;// can pour all the water from a to b and empty a
			else
				return 0;// can fill b but not empty a
		}
		else
			return -1;// cannot pour
	}
	
	// check whether the target amount is in the vertex
	public boolean targetStatus(int t)
	{
		for(int i = 0; i < size; i++)
		{
			if(jug[i] == t)
				return true;
		}
		return false;
	}
	
	// trace back and print all the vertices from the target vertex to the source vertex
	public void trace(Status s)
	{
		Status t = this;
		String str = new String();
		for(int i = 0; i < size; i++)
			str += "jug" + ( i + 1 ) + "\t"; 
		str += "Number of steps";
		System.out.println(str);
		while(!t.equals(s))
		{
			System.out.println(t.toString());
			t = t.predecessor;
		}
		System.out.println(s.toString());
	}

}