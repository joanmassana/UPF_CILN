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

    # print "Start's successors:", problem.getSuccessors(problem.getStartState())

    dfs_stack = util.Stack()
    visited_nodes = []
    actions = []

    # We push the first node to the stack + no actions to get to it
    dfs_stack.push((problem.getStartState(), []))

    # While the stack is empty...
    while dfs_stack.isEmpty() == 0:

        # We pop the top state of the stack + actions to get to it
        state, actions = dfs_stack.pop()
        # We add the state to our visited states
        visited_nodes.append(state)
        # print "Pop: ", state

        # If the node we are visiting is the goal state, we return the actions to get to it
        if problem.isGoalState(state) == 1:
            return actions
        # We check the leafs of the actual node
        for leaf in problem.getSuccessors(state):
            # print "Successors : ", problem.getSuccessors(state)
            next_state = leaf[0]
            next_direction = leaf[1]
            # print "Visited: ", visited_nodes
            # If the next leaf state is not in visited nodes, we push it to the stack with the actions to get to it
            if next_state not in visited_nodes:
                # print "Pushing: ", next_state
                dfs_stack.push((next_state, actions + [next_direction]))

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    "*** YOUR CODE HERE ***"

    bfs_queue = util.Queue()
    visited_nodes = []
    actions = []
    # We push the first node to the queue + no actions to get to it
    bfs_queue.push((problem.getStartState(), []))
    visited_nodes.append(problem.getStartState())

    while bfs_queue.isEmpty() == 0:
        # We pop the top state of the stack + actions to get to it
        state, actions = bfs_queue.pop()
        # If the node we are visiting is the goal state, we return the actions to get to it
        if problem.isGoalState(state) == 1:
            return actions
        # We check the leafs of the actual node
        for leaf in problem.getSuccessors(state):
            next_state = leaf[0]
            next_direction = leaf[1]

            # If the next leaf state is not in visited nodes, we push it to the queue with the actions to get to it
            if next_state not in visited_nodes:
                bfs_queue.push((next_state, actions + [next_direction]))
                # We add the state to our visited states
                visited_nodes.append(next_state)

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    "*** YOUR CODE HERE ***"
    # Declaramos una cola de prioridad para implementar este tipo de busqueda
    ucs_priorityQueue = util.PriorityQueue()
    visited_nodes = []
    actions = []
    # Push del primer nodo a la cola de prioridad, que toma un item y una prioridad asociada
    ucs_priorityQueue.push((problem.getStartState(), actions), 0)

    while ucs_priorityQueue.isEmpty() == 0:

        # Cogemos el nodo de mas prioridad y guardamos su estado y las acciones
        state, actions = ucs_priorityQueue.pop()

        # Mientras sea un nodo que aun no hemos visitado, lo anadimos a la lista de visitados y comprobamos si es goalState
        if state not in visited_nodes:
            visited_nodes.append(state)

            if problem.isGoalState(state) == 1:
                return actions

            # Comprobamos los sucesores del nodo, si no los hemos visitado, los anadimos a la cola de prioridad, asignando como prioridad el coste que tienen sus acciones
            for leaf in problem.getSuccessors(state):
                next_state = leaf[0]
                next_direction = leaf[1]

                if next_state not in visited_nodes:
                    ucs_priorityQueue.push((next_state, actions + [next_direction]),
                                           problem.getCostOfActions(actions + [next_direction]))

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function  estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    "*** YOUR CODE HERE ***"
    # Declaramos una cola de prioridad para implementar este tipo de busqueda
    aStar_priorityQueue = util.PriorityQueue()
    visited_nodes = []
    actions = []
    # Push del primer nodo a la cola de prioridad, que toma un item y una prioridad asociada, que en este caso es una heuristica
    aStar_priorityQueue.push((problem.getStartState(), []), heuristic(problem.getStartState(), problem))

    while aStar_priorityQueue.isEmpty() == 0:

        # Cogemos el nodo de mas prioridad y guardamos su estado y las acciones
        state, actions = aStar_priorityQueue.pop()

        # Mientras sea un nodo que aun no hemos visitado, lo anadimos a la lista de visitados y comprobamos si es goalState
        if state not in visited_nodes:
            visited_nodes.append(state)

            if problem.isGoalState(state) == 1:
                return actions

            # Comprobamos los sucesores del nodo, si no los hemos visitado, los anadimos a la cola de prioridad, asignando como prioridad el coste que tienen sus acciones + la heuristica
            for leaf in problem.getSuccessors(state):
                next_state = leaf[0]
                next_direction = leaf[1]

                if next_state not in visited_nodes:
                    aStar_priorityQueue.push((next_state, actions + [next_direction]),
                                             problem.getCostOfActions(actions + [next_direction]) + heuristic(
                                                 next_state, problem))

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
