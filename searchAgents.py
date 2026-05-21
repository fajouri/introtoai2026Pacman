# searchAgents.py
# ---------------
# Licensing Information: You are free to use and modify this project for educational purposes.
# This version has been adapted for coursework at Ascencia University by Professor Fajouri.

"""
Agent that uses a search algorithm to find the optimal path to the food (fruit).

Usage examples:
  python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
  python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
  python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
  python pacman.py -l mediumMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
  python pacman.py -l mediumMaze -p SearchAgent -a fn=astar,heuristic=euclideanHeuristic
  python pacman.py -l tinyMaze  -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
"""

from game import Directions
from game import Agent
from game import Actions
import time
import search


class SearchAgent(Agent):
    """
    Finds a path to the food using the specified search algorithm, then
    follows that path.  Supports: dfs, bfs, ucs, astar.
    Default: A* with Manhattan heuristic.
    """

    def __init__(self, fn='astar', prob='PositionSearchProblem', heuristic='manhattanHeuristic'):
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] Algorithm: ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a heuristic in searchAgents.py or search.py.')
            print('[SearchAgent] Algorithm: %s  |  Heuristic: %s' % (fn, heuristic))
            self.searchFunction = lambda x: func(x, heuristic=heur)

        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in searchAgents.py.')
        self.searchType = globals()[prob]

    def registerInitialState(self, state):
        """Plans the path before the game starts and prints planning statistics."""
        if self.searchFunction is None:
            raise Exception('No search function provided for SearchAgent')
        start_time = time.time()
        problem = self.searchType(state)
        self.actions = self.searchFunction(problem)
        if self.actions is None:
            self.actions = []
        elapsed = time.time() - start_time
        total_cost = problem.getCostOfActions(self.actions)
        print('\n=== Path Planning Results ===')
        print('Path length (steps) : %d' % len(self.actions))
        print('Total path cost     : %d' % total_cost)
        print('Planning time       : %.4f seconds' % elapsed)
        if '_expanded' in dir(problem):
            print('Nodes expanded      : %d' % problem._expanded)
        print('=============================')

    def getAction(self, state):
        """Returns the next pre-planned action."""
        if 'actionIndex' not in dir(self):
            self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    Search problem for navigating Pacman to the food (fruit).
    The goal is automatically set to the position of the food item.
    """

    def __init__(self, gameState, costFn=lambda x: 1, goal=None, start=None, warn=True, visualize=True):
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start is not None:
            self.startState = start
        # Auto-detect food position
        if goal is None:
            food_list = gameState.getFood().asList()
            goal = food_list[0] if food_list else (1, 1)
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a single-food maze')
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display):
                    __main__._display.drawExpandedCells(self._visitedlist)
        return isGoal

    def getSuccessors(self, state):
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                cost = self.costFn((nextx, nexty))
                successors.append(((nextx, nexty), action, cost))
        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)
        return successors

    def getCostOfActions(self, actions):
        if actions is None:
            return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += self.costFn((x, y))
        return cost


def manhattanHeuristic(position, problem, info={}):
    "Manhattan distance heuristic for PositionSearchProblem."
    x1, y1 = position
    x2, y2 = problem.goal
    return abs(x1 - x2) + abs(y1 - y2)


def euclideanHeuristic(position, problem, info={}):
    "Euclidean distance heuristic for PositionSearchProblem."
    x1, y1 = position
    x2, y2 = problem.goal
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
