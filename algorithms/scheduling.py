"""
algorithms/scheduling.py
Production Scheduling, Topological Sorting, and Critical Path Method (CPM).
Required explicitly for Project 19 (Supply Chain Manager).

Features:
1. Topological Sort via Kahn's Algorithm (In-degree queue)
2. Topological Sort via DFS with discovery/finish ordering
3. Cycle Detection with cycle path extraction and display
4. Critical Path Method (CPM):
   - Earliest Start Time (EST)
   - Earliest Finish Time (EFT)
   - Latest Start Time (LST)
   - Latest Finish Time (LFT)
   - Total Slack / Float
   - Critical Path (zero slack path / longest duration path in DAG)
"""

from typing import Dict, List, Optional, Tuple, Set, Any
from structures.common_utils import Queue, Stack
from structures.graph import Graph


class ProductionTask:
    def __init__(self, task_id: str, name: str, duration_days: float):
        self.task_id = task_id
        self.name = name
        self.duration = duration_days

    def __repr__(self) -> str:
        return f"Task({self.task_id}: '{self.name}', dur={self.duration}d)"


class ScheduleResult:
    def __init__(self, has_cycle: bool, topological_order: Optional[List[str]] = None, cycle_nodes: Optional[List[str]] = None, cpm_table: Optional[List[Dict[str, Any]]] = None, critical_path: Optional[List[str]] = None, project_duration: float = 0.0):
        self.has_cycle = has_cycle
        self.topological_order = topological_order or []
        self.cycle_nodes = cycle_nodes or []
        self.cpm_table = cpm_table or []
        self.critical_path = critical_path or []
        self.project_duration = project_duration

    def print_cpm_table(self) -> str:
        if self.has_cycle:
            return f"Cannot schedule: Cycle detected in production workflow!\nCycle Path: {' -> '.join(self.cycle_nodes)}"

        lines = []
        lines.append("=" * 105)
        lines.append(f"{'Task ID':<10} | {'Task Name':<28} | {'Dur(d)':<7} | {'EST':<6} | {'EFT':<6} | {'LST':<6} | {'LFT':<6} | {'Slack':<6} | {'Critical?'}")
        lines.append("-" * 105)
        for row in self.cpm_table:
            crit_flag = "★ YES" if row['is_critical'] else "  No"
            lines.append(f"{row['task_id']:<10} | {row['name']:<28} | {row['duration']:<7.1f} | {row['est']:<6.1f} | {row['eft']:<6.1f} | {row['lst']:<6.1f} | {row['lft']:<6.1f} | {row['slack']:<6.1f} | {crit_flag}")
        lines.append("=" * 105)
        lines.append(f"TOTAL PROJECT CRITICAL DURATION: {self.project_duration:.1f} days")
        lines.append(f"CRITICAL PATH: {' -> '.join(self.critical_path)}")
        lines.append("=" * 105)
        return "\n".join(lines)


class ProductionScheduler:
    """
    Production Workflow DAG Scheduler.
    Computes Topological ordering, detects cycles, and calculates Critical Path Method parameters.
    """
    def __init__(self):
        self.tasks: Dict[str, ProductionTask] = {}
        # Precedence graph: u -> v means u must precede v
        self.graph = Graph(is_directed=True, is_weighted=True)

    def add_task(self, task_id: str, name: str, duration_days: float) -> None:
        self.tasks[task_id] = ProductionTask(task_id, name, duration_days)
        self.graph.add_vertex(task_id, {"name": name, "duration": duration_days})

    def add_dependency(self, prereq_id: str, next_id: str) -> None:
        """prereq_id must complete before next_id can start."""
        if prereq_id not in self.tasks:
            raise ValueError(f"Task '{prereq_id}' not found")
        if next_id not in self.tasks:
            raise ValueError(f"Task '{next_id}' not found")
        self.graph.add_edge(prereq_id, next_id, weight=self.tasks[prereq_id].duration)

    # ------------------ 1. Kahn's Algorithm (Topological Sort) ------------------
    def topological_sort_kahn(self) -> Tuple[bool, List[str], List[str]]:
        """
        Kahn's In-Degree Algorithm for Topological Sorting and Cycle Detection.
        Returns: (has_cycle, order_if_acyclic, cycle_nodes_if_any)
        """
        in_degree: Dict[str, int] = {v: 0 for v in self.graph.vertices}
        for u in self.graph.vertices:
            for v, _ in self.graph.get_neighbors(u):
                in_degree[v] += 1

        q = Queue()
        for v in self.graph.vertices:
            if in_degree[v] == 0:
                q.enqueue(v)

        order = []
        while not q.is_empty():
            curr = q.dequeue()
            order.append(curr)

            for neighbor, _ in self.graph.get_neighbors(curr):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    q.enqueue(neighbor)

        if len(order) < len(self.graph.vertices):
            # Graph has a cycle; collect remaining vertices
            cycle_candidates = [v for v in self.graph.vertices if in_degree[v] > 0]
            cycle = self._extract_cycle(cycle_candidates)
            return True, [], cycle

        return False, order, []

    # ------------------ 2. DFS Topological Sort ------------------
    def topological_sort_dfs(self) -> Tuple[bool, List[str], List[str]]:
        """
        DFS-based Topological Sort using 3-coloring (0=White, 1=Gray, 2=Black).
        Returns: (has_cycle, order_if_acyclic, cycle_nodes_if_any)
        """
        color: Dict[str, int] = {v: 0 for v in self.graph.vertices}
        parent: Dict[str, Optional[str]] = {v: None for v in self.graph.vertices}
        order: List[str] = []
        cycle: List[str] = []
        has_cycle = False

        def _dfs(u: str) -> bool:
            nonlocal has_cycle
            color[u] = 1  # Gray (visiting)

            for v, _ in self.graph.get_neighbors(u):
                if color[v] == 1:
                    # Back edge found -> cycle!
                    has_cycle = True
                    cycle.clear()
                    curr = u
                    cycle.append(v)
                    while curr != v and curr is not None:
                        cycle.append(curr)
                        curr = parent[curr]
                    cycle.append(v)
                    cycle.reverse()
                    return False
                elif color[v] == 0:
                    parent[v] = u
                    if not _dfs(v):
                        return False

            color[u] = 2  # Black (finished)
            order.append(u)
            return True

        for v in self.graph.vertices:
            if color[v] == 0:
                if not _dfs(v):
                    break

        if has_cycle:
            return True, [], cycle

        order.reverse()
        return False, order, []

    def _extract_cycle(self, candidates: List[str]) -> List[str]:
        """Extracts simple cycle from candidate vertices."""
        visited = set()
        stack = []
        in_stack = set()

        def _find(u: str) -> Optional[List[str]]:
            visited.add(u)
            stack.append(u)
            in_stack.add(u)
            for v, _ in self.graph.get_neighbors(u):
                if v in in_stack:
                    idx = stack.index(v)
                    return stack[idx:] + [v]
                if v not in visited and v in candidates:
                    cyc = _find(v)
                    if cyc:
                        return cyc
            stack.pop()
            in_stack.remove(u)
            return None

        for c in candidates:
            if c not in visited:
                cyc = _find(c)
                if cyc:
                    return cyc
        return candidates

    # ------------------ 3. Critical Path Method (CPM) ------------------
    def compute_critical_path(self) -> ScheduleResult:
        """
        Computes EST, EFT, LST, LFT, Slack and Critical Path using CPM on DAG.
        """
        has_cycle, topo_order, cycle_nodes = self.topological_sort_kahn()
        if has_cycle:
            return ScheduleResult(True, cycle_nodes=cycle_nodes)

        # 1. Forward Pass: Earliest Start Time (EST) & Earliest Finish Time (EFT)
        est: Dict[str, float] = {v: 0.0 for v in topo_order}
        eft: Dict[str, float] = {v: 0.0 for v in topo_order}

        # Predecessors map
        predecessors: Dict[str, List[str]] = {v: [] for v in topo_order}
        for u in topo_order:
            for v, _ in self.graph.get_neighbors(u):
                predecessors[v].append(u)

        for u in topo_order:
            dur = self.tasks[u].duration
            if predecessors[u]:
                est[u] = max(eft[p] for p in predecessors[u])
            else:
                est[u] = 0.0
            eft[u] = est[u] + dur

        # Total project duration is max EFT across all sink nodes
        project_duration = max(eft.values()) if eft else 0.0

        # 2. Backward Pass: Latest Finish Time (LFT) & Latest Start Time (LST)
        lft: Dict[str, float] = {v: project_duration for v in topo_order}
        lst: Dict[str, float] = {v: 0.0 for v in topo_order}

        for u in reversed(topo_order):
            dur = self.tasks[u].duration
            successors = [v for v, _ in self.graph.get_neighbors(u)]
            if successors:
                lft[u] = min(lst[s] for s in successors)
            else:
                lft[u] = project_duration
            lst[u] = lft[u] - dur

        # 3. Calculate Slack and identify Critical Path
        slack: Dict[str, float] = {}
        cpm_table = []
        for v in topo_order:
            slk = round(lst[v] - est[v], 4)
            # Guard against negative zero float
            if abs(slk) < 1e-9:
                slk = 0.0
            slack[v] = slk
            is_critical = (slk == 0.0)
            cpm_table.append({
                "task_id": v,
                "name": self.tasks[v].name,
                "duration": self.tasks[v].duration,
                "est": est[v],
                "eft": eft[v],
                "lst": lst[v],
                "lft": lft[v],
                "slack": slk,
                "is_critical": is_critical
            })

        # Trace the critical path (nodes with slack == 0 where eft[u] == est[v])
        crit_nodes = [v for v in topo_order if slack[v] == 0.0]
        critical_path = []
        if crit_nodes:
            curr = crit_nodes[0]
            critical_path.append(curr)
            while True:
                next_crit = None
                for succ, _ in self.graph.get_neighbors(curr):
                    if slack[succ] == 0.0 and abs(eft[curr] - est[succ]) < 1e-9:
                        next_crit = succ
                        break
                if next_crit:
                    critical_path.append(next_crit)
                    curr = next_crit
                else:
                    break

        return ScheduleResult(
            has_cycle=False,
            topological_order=topo_order,
            cpm_table=cpm_table,
            critical_path=critical_path,
            project_duration=project_duration
        )

