# adversarialAgents.py
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
#
# Modified for use at University of Bath.
from math import inf

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    """

    def getAction(self, gameState):
        """
        getAction chooses among the best options according to the evaluation
        function.

        getAction takes a GameState and returns some Directions.X
        for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action)
                  for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores))
                       if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are
        better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class AdversarialSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    adversarial searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent and AlphaBetaPacmanAgent.

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


class MinimaxAgent(AdversarialSearchAgent):
    """
    Your minimax agent (question 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing
        minimax.

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

        "*** YOUR CODE HERE ***"

        gameStateList = []

        # Generates the first nodes for minimax
        for i in (gameState.getLegalActions(0)):
            gameStateList.append([[i, gameState.generateSuccessor(0, i)], []])

        for i in gameStateList:
            # Generates all of the nodes for the minimax function
            i = self.expandNode(i, 1, gameState, 1)


        # Initialise values in order to start minimax search
        bestScore = -100000000000000
        bestMove = ""
        resultsList = []
        bestResultsList = []
        numAgents = gameState.getNumAgents()
        # Loops through the top three choices, and performs minimax on each of them. Chooses best of choices once
        # minimax is performed because player will always be last and will always choose max
        for i in gameStateList:
            result = self.miniMax(i, (self.depth * numAgents) - 1)
            resultsList.append([i[0][0], result])
            if result[1] > bestScore:
                # We have disallowed pacman to stop in order to remain true to real pacman, in which the player also
                # cannot stop.
                if i[0][0] == "Stop":
                    pass
                else:
                    bestMove = i[0][0]
                    bestScore = result[1]
        # If there are multiple ones with the same score add them to a list
        for i in resultsList:
            if i[1][1] == bestScore and i[0] != "Stop":
                bestResultsList.append(i[0])
        # and choose one at random
        if len(bestResultsList) > 1:
            return random.choice(bestResultsList)

        return bestMove

    # Recursively checks the values given by the evaluation function on each node, returning the appropriate node
    # depending on whether it is max or min we did not realise we could just copy the pseudocode for this part of our
    # program, so as you can see, it's a bit of a mess. But despite this, from our brief testing, our minimax
    # algorithm actually outperforms the one that is just a direct copy of the pseudocode with the added benefit that
    # we developed this ourselves without using the pseudocode.
    def miniMax(self, node, depth):
        numAgents = node[0][1].getNumAgents()
        # this is how we handle whether its  a min or  a max
        if numAgents == 3:
            minmaxlist = ["Min", "Min", "Max"] * (((self.depth * numAgents) // numAgents) + 1)
        elif numAgents == 2:
            minmaxlist = ["Min", "Max"] * (((self.depth * numAgents) // numAgents) + 1)

        if depth == 0:
            return [node[0][1], node[0][1].getScore()]
        # just typical minimax
        elif minmaxlist[(self.depth * numAgents) - 1 - depth] == "Min":
            minScore = 1000000
            minList = []
            minNode = None
            for i in node[1]:
                minList.append(self.miniMax(i, depth - 1))
            for i in minList:
                if i[1] < minScore:
                    minScore = i[1]
                    minNode = i[0]
            if minNode == None:
                pass
            return [minNode, minScore]
        elif minmaxlist[(self.depth * numAgents) - 1 - depth] == "Max":
            maxScore = -10000000000000
            maxList = []
            maxNode = None
            for i in node[1]:
                maxList.append(self.miniMax(i, depth - 1))

            for i in maxList:
                if i[1] > maxScore:
                    maxScore = i[1]
                    maxNode = i[0]

            return [maxNode, maxScore]

    # Recursively expands all of the nodes and places them into a tree to be used in the minimax function
    def expandNode(self, nodeToBeExpanded, depth, gameState, agent):
        if agent > (gameState.getNumAgents() - 1):
            agent = 0
        depth += 1
        for i in nodeToBeExpanded[0][1].getLegalActions(agent):
            nodeToBeExpanded[1].append([[i, nodeToBeExpanded[0][1].generateSuccessor(agent, i)], []])
        if nodeToBeExpanded[0][1].getLegalActions(agent) == []:
            nodeToBeExpanded[1].append([["Stop", nodeToBeExpanded[0][1]], []])
        if depth < (self.depth * gameState.getNumAgents()):
            for i in nodeToBeExpanded[1]:
                self.expandNode(i, depth, gameState, agent + 1)
        else:
            return nodeToBeExpanded

class AlphaBetaAgent(AdversarialSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax with alpha-beta pruning action using self.depth and
        self.evaluationFunction
        """

        "*** YOUR CODE HERE ***"

        agentNum = 0
        # The first move will always be a max, as it is pacman's move
        value, move = self.Max(gameState, float(-inf), float(inf), 0, agentNum)
        return move

    # Expands the next nodes and, if they are terminal states, finds their evaluation values then prunes accordingly
    # It then returns the node with the highest evaluation value
    def Max(self, state, alpha, beta, depth, agentNum):
        move = None
        if depth == self.depth * state.getNumAgents() or state.isWin() or state.isLose():
            return self.evaluationFunction(state), None

        value = float(-inf)

        for i in state.getLegalActions(0):
            if i != "Stop":
                value2, i2 = self.Min(state.generateSuccessor(0, i), alpha, beta, depth+1, agentNum +1)

                if value2 > value:
                    value, move = value2, i
                    alpha = max(alpha, value)
                if value > beta:
                    return value, move
        return value, move

    # Expands the next nodes and, if they are terminal states, finds their evaluation values then prunes accordingly
    # It then returns the node with the lowest evaluation value
    def Min(self, state, alpha, beta, depth, agentNum):
        move = None
        if depth == self.depth * state.getNumAgents() or state.isWin() or state.isLose():
            return self.evaluationFunction(state), None

        value = float(inf)

        for i in state.getLegalActions(agentNum):
            if i != "Stop":
                if agentNum != state.getNumAgents() - 1:
                    value2, i2 = self.Min(state.generateSuccessor(agentNum, i), alpha, beta, depth + 1, agentNum + 1)
                else:
                    value2, i2 = self.Max(state.generateSuccessor(agentNum, i), alpha, beta, depth + 1, 0)

                if value2 < value:
                    value, move = value2, i
                    beta = min(beta, value)
                if value < alpha:
                    return value, move
        return value, move


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 3).

    DESCRIPTION: We used the manhattanDistance function to find the distance of each pellet from pacman's position, and
                increased the return value if the average distance was lower, encouraging pacman to move towards clusters
                of pellets. We also added something that made it so, if a capsule was in the immediate vicinity of
                pacman, the return value would massively increase for that move, meaning pacman would always go for
                the capsule.
    """

    "*** YOUR CODE HERE ***"
    foodGrid = currentGameState.getFood()
    counter = 0
    total = 0
    returnAmount = 0

    for i in foodGrid.asList():
        counter = counter + 1
        total += manhattanDistance(i, currentGameState.getPacmanPosition())
    if counter != 0:
        average = total / counter

        returnAmount = 1 / average
        returnAmount *= 100

    if currentGameState.getGhostState(1).scaredTimer == 38:
        returnAmount += 100


    return  returnAmount + currentGameState.getScore()
