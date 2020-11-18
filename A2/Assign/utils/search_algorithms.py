from utils.priority_queue import PriorityQueue
import queue


def UCS(initial_state, heuristic):
    """ UCS search"""
    frontier = queue.Queue()
    frontier.put(initial_state)
    frontier_config = {}
    frontier_config[tuple(initial_state.config)] = True
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0

    while not frontier.empty():
        state = frontier.get()
        print("****** State ******")
        state.display()
        explored.add(state.config)
        if state.is_goal():
            return state, nodes_expanded, max_search_depth

        nodes_expanded += 1
        for neighbor in state.expand(RLDU=False):
            if neighbor.config not in explored and tuple(neighbor.config) not in frontier_config:
                frontier.put(neighbor)
                frontier_config[tuple(neighbor.config)] = True
                if neighbor.cost > max_search_depth:
                    max_search_depth = neighbor.cost
    return None


def GBFS(initial_state, heuristic):
    """GBFS search"""
    frontier = queue.LifoQueue()
    frontier.put(initial_state)
    frontier_config = {}
    frontier_config[tuple(initial_state.config)] = True
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0

    while not frontier.empty():
        state = frontier.get()
        print("****** State ******")
        state.display()
        explored.add(state.config)
        if state.is_goal():
            return state, nodes_expanded, max_search_depth

        nodes_expanded += 1
        for neighbor in state.expand():
            if neighbor.config not in explored and tuple(neighbor.config) not in frontier_config:
                frontier.put(neighbor)
                frontier_config[tuple(neighbor.config)] = True
                if neighbor.cost > max_search_depth:
                    max_search_depth = neighbor.cost
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

    while frontier:
        state = frontier.pop()
        print("****** State ******")
        state.display()
        explored.add(state)
        if state.is_goal():
            return state, nodes_expanded, max_search_depth

        nodes_expanded += 1
        for neighbor in state.expand(RLDU=False):
            if neighbor not in explored and tuple(neighbor.config) not in frontier_config:
                frontier.append(neighbor)
                frontier_config[tuple(neighbor.config)] = True
                if neighbor.cost > max_search_depth:
                    print("hey")
                    max_search_depth = neighbor.cost
            elif neighbor in frontier:
                if heuristic(neighbor) < frontier[neighbor]:
                    frontier.__delitem__(neighbor)
                    frontier.append(neighbor)
    return None
