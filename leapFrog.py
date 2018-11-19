"""
Leap frog problem using Reinforcement Learning
Nov. 8, 2018
@author: kwchang
"""
import random
from tkinter import *

#^^^^^^^^ UI Part ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def correctFrog(frog):
    corrFrog = []
    for i in range(2*frog+1):
        if i < frog:
            corrFrog.append('L')
        elif i == frog:
            corrFrog.append('X')
        else:
            corrFrog.append('R')
    return corrFrog


def initialState(frog):
    state = []
    for n in range(frog*2+1):
        if n <= frog - 1:
            state.append('R')
        elif n == frog:
            state.append('X')
        else:
            state.append('L')
    return state
    

def showCase(state, leftFrog, rightFrog, space, x0, y0, size, gap):
    for i in range(len(state)):
        if state[i] == 'R':
            canvas.create_image(x0, y0, image=rightFrog, anchor='sw')
        elif state[i] == 'X':
            canvas.create_image(x0, y0, image=space, anchor='sw')
        elif state[i] == 'L':
            canvas.create_image(x0, y0, image=leftFrog, anchor='sw')
        x0 = x0 + (size + gap) 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# to check if the state is dead end or able to go on
def deadEnd(state):
    dead = False
    indX = state.index('X')
    if indX == 0:
        if state[indX+1] == 'R' and state[indX+2] == 'R':
            dead = True
    elif indX == 1:
        if state[indX-1] == 'L' and state[indX+1] == 'R' and state[indX+2] == 'R':
            dead = True
    elif indX == 2*nFrog:
        if state[indX-1] == 'L' and state[indX-2] == 'L':
            dead = True
    elif indX == 2*nFrog-1:
        if state[indX+1] == 'R' and state[indX-1] == 'L' and state[indX-2] == 'L':
            dead = True
    elif (state[indX-1] == 'L' and state[indX-2] == 'L') \
    and (state[indX+1] == 'R' and state[indX+2] == 'R'):
        dead = True
    
    return dead
#----------------------------------------------------

# to check if the state is valid one or not
def checkValidState(frogId, state):
    
    validState = False
    if state[frogId] == 'R':           # the chosen frog is 'R'
        if frogId < len(state)-1 and state[frogId+1] == 'X':
            state[frogId]   = 'X'
            state[frogId+1] = 'R'
            validState = True
        elif frogId < len(state)-2 and state[frogId+2] == 'X':
            state[frogId]   = 'X'
            state[frogId+2] = 'R'
            validState = True
    else:                           # the chosen frog is 'L'
        if frogId > 0 and state[frogId-1] == 'X':
            state[frogId]   = 'X'
            state[frogId-1] = 'L'
            validState = True
        elif frogId > 1 and state[frogId-2] == 'X':
            state[frogId]   = 'X'
            state[frogId-2] = 'L'
            validState = True
            
    return validState, state
#----------------------------------------------------

# choose a frog using exploitation and exploration
def selectFrog(stateIdx, state, Q, Action):
    validState = False
    
    if Q == []:       
        while not validState:
            frogId = random.randint(0, len(state)-1)
            if state[frogId] != 'X':
                validState, nextState = checkValidState(frogId, state)
           
    else:
        if Q[stateIdx] == []:
            while not validState:
                frogId = random.randint(0, len(state)-1)
                if state[frogId] != 'X':
                    validState, nextState = checkValidState(frogId, state)
                
        else:
            dice = random.random()
            diceThres = 0.2                       
            if dice > diceThres:
                maxIdx = Q[stateIdx].index(max(Q[stateIdx]))                
                frogId = Action[stateIdx][maxIdx]
                validState, nextState = checkValidState(frogId, state)
            
            else:
                # exploration: random search for a new state we never tried before.
                maxTry = 50
                m = 0
                while not validState:
                    frogId = random.randint(0, len(state)-1)                    
                    if state[frogId] != 'X':
                        if frogId not in Action[stateIdx] or m > maxTry:                           
                            validState, nextState = checkValidState(frogId, state)

                        m += 1
                
    return frogId, nextState
#-----------------------------------------------------

#=== Game Training ===================================
def gameTraining(nFrog):
    # hyper parameters and rewards =====
    alpha = 0.2   # learning rate
    # gamma is discount fator. if 0, greedy strategy. 
    # When gamma is larger, the RL becomes more long term reward oriented. 
    # If gamma = 0, this program may be in infinite loop up and down forever.
    gamma = 0.5
    prize = 100
    penalty = -100
    onGoing = -1
    episode = 3000
    
    # to define the correct state (desirable happy ending!)
    corrState = correctFrog(nFrog)
        
    # to define the initial state: 'R', 'R', 'X', 'L', 'L' when nFrog = 2.
    state = []
    firstState = initialState(nFrog)
    state.append(firstState)
    
    Q = []             # Q-table
    Q.append([])       # state 0
    R = []             # Reward table
    R.append([])       # reward for state 0
    Action = []        # Action sequence at each state
    Action.append([])
    nextStateTable = []         # stores all the next states when an action is taken at the current state
    nextStateTable.append([])
    deadEndState = -100
    happyEndState = -1
    
    for ep in range(episode):
        currentState = state[0].copy()

        while not deadEnd(currentState):            
            currentStateIdx = state.index(currentState)
            chosenFrogId, nextState = selectFrog(currentStateIdx, currentState, Q, Action)
    
            if nextState == corrState:                             # we need to check happy end first and happy end is also a dead end case.
                print('happy end!!!!!!!!!!!!')
                if chosenFrogId not in Action[currentStateIdx]:
                    Action[currentStateIdx].append(chosenFrogId)
                    Q[currentStateIdx].append(0)                        # intialize Q-table for new action of a state.
                    R[currentStateIdx].append(prize)
                    nextStateTable[currentStateIdx].append(happyEndState)                                   
                break
            elif deadEnd(nextState):
                if chosenFrogId not in Action[currentStateIdx]:
                    Action[currentStateIdx].append(chosenFrogId)
                    Q[currentStateIdx].append(0)                    # intialize Q-table for new action of a state.
                    R[currentStateIdx].append(penalty)
                    nextStateTable[currentStateIdx].append(deadEndState)
                break
            else:
                if chosenFrogId not in Action[currentStateIdx]:
                    Action[currentStateIdx].append(chosenFrogId)
                    Q[currentStateIdx].append(0)                    # intialize Q-table for new action of a state.
                    R[currentStateIdx].append(onGoing)                
                    if nextState not in state:                             # the next state does not exist yet
                        state.append(nextState)  
                        Action.append([])                          # append Action list for new state
                        Q.append([])                               # append Q list for new state
                        R.append([])                               # append R list for new state
                        nextStateTable.append([])
                    nextStateTable[currentStateIdx].append(state.index(nextState))
                currentState = nextState.copy()
                        
        # to update Q-table using SARSA algorithm
        for m in range(len(Q)):
            for n in range(len(Q[m])):
                # calculate maxOutcome: max. expected future reward given the new state and all possible actions at that new state.                        
                if nextStateTable[m][n] >= 0:
                    nextStateIndex = nextStateTable[m][n]
                    maxOutcome = max(Q[nextStateIndex])
                else:
                    maxOutcome = 0
                Q[m][n] = Q[m][n] + alpha*(R[m][n] + gamma*maxOutcome - Q[m][n])
                
    return state, nextStateTable, Q

# Main Body -------------------------------------------------------------------------------------------------------------
maxFrog = 5   # max. allowed number of frogs
nFrog = 2
i = 1
while i < 2:
    nFrog = int(input('Enter the number of frogs (1~5): '))
    if nFrog > maxFrog or nFrog < 1:
        i = 1
    else:
        i = 2

size = 60
gap = 20
x0 = 30
y0 = 100
corrState = correctFrog(nFrog)

root = Tk()
canvas = Canvas(root, width=nFrog*170 + 100, height=160, background='white')
canvas.pack(expand=YES, fill=BOTH)
rightFrog = PhotoImage(file='RightFrog_1.png')
leftFrog = PhotoImage(file='LeftFrog_1.png')
space = PhotoImage(file='space_1.png')

# create the initial game board
showCase(initialState(nFrog), leftFrog, rightFrog, space, x0, y0, size, gap)

# execute game training!!!
text1 = canvas.create_text(100,130,fill="darkblue",font="Times 15 italic bold", \
                        text="On Training...")
canvas.update()

state = []
nextStateTable = []
Q = []
state, nextStateTable, Q = gameTraining(nFrog)

#canvas.update()
canvas.after(1000)
canvas.delete(text1)
canvas.create_text(100,130,fill="darkblue",font="Times 15 italic bold", \
                        text="Training Completed!")
canvas.update()
canvas.after(1000)

# this part below is for animating the frog's jumping actions.
m = 0   
currentState = state[m]     
while currentState != corrState:
    print(currentState)
    actionIdx = Q[m].index(max(Q[m]))
    
    # display (animation) on canvas
    canvas.delete("all")
    showCase(currentState, leftFrog, rightFrog, space, x0, y0, size, gap)
    canvas.update()
    canvas.after(1200)
    
    m = nextStateTable[m][actionIdx]   
    if m == -1:
        print(corrState)
        print('Happy End!!!!!!')
        break  
    if m == -100:
        print('Dead End!')
        break
    currentState = state[m].copy()

if m == -1:    
    canvas.delete("all")
    showCase(corrState, leftFrog, rightFrog, space, x0, y0, size, gap)
    canvas.update()
    canvas.after(1200)
    canvas.create_text(100,130,fill="red",font="Times 15 italic bold", \
                            text="Solved!")
elif m == -100:
    canvas.after(1200)
    canvas.create_text(100,130,fill="darkblue",font="Times 15 italic bold", \
                            text="Ooops!")

root.mainloop() 

