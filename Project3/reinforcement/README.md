## Taylan Unal CMPSC442-AI SP21
## Project 3: Multi-Agent Search, Due Sunday 2/21 at 11:59pm

### Files to Read:
mdp.py
learningAgents.py

### Files to Edit:
valueIterationAgents.py
qlearningAgents.py
analysis.py

# TODO:
- Q5*

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

## Question 3:
python autograder.py -q q3

## Question 4:
python autograder.py -q q4
python gridworld.py -a asynchvalue -i 1000 -k 10

## Question 5:
python autograder.py -q q5
python gridworld.py -a priosweepvalue -i 1000

## Question6:
python autograder.py -q q6
python gridworld.py -a q -k 5 -m

## Question7:
python gridworld.py -a q -k 100
python gridworld.py -a q -k 100 --noise 0.0 -e 0.1
python gridworld.py -a q -k 100 --noise 0.0 -e 0.9
python autograder.py -q q7
python crawler.py

## Question8:
python gridworld.py -a q -k 50 -n 0 -g BridgeGrid -e 1
python autograder.py -q q8

## Question9:
python pacman.py -p PacmanQAgent -x 2000 -n 2010 -l smallGrid
python autograder.py -q q9

## Question10:
python pacman.py -p ApproximateQAgent -x 2000 -n 2010 -l smallGrid
python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumGrid
python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic
python autograder.py -q q10

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