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


from webbrowser import get
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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        newx, newy = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newPacmanStates = successorGameState.getPacmanState()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newPos = successorGameState.getPacmanPosition()
        walls = currentGameState.getWalls()

        "*** YOUR CODE HERE ***"
        for pacState in newPacmanStates:
            if newPos == pacState.getWalls():
                return 10
            
def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


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
        self.goali = 0


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
        "*** YOUR CODE HERE ***"
        legal_acts: list = gameState.getLegalActions(self.index)
        print(legal_acts)

        depth = 0
        goal_i = 0
        current_state = gameState
        agent_index = 0

        print(self.min_max(current_state, agent_index, depth, True), "  ,  ")
        print(legal_acts[self.goali])

        return legal_acts[self.goali]

    def min_max(self, gameState, agent_index, depth, set_goal=False):
        num_of_agents = gameState.getNumAgents()
        if set_goal is False and agent_index == 0:
            depth += 1
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        index = 0

        t_acts = gameState.getLegalActions(agent_index)
        # max
        if agent_index == 0:
            value = -float("inf")

            for act in t_acts:
                tv = self.min_max(gameState.generateSuccessor(agent_index, act), agent_index + 1, depth)
                if set_goal and value < tv:
                    self.goali = index
                    print("goal", self.goali)

                value = max(tv, value)
                index += 1
        # min
        else:
            value = float("inf")
            for act in t_acts:
                tv = self.min_max(gameState.generateSuccessor(agent_index, act), (agent_index + 1) % num_of_agents,
                                  depth)
                value = min(tv, value)
        return value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        legal_acts: list = gameState.getLegalActions(self.index)
        print(legal_acts)

        depth = 0
        goal_i = 0
        self.goali = 0
        current_state = gameState
        agent_index = 0
        a = -float("inf")
        b = float("inf")
        self.alph_beta(current_state, agent_index, 0, a, b, True)
        # print(self.alph_beta(current_state, agent_index, depth, a, b, True), "  ,  ")
        # print(legal_acts[self.goali])

        return legal_acts[self.goali]

    def alph_beta(self, gameState, agent_index, depth, a, b, set_goal=False):
        num_of_agents = gameState.getNumAgents()
        if set_goal is False and agent_index == 0:
            print("dep ", depth)

            depth += 1
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        index = 0

        t_acts = gameState.getLegalActions(agent_index)
        # max
        if agent_index == 0:
            value = -float("inf")

            for act in t_acts:
                tv = self.alph_beta(gameState.generateSuccessor(agent_index, act), agent_index + 1, depth, a, b)
                if set_goal and value < tv:
                    self.goali = index
                    print("goal", self.goali)
                value = max(tv, value)

                if value > b and set_goal is False:
                    return value
                a = max(a, value)
                index += 1
        # min
        else:
            value = float("inf")
            for act in t_acts:
                tv = self.alph_beta(gameState.generateSuccessor(agent_index, act),
                                    (agent_index + 1) % num_of_agents, depth, a, b)
                value = min(tv, value)
                if value < a:
                    print("dep ", depth, " : exe  ", value)
                    return value
                b = min(b, value)
        return value


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
        legal_acts: list = gameState.getLegalActions(self.index)
        print(legal_acts)

        depth = 0
        goal_i = 0
        current_state = gameState
        agent_index = 0

        print(self.expc_max(current_state, agent_index, depth, True), "  ,  ")
        print(legal_acts[self.goali])

        return legal_acts[self.goali]

    def expc_max(self, gameState, agent_index, depth, set_goal=False):
        num_of_agents = gameState.getNumAgents()
        if set_goal is False and agent_index == 0:
            depth += 1
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        index = 0

        t_acts = gameState.getLegalActions(agent_index)
        # max
        if agent_index == 0:
            value = -float("inf")

            for act in t_acts:
                tv = self.expc_max(gameState.generateSuccessor(agent_index, act), agent_index + 1, depth)
                if set_goal and value < tv:
                    self.goali = index
                    print("goal", self.goali)

                value = max(tv, value)
                index += 1
        # min
        else:
            n = len(t_acts)
            value = 0.0
            for act in t_acts:
                tv = self.expc_max(gameState.generateSuccessor(agent_index, act), (agent_index + 1) % num_of_agents,
                                   depth)
                value += tv / n
        return value


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
