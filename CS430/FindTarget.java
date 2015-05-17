import java.util.ArrayList;
import java.util.Scanner;

public class FindTarget {

	public static void main(String[] args) {
		
		Scanner scan = new Scanner(System.in);
		System.out.println("Please enter a positive integer as the number of jugs: ");
		int num = Integer.parseInt(scan.next());
		int[] max = new int[num];
		int[] jug = new int[num];
		for(int i = 0; i < num; i++)
		{
			System.out.println("Please enter an integer as the maximum amount for jug " + ( i + 1 ) + ": ");
			max[i] = Integer.parseInt(scan.next());
			System.out.println("Please enter an integer as the intial amount in jug " + ( i + 1 ) + ", and make sure the value is between 0 and " + max[i] + " : ");
			jug[i] = Integer.parseInt(scan.next());
		}
		System.out.println("Please enter an integer as the target amount you would like to get: ");
		int target = Integer.parseInt(scan.next());
		scan.close();
		
		Status source = new Status(jug, max);
		ArrayList<Status> sal = new ArrayList<Status>();
		sal.add(source);
		
		int preSize = sal.size();
		sal = source.pour(sal);
		int postSize = sal.size();
		
		while(preSize != postSize)
		{
			for(int i = preSize - 1; i < postSize; i ++)
				sal = sal.get(i).pour(sal);
			preSize = postSize;
			postSize = sal.size();
		}
		
		// traverse to see whether the target amount can be obtained
		Status t = null;
		for(Status s: sal)
		{
			if(s.targetStatus(target))
			{
				t = s;
				break;
			}
		}
		
		if(t != null)
			t.trace(source); // print out the vertices visited from source vertex to target vertex in reverse order
		else
			System.out.println("Target amount not found");
	}

}
