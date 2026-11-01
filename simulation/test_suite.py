"""
simulation/test_suite.py
Comprehensive Automated Verification Test Suite (18 Automated Test Cases).
Satisfies all Section 4 requirements:
- At least 15 automated test cases covering normal, edge, and failure inputs
- Cross-checking results (Prim vs Kruskal MST weights, BFS vs Dijkstra on unweighted graphs)
- BST vs AVL on 1,000 sorted IDs
- AVL 10,000 random operations stress test with verify()
- Expression Tree error handling (operand shortage, division by zero)
- Graph properties: >= 12 nodes, disconnected component, one-way edge
- Production workflow DAG with CPM and cycle detection
- Dijkstra negative edge counterexample
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
import math
import time
from typing import List, Tuple

from structures.common_utils import Stack, Queue, merge_sort
from structures.general_tree import GeneralTree
from structures.bst import BinarySearchTree
from structures.avl_tree import AVLTree
from structures.expression_tree import ExpressionTree
from structures.disjoint_set import DisjointSet
from structures.graph import Graph
from algorithms.dijkstra import dijkstra_array_based, demonstrate_negative_edge_failure
from algorithms.mst import prim_array_based, kruskal_mst
from algorithms.scheduling import ProductionScheduler
from simulation.supply_chain_data import (
    create_sample_supply_chain_graph,
    create_sample_category_tree,
    create_sample_inventory_bst,
    create_sample_supplier_avl,
    create_production_schedulers,
    generate_random_graph
)


class TestRunner:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.failures = []

    def run_test(self, test_name: str, test_func):
        self.tests_run += 1
        print(f"[{self.tests_run:02d}] Running: {test_name:<65}", end="")
        try:
            test_func()
            self.tests_passed += 1
            print("[\033[92mPASS\033[0m]")
        except AssertionError as e:
            self.failures.append((test_name, str(e)))
            print(f"[\033[91mFAIL\033[0m] -> {e}")
        except Exception as e:
            self.failures.append((test_name, f"Exception: {type(e).__name__}: {e}"))
            print(f"[\033[91mERROR\033[0m] -> {type(e).__name__}: {e}")

    def summary(self) -> bool:
        print("\n" + "=" * 80)
        print(f"TEST SUITE SUMMARY: {self.tests_passed} / {self.tests_run} Passed")
        if self.failures:
            print("Failures:")
            for name, reason in self.failures:
                print(f"  - {name}: {reason}")
            print("=" * 80)
            return False
        else:
            print("ALL AUTOMATED SELF-TESTS PASSED SUCCESSFULLY! (100% Complete)")
            print("=" * 80)
            return True


# =====================================================================
# INDIVIDUAL TEST CASES
# =====================================================================

def test_01_general_tree_insert_and_delete_subtree():
    gt = GeneralTree("Root")
    assert gt.insert("Root", "A")
    assert gt.insert("Root", "B")
    assert gt.insert("A", "A1")
    assert gt.insert("A", "A2")
    assert gt.find_node("A1") is not None
    assert gt.delete_subtree("A")
    assert gt.find_node("A") is None
    assert gt.find_node("A1") is None
    assert gt.find_node("B") is not None


def test_02_general_tree_traversals():
    gt = GeneralTree("Corp")
    gt.insert("Corp", "DivA")
    gt.insert("Corp", "DivB")
    gt.insert("DivA", "Prod1")
    gt.insert("DivA", "Prod2")

    # Verify recursive matches iterative
    pre_rec = gt.preorder_recursive()
    pre_iter = gt.preorder_iterative()
    assert pre_rec == pre_iter, f"Preorder mismatch: {pre_rec} vs {pre_iter}"

    post_rec = gt.postorder_recursive()
    post_iter = gt.postorder_iterative()
    assert post_rec == post_iter, f"Postorder mismatch: {post_rec} vs {post_iter}"

    lvl_rec = gt.level_order_recursive()
    lvl_iter = gt.level_order_iterative()
    assert lvl_rec == lvl_iter, f"Level-order mismatch: {lvl_rec} vs {lvl_iter}"


def test_03_bst_crud_and_three_delete_cases():
    bst = BinarySearchTree()
    # Insert keys
    for k in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(k, f"Item_{k}")

    # Case 1: Delete Leaf (20)
    ok, case1 = bst.delete(20)
    assert ok and "Case 1" in case1
    assert bst.search(20) is None

    # Case 2: Delete Node with 1 Child
    # 30 now has only right child (40)
    ok, case2 = bst.delete(30)
    assert ok and "Case 2" in case2
    assert bst.search(30) is None
    assert bst.search(40) is not None

    # Case 3: Delete Node with 2 Children (50 root)
    ok, case3 = bst.delete(50)
    assert ok and "Case 3" in case3
    assert bst.search(50) is None
    # Root should now be successor (60)
    assert bst.root.sku == 60


def test_04_bst_search_min_max_pred_succ_range():
    bst = BinarySearchTree()
    for k in [10, 25, 5, 15, 30, 2, 8]:
        bst.insert(k, f"Item_{k}")

    assert bst.find_min().sku == 2
    assert bst.find_max().sku == 30
    assert bst.successor(10).sku == 15
    assert bst.predecessor(10).sku == 8

    # Range Query [5, 20] -> [5, 8, 10, 15]
    range_items = bst.range_query(5, 20)
    skus = [n.sku for n in range_items]
    assert skus == [5, 8, 10, 15], f"Range query failed: {skus}"


def test_05_bst_traversals_recursive_vs_iterative():
    bst = BinarySearchTree()
    for k in [40, 20, 60, 10, 30, 50, 70]:
        bst.insert(k, f"Item_{k}")

    assert bst.inorder_recursive() == bst.inorder_iterative() == [10, 20, 30, 40, 50, 60, 70]
    assert bst.preorder_recursive() == bst.preorder_iterative() == [40, 20, 10, 30, 60, 50, 70]
    assert bst.postorder_recursive() == bst.postorder_iterative() == [10, 30, 20, 50, 70, 60, 40]
    assert bst.level_order_recursive() == bst.level_order_iterative() == [40, 20, 60, 10, 30, 50, 70]


def test_06_bst_vs_avl_height_on_1000_sorted():
    bst = BinarySearchTree()
    avl = AVLTree()
    for i in range(1, 1001):
        bst.insert(i, f"Item_{i}")
        avl.insert(i, f"Supplier_{i}")

    bst_h = bst.height()
    avl_h = avl.height()
    # Degenerate BST on sorted input: height = 1000
    assert bst_h == 1000, f"BST height on sorted should be 1000, got {bst_h}"
    # AVL height is guaranteed <= 1.44 * log2(1002) ~ 14
    assert avl_h <= 14, f"AVL height on 1000 items should be <= 14, got {avl_h}"
    assert avl.verify()[0], "AVL verify failed"


def test_07_avl_rotations_all_four_cases():
    # 1. LL Rotation (Single Right)
    avl_ll = AVLTree()
    avl_ll.insert(30, "S30")
    avl_ll.insert(20, "S20")
    avl_ll.insert(10, "S10")  # LL triggered
    assert avl_ll.root.supplier_id == 20
    assert avl_ll.verify()[0]

    # 2. RR Rotation (Single Left)
    avl_rr = AVLTree()
    avl_rr.insert(10, "S10")
    avl_rr.insert(20, "S20")
    avl_rr.insert(30, "S30")  # RR triggered
    assert avl_rr.root.supplier_id == 20
    assert avl_rr.verify()[0]

    # 3. LR Rotation (Left-Right Double)
    avl_lr = AVLTree()
    avl_lr.insert(30, "S30")
    avl_lr.insert(10, "S10")
    avl_lr.insert(20, "S20")  # LR triggered
    assert avl_lr.root.supplier_id == 20
    assert avl_lr.verify()[0]

    # 4. RL Rotation (Right-Left Double)
    avl_rl = AVLTree()
    avl_rl.insert(10, "S10")
    avl_rl.insert(30, "S30")
    avl_rl.insert(20, "S20")  # RL triggered
    assert avl_rl.root.supplier_id == 20
    assert avl_rl.verify()[0]


def test_08_avl_10000_random_operations_stress():
    """Rigorously tests at least 10,000 random inserts and deletes with verify()."""
    avl = AVLTree(trace_rotations=False)
    random.seed(999)
    keys = list(range(1, 10001))
    random.shuffle(keys)

    # 10,000 random inserts
    for k in keys:
        avl.insert(k, f"Sup_{k}", "Metals", 5, 4.5, "Indore")

    assert avl.size() == 10000
    ok, msg = avl.verify()
    assert ok, f"AVL verification failed after 10,000 inserts: {msg}"
    assert avl.height() <= math.ceil(1.44 * math.log2(10002))

    # 5,000 random deletes
    delete_keys = keys[:5000]
    for k in delete_keys:
        avl.delete(k)

    assert avl.size() == 5000
    ok, msg = avl.verify()
    assert ok, f"AVL verification failed after 5,000 deletes: {msg}"


def test_09_expression_tree_valid_evaluation_and_minimal_parens():
    # Expression from PDF example: "dist rate * toll + 2 /"
    expr = ExpressionTree("dist rate * toll + 2 /")
    val_map = {"dist": 100.0, "rate": 5.0, "toll": 50.0}
    # (100 * 5 + 50) / 2 = 550 / 2 = 275.0
    ans = expr.evaluate(val_map)
    assert abs(ans - 275.0) < 1e-6

    # Minimal parentheses format check: "(dist * rate + toll) / 2"
    infix = expr.to_infix_minimal_parentheses()
    assert infix == "(dist * rate + toll) / 2"


def test_10_expression_tree_division_by_zero_and_operand_shortage():
    # 1. Division by zero
    expr = ExpressionTree("10 0 /")
    try:
        expr.evaluate()
        assert False, "Should have raised ZeroDivisionError"
    except ZeroDivisionError:
        pass

    # 2. Operand shortage
    try:
        ExpressionTree("10 +")
        assert False, "Should have raised ValueError for operand shortage"
    except ValueError as e:
        assert "operand shortage" in str(e).lower()


def test_11_graph_switchable_representation_and_memory():
    g = create_sample_supply_chain_graph()
    assert g.representation_mode == "list"
    g.set_representation_mode("matrix")
    assert g.representation_mode == "matrix"

    # Neighbors should match in both modes
    g.set_representation_mode("list")
    nbrs_list = set(v for v, _ in g.get_neighbors("MUM"))
    g.set_representation_mode("matrix")
    nbrs_matrix = set(v for v, _ in g.get_neighbors("MUM"))
    assert nbrs_list == nbrs_matrix, "Neighbors mismatched between list and matrix representations"

    # Memory report
    mem = g.report_memory_usage()
    assert mem["num_vertices"] >= 12
    assert mem["matrix_theoretical_bytes"] > 0
    assert mem["list_theoretical_bytes"] > 0


def test_12_bfs_fewest_stops_and_agreement_with_unweighted_dijkstra():
    # Unweighted graph where BFS and Dijkstra MUST yield identical shortest path distance
    g = Graph(is_directed=False, is_weighted=False)
    edges = [("A", "B"), ("B", "C"), ("C", "D"), ("A", "E"), ("E", "D")]
    for u, v in edges:
        g.add_edge(u, v, 1.0)

    # BFS
    bfs_path, bfs_hops = g.bfs_fewest_stops("A", "D")

    # Dijkstra on unweighted graph
    dijk_res = dijkstra_array_based(g, "A")
    dijk_path, dijk_cost = dijk_res.get_path("D")

    assert bfs_hops == dijk_cost == 2.0, "BFS and Dijkstra disagreed on unweighted graph!"
    assert len(bfs_path) == len(dijk_path) == 3


def test_13_dfs_edge_classification_and_scc():
    g = Graph(is_directed=True, is_weighted=False)
    # 1 -> 2 -> 3 -> 1 (Cycle / Back edge)
    # 1 -> 4 (Tree edge)
    g.add_edge("1", "2", 1.0)
    g.add_edge("2", "3", 1.0)
    g.add_edge("3", "1", 1.0)
    g.add_edge("1", "4", 1.0)

    res = g.dfs_edge_classification()
    edge_types = [etype for _, _, etype in res["classified_edges"]]
    assert any("Back Edge" in et for et in edge_types), "Back edge should be detected"
    assert any("Tree Edge" in et for et in edge_types), "Tree edge should be detected"

    sccs = g.strongly_connected_components()
    # Expect 2 SCCs: {1, 2, 3} and {4}
    assert len(sccs) == 2


def test_14_mst_prim_vs_kruskal_agreement():
    g = create_sample_supply_chain_graph()
    prim_res = prim_array_based(g)
    kruskal_res = kruskal_mst(g)

    # Both must give the EXACT same total weight
    assert abs(prim_res.total_weight - kruskal_res.total_weight) < 1e-4, (
        f"MST weights disagreed: Prim={prim_res.total_weight}, Kruskal={kruskal_res.total_weight}"
    )
    # Both must identify the disconnected island depot IXZ
    assert prim_res.is_forest and kruskal_res.is_forest
    assert prim_res.component_count == kruskal_res.component_count == 2


def test_15_topological_sort_kahn_and_dfs():
    sched_acyclic, _ = create_production_schedulers()

    # Kahn's
    has_cycle_k, order_k, _ = sched_acyclic.topological_sort_kahn()
    assert not has_cycle_k
    assert len(order_k) == 8

    # DFS
    has_cycle_d, order_d, _ = sched_acyclic.topological_sort_dfs()
    assert not has_cycle_d
    assert len(order_d) == 8

    # Verify precedence: T1 before T2, T2 before T3 and T4, etc.
    assert order_k.index("T1") < order_k.index("T2")
    assert order_k.index("T2") < order_k.index("T3")
    assert order_k.index("T7") < order_k.index("T8")


def test_16_cycle_detection_in_cyclic_workflow():
    _, sched_cyclic = create_production_schedulers()

    has_cycle_k, _, cycle_nodes_k = sched_cyclic.topological_sort_kahn()
    assert has_cycle_k, "Kahn should have detected cycle"
    assert len(cycle_nodes_k) > 0

    has_cycle_d, _, cycle_nodes_d = sched_cyclic.topological_sort_dfs()
    assert has_cycle_d, "DFS should have detected cycle"
    assert len(cycle_nodes_d) > 0


def test_17_critical_path_method_calculations():
    sched_acyclic, _ = create_production_schedulers()
    res = sched_acyclic.compute_critical_path()

    assert not res.has_cycle
    # T1 (4) -> T2 (2) -> T3 (6) -> T5 (5) -> T6 (2) -> T7 (4) -> T8 (1) = 24.0 days
    assert abs(res.project_duration - 24.0) < 1e-4, f"Expected 24 days, got {res.project_duration}"
    assert res.critical_path == ["T1", "T2", "T3", "T5", "T6", "T7", "T8"]

    # Verify T4 has positive slack:
    t4_entry = next(r for r in res.cpm_table if r['task_id'] == 'T4')
    assert t4_entry['slack'] > 0.0, "T4 should have positive slack"
    assert not t4_entry['is_critical']


def test_18_dijkstra_negative_edge_failure_demonstration():
    demo = demonstrate_negative_edge_failure()
    assert demo["dijkstra_cost"] != demo["true_cost"], "Dijkstra should fail on negative weight counterexample"
    assert demo["dijkstra_cost"] == 3.0
    assert demo["true_cost"] == 1.0


def run_all_self_tests() -> bool:
    runner = TestRunner()
    runner.run_test("01. General Tree Insert & Delete Subtree", test_01_general_tree_insert_and_delete_subtree)
    runner.run_test("02. General Tree Traversals (Recursive == Iterative)", test_02_general_tree_traversals)
    runner.run_test("03. BST CRUD & 3 Delete Cases (Leaf, 1 Child, 2 Children)", test_03_bst_crud_and_three_delete_cases)
    runner.run_test("04. BST Search, Min, Max, Pred, Succ, Range Query", test_04_bst_search_min_max_pred_succ_range)
    runner.run_test("05. BST 4 Traversals (Recursive == Iterative Stack/Queue)", test_05_bst_traversals_recursive_vs_iterative)
    runner.run_test("06. BST vs AVL Height on 1,000 Sorted IDs", test_06_bst_vs_avl_height_on_1000_sorted)
    runner.run_test("07. AVL Balancing: All 4 Rotations (LL, RR, LR, RL)", test_07_avl_rotations_all_four_cases)
    runner.run_test("08. AVL 10,000 Random Operations Verification Stress Test", test_08_avl_10000_random_operations_stress)
    runner.run_test("09. Expression Tree Postfix Build & Minimal Parentheses Infix", test_09_expression_tree_valid_evaluation_and_minimal_parens)
    runner.run_test("10. Expression Tree Error Handling (Zero Div & Operand Shortage)", test_10_expression_tree_division_by_zero_and_operand_shortage)
    runner.run_test("11. Graph Switchable Representations (Matrix/List) & Memory", test_11_graph_switchable_representation_and_memory)
    runner.run_test("12. BFS Fewest Stops & Cross-Check with Unweighted Dijkstra", test_12_bfs_fewest_stops_and_agreement_with_unweighted_dijkstra)
    runner.run_test("13. DFS Edge Classification (Tree, Back, Forward, Cross) & SCC", test_13_dfs_edge_classification_and_scc)
    runner.run_test("14. MST Prim vs Kruskal Exact Total Weight Agreement & Forest", test_14_mst_prim_vs_kruskal_agreement)
    runner.run_test("15. Production Scheduling Topological Sort (Kahn & DFS)", test_15_topological_sort_kahn_and_dfs)
    runner.run_test("16. Cycle Detection & Sequence Extraction in Cyclic Workflow", test_16_cycle_detection_in_cyclic_workflow)
    runner.run_test("17. Critical Path Method (EST, EFT, LST, LFT, Slack, Crit Path)", test_17_critical_path_method_calculations)
    runner.run_test("18. Shortest Path Dijkstra Negative Edge Failure Counterexample", test_18_dijkstra_negative_edge_failure_demonstration)

    return runner.summary()


if __name__ == "__main__":
    run_all_self_tests()
