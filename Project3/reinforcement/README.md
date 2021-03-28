## Taylan Unal CMPSC442-AI SP21
## Project 3: Multi-Agent Search, Due Sunday 2/21 at 11:59pm

### Files to Read:
mdp.py
learningAgents.py

### Files to Edit:
valueIterationAgents.py
qlearningAgents.py
analysis.py

## Activate Conda Environment
1. conda create --name <env-name> python=3.6
2. source activate <env-name>
If you run python -V, should see Python 3.6.x

## Leaving Conda Environment
1. source deactivate
If you run python -V, should see Python 3.6.x

## COMMANDS TO RUN:
### Run Gridworld in manual control:
python gridworld.py -m

### View Options:
python gridworld.py -m

## Question 1:
python autograder.py -q q1
python gridworld.py -a value -i 100 -k 10
python gridworld.py -a value -i 5

## Question 2:
python gridworld.py -a value -i 100 -g BridgeGrid --discount 0.9 --noise 0.2

#### MDP FUNCTIONS DEFINED:
mdp.getStates()
    """
    Return a list of all states in the MDP.
    Not generally possible for large MDPs.
    """

mdp.getPossibleActions(state)
    """
    Return list of possible actions from 'state'.
    """

mdp.getTransitionStatesAndProbs(state, action)
    """
    Returns list of (nextState, prob) pairs
    representing the states reachable
    from 'state' by taking 'action' along
    with their transition probabilities.

    Note that in Q-Learning and reinforcment
    learning in general, we do not know these
    probabilities nor do we directly model them.
    """

mdp.getReward(state, action, nextState)
    """
    Get the reward for the state, action, nextState transition.
    Not available in reinforcement learning.
    """

mdp.isTerminal(state)
    """
    Returns true if the current state is a terminal state.  By convention,
    a terminal state has zero future rewards.  Sometimes the terminal state(s)
    may have no possible actions.  It is also common to think of the terminal
    state as having a self-loop action 'pass' with zero reward; the formulations
    are equivalent.
    """