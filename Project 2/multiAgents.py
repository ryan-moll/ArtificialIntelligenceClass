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
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()

        #print("\n__________\ncurrentGameState:\n", currentGameState, "\nsuccessorGameState:\n", successorGameState, sep='')
        x = 0
        y = 0
        foodCount = 0
        closestFood = [(-1,-1), -1]
        for food in newFood.asList(): # (game.py 172/273)
            foodDist = abs(newPos[0]-food[0])+abs(newPos[1]-food[1])
            if foodCount is 0:
                #print(food)
                closestFood[0] = food
                closestFood[1] = foodDist
                foodCount += 1
                continue
            if foodDist < closestFood[1]:
                closestFood[0] = food
                closestFood[1] = foodDist
            foodCount += 1
            #print("food[x]: ", food)
        #print(closestFood)
        if not closestFood[1]:
            f = float(2)
        else:
            f = float(1/closestFood[1])


        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #print(newGhostStates)
        # for ghost in newGhostStates:
        #     print(getGhostPosition)
        ghostDistance = 0
        for ghost in successorGameState.getGhostPositions(): #(pacman.py 61/170)
            curGhostDistance = abs(newPos[0]-ghost[0])+abs(newPos[1]-ghost[1])
            # print(curGhostDistance)
            ghostDistance += curGhostDistance
            #print(ghost)
        if not ghostDistance:
            g = float(5)
        else:
            g = float(1/ghostDistance)

        return successorGameState.getScore() + f - g

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        #print(gameState.getLegalActions(0)) # legal actions for pacman
        def minimax(s, d, a): # s=state d=depthlevel a=agentnumber
            # print("depth: ", d, " agent: ", a, " s.state: ", s.state)
            if s.isWin() or s.isLose() or d == self.depth:
                # print("State: ", s.state)
                return self.evaluationFunction(s) #(54 defined by me)
            elif a == 0: #agent is pacman
                # print("Pacman!")
                actionCosts = []
                # print("Max- Legal actions: ", s.getLegalActions(0))
                for action in s.getLegalActions(0):
                    # print("Max: Calling minimax for action '", action, "'", sep='')
                    actionCost = minimax(s.generateSuccessor(0, action), d+1, 1)
                    actionCosts.append(actionCost)
                return max(actionCosts)
            else: #agent is a ghost
                # print("Ghost. Agent ", a)
                nxt = a + 1
                if nxt == gameState.getNumAgents():
                    nxt = 0
                    d += 1
                actionCosts = []
                # print("Min- Legal actions: ", s.getLegalActions(0))
                for action in s.getLegalActions(a):
                    # print("Min: Calling minimax for action '", action, "'", sep='')
                    actionCost = minimax(s.generateSuccessor(a, action), d, nxt)
                    actionCosts.append(actionCost)
                return min(actionCosts)



        successorStates = []
        mx = -999999
        # print("numAgents: ", gameState.problem.numAgents)
        # print("winStates: ", gameState.problem.winStates)
        # print("loseStates: ", gameState.problem.loseStates)
        # print("evaluation: ", gameState.problem.evaluation)
        # print("successors: ", gameState.problem.successors)
        # print("stateToSuccessorMap: ", gameState.problem.stateToSuccessorMap)
        # print("stateToActions: ", gameState.problem.stateToActions)
        # print("Start- Legal actions: ", gameState.getLegalActions(0))
        for action in gameState.getLegalActions(0):
            # print("Calling minimax for action: ", str(action))
            result = minimax(gameState.generateSuccessor(0, action), 0, 1)
            if result > mx:
                move = action
                mx = result

        try:
           move
        except NameError:
            Directions.NORTH

        # print("getAction returning '", move, "'", sep='')
        return move
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
