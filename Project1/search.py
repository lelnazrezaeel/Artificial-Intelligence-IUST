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
from game import Directions

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

def dfs_helper(problem, state, visited, route):
    visited.append(state[0])
    route.push(state[1])
    if problem.isGoalState(state[0]):
        return True
    for child in problem.getSuccessors(state[0]):
        if child[0] not in visited:
            if dfs_helper(problem, child, visited, route):
                return True
    route.pop()
    return False

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
    "*** YOUR CODE HERE ***"
    route = util.Stack()
    visited = [problem.getStartState()]
    for state in problem.getSuccessors((problem.getStartState())):
        if state[0] not in visited:
            if dfs_helper(problem, state, visited, route):
                return route.list

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    routes = util.Queue()
    routes.push([])
    queue = util.Queue()
    visited = []
    queue.push((problem.getStartState(), None, None))
    while not queue.isEmpty():
        state = queue.pop()
        route = routes.pop()
        if state[1] == None:
            visited.append(state[0])
        if problem.isGoalState(state[0]):
            return route
        for child in problem.getSuccessors(state[0]):
            if child[0] not in visited:
                queue.push(child)
                visited.append(child[0])                
                routes.push((route + [child[1]]))


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    queue = util.PriorityQueue()
    visited = []
    queue.push([(problem.getStartState(), None, 0)], 0)
    while not queue.isEmpty():
        routeToNewState = queue.pop()
        if routeToNewState[-1][1] == None:
            visited.append(routeToNewState[-1][0])
        if problem.isGoalState(routeToNewState[-1][0]):
            return list(map(lambda state: state[1], routeToNewState[1:]))
        for child in problem.getSuccessors(routeToNewState[-1][0]):
            if child[0] not in visited:
                queue.push(routeToNewState + [child], sum(map(lambda state: state[2], routeToNewState )) + child[2])
                if not problem.isGoalState(child[0]):
                  visited.append(child[0])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    queue = util.PriorityQueue()
    visited = []
    queue.push([(problem.getStartState(), None, 0)], 0)
    while not queue.isEmpty():
        routeToNewState = queue.pop()
        if routeToNewState[-1][1] == None:
            visited.append(routeToNewState[-1][0])
        if problem.isGoalState(routeToNewState[-1][0]):
            return list(map(lambda state: state[1], routeToNewState[1:]))
        for child in problem.getSuccessors(routeToNewState[-1][0]):
            if child[0] not in visited:
                queue.push(routeToNewState + [child], sum(map(lambda state: state[2], routeToNewState )) + child[2] + heuristic(child[0], problem))
                if not problem.isGoalState(child[0]):
                  visited.append(child[0])



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
