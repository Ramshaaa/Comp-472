from utils.priority_queue import PriorityQueue
import queue


def UCS(initial_state, heuristic):
    """UCS search"""
    frontier = PriorityQueue('min', heuristic)
    frontier.append(initial_state)
    frontier_config = {}
    frontier_config[tuple(initial_state.config)] = True
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0
    search_path = []

    while frontier:
        state = frontier.pop()
        print("****** State ******")
        state.display()
        explored.add(state)
        search_path.append(state)
        if state.is_goal():
            return state, nodes_expanded, max_search_depth, search_path

        nodes_expanded += 1
        for neigbhor in state.expand(RLDU=False):
            if neigbhor not in explored and tuple(neigbhor.config) not in frontier_config:
                frontier.append(neigbhor)
                frontier_config[tuple(neigbhor.config)] = True
                if neigbhor.cost > max_search_depth:
                    max_search_depth = neigbhor.cost
            elif neigbhor in frontier:
                if heuristic(neigbhor) < frontier[neigbhor]:
                    frontier.__delitem__(neigbhor)
                    frontier.append(neigbhor)
    return None


def GBFS(initial_state, heuristic):
    """GBFS search"""
    frontier = PriorityQueue('min', heuristic)
    frontier.append(initial_state)
    frontier_config = {}
    frontier_config[tuple(initial_state.config)] = True
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0
    search_path = []

    while frontier:
        state = frontier.pop()
        print("****** State ******")
        state.display()
        explored.add(state)
        search_path.append(state)
        if state.is_goal():
            return state, nodes_expanded, max_search_depth, search_path

        nodes_expanded += 1
        for neigbhor in state.expand(RLDU=False):
            if neigbhor not in explored and tuple(neigbhor.config) not in frontier_config:
                frontier.append(neigbhor)
                frontier_config[tuple(neigbhor.config)] = True
                if neigbhor.cost > max_search_depth:
                    max_search_depth = neigbhor.cost
            elif neigbhor in frontier:
                if heuristic(neigbhor) < frontier[neigbhor]:
                    frontier.__delitem__(neigbhor)
                    frontier.append(neigbhor)
    return None


def A_STAR(initial_state, heuristic):
    """A * search"""
    frontier = PriorityQueue('min', heuristic)
    frontier.append(initial_state)
    frontier_config = {}
    frontier_config[tuple(initial_state.config)] = True
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0
    search_path = []

    while frontier:
        state = frontier.pop()
        print("****** State ******")
        state.display()
        explored.add(state)
        search_path.append(state)
        if state.is_goal():
            return state, nodes_expanded, max_search_depth, search_path

        nodes_expanded += 1
        for neigbhor in state.expand(RLDU=False):
            if neigbhor not in explored and tuple(neigbhor.config) not in frontier_config:
                frontier.append(neigbhor)
                frontier_config[tuple(neigbhor.config)] = True
                if neigbhor.cost > max_search_depth:
                    max_search_depth = neigbhor.cost
            elif neigbhor in frontier:
                if heuristic(neigbhor) < frontier[neigbhor]:
                    frontier.__delitem__(neigbhor)
                    frontier.append(neigbhor)
    return None