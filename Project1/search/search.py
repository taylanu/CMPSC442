# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

## Project1 Question 1
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    ## DFS uses Stack, defined in util.py
    startState = problem.getStartState() # inits state as the starty state
    visited = [] # init as empty array

    fringe = util.Stack()
    fringe.push((startState, ())) # fringe is defined as (state, heading) pairs

    while not fringe.isEmpty():
        state, heading = fringe.pop() # pulls state, heading from node

        # base/end case, where if at goal state, end game, return 
        if problem.isGoalState(state):
            return list(heading)

        # loop case, if currentstate hasnt been visited, add to visited, 
        # discover sucesssors, and generate path plan for agent
        if not state in visited:
            visited.append(state)
            paths = problem.getSuccessors(state) # defines paths possible for agent to take (eg. North,South,East,West)

            for path in paths:
                pathPlan = list(heading)
                pathPlan.append(path[1])
                
                if not path[0] in visited:
                    fringe.push((path[0], tuple(pathPlan)))

## Project1 Question 2
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    ## DFS uses Queue, defined in util.py
    startState = problem.getStartState()
    visited = [] # init as empty array

    fringe = util.Queue()
    fringe.push((startState, ())) # fringe is defined as (state, heading) pairs

    while not fringe.isEmpty():
        state, heading = fringe.pop()

        if problem.isGoalState(state):
            return list(heading)

        if not state in visited:
            visited.append(state)
            paths = problem.getSuccessors(state)

            for path in paths:
                pathPlan = list(heading)
                pathPlan.append(path[1])

                if not path[0] in visited:
                    fringe.push((path[0], tuple(pathPlan)))

## Project 1 Problem 3
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    ## DFS uses PriorityQueue, defined in util.py
    startState = problem.getStartState()
    visited = [] # init as empty array
    
    fringe = util.PriorityQueue()
    fringe.push((startState, ()), 0) # fringe node defined as ((state, direction), priority)
    # NOTE: def push(self, item, priority):

    while not fringe.isEmpty():
        state, heading = fringe.pop() 

        # base/end case, where if at goal state, end game, return 
        if problem.isGoalState(state):
            return list(heading)

        # loop case, if currentstate hasnt been visited, add to visited, 
        # discover sucesssors, and generate path plan for agent
        if not state in visited: # MAY BE ISSUE
            visited.append(state)
            paths = problem.getSuccessors(state) # defines paths possible for agent to take (eg. North,South,East,West)

            # paths references successors (not current)
            for path in paths:
                pathPlan = list(heading)
                pathPlan.append(path[1]) # path[1] references direction
                cost = problem.getCostOfActions(pathPlan)
                
                if not path[0] in visited:
                    fringe.push((path[0], tuple(pathPlan)), cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

## Project 1 Problem 4
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    ## A* Search uses PriorityQueue, defined in util.py
    startState = problem.getStartState()
    visited = [] # init as empty array

    fringe = util.PriorityQueue()
    fringe.push((startState, ()), heuristic(startState, problem)) # ((state, direction), priority) should be good
    # NOTE: push defined as push(self, item, priority). Item is the (state,direction) pair

    while not fringe.isEmpty(): # may be issue
        state, heading = fringe.pop()

        # base/end case, where if at goal state, end game, return 
        if problem.isGoalState(state):
            return list(heading)

        # loop case, if currentstate hasnt been visited, add to visited, 
        # discover sucesssors, and generate path plan for agent
        if not state in visited: 
            visited.append(state)
            paths = problem.getSuccessors(state) # defines paths possible for agent to take (eg. North,South,East,West)

            # paths references successors (not current)
            for path in paths:
                newPlan = list(heading)
                newPlan.append(path[1]) # path[2] references priority
                nextNode = ((path[0], path[1]), path[2])
                nextNode = (path[0], tuple(newPlan))
                cost = problem.getCostOfActions(newPlan) + heuristic(path[0], problem)
                
                if not path[0] in visited:
                    fringe.push(nextNode, cost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
