import numpy as np
from puzzle import Puzzle

class Node:
    """
        A node class for GBFS Search Algorithm
        - parent is parent of the current Node
        - position is current position of the Node in the maze
        - h is heuristic based estimated cost for current Node to end Node
    """
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position
        self.h = 0
        self.value = 0;

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node, puzzle):
    path = []
    #no_rows, no_columns = np.shape(puzzle)

    # Here we create initialized result maze with -1 in every position
    #result = [[-1 for i in range (no_columns)] for j in range (no_rows)]

    result = Puzzle(puzzle, 2, 4)  # create object from Puzzle class
    no_rows, no_columns = np.shape(result);

    current = current_node

    while current is not None:
        path.append(current.position)
        current = current.parent

    # Return reverse path as we need to show from start to end path
    path = path[::-1]
    start_value = 0

    # We update the path of start to end found by A* search with every step incremented by 1  NOTE: MIGHT WANNA CHANGE THIS FOR PUZZLE
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result


def search(puzzle, start, end):
    """
        Returns a list of tuples as a path from the given start to the given end in the given puzzle
    """

    print("Printing index and value of each element in the list")
    for index, val in enumerate(puzzle):
        print("Index:", index, "| Value:", val)

    #print("\nInitializing node values and coordinates for each element in the puzzle list")

    print("\nReshaping puzzle to perform search")
    result_puzzle = Puzzle(puzzle, 2, 4)  # create object from Puzzle class
    print("Your puzzle will look like this: ")
    result_puzzle.show()

    # find puzzle has got how many rows and columns
    # no_rows, no_columns = np.shape(puzzle)
    no_rows = result_puzzle.height
    print("\nnumber of rows: ", no_rows)
    no_columns = result_puzzle.width
    print("number of columns: ", no_columns, "\n")

    #for row in enumerate(result_puzzle.getState()):
        #for elem in row:
            #print(elem)

    for idx, value in np.ndenumerate(result_puzzle.getCurrent()):
        print(idx, value)

    # Create start and end node with initialized values for f, h and f  MIGHT WANNA LOCATE 0 IN THE PUZZLE HERE
    start_node = Node(None, tuple(start))
    start_node.h = 0
    start_node.value = 0

    end_node = Node(None, tuple(end))
    end_node.h = 0


    # Initialize both open (yet to visit) and closed (visited) list
    # put all nodes that are yet to be visited and we will pick the lowest cost node to be put in closed list as well as to be expanded
    open_list = []

    # This list will contain all the explored Nodes that don't need to be explored
    closed_list = []

    # We add the start node to the open_list
    open_list.append(start_node)


    # Stop condition to avoid infinite loops/stopping execution after some certain steps NOTE: MIGHT WANNA CHANGE THIS FOR PUZZLE
    outer_iter = 0
    max_iter = (len(puzzle)//2)**10 #MIGHT WANNA CHANGE SHIT FOR PUZZLE

    # What squares do we search, search movement is left-right-top-bottom-diagonal moves (8 movements from every position)
    move = [[-1, 0],  # go up
            [0, -1],  # go left
            [1, 0],   # go down
            [0, 1],    # go right
            #Diagonal moves
            [-1, 1],   # right upper diagonal
            [-1, -1],  # left upper diagonal
            [1, 1],    # right lower diagonal
            [1, -1]]  # left lower diagonal


    """
        1) We first get the current node by comparing all h cost and selecting the lowest cost node for further expansion
        2) Check max iteration reached or not . Set a message and stop execution
        3) Remove the selected node from yet_to_visit list and add this node to visited list
        4) Perofmr Goal test and return the path else perform below steps
        5) For selected node find out all children (use move to find children)
            a) get the current postion for the selected node (this becomes parent node for the children)
            b) check if a valid position exist (boundary will make few nodes invalid)
            c) if any node is a wall then ignore that
            d) add to valid children node list for the selected parent

            For all the children node
                a) if child in visited list then ignore it and try next node
                b) calculate child node g, h and f values
                c) if child in yet_to_visit list then ignore it
                d) else move the child to yet_to_visit list
    """

    # Loop until you find the end
    while len(open_list) > 0:
        # Every time any node is referred from open_list, counter of limit operation incremented
        outer_iter += 1
        print("outer_iter", outer_iter)

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        print("current node's position: ", current_node.position)
        print("current node's parent: ", current_node.parent)
        print("current node's h: ", current_node.h)
        print("current node's index: ", current_index)
        print("\n")

        print("looping through open list")
        for index, item in enumerate(open_list):
            print("Index",index,":item.h=",item.h,",current_node.h=",current_node.h)
            if item.h < current_node.h:
                print("replace current_node with lowest cost node at index...")
                current_node = item
                current_index = index

        print("\n")
        # if we hit this point return the path such as it may be no solution or
        # computation cost is too high
        if outer_iter > max_iter:
            print("giving up on pathfinding too many iterations")
            #return return_path(current_node, result_puzzle)

        # Pop current node out off open_list, add to closed_list
        print("Popping current node out of open_list and adding to closed_list")
        open_list.pop(current_index)
        closed_list.append(current_node)
        print("OPEN list will now look like this: ")
        for index, item in enumerate(open_list):
            print("Index",index,":item.h=",item.h,",current_node.h=",current_node.h)
        print("\n")
        print("CLOSED list will now look like this: ")
        for index, item in enumerate(closed_list):
            print("Index", index, ":item.h=", item.h, ",current_node.h=", current_node.h)

        print("\n")
        print("Checking if end goal has ben reached..")
        # test if goal is reached or not, if yes then return the path
        if current_node == end_node:
            #return return_path(current_node, result_puzzle)
            print("End goal has been reached")

        print("Sadly is has not been reached so we will be generating our successors")
        print("Generating successors..")
        # Generate children from all adjacent squares
        successors = []

        for new_position in move:

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range (check if within maze boundary)
            if (node_position[0] > (no_rows - 1) or
                    node_position[0] < 0 or
                    node_position[1] > (no_columns - 1) or
                    node_position[1] < 0):
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            successors.append(new_node)

        # Loop through children
        for successor in successors:

            # Child is on the visited list (search entire visited list)
            if len([visited_successor for visited_successor in open_list if visited_successor == successor]) > 0:
                continue


            ## Heuristic costs calculated here, this is using eucledian distance
            #successor.h = (((successor.position[0] - end_node.position[0]) ** 2) +
                       #((successor.position[1] - end_node.position[1]) ** 2))

            # Child is already in the yet_to_visit list and g cost is already lower
            if len([i for i in open_list if successor == i and successor.h > i.h]) > 0:
                continue

            # Add the child to the yet_to_visit list
            open_list.append(successor)

"""
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

if __name__ == '__main__':
    maze = [[0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0]]

    start = [0, 0]  # starting position
    end = [1, 5]  # ending position
    cost = 1  # cost per movement

    path = search(maze, cost, start, end)
    #print(path, '\n'
                #'')

    #print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row])
                     for row in path]))
"""



search([4, 2, 3, 1, 5, 6, 7, 0], [1, 7], [0,0])

#create_puzzle = Puzzle([1, 0, 3, 7, 5, 2, 6, 4], 2, 4)  # create object from Puzzle class
#create_puzzle.show()