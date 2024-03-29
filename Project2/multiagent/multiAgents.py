# multiAgents.py
# --------------
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

# CMPSC442 Project2
# Taylan Unal

from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent

# Project2 Q1
class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    # Project2 Q1: Complete Evaluation Function
    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action) # Displays ASCII version of the game display
        newPos = successorGameState.getPacmanPosition() # Displays the x,y coordinates of the next pacman position
        newFood = successorGameState.getFood() # displays game board array of boolean (T/F) of food on board.
        newGhostStates = successorGameState.getGhostStates() #returns an AgentState object for each ghost.
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # if a super pellet is collected, will start a 40 frame timer, counting down by frame until ghosts are no longer scared

        # Initialize variables and lists to use in evaluation
        currentScore = scoreEvaluationFunction(currentGameState)
        foodLocations = []
        scaredGhosts = []
        activeGhosts = []
        minScared = 1000
        minActive = 1000

        food = newFood.asList()

        # Checks if the next gamestate is a win
        if successorGameState.isWin():
            # float("inf") is unbounded upper value to compare against.
            return float("inf")

        # For each food pellet, update the agent's distance from the pellet
        for i in food:  # append all food positions and keep in closestfood the one closest
            foodLocations.append(util.manhattanDistance(newPos, i))  # to pacman's position
        closestFood = min(foodLocations)

        # For each Ghost, checks agent position vs ghost position, and updates scared/active ghost lists.
        for i in newGhostStates:
            # If agent is in position of ghost, agent loses game, else continues.
            if newPos == i.getPosition():
                return -1
            else:
                if i.scaredTimer:  # If Ghost in scared state, update Ghost's distance to player.
                    scaredGhosts.append(
                        util.manhattanDistance(newPos, i.getPosition()))
                else:  # If Ghost in active state, update Ghost's distance to player.
                    activeGhosts.append(
                        util.manhattanDistance(newPos, i.getPosition()))

        if (len(scaredGhosts) > 0):  # if there are any keep the minimum distances from them
            minScared = min(scaredGhosts)

        if (len(activeGhosts) > 0):  # in any other case, keep the default values
            minActive = min(activeGhosts)

        # score found by taking current score, and the sum of the reciprocal of each factor
        score = currentScore + (1.0/closestFood) + (1.0/minScared) - (1.0/minActive) + (1.0/len(food)) + len(currentGameState.getCapsules())
        return score + successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

# Project2 Q2
class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game
        Note: Includes pacman agent AND ghost agents.

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Implement Minimax Algorithm:

        # Initialize variables and lists to use in getAction
        legalActions = gameState.getLegalActions()
        # print(legalActions)
        ghosts = gameState.getNumAgents() - 1  # all agents except pacman agent
        # print(ghosts)
        maxActions = []  # actions resulting in max utility
        score = -float("inf")  # initialize score at 0

        # Generate successor gamestates for each legal move.
        for i in legalActions:
            successor = gameState.generateSuccessor(0, i)
            tempScore = score  # save score in temp variable
            # Chooses action with highest utility
            score = max(score, self.minValue(successor, self.depth, 1, ghosts))
            if score > tempScore:
                # if the action i returns a max score, add to maxActions array.
                maxActions.append(i)

        # Return maxActions for agents to take
        while len(maxActions) != 0:
            return maxActions.pop()

    # Define maxValue function
    def maxValue(self, gameState, depth, agents):
        # Define base cases, which will end evaluation
        if(gameState.isWin() or gameState.isLose() or depth == 0):
            return self.evaluationFunction(gameState)

        score = -float("inf")
        legalActions = gameState.getLegalActions()
        # Case1, Generate successors for each legal move, keeping max score from min value of score and min value of children
        for i in legalActions:
            successor = gameState.generateSuccessor(0, i)
            # Determines best score from min value of score and min values of children
            score = max(score, self.minValue(successor, depth, 1, agents))
        return score

    # Define minValue function
    def minValue(self, gameState, depth, agents, ghosts):
        # Define base cases, which will end evaluation
        if(gameState.isWin() or gameState.isLose() or depth == 0):
            return self.evaluationFunction(gameState)
        score = float("inf")
        legalActions = gameState.getLegalActions(agents)

        # Case1, where only agent playing is Pacman. (base)
        if agents == ghosts:
            for i in legalActions:
                successor = gameState.generateSuccessor(agents, i)
                # Determines best score from min value of score and max values of children
                score = min(score, self.maxValue(
                    successor, depth-1, ghosts))
        # Case2, where ghosts are playing alongside Pacman
        else:
            for i in legalActions:
                successor = gameState.generateSuccessor(agents, i)
                # Determines best score from min value of score and min values of children
                score = min(score, self.minValue(
                    successor, depth, agents+1, ghosts))
        # Return best score determined by maxValue function
        return score

# Project2 Q3
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    # Implement AlphaBetaAgent, refer to Lecture7 Minimax Search pg35 or Project Document

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        # Initialize variables and lists to use in getAction
        legalActions = gameState.getLegalActions()
        ghosts = gameState.getNumAgents() - 1  # all agents except pacman agent
        maxActions = []  # actions resulting in max utility
        score = -float("inf")  # initialize score, a, b at neg infinity for comparison
        alpha = -float("inf")
        beta = float("inf")

        # Generate successor gamestates for each legal move.
        for i in legalActions:
            successors=gameState.generateSuccessor(0,i)
            temp=score
            # Score calculated by taking max of min child vals.
            score=max(score, self.minAlphaBeta(successors, self.depth, 1, ghosts, alpha, beta))

            # Store and save actions with max utility
            if score>temp:
                maxActions.append(i)

            if score>beta:
                return score
            alpha=max(alpha, score)

        # Return all maxactions. each value
        while len(maxActions) != 0: # or !=0
            return maxActions.pop()

    def maxAlphaBeta(self, gameState, depth, ghosts, alpha, beta):
        # Initialize score and legalActions to test
        v = -float("inf") # Slides/Project document refer to score as v. Score == v == -inf
        legalActions=gameState.getLegalActions(0)

        # Base/End case
        if gameState.isWin() or gameState.isLose() or depth==0:
            return self.evaluationFunction(gameState)

        for i in legalActions:
            successor=gameState.generateSuccessor(0,i)
            v=max(v, self.minAlphaBeta(successor, depth, 1, ghosts, alpha, beta))
            if v>beta:
                return v
            alpha=max(alpha, v)
        return v

    def minAlphaBeta(self, gameState, depth, agents, ghosts, alpha, beta):
        # Initialize score and legalActions to test
        v=float("inf")
        legalActions=gameState.getLegalActions(agents)

        # Base/End case
        if gameState.isWin() or gameState.isLose() or depth==0:
            return self.evaluationFunction(gameState)

        if agents==ghosts:
            for i in legalActions:
                successors=gameState.generateSuccessor(agents, i)
                v=min(v, self.maxAlphaBeta(successors, depth-1, ghosts, alpha, beta))
                if v<alpha:                                                                 #return-start recursion backwards
                    return v
                beta=min(beta, v)
        else:
            for i in legalActions:
                successors=gameState.generateSuccessor(agents, i)
                v=min(v, self.minAlphaBeta(successors, depth, agents+1, ghosts, alpha, beta))
                if v<alpha:
                    break
                beta=min(beta, v)
        return v



#Project2 Q4
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Initialize variables and lists to use in getAction
        legalActions = gameState.getLegalActions()
        ghosts = gameState.getNumAgents() - 1  # all agents except pacman agent
        maxActions = []  # actions resulting in max utility
        score = -float("inf")  # initialize score at 0

        #Generate Successors for each legalAction
        for i in legalActions:
            successors = gameState.generateSuccessor(0,i)
            temp = score
            score=max(score, self.expectiMin(successors, self.depth, 1, ghosts))
            if score > temp:
                maxActions.append(i)
        while len(maxActions)!=0:
            return maxActions.pop()

    # Define ExpectiMax helper function to find max nodes
    def expectiMax(self, gameState, depth, ghosts):
        score=-(float("inf"))
        legalActions=gameState.getLegalActions(0)

        # Base/End case
        if gameState.isWin() or gameState.isLose() or depth==0:
            return self.evaluationFunction(gameState)


        for i in legalActions:
            successors=gameState.generateSuccessor(0,i)
            score=max(score,self.expectiMin(successors,depth,1,ghosts))
        return score

    # Define ExpectiMax helper function to find max nodes
    def expectiMin(self,gameState, depth, agents, ghosts):
        score = 0
        legalActions=gameState.getLegalActions(agents)


        if gameState.isWin() or gameState.isLose() or depth==0:
            return self.evaluationFunction(gameState)
        if agents==ghosts:
            for i in legalActions:
                successors=gameState.generateSuccessor(agents, i)
                score+=self.expectiMax(successors,depth-1,ghosts)

        else:
            for i in legalActions:
                successors=gameState.generateSuccessor(agents, i)
                score+=self.expectiMin(successors, depth, agents + 1, ghosts)
        return score

#Project2 Q5
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    In this evaluation function, to improve
    """
    currPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    currScore=scoreEvaluationFunction(currentGameState)
    food=[]
    f=[]
    foodLocations=[]
    scaredGhosts=[]
    activeGhosts=[]
    minScared=1000
    minActive=1000

    food=newFood.asList()

    # Base/End Cases
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return -float("inf")
    closestfood = float("inf")

    for i in food:
        f.append(util.manhattanDistance(i, currPos))
    temp = min(f)                                      #calculate position of closest food piece
    if temp<closestfood:
        closestfood=temp
    foodLocations.append(closestfood)

    # Pops top of stack, or closest food location.
    f=foodLocations.pop()

    # Iterate through each ghost state
    for i in newGhostStates:
        # Base/End Case, if Pacman position is on top of ghost position, return error
        if currPos==i.getPosition():
            return -1
        else:
            # Update positions of ghosts
            if i.scaredTimer:
                scaredGhosts.append(util.manhattanDistance(currPos, i.getPosition()))
            else:
                activeGhosts.append(util.manhattanDistance(currPos, i.getPosition()))
    if len(scaredGhosts):
        minScared=min(scaredGhosts)
    if len(activeGhosts):
        minActive=min(activeGhosts)

    endScore = currScore - (0.5*f) - (0.5*minScared)+(5.0*minActive)-(0.5*len(food)) - (0.5*len(currentGameState.getCapsules()))
    return endScore