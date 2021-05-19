import os
import glob
from puzzle.puzzle_solver import PuzzleSolver


if __name__ == '__main__':
    chosen_heuristic = None
    chosen_algorithm = None

    value = input("Please type to choose a search function:\nucs  gbfs   ast\n")
    if value == 'ucs':
        chosen_algorithm = 'ucs'
    elif value == 'gbfs':
        chosen_algorithm = 'gbfs'
    elif value == 'ast':
        chosen_algorithm = 'ast'
    else:
        raise Exception("Wrong input search function !")

    with open('5_random_puzzles.txt') as f:
        puzzleList = []
        for line in f:
            line = line.split()
            if line:
                line = [int(i) for i in line]
                puzzleList.append(line)

    if chosen_algorithm == 'gbfs' or chosen_algorithm == 'ast':
        value = input(
            "\nPlease enter a number to choose a heuristic function:\n[0] Naive  [1] Manhattan Distance  [2] Euclidean "
            "Distance\n")
        if value == str(0):
            chosen_heuristic = "naive"
        elif value == str(1):
            chosen_heuristic = "manhattan"
        elif value == str(2):
            chosen_heuristic = "euclidean"
        else:
            raise Exception("Wrong input heuristic function !")

    len_solution = 0
    len_search = 0
    cost = 0
    runtime = 0
    counter = 1

    global solver
    for i in puzzleList:
        solver = PuzzleSolver(i, [1, 2, 3, 4, 5, 6, 7, 0], [1, 3, 5, 7, 2, 4, 6, 0],
                              counter, chosen_algorithm, heuristic=chosen_heuristic)

        result = solver.solve()
        len_solution += result[0]
        len_search += result[1]
        cost += result[2]
        runtime += result[3]
        counter += 1

    solver.printAnalysis(len_solution, len_search, cost, runtime)
