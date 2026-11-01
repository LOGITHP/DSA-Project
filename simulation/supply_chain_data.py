"""
simulation/supply_chain_data.py
Realistic pre-configured dataset for Supply Chain Manager (Project 19).

Features:
1. 13-node nationwide multimodal logistics network:
   - Includes at least 1 isolated/disconnected depot (IXZ - Port Blair Island Depot)
   - Includes at least 1 one-way edge (MUM -> PUN Express Cargo Transit corridor)
2. Production stage workflow with task durations:
   - Acyclic production DAG for Critical Path Method
   - Cyclic workflow for cycle detection demonstration
3. Hierarchical product taxonomy (General Tree)
4. Sample inventory by SKU (BST)
5. Certified supplier directory (AVL Tree)
6. Random graph and key generator with fixed seed for reproducible experiments
"""

import random
from typing import Tuple, List, Dict, Any
from structures.graph import Graph
from structures.general_tree import GeneralTree
from structures.bst import BinarySearchTree
from structures.avl_tree import AVLTree
from algorithms.scheduling import ProductionScheduler


def create_sample_supply_chain_graph() -> Graph:
    """
    Creates a 13-depot realistic multimodal supply chain graph.
    - Total Nodes: 13 (>= 12 requirement satisfied)
    - Disconnected Area: 'IXZ' (Port Blair Island Depot is isolated by sea)
    - One-way Edge: 'MUM' -> 'PUN' (One-way priority express pipeline)
    """
    g = Graph(is_directed=False, is_weighted=True)

    # 13 Depots
    depots = [
        ("MUM", {"name": "Mumbai West Gateway Hub", "type": "Sea/Air Port"}),
        ("DEL", {"name": "Delhi Northern Mega Hub", "type": "Inland Port"}),
        ("BLR", {"name": "Bengaluru Southern Hub", "type": "High-Tech Cargo"}),
        ("CHE", {"name": "Chennai Coastal Terminal", "type": "Sea Port"}),
        ("KOL", {"name": "Kolkata Eastern Hub", "type": "Riverine Port"}),
        ("HYD", {"name": "Hyderabad Central Depot", "type": "Air Cargo"}),
        ("PUN", {"name": "Pune Manufacturing Center", "type": "Industrial Depot"}),
        ("AHM", {"name": "Ahmedabad Logistics Hub", "type": "Textile/Chemical"}),
        ("JAI", {"name": "Jaipur Transit Depot", "type": "Rail Freight"}),
        ("LKO", {"name": "Lucknow North Depot", "type": "Regional Hub"}),
        ("NAG", {"name": "Nagpur Central Junction", "type": "Multimodal Hub"}),
        ("KOC", {"name": "Kochi Deepwater Terminal", "type": "Maritime Terminal"}),
        ("IXZ", {"name": "Port Blair Island Depot", "type": "Isolated Depot"})  # Disconnected!
    ]

    for code, meta in depots:
        g.add_vertex(code, meta)

    # Undirected bidirectional logistics routes (distances in km)
    routes = [
        ("MUM", "AHM", 525.0),
        ("AHM", "JAI", 650.0),
        ("JAI", "DEL", 280.0),
        ("DEL", "LKO", 500.0),
        ("LKO", "KOL", 980.0),
        ("DEL", "NAG", 1080.0),
        ("MUM", "NAG", 815.0),
        ("NAG", "HYD", 500.0),
        ("NAG", "KOL", 1120.0),
        ("HYD", "BLR", 570.0),
        ("BLR", "CHE", 345.0),
        ("BLR", "KOC", 540.0),
        ("CHE", "KOL", 1660.0),
        ("HYD", "CHE", 630.0),
        ("PUN", "HYD", 560.0),
    ]

    for u, v, w in routes:
        g.add_edge(u, v, w)

    # Add Directed one-way corridor: MUM -> PUN (150.0 km automated expressway)
    # To represent one-way in an otherwise undirected graph, we insert an edge specifically
    g.adj_list["MUM"].append(("PUN", 150.0))
    # In matrix:
    u_idx = g.vertex_to_index["MUM"]
    v_idx = g.vertex_to_index["PUN"]
    g.adj_matrix[u_idx][v_idx] = 150.0
    g.edges.append(g.edges[-1].__class__("MUM", "PUN", 150.0))

    return g


def create_sample_category_tree() -> GeneralTree:
    """Creates a sample 3-level Product Category General Tree."""
    tree = GeneralTree("Global Supply Chain Master Catalog")
    # Divisions
    tree.insert("Global Supply Chain Master Catalog", "Raw Materials")
    tree.insert("Global Supply Chain Master Catalog", "Intermediate Assemblies")
    tree.insert("Global Supply Chain Master Catalog", "Finished Consumer Goods")

    # Categories under Raw Materials
    tree.insert("Raw Materials", "Metals & Structural Alloys")
    tree.insert("Raw Materials", "Polymers & Resin Compounds")

    # Categories under Intermediate Assemblies
    tree.insert("Intermediate Assemblies", "Micro-Electronics & Sensors")
    tree.insert("Intermediate Assemblies", "Mechanical Actuators & Motors")

    # Categories under Finished Goods
    tree.insert("Finished Consumer Goods", "Consumer Robotics")
    tree.insert("Finished Consumer Goods", "Smart IoT Appliances")

    # Leaf product lines
    tree.insert("Metals & Structural Alloys", "Aerospace Grade Aluminum 7075")
    tree.insert("Metals & Structural Alloys", "Titanium Ti-6Al-4V Sheets")
    tree.insert("Micro-Electronics & Sensors", "ARM Cortex-M4 Microcontroller")
    tree.insert("Micro-Electronics & Sensors", "LiDAR Time-of-Flight Sensors")
    tree.insert("Consumer Robotics", "Autonomous Delivery Rover Mk-IV")

    return tree


def create_sample_inventory_bst() -> BinarySearchTree:
    """Pre-populates BST with sample SKU items."""
    bst = BinarySearchTree()
    sample_skus = [
        (500, "Core Processing Unit", 120, 185.50, "Electronics"),
        (250, "Aluminum Billet 50kg", 450, 42.00, "Raw Materials"),
        (750, "Lithium Polymer Battery 5Ah", 300, 68.75, "Energy"),
        (120, "Stepper Motor NEMA 17", 800, 15.20, "Actuators"),
        (380, "Precision Gearbox 10:1", 210, 54.30, "Mechanical"),
        (620, "Industrial Power Supply 24V", 160, 89.00, "Power"),
        (890, "Finished AGV Delivery Rover", 45, 1250.00, "Finished Goods"),
        (60, "Stainless Steel Fasteners (Pack 100)", 2500, 8.50, "Hardware"),
        (180, "Optical Encoders 1000-PPR", 340, 22.40, "Sensors"),
        (310, "Carbon Fiber Tube 1m", 190, 78.00, "Composites"),
        (440, "Thermal Interface Pad", 1200, 4.10, "Thermal")
    ]
    for sku, name, qty, price, cat in sample_skus:
        bst.insert(sku, name, qty, price, cat)
    return bst


def create_sample_supplier_avl() -> AVLTree:
    """Pre-populates AVL with sample certified suppliers."""
    avl = AVLTree(trace_rotations=False)
    sample_suppliers = [
        (201, "Bharat Heavy Metals Ltd", "Raw Materials", 14, 4.8, "Mumbai"),
        (105, "Silicon SemiTech Systems", "Semiconductors", 7, 4.9, "Bengaluru"),
        (315, "Precision Electro-Mech Corp", "Actuators", 10, 4.5, "Pune"),
        (420, "Apex Poly-Plastics Co", "Polymers", 5, 4.3, "Ahmedabad"),
        (150, "Eastern Steel & Wire Corp", "Metals", 18, 4.6, "Kolkata"),
        (280, "Delta Lithium Energy Storage", "Batteries", 8, 4.7, "Hyderabad"),
        (510, "Northline Sensorics Pvt Ltd", "Sensors", 6, 4.9, "Delhi")
    ]
    for sid, name, cat, lead, rating, loc in sample_suppliers:
        avl.insert(sid, name, cat, lead, rating, loc)
    return avl


def create_production_schedulers() -> Tuple[ProductionScheduler, ProductionScheduler]:
    """
    Returns:
      (acyclic_scheduler, cyclic_scheduler)
    Satisfies requirement: One acyclic dependency list with durations and one containing a cycle.
    """
    # 1. Acyclic Scheduler (Valid Workflow for CPM)
    sched_acyclic = ProductionScheduler()
    tasks = [
        ("T1", "Raw Material Sourcing", 4.0),
        ("T2", "Quality & Chemical Testing", 2.0),
        ("T3", "Sub-Assembly Fabrication", 6.0),
        ("T4", "PCB SMT Pick & Place", 3.0),
        ("T5", "System Enclosure Integration", 5.0),
        ("T6", "Firmware Flash & Calibration", 2.0),
        ("T7", "Environmental Stress Test", 4.0),
        ("T8", "Final Packaging & Dispatch", 1.0)
    ]
    for tid, name, dur in tasks:
        sched_acyclic.add_task(tid, name, dur)

    # Dependencies
    sched_acyclic.add_dependency("T1", "T2")
    sched_acyclic.add_dependency("T2", "T3")
    sched_acyclic.add_dependency("T2", "T4")
    sched_acyclic.add_dependency("T3", "T5")
    sched_acyclic.add_dependency("T4", "T5")
    sched_acyclic.add_dependency("T5", "T6")
    sched_acyclic.add_dependency("T6", "T7")
    sched_acyclic.add_dependency("T7", "T8")

    # 2. Cyclic Scheduler (Contains feedback loop for cycle detection testing)
    sched_cyclic = ProductionScheduler()
    for tid, name, dur in tasks:
        sched_cyclic.add_task(tid, name, dur)

    sched_cyclic.add_dependency("T1", "T2")
    sched_cyclic.add_dependency("T2", "T3")
    sched_cyclic.add_dependency("T3", "T5")
    sched_cyclic.add_dependency("T5", "T7")
    # Circular feedback loop: T7 (Environmental Test) rejects batch back to T3 (Sub-Assembly)!
    sched_cyclic.add_dependency("T7", "T3")
    sched_cyclic.add_dependency("T7", "T8")

    return sched_acyclic, sched_cyclic


def generate_random_graph(V: int, edge_factor: float, seed: int = 42, is_directed: bool = False) -> Graph:
    """
    Generates reproducible random connected graph using fixed seed.
    Sparse: edge_factor ~ 2.0 (E ~ 2V)
    Dense:  edge_factor ~ V/4.0 (E ~ V^2 / 4)
    """
    random.seed(seed)
    g = Graph(is_directed=is_directed, is_weighted=True)

    # Add vertices
    for i in range(V):
        g.add_vertex(f"Hub_{i}")

    # Build a spanning backbone first to guarantee connectivity
    for i in range(1, V):
        p = random.randint(0, i - 1)
        w = round(random.uniform(10.0, 500.0), 1)
        g.add_edge(f"Hub_{p}", f"Hub_{i}", w)

    # Target total edges
    target_edges = int(V * edge_factor)
    current_edges = V - 1

    existing_edges = set()
    for e in g.edges:
        existing_edges.add((e.u, e.v))
        if not is_directed:
            existing_edges.add((e.v, e.u))

    attempts = 0
    max_attempts = target_edges * 10
    while current_edges < target_edges and attempts < max_attempts:
        attempts += 1
        u = f"Hub_{random.randint(0, V - 1)}"
        v = f"Hub_{random.randint(0, V - 1)}"
        if u != v and (u, v) not in existing_edges:
            w = round(random.uniform(10.0, 500.0), 1)
            g.add_edge(u, v, w)
            existing_edges.add((u, v))
            if not is_directed:
                existing_edges.add((v, u))
            current_edges += 1

    return g

