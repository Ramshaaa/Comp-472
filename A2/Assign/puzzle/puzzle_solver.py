from utils.distance_metrics import manhattan_distance, euclidean_distance
from utils.search_algorithms import UCS, GBFS, A_STAR
from puzzle.puzzle_state import PuzzleState
import math
import time


class PuzzleSolver(object):

    def __init__(self, initial_state, goal, algorithm='ucs', heuristic=None):

        self.initial_state = initial_state

        # Assign the search algorithm that will be used in the solver.
        if algorithm == 'ucs':
            self.search_alg = GBFS
        elif algorithm == 'gbfs':
            self.search_alg = UCS
        elif algorithm == 'ast':
            self.search_alg = A_STAR
        else:
            raise NotImplementedError("No such algorithm is supported.")

        # Assign the heuristic algorithm that will be used in the solver.
        if heuristic is None and algorithm == 'gbfs':
            raise AttributeError("Required Attribute `heuristic` in case of using GBFS Search.")
        if heuristic is None and algorithm == 'ast':
            raise AttributeError("Required Attribute `heuristic` in case of using A* Search.")
        elif heuristic == 'manhattan':
            self.dist_metric = manhattan_distance
        elif heuristic == 'euclidean':
            self.dist_metric = euclidean_distance
        elif heuristic is None and algorithm != 'gbfs' or heuristic is None and algorithm != 'ast':
            pass
        else:
            raise NotImplementedError("No such Heuristic is supported.")

        # Create a Puzzle State Object with the inputs for Solver.
        initial_state = tuple(map(int, initial_state))

        N = 2
        M = N * int(math.sqrt(len(initial_state)))
        self.puzzle_state = PuzzleState(initial_state, N, M, goal, self.calculate_total_cost)

    def calculate_total_cost(self, state):
        """calculate the total estimated cost of a state"""
        sum_heuristic = 0
        for i, item in enumerate(state.config):
            current_row = i % state.n
            current_col = i % state.m
            goal_idx = state.goal.index(item)
            goal_row = goal_idx % state.n
            goal_col = goal_idx % state.m
            sum_heuristic += self.dist_metric(current_row, current_col, goal_row, goal_col)
        return sum_heuristic + state.cost

    def writeOutput(self, result, running_time):
        final_state, nodes_expanded, max_search_depth = result
        path_to_goal = [final_state.action]
        cost_of_path = final_state.cost
        parent_state = final_state.parent

        while parent_state:
            if parent_state.parent:
                path_to_goal.append(parent_state.action)
            parent_state = parent_state.parent
        path_to_goal.reverse()
        search_depth = len(path_to_goal)

        print("******* Results *******")
        print("path_to_goal: " + str(path_to_goal) + "\n")
        print("cost_of_path: " + str(cost_of_path) + "\n")
        print("nodes_expanded: " + str(nodes_expanded) + "\n")
        print("search_depth: " + str(search_depth) + "\n")
        print("max_search_depth: " + str(max_search_depth) + "\n")
        print("running_time: " + str(running_time) + "\n")

    def solve(self):
        start_time = time.time()
        if self.search_alg == GBFS:
            results = GBFS(self.puzzle_state, self.calculate_total_cost)
            running_time = time.time() - start_time
            self.writeOutput(results, running_time)
        if self.search_alg == A_STAR:
            results = A_STAR(self.puzzle_state, self.calculate_total_cost)
            running_time = time.time() - start_time
            self.writeOutput(results, running_time)
        if self.search_alg == UCS:
            results = UCS(self.puzzle_state)
            running_time = time.time() - start_time
            self.writeOutput(results, running_time)
