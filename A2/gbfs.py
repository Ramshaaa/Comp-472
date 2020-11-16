import copy
from time import perf_counter


# for i in open_list:
#     print(f'New append  {i.getState()}')



def gbfs(puzzle, h):
    start_time = perf_counter()
    open_list = []
    closed_list = []
    search = []
    open_list.append(puzzle)

    elapsed_time = 0
    while not closed_list or not closed_list[-1].isGoal():  # as long is it dosnt find the goal keep loopin

        search.append([0, 0, open_list[0].getTotCost(), open_list[0].getState()])

        moves = open_list[0].getMoves()  # expand all the valid possible configurations
        for item in moves:
            p = copy.deepcopy(open_list[0])
            p.move(item[0])
            if p.getState() not in [x.getState() for x in closed_list] and p.getState() not in [x.getState() for x in
                                                                                              open_list]:  # checks lists
                open_list.append(p)

        closed_list.append(open_list.pop(0))

        if h == 1:
            open_list.sort(key=lambda x: x.getSumOfPermInv())  # this sorts the list using sum of inv perm
        if h == 2:
            open_list.sort(key=lambda x: x.getManhattanDist())  # this sorts the list using sum of inv perm

        elapsed_time = perf_counter() - start_time
        if elapsed_time > 60:
            return

    return search, closed_list[-1].getSolution(), closed_list[-1].getTotCost(), elapsed_time
