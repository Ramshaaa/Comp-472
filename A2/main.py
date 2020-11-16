from puzzle import Puzzle
from gbfs import gbfs
from ucs import ucs
import out

puzzNum = 3
create_puzzle = Puzzle([1, 0, 3, 7, 5, 2, 6, 4], 2, 4)  # create object from Puzzle class
# create_puzzle = Puzzle([0, 3, 1, 4, 2, 6, 5, 7], 2, 4)
# create_puzzle = Puzzle([3, 0, 1, 4, 2, 6, 5, 7], 2, 4)
# create_puzzle = Puzzle([6, 3, 4, 7, 1, 2, 5, 0], 2, 4)
# create_puzzle = Puzzle([1, 0, 3, 6, 5, 2, 7, 4], 2, 4)

# gbfs_h0 = gbfs(create_puzzle, 0)
gbfs_h1 = gbfs(create_puzzle, 1)
gbfs_h2 = gbfs(create_puzzle, 2)

# Output

# READ
#	****look at my return function in gbfs for details on the parameters of the output file functions**********
#	search takes in a list of lists per itteration so i append a list of [f-score, g-score, h-score, currentState] at each itteration for search
#	solution file takes in the (finalNode.getSolution(), finalScore, time) is a tuple,
#	I returned everything i needed when i call my fucntion so everyting is avalable for calling

if ucs(create_puzzle) is not None:
    out.solutionFile(gbfs_h1[1:], f'{puzzNum}_gbfs-h1_solution')
    out.searchFile(gbfs_h1[0], f'{puzzNum}_gbfs-h1_search')
    out.solutionFile(gbfs_h2[1:], f'{puzzNum}_gbfs-h2_solution')
    out.searchFile(gbfs_h2[0], f'{puzzNum}_gbfs-h2_search')
    out.solutionFile(ucs(create_puzzle)[1:], f'{puzzNum}_ucs_solution')
    out.searchFile(ucs(create_puzzle)[0], f'{puzzNum}_ucs_search')
