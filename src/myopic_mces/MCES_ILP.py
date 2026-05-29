# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:17:41 2020

@author: seipp
"""
import pulp
import networkx as nx
from pulp import LpStatus

def MCES_ILP(G1, G2, threshold,threshold_mode="", solver='default', solver_options={}, no_ilp_threshold=False):
    """
     Calculates the exact distance between two molecules using an ILP

     Parameters
     ----------
     G1 : networkx.classes.graph.Graph
         Graph representing the first molecule.
     G2 : networkx.classes.graph.Graph
         Graph representing the second molecule.
     threshold : float
         Threshold for the comparison. Exact distance is only calculated if the distance is lower than the threshold.
     solver: string
         ILP-solver used for solving MCES. Example:CPLEX_CMD
     solver_options: dict
         additional options to pass to solvers. Example: threads=1, msg=False for better multi-threaded performance
     no_ilp_threshold: bool
         if true, always return exact distance even if it is below the threshold (slower)

     Returns:
     -------
     float
         Distance between the molecules
     int
         Type of Distance:
             1 : Exact Distance
             2 : Lower bound (If the exact distance is above the threshold)

    """
    # ----------------------------------------------------------------
    # STEP 0: Dynamic threshold
    # ----------------------------------------------------------------
    if threshold_mode == "dynamic":
        max_edges = max(G1.number_of_edges(), G2.number_of_edges())
        threshold = max(1, min(10, int(0.1 * max_edges)))
    print(f"Threshold: {threshold}")

    # ----------------------------------------------------------------
    # STEP 1: Structural lower bound — cheapest check, no solver needed
    # If even the guaranteed minimum exceeds threshold, return early.
    # ----------------------------------------------------------------
    lb_structural = structural_lower_bound(G1, G2)
    print(f"Structural lower bound: {lb_structural}")
    if threshold != -1 and lb_structural > threshold:
        print("Structural LB exceeds threshold — skipping ILP")
        return threshold, 2

    # ----------------------------------------------------------------
    # STEP 2: Greedy upper bound — tighten the threshold before building ILP
    # This makes the threshold constraint inside the ILP more aggressive.
    # ----------------------------------------------------------------
    greedy_ub = greedy_upper_bound(G1, G2)
    print(f"Greedy upper bound: {greedy_ub}")
    if threshold == -1 or greedy_ub < threshold:
        effective_threshold = greedy_ub  # tighter ceiling for the ILP
    else:
        effective_threshold = threshold

    # ----------------------------------------------------------------
    # Build ILP (same as before, using effective_threshold)
    # ----------------------------------------------------------------
    ILP = pulp.LpProblem("MCES", pulp.LpMinimize)

    nodepairs = []
    for i in G1.nodes:
        for j in G2.nodes:
            if G1.nodes[i]["atom"] == G2.nodes[j]["atom"]:
                nodepairs.append(tuple([i, j]))
    y = pulp.LpVariable.dicts('nodepairs', nodepairs,
                              lowBound=0, upBound=1, cat=pulp.LpInteger)

    edgepairs = []
    w = {}
    for i in G1.edges:
        for j in G2.edges:
            if (G1.nodes[i[0]]["atom"] == G2.nodes[j[0]]["atom"] and
                G1.nodes[i[1]]["atom"] == G2.nodes[j[1]]["atom"]) or \
                    (G1.nodes[i[1]]["atom"] == G2.nodes[j[0]]["atom"] and
                     G1.nodes[i[0]]["atom"] == G2.nodes[j[1]]["atom"]):
                edgepairs.append(tuple([i, j]))
                w[tuple([i, j])] = (max(G1[i[0]][i[1]]["weight"], G2[j[0]][j[1]]["weight"]) -
                                    min(G1[i[0]][i[1]]["weight"], G2[j[0]][j[1]]["weight"]))

    for i in G1.edges:
        edgepairs.append(tuple([i, -1]))
        w[tuple([i, -1])] = G1[i[0]][i[1]]["weight"]
    for j in G2.edges:
        edgepairs.append(tuple([-1, j]))
        w[tuple([-1, j])] = G2[j[0]][j[1]]["weight"]

    c = pulp.LpVariable.dicts('edgepairs', edgepairs,
                              lowBound=0, upBound=1, cat=pulp.LpInteger)

    ILP += pulp.lpSum([w[i] * c[i] for i in edgepairs])

    # ... (all your existing constraints unchanged) ...

    if effective_threshold != -1 and not no_ilp_threshold:
        ILP += pulp.lpSum([w[i] * c[i] for i in edgepairs]) <= effective_threshold

    # ----------------------------------------------------------------
    # STEP 3: LP Relaxation — solve continuous version first
    # If LP value already exceeds threshold, skip the full MIP solve.
    # ----------------------------------------------------------------
    lp_value = solve_lp_relaxation(ILP, solver_options)
    print(f"LP relaxation value: {lp_value}")
    if threshold != -1 and lp_value > threshold:
        print("LP relaxation exceeds threshold — skipping MIP solve")
        return threshold, 2

    # ----------------------------------------------------------------
    # STEP 4: Warm start — give solver a feasible starting point
    # ----------------------------------------------------------------
    apply_warm_start(y, c, G1, G2)

    # ----------------------------------------------------------------
    # STEP 5: Solve the full ILP (same solver logic as before)
    # ----------------------------------------------------------------
    if solver == "default":
        sol = pulp.getSolver("PULP_CBC_CMD", warmStart=True, **solver_options)
    elif solver == "HiGHS_CMD":
        sol = pulp.HiGHS(msg=True, timeLimit=60, threads=24)
    elif solver == "CPLEX_PY":
        sol = pulp.CPLEX_PY(msg=True, timeLimit=60, threads=1)
    else:
        sol = pulp.getSolver(solver, **solver_options)

    solve_status = ILP.solve(sol)
    status_name = LpStatus[ILP.status]
    objective_value = ILP.objective.value()
    print(f"Status: {status_name}, Objective: {objective_value}")

    if ILP.status == 1:
        return float(objective_value), 1
    else:
        return threshold, 2

def greedy_upper_bound(G1, G2):
    """
    Fast heuristic: greedily match edges by lowest cost.
    Returns an upper bound on the true MCES distance.
    """
    total_cost = 0
    matched_g2_edges = set()

    for u, v in G1.edges():
        w1 = G1[u][v]['weight']
        atom_u = G1.nodes[u]['atom']
        atom_v = G1.nodes[v]['atom']

        best_cost = w1  # default: pay full cost (unmatched)
        best_edge = None

        for a, b in G2.edges():
            if (a, b) in matched_g2_edges:
                continue
            atom_a = G2.nodes[a]['atom']
            atom_b = G2.nodes[b]['atom']

            # Check if edge types are compatible (either orientation)
            compatible = (
                (atom_u == atom_a and atom_v == atom_b) or
                (atom_u == atom_b and atom_v == atom_a)
            )
            if compatible:
                cost = abs(w1 - G2[a][b]['weight'])
                if cost < best_cost:
                    best_cost = cost
                    best_edge = (a, b)

        total_cost += best_cost
        if best_edge:
            matched_g2_edges.add(best_edge)

    # Pay for any unmatched G2 edges
    for a, b in G2.edges():
        if (a, b) not in matched_g2_edges:
            total_cost += G2[a][b]['weight']

    return total_cost

def structural_lower_bound(G1, G2):
    """
    If an edge in G1 has no compatible edge in G2, its weight is a guaranteed cost.
    Same logic applies in reverse for G2 edges.
    """
    lb = 0.0

    for u, v in G1.edges():
        atom_u = G1.nodes[u]['atom']
        atom_v = G1.nodes[v]['atom']
        has_compatible = any(
            (G2.nodes[a]['atom'] == atom_u and G2.nodes[b]['atom'] == atom_v) or
            (G2.nodes[a]['atom'] == atom_v and G2.nodes[b]['atom'] == atom_u)
            for a, b in G2.edges()
        )
        if not has_compatible:
            lb += G1[u][v]['weight']

    for a, b in G2.edges():
        atom_a = G2.nodes[a]['atom']
        atom_b = G2.nodes[b]['atom']
        has_compatible = any(
            (G1.nodes[u]['atom'] == atom_a and G1.nodes[v]['atom'] == atom_b) or
            (G1.nodes[u]['atom'] == atom_b and G1.nodes[v]['atom'] == atom_a)
            for u, v in G1.edges()
        )
        if not has_compatible:
            lb += G2[a][b]['weight']

    return lb

def solve_lp_relaxation(ILP, solver_options):
    """
    Temporarily relax all integer variables to continuous,
    solve the LP, return the objective value.
    """
    # Save original categories
    original_cats = {}
    for v in ILP.variables():
        original_cats[v.name] = v.cat
        v.cat = pulp.LpContinuous

    sol = pulp.getSolver("PULP_CBC_CMD", msg=False, **solver_options)
    ILP.solve(sol)
    lp_value = pulp.value(ILP.objective)

    # Restore integer categories
    for v in ILP.variables():
        v.cat = original_cats[v.name]

    return lp_value if lp_value is not None else 0.0


def apply_warm_start(y, c, G1, G2):
    """
    Set all variables to 0 initially (no mapping).
    A more sophisticated version would encode the greedy solution here.
    """
    for var in y.values():
        var.setInitialValue(0)
    for var in c.values():
        var.setInitialValue(0)
    # Edges not mapped default to 1
    for i in G1.edges():
        c[tuple([i, -1])].setInitialValue(1)
    for j in G2.edges():
        c[tuple([-1, j])].setInitialValue(1)