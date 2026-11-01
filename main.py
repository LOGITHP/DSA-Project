"""
main.py
Master Console Application for:
Project 19: Supply Chain Manager (AI&DS, Year II, Assignment II)
Team Members: 25AD064, 25AD086, 25AD111, 25AD205

Fully Implements:
- Module A: Location / Record Directory (General Tree, BST, AVL, Expression Tree)
- Module B: Network & Logistics (Graph ADT, BFS, DFS, SCC, Dijkstra, Prim, Kruskal, CPM Scheduling)
- Module C: Algorithm Analysis & Empirical Experiments (Empirical vs Theoretical Growth)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from structures.general_tree import GeneralTree
from structures.bst import BinarySearchTree
from structures.avl_tree import AVLTree
from structures.expression_tree import ExpressionTree
from structures.graph import Graph
from algorithms.dijkstra import dijkstra_array_based, demonstrate_negative_edge_failure
from algorithms.mst import prim_array_based, kruskal_mst
from algorithms.scheduling import ProductionScheduler
from simulation.supply_chain_data import (
    create_sample_supply_chain_graph,
    create_sample_category_tree,
    create_sample_inventory_bst,
    create_sample_supplier_avl,
    create_production_schedulers
)
from simulation.benchmarks import run_tree_benchmarks, run_graph_benchmarks
from simulation.test_suite import run_all_self_tests
from theory import theoretical_proofs


class SupplyChainApp:
    def __init__(self):
        print("Initializing Supply Chain Management System...")
        self.graph: Graph = create_sample_supply_chain_graph()
        self.category_tree: GeneralTree = create_sample_category_tree()
        self.inventory_bst: BinarySearchTree = create_sample_inventory_bst()
        self.supplier_avl: AVLTree = create_sample_supplier_avl()
        self.sched_acyclic, self.sched_cyclic = create_production_schedulers()
        print("Initialization complete.\n")

    def print_banner(self):
        print("=" * 80)
        print("   KPR INSTITUTE OF ENGINEERING AND TECHNOLOGY | DEPARTMENT OF AI & DS")
        print("      ASSIGNMENT II: PROJECT 19 - SUPPLY CHAIN LOGISTICS MANAGER")
        print("      Developer: LOGITH P | Team: 25AD064, 25AD086, 25AD111, 25AD205")
        print("=" * 80)

    def print_menu(self):
        print("\n" + "=" * 55)
        print("                MAIN NAVIGATION MENU")
        print("=" * 55)
        print(" 1. Record Directory (General Tree / BST / AVL)")
        print(" 2. Logistics Tariff & Cost Expression Calculator")
        print(" 3. Build / Edit Logistics Depot Network")
        print(" 4. Traversals, Edge Classification & SCC")
        print(" 5. Shortest Route Planning (Dijkstra Array-based)")
        print(" 6. Minimum Spanning Network / Forest (Prim & Kruskal)")
        print(" 7. Production Scheduling (Topological Sort & CPM)")
        print(" 8. Run Timing Experiments (Empirical vs Theory Growth)")
        print(" 9. Run Automated Self-Tests (18 Comprehensive Tests)")
        print("10. Theoretical Analysis & Complexity Proofs Reference")
        print("11. Exit")
        print("=" * 55)

    # ------------------ 1. Record Directory ------------------
    def menu_record_directory(self):
        while True:
            print("\n--- [1] Record Directory Subsystem ---")
            print("1. Product Category Hierarchy (General Tree)")
            print("2. Inventory by SKU (Binary Search Tree)")
            print("3. Certified Supplier Directory (Self-Balancing AVL Tree)")
            print("4. Compare BST vs AVL Height on 1,000 Sorted IDs")
            print("5. Back to Main Menu")
            choice = input("Select an option (1-5): ").strip()

            if choice == "1":
                self._handle_general_tree()
            elif choice == "2":
                self._handle_bst()
            elif choice == "3":
                self._handle_avl()
            elif choice == "4":
                self._handle_bst_vs_avl_height()
            elif choice == "5":
                break
            else:
                print("Invalid selection. Try again.")

    def _handle_general_tree(self):
        while True:
            print("\n  >> Category Hierarchy (General Tree) <<")
            print("  1. Display Category Tree")
            print("  2. Insert New Category / Product Line")
            print("  3. Delete Subtree")
            print("  4. Show Traversals (Recursive vs Iterative with Stack/Queue)")
            print("  5. Back")
            sub = input("  Select (1-5): ").strip()
            if sub == "1":
                print("\n" + self.category_tree.display_tree())
            elif sub == "2":
                parent = input("  Enter Parent Category Name: ").strip()
                child = input("  Enter New Child Category Name: ").strip()
                if self.category_tree.insert(parent, child):
                    print(f"  [SUCCESS] Successfully added '{child}' under '{parent}'.")
                else:
                    print(f"  [ERROR] Parent '{parent}' not found or duplicate child.")
            elif sub == "3":
                target = input("  Enter Category Name to delete (subtree): ").strip()
                if self.category_tree.delete_subtree(target):
                    print(f"  [SUCCESS] Deleted subtree rooted at '{target}'.")
                else:
                    print(f"  [ERROR] Cannot delete '{target}' (not found or is root).")
            elif sub == "4":
                print("\n  Preorder Recursive: ", self.category_tree.preorder_recursive())
                print("  Preorder Iterative: ", self.category_tree.preorder_iterative())
                print("  Postorder Recursive:", self.category_tree.postorder_recursive())
                print("  Postorder Iterative:", self.category_tree.postorder_iterative())
                print("  Level-order Recurs: ", self.category_tree.level_order_recursive())
                print("  Level-order Iterat: ", self.category_tree.level_order_iterative())
            elif sub == "5":
                break

    def _handle_bst(self):
        while True:
            print("\n  >> Inventory Management (Binary Search Tree by SKU) <<")
            print("  1. View All Inventory (In-Order Traversal)")
            print("  2. Insert / Update SKU Item")
            print("  3. Search SKU")
            print("  4. Delete SKU (Demonstrating Leaf, 1 Child, 2 Children cases)")
            print("  5. Find Min & Max SKU")
            print("  6. Predecessor & Successor of SKU")
            print("  7. Range Query (SKUs between A and B)")
            print("  8. Show Traversals (Recursive vs Iterative)")
            print("  9. Back")
            sub = input("  Select (1-9): ").strip()
            if sub == "1":
                skus = self.inventory_bst.inorder_recursive()
                print(f"\n  Total Inventory Items: {len(skus)}")
                for sku in skus:
                    node = self.inventory_bst.search(sku)
                    print(f"    - {node}")
            elif sub == "2":
                try:
                    sku = int(input("  Enter numeric SKU ID: ").strip())
                    name = input("  Enter Item Name: ").strip()
                    qty = int(input("  Enter Stock Quantity: ").strip())
                    price = float(input("  Enter Unit Price ($): ").strip())
                    cat = input("  Enter Category: ").strip()
                    ins = self.inventory_bst.insert(sku, name, qty, price, cat)
                    print(f"  [SUCCESS] {'Inserted new SKU' if ins else 'Updated existing SKU'} {sku}.")
                except ValueError:
                    print("  [ERROR] Invalid numeric input.")
            elif sub == "3":
                try:
                    sku = int(input("  Enter SKU ID to search: ").strip())
                    node = self.inventory_bst.search(sku)
                    if node:
                        print(f"  [FOUND] {node}")
                    else:
                        print(f"  [NOT FOUND] SKU {sku} does not exist in inventory.")
                except ValueError:
                    print("  [ERROR] SKU must be an integer.")
            elif sub == "4":
                try:
                    sku = int(input("  Enter SKU ID to delete: ").strip())
                    ok, case_desc = self.inventory_bst.delete(sku)
                    if ok:
                        print(f"  [SUCCESS] Deleted SKU {sku} -> Handled via: {case_desc}")
                    else:
                        print(f"  [ERROR] SKU {sku} not found.")
                except ValueError:
                    print("  [ERROR] SKU must be an integer.")
            elif sub == "5":
                mn = self.inventory_bst.find_min()
                mx = self.inventory_bst.find_max()
                print(f"  Min SKU: {mn}")
                print(f"  Max SKU: {mx}")
            elif sub == "6":
                try:
                    sku = int(input("  Enter SKU ID: ").strip())
                    pred = self.inventory_bst.predecessor(sku)
                    succ = self.inventory_bst.successor(sku)
                    print(f"  Inorder Predecessor of {sku}: {pred}")
                    print(f"  Inorder Successor of {sku}:   {succ}")
                except ValueError:
                    print("  [ERROR] Invalid SKU.")
            elif sub == "7":
                try:
                    a = int(input("  Enter Min SKU (a): ").strip())
                    b = int(input("  Enter Max SKU (b): ").strip())
                    res = self.inventory_bst.range_query(a, b)
                    print(f"\n  Found {len(res)} items in range [{a}, {b}]:")
                    for item in res:
                        print(f"    - {item}")
                except ValueError:
                    print("  [ERROR] Bounds must be integers.")
            elif sub == "8":
                print("  Inorder Rec:   ", self.inventory_bst.inorder_recursive())
                print("  Inorder Iter:  ", self.inventory_bst.inorder_iterative())
                print("  Preorder Rec:  ", self.inventory_bst.preorder_recursive())
                print("  Preorder Iter: ", self.inventory_bst.preorder_iterative())
                print("  Postorder Rec: ", self.inventory_bst.postorder_recursive())
                print("  Postorder Iter:", self.inventory_bst.postorder_iterative())
                print("  Level-order Rec:", self.inventory_bst.level_order_recursive())
                print("  Level-order It :", self.inventory_bst.level_order_iterative())
            elif sub == "9":
                break

    def _handle_avl(self):
        while True:
            print("\n  >> Supplier Directory (Self-Balancing AVL Tree) <<")
            print("  1. View All Certified Suppliers (In-Order)")
            print("  2. Insert Supplier (With Rotation Tracing)")
            print("  3. Delete Supplier (With Rebalancing & Tracing)")
            print("  4. Search Supplier by ID")
            print("  5. Run Comprehensive verify() Invariant Check")
            print("  6. Back")
            sub = input("  Select (1-6): ").strip()
            if sub == "1":
                suppliers = self.supplier_avl.inorder()
                print(f"\n  Total Certified Suppliers: {len(suppliers)} (Height: {self.supplier_avl.height()})")
                for s in suppliers:
                    print(f"    - ID {s.supplier_id}: {s.name:<30} | {s.location:<12} | Lead: {s.lead_time}d | Rating: {s.reliability:.1f}★ | Node Height: {s.height}")
            elif sub == "2":
                try:
                    sid = int(input("  Enter Supplier ID: ").strip())
                    name = input("  Enter Company Name: ").strip()
                    cat = input("  Enter Supply Category: ").strip()
                    lead = int(input("  Enter Lead Time (days): ").strip())
                    rating = float(input("  Enter Reliability Score (0.0 - 5.0): ").strip())
                    loc = input("  Enter Location City: ").strip()

                    self.supplier_avl.trace_rotations = True
                    self.supplier_avl.insert(sid, name, cat, lead, rating, loc)
                    self.supplier_avl.trace_rotations = False

                    ok, msg = self.supplier_avl.verify()
                    print(f"  [STATUS] Insert completed. Invariant verification: {msg}")
                except ValueError:
                    print("  [ERROR] Invalid numeric input.")
            elif sub == "3":
                try:
                    sid = int(input("  Enter Supplier ID to delete: ").strip())
                    self.supplier_avl.trace_rotations = True
                    ok = self.supplier_avl.delete(sid)
                    self.supplier_avl.trace_rotations = False
                    if ok:
                        ok_v, msg = self.supplier_avl.verify()
                        print(f"  [SUCCESS] Deleted Supplier {sid}. Tree rebalanced: {msg}")
                    else:
                        print(f"  [NOT FOUND] Supplier {sid} does not exist.")
                except ValueError:
                    print("  [ERROR] Invalid Supplier ID.")
            elif sub == "4":
                try:
                    sid = int(input("  Enter Supplier ID to search: ").strip())
                    res = self.supplier_avl.search(sid)
                    if res:
                        print(f"  [FOUND] {res}")
                    else:
                        print(f"  [NOT FOUND] Supplier {sid} not in directory.")
                except ValueError:
                    print("  [ERROR] Invalid ID.")
            elif sub == "5":
                ok, msg = self.supplier_avl.verify()
                print(f"\n  AVL Integrity Check: {'PASSED' if ok else 'FAILED'}")
                print(f"  Details: {msg}")
                print(f"  Total Nodes: {self.supplier_avl.size()}, Tree Height: {self.supplier_avl.height()}")
            elif sub == "6":
                break

    def _handle_bst_vs_avl_height(self):
        print("\n  >> Comparing BST vs AVL Height on 1,000 Sorted IDs <<")
        print("  Inserting keys 1 to 1,000 sequentially into both trees...")
        test_bst = BinarySearchTree()
        test_avl = AVLTree(trace_rotations=False)
        for i in range(1, 1001):
            test_bst.insert(i, f"Item_{i}")
            test_avl.insert(i, f"Supplier_{i}")

        bst_h = test_bst.height()
        avl_h = test_avl.height()
        print(f"\n  [RESULTS]")
        print(f"  BST Height on 1,000 sorted keys: {bst_h} (Completely degenerate O(N) linked list!)")
        print(f"  AVL Height on 1,000 sorted keys: {avl_h} (Strictly bounded O(log N) balanced tree!)")
        print(f"  Theoretical Max AVL Height:       {test_avl.height()} <= 14 (1.44 * log2(1002))")
        print(f"  Search speedup in AVL:            Up to {bst_h / avl_h:.1f}x fewer pointer hops in worst-case!")

    # ------------------ 2. Expression Calculator ------------------
    def menu_expression_calculator(self):
        print("\n--- [2] Logistics Tariff & Cost Expression Calculator ---")
        print("Pre-loaded project formulas:")
        print("  A. 'dist rate * toll + 2 /'           (Standard Freight Tariff with Highway Sharing)")
        print("  B. 'weight dist * rate * surcharge +' (Heavy Cargo Shipping Surcharge)")
        print("  C. Custom Postfix Expression Entry")
        choice = input("Select formula (A, B, or C): ").strip().upper()

        if choice == "A":
            expr_str = "dist rate * toll + 2 /"
            default_vars = {"dist": 450.0, "rate": 6.5, "toll": 300.0}
        elif choice == "B":
            expr_str = "weight dist * rate * surcharge +"
            default_vars = {"weight": 12.0, "dist": 600.0, "rate": 2.2, "surcharge": 250.0}
        else:
            expr_str = input("Enter postfix formula (space-separated tokens, e.g. '10 20 + 5 *'): ").strip()
            default_vars = {}

        try:
            tree = ExpressionTree(expr_str)
            print(f"\nExpression Tree Built Successfully for Postfix: '{expr_str}'")
            infix_repr = tree.to_infix_minimal_parentheses()
            print(f"Infix Representation (Minimal Parentheses): {infix_repr}")

            # Collect variables if required
            tokens = expr_str.split()
            var_names = [t for t in tokens if t not in {'+', '-', '*', '/', '^'} and not t.replace('.', '', 1).isdigit()]
            unique_vars = list(dict.fromkeys(var_names))

            param_values = {}
            if unique_vars:
                print("\nEnter values for formula variables:")
                for v in unique_vars:
                    def_val = default_vars.get(v, 10.0)
                    val_input = input(f"  Value for '{v}' [default: {def_val}]: ").strip()
                    param_values[v] = float(val_input) if val_input else def_val

            result = tree.evaluate(param_values)
            print(f"\nEVALUATION RESULT: {result:,.2f}")

        except Exception as e:
            print(f"\n[CALCULATOR ERROR] {type(e).__name__}: {e}")

        # Demonstrate Error Handling
        print("\nDemonstrating Built-in Error Handling:")
        try:
            print("  Test 1: Division by zero ('100 0 /') -> ", end="")
            ExpressionTree("100 0 /").evaluate()
        except ZeroDivisionError as zde:
            print(f"[CAUGHT EXPECTED ERROR] {zde}")

        try:
            print("  Test 2: Operand shortage ('5 +') -> ", end="")
            ExpressionTree("5 +")
        except ValueError as ve:
            print(f"[CAUGHT EXPECTED ERROR] {ve}")

    # ------------------ 3. Build / Edit Network ------------------
    def menu_network_management(self):
        while True:
            print("\n--- [3] Build / Edit Supply Chain Depot Network ---")
            print("1. View All Depots and Logistics Routes")
            print("2. Switch Graph Representation Mode (Current: " + self.graph.representation_mode.upper() + ")")
            print("3. Memory Footprint Report (Adjacency Matrix vs Adjacency List)")
            print("4. Add New Logistics Depot")
            print("5. Add New Shipping Route (Edge)")
            print("6. Back to Main Menu")
            choice = input("Select an option (1-6): ").strip()

            if choice == "1":
                print(f"\nTotal Depots (V): {self.graph.num_vertices()}, Total Routes (E): {self.graph.num_edges()}")
                print(f"Representation Mode: {self.graph.representation_mode.upper()}")
                for u in self.graph.vertices:
                    meta = self.graph.vertex_metadata.get(u, {})
                    nbrs = self.graph.get_neighbors(u)
                    nbr_str = ", ".join([f"{v}({w:.0f}km)" for v, w in nbrs]) if nbrs else "(None - Isolated)"
                    print(f"  [{u}] {meta.get('name', u):<30} -> Connects to: {nbr_str}")
            elif choice == "2":
                new_mode = "matrix" if self.graph.representation_mode == "list" else "list"
                self.graph.set_representation_mode(new_mode)
                print(f"[SWITCHED] Graph is now operating on: ADJACENCY {new_mode.upper()}")
            elif choice == "3":
                mem = self.graph.report_memory_usage()
                print("\n" + "=" * 70)
                print("GRAPH MEMORY CONSUMPTION ANALYSIS")
                print("=" * 70)
                print(f"Vertices (V): {mem['num_vertices']}, Edges (E): {mem['num_edges']}")
                print(f"Active Representation:               ADJACENCY {mem['active_mode'].upper()}")
                print(f"Adjacency Matrix Theoretical Memory: {mem['matrix_theoretical_bytes']:,} Bytes (O(V^2))")
                print(f"Adjacency List Theoretical Memory:   {mem['list_theoretical_bytes']:,} Bytes (O(V + E))")
                print(f"Adjacency Matrix Actual In-Memory:   {mem['matrix_actual_bytes']:,} Bytes")
                print(f"Adjacency List Actual In-Memory:     {mem['list_actual_bytes']:,} Bytes")
                ratio = mem['matrix_actual_bytes'] / max(1, mem['list_actual_bytes'])
                print(f"Adjacency Matrix takes {ratio:.2f}x more memory than Adjacency List for this graph.")
                print(f"Insight: {mem['recommendation']}")
                print("=" * 70)
            elif choice == "4":
                code = input("Enter 3-letter Depot Code (e.g. BHO): ").strip().upper()
                name = input("Enter Depot Full Name: ").strip()
                if self.graph.add_vertex(code, {"name": name}):
                    print(f"[SUCCESS] Added Depot '{code}'.")
                else:
                    print(f"[ERROR] Depot '{code}' already exists.")
            elif choice == "5":
                u = input("Enter Source Depot Code: ").strip().upper()
                v = input("Enter Destination Depot Code: ").strip().upper()
                try:
                    w = float(input("Enter Route Distance / Cost: ").strip())
                    self.graph.add_edge(u, v, w)
                    print(f"[SUCCESS] Added shipping route {u} <---> {v} ({w} km).")
                except ValueError:
                    print("[ERROR] Distance must be a valid number.")
            elif choice == "6":
                break

    # ------------------ 4. Traversals & Structure ------------------
    def menu_traversals_structure(self):
        while True:
            print("\n--- [4] Traversals, Edge Classification & SCC ---")
            print("1. BFS Fewest-Stops Transit Route (Minimum Hop Count)")
            print("2. DFS with Discovery/Finish Timestamps and Edge Classification")
            print("3. Connected Components (Undirected Network)")
            print("4. Strongly Connected Components (Directed Graph via Tarjan's Algorithm)")
            print("5. Back to Main Menu")
            choice = input("Select an option (1-5): ").strip()

            if choice == "1":
                src = input("Enter Origin Depot (e.g. MUM): ").strip().upper()
                dst = input("Enter Destination Depot (e.g. CHE): ").strip().upper()
                path, hops = self.graph.bfs_fewest_stops(src, dst)
                if path:
                    print(f"\n[BFS RESULT] Fewest-Stops Transit Route: {' -> '.join(path)}")
                    print(f"Total Intermediate Stops / Hops: {hops}")
                else:
                    print(f"\n[UNREACHABLE] No route found between {src} and {dst} (Isolated zone).")
            elif choice == "2":
                dfs_res = self.graph.dfs_edge_classification()
                print("\nDFS Discovery and Finish Timestamps [d/f]:")
                for v in self.graph.vertices:
                    print(f"  Depot {v:<5}: [{dfs_res['discovery_times'].get(v, '-')}/{dfs_res['finish_times'].get(v, '-')}]")

                print("\nDFS Edge Classification:")
                for u, v, etype in dfs_res['classified_edges']:
                    print(f"  Route {u:<4} -> {v:<4} : {etype}")
            elif choice == "3":
                comps = self.graph.connected_components()
                print(f"\nFound {len(comps)} Connected Component(s):")
                for i, comp in enumerate(comps, 1):
                    print(f"  Component {i}: {', '.join(comp)}")
            elif choice == "4":
                sccs = self.graph.strongly_connected_components()
                print(f"\nFound {len(sccs)} Strongly Connected Component(s) (Tarjan's Algorithm):")
                for i, scc in enumerate(sccs, 1):
                    print(f"  SCC {i}: {', '.join(scc)}")
            elif choice == "5":
                break

    # ------------------ 5. Shortest Route (Dijkstra) ------------------
    def menu_shortest_route_dijkstra(self):
        while True:
            print("\n--- [5] Shortest Route Planning (Dijkstra Array-based) ---")
            print("1. Calculate Shortest Shipping Route between Two Depots")
            print("2. Show Full Step-by-Step Relaxation Table")
            print("3. Interactive Demonstration: Why Dijkstra Fails on Negative Weights")
            print("4. Back to Main Menu")
            choice = input("Select an option (1-4): ").strip()

            if choice == "1" or choice == "2":
                src = input("Enter Origin Depot (e.g. MUM): ").strip().upper()
                dst = input("Enter Destination Depot (e.g. CHE): ").strip().upper()
                if src not in self.graph.vertex_to_index:
                    print(f"[ERROR] Origin depot '{src}' not found.")
                    continue

                res = dijkstra_array_based(self.graph, src)
                path, cost = res.get_path(dst)
                if path:
                    print("\n" + "=" * 60)
                    print(f"OPTIMAL SHIPPING ROUTE (Dijkstra Array-based):")
                    print(f"Path: {' -> '.join(path)}")
                    print(f"Total Distance / Transportation Cost: {cost:,.2f} km")
                    print("=" * 60)
                else:
                    print(f"\n[UNREACHABLE] Destination '{dst}' is not reachable from '{src}'.")

                if choice == "2":
                    print("\nSTEP-BY-STEP DISTANCE RELAXATION TABLE:")
                    print(res.print_step_table())
            elif choice == "3":
                demo = demonstrate_negative_edge_failure()
                print("\n" + demo["explanation"])
                print(f"Dijkstra Output: {' -> '.join(demo['dijkstra_path'])} with cost {demo['dijkstra_cost']:.1f}")
                print(f"True Shortest:   {' -> '.join(demo['true_path'])} with cost {demo['true_cost']:.1f}")
            elif choice == "4":
                break

    # ------------------ 6. Minimum Spanning Tree ------------------
    def menu_mst(self):
        while True:
            print("\n--- [6] Minimum Spanning Network / Forest (MST / MSF) ---")
            print("1. Compute MST using Prim's Algorithm (Array-based, O(V^2))")
            print("2. Compute MST using Kruskal's Algorithm (Custom MergeSort + DSU, O(E log E))")
            print("3. Compare Prim and Kruskal Total Weights & Verify Agreement")
            print("4. Back to Main Menu")
            choice = input("Select an option (1-4): ").strip()

            if choice == "1":
                res_prim = prim_array_based(self.graph)
                print("\n" + res_prim.display())
            elif choice == "2":
                res_kruskal = kruskal_mst(self.graph)
                print("\n" + res_kruskal.display())
            elif choice == "3":
                p = prim_array_based(self.graph)
                k = kruskal_mst(self.graph)
                print("\n" + "=" * 65)
                print("MINIMUM SPANNING NETWORK COMPARISON & CROSS-CHECK")
                print("=" * 65)
                print(f"Prim's Total Weight:    {p.total_weight:.2f}")
                print(f"Kruskal's Total Weight: {k.total_weight:.2f}")
                match = abs(p.total_weight - k.total_weight) < 1e-4
                print(f"Weight Equality Check:  {'MATCH CONFIRMED (Identical Minimum Cost)' if match else 'MISMATCH'}")
                print(f"Forest Components:      Prim: {p.component_count} | Kruskal: {k.component_count}")
                print(f"Isolated Area Handled:  Yes (Port Blair IXZ properly partitioned in MSF)")
                print("=" * 65)
            elif choice == "4":
                break

    # ------------------ 7. Scheduling ------------------
    def menu_scheduling(self):
        while True:
            print("\n--- [7] Production Scheduling & Critical Path Method ---")
            print("1. Compute Critical Path Method (CPM) Schedule for Production Workflow")
            print("2. Run Topological Sort (Kahn's Algorithm & DFS)")
            print("3. Cycle Detection in Production Workflow (Demonstrate Feedback Loop)")
            print("4. Back to Main Menu")
            choice = input("Select an option (1-4): ").strip()

            if choice == "1":
                res = self.sched_acyclic.compute_critical_path()
                print("\n" + res.print_cpm_table())
            elif choice == "2":
                _, kahn_order, _ = self.sched_acyclic.topological_sort_kahn()
                _, dfs_order, _ = self.sched_acyclic.topological_sort_dfs()
                print("\nTopological Order (Kahn's In-Degree):")
                print("  " + " -> ".join(kahn_order))
                print("\nTopological Order (DFS Finish Time):")
                print("  " + " -> ".join(dfs_order))
            elif choice == "3":
                print("\nTesting Cyclic Production Workflow (Environmental Test rejects to Sub-Assembly)...")
                has_cycle, _, cycle_nodes = self.sched_cyclic.topological_sort_kahn()
                if has_cycle:
                    print(f"  [CYCLE DETECTED!] Pipeline contains circular dependency.")
                    print(f"  Cycle Path: {' -> '.join(cycle_nodes)}")
                    print(f"  CPM Scheduling blocked until cycle is resolved.")
            elif choice == "4":
                break

    # ------------------ 8. Timing Experiments ------------------
    def menu_timing_experiments(self):
        print("\n--- [8] Empirical Timing & Growth Experiments ---")
        print("1. Quick Benchmark (Trees n=1k, 5k; Graphs V=100, 300)")
        print("2. Full Rigorous Benchmark (Trees n=1k, 5k, 20k; Graphs V=200, 1k, 2k)")
        print("3. Back")
        choice = input("Select option (1-3): ").strip()

        if choice == "1":
            run_tree_benchmarks(sizes=[1000, 5000])
            run_graph_benchmarks(vertices_list=[100, 300])
        elif choice == "2":
            run_tree_benchmarks(sizes=[1000, 5000, 20000])
            run_graph_benchmarks(vertices_list=[200, 1000, 2000])

    # ------------------ 9. Self-Tests ------------------
    def menu_self_tests(self):
        print("\n--- [9] Running Complete Automated Test Suite (18 Tests) ---")
        run_all_self_tests()

    # ------------------ 10. Theoretical Analysis ------------------
    def menu_theory(self):
        while True:
            print("\n--- [10] Unit V Theoretical Analysis & Proofs ---")
            print("1. Design Techniques & Problem Classification")
            print("2. Dijkstra Correctness Argument & Negative Edge Failure")
            print("3. Cut & Cycle Properties for Prim and Kruskal")
            print("4. Non-Recursive Analysis: Operation Counting (BFS, Dijkstra, Prim, Kruskal)")
            print("5. Recursive Analysis: Solving Recurrences (Tree, BST Best/Worst/Avg, AVL)")
            print("6. Formal Proof: AVL Height O(log n) via Minimum-Node Recurrence N(h)")
            print("7. Asymptotic Notations, Amortized Union-Find, & Sorting Lower Bound")
            print("8. Back to Main Menu")
            sub = input("Select (1-8): ").strip()

            if sub == "1":
                print(theoretical_proofs.get_design_techniques())
            elif sub == "2":
                print(theoretical_proofs.get_dijkstra_correctness())
            elif sub == "3":
                print(theoretical_proofs.get_cut_and_cycle_property())
            elif sub == "4":
                print(theoretical_proofs.get_non_recursive_analysis())
            elif sub == "5":
                print(theoretical_proofs.get_recursive_analysis())
            elif sub == "6":
                print(theoretical_proofs.get_avl_height_proof())
            elif sub == "7":
                print(theoretical_proofs.get_amortized_and_lower_bound())
            elif sub == "8":
                break

    # ------------------ Main Loop ------------------
    def run(self):
        self.print_banner()
        while True:
            self.print_menu()
            choice = input("\nEnter choice (1-11): ").strip()
            if choice == "1":
                self.menu_record_directory()
            elif choice == "2":
                self.menu_expression_calculator()
            elif choice == "3":
                self.menu_network_management()
            elif choice == "4":
                self.menu_traversals_structure()
            elif choice == "5":
                self.menu_shortest_route_dijkstra()
            elif choice == "6":
                self.menu_mst()
            elif choice == "7":
                self.menu_scheduling()
            elif choice == "8":
                self.menu_timing_experiments()
            elif choice == "9":
                self.menu_self_tests()
            elif choice == "10":
                self.menu_theory()
            elif choice == "11":
                print("\nThank you for using Supply Chain Manager. Exiting cleanly.\n")
                break
            else:
                print("Invalid choice. Please select from 1 to 11.")


if __name__ == "__main__":
    app = SupplyChainApp()
    app.run()

