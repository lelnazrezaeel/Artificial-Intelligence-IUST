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


from cmath import inf
from copy import copy
from os import stat
import mdp, util

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
    def __init__(self, mdp, discount = 0.9, iterations = 100):
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
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for iteration in range(self.iterations):
            copy_val = self.values.copy()
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    continue
                copy_val[state] = self.computeQValueFromValues(state, self.computeActionFromValues(state))
            self.values = copy_val


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_value = 0
        
        for next_state, prob in self.mdp.getTransitionStatesAndProbs(state,action):
            q_value += prob * (self.mdp.getReward(state, action, next_state) + self.discount * self.values[next_state])
        
        return q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        argmax = ""
        mostValue = float('-inf')
        
        for action in self.mdp.getPossibleActions(state):
            if self.computeQValueFromValues(state, action) > mostValue :
                mostValue = self.computeQValueFromValues(state, action)
                argmax = action
        return argmax

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
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
        "*** YOUR CODE HERE ***"
        totalStates = len(self.mdp.getStates())
        for iteration in range(self.iterations):
            state = self.mdp.getStates()[iteration % totalStates]
            if self.mdp.isTerminal(state):
                continue
            self.values[state] = self.computeQValueFromValues(state, self.computeActionFromValues(state))
        

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessors = {}
        priorityQueue = util.PriorityQueue()
        #calculate predecessors of all states
        for s in self.mdp.getStates():
            if self.mdp.isTerminal(s):
                continue
            for action in self.mdp.getPossibleActions(s):
                for next_state, prob in self.mdp.getTransitionStatesAndProbs(s, action):
                    if next_state in predecessors:
                        predecessors[next_state].add(s)
                    else:
                        predecessors[next_state] = {s}
        #compute diff
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state):
                continue
            highest_Qvalue = max([self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)])
            diff = abs(highest_Qvalue - self.values[state])
            priorityQueue.push(state, -diff)
        #for iteration 0, 1 , ...
        for iteration in range(self.iterations):
            if priorityQueue.isEmpty():
                break
            
            s = priorityQueue.pop()
            
            if not self.mdp.isTerminal(s) :
                highest_Qvalue = max([self.computeQValueFromValues(s, action) for action in self.mdp.getPossibleActions(s)])
                self.values[s] = highest_Qvalue
            #For each predecessor p of s ...
            for predecessor in predecessors[s]:
                if self.mdp.isTerminal(predecessor):
                    continue
                highest_Qvalue = max([self.computeQValueFromValues(predecessor, action) for action in self.mdp.getPossibleActions(predecessor)])
                diff = abs(highest_Qvalue - self.values[predecessor])
                if diff > self.theta:
                    priorityQueue.update(predecessor, -diff)