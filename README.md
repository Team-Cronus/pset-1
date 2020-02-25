# pset-1

	To test the program, please run pset1.py

0(a) Collaboration
Thomas Her, UID: 305186096
Frank Ren, UID: 904826309
Junyu Lu, UID: 905179762

0(b) Resources
We did not consult any other resources other than
the class notes on MDP.

Problem 1
1(a). We created a state space by creating a 2D array of total size Ns where Ns=L*H.
1(b). We then created a 1D array of size N_A where N_A = 5 and consists of {Up, Down, Left, Right, notMove}.
1(c). For the transition probability  probability p_sa(s'), the total size is Ns^2*N_A. We have to consider
      different probability for different situations. For example, 
	  1. if the current state and our next state, s', aren't adjacent to each other, then the probability is zero. 
	  2. If action is not move, and our current state equals to next state, the probability is one
	  3. If action is not move, and our current state isn't equals to next state, the probability is zero
	  4. If current state is on one of the 4 corners, then
			if our current state = next state and our current state plus the action will exceeds the boundary:
				the probability is 1-Pe/2
			else if our current state = next state, but the action will not exceed the boundary:
				the probability is Pe/2
	  5. For other cases, if our current state plus action equals our next state, then the probability will be 1-3Pe/4
		 else, the probability is Pe/4.
		 
Problem 2
To recrate the example grid world, we model our 1(a) with L=5 and H=6. We also manually coded the obstacles such that
he robot cannot occupy those states
2(a). To update the state transition function from 1(c) to incororate the dislayed obstacles, 
	  1. If our next state is an obstacle, the probability is zero
	  2. There are more "corner" cases due to the obstacle, instead of checking if our current
	     state is at the corners only, we also check to see if there it's at a position where there's
		 wall and an obstacle next to it, i.e when y=3 and x=0. or if it's at a position where's 
		 two obstacles next to it, i.e. when y=2 and x=1.
2(b). To write a function that returns reward of given state, we decide to add attribute to our state.
      To get the reward of a given state, we can call a function called getStateReward with input s, which return
	  s.reward, where s is the input state. 
	  
Problem 3
For the ease of our program, we use number to indicate our action.
0 = notMove
1 = left
2 = right
3 = up
4 = down

We created a new Class called GridWorld which will contains our policy matrix and value matrix
that we will be using for both problem 3 and problem 4.
3(a). We created a policy matrix by creating a 2D array of the size of our state, and we filled it
      up with action=left.

3(b) We wrote a function called display_policy_matrix, which can take in any policy matrix, its length,
     and its height, and we can output it. Below is the display of our initial policy matrix.
	 
	                   1       1       1       1       1
					   1       1       1       1       1
					   1       1       1       1       1
					   1       1       1       1       1
					   1       1       1       1       1
					   1       1       1       1       1
3(c) In 3C we do policy evalutaion, which we have to calculate the value for each state given the
     initial policy. To calculate the value for each state, we created a function getSum which basically
	 implemented the following formula:
			V(s) = summation over all the possible next state(P_s'(s,a) *(Reward_s' + gamma*V(s')))
	 For detailed implementation, please view our codes and corresponding comments.
	 
3(d) For 3(d), we do policy improvement, which repeatedly call our getSum with our current state but with
     different actions (Loop around our action space). We then find the action that maximize the value, which 
	 is the getSum return, and we then update our policy matrix and replace our old action with our new action.
	 Basically, we implemented the following formula:
		 pi_s = arg_max(a) summation over all the possible next state(P_s'(s,a) *(Reward_s' + gamma*V(s')))
		 
3(e) To do the full policy iteration, we have to combine our 3(c) and 3(d). We used a loop to loop through
     policy evalutation and then policy improvement, and we stop when our policy matrix stops changing.
	 
3(f)-3(g)
	We use timer tool from python to calculate the compute time. It takes 0.21 seconds to compute the
	optimal policy, with the optimal policy matrix shown as below.
		4.000 2.000 2.000 4.000 1.000
		4.000 2.000 2.000 4.000 1.000
		4.000 4.000 2.000 4.000 1.000
		4.000 2.000 2.000 4.000 1.000
		4.000 4.000 4.000 4.000 1.000
		2.000 2.000 0.000 1.000 1.000
	We then created a function that takes a initial state and optimal policy, and plot the trajectory with
	given gamma and probability of error. With gamma=0.9 and perror = 0.01. We have our trajectory of 
	[2, 4, 4, 4, 4, 4, 1, 0], which translates to go right, down, down, down, down, down, down, left, and not move.
	We can see it can correctly maximize the reward.
	
Problem 4
For problem 4, we have a very similar problem. Instead of doing policy iteration, we do value iteration, which will
use the value matrix. 
4(a). We used a similar appraoch we used in 3(d).
4(b)-4(c). For our policy iteration we get an evaluation of 0.354 seconds, and our value iteration we recieve
a computation time of 2.26 seconds. In terms of the results, they are the exact same.
		   

Probelm 5
For problem 5, we explore different policies using different values of discount factors and errors.
We change the error probability from 0.01 to 0.2 and 0.4. In our program we noticed that the policy changes
depending on those two factors. For the higher probability error settings, the optimal policy will
change from a safer route which is to go left and avoid the negative reward areas and then going down to its
goal. If we were to have an error with very small probability than the optimal policy
could take more risky and faster routes. 
perror = 0.01
4.000 4.000 4.000 4.000 1.000
4.000 1.000 2.000 4.000 1.000
4.000 4.000 4.000 4.000 1.000
4.000 2.000 2.000 4.000 1.000
4.000 4.000 4.000 4.000 1.000
2.000 2.000 0.000 1.000 1.000

perror = 0.2
4.000 1.000 1.000 1.000 1.000
4.000 1.000 1.000 1.000 1.000
4.000 4.000 4.000 4.000 1.000
4.000 1.000 1.000 4.000 1.000
4.000 4.000 4.000 4.000 1.000
2.000 2.000 0.000 1.000 1.000

perror = 0.4
4.000 1.000 1.000 0.000 2.000
4.000 1.000 1.000 0.000 2.000
4.000 4.000 4.000 0.000 2.000
4.000 1.000 1.000 0.000 2.000
4.000 4.000 4.000 4.000 1.000
2.000 2.000 0.000 1.000 1.000