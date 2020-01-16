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

def depthFirstSearch(problem):
    succ = util.Stack()                                     # Stack will hold tuples of nodes and their paths we still need to visit.
    succ.push((problem.getStartState(), []))                # Starting with start node. No path to start node.
    visited = []                                            # List to track which nodes we've visited.
    while True:                                             # Break when we hit goal node.
        cur = succ.pop()                                    # Start with the most recently added node (DFS).
        visited.append(cur[0])
        if not problem.isGoalState(cur[0]):                 # Current node is not the finish node.
            for successor in problem.getSuccessors(cur[0]): # Check all successors of the current node.
                if successor[0] not in visited:             # Skip it if we've already visited it.
                    path = cur[1][:]                        # Copy the path from the current node...
                    path.append(successor[1])               #      and add the direction towards the successor to it.
                    succ.push((successor[0], path))         # Add the successor to the list of nodes to be visited.
        else:                                               # Found goal.
            actions = cur[1]                                # Get the saved path to the goal node.
            break                                           # Stop looping.

    return actions                                          # Return the path to the goal node.

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    succ = util.Queue()                                     # Queue will hold tuples of nodes we still need to visit and their paths.
    succ.push((problem.getStartState(), []))                # Starting with start node. No path to start node.
    visited = []                                            # List to track which nodes we've visited.
    while True:                                             # Break when we hit goal node.
        # print(succ.list)
        cur = succ.pop()                                    # Start with the most recently added node (DFS).
        if not problem.isGoalState(cur[0]):                 # Current node is not the finish node.
            if cur[0] not in visited:                       # Skip it if we've already visited it.
                visited.append(cur[0])
                for successor in problem.getSuccessors(cur[0]): # Check all successors of the current node.
                    path = cur[1][:]                        # Copy the path from the current node...
                    path.append(successor[1])               #      and add the direction towards the successor to it.
                    succ.push((successor[0], path))         # Add the successor to the list of nodes to be visited.
        else:                                               # Found goal.
            actions = cur[1]                                # Get the saved path to the goal node.
            break                                           # Stop looping.

    return actions                                          # Return the path to the goal node.

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    succ = util.PriorityQueue()                             # Priority Queue will hold tuples of nodes we still need to visit, their paths, and the cost to reach them.
    succ.push((problem.getStartState(), [], 0), 0)          # Starting with start node. No path to start node.
    visited = []                                            # List to track which nodes we've visited.
    #solution = []                                          # Store the most optimal path to finsih so far.
    while True:                                             # Break when we hit goal node.
        cur = succ.pop()                                    # Start with the most recently added node (DFS).
        visited.append(cur[0])
        if not problem.isGoalState(cur[0]):                 # Current node is not the finish node.
            for successor in problem.getSuccessors(cur[0]): # Check all successors of the current node.
                if successor[0] not in visited:             # Skip it if we've already visited it.
                    path = cur[1][:]                        # Copy the path from the current node...
                    path.append(successor[1])               #      and add the direction towards the successor to it.
                    cost = cur[2] + successor[2]
                    succ.push((successor[0], path, cost), cost) # Add the successor to the list of nodes to be visited.
        else:                                               # Found goal.
            actions = cur[1]                                # Get the saved path to the goal node.
            break                                           # Stop looping.
        #     if not solution:                                # This is the first successful path.
        #         solution = cur[1][:]                        # Store the path.
        #     else:                                           # This is not the first successful path found.
        #         if len(solution) > len(cur[1]):             # Check if this new path is shorter than the previous one.
        #             solution = cur[1][:]                    # Update if it is.
        # if succ.isEmpty():                                  # No new nodes to try.
        #     break

    return actions                                          # Return the optimal path to the goal node.

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    start = problem.getStartState()
    succ = util.PriorityQueue()                             # Priority Queue will hold tuples of nodes we still need to visit, their paths, and the cost to reach them.
    succ.push((start, [], 0), heuristic(start, problem))    # Starting with start node. No path to start node. Using the heuristic as the priority.
    visited = []                                            # List to track which nodes we've visited.
    while True:                                             # Break when we hit goal node.
        cur = succ.pop()                                    # Start with the most recently added node (DFS).
        if not problem.isGoalState(cur[0]):                 # Current node is not the finish node.
            if cur[0] not in visited:             # Skip it if we've already visited it.
                visited.append(cur[0])
                for successor in problem.getSuccessors(cur[0]): # Check all successors of the current node.
                    path = cur[1][:]                        # Copy the path from the current node...
                    path.append(successor[1])               #      and add the direction towards the successor to it.
                    cost = cur[2] + successor[2]
                    succ.push((successor[0], path, cost), heuristic(successor[0], problem) + cost) # Add the successor to the list of nodes to be visited.
        else:                                               # Found goal.
            actions = cur[1]                                # Get the saved path to the goal node.
            break                                           # Stop looping.
        # if succ.isEmpty():
        #     break

    return actions                                          # Return the optimal path to the goal node.


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
