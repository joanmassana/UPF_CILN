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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    dfs_stack = util.Stack()
    visited_nodes = []
    actions = []
    dfs_stack.push((problem.getStartState(), []))

    while dfs_stack.isEmpty() == 0:

        state, actions = dfs_stack.pop()
        visited_nodes.append(state)
        #print "Pop: ", state

        if problem.isGoalState(state) == 1:
            return actions

        for leaf in problem.getSuccessors(state):
            #print "Successors : ", problem.getSuccessors(state)
            next_state = leaf[0]
            next_direction = leaf[1]
            #print "Visited: ", visited_nodes
            if next_state not in visited_nodes:
                #print "Pushing: ", next_state
                dfs_stack.push((next_state, actions + [next_direction]))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    "*** YOUR CODE HERE ***"	
    
    bfs_queue = util.Queue()
    visited_nodes = []
    actions = []
    bfs_queue.push((problem.getStartState(), []))
    visited_nodes.append(problem.getStartState())

    while bfs_queue.isEmpty() == 0:
        state, actions = bfs_queue.pop()

        if problem.isGoalState(state) == 1:
            return actions

        for leaf in problem.getSuccessors(state):
            next_state = leaf[0]
            next_direction = leaf[1]

            if next_state not in visited_nodes:
                bfs_queue.push((next_state, actions + [next_direction]))
                visited_nodes.append(next_state)

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    "*** YOUR CODE HERE ***"
    
    ucs_priorityQueue = util.PriorityQueue()
    visited_nodes = []
    actions = []
    ucs_priorityQueue.push((problem.getStartState(), []), 0)  #push(self,item,priority)    
    
    while ucs_priorityQueue.isEmpty() == 0:

        state, actions = ucs_priorityQueue.pop()

        if state not in visited_nodes:
            visited_nodes.append(state)

            if problem.isGoalState(state) == 1:
                return actions

            for leaf in problem.getSuccessors(state):
                next_state = leaf[0]
                next_direction = leaf[1]

                if next_state not in visited_nodes:
                    ucs_priorityQueue.push((next_state, actions + [next_direction]), problem.getCostOfActions(actions + [next_direction]))

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    "*** YOUR CODE HERE ***"
    
    aStar_priorityQueue = util.PriorityQueue()
    visited_nodes = []
    actions = []
    aStar_priorityQueue.push((problem.getStartState(), []), heuristic(problem.getStartState(), problem))     
    
    while aStar_priorityQueue.isEmpty() == 0:

        state, actions = aStar_priorityQueue.pop()

        if state not in visited_nodes:
            visited_nodes.append(state)

            if problem.isGoalState(state) == 1:
                return actions

            for leaf in problem.getSuccessors(state):
                next_state = leaf[0]
                next_direction = leaf[1]

                if next_state not in visited_nodes:
                    aStar_priorityQueue.push((next_state, actions + [next_direction]), problem.getCostOfActions(actions + [next_direction]) + heuristic(next_state, problem))

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
