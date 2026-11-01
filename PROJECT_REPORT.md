# KPR INSTITUTE OF ENGINEERING AND TECHNOLOGY
## Department of Artificial Intelligence and Data Science
### Academic Year 2026–2027 | II Year, Section C
### Course: Data Structures and Algorithms (Units III, IV and V)
### ASSIGNMENT II: PROJECT-BASED ASSESSMENT REPORT

---

# PROJECT 19: SUPPLY CHAIN MANAGER
### *Multimodal Logistics Routing, Production Scheduling, and Hierarchical Inventory Management*

**Project Lead & Lead Developer:** **LOGITH P** ([GitHub: @LOGITHP](https://github.com/LOGITHP))  
**Team Members (Register Numbers):**
1. **LOGITH P** — System Architecture, Complete Implementation & Integration
2. **25AD064** — Tree Data Structures (General Tree, BST, AVL) & Inventory Subsystem
3. **25AD086** — Graph Algorithms (Dijkstra, Prim, Kruskal, Disjoint Set) & Multimodal Routing
4. **25AD111** — Scheduling (Kahn, DFS, Critical Path Method) & Expression Calculator
5. **25AD205** — Empirical Benchmarking, Asymptotic Derivations & Test Automation

**Language of Implementation:** Python 3.12 (Strictly from first principles; zero built-in tree, graph, or priority-queue libraries used).

---

## 1. Problem Statement & Scenario Description

In modern industrial supply chains, managing goods from raw material procurement to multi-depot shipping requires a composite algorithmic infrastructure. A supply chain manager must solve four interconnected computational challenges:

1. **Hierarchical Categorization & Rapid Inventory Lookups (Unit III):**
   - Products are categorized hierarchically (Division $\to$ Category $\to$ Subcategory $\to$ Product Line) represented as an $n$-ary General Tree.
   - Active stock is indexed by numeric Stock Keeping Unit (SKU) IDs in a Binary Search Tree (BST) supporting range queries ($a \le \text{SKU} \le b$), dynamic updates, and successor/predecessor lookups.
   - Certified suppliers must be indexed by Supplier ID in a strictly height-balanced self-balancing AVL Tree to guarantee $O(\log n)$ worst-case lookups regardless of insertion order.
   - Dynamic freight tariffs, fuel surcharges, and tax levies must be evaluated on the fly using postfix Expression Trees that output human-readable infix notation with minimal parentheses.

2. **Multimodal Transport Network & Routing Optimization (Unit IV):**
   - A logistics network spanning 13 major nationwide depots is modeled as a weighted Graph with switchable representations (Adjacency List for memory efficiency on sparse routes and Adjacency Matrix for fast dense lookups).
   - Shortest transit paths are computed via an array-based Dijkstra's algorithm with step-by-step distance table logging.
   - Minimal transit stops are resolved via Breadth-First Search (BFS).
   - Minimum cabling and inter-hub connection costs are optimized using both Prim's and Kruskal's algorithms, generating a Minimum Spanning Forest when maritime depots (such as Port Blair Island) are isolated.

3. **Manufacturing Workflow & Critical Path Scheduling (Unit IV):**
   - Production involves sequential stages with task durations. Precedence constraints are modeled as a Directed Acyclic Graph (DAG).
   - Valid assembly sequences are computed via Kahn's algorithm and DFS topological sort.
   - Critical Path Method (CPM) identifies Earliest Start Time (EST), Latest Start Time (LST), and Slack, pinpointing the bottleneck tasks that determine total project duration. Circular quality feedback loops are detected via cycle-detection algorithms.

4. **Empirical vs. Theoretical Algorithm Analysis (Unit V):**
   - Theoretical Big-$O$, Big-$\Omega$, and Big-$\Theta$ bounds are derived from first principles.
   - Systematic empirical experiments ($n \in \{1k, 5k, 20k\}$ for trees and $V \in \{200, 1k, 2k\}$ for graphs) confirm the theoretical growth ratios and establish when specific algorithms (e.g., Kruskal vs. Prim) outperform each other.

---

## 2. System Architecture & Abstract Data Types (ADTs)

The system is structured into four distinct decoupled packages:

```
DSA/
├── structures/             # Custom Abstract Data Types (No external libraries)
│   ├── common_utils.py     # Custom Stack, Queue (O(1) linked), and MergeSort
│   ├── general_tree.py     # n-ary Product Category Tree (Recursive & Iterative)
│   ├── bst.py              # Inventory SKU BST (CRUD, 3-case delete, Range Query)
│   ├── avl_tree.py         # Self-balancing Supplier AVL (LL, RR, LR, RL, verify())
│   ├── expression_tree.py  # Tariff Syntax Tree (Minimal parens, robust errors)
│   ├── disjoint_set.py     # Union-Find with Path Compression & Union by Rank
│   └── graph.py            # Graph ADT (Matrix & List switchable, BFS, DFS, SCC)
├── algorithms/             # Routing, Optimization & Scheduling Engines
│   ├── dijkstra.py         # Array-based Dijkstra, Step Table, Negative-edge Demo
│   ├── mst.py              # Array-based Prim & Kruskal (MergeSort + DSU)
│   └── scheduling.py       # Kahn's, DFS Top-Sort, CPM (EST, LST, Slack, Critical Path)
├── simulation/             # Benchmarks, Datasets & Automated Verification
│   ├── supply_chain_data.py# 13-depot network, production stages DAG, random generator
│   ├── benchmarks.py       # Unit V empirical timing suite & doubling ratio analysis
│   └── test_suite.py       # 18 automated self-tests cross-checking correctness
├── theory/                 # Reference mathematical proofs & recurrences
│   └── theoretical_proofs.py
└── main.py                 # Interactive 11-option console user interface
```

### 2.1 Custom Elementary Structures
- **Custom `Stack` (LIFO):** Implemented via singly linked `StackNode` elements. Push, pop, and peek execute in strict $O(1)$ time without relying on Python's `collections.deque` or `list.pop()`.
- **Custom `Queue` (FIFO):** Implemented via head and tail pointers on linked `QueueNode` items. Enqueue and dequeue execute in deterministic $O(1)$ time.
- **Custom `MergeSort`:** Comparison-based out-of-place sorting algorithm implemented recursively from scratch ($O(E \log E)$ worst-case time, $O(E)$ space).

---

## 3. Core Algorithm Designs & Pseudocode

### 3.1 AVL Tree Deletion & Rebalancing Pseudocode

When a node $z$ is deleted from an AVL tree, the standard BST deletion is performed first, followed by an upward traversal updating heights and applying rotations:

```text
Algorithm AVL_Delete(node, key):
    1. If node is NULL: return NULL
    2. If key < node.key:
           node.left = AVL_Delete(node.left, key)
       Else if key > node.key:
           node.right = AVL_Delete(node.right, key)
       Else:
           // Node found! Handle 3 delete cases:
           If node.left is NULL: return node.right
           Else if node.right is NULL: return node.left
           Else:
               succ = Find_Min(node.right)
               node.key = succ.key
               node.data = succ.data
               node.right = AVL_Delete(node.right, succ.key)

    3. If node is NULL: return NULL
    4. node.height = 1 + max(Height(node.left), Height(node.right))
    5. balance = Height(node.left) - Height(node.right)

    // Rebalance 4 Rotation Cases:
    6. If balance > 1 and Get_Balance(node.left) >= 0:
           return Rotate_Right(node)                  // LL Case
    7. If balance > 1 and Get_Balance(node.left) < 0:
           node.left = Rotate_Left(node.left)
           return Rotate_Right(node)                  // LR Case
    8. If balance < -1 and Get_Balance(node.right) <= 0:
           return Rotate_Left(node)                   // RR Case
    9. If balance < -1 and Get_Balance(node.right) > 0:
           node.right = Rotate_Right(node.right)
           return Rotate_Left(node)                   // RL Case

    10. Return node
```

### 3.2 Array-Based Dijkstra's Shortest Path Pseudocode

```text
Algorithm Array_Dijkstra(Graph G, Source s):
    Input: Graph G = (V, E) with non-negative weights, source vertex s
    Output: dist[] array, parent[] array, step_table[] log

    1. For each v in V:
           dist[v] = infinity
           visited[v] = false
           parent[v] = NULL
    2. dist[s] = 0

    3. Repeat |V| times:
           min_dist = infinity
           u = NULL
           // Linear array scan for minimum unvisited vertex:
           For each v in V:
               If not visited[v] and dist[v] < min_dist:
                   min_dist = dist[v]
                   u = v

           If u is NULL or min_dist == infinity:
               Break // Remaining nodes unreachable

           visited[u] = true
           Record step in step_table

           // Edge relaxation:
           For each neighbor (v, weight) of u:
               If not visited[v]:
                   new_dist = dist[u] + weight
                   If new_dist < dist[v]:
                       dist[v] = new_dist
                       parent[v] = u

    4. Return dist, parent, step_table
```

### 3.3 Disjoint Set Union (DSU) with Path Compression & Union by Rank

```text
Algorithm Make_Set(x):
    parent[x] = x
    rank[x] = 0

Algorithm Find(x):
    If parent[x] != x:
        parent[x] = Find(parent[x]) // Two-pass Path Compression
    Return parent[x]

Algorithm Union(x, y):
    root_x = Find(x)
    root_y = Find(y)
    If root_x == root_y:
        Return false // Cycle detected; already connected

    // Union by rank:
    If rank[root_x] < rank[root_y]:
        parent[root_x] = root_y
    Else if rank[root_x] > rank[root_y]:
        parent[root_y] = root_x
    Else:
        parent[root_y] = root_x
        rank[root_x] = rank[root_x] + 1
    Return true
```

### 3.4 Critical Path Method (CPM) Forward & Backward Pass

```text
Algorithm Compute_CPM(DAG G, durations D):
    1. topo_order = Topological_Sort_Kahn(G)
    2. If cycle detected: Raise CycleException

    // Forward Pass:
    3. For each u in topo_order:
           EST[u] = max_{(p, u) in E} (EFT[p]), or 0 if no predecessors
           EFT[u] = EST[u] + D[u]
    4. Project_Duration T = max_{u} (EFT[u])

    // Backward Pass:
    5. For each u in reverse(topo_order):
           LFT[u] = min_{(u, s) in E} (LST[s]), or T if no successors
           LST[u] = LFT[u] - D[u]

    // Slack and Critical Path:
    6. For each u in topo_order:
           Slack[u] = LST[u] - EST[u]
           Is_Critical[u] = (Slack[u] == 0)

    7. Trace Critical Path sequence from start node to end node where Slack == 0.
```

---

## 4. Unit IV: Graph & Network Structural Analysis

### 4.1 Logistics Depot Topology (13 Depots)
The pre-configured dataset contains 13 logistics depots strategically positioned across India:
- **Major Hubs:** Mumbai (`MUM`), Delhi (`DEL`), Bengaluru (`BLR`), Chennai (`CHE`), Kolkata (`KOL`), Hyderabad (`HYD`), Pune (`PUN`), Ahmedabad (`AHM`), Jaipur (`JAI`), Lucknow (`LKO`), Nagpur (`NAG`), Kochi (`KOC`).
- **Disconnected Area:** Port Blair Island Depot (`IXZ`). Isolated by sea, validating that MST algorithms yield a Spanning Forest of 2 components.
- **One-Way Priority Corridor:** Mumbai to Pune (`MUM` $\to$ `PUN`, 150 km priority transit link), ensuring directed edges are tested.

### 4.2 Representation Memory Footprint Comparison

| Metric | Adjacency Matrix ($V \times V$) | Adjacency List ($V + E$) |
| :--- | :--- | :--- |
| **Theoretical Storage** | $\Theta(V^2)$ pointers / floats | $\Theta(V + E)$ nodes / tuples |
| **For $V=13, E=16$** | 1,352 Bytes theoretical | 616 Bytes theoretical |
| **For $V=1000, E=2000$ (Sparse)** | 8,000,000 Bytes ($8.0$ MB) | 40,000 Bytes ($0.04$ MB) |
| **For $V=1000, E=250,000$ (Dense)** | 8,000,000 Bytes ($8.0$ MB) | 4,008,000 Bytes ($4.0$ MB) |
| **Edge Lookup Time** | $\Theta(1)$ direct indexed access | $O(\text{deg}(u))$ list traversal |
| **Neighbor Iteration** | $\Theta(V)$ must scan row | $\Theta(\text{deg}(u))$ exact neighbors |

### 4.3 DFS Discovery/Finish Times & Edge Classification
Running Depth-First Search on the logistics network produces 4 edge classifications based on node visitation timestamps $[d/f]$:
1. **Tree Edges:** Edges $(u, v)$ discovering an unvisited (white) vertex $v$.
2. **Back Edges:** Edges $(u, v)$ pointing to an ancestor currently on the recursion stack (gray vertex). Indicates presence of cycles.
3. **Forward Edges:** Edges $(u, v)$ pointing to a descendant already fully explored (black vertex) where $d[u] < d[v]$.
4. **Cross Edges:** Edges $(u, v)$ connecting branches in different DFS subtrees where $d[u] > d[v]$.

### 4.4 Why Dijkstra Fails on Negative Weight Edges

Dijkstra's algorithm is built on the **Greedy Choice Property**: once vertex $u$ is chosen from the unvisited set with minimum distance $\text{dist}[u]$, its shortest path is assumed permanently settled.

**Concrete Counterexample:**
```text
      (3)
  A --------> B
   \         ^
(5) \       / (-4)
     v     /
        C
```
- True Shortest Path from $A$ to $B$: $A \to C \to B$ with total cost $5 + (-4) = 1.0$.
- **Dijkstra's Execution:**
  - Step 1: Settles $A$ ($\text{dist}[A] = 0$). Unvisited keys: $\text{dist}[B] = 3$, $\text{dist}[C] = 5$.
  - Step 2: Picks minimum unvisited: $B$ ($\text{dist}[B] = 3$). Vertex $B$ is marked **VISITED** and settled!
  - Step 3: Settles $C$ ($\text{dist}[C] = 5$). Examines edge $C \to B$ with weight $-4$.
    New potential distance: $5 + (-4) = 1$.
    However, because $B$ is already settled, Dijkstra's algorithm ignores $B$, refusing to relax it.
  - Output: Dijkstra reports path $A \to B$ with cost $3.0$, which is **sub-optimal**!

---

## 5. Unit V: Algorithm Analysis, Derivations & Proofs

### 5.1 Algorithm Design Technique Classification

| Algorithm | Problem Domain | Design Technique | Optimal Substructure? |
| :--- | :--- | :--- | :--- |
| **BFS (Fewest Stops)** | Unweighted Shortest Path | Graph Traversal (Queue) | Yes |
| **DFS Edge Classification** | Structural Decomposition | Backtracking / Traversal | Yes |
| **Tarjan's SCC** | Strongly Connected Components | Depth-First Search | Yes |
| **Dijkstra (Array)** | Single-Source Shortest Path | Greedy Method | Yes |
| **Prim's Algorithm** | Minimum Spanning Tree | Greedy Method (Cut Property) | Yes |
| **Kruskal's Algorithm**| Minimum Spanning Tree | Greedy Method (Cycle Property)| Yes |
| **Kahn's Algorithm** | Topological Sort | Decrease & Conquer | Yes |
| **Critical Path Method** | DAG Scheduling / Longest Path | Dynamic Programming | Yes |
| **AVL Balancing** | Self-Balancing Search Index | Divide & Conquer | Yes |

### 5.2 Correctness Arguments for Prim & Kruskal (Cut & Cycle Properties)

#### The Cut Property (Prim's Algorithm)
Let $G = (V, E)$ be a connected, weighted, undirected graph. Let $S \subset V$ be an arbitrary subset of vertices defining a cut $(S, V - S)$. If edge $e = (u, v)$ is a light edge crossing $(S, V - S)$ (i.e., has minimum weight among all edges with $u \in S$ and $v \in V - S$), then $e$ belongs to some Minimum Spanning Tree of $G$.

*Proof:*
Let $T$ be an MST that does not contain $e$. Adding $e$ to $T$ produces a cycle $C$. Because $e$ connects $S$ to $V - S$, the cycle must cross the cut at least once more via another edge $e' = (x, y)$. Consider $T' = (T \setminus \{e'\}) \cup \{e\}$. Since $e$ is a light edge crossing the cut, $w(e) \le w(e')$. Therefore, $w(T') = w(T) - w(e') + w(e) \le w(T)$. Since $T$ is an MST, $w(T') = w(T)$, proving $T'$ is also an MST containing $e$. Because Prim's algorithm always selects a light edge crossing the cut $(S, V - S)$ where $S$ is the settled set, every edge picked is guaranteed to belong to an MST.

#### The Cycle Property (Kruskal's Algorithm)
Let $C$ be any simple cycle in $G = (V, E)$, and let $e$ be the strictly heaviest edge in $C$. Then $e$ cannot belong to any Minimum Spanning Tree of $G$.

*Proof:*
Suppose for contradiction that $e$ belongs to an MST $T$. Deleting $e$ from $T$ partitions the vertices into two components $S$ and $V - S$. The remaining edges in $C \setminus \{e\}$ form an alternative path between the endpoints of $e$ and must cross the cut $(S, V - S)$ via at least one edge $e'$. Since $e$ was strictly heaviest in cycle $C$, $w(e') < w(e)$. Construct $T' = (T \setminus \{e\}) \cup \{e'\}$. Then $w(T') = w(T) - w(e) + w(e') < w(T)$, which contradicts the minimality of $T$. Hence, the heaviest edge on any cycle cannot belong to any MST. Kruskal's algorithm, by sorting edges and rejecting any edge that closes a cycle, strictly avoids including the heaviest edge in any cycle.

### 5.3 Non-Recursive Operation Counting Derivations

1. **BFS on Adjacency List:**
   - Queue setup and visited array initialization: $c_1 V$ operations.
   - Enqueue/Dequeue: Each vertex is enqueued and dequeued exactly once: $2 c_2 V$ operations.
   - Neighbor iteration: Loop runs $\sum_{u \in V} \text{deg}(u) = 2E$ times.
   - Total elementary operations: $T(V, E) = c_1 V + 2 c_2 V + c_3 (2E) = \Theta(V + E)$.

2. **Array-Based Dijkstra:**
   - Distance array initialization: $\Theta(V)$.
   - Outer loop executes exactly $V$ times.
   - In each iteration, a linear scan finds the minimum unvisited vertex:
     $$\sum_{i=1}^{V} V = V^2 \text{ comparisons}.$$
   - Total edge relaxations across all iterations: $\sum_{u \in V} \text{out-deg}(u) = E$.
   - Total cost: $T(V, E) = \Theta(V^2 + E) = \Theta(V^2)$.
   - *Preference:* Optimal for dense graphs where $E \approx V^2$, avoiding binary heap overhead ($O(E \log V)$).

3. **Array-Based Prim:**
   - Outer loop executes $V$ times.
   - Key array linear scan: $V \times V = V^2$ comparisons.
   - Key relaxations: $\sum \text{deg}(u) = 2E$.
   - Total cost: $\Theta(V^2)$. Optimal for dense graphs.

4. **Kruskal's Algorithm (MergeSort + DSU):**
   - Edge Sorting via MergeSort: $\Theta(E \log E)$ comparisons.
   - DSU Operations: $V$ `make_set` calls, $2E$ `find` calls, and $V - 1$ `union` calls.
   - With Path Compression and Union by Rank, each DSU operation takes $O(\alpha(V))$ amortized time.
   - Total cost: $\Theta(E \log E + E \cdot \alpha(V)) = \Theta(E \log E) = \Theta(E \log V)$.
   - *Preference:* Vastly superior for sparse graphs ($E \approx 2V$), where $E \log E \approx 2V \log V \ll V^2$.

### 5.4 Recursive Analysis & Recurrences

1. **Tree Traversal Recurrence:**
   $$T(n) = T(k) + T(n - k - 1) + c$$
   For a balanced binary tree ($k = n/2$):
   $$T(n) = 2 T(n/2) + c$$
   By Master Theorem ($a = 2, b = 2, f(n) = c = O(n^0)$):
   $$n^{\log_b a} = n^{\log_2 2} = n^1 \implies T(n) = \Theta(n).$$

2. **BST Insertion Recurrences:**
   - **Best Case (Balanced partition):**
     $$T(n) = T(n/2) + c \implies T(n) = \Theta(\log n).$$
   - **Worst Case (Sorted input):**
     $$T(n) = T(n - 1) + c \implies T(n) = \sum_{i=1}^n c = \Theta(n).$$
     Total time to insert $n$ sorted keys is $\sum_{i=1}^n i = \Theta(n^2)$.
   - **Average Case (Uniform random keys):**
     $$T(n) = \frac{1}{n} \sum_{k=0}^{n-1} [T(k) + T(n - 1 - k)] + c = \frac{2}{n} \sum_{k=0}^{n-1} T(k) + c.$$
     Solving via telescoping differences yields $T(n) = 2(n + 1) H_n \approx 1.386 \log_2 n = \Theta(\log n)$.

### 5.5 Formal Proof: AVL Tree Height is $O(\log n)$

**Theorem:** An AVL tree containing $n$ nodes has height $h \le 1.4404 \log_2(n + 2) - 0.328 = O(\log n)$.

*Proof:*
Let $N(h)$ be the minimum number of nodes in an AVL tree of height $h$.
- Base Cases: $N(0) = 0$, $N(1) = 1$, $N(2) = 2$.
- For height $h$, the root must have one child of height $h - 1$ and another of height $h - 2$ (the minimum allowed by the balance condition $|BF| \le 1$):
  $$N(h) = N(h - 1) + N(h - 2) + 1.$$
Adding 1 to both sides:
  $$N(h) + 1 = [N(h - 1) + 1] + [N(h - 2) + 1].$$
Define $S(h) = N(h) + 1$. Then $S(h) = S(h - 1) + S(h - 2)$ with $S(1) = 2 = F(3)$ and $S(2) = 3 = F(4)$.
By induction, $S(h) = F(h + 2)$, which gives:
  $$N(h) = F(h + 2) - 1,$$
where $F(k)$ is the $k$-th Fibonacci number.
Using Binet's formula $F(k) \approx \frac{\phi^k}{\sqrt{5}}$ where $\phi = \frac{1 + \sqrt{5}}{2} \approx 1.618034$:
  $$n \ge N(h) > \frac{\phi^{h + 2}}{\sqrt{5}} - 1 \implies \phi^{h + 2} < \sqrt{5}(n + 1).$$
Taking $\log_\phi$ of both sides:
  $$h + 2 < \log_\phi(\sqrt{5}(n + 1)) = \frac{\log_2(\sqrt{5}(n + 1))}{\log_2(\phi)}.$$
Since $\frac{1}{\log_2(\phi)} = \frac{1}{0.69424} \approx 1.44042$:
  $$h < 1.4404 \log_2(n + 2) = O(\log n). \quad \blacksquare$$

### 5.6 Amortized Analysis of Union-Find & Kruskal Sorting Lower Bound

- **Amortized Bound of Union-Find:**
  Using the potential method $\Phi = \sum_{v \in V} \text{rank\_potential}(v)$, path compression and union by rank ensure that every sequence of $m$ operations on $n$ elements executes in $O(m \cdot \alpha(n))$ time, where $\alpha$ is the Inverse Ackermann function. Since $\alpha(n) \le 4$ for any $n \le 2^{65536}$, each operation has an effective amortized runtime of $O(1)$.
- **Comparison-Based Sorting Lower Bound:**
  Any deterministic comparison-based sort operates as a binary Decision Tree. Sorting $E$ edges requires distinguishing among $E!$ possible permutations, demanding at least $E!$ leaves. A binary tree of height $h$ has at most $2^h$ leaves. Therefore, $2^h \ge E! \implies h \ge \log_2(E!) = \Omega(E \log E)$. Hence, Kruskal's sorting stage cannot run faster than $\Omega(E \log E)$.

---

## 6. Empirical Results & Performance Analysis

### 6.1 Tree Benchmark: BST vs. AVL ($n \in \{1k, 5k, 20k\}$)

| Input Size ($n$) | BST Rand (ms) | BST Rand Height | AVL Rand (ms) | AVL Rand Height | AVL Sorted (ms) | AVL Sorted Height | Max Theoretical AVL Height |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1,000** | 2.40 | 23 | 24.98 | 12 | 26.95 | 10 | 15 |
| **5,000** | 20.66 | 29 | 150.10 | 14 | 123.13 | 13 | 18 |
| **20,000**| 108.52| 36 | 682.40 | 17 | 590.20 | 15 | 21 |

#### Empirical Growth Ratio Analysis:
- When $n$ scales from $1,000$ to $5,000$ ($5.0\times$ increase):
  - Theoretical $O(n \log n)$ Expected Growth: $\frac{5000 \log_2 5000}{1000 \log_2 1000} = \frac{5000 \times 12.29}{1000 \times 9.97} \approx 6.16\times$.
  - AVL Empirical Growth: $\frac{150.10}{24.98} \approx 6.01\times$.
  - **Verdict:** The empirical growth ratio ($6.01\times$) matches the theoretical prediction ($6.16\times$) with $97.6\%$ fidelity!
- **Degeneration on Sorted Input:**
  - Inserting $1,000$ sorted keys into BST results in a degenerate linked list of height $1,000$.
  - In contrast, the AVL tree balances continuously via rotations, maintaining a height of only $10 \le 15$.

### 6.2 Graph Benchmark: Prim vs. Kruskal ($V \in \{200, 1000, 2000\}$)

| Vertices ($V$) | Sparse $E$ | Prim Sparse (ms) | Kruskal Sparse (ms) | Dense $E$ | Prim Dense (ms) | Kruskal Dense (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **200** | 400 | 3.52 | 4.81 | 10,000 | 8.92 | 84.10 |
| **1,000** | 2,000 | 82.40 | 31.20 | 250,000 | 164.50 | 1,842.10 |
| **2,000** | 4,000 | 321.10 | 72.50 | 1,000,000 | 670.30 | 8,950.40 |

#### Performance Crossover & Doubling Ratio Analysis:
1. **Sparse Graphs ($E \approx 2V$):**
   - At $V = 2000, E = 4000$, Kruskal's algorithm ($72.5\text{ ms}$) executes **$4.4\times$ faster** than array-based Prim ($321.1\text{ ms}$).
   - *Why:* Kruskal operates in $O(E \log E) \approx O(V \log V)$, whereas array-based Prim is bound by its $O(V^2)$ unvisited linear scans regardless of edge sparsity.
2. **Dense Graphs ($E \approx V^2 / 4$):**
   - At $V = 1000, E = 250,000$, array-based Prim ($164.5\text{ ms}$) runs **$11.2\times$ faster** than Kruskal ($1,842.1\text{ ms}$).
   - *Why:* Kruskal must sort 250,000 edges ($O(E \log E)$), whereas Prim scans its fixed $V$-length array in $O(V^2)$ without sorting overhead.
3. **Doubling $V$ on Array-based Prim:**
   - Scaling $V$ from $1,000$ to $2,000$ ($2.0\times$ increase):
   - Theoretical $O(V^2)$ ratio: $2^2 = 4.0\times$.
   - Empirical Prim Sparse ratio: $\frac{321.1}{82.4} \approx 3.89\times$.
   - Empirical Prim Dense ratio: $\frac{670.3}{164.5} \approx 4.07\times$.
   - **Verdict:** Confirms quadratic theoretical scaling $\Theta(V^2)$.

---

## 7. Automated Verification & Test Suite Summary

The test harness in `simulation/test_suite.py` executes 18 automated self-tests covering edge cases, invalid inputs, and algorithmic invariants:

| Test ID | Feature Tested | Verification Condition | Result |
| :---: | :--- | :--- | :---: |
| `01` | General Tree Insert & Delete Subtree | Sibling isolation and cascading subtree removal | **PASS** |
| `02` | General Tree Traversals | Recursive matches Iterative (Stack/Queue) | **PASS** |
| `03` | BST CRUD & 3 Delete Cases | Leaf, 1 child, and 2 children via successor | **PASS** |
| `04` | BST Search, Min, Max, Pred, Succ, Range | Range $[a, b]$ returns exact sorted subset | **PASS** |
| `05` | BST 4 Traversals | In, Pre, Post, Level (Rec == Iter) | **PASS** |
| `06` | BST vs AVL on 1,000 Sorted IDs | BST height $= 1000$; AVL height $\le 14$ | **PASS** |
| `07` | AVL Rotations (LL, RR, LR, RL) | Trigger each rotation; verify BST & BF | **PASS** |
| `08` | AVL 10,000 Random Ops Stress Test | 10k inserts + 5k deletes with `verify()` | **PASS** |
| `09` | Expression Tree Evaluation & Minimal Parens | Proper syntax tree build & evaluation | **PASS** |
| `10` | Expression Tree Error Handling | Catches division by zero & operand shortage | **PASS** |
| `11` | Graph Dual Representation & Memory | Matrix $\leftrightarrow$ List consistency & memory | **PASS** |
| `12` | BFS Fewest Stops vs Unweighted Dijkstra | Exact hop count and path agreement | **PASS** |
| `13` | DFS Edge Classification & Tarjan's SCC | Tree, Back, Forward, Cross, and SCC counts | **PASS** |
| `14` | MST Prim vs Kruskal Agreement & Forest | Identical total weights on Spanning Forest | **PASS** |
| `15` | Production Scheduling Topological Sort | Kahn and DFS yield valid precedence | **PASS** |
| `16` | Cycle Detection in Production Workflow | Detects circular dependency and prints cycle | **PASS** |
| `17` | Critical Path Method Calculations | EST, EFT, LST, LFT, Slack, and Critical Path | **PASS** |
| `18` | Dijkstra Negative Edge Failure Demo | Explains and demonstrates failure case | **PASS** |

**Final Verification Result:** 18 / 18 Tests Passed (100% Pass Rate).

---

## 8. Sample System Execution Transcripts

### 8.1 Production Scheduling & Critical Path Method Output
```text
=========================================================================================================
Task ID    | Task Name                    | Dur(d)  | EST    | EFT    | LST    | LFT    | Slack  | Critical?
---------------------------------------------------------------------------------------------------------
T1         | Raw Material Sourcing        | 4.0     | 0.0    | 4.0    | 0.0    | 4.0    | 0.0    | ★ YES
T2         | Quality & Chemical Testing   | 2.0     | 4.0    | 6.0    | 4.0    | 6.0    | 0.0    | ★ YES
T3         | Sub-Assembly Fabrication     | 6.0     | 6.0    | 12.0   | 6.0    | 12.0   | 0.0    | ★ YES
T4         | PCB SMT Pick & Place         | 3.0     | 6.0    | 9.0    | 9.0    | 12.0   | 3.0    |   No
T5         | System Enclosure Integration | 5.0     | 12.0   | 17.0   | 12.0   | 17.0   | 0.0    | ★ YES
T6         | Firmware Flash & Calibration | 2.0     | 17.0   | 19.0   | 17.0   | 19.0   | 0.0    | ★ YES
T7         | Environmental Stress Test    | 4.0     | 19.0   | 23.0   | 19.0   | 23.0   | 0.0    | ★ YES
T8         | Final Packaging & Dispatch   | 1.0     | 23.0   | 24.0   | 23.0   | 24.0   | 0.0    | ★ YES
=========================================================================================================
TOTAL PROJECT CRITICAL DURATION: 24.0 days
CRITICAL PATH: T1 -> T2 -> T3 -> T5 -> T6 -> T7 -> T8
=========================================================================================================
```

### 8.2 Array-Based Dijkstra Step-by-Step Distance Table
```text
================================================================================
Step   | Settled Node   | Current Dist   | Relaxed Neighbors / Updates             
--------------------------------------------------------------------------------
1      | MUM            | 0.0            | AHM: 525.0, NAG: 815.0, PUN: 150.0      
2      | PUN            | 150.0          | HYD: 710.0                              
3      | AHM            | 525.0          | JAI: 1175.0                             
4      | HYD            | 710.0          | BLR: 1280.0, CHE: 1340.0                
5      | NAG            | 815.0          | DEL: 1895.0, KOL: 1935.0                
6      | JAI            | 1175.0         | DEL: 1455.0                             
7      | BLR            | 1280.0         | KOC: 1820.0                             
8      | CHE            | 1340.0         | (None)                                  
9      | DEL            | 1455.0         | LKO: 1955.0                             
10     | KOC            | 1820.0         | (None)                                  
11     | KOL            | 1935.0         | (None)                                  
12     | LKO            | 1955.0         | (None)                                  
================================================================================
OPTIMAL ROUTE: MUM -> PUN -> HYD -> CHE (Transportation Distance: 1,340.00 km)
```

---

## 9. Team Contribution Table

As required by Section 6 and Section 7 of the evaluation rubric, individual contributions across modules are documented below:

| Register No. | Student Name | Core Module Responsibilities | Specific Code / Section Contributions | Contribution (%) |
| :---: | :---: | :--- | :--- | :---: |
| **25AD064** | Member 1 | **Module A: Hierarchical Trees & Indices** | Implemented `GeneralTree`, `BinarySearchTree` (CRUD, 3-case delete, Range Query), and `AVLTree` balancing with LL/RR/LR/RL rotations and `verify()` function. | 25% |
| **25AD086** | Member 2 | **Module B: Graph ADT & Routing Engines** | Built `Graph` ADT (switchable Adjacency Matrix & List), memory calculation, `Dijkstra` array-based routing, step table generator, and negative edge failure analysis. | 25% |
| **25AD111** | Member 3 | **Module B: MST & Production Scheduling** | Implemented `DisjointSet` (Rank + Path Compression), `Prim`, `Kruskal` (custom MergeSort), `ProductionScheduler` (Kahn, DFS, CPM, Slack), and `ExpressionTree`. | 25% |
| **25AD205** | Member 4 | **Module C: Analysis, Benchmarks & Testing** | Designed `benchmarks.py` ($n=1k, 5k, 20k$ and $V=200, 1k, 2k$), growth ratio derivations, 18 automated self-tests, and theoretical proofs compilation. | 25% |
| **Total** | | **Full System Integration & Verification** | **All 4 members participated in integration, code review, and CLI validation.** | **100%** |

---

## 10. Conclusion & Verification Certification

The **Supply Chain Manager (Project 19)** codebase fulfills all specifications set forth in Assignment II:
1. All tree and graph data structures have been designed and coded from first principles without relying on third-party libraries.
2. Complete functional parity between recursive and iterative traversals using explicit Stack and Queue structures has been demonstrated.
3. High-load stress tests (10,000 AVL operations and $V=2,000$ graph algorithms) verified numerical and structural invariants.
4. Empirical growth ratios match asymptotic theoretical bounds.

**Course Faculty / Head of the Department Signature:** ___________________________

