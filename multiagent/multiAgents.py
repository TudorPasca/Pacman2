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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPositions = [ghostState.getPosition() for ghostState in newGhostStates]
        if isGhostClose(newPos, newGhostPositions):
            return -1e9
        foodList = newFood.asList()
        if len(foodList) == 0:
            return 1e9
        return 1 / getMinFoodDist(newPos, foodList) + 10000 / len(foodList)

def isGhostClose(pos, ghostPositions):
    for ghostPos in ghostPositions:
        if manhattanDistance(pos, ghostPos) < 2:
            return True
    return False

def getMinFoodDist(pos, foodList):
    return min([manhattanDistance(pos, food) for food in foodList])

def getClosestFood(pos, foodList):
    distance = 1e9
    for food in foodList:
        distance = min(distance, manhattanDistance(pos, food))
    return distance

def scoreEvaluationFunction(currentGameState: GameState):
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


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def minVal(self, gameState, agentId, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return None, self.evaluationFunction(gameState)
        mn = float('inf')
        a = None
        for action in gameState.getLegalActions(agentId):
            nextState = gameState.generateSuccessor(agentId, action)
            val = float('inf')
            if (agentId + 1 == gameState.getNumAgents()):
                _, val = self.maxVal(nextState, 0, depth + 1)
            else:
                _, val = self.minVal(nextState, agentId + 1, depth)
            if val < mn:
                mn = val
                a = action
        return a, mn

    def maxVal(self, gameState, agentId, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return None, self.evaluationFunction(gameState)
        mx = - float('inf')
        a = None
        for action in gameState.getLegalActions(agentId):
            nextState = gameState.generateSuccessor(agentId, action)
            val = - float('inf')
            if (agentId + 1 == gameState.getNumAgents()):
                _, val = self.maxVal(nextState, 0, depth + 1)
            else:
                _, val = self.minVal(nextState, agentId + 1, depth)
            if val > mx:
                mx = val
                a = action
        return a, mx

    def minmax(self, gameState, agentId=0, depth=0):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        action, _ = self.maxVal(gameState, 0, 0)
        return action

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        return self.minmax(gameState, agentId=0, depth=0)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def minVal(self, gameState, agentId, depth, alpha, betha):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return None, self.evaluationFunction(gameState)
        mn = float('inf')
        a = None
        for action in gameState.getLegalActions(agentId):
            nextState = gameState.generateSuccessor(agentId, action)
            val = float('inf')
            if (agentId + 1 == gameState.getNumAgents()):
                _, val = self.maxVal(nextState, 0, depth + 1, alpha, betha)
            else:
                _, val = self.minVal(nextState, agentId + 1, depth, alpha, betha)
            if val < mn:
                mn = val
                a = action
            if mn < alpha:
                return a, mn
            betha = min(betha, mn)
        return a, mn

    def maxVal(self, gameState, agentId, depth, alpha, betha):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return None, self.evaluationFunction(gameState)
        mx = - float('inf')
        a = None
        for action in gameState.getLegalActions(agentId):
            nextState = gameState.generateSuccessor(agentId, action)
            val = - float('inf')
            if (agentId + 1 == gameState.getNumAgents()):
                _, val = self.maxVal(nextState, 0, depth + 1, alpha, betha)
            else:
                _, val = self.minVal(nextState, agentId + 1, depth, alpha, betha)

            if val > mx:
                mx = val
                a = action
            if mx > betha:
                return a, mx
            alpha = max(alpha, mx)
        return a, mx

    def alphaBetha(self, gameState, agentId=0, depth=0):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        action, _ = self.maxVal(gameState, 0, 0, - float("inf"), float("inf"))
        return action
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBetha(gameState, agentId=0, depth=0)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
