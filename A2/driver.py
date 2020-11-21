from puzzle.puzzle_solver import PuzzleSolver
import sys

if __name__ == '__main__':

    chosen_heuristic = None

    chosen_algorithm = 'ast'

    with open('50_random_puzzles.txt') as f:
        puzzleList = []
        for line in f:
            line = line.split()  # to deal with blank
            if line:  # lines (ie skip them)
                line = [int(i) for i in line]
                puzzleList.append(line)

    if chosen_algorithm == 'ast' or chosen_algorithm == 'gbfs' or chosen_algorithm == 'ucs':
        value = input("Please choose a heuristic function:\n[1] Manhattan Distance  [2] Euclidean Distance  ")
        if value == str(1):
            chosen_heuristic = "manhattan"
        elif value == str(2):
            chosen_heuristic = "euclidean"
        else:
            raise Exception("Wrong input heuristic function !")

    for i in puzzleList:
        solver = PuzzleSolver(i, [1, 2, 3, 4, 5, 6, 7, 0], chosen_algorithm, heuristic=chosen_heuristic)
        solver.solve()
        solver.puzzle_state.display()

# ast 0,5,2,4,1,3,7,6
# ast 3,0,1,4,2,6,5,7
# ast 6,3,4,7,1,2,5,0
# ast 1,0,3,6,5,2,7,4
