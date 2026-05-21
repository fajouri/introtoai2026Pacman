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
from typing import List

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




def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the deepest nodes in the search tree first."""
    frontier = util.Stack()
    visited = set()
    frontier.push((problem.getStartState(), []))

    while not frontier.isEmpty():
        state, actions = frontier.pop()
        if problem.isGoalState(state):
            return actions
        if state in visited:
            continue
        visited.add(state)
        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:
                frontier.push((successor, actions + [action]))

    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    visited = set()

    start = problem.getStartState()
    frontier.push((start, []))  # (state, actions so far)

    while not frontier.isEmpty():
        state, actions = frontier.pop()

        if problem.isGoalState(state):
            return actions

        if state in visited:
            continue
        visited.add(state)

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:
                frontier.push((successor, actions + [action]))

    return []  # No solution found

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue()
    visited = set()
    frontier.push((problem.getStartState(), []), 0)

    while not frontier.isEmpty():
        state, actions = frontier.pop()
        if problem.isGoalState(state):
            return actions
        if state in visited:
            continue
        visited.add(state)
        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:
                new_actions = actions + [action]
                frontier.push((successor, new_actions), problem.getCostOfActions(new_actions))

    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    visited = set()
    start = problem.getStartState()
    frontier.push((start, []), heuristic(start, problem))

    while not frontier.isEmpty():
        state, actions = frontier.pop()
        if problem.isGoalState(state):
            return actions
        if state in visited:
            continue
        visited.add(state)
        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:
                new_actions = actions + [action]
                g = problem.getCostOfActions(new_actions)
                h = heuristic(successor, problem)
                frontier.push((successor, new_actions), g + h)

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
