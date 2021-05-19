from utils.distance_metrics import no_heuristic, manhattan_distance, euclidean_distance
from utils.search_algorithms import UCS, GBFS, A_STAR
from puzzle.puzzle_state import PuzzleState
import time
import os


class PuzzleSolver(object):

    def __init__(self, initial_state, goal1, goal2, counter, algorithm='ucs', heuristic=None):

        self.algorithm = algorithm
        self.initial_state = initial_state
        self.heuristic = heuristic
        self.counter = counter

        # Assign the search algorithm that will be used in the solver.
        if self.algorithm == 'ucs':
            self.search_alg = UCS
        elif self.algorithm == 'gbfs':
            self.search_alg = GBFS
        elif self.algorithm == 'ast':
            self.search_alg = A_STAR
        else:
            raise NotImplementedError("No such algorithm is supported.")

        if self.heuristic is None:
            self.dist_metric = no_heuristic
        elif self.heuristic == 'naive':
            self.heur = 0
        elif self.heuristic == 'manhattan':
            self.dist_metric = manhattan_distance
            self.heur = 1
        elif self.heuristic == 'euclidean':
            self.dist_metric = euclidean_distance
            self.heur = 2

        # Create a Puzzle State Object with the inputs for Solver.
        initial_state = tuple(map(int, initial_state))
        self.puzzle_state = PuzzleState(initial_state, 2, 4, goal1, goal2, self.calculate_total_cost)

    def calculate_total_cost(self, state):
        """calculate the total estimated cost of a state"""

        sum_heuristic = 0
        result = []

        if self.heuristic != 'naive':

            for i, item in enumerate(state.config):
                current_row = i // state.m
                current_col = i % state.m
                goal1_idx = state.goal1.index(item)
                goal1_row = goal1_idx // state.m
                goal1_col = goal1_idx % state.m
                sum_heuristic += self.dist_metric(current_row, current_col, goal1_row, goal1_col)
                result.append(sum_heuristic)

            for i, item in enumerate(state.config):
                current_row = i // state.m
                current_col = i % state.m
                goal2_idx = state.goal2.index(item)
                goal2_row = goal2_idx // state.m
                goal2_col = goal2_idx % state.m
                sum_heuristic += self.dist_metric(current_row, current_col, goal2_row, goal2_col)
                result.append(sum_heuristic)

            if self.algorithm == 'ucs':
                return state.cost
            elif self.algorithm == 'gbfs':
                return min(result[0], result[1])
            elif self.algorithm == 'ast':
                return state.cost + min(result[0], result[1])

        else:
            # Naive heuristic h0, for demo purposes
            zero_idx = state.config.index(0)
            row = zero_idx // state.m
            col = zero_idx % state.m

            if row == 1 and col == 3:
                result.append(0)
            else:
                result.append(1)

            if self.algorithm == 'ucs':
                return state.cost
            elif self.algorithm == 'gbfs':
                return result[0]
            elif self.algorithm == 'ast':
                return state.cost + result[0]

    def printSolutionFile(self, state_list, cost_of_path, running_time):
        if self.algorithm == 'ucs':
            name = 'output files/' + str(self.counter) + '_' + self.algorithm + '_solution.txt'
        else:
            name = 'output files/' + str(self.counter) + '_' + self.algorithm + '_h' + str(self.heur) + '_solution.txt'

        with open(os.path.join(name), 'w') as f:
            f.write('0 0' + ' ' + ' '.join([str(v) for v in self.initial_state]) + '\n')
            for i in state_list:
                f.write(str(i.tile) + ' ' + str(i.cost_of_move) + ' ' + ' '.join([str(v) for v in i.config]) + '\n')
            f.write(str(cost_of_path) + ' ' + str(running_time) + '\n')
        f.close()

    def printSearchFile(self, explored):
        if self.algorithm == 'ucs':
            name = 'output files/' + str(self.counter) + '_' + self.algorithm + '_search.txt'
        else:
            name = 'output files/' + str(self.counter) + '_' + self.algorithm + '_h' + str(self.heur) + '_search.txt'

        with open(os.path.join(name), 'w') as f:
            if self.algorithm == 'ucs':
                for i in explored:
                    f.write('0' + ' ' + str(i.cost) + ' ' + '0' + ' ' + ' '.join([str(v) for v in i.config]) + '\n')
            elif self.algorithm == 'gbfs':
                for i in explored:
                    f.write('0' + ' ' + '0' + ' ' + str(i.cost) + ' ' + ' '.join([str(v) for v in i.config]) + '\n')
            elif self.algorithm == 'ast':
                for i in explored:
                    f.write(str(i.cost) + ' ' + '0' + ' ' + '0' + ' ' + ' '.join([str(v) for v in i.config]) + '\n')
        f.close()

    def printAnalysis(self, search_depth, nodes_expanded, cost_of_path, running_time):
        if self.algorithm == 'ucs':
            name = 'output files/' + self.algorithm + '_analysis.txt'
        else:
            name = 'output files/' + self.algorithm + '_h' + str(self.heur) + '_analysis.txt'

        with open(os.path.join(name), 'w') as f:
            f.write('Total length of solution: ' + str(search_depth)
                    + '\nTotal length of search: ' + str(nodes_expanded)
                    + '\nTotal number of no solution: ' + str(0)
                    + '\nTotal cost: ' + str(cost_of_path)
                    + '\nTotal runtime: ' + str(running_time)

                    + '\n\nAverage length of solution : ' + str(search_depth / self.counter)
                    + '\nAverage length of search : ' + str(nodes_expanded / self.counter)
                    + '\nAverage number of no solution: ' + str(0 / self.counter)
                    + '\nAverage cost: ' + str(cost_of_path / self.counter)
                    + '\nAverage runtime: ' + str(running_time / self.counter))

    def writeOutput(self, result, running_time):
        final_state, nodes_expanded, max_search_depth, explored = result
        path_to_goal = [final_state.action]
        cost_of_path = final_state.cost
        parent_state = final_state.parent
        state_list = [final_state]

        while parent_state:
            if parent_state.parent:
                state_list.append(parent_state)
                path_to_goal.append(parent_state.action)
            parent_state = parent_state.parent

        state_list.reverse()
        path_to_goal.reverse()
        search_depth = len(path_to_goal)

        print("******* Results *******")
        print("path_to_goal (the moves): " + str(path_to_goal) + "\n")
        print("search_depth (length of solution): " + str(search_depth) + "\n")
        print("nodes_expanded (length of search): " + str(nodes_expanded) + "\n")
        print("cost_of_path (cost of solution): " + str(cost_of_path) + "\n")
        print("max_search_depth: " + str(max_search_depth) + "\n")
        print("running_time: " + str(running_time) + "\n")
        self.printSolutionFile(state_list, cost_of_path, running_time)
        self.printSearchFile(explored)
        return search_depth, nodes_expanded, cost_of_path, running_time

    def solve(self):
        print("")
        start_time = time.time()
        if self.search_alg == UCS:
            results = UCS(self.puzzle_state, self.calculate_total_cost)
        elif self.search_alg == GBFS:
            results = GBFS(self.puzzle_state, self.calculate_total_cost)
        else:
            results = A_STAR(self.puzzle_state, self.calculate_total_cost)
        running_time = time.time() - start_time
        return self.writeOutput(results, running_time)
