# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp
import util

from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()
        # print("AFTER RUNVAL")
        # print(mdp.getStates())

    # Project3 Q1
    def runValueIteration(self):

        # Get MDP States
        states = self.mdp.getStates()
        for i in range(self.iterations):
            vals = self.values.copy()
            for state in states:
                # Check if state is an end state
                if not self.mdp.isTerminal(state):
                    action = self.getAction(state)
                    vals[state] = self.computeQValueFromValues(state, action)
            # update mdp values to updated values with terminal state.
            self.values = vals

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    # Project3 Q1
    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """

        # Initialize q to 0 and find new Q value from Transition States and their Weights
        q = 0
        for tState in self.mdp.getTransitionStatesAndProbs(state, action):
            q += tState[1] * (self.mdp.getReward(state, action,
                              tState[0]) + self.discount * self.values[tState[0]])
        return q

    # Project3 Q1
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """

        # Catch case where state is a terminal/end state, where no actions left. [As noted in Document]
        if self.mdp.isTerminal(state):
            return None  # end case.

        # Scan all posssible actions from the state, find max value action.
        actionValues = util.Counter()  # Using util.Counter() to initialize empty dict
        for action in self.mdp.getPossibleActions(state):
            actionValues[action] = self.computeQValueFromValues(state, action)
        return actionValues.argMax()  # find optimal action from Q values.

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

# Project3 Q4
class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        # Get MDP States
        states = self.mdp.getStates()

        # Scan each iteration, and update state
        for i in range(self.iterations):
            vals = self.values.copy()
            state = states[i % len(states)]
            # Check if state is an end state
            if not self.mdp.isTerminal(state):
                action = self.getAction(state)
                vals[state] = self.computeQValueFromValues(state, action)
            # update mdp values to updated values with terminal state.
            self.values = vals

# Project3 Q5
class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """

    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        # Initialize empty dict with sets for each state in MDP
        predecessors = {}
        for state in self.mdp.getStates():
            predecessors[state] = set([])

        # For each state in MDP, fill predecessors dict and build priorityQueue in order
        pq = util.PriorityQueue()
        for prevState in self.mdp.getStates():
            qValue = -float("inf")
            # For each action, checks current and previous action, comparing qValues, keeps max
            for action in self.mdp.getPossibleActions(prevState):
                qValue = max(qValue, self.getQValue(prevState, action))
                for nextState, prob in self.mdp.getTransitionStatesAndProbs(prevState, action):
                    predecessors[nextState].add(prevState)
            if not self.mdp.isTerminal(prevState):
                diff = abs(qValue - self.getValue(prevState))
                pq.push(prevState, -1 * diff)

        for k in range(self.iterations):
            if pq.isEmpty():
                break

            state = pq.pop() # pulls current state, check if not Terminal, will then find qValue
            if not self.mdp.isTerminal(state):
                actions = self.mdp.getPossibleActions(state)
                value = -float("inf")
                for action in actions: # find max Qvalue
                    value = max(value, self.getQValue(state, action))

                # Update value in pririty queue with correct qValue.
                self.values[state] = value
                for state in predecessors[state]:
                    qValue = max([self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)])
                    diff = abs(qValue - self.getValue(state))
                    if diff > self.theta:
                        pq.update(state, -1*diff)