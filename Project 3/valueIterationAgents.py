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
        #stateValues = self.values.copy()
        for i in range(self.iterations):
            stateValues = self.values.copy()
            for state in self.mdp.getStates():
                stateActionValues = [] # TODO: Make counter()
                for action in self.mdp.getPossibleActions(state):
                    val = 0
                    for neighbor in self.mdp.getTransitionStatesAndProbs(state, action): # Returns list of (nextState, prob) pairs
                        #val += (neighbor[1]*(self.mdp.getReward(state, action, neighbor[0]) + self.discount*self.values[neighbor[0]]))
                        val += (neighbor[1]*(self.mdp.getReward(state, action, neighbor[0]) + self.discount*stateValues[neighbor[0]])) #TODO: Replace w computeQValueFromValues???
                    stateActionValues.append(val)
                if len(self.mdp.getPossibleActions(state)) > 0:
                    optimalAction = max(stateActionValues)
                    self.values[state] = optimalAction
                    #stateValues[state] = optimalAction
        #self.values += stateValues




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
        val = 0
        for neighbor in self.mdp.getTransitionStatesAndProbs(state, action):
            val += (neighbor[1]*(self.mdp.getReward(state, action, neighbor[0]) + self.discount*self.values[neighbor[0]]))
        return val

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        mx = -9999999999
        ret = None
        for action in self.mdp.getPossibleActions(state):
            actionQ = self.computeQValueFromValues(state, action)
            if actionQ  > mx:
                mx = actionQ
                ret = action
        return ret

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
        stateList = self.mdp.getStates()
        numStates = len(stateList)
        for i in range(self.iterations):
            stateValues = self.values.copy()
            state = stateList[i%numStates]
            if self.mdp.isTerminal(state):
                stateValues[state] = 0
            else:
                stateActionValues = []
                for action in self.mdp.getPossibleActions(state):
                    val = 0
                    for neighbor in self.mdp.getTransitionStatesAndProbs(state, action):
                        val += (neighbor[1]*(self.mdp.getReward(state, action, neighbor[0]) + self.discount*stateValues[neighbor[0]]))
                    stateActionValues.append(val)
                if len(self.mdp.getPossibleActions(state)) > 0:
                    optimalAction = max(stateActionValues)
                    stateValues[state] = optimalAction
            self.values[state] = stateValues[state]


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
        # Compute the predecessors of all states
        predecessors = {}
        for state in self.mdp.getStates():
            p = set()
            for subState in self.mdp.getStates():
                for action in self.mdp.getPossibleActions(subState):
                    for neighbor in self.mdp.getTransitionStatesAndProbs(subState, action):
                        if neighbor[0] is state:
                            p.add(subState)
            predecessors[state] = p

        # Initialize an empty priority queue
        q = util.PriorityQueue()

        # For each non-terminal state s: (note: must iterate over states in the order returned by self.mdp.getStates())
        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):
                # Find the absolute value of the difference between the current value of s in self.values and the highest Q-value across all possible actions from s (this represents what the value should be); call this number diff. Do NOT update self.values[s] in this step.
                stateActionValues = []
                for action in self.mdp.getPossibleActions(s):
                    stateActionValues.append(self.getQValue(s, action))
                optimalAction = max(stateActionValues)
                diff = 0 - abs(self.values[s] - optimalAction)
                # Push s into the priority queue with priority -diff (note that this is negative). We use a negative because the priority queue is a min heap, but we want to prioritize updating states that have a higher error.
                q.push(s, diff)
            else: # (s is a terminal state)
                self.values[s] = 0

        # For iteration in 0, 1, 2, ..., self.iterations - 1:
        for i in range(self.iterations - 1):
            # If the priority queue is empty, then terminate.
            if q.isEmpty():
                break
            # Pop a state s off the priority queue.
            s = q.pop()
            # Update s's value (if it is not a terminal state) in self.values.
            if not self.mdp.isTerminal(s):
                stateActionValues = []
                for action in self.mdp.getPossibleActions(s):
                    stateActionValues.append(self.computeQValueFromValues(s, action))
                optimalAction = max(stateActionValues)
                self.values[s] = optimalAction

                #self.values[s] = self.getValue(state) #sus

            # For each predecessor p of s:
            for p in predecessors[s]:
                # Find the absolute value of the difference between the current value of p in self.values and the highest Q-value across all possible actions from p (this represents what the value should be); call this number diff. Do NOT update self.values[p] in this step.
                stateActionValues = []
                for action in self.mdp.getPossibleActions(s):
                    stateActionValues.append(self.getQValue(s, action))
                optimalAction = max(stateActionValues)
                diff = abs(self.getValue(s) - optimalAction)
                # If diff > theta, push p into the priority queue with priority -diff (note that this is negative), as long as it does not already exist in the priority queue with equal or lower priority. As before, we use a negative because the priority queue is a min heap, but we want to prioritize updating states that have a higher error.
                if diff > self.theta:
                    diff = 0 - diff
                    q.update(p, diff)
