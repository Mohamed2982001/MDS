"""
Master Design System (MDS) — DAG Compiler & Dependency Closure
Phase 9.7.10: Unified Local Orchestrator CLI & Master Validation Pipeline
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)
"""

from __future__ import annotations

from typing import Dict, List, Set, Optional
from .models import SubsystemDefinition
from .registry import ORCHESTRATOR_SUBSYSTEM_REGISTRY, MANDATORY_SAFETY_GATES


class OrchestratorDependencyCycleError(RuntimeError):
    """Raised when a dependency cycle is detected in the DAG."""
    pass


class OrchestratorInvalidDependencyError(KeyError):
    """Raised when a subsystem declares a dependency on an unknown ID."""
    pass


DAGCycleError = OrchestratorDependencyCycleError
InvalidTargetError = OrchestratorInvalidDependencyError


class DAGCompiler:
    """
    Compiles deterministic execution plans from ORCHESTRATOR_SUBSYSTEM_REGISTRY.
    Enforces Target Execution Closure, Kahn's algorithm with alphabetical tie-breaking,
    duplicate collapsing, and cycle detection.
    """

    def __init__(self, registry: Optional[Dict[str, SubsystemDefinition]] = None):
        self.registry = registry or ORCHESTRATOR_SUBSYSTEM_REGISTRY

    def get_transitive_closure(self, subsystem_id: str) -> Set[str]:
        """
        Recursively computes transitive dependency closure:
        TransitiveClosure(S) = union_{d in S.deps} ({d} union TransitiveClosure(d))
        """
        if subsystem_id not in self.registry:
            raise OrchestratorInvalidDependencyError(
                f"Subsystem '{subsystem_id}' is not in ORCHESTRATOR_SUBSYSTEM_REGISTRY"
            )

        closure: Set[str] = set()
        stack: List[str] = list(self.registry[subsystem_id].dependencies)

        while stack:
            dep = stack.pop()
            if dep not in self.registry:
                raise OrchestratorInvalidDependencyError(
                    f"Subsystem '{subsystem_id}' depends on unknown subsystem '{dep}'"
                )
            if dep not in closure:
                closure.add(dep)
                stack.extend(self.registry[dep].dependencies)

        return closure

    get_transitive_dependencies = get_transitive_closure

    def compute_target_closure(self, target_id: str) -> Set[str]:
        """
        Target Execution Closure:
        C(target) = MandatorySafetyGates union TransitiveClosure(target) union {target}
        """
        if target_id not in self.registry:
            raise OrchestratorInvalidDependencyError(
                f"Target subsystem '{target_id}' is not in ORCHESTRATOR_SUBSYSTEM_REGISTRY"
            )

        closure = set(MANDATORY_SAFETY_GATES)
        closure.update(self.get_transitive_closure(target_id))
        closure.add(target_id)
        return closure

    def detect_cycles(self, node_set: Set[str]) -> None:
        """
        Detects any cycles in the subgraph of node_set using depth-first traversal.
        Raises OrchestratorDependencyCycleError if a cycle is found.
        """
        visited: Dict[str, int] = {node: 0 for node in node_set}  # 0: unvisited, 1: visiting, 2: visited

        def dfs(node: str, path: List[str]) -> None:
            visited[node] = 1
            for dep in self.registry[node].dependencies:
                if dep in node_set:
                    if visited[dep] == 1:
                        cycle_path = " -> ".join(path + [dep])
                        raise OrchestratorDependencyCycleError(
                            f"Dependency cycle detected in execution subgraph: {cycle_path}"
                        )
                    if visited[dep] == 0:
                        dfs(dep, path + [dep])
            visited[node] = 2

        for node in sorted(node_set):
            if visited[node] == 0:
                dfs(node, [node])

    def compile_plan(self, selected_nodes: Set[str]) -> List[SubsystemDefinition]:
        """
        Compiles a deterministically ordered execution plan for selected_nodes using Kahn's algorithm.
        Sibling nodes with in-degree 0 at equal depth are ordered alphabetically by subsystem_id.
        Duplicate dependencies are collapsed.
        """
        # Validate that all nodes exist
        for node in selected_nodes:
            if node not in self.registry:
                raise OrchestratorInvalidDependencyError(
                    f"Selected node '{node}' is not registered"
                )

        # Detect any cycles
        self.detect_cycles(selected_nodes)

        # Compute in-degree within the selected subgraph
        in_degree: Dict[str, int] = {node: 0 for node in selected_nodes}
        graph: Dict[str, List[str]] = {node: [] for node in selected_nodes}

        for node in selected_nodes:
            for dep in self.registry[node].dependencies:
                if dep in selected_nodes:
                    graph[dep].append(node)
                    in_degree[node] += 1

        # Kahn's algorithm with alphabetical tie-breaking queue
        ready_queue: List[str] = sorted([n for n, deg in in_degree.items() if deg == 0])
        ordered_ids: List[str] = []

        while ready_queue:
            # Deterministic: pop the alphabetically lowest node
            current = ready_queue.pop(0)
            ordered_ids.append(current)

            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    ready_queue.append(neighbor)
                    ready_queue.sort()

        if len(ordered_ids) != len(selected_nodes):
            unprocessed = selected_nodes - set(ordered_ids)
            raise OrchestratorDependencyCycleError(
                f"Kahn's resolution failed: unprocessed nodes {sorted(unprocessed)}"
            )

        # Return list of SubsystemDefinition in deterministic execution order
        return [self.registry[node_id] for node_id in ordered_ids]

    def compile_profile(
        self,
        profile: str,
        target_subsystem: Optional[str] = None,
        registry: Optional[Dict[str, SubsystemDefinition]] = None,
    ) -> List[SubsystemDefinition]:
        """
        Compiles execution plan based on execution profile and optional targeted subsystem.
        """
        old_reg = self.registry
        if registry is not None:
            self.registry = registry

        try:
            if target_subsystem:
                from .registry import resolve_subsystem_id
                resolved = resolve_subsystem_id(target_subsystem)
                target_id = resolved if resolved else (target_subsystem if target_subsystem in self.registry else target_subsystem.upper())
                selected = self.compute_target_closure(target_id)
            else:
                profile_clean = profile.lower()
                if profile_clean == "fast":
                    selected = {
                        s_id
                        for s_id, s_def in self.registry.items()
                        if s_def.stage in (1, 2) and "fast" in s_def.supported_profiles
                    }
                elif profile_clean == "core":
                    selected = {
                        s_id
                        for s_id, s_def in self.registry.items()
                        if s_def.stage in (1, 2, 3) and "core" in s_def.supported_profiles
                    }
                elif profile_clean in ("full", "ci"):
                    selected = set(self.registry.keys())
                else:
                    selected = set(self.registry.keys())

                # Always ensure Mandatory Safety Gates are present if they exist in registry
                selected.update(g for g in MANDATORY_SAFETY_GATES if g in self.registry)

            return self.compile_plan(selected)
        finally:
            if registry is not None:
                self.registry = old_reg
