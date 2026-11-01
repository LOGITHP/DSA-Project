"""
theory/theoretical_proofs.py
Complete Unit V Theoretical Analysis, Proofs, Recurrences, and Derivations.
Includes:
1. Design Techniques & Problem Classification for all algorithms
2. Correctness Argument for Dijkstra & Failure with Negative Edges
3. Correctness Proof for Kruskal & Prim via Cut/Cycle Properties
4. Non-Recursive Analysis: Step-by-Step Operation Counting (BFS, Dijkstra, Prim, Kruskal)
5. Recursive Analysis: Solving Recurrences (Tree Traversals, BST Best/Worst/Avg, AVL Insertion)
6. Proof that AVL Tree has Height O(log N) via Minimum Node Recurrence N(h) = N(h-1) + N(h-2) + 1
7. Asymptotic Notations (O, Omega, Theta), Formal Property Proof with Supply Chain Example
8. Amortized Analysis of Union-Find (Path Compression + Rank)
9. Comparison-based Sorting Lower Bound Omega(E log E) for Kruskal
"""


def get_design_techniques() -> str:
    return """
====================================================================================================
1. ALGORITHM DESIGN TECHNIQUES & PROBLEM CLASSIFICATION (Unit V, 0.75 Marks)
====================================================================================================

Algorithm             | Problem Type                     | Design Technique    | Optimal Substructure?
----------------------|----------------------------------|---------------------|----------------------
BFS (Fewest Stops)    | Single-Source Unweighted Path    | Graph Traversal     | Yes (Level Queue)
DFS Classification    | Graph Structure / Cycle Detect   | Graph Traversal     | Yes (Backtracking)
Tarjan's SCC          | Strongly Connected Components    | Depth-First Search  | Yes (Low-link values)
Dijkstra (Array)      | Single-Source Shortest Path      | Greedy Method       | Yes (Dijkstra property)
Prim's Algorithm      | Minimum Spanning Tree (MST)      | Greedy Method       | Yes (Cut Property)
Kruskal's Algorithm   | Minimum Spanning Tree (MST)      | Greedy Method       | Yes (Cycle Property)
Kahn's Algorithm      | Topological Ordering / DAG       | Decrease & Conquer  | Yes (Indegree reduction)
Critical Path (CPM)   | Project Scheduling / Longest Path| Dynamic Programming | Yes (Forward/Backward pass)
AVL Balancing         | Dictionary / Index Lookups       | Divide & Conquer    | Yes (Height Invariance)
Expression Tree       | Formula Parsing & Evaluation     | Syntax Tree (Tree)  | Yes (Subtree evaluation)
"""


def get_dijkstra_correctness() -> str:
    return """
====================================================================================================
2. CORRECTNESS ARGUMENT FOR DIJKSTRA & WHY IT FAILS ON NEGATIVE EDGES
====================================================================================================

THEOREM:
For a directed or undirected graph G = (V, E) with non-negative edge weights w(u, v) >= 0,
Dijkstra's algorithm terminates with dist[u] = delta(s, u) for all u in V.

PROOF SKETCH (By Induction on |S|, the settled set):
Base Case:
  At step 0, S = {s}, dist[s] = 0 = delta(s, s). All other dist[v] = infinity. Holds.
Inductive Step:
  Suppose for all u in S, dist[u] = delta(s, u).
  Let v* in (V - S) be the vertex chosen in the greedy step, i.e., dist[v*] = min_{v in V-S} dist[v].
  Suppose for contradiction that dist[v*] > delta(s, v*).
  Then there must exist a shorter path P from s to v*.
  Since s in S and v* in (V - S), path P must leave set S at some edge (x, y) where x in S, y in (V - S).
  Length of path P:
    delta(s, v*) = delta(s, x) + w(x, y) + length(y to v*)
  Since all edge weights w >= 0:
    delta(s, v*) >= delta(s, x) + w(x, y) = dist[x] + w(x, y) >= dist[y]
  Because v* was chosen with minimal distance among all vertices in (V - S):
    dist[v*] <= dist[y] <= delta(s, v*)
  This contradicts dist[v*] > delta(s, v*). Hence dist[v*] = delta(s, v*).

WHY DIJKSTRA FAILS WITH NEGATIVE EDGES:
  The key step in the proof assumes:
    delta(s, v*) >= delta(s, y)  due to  length(y to v*) >= 0.
  If an edge along (y to v*) has a NEGATIVE weight, this inequality collapses!
  Once v* is marked as 'visited' / settled, Dijkstra never reconsidered or relaxed it again.
  Therefore, an initially chosen 'longer' path through y might subsequently decrease and become
  shorter than dist[v*], but Dijkstra's greedy permanence blindfold permanently misses it.
"""


def get_cut_and_cycle_property() -> str:
    return """
====================================================================================================
3. CUT PROPERTY & CYCLE PROPERTY PROOFS FOR MST (PRIM & KRUSKAL)
====================================================================================================

1. THE CUT PROPERTY (Used by Prim's Algorithm):
   Let G = (V, E) be a connected undirected weighted graph. Let S be any proper subset of V.
   A cut (S, V - S) partitions the vertices.
   If edge e = (u, v) is a light edge crossing the cut (i.e., has minimum weight among all edges
   crossing the cut), then e belongs to SOME minimum spanning tree of G.

   Proof:
   Let T be an MST that does not contain e. Adding e to T creates a unique cycle C.
   Since e connects S to V - S, the cycle C must cross the cut at least once more via another edge e'.
   Now consider T' = (T - {e'}) U {e}.
   Because e is a light edge crossing the cut, w(e) <= w(e').
   Therefore:
     w(T') = w(T) - w(e') + w(e) <= w(T).
   Since T was already an MST, w(T') cannot be strictly less than w(T). Thus w(T') = w(T).
   Hence T' is also an MST containing e.
   Since Prim's algorithm always adds a light edge crossing the cut (S, V - S) where S is the set of
   visited vertices, every edge selected by Prim is guaranteed to belong to the MST.

2. THE CYCLE PROPERTY (Used by Kruskal's Algorithm):
   Let C be any cycle in G = (V, E), and let e be the strictly heaviest edge in C.
   Then e CANNOT belong to any minimum spanning tree of G.

   Proof:
   Suppose e is in an MST T. Removing e from T disconnects T into two components S and V - S.
   The remaining edges in cycle C - {e} must cross the cut (S, V - S) at least once via edge e'.
   Since e is the strictly heaviest edge on cycle C, w(e') < w(e).
   Adding e' creates a new spanning tree T' = (T - {e}) U {e'} with:
     w(T') = w(T) - w(e) + w(e') < w(T).
   This contradicts the assumption that T was an MST!
   Hence e cannot belong to any MST.
   Since Kruskal's algorithm rejects any edge that forms a cycle with previously chosen edges,
   it effectively avoids including the heaviest edge in any cycle, preserving MST optimality.
"""


def get_non_recursive_analysis() -> str:
    return """
====================================================================================================
4. NON-RECURSIVE COMPLEXITY ANALYSIS VIA OPERATION COUNTING (Unit V, 0.75 Marks)
====================================================================================================

1. BFS (Breadth-First Search):
   - Initialization: visited array and queue setup -> Theta(V) operations.
   - Enqueue / Dequeue: Each vertex is enqueued exactly once and dequeued once -> 2 * V operations.
   - Neighbor iteration:
     * Using Adjacency List: The for-loop over neighbors runs sum_{u in V} deg(u) = 2E times (undirected) or E times (directed).
     * Inside loop: lookup visited (O(1)), push to queue (O(1)).
   - Total Basic Operations = c1 * V + c2 * E.
   - Complexity: Theta(V + E) on Adjacency List; Theta(V^2) on Adjacency Matrix.

2. DIJKSTRA (Array-based Version):
   - Initialization: dist array (inf) and visited array (false) -> Theta(V).
   - Outer Loop: Exactly V iterations (settles one unvisited vertex per step).
   - Finding Minimum Vertex: Linear scan through all V vertices in unvisited array -> V operations per outer step.
     * Total minimum-finding cost: V * V = V^2 operations.
   - Edge Relaxation:
     * Over all V steps, every edge (u, v) is examined once (directed) or twice (undirected).
     * Relaxation step: dist[u] + w < dist[v] involves 1 addition and 1 comparison.
     * Total relaxation cost: Theta(E).
   - Total Cost: Theta(V^2 + E) = Theta(V^2) because E <= V^2.
   - Preference: Array-based Dijkstra is optimal for DENSE graphs where E approx V^2, avoiding priority queue overhead.

3. PRIM'S ALGORITHM (Array-based Version):
   - Outer loop executes V times.
   - Scanning unvisited key array takes V operations per iteration -> V * V = V^2 operations.
   - Updating neighbor keys: sum of degrees = Theta(E).
   - Total Cost: Theta(V^2).
   - Preference: Superior for DENSE graphs (E approx V^2/4).

4. KRUSKAL'S ALGORITHM (MergeSort + Union-Find):
   - Step 1: Sorting E edges.
     * MergeSort divides list in half log2(E) times; merging takes E comparisons per level.
     * Total comparisons: Theta(E log E).
   - Step 2: DSU Operations:
     * V make_set() calls -> Theta(V).
     * 2E find() calls and at most V - 1 union() calls.
     * With Path Compression + Union by Rank, each operation takes amortized O(alpha(V)).
     * Total DSU cost: Theta(E * alpha(V)).
   - Total Complexity: Theta(E log E + E * alpha(V)) = Theta(E log E).
   - Since E <= V^2, log E <= 2 log V, so Theta(E log E) = Theta(E log V).
   - Preference: Vastly superior for SPARSE graphs where E approx 2V:
     * Kruskal takes O(V log V) << O(V^2) for Prim array!
"""


def get_recursive_analysis() -> str:
    return """
====================================================================================================
5. RECURSIVE ANALYSIS & RECURRENCES (Unit V, 0.75 Marks)
====================================================================================================

1. TREE TRAVERSAL RECURRENCE:
   At each node, we perform O(1) visit work and recursively call traversal on left and right subtrees.
   Recurrence:
     T(n) = T(k) + T(n - k - 1) + c, where k is size of left subtree.
   For a balanced binary tree (k = n/2):
     T(n) = 2 * T(n/2) + c.
   Using Master Theorem:
     a = 2, b = 2, f(n) = c = O(n^0).
     n^{log_b a} = n^{log_2 2} = n^1.
     Since f(n) = O(n^{1 - epsilon}), Case 1 applies:
     T(n) = Theta(n).

2. BST INSERTION RECURRENCES:
   (a) Best Case (Balanced Partition):
       Recurrence: T(n) = T(n/2) + c.
       By Master Theorem (a=1, b=2, f(n)=c):
       T(n) = Theta(log n).

   (b) Worst Case (Sorted / Reverse-Sorted Degenerate Input):
       Recurrence: T(n) = T(n - 1) + c.
       Expanding:
         T(n) = T(n - 1) + c
              = T(n - 2) + 2c
              = ... = T(0) + n*c = Theta(n).
       Inserting n sorted elements takes sum_{i=1}^n i = Theta(n^2) total time.

   (c) Average Case (Random Uniform Keys):
       Recurrence:
         T(n) = 1/n * sum_{k=0}^{n-1} [ T(k) + T(n - 1 - k) ] + c
              = 2/n * sum_{k=0}^{n-1} T(k) + c.
       Multiplying by n:
         n * T(n) = 2 * sum_{k=0}^{n-1} T(k) + c*n.
       Subtracting (n - 1)*T(n - 1):
         n*T(n) - (n - 1)*T(n - 1) = 2*T(n - 1) + c.
         n*T(n) = (n + 1)*T(n - 1) + c.
       Dividing by n(n + 1):
         T(n)/(n + 1) = T(n - 1)/n + c/(n*(n + 1)).
       Telescoping sum yields harmonic series:
         T(n) = 2 * (n + 1) * H_n approx 2 * n * ln(n).
       Average depth of a node in a random BST is 2 * ln(n) approx 1.386 log_2(n).
       Therefore, average case insertion is Theta(log n).

3. AVL INSERTION RECURRENCE:
   At each level, we make one recursive descent:
     T(n) = T(n/2) + O(1) search + O(1) rotation on unwind.
   Since height is strictly capped at 1.44 log_2 n:
     T(n) = Theta(log n) in the absolute WORST case!
"""


def get_avl_height_proof() -> str:
    return """
====================================================================================================
6. FORMAL PROOF: AVL TREE WITH n NODES HAS HEIGHT O(log n) (Unit V, 0.75 Marks)
====================================================================================================

THEOREM:
The height h of an AVL tree containing n nodes satisfies:
  h < 1.4404 * log_2(n + 2) - 0.328 = O(log n).

PROOF:
Let N(h) be the MINIMUM number of nodes in an AVL tree of height h.
Base Cases:
  Height h = 0 (empty tree):        N(0) = 0
  Height h = 1 (single node root):   N(1) = 1
  Height h = 2:                      N(2) = 2

Inductive Step:
  To construct an AVL tree of height h with the minimum possible number of nodes:
  - The root must have one child of height h - 1 (to achieve height h).
  - To minimize nodes while strictly satisfying the AVL balance factor (|BF| <= 1),
    the other child must have height h - 2.
  - Both children must themselves be minimum-node AVL trees of their respective heights.
  Therefore:
    N(h) = N(h - 1) + N(h - 2) + 1.

Relation to Fibonacci Numbers:
  Recall Fibonacci sequence: F(0) = 0, F(1) = 1, F(2) = 1, F(3) = 2, F(4) = 3, F(5) = 5...
  Notice:
    N(0) + 1 = 1 = F(2)
    N(1) + 1 = 2 = F(3)
    N(2) + 1 = 3 = F(4)
    N(3) + 1 = 2 + 1 + 1 + 1 = 5 = F(5)
  By mathematical induction:
    N(h) + 1 = F(h + 2)   ==>   N(h) = F(h + 2) - 1.

Golden Ratio Closed Form (Binet's Formula):
  F(k) = (phi^k - psi^k) / sqrt(5), where phi = (1 + sqrt(5))/2 approx 1.618034.
  For large h, psi^k -> 0, so:
    F(h + 2) approx (phi^(h + 2)) / sqrt(5).
  Therefore:
    n >= N(h) = F(h + 2) - 1 > (phi^(h + 2) / sqrt(5)) - 1.
    n + 1 > phi^(h + 2) / sqrt(5).
    sqrt(5) * (n + 1) > phi^(h + 2).

Taking log_phi on both sides:
    h + 2 < log_phi(sqrt(5) * (n + 1)) = log_2(sqrt(5) * (n + 1)) / log_2(phi).
  Since 1 / log_2(phi) = 1 / log_2(1.618034) approx 1.44042:
    h < 1.4404 * log_2(n + 2) = O(log n).  [Q.E.D.]

COROLLARY FOR SUPPLY CHAIN INVENTORY / SUPPLIER DIRECTORY:
  Even with 1,000,000 suppliers in the AVL index:
    h_max <= 1.4404 * log_2(1,000,002) approx 1.4404 * 19.93 <= 28 comparisons!
  Search never degrades into a linear scan, in stark contrast to an unmanaged BST.
"""


def get_amortized_and_lower_bound() -> str:
    return """
====================================================================================================
7. ASYMPTOTIC NOTATIONS, AMORTIZED ANALYSIS & SORTING LOWER BOUND (Unit V, 0.5 Marks)
====================================================================================================

1. DEFINITIONS OF ASYMPTOTIC NOTATIONS:
   - Big-O (O): Asymptotic upper bound. f(n) in O(g(n)) iff exists c > 0, n_0 > 0 s.t. 0 <= f(n) <= c*g(n) for all n >= n_0.
   - Big-Omega (Omega): Asymptotic lower bound. f(n) in Omega(g(n)) iff exists c > 0, n_0 > 0 s.t. 0 <= c*g(n) <= f(n) for all n >= n_0.
   - Big-Theta (Theta): Asymptotically tight bound. f(n) in Theta(g(n)) iff f(n) in O(g(n)) and f(n) in Omega(g(n)).

2. FORMAL PROPERTY PROOF WITH SUPPLY CHAIN PROJECT EXAMPLE:
   Property: If f(n) in O(g(n)) and g(n) in O(h(n)), then f(n) in O(h(n)) (Transitivity).
   Proof:
     Exists c1, n1 s.t. f(n) <= c1 * g(n) for n >= n1.
     Exists c2, n2 s.t. g(n) <= c2 * h(n) for n >= n2.
     For n >= max(n1, n2): f(n) <= c1 * (c2 * h(n)) = (c1 * c2) * h(n).
     Choosing c3 = c1 * c2 and n0 = max(n1, n2), f(n) in O(h(n)).
   Project Application:
     In our Supply Chain Dijkstra path calculation, step scan cost f(V) = 2V + 5 in O(V),
     and total path relaxations across all vertices g(V) = V * O(V) = O(V^2).
     Thus the complete routing engine runtime is bounded transitively by O(V^2).

3. AMORTIZED ANALYSIS OF UNION-FIND (Path Compression + Union by Rank):
   Let m be the total number of operations (make_set, union, find) on n elements.
   - Union by Rank ensures that any tree with rank r contains at least 2^r nodes.
     Thus, the maximum possible rank of any root is bounded by floor(log_2 n).
   - Path Compression flattens trees during find() calls, pointing traversed nodes directly to root.
   - Accounting / Potential Function Method:
     Define the potential Phi = sum_{v in V} rank_diff_potential(v).
     Each find operation costs length of the path.
     Nodes whose parent pointer changes have their cost paid by the reduction in potential Phi!
     Tarjan proved that m operations take total time:
       T(m, n) = O(m * alpha(n)),
     where alpha(n) is the extremely slow-growing INVERSE ACKERMANN FUNCTION.
     For all realistic universes (n < 2^65536, greater than the atoms in the universe), alpha(n) <= 4.
     Hence, the amortized cost per Union-Find operation is effectively O(1).

4. COMPARISON-BASED SORTING LOWER BOUND FOR KRUSKAL:
   - Any deterministic comparison-based sorting algorithm can be modeled as a binary Decision Tree.
   - For an array of E edges, there are E! possible permutations.
   - The decision tree must contain at least E! leaves to correctly identify any permutation.
   - A binary tree of height h has at most 2^h leaves:
       2^h >= E!  ==>  h >= log_2(E!).
   - Using Stirling's Approximation: ln(E!) approx E ln(E) - E:
       h >= log_2(E!) = Omega(E log E).
   - Therefore, the sorting step in Kruskal's algorithm CANNOT run faster than Omega(E log E)
     using comparison-based sorting.
"""

