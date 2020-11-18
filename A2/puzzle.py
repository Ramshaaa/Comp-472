import copy
from numpy import reshape


class Puzzle:
    # initializes the game board
    def __init__(self, puzzle, height, width):
        self.puzzle = puzzle
        self.height = height
        self.width = width
        self.cost = 0
        self.moves = ['up', 'down', 'left', 'right', 'diagLeft', 'diagRight']
        self.moveList = [0]
        self.CostList = [0]
        self.stateList = [copy.deepcopy(puzzle)]
        self.goal_state0 = [1, 2, 3, 4, 5, 6, 7, 0]
        self.goal_state1 = [1, 3, 5, 7, 2, 4, 6, 0]

    # prints the current state of the board
    def printState(self):
        for i in range(self.height):
            w = self.width
            print(*self.puzzle[i * w:(i + 1) * w], sep=" ")

    # prints the current state of the board
    def show(self):
        matrix = reshape(self.puzzle, (-1, self.width))
        for row in matrix:
            print(*row)

    def getState(self):
        return self.puzzle

    # returns the current total cost
    def getTotCost(self):
        return self.cost

    def getCurrent(self):
        return self.puzzle

    # return true if puzzle is completed
    def isGoal(self):
        if self.puzzle == self.goal_state0 or self.puzzle == self.goal_state1:
            return True
        return False

    # private function for swapping positions on the board
    def __swap(self, pos1, pos2):
        self.puzzle[pos1], self.puzzle[pos2] = self.puzzle[pos2], self.puzzle[pos1]
        if self.puzzle[pos1] == 0:
            return self.puzzle[pos2]
        else:
            return self.puzzle[pos1]

    # swaps the 0 slot up or down and adds to cost
    def upVerticalMove(self):
        pos = self.puzzle.index(0)
        w = self.width
        self.cost += 1
        return self.__swap(pos, pos - w)

    def downVerticalMove(self):
        pos = self.puzzle.index(0)
        w = self.width
        self.cost += 1
        return self.__swap(pos, pos + w)

    # moves 0 left and adds 1 to cost, if 0 is on the left edge then it wraps around and cost += 2
    def leftHorizontalMove(self):
        pos = self.puzzle.index(0)
        w = self.width

        if pos % w == 0:
            self.cost += 2
            return self.__swap(pos, pos + w - 1), 2

        else:
            self.cost += 1
            return self.__swap(pos, pos - 1), 1

    # moves 0 right and adds 1 to cost, if 0 is on the right edge then it wraps around and cost += 2
    def rightHorizontalMove(self):
        pos = self.puzzle.index(0)
        w = self.width

        if pos % w == w - 1:
            self.cost += 2
            return self.__swap(pos, pos - w + 1), 2

        else:
            self.cost += 1
            return self.__swap(pos, pos + 1), 1

    # moves the 0 diag left if 0 is in one of the corners and adds 3 to cost
    def leftDiagMove(self):
        pos = self.puzzle.index(0)
        w = self.width
        h = self.height

        top_r = w - 1           #3
        bottom_r = (w * h) - 1  #7
        top_l = 0               #0
        bottom_l = w * (h - 1)  #4

        self.cost += 3

        if pos == top_r:
            return self.__swap(pos, pos + w - 1)  #6
        elif pos == bottom_r:
            return self.__swap(pos, pos - w - 1)  #2
        if pos == top_l:
            return self.__swap(pos, bottom_r)  #7
        elif pos == bottom_l:
            return self.__swap(pos, top_r)  #3

    # moves the 0 diag right if 0 is in one of the corners and adds 3 to cost
    def rightDiagMove(self):
        pos = self.puzzle.index(0)
        w = self.width
        h = self.height

        top_l = 0               #0
        bottom_l = w * (h - 1)  #4
        top_r = w - 1           #3
        bottom_r = (w * h) - 1  #7

        self.cost += 3

        if pos == top_l:
            return self.__swap(pos, pos + w + 1)  #5
        elif pos == bottom_l:
            return self.__swap(pos, pos - w + 1)  #1
        elif pos == top_r:
            return self.__swap(pos, bottom_l)  #4
        elif pos == bottom_r:
            return self.__swap(pos, top_l)  #0

    def getSolution(self):
        sol = []
        for x in range(len(self.moveList)):
            sol.append([self.moveList[x], self.CostList[x], self.stateList[x]])
        return sol

    def getSumOfPermInv(self):
        count = 0
        count2 = 0
        current = self.puzzle
        for x in current:
            remain = current[current.index(x) + 1:]
            f1 = self.goal_state0
            f2 = self.goal_state1
            f1 = f1[:f1.index(x)]
            f2 = f2[:f2.index(x)]
            for x in remain:
                if x in f1:
                    count += 1
                if x in f2:
                    count2 += 1
        return min(count, count2)

    def getManhattanDist(self):
        total_dist = [0, 0]
        puzzle = self.getState()
        global final_puzzle
        for x in range(2):
            if x == 0:
                final_puzzle = self.goal_state0
            else:
                final_puzzle = self.goal_state1
            w = self.width
            i = 0
            for tile in puzzle:
                if tile == 0:
                    i += 1
                    continue

                row_pos = int(i / w)
                col_pos = i % w

                j = final_puzzle.index(tile)

                row_final = int(j / w)
                col_final = j % w

                dist_row = abs(row_pos - row_final)
                dist_col = abs(col_pos - col_final)

                total_dist[x] += dist_row + dist_col
                i += 1

        return min(total_dist[0], total_dist[1])

    def getMoves(self):
        pos = self.puzzle.index(0)
        w = self.width
        h = self.height

        top_l = 0
        bottom_l = w * (h - 1)
        top_r = w - 1
        bottom_r = (w * h) - 1

        moves = [('up', 1), ('down', 1)]

        if top_l <= pos <= top_r:
            moves.remove(('up', 1))
        elif bottom_l <= pos <= bottom_r:
            moves.remove(('down', 1))

        if pos == top_l or pos == bottom_l:
            moves.append(('left', 2))
            moves.append(('diagLeft', 3))
            moves.append(('diagRight', 3))
        else:
            moves.append(('left', 1))

        if pos == top_r or pos == bottom_r:
            moves.append(('right', 2))
            moves.append(('diagLeft', 3))
            moves.append(('diagRight', 3))
        else:
            moves.append(('right', 1))

        moves.sort(key=lambda tup: tup[1])
        return moves  # returns all valid moves for a configuration

    def move(self, direction):
        if direction == 'up':
            self.moveList.append(self.upVerticalMove())
            self.CostList.append(1)
            self.stateList.append(copy.deepcopy(self.getCurrent()))
        if direction == 'down':
            self.moveList.append(self.downVerticalMove())
            self.CostList.append(1)
            self.stateList.append(copy.deepcopy(self.getCurrent()))
        if direction == 'left':
            temp = self.leftHorizontalMove()
            self.moveList.append(temp[0])
            self.CostList.append(temp[1])
            self.stateList.append(copy.deepcopy(self.getCurrent()))
        if direction == 'right':
            temp = self.rightHorizontalMove()
            self.moveList.append(temp[0])
            self.CostList.append(temp[1])
            self.stateList.append(copy.deepcopy(self.getCurrent()))
        if direction == 'diagLeft':
            self.moveList.append(self.leftDiagMove())
            self.CostList.append(3)
            self.stateList.append(copy.deepcopy(self.getCurrent()))
        if direction == 'diagRight':
            self.moveList.append(self.rightDiagMove())
            self.CostList.append(3)
            self.stateList.append(copy.deepcopy(self.getCurrent()))
