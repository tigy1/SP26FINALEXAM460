# The Torchbearer

**Student Name:** Henry To
**Student ID:** 132564767
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis
- **Why a single shortest-path run from S is not enough:**
  - A single shortest-path run is not enough, because the problem requires you to traverse through specific nodes, specified in M, that a shortest-path solution from S to the end T may not pass through. This relic node condition may necessitate a more unoptimal path solution before reaching the end.

- **What decision remains after all inter-location costs are known:**
  - We need to figure out in which order is most optimal to visit all the relic nodes that will result in a shortest cost path

- **Why this requires a search over orders (one sentence):**
  - Because each different chosen order in picking relics produces different costs that seem unintuitive to pick out
  - Therefore, we must search over the different orders in order to find the best one

---

## Part 2: Precomputation Design

### Part 2a: Source Selection
| Source Node Type | Why it is a source |
|---|---|
| Entrance (S) | This is the set starting point that you need to start all runs at. |
| Relic (M[i]) | Each relic is a source because it serves as a checkpoint where you can calculate and compare the distance from it to other relics or the end. |

### Part 2b: Distance Storage
| Property | Your answer |
|---|---|
| Data structure name | Dictionary |
| What the keys represent | Each node in the dungeon/graph |
| What the values represent | Shortest distance from entrace node to each key node |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | O(1) because dictionary is a hashmap where each access with a Key is O(1) time complexity |

### Part 2c: Precomputation Complexity
- **Number of Dijkstra runs:** 
  - Number of relics (|M|) + 1
- **Cost per run:** 
  - O((V+E)log V)
- **Total complexity:** 
  - O((V+E)log V * (|M| + 1))
- **Justification (one line):** 
  - This is because we'll be running dijkstras algorithm for the entrance and all relic nodes to traverse from one to the other until the end

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means
- **For nodes already finalized (in S):**
  - This means that the cost of the node in dist['v'] is the smallest distance cost from the start node 

- **For nodes not yet finalized (not in S):**
  - The cost of the nodes not yet finalized signifies the lowest cost or shortest path to that node from all nodes visited so far

### Part 3b: Why Each Phase Holds
- **Initialization : why the invariant holds before iteration 1:**
  - Before the iteration, there is no finalized nodes as no nodes have been seen yet except for the starting node
  - Therefore, the starting node will be finalized and have cost 0 because that's where you're starting, and all other unfinalized nodes have cost infinity because there's no possible way to traverse to those nodes, which still qualifies as the shortest path from all nodes visited so far

- **Maintenance : why finalizing the min-dist node is always correct:**
  - Finalizing the min-dist node is always correct, since because each node only adds non-negative weight, the cost of traversal is either only maintained or increasing
  - Therefore, if that node is the minimum distance node currently seen, all other paths have equal or higher cost, meaning that no shorter path to that node could be found later 

- **Termination : what the invariant guarantees when the algorithm ends:**
  - At termination, every node will be finalized, so the cost of every node signifies the shortest path distance to get to that node from the starting node

### Part 3c: Why This Matters for the Route Planner
- Having correct distances ensures that the relics routed are truly minimized in their distances between eachother, and the opposite would lead to unoptimized nodal paths or a minimized cost route

---

## Part 4: Search Design

### Why Greedy Fails
- **The failure mode:** 
  - The greedy algorithm in this case is to choose the path to the next lowest cost relic available from one's current location
- **Counter-example setup:**
  - Start at S and assume there are two relics
  - From S, let distance to R_1 be 1 and distance to R_2 be 2
  - From R_1, let the distance to R_2 be 50 and R_1 to T be 1
  - From R_2, let the distance to R_1 be 1 and R_2 to T be 1
- **What greedy picks:**
  - Greedy picks the route to R_1 because its the lowest immediate cost of 1 over cost of 2
  - Then, it's forced to traverse from R_1 to R_2 with the cost of 50
  - Finally, once it finishes the traversal to T, the final cost is 52
- **What optimal picks:** 
  - The optimal solution chooses to pick up relic R_2 first with a cost of 2
  - Then it traverses to relic R_1 with a cost of 1
  - Finally, it finishes the traversal to T with the final cost being 4
- **Why greedy loses:** 
  - The greedy solution fails because picking the local optimal doesn't guarantee a global optimal solution
  - Early choices can affect how later choices play out and block one from optimal solutions
  - With this framework, this is why a greedy algorithm isn't the best choice for this type of problem

### What the Algorithm Must Explore
- The algorithm must explore all possible different combinations of orders in picking the relics so that the minimum cost path can be chosen

---

## Part 5: State and Search Space

### Part 5a: State Representation
| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | node | The current node along any path that you're on, including any relics or the entrance |
| Relics already collected | relics_visited_order | list | The local list of relics storing the nodes that you've visited along the path currently traversing |
| Fuel cost so far | cost_so_far | int | the cost it takes to get to current node |

### Part 5b: Data Structure for Visited Relics
| Property | Your answer |
|---|---|
| Data structure chosen | set |
| Operation: check if relic already collected | Time complexity: O(1) |
| Operation: mark a relic as collected | Time complexity: O(1) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) |
| Why this structure fits | This structure fits because there's only a unique number of relics, so every time you visit, you can remove it from the set, allowing for marking/unmarking cleanly |

### Part 5c: Worst-Case Search Space
- **Worst-case number of orders considered:**
  - O(k!)
- **Why:**
  - The worst case is the case where you traverse through all combinations of relics, when each path gives a more optimal cost and nothing is pruned

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking
- **What is tracked:** 
  - Cost of lowest cost route so far and traversal path of lowest cost route
- **When it is used:** 
  - It is used before the recursive loop to compare against the cost of the current path checked
- **What it allows the algorithm to skip:**
  - Because of this, it allows the algorithm to skip exploring paths that already cost as much or more than the best solution found so far

### Part 6b: Lower Bound Estimation
- **What information is available at the current state:**
  - The current location, the relics remaining to visit, and the current accumulated travel cost
- **What the lower bound accounts for:** 
  - The current cost of the partial path being traversed
- **Why it never overestimates:**
  - Because traveling to other nodes only adds cost, the current cost can only be maintained or increased, meaning that the optimal path can never be pruned or fail to be achieved

### Part 6c: Pruning Correctness
- Pruning is safe because all distances are nonnegative, so continuing along a path can only increase or maintain the current cost
- If a partial route already costs as much or more than the best complete route found so far, it can't possibly lead to a more optimal solution

---

## References
- Lecture notes