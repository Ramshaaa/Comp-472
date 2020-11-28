class PuzzleState(object):
    """docstring for PuzzleState"""

    def __init__(self, config, n, m, goal1, goal2, cost_function, parent=None, action="Initial", cost=0, movement_cost=0, tile=0):

        if n * m != len(config):
            raise AttributeError("The length of config entered is not correct or less than required!")

        self.tile = tile
        self.cost_of_move = movement_cost   # g cost
        self.n = n  # row
        self.m = m  # col
        self.cost = cost  # f cost
        self.parent = parent
        self.action = action
        self.dimension = n * m
        self.config = config
        self.blank_space = self.config.index(0)
        self.children = []
        self.goal1 = goal1
        self.goal2 = goal2
        self.cost_function = cost_function

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.m
                self.blank_col = i % self.m
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
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Wrap_Left",
                               cost=self.cost + 2, movement_cost=2, tile=self.config[target])
        else:
            blank_index = self.blank_row * self.m + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Left",
                               cost=self.cost + 1, movement_cost= 1, tile=self.config[target])

    def move_right(self):
        if self.blank_col == self.m - 1:
            blank_index = self.blank_row * self.m + self.blank_col
            target = blank_index - self.m + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Wrap_Right",
                               cost=self.cost + 2, movement_cost= 2, tile=self.config[target])
        else:
            blank_index = self.blank_row * self.m + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Right",
                               cost=self.cost + 1, movement_cost= 1, tile=self.config[target])

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.m + self.blank_col
            target = blank_index - self.m
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Up",
                               cost=self.cost + 1, movement_cost=1, tile=self.config[target])

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.m + self.blank_col
            target = blank_index + self.m
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Down",
                               cost=self.cost + 1, movement_cost=1, tile=self.config[target])

    def move_diag(self):
        if self.blank_row == 0 and self.blank_col == 0:
            blank_index = self.blank_row * self.m + self.blank_col  # 0
            target = blank_index + self.m + 1  # 5
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Down_Right_Diag",
                               cost=self.cost + 3, movement_cost=3, tile=self.config[target])
        if self.blank_row == 1 and self.blank_col == 0:
            blank_index = self.blank_row * self.m + self.blank_col  # 4
            target = blank_index - self.m + 1  # 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Up_Right_Diag",
                               cost=self.cost + 3, movement_cost=3, tile=self.config[target])
        if self.blank_row == 0 and self.blank_col == 3:
            blank_index = self.blank_row * self.m + self.blank_col  # 3
            target = blank_index + self.m - 1  # 6
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Down_Left_Diag",
                               cost=self.cost + 3, movement_cost=3, tile=self.config[target])
        if self.blank_row == 1 and self.blank_col == 3:
            blank_index = self.blank_row * self.m + self.blank_col  # 7
            target = blank_index - self.m - 1  # 2
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Up_Left_Diag",
                               cost=self.cost + 3, movement_cost=3, tile=self.config[target])
        if self.blank_row == 0 and self.blank_col == 0:
            blank_index = self.blank_row * self.m + self.blank_col  # 0
            target = blank_index + 2 * self.m - 1  # 7
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Top_Left_Corner_Opposed_Diag",
                               cost=self.cost + 3, movement_cost=3, tile=self.config[target])
        if self.blank_row == 1 and self.blank_col == 0:
            blank_index = self.blank_row * self.m + self.blank_col  # 4
            target = blank_index - 1  # 3
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Bottom_Left_Corner_Opposed_Diag",
                               cost=self.cost + 3, movement_cost=3, tile=self.config[target])
        if self.blank_row == 0 and self.blank_col == 3:
            blank_index = self.blank_row * self.m + self.blank_col  # 3
            target = blank_index + 1  # 4
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Top_Right_Corner_Opposed_Diag",
                               cost=self.cost + 3, movement_cost=3, tile=self.config[target])
        if self.blank_row == 1 and self.blank_col == 3:
            blank_index = self.blank_row * self.m + self.blank_col  # 7
            target = blank_index - 2 * self.m + 1  # 0
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.m, self.goal1, self.goal2, self.cost_function, parent=self,
                               action="Bottom_Right_Corner_Opposed_Diag",
                               cost=self.cost + 3, movement_cost=3, tile=self.config[target])

    def expand(self):
        """expand the node"""
        global UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT
        if len(self.children) == 0:
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

    def is_goal(self):
        if list(self.config) == self.goal1:
            return True
        elif list(self.config) == self.goal2:
            return True
        else:
            return False

    def __lt__(self, other):
        return self.cost_function(self) < self.cost_function(other)

    def __le__(self, other):
        return self.cost_function(self) <= self.cost_function(other)