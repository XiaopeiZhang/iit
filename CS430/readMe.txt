Both classes are written in java. Please compile under proper environment.

Attention: For simplicity, the client program does not use exceptions or loops to eliminate unreasonable inputs. Please type reasonable integers as instructed so that the program would properly execute.

Status.java is a class representing jugs with water. size is the number of jugs. jug[] is the amount of water in each corresponding jug. MAXJUG[] is the capacity of each jug. predecessor is the status that is one step before this status. The predecessor of the source status is null. step is the shortest distance from the source status to this status. The step of the source status is 0.

FindTarget.java is a client class to get inputs of the number of jugs, the capacity of each jug, the initial amount of water in each jug and the target amount. The program would output all the statuses from the source target status to the source status with the shortest steps if the target is found. If the target is not found, a report that the target is not found would be output.



Example of successful search:

Output of test with 3 jugs with capacities (3, 5, 8), initial status (0, 0, 8) and target amount 4:

Please enter a positive integer as the number of jugs: 
3
Please enter an integer as the maximum amount for jug 1: 
3
Please enter an integer as the amount in jug 1, and make sure the value is between 0 and 3 : 
0
Please enter an integer as the maximum amount for jug 2: 
5
Please enter an integer as the amount in jug 2, and make sure the value is between 0 and 5 : 
0
Please enter an integer as the maximum amount for jug 3: 
8
Please enter an integer as the amount in jug 3, and make sure the value is between 0 and 8 : 
8
Please enter an integer as the target amount you would like to get: 
4
jug1	jug2	jug3	Number of steps
3	4	1	Step: 6
2	5	1	Step: 5
2	0	6	Step: 4
0	2	6	Step: 3
3	2	3	Step: 2
0	5	3	Step: 1
0	0	8	Step: 0



Example of unsuccessful search:

Output of test with 4 jugs with capacities (2, 2, 2, 6), initial status (0, 0, 0, 6) and target amount 5:

Please enter a positive integer as the number of jugs: 
4
Please enter an integer as the maximum amount for jug 1: 
2
Please enter an integer as the amount in jug 1, and make sure the value is between 0 and 2 : 
0
Please enter an integer as the maximum amount for jug 2: 
2
Please enter an integer as the amount in jug 2, and make sure the value is between 0 and 2 : 
0
Please enter an integer as the maximum amount for jug 3: 
2
Please enter an integer as the amount in jug 3, and make sure the value is between 0 and 2 : 
0
Please enter an integer as the maximum amount for jug 4: 
6
Please enter an integer as the amount in jug 4, and make sure the value is between 0 and 6 : 
6
Please enter an integer as the target amount you would like to get: 
5
Target amount not found
