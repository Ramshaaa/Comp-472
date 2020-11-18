import copy
from time import perf_counter


def ucs(puzzle):
    start_time = perf_counter()
    open_list = []
    closed_list = []
    search = []
    open_list.append(puzzle)

    elapsed_time = 0
    while not closed_list or not closed_list[-1].isGoal():
        search.append([0, open_list[0].getTotCost(), 0, open_list[0].getState()])

        moves = open_list[0].getMoves()  # expand all the valid possible configurations
        for item in moves:
            p = copy.deepcopy(open_list[0])
            p.move(item[0])  # play the move
            if p.getState() not in [x.getState() for x in closed_list] and p.getState() not in [x.getState() for x in
                                                                                                open_list]:  # checks lists
                open_list.append(p)  # append each expanded configuration

        closed_list.append(open_list.pop(0))

        open_list.sort(key=lambda a: a.cost)

        elapsed_time = perf_counter() - start_time
        if elapsed_time > 60:
            print(f'The time is greater than 60 : {elapsed_time}')
            return

    return search, closed_list[-1].getSolution(), closed_list[-1].getTotCost(), elapsed_time

# puzzle = Puzzle([1, 0, 3, 7, 5, 2, 6, 4],2, 4)
# puzzle = Puzzle([0, 3, 1, 4, 2, 6, 5, 7], 2, 4)

# puzzle = Puzzle([3, 0, 1, 4, 2, 6, 5, 7], 2, 4)
# puzzle = Puzzle([6, 3, 4, 7, 1, 2, 5, 0], 2, 4)
# puzzle = Puzzle([1, 0, 3, 6, 5, 2, 7, 4], 2, 4)

# puzzle = Puzzle([1, 2, 3, 4, 5, 6, 7, 0], 2, 4)
# puzzle = Puzzle([1, 3, 5, 7, 2, 4, 6, 0], 2, 4)
