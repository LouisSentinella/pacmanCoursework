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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='5'):
        self.index = 0 # Pacman is always agent index 0
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

        for i in (gameState.getLegalActions(0)):
            gameStateList.append([[i, gameState.generateSuccessor(0, i)],[]])



        for i in gameStateList:
            for j in i[0][1].getLegalActions():
                i[1].append([[j, i[0][1].generateSuccessor(0,j)], []])

        #print(gameStateList)

        for i in gameStateList:
            for j in i[1]:
                for k in j[0][1].getLegalActions():
                    j[1].append([[k, j[0][1].generateSuccessor(0, k)], []])

        for i in gameStateList:
            for j in i[1]:
                for k in j[1]:
                    for l in k[0][1].getLegalActions():
                        k[1].append([[l, k[0][1].generateSuccessor(0, l)], []])

        for i in gameStateList:
            for j in i[1]:
                for k in j[1]:
                    for l in k[1]:
                        for m in l[0][1].getLegalActions():
                            l[1].append([[m, l[0][1].generateSuccessor(0, m)], []])

        for i in gameStateList:
            for j in i[1]:
                for k in j[1]:
                    for l in k[1]:
                        for m in l[1]:
                            for n in m[0][1].getLegalActions():
                                m[1].append([[n, m[0][1].generateSuccessor(0, n)], []])

        for i in gameStateList:
            for j in i[1]:
                for k in j[1]:
                    for l in k[1]:
                        for m in l[1]:
                            for n in m[1]:
                                for o in n[0][1].getLegalActions():

                                    n[1].append([[o, n[0][1].generateSuccessor(0, o)], []])

        for i in gameStateList:
            for j in i[1]:
                for k in j[1]:
                    for l in k[1]:
                        for m in l[1]:
                            for n in m[1]:
                                for o in n[1]:
                                    for p in o[0][1].getLegalActions():

                                        o[1].append([[p,o[0][1].generateSuccessor(0, p)], []])

        #print(gameStateList)

        bestI = []
        bestIScore = -100000000000


        for i in gameStateList:

            worstJ = []
            worstJScore = 100000000000

            for j in i[1]:
                bestK = []
                bestKScore = -100000000000

                for k in j[1]:

                    worst = []
                    worstL = 10000000000

                    for l in k[1]:

                        best = []
                        bestScore = -10000000000

                        for m in l[1]:

                            worstN = []
                            worstNScore = 1000000000000000

                            for n in m[1]:

                                bestO = []
                                bestOScore = -100000000000

                                for o in n[1]:

                                    worstP = []
                                    worstPScore = 100000000000

                                    for p in o[1]:
                                        if p[0][1].getScore() < worstPScore:
                                            worstP = p[0]
                                            worstPScore = p[0][1].getScore()

                                    o[1] = [worstP, worstPScore]

                                    if o[0][1].getScore() > bestOScore:
                                        bestO = o[0]
                                        bestOScore = o[0][1].getScore()

                                n[1] = [bestO, bestOScore]

                                if n[0][1].getScore() < worstNScore:
                                    worstN = n[0]
                                    worstNScore = n[0][1].getScore()

                            m[1] = [worstN, worstNScore]

                            if m[0][1].getScore() > bestScore:
                                best = m[0]
                                bestScore = m[0][1].getScore()

                        l[1]  = [best, bestScore]

                        if l[0][1].getScore() < worstL:
                            worst = l[0]
                            worstL = l[0][1].getScore()
                    k[1] = [worst, worstL]

                    if k[0][1].getScore() > bestKScore:
                        bestK = k[0]
                        bestKScore = k[0][1].getScore()

                j[1] = [bestK, bestKScore]

                if j[0][1].getScore() < worstJScore:
                    worstJ = j[0]
                    worstJScore = j[0][1].getScore()

            i[1] = [worstJ, worstJScore]

            if i[0][1].getScore() > bestIScore:
                bestI = i[0]
                bestIScore = i[0][1].getScore()

        if bestI[0] == "Stop":
            return(random.choice(gameStateList)[0][0])
        return bestI[0]


class MaxAgent(AdversarialSearchAgent):
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

        for i in (gameState.getLegalActions(0)):
            gameStateList.append([[i, gameState.generateSuccessor(0, i)],[]])



        for i in gameStateList:
            for j in i[0][1].getLegalActions():
                i[1].append([[j, i[0][1].generateSuccessor(0,j)], []])

        #print(gameStateList)

        for i in gameStateList:
            for j in i[1]:
                for k in j[0][1].getLegalActions():
                    j[1].append([[k, j[0][1].generateSuccessor(0, k)], []])

        for i in gameStateList:
            for j in i[1]:
                for k in j[1]:
                    for l in k[0][1].getLegalActions():
                        k[1].append([[l, k[0][1].generateSuccessor(0, l)], []])

        for i in gameStateList:
            for j in i[1]:
                for k in j[1]:
                    for l in k[1]:
                        for m in l[0][1].getLegalActions():
                            l[1].append([[m, l[0][1].generateSuccessor(0, m)], []])

        #print(gameStateList)

        bestI = []
        bestIScore = -100000000000


        for i in gameStateList:

            bestJ = []
            bestJScore = -100000000000

            for j in i[1]:
                bestK = []
                bestKScore = -100000000000

                for k in j[1]:

                    bestL = []
                    bestLScore = -10000000000

                    for l in k[1]:

                        best = []
                        bestScore = -10000000000

                        for m in l[1]:


                            if m[0][1].getScore() > bestScore:
                                best = m[0]
                                bestScore = m[0][1].getScore()

                        l[1]  = [best, bestScore]

                        if l[0][1].getScore() > bestLScore:
                            bestL = l[0]
                            bestLScore = l[0][1].getScore()
                    k[1] = [bestL, bestLScore]

                    if k[0][1].getScore() > bestKScore:
                        bestK = k[0]
                        bestKScore = k[0][1].getScore()

                j[1] = [bestK, bestKScore]

                if j[0][1].getScore() > bestJScore:
                    bestJ = j[0]
                    bestJScore = j[0][1].getScore()

            i[1] = [bestJ, bestJScore]

            if i[0][1].getScore() > bestIScore:
                bestI = i[0]
                bestIScore = i[0][1].getScore()

        if bestI[0] == "Stop":
            return(random.choice(gameStateList)[0][0])
        return bestI[0]


class AlphaBetaAgent(AdversarialSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax with alpha-beta pruning action using self.depth and
        self.evaluationFunction
        """
        # John is a punk
        # John = cool kid
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
    # Testy cunt

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 3).

    DESCRIPTION: <write something here so we know what you did>
    """

    "*** YOUR CODE HERE ***"

    isLouisCool = True
    util.raiseNotDefined()


