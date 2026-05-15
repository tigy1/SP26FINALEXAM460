"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Henry To
Student ID:   132564767

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq

# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    """
    return ("Why a single shortest-path run from S is not enough: A single shortest-path run is not enough, because the problem requires you to traverse through specific nodes, specified in M, that a shortest-path solution from S to the end T may not pass through"
            "\nWhat decision remains after all inter-location costs are known: We need to figure out in which order is most optimal to visit all the relic nodes that will result in a shortest cost path"
            "\nWhy this requires a search over orders: Because each different chosen order in picking relics produces different costs that seem unintuitive to pick out. Therefore, we must search over the different orders in order to find the best one")

# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    source_list = [0] * (len(relics) + 1)
    source_list[0] = spawn
    for i in range(len(relics)):
        source_list[i + 1] = relics[i]
    return source_list

def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    pq = [(0, source)]
    visited = set()
    res = {}
    while len(pq) is not 0:
        curr = heapq.heappop(pq)
        if curr[1] in visited:
            continue
        visited.add(curr[1])
        res[curr[1]] = curr[0]
        for nodes in graph[curr[1]]:
            if nodes[0] not in visited:
                heapq.heappush(pq, (curr[0] + nodes[1], nodes[0]))
    for node in graph:
        if node not in res:
            res[node] = float('inf')
    return res

def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.
    """
    res = {}
    res[spawn] = run_dijkstra(graph, spawn)
    for relic in relics:
        res[relic] = run_dijkstra(graph, relic)
    return res

# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    """
    return ("For nodes already finalized (in S): This means that the cost of the node in dist['v'] is the smallest distance cost from the start node"
            "\nFor nodes not yet finalized (not in S): The cost of the nodes not yet finalized signifies the lowest cost or shortest path to that node from all nodes visited so far"
            "\nInitialization : why the invariant holds before iteration 1: Before the iteration, there is no finalized nodes as no nodes have been seen yet except for the starting node. Therefore, the starting node will be finalized and have cost 0 because that's where you're starting, and all other unfinalized nodes have cost infinity because there's no possible way to traverse to those nodes, which still qualifies as the shortest path from all nodes visited so far"
            "\nMaintenance : why finalizing the min-dist node is always correct: Finalizing the min-dist node is always correct, since because each node only adds non-negative weight, the cost of traversal is either only maintained or increasing. Therefore, if that node is the minimum distance node currently seen, all other paths have equal or higher cost, meaning that no shorter path to that node could be found later"
            "\nTermination : what the invariant guarantees when the algorithm ends: At termination, every node will be finalized, so the cost of every node signifies the shortest path distance to get to that node from the starting node"
            "\nWhy This Matters for the Route Planner: Having correct distances ensures that the relics routed are truly minimized in their distances between eachother, and the opposite would lead to unoptimized nodal paths or a minimized cost route")


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    """
    return ("The failure mode: The greedy algorithm in this case is to choose the path to the next lowest cost relic available from one's current location."
            "\nCounter-example setup: Start at S and assume there are two relics. From S, let distance to R_1 be 1 and distance to R_2 be 2. From R_1, let the distance to R_2 be 50 and R_1 to T be 1. From R_2, let the distance to R_1 be 1 and R_2 to T be 1."
            "\nWhat greedy picks: Greedy picks the route to R_1 because its the lowest immediate cost of 1 over cost of 2. Then, it's forced to traverse from R_1 to R_2 with the cost of 50. Finally, once it finishes the traversal to T, the final cost is 52."
            "\nWhat optimal picks: The optimal solution chooses to pick up relic R_2 first with a cost of 2. Then it traverses to relic R_1 with a cost of 1. Finally, it finishes the traversal to T with the final cost being 4."
            "\nWhy greedy loses: The greedy solution fails because picking the local optimal doesn't guarantee a global optimal solution. Early choices can affect how later choices play out and block one from optimal solutions. With this framework, this is why a greedy algorithm isn't the best choice for this type of problem."
            "\nWhat the Algorithm Must Explore: The algorithm must explore all possible different combinations of orders in picking the relics so that the minimum cost path can be chosen")


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """ 
    best = [float('inf'), []]
    _explore(dist_table, spawn, set(relics), [], 0, exit_node, best)
    return best

def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float (signifies lowest cost)
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.
    
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    if not relics_remaining:
        cost_so_far += dist_table[current_loc][exit_node]
        if cost_so_far < best[0]:
            best[1] = relics_visited_order.copy()
            best[0] = cost_so_far
        return
    # The pruning condition is below
    # This cannot skip the optimal solution, because if the current path costs the same or more to traverse than
    # the best path seen so far, and traversing only adds cost, then there's no universe where the current
    # path can be better than the optimal path
    if cost_so_far >= best[0]:
        return
    for relic in list(relics_remaining):
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)
        _explore(dist_table, relic, relics_remaining, relics_visited_order, cost_so_far + dist_table[current_loc][relic], exit_node, best)
        relics_remaining.add(relic)
        relics_visited_order.pop()

# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    optimal_route = find_optimal_route(dist_table, spawn, relics, exit_node)
    return optimal_route


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
