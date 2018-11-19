# leapFrog
Solving leap frog problem using reinforcement learning

This project let reinforcement learning algorithm learn how to play leap frog game. 
If you are not familiar with leap frog game, please refer to the link below and try it!
http://www.logicgames.com/webgames/frogjump.html

Dissimilarly to frozen lake problem or the knight and the princess game where all the states are well known before the game starts, 
we don't know the complete set of states and the feasible actions before the game starts.
So, I used a method of dynamic state and action registration method - whenever new action is found via exploitation and explorartion policy at the current state, we register this action into Action list of current state.
Subsequently the next state resulted from the new action of current state will be new state which needs to be registered to the list of state, Q-table, Reward and nextStateTable.
Q-table is updated using SARSA method.
The overall procedure is described as below.

1. initialize Q-table and Reward table
2. Repeat for the num. of episodes
3. current state = initial state
4. Repeat until current state is dead end of achieved the goal
5. Get current state
6. Choose an action via exploitation and exploration
7. Perform the selected action
8. move to next state
9. register this state into Q(s,) if it's new
10. Update Q-table (SARSA) -> go back to 4.
11. If reached the num. of episodes, the latest Q-table becomes the optimal Q.
12. animate the game play.
