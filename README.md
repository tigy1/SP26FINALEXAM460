# The Torchbearer

**Student Name:** Henry To
**Student ID:** 132564767
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

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

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** Number of relics + 1
- **Cost per run:** _your answer_
- **Total complexity:** _your answer_
- **Justification (one line):** _your answer_

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  _Your answer here._

- **For nodes not yet finalized (not in S):**
  _Your answer here._

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  _Your answer here._

- **Maintenance : why finalizing the min-dist node is always correct:**
  _Your answer here._

- **Termination : what the invariant guarantees when the algorithm ends:**
  _Your answer here._

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

_Your answer here._

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

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | | | |
| Relics already collected | | | |
| Fuel cost so far | | | |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
