from utils.distance_metrics import manhattan_distance, euclidean_distance
from utils.search_algorithms import UCS, GBFS, A_STAR
from puzzle.puzzle_state import PuzzleState
import time
import os


class PuzzleSolver(object):

    def __init__(self, initial_state, goal, algorithm='ucs', heuristic=None):

        self.algorithm = algorithm
        self.heur = heuristic
        self.initial_state = initial_state

        # Assign the search algorithm that will be used in the solver.
        if self.algorithm == 'ucs':
            self.search_alg = UCS
        elif self.algorithm == 'gbfs':
            self.search_alg = GBFS
        elif self.algorithm == 'ast':
            self.search_alg = A_STAR
        else:
            raise NotImplementedError("No such algorithm is supported.")

        if heuristic == 'manhattan':
            self.dist_metric = manhattan_distance
        elif heuristic == 'euclidean':
            self.dist_metric = euclidean_distance

        # Create a Puzzle State Object with the inputs for Solver.
        initial_state = tuple(map(int, initial_state))
        self.puzzle_state = PuzzleState(initial_state, 2, 4, goal, self.calculate_total_cost)

    def calculate_total_cost(self, state):
        """calculate the total estimated cost of a state"""
        sum_heuristic = 0
        for i, item in enumerate(state.config):
            current_row = i // state.m
            current_col = i % state.m
            goal_idx = state.goal.index(item)
            goal_row = goal_idx // state.m
            goal_col = goal_idx % state.m
            sum_heuristic += self.dist_metric(current_row, current_col, goal_row, goal_col)
        if self.algorithm == 'ucs':
            return state.cost
        elif self.algorithm == 'gbfs':
            return sum_heuristic
        else :
            return state.cost + sum_heuristic

    def printSolutionFile(self, state_list, costofpath, runningtime, initial):
        #change the name here
        name = '2_ASTAR_solution.txt'

        with open(os.path.join(name), 'w') as f:
            f.write('0 0' + ' ' + str(initial)[1:-1] + '\n')
            for i in state_list:
                f.write(str(i.tile) + ' ' + str(i.costOfMove) + ' ' + str(i.config)[1:-1] + '\n')
            f.write(str(costofpath) + ' ' + str(runningtime))
        f.close()

    def printSearchFile(self, explored):
        #change the name here
        name = '2_ASTAR_search.txt'
        with open(os.path.join(name), 'w') as f:
            for i in explored:
                f.write(str(i.cost) + ' ' + str(i.config)[1:-1] + '\n')
        f.close()

    def writeOutput(self, result, running_time):
        final_state, nodes_expanded, max_search_depth, search = result
        path_to_goal = [final_state.action]
        cost_of_path = final_state.cost
        parent_state = final_state.parent
        state_list = [final_state]

        while parent_state:
            if parent_state.parent:
                state_list.append(parent_state)
                path_to_goal.append(parent_state.action)
            parent_state = parent_state.parent
        path_to_goal.reverse()
        state_list.reverse()
        search_depth = len(path_to_goal)

        print("******* Results *******")
        print("path_to_goal: " + str(path_to_goal) + "\n")
        print("cost_of_path: " + str(cost_of_path) + "\n")
        print("nodes_expanded: " + str(nodes_expanded) + "\n")
        print("search_depth: " + str(search_depth) + "\n")
        print("max_search_depth: " + str(max_search_depth) + "\n")
        print("running_time: " + str(running_time) + "\n")
        self.printSolutionFile(state_list, cost_of_path, running_time, self.initial_state)
        self.printSearchFile(search)

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
            results = UCS(self.puzzle_state, self.calculate_total_cost)
            running_time = time.time() - start_time
            self.writeOutput(results, running_time)
