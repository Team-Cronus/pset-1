import random
import time

ROW_NUM = 6
COL_NUM = 5
ACT_SPACE = 5
NOT_MOVE=0
LEFT=1
TOP=3
RIGHT=2
DOWN=4
###############################################################################
#1a) the size of the state space N(s)=N(rows)*N(cols)=6*5=30
###############################################################################
class oneState:
    col = row  = reward = hasObs = 0    
    def __init__(self,row,col,reward):
       self.row=row
       self.col=col
       self.reward=reward
#this function is used for copying state
    def copyState(self):
        copy_state = State(self.row,self.col,self.reward)
        return copy_state
#prints information of the space
    def myPrint(self):
        print("(",self.row,",",self.col,",o=",self.hasObs,",r=",self.reward,")", end=" ")

class stateSpace:
    row_num = col_num =state2Darray= 0
    def __init__(self,row_num,col_num):
        self.row_num = row_num-1
        self.col_num = col_num-1
        self.state2Darray=[]
        for i in range(row_num):
            self.state2Darray.append([oneState(row=i,col=j,reward=0) 
                                       for j in range(col_num)])
#function for setting reward for states
    def setStateReward(self,r,c,re):
         self.state2Darray[r][c].reward = re
#function for getting reward for states
    def getStateReward(self,r,c):
         return self.state2Darray[r][c].reward
#function for compare two states
    def compareTwoStates(self,otherState):
         if(self.row == otherState.row and self.col == otherState.col):
             return ture
         return false
    #setter to set obstacle in this state location    
    def setObs(self, row, col, has):
        self.state2Darray[row][col].hasObs = has
    def getObs(self,row,col,has):
        return self.state2Darray[row][col].hasObs
#prints every single state in statespace
    def printAll(self):
        for i in range(ROW_NUM-1,-1,-1):
            print("")
            for j in range(COL_NUM):
                self.state2Darray[i][j].myPrint()
        print("")
###############################################################################
#1b) the size of the action space N(A)=5
###############################################################################
class robotAction:
    row=col=0
    directionForMove=0  #0:stay(no move),1:left,2:right,3:up,4:down
    def __init__(self, direction_move):
        self.directionForMove=direction_move

        if(self.directionForMove==0):
          self.row=0
          self.col=0
        elif(self.directionForMove==1):
          self.row=0
          self.col=-1
        elif(self.directionForMove==2):
          self.row=0
          self.col=1
        elif(self.directionForMove==3):
          self.row=1
          self.col=0
        elif(self.directionForMove==4):
          self.row=-1
          self.col=0
###############################################################################
#1c) returns the probability Psa(s') given inputs s, a, s'
###############################################################################
def to_Next_State_Prob(action,currState,error,nextState):
#check if the states are adjacent to each other
    if(abs(currState.row-nextState.row)+abs(currState.col-nextState.col)>1):
        return 0
#if the robot choose not to move (action is (0,0))
    if(action.directionForMove == 0 and (currState.row==nextState.row
       and currState.col==nextState.col)):
        return 1
#if action is not move and s' does not equal s
    if(action.directionForMove==0 and (currState.row != nextState.row 
       or currState.col != nextState.col)):
        return 0
    if(isObstacle(nextState)):
        return 0
#if the robot choose to move(action is not (0,0))
    #First, current state is on one of the 4 corners
    if(checkcornerAndObsta(currState)): 
        #if current state + action is greater than boundary 
        if(exceedBound(currState, action) and currState.col==nextState.col and currState.row == nextState.row):
               return 1-error+error/2
        else:
            if(currState.col==nextState.col and currState.row == nextState.row):
               return error/2
    #Second,current state is not on the corner of the gridworld
    if((currState.row+action.row)==nextState.row 
        and (currState.col+action.col)==nextState.col):
        return 1-error+error/4
    else:
#        print(action.row," ",action.col)
        return error/4

def isObstacle(state):
    if ((state.row == 1 and state.col == 1) or
        (state.row == 1 and state.col == 2) or
        (state.row == 3 and state.col == 2) or
        (state.row == 3 and state.col == 1)):
        return True
    else:
        return False

#helper function to check if the current state is on corner
def checkcorner(currState):
    if((currState.row==0 and currState.col==0) 
         or (currState.row==0 and currState.col==COL_NUM)
         or (currState.row==ROW_NUM and currState.col==COL_NUM)
         or (currState.row==ROW_NUM and currState.col==0)):
        return True
    else:
        return False

#helper function to check if the currentState + action exceed the regular bound of the frame
def exceedBound(currState, action):
    if(currState.row+action.row<0 or currState.row+action.row> ROW_NUM
         or currState.col+action.col<0 or currState.col+action.col>COL_NUM):   
        return True
    else:       
        return False 

###############################################################################
#2a)  incorporate the displayed obstacles, edit 1C
###############################################################################
#the things we need to change here is to change the checkcorner function,
#this function will also include the 6 positions that are near the obstacles
#the coordinates are (3,0),(2,1),(2,2),(1,0),(0,1),(0,2)
def checkcornerAndObsta(currState):
    if((currState.row==0 and currState.col==0) 
         or (currState.row==0 and currState.col==(COL_NUM-1))
         or (currState.row==(ROW_NUM - 1) and currState.col==(COL_NUM-1))
         or (currState.row==(ROW_NUM - 1) and currState.col==0)
         or (currState.row==3 and currState.col==0)
         or (currState.row==1 and currState.col==0)
         or (currState.row==2 and currState.col==1)
         or (currState.row==2 and currState.col==2)
         or (currState.row==0 and currState.col==1)
         or (currState.row==0 and currState.col==2)):
        return True
    else:
        return False
        
###############################################################################
#2b) returns the reward r(s) given input s
###############################################################################
def getStateReward(s):
    return s.reward

#######################################################
#this class is used for generate the gridWorld
#######################################################
class gridWorld:
    col_num=row_num=error=value_matrix=0
    policy_matrix=[]
    state_space=0
    def __init__(self,col,row,error):
        self.row_num=row - 1
        self.col_num=col - 1
        self.error=error
        self.state_space=stateSpace(ROW_NUM,COL_NUM)
        self.policy_matrix= self.policyMatrix()
        self.initialize_value_matrix()
    def return_value(self,oneSate):
        return self.value_matrix[oneState.row][oneState.col];
    
    def return_policy(self,oneState):
        return self.policy_matrix[oneState.row][oneState.col]

    def initialize_value_matrix(self):
        self.value_matrix = []
        for i in range(ROW_NUM):
            self.value_matrix.append([0 for j in range(COL_NUM)])
        
    def display_value_matrix(self):
        for i in range(ROW_NUM-1,-1,-1):
            print("")
            for j in range(COL_NUM):
                print(f'{self.value_matrix[i][j]:.3f}',end=" ")
        print("")
###############################################################################
#3a) Create and populate a matrix/array that contains the actions
###############################################################################
    def policyMatrix(self):
       policy_matrix=[]
       for i in range(ROW_NUM):
            policy_matrix.append([LEFT for j in range(COL_NUM)])
       print("")
       return policy_matrix

###############################################################################
#3b) a function to display any input policy π, and use it to display π0.
###############################################################################
    def display_policy_matrix(self, pmat):
       for i in range(ROW_NUM-1,-1,-1):
            print("")
            for j in range(COL_NUM):
                print(f'{pmat[i][j]:.3f}',end=" ")
       print("")
###############################################################################
#3c) a function to compute the policy evaluation of a policy π.
###############################################################################
    def evaluatePolicy(self, policy_matrix, gamma):
        temp = 0.2
        #while(temp>0.1):
        #delta=0
        for x in range(1):
            temp = 0
            for i in range(ROW_NUM):
                for j in range(COL_NUM):
                    state = self.state_space.state2Darray[i][j]
                    #value = self.return_value(state)
                    value = self.value_matrix[i][j]
                    a = self.policy_matrix[state.row][state.col]
                    self.value_matrix[i][j] = self.getSum(state, a, gamma)
                    #abs_value = abs(value-self.value_matrix[i][j])
                    
                    #temp = max(temp, abs(value-self.value_matrix[i][j]))                   

    def getSum(self, s, a, gamma):
        sum1 = 0
        for i in range(ROW_NUM):
            for j in range (COL_NUM):
                s_prime = self.state_space.state2Darray[i][j]
                New_a = robotAction(a)
                t_fn = to_Next_State_Prob(New_a, s, self.error, s_prime)
                v_fn = self.value_matrix[i][j]
                reward = self.state_space.getStateReward(i,j) 
                sum1 = sum1 + t_fn*(reward + gamma*v_fn)
                if (sum1 > 100):
                	sum1 = sum1/100
        return sum1

###############################################################################
#3d)    output: boolean value to determine its completion, also changes the policy matrix
#       input: No input
#       Function: Use a function, V(s), that calculates the value to find the
#                 optimal policy. We do this by using a greedy algorithm to
#                 find the maximum value 
###############################################################################

    def getMaxPolicy(self, gamma):  
        g = gamma
        isOpt = True
        for col in range (0, COL_NUM):
            for row in range (0, ROW_NUM):
               #self.display_policy_matrix()
               Vprev = -1000
               prevAction = self.policy_matrix[row][col]    #left->
               state = self.state_space.state2Darray[row][col]  #
               optAction = -1
               for action in range(0, ACT_SPACE):
                   Vnext = self.getSum(state, action, g)                
                   if Vnext > Vprev:
                       optAction = action
                       Vprev = Vnext
                   
               if optAction != prevAction:
                   isOpt = False
               self.policy_matrix[row][col] = optAction
        #self.display_policy_matrix()
        return isOpt
           
###############################################################################
#3e) Combine the function from 3(c) and 3(d) to compute the policy iteration.
#
###############################################################################
    def policyIteration(self, gamma):
        st_time = time.time()
        #self.initialize_value_matrix()
        stop = False
        while(stop == False):
        #for i in range(10):
            self.evaluatePolicy( self.policy_matrix, gamma)
            #world.display_value_matrix(self.policy_matrix)
            stop = self.getMaxPolicy(gamma)
            #world.display_policy_matrix(self.policy_matrix)	
        end_time = time.time()
        print('Optimal policy took ' + str(end_time - st_time) + ' seconds to finish.\n')

 #################################################################################
 # 3g) Input: state space position as col and row, discount factor as gamma
 #     Output: The trajectory as an array of a sequence of actions
 #################################################################################
    def plot_trajectory(self, col, row, discount):
        trajectory, reward, realTrajectory, reward2 = self.getTrajectoryAndReward(col,row,discount)
        #prints trajectory as an array of numbers 0-5, and reward
        #will plot trajectory via other program like excel
        print("trajectory", trajectory, " Reward: ", reward)
        print("Real trajectory", realTrajectory, " Reward2: ", reward2)
    
    #as the function name suggested, it will get a trajectory of ideal robot movement case where the
    #probability of error is 0. It will also get a trajectory of real-world robot movement where the
    #probability of error is user-defined. Both trajectory will output the discounted sum of reward.
    def getTrajectoryAndReward(self, col, row, discount):
        self.col_num = col
        self.row_num = row
        trajectory = []
        realTrajectory = []
        step = step2 = 0
        reward = reward2 = 0
        #if the action is not_move, then we are at our goal
        #otherwise, keep iterating through policies
        action = self.policy_matrix[self.row_num][self.col_num]
        realAction = self.policy_matrix[self.row_num][self.col_num]
        #calculate an ideal trajectory
        while action != 0:      
            #append the action to the trajectory
            action = self.policy_matrix[self.row_num][self.col_num]
            trajectory.append(action)
            #update discounted reward
            reward += discount**step * self.state_space.getStateReward(self.row_num,self.col_num)
            #update the position of state space using the action
            self.updateState(action)
            step += 1
        #bring state back to initial for second calculation
        self.col_num = col
        self.row_num = row
        #calculate a non ideal trajectory
        while realAction != 0:      
            #append the action to the trajectory
            realAction = self.policy_matrix[self.row_num][self.col_num]
            realAction = self.getRealAction(realAction, self.error)
            realTrajectory.append(realAction)
            #update discounted reward
            reward2 += discount**step2 * self.state_space.getStateReward(self.row_num,self.col_num)
            #update the position of state space using the action
            self.updateState(realAction)
            step2 += 1
        return trajectory, reward, realTrajectory, reward2 
    #updates state based off of action given
    #make sure that if robot is moving into a wall or obstacle, it is staying at its current place        
    def updateState(self, action):
        if action == 1: #left
            if self.col_num == 0:
                self.col_num = self.col_num
            elif self.col_num ==3 and (self.row_num == 3 or self.row_num == 1):
                self.col_num = self.col_num
            else:
                self.col_num -= 1
        elif action == 2: #right
            if self.col_num == 4:
                    self.col_num = self.col_num
            elif(self.col_num ==0 and (self.row_num == 3 or self.row_num == 1)):
                self.col_num = self.col_num
            else:
                self.col_num += 1
        elif action == 3: #up
            if(self.row_num == 5):
                self.row_num = self.row_num
            elif((self.row_num ==2 or self.row_num == 0) and (self.col_num == 1 or self.col_num == 2)):
                self.row_num = self.row_num
            else:
                self.row_num += 1
        elif action == 4: #down
            if(self.row_num == 0):
                self.row_num = self.row_num
            elif((self.row_num ==2 or self.row_num == 4) and (self.col_num == 1 or self.col_num == 2)):
                self.row_num = self.row_num
            else:
                self.row_num -= 1
    #use random generator to simulate the robot movement in the real world with provided Probability of error
    def getRealAction(self, action, perror):
        temp = 1 - perror + perror/4
        temp2 = 10000*temp - 1
        temp3 = random.randint(0, 9999)
        if(temp3 <= temp2):
            return action
        else:
            temp4 = random.randint(0,2)
            if(temp4 == 0):
                action_temp = action+1
                if(action_temp > 4):
                    action_temp = action_temp - 4
                    return action_temp
            elif(temp4 == 1):
                action_temp = action+2
                if(action_temp > 4):
                    action_temp = action_temp - 4
                    return action_temp
            elif(temp4 == 2):
                action_temp = action+3
                if(action_temp > 4):
                    action_temp = action_temp - 4
                    return action_temp


###########################################################################
#4a) compute value iteration, again returning
# optimal policy π∗ with optimal valueV ∗.
###########################################################################
    def value_iteration(self, gamma):
        begin = time.time()
        self.initialize_value_matrix()
        delta = 0.2      
        while(delta >= 0.1):
            delta = 0
            for i in range(ROW_NUM):
                 for j in range(COL_NUM):
                     value = self.value_matrix[i][j]
                     curr_state = self.state_space.state2Darray[i][j]
                     vprev = -1000
                     optAct = 0
                     for action in range(ACT_SPACE):     
                          vnext = self.getSum(curr_state,action,gamma)
                          if(vnext > vprev):
                              vprev=vnext
                              optAct = action
                     self.value_matrix[i][j] = vprev
                     self.policy_matrix[i][j] =optAct
                     delta = max(delta,abs(value - vprev))   
        end = time.time()
        timedelta = end-begin
        print('time for value-iteration: ', timedelta)



######################################################
# TESTING FUNCTIONALITY                              #
######################################################

######################################################
# Initialize world                                   #
######################################################
perror = 0.01 #probability error
gamma = 0.9 #discount
#list of coordinates where obstacles will exist
obstacles = [(3,1),(3,2),(1,1),(1,2)]
#3a, initizlize grid world
world = gridWorld(COL_NUM,ROW_NUM,perror)
#set obstacles
for obs in obstacles:
    world.state_space.setObs(obs[0],obs[1],1)
#set the rewards in grid
rewards = [(5,4,-100),(4,4,-100),(3,4,-100),(2,4,-100),(1,4,-100),(0,4,-100),(2,2,1),
           (0,2,10)]
for r in rewards:
    world.state_space.setStateReward(r[0],r[1],r[2])
#printing the board
print("PRINTING THE GRID WORLD")
print("Policy with discount = ",gamma,", perror = ",perror)
world.state_space.printAll()


#grid.
#testing probability checking
state = oneState(4,2,0)
state2 = oneState(3,2,0)
prb = [0] * ACT_SPACE

for i in range(0,ACT_SPACE):
    action = robotAction(i)
    prb[i] = to_Next_State_Prob(action, state, 0.4, state2)
print(prb)

#3b testing populating matrices and displaying
print("PRINTING INITIAL POLICY MATRIX")
world.display_policy_matrix(world.policy_matrix)

#3c calculate value matrix test
print("Evaluating the initial policy")
world.evaluatePolicy(world.policy_matrix, gamma)
world.display_value_matrix()

#3d && #3e
print("COMPUTING OPTIMAL POLICY VIA POLICY ITERATION")
world.policyIteration(gamma)
#world.display_policy_matrix()

#3g
print("PRINTING AN ARRAY THAT SHOWS THE MOVEMENTS OF BOTH AN IDEAL TRAJECTORY\n",
      "AND ONE THAT IS NON-IDEAL AND ACCOUNTS FOR ERROR IN MOVEMENT, ALSO\n",
      "DISPLAYS DISCOUNTED REWARD FOR IDEAL TRAJECTORY AND\n",
      "DISCOUNTED SUM OF REWARDS FOR EXPECTED TRAJECTORY")
world.plot_trajectory( 2, 5, 0.9)


#4a,4b,4c evaluating value iteration
#reseting policy matrix back to all LEFT
print("\nCOMPUTING OPTIMAL POLICY VIA VALUE ITERATION AND DISPLAYING IS TRAJECTORY")
world.policy_matrix = world.policyMatrix()
world.value_iteration(gamma)
world.display_policy_matrix(world.policy_matrix)
world.plot_trajectory(2,5,gamma)


#5a setting up a new world to evaluate
print("\nEVALUATING OPTIMAL POLICIES FOR WORLDS WITH NEW ERROR AND DISCOUNT VALUES")

gamma2 = 0.9
perror2 = 0.2
print("\nPolicy with discount = ",gamma2,", perror = ",perror2)
world2 = gridWorld(COL_NUM,ROW_NUM,perror2)
for r in rewards:
    world2.state_space.setStateReward(r[0],r[1],r[2])
world2.policyIteration(gamma2)
world2.display_policy_matrix(world2.policy_matrix)

gamma3 = 0.9
perror3 = 0.4
print("\nPolicy with discount = ",gamma3,", perror = ",perror3)
world3 = gridWorld(COL_NUM,ROW_NUM,perror3)
for r in rewards:
    world3.state_space.setStateReward(r[0],r[1],r[2])
world3.policyIteration(gamma3)
world3.display_policy_matrix(world3.policy_matrix)

