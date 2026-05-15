# Development Log – The Torchbearer

**Student Name:** Henry To
**Student ID:** 132564767

---

## Entry 1 – [5/9/2026]: Initial Plan
I plan to do much of the README first to establish a solid theory understanding of the problem at hand. The two parts that I expect to be the hardest are implementing the functions for dikjstras and using backtracking & recursion to traverse the labrynth to achieve an optimal answer.

---

## Entry 2 – [5/14/2026]: Implementing "_explore" Problems
A wrong assumption that I initially had when writing the helper method "_explore" was that the variable "cost_so_far" would be used to display the best cost path, and that I was only calculating the current path's cost once all relics were traversed in order to compare with the cheapest cost so far. This came with a few problems: first, I couldn't treat an immutable variable as a global updatable variable, and updating "cost_so_far" wouldn't allow other stack frames to use this data to compare to the current path's cost. Also, calculating the path's cost at the end blocked optimizing the algorithm with pruning, as I couldn't check the cost of the path along the way. I resolved this issue by treating "cost_so_far" as a current cost variable and also storing the best cost within the "best" list in its first index, and stored the best path as an embedded list in the list's second index, allowing for global updates and live-time local path cost tracking.

---

## Entry 3 – [5/14/2026]: Post-Implementation Reflection
I think there could be a much better solution to mine in finding the optimal path, in which O(k!) worst case is not achieved. Given more time, I would try to improve the search using dynamic programming or memoization so repeated subproblems are not recomputed, because there could potentially be a way to prevent reuse of the same subpaths.

---

## Final Entry – [5/14/2026]: Time Estimate
| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 1 |
| Part 2: Precomputation Design | .75 |
| Part 3: Algorithm Correctness | 1 |
| Part 4: Search Design | 1 |
| Part 5: State and Search Space | .5 |
| Part 6: Pruning | .5 |
| Part 7: Implementation | 3 |
| README and DEVLOG writing | 1 |
| **Total** | 8.75 |
