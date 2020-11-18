class PuzzleState(object):
    """docstring for PuzzleState"""

    def __init__(self, config, n, m, goal, cost_function, parent=None, action="Initial", cost=0):

        if n * m != len(config):
            raise AttributeError("The length of config entered is not correct or less than required!")

        self.n = n
        self.m = m
        self.cost = cost       # g cost
        self.parent = parent
        self.action = action
        self.dimension = n * m
        self.config = config
        self.blank_space = self.config.index(0)
        self.children = []
        self.goal = goal
        self.cost_function = cost_function   # f cost

        for i in range(self.n):
            offset = i * self.m
            for j in range(self.m):
                if self.config[offset + j] == 0:
                    self.blank_row = i
                    self.blank_col = j
                    break

    def display(self):
        for i in range(self.n):
            line = []
            offset = i * self.m
            for j in range(self.m):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):
        if self.blank_col == 0:
            blank_index = self.blank_row * self.m + self.blank_col
            target = blank_index + self.m - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Wrap_Left",
                               cost=self.cost + 2)
        else:
            blank_index = self.blank_row * self.m + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Left",
                               cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.m - 1:
            blank_index = self.blank_row * self.m + self.blank_col
            target = blank_index - self.m + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Wrap_Right",
                               cost=self.cost + 2)
        else:
            blank_index = self.blank_row * self.m + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Right",
                               cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.m + self.blank_col
            target = blank_index - self.m
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Up",
                               cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.m + self.blank_col
            target = blank_index + self.m
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Down",
                               cost=self.cost + 1)

    def move_diag(self):
        if self.blank_row == 0 and self.blank_col == 0:
            blank_index = self.blank_row * self.m + self.blank_col  # 0
            target = blank_index + self.m + 1  # 5
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Down_Right_Diag",
                               cost=self.cost + 3)
        if self.blank_row == 1 and self.blank_col == 0:
            blank_index = self.blank_row * self.m + self.blank_col  # 4
            target = blank_index - self.m + 1  # 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Up_Right_Diag",
                               cost=self.cost + 3)
        if self.blank_row == 0 and self.blank_col == 3:
            blank_index = self.blank_row * self.m + self.blank_col  # 3
            target = blank_index + self.m - 1  # 6
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Down_Left_Diag",
                               cost=self.cost + 3)
        if self.blank_row == 1 and self.blank_col == 3:
            blank_index = self.blank_row * self.m + self.blank_col  # 7
            target = blank_index - self.m - 1  # 2
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Up_Left_Diag",
                               cost=self.cost + 3)
        if self.blank_row == 0 and self.blank_col == 0:
            blank_index = self.blank_row * self.m + self.blank_col  # 0
            target = blank_index + 2 * self.m - 1  # 7
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Top_Left_Corner_Opposed_Diag",
                               cost=self.cost + 3)
        if self.blank_row == 1 and self.blank_col == 0:
            blank_index = self.blank_row * self.m + self.blank_col  # 4
            target = blank_index - 1  # 3
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Bottom_Left_Corner_Opposed_Diag",
                               cost=self.cost + 3)
        if self.blank_row == 0 and self.blank_col == 3:
            blank_index = self.blank_row * self.m + self.blank_col  # 3
            target = blank_index + 1  # 4
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Top_Right_Corner_Opposed_Diag",
                               cost=self.cost + 3)
        if self.blank_row == 1 and self.blank_col == 3:
            blank_index = self.blank_row * self.m + self.blank_col  # 7
            target = blank_index - 2 * self.m + 1  # 0
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal, self.cost_function, parent=self, action="Bottom_Right_Corner_Opposed_Diag",
                               cost=self.cost + 3)

    def expand(self, RLDU=True):
        """expand the node"""
        global UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT
        if len(self.children) == 0:
            # if self.blank_row - 1 >= 0:  # check if blank tile is in borders but not corners
            #     return
            # if self.blank_row - 1 >= 0 and self.blank_col + 1 <= 3:
            #     return
            # if self.blank_col + 1 <= 3:
            #     return
            # if self.blank_row + 1 <= 2 and self.blank_col + 1 <= 3:
            #     return
            # if self.blank_row + 1 <= 2:
            #     return
            # if self.blank_row + 1 <= 2 and self.blank_col - 1 >= 0:
            #     return
            # if self.blank_col - 1 >= 0:
            #     return
            # if self.blank_row - 1 >= 0 and self.blank_col - 1 >= 0:
            #     return


            if RLDU:  # RLDU Diag
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)
                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)
                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)
                diag_child = self.move_diag()
                if diag_child is not None:
                    self.children.append(diag_child)
            else:  # UDLR Diag
                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)
                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)
                diag_child = self.move_diag()
                if diag_child is not None:
                    self.children.append(diag_child)
        return self.children

    # def is_solvable(self, N, M, B):
    #     inversion = 0
    #     for i in range(len(self.config)):
    #         for j in range(i + 1, len(self.config)):
    #             if (self.config[i] > self.config[j]) and self.config[i] != 0 and self.config[j] != 0:
    #                 inversion += 1
    #     if M % 2 == 1:
    #         return inversion % 2 == 0
    #     if M % 2 == 0 and N % 2 == 0:
    #         return (inversion + B) % 2 == 0
    #     if M % 2 == 0 and N % 2 == 1:
    #         return (inversion + B) % 2 == 1

    def is_goal(self):
        return list(self.config) == self.goal

    def __lt__(self, other):
        return self.cost_function(self) < self.cost_function(other)

    def __le__(self, other):
        return self.cost_function(self) <= self.cost_function(other)

# ucs 1,8,2,0,4,3,7,6,5
# 0,5,2,4,1,3,7,6
