# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:17:41 2020

@author: seipp

Corrected version keeping the same overall structure and call pattern:
    distance, compute_mode = MCES_ILP(G1, G2, threshold, threshold_mode, solver,
                                      solver_options=solver_options,
                                      no_ilp_threshold=no_ilp_threshold)
"""
import pulp
import networkx as nx
from pulp import LpStatus
import time
from collections import defaultdict


def structural_lower_bound(G1, G2):
    """
    Cheap valid lower bound:
    if an edge in one graph has no compatible atom-type edge in the other graph,
    then that edge must necessarily be unmatched.
    """
    lb = 0.0

    for u, v in G1.edges:
        atom_u = G1.nodes[u]["atom"]
        atom_v = G1.nodes[v]["atom"]
        has_compatible = any(
            (G2.nodes[a]["atom"] == atom_u and G2.nodes[b]["atom"] == atom_v) or
            (G2.nodes[a]["atom"] == atom_v and G2.nodes[b]["atom"] == atom_u)
            for a, b in G2.edges
        )
        if not has_compatible:
            lb += G1[u][v]["weight"]

    for a, b in G2.edges:
        atom_a = G2.nodes[a]["atom"]
        atom_b = G2.nodes[b]["atom"]
        has_compatible = any(
            (G1.nodes[u]["atom"] == atom_a and G1.nodes[v]["atom"] == atom_b) or
            (G1.nodes[u]["atom"] == atom_b and G1.nodes[v]["atom"] == atom_a)
            for u, v in G1.edges
        )
        if not has_compatible:
            lb += G2[a][b]["weight"]

    return lb


def solve_lp_relaxation(ILP, solver_options={}):
    """
    Temporarily relax all integer variables to continuous, solve the LP,
    restore the variable categories, and return (status, objective_value).

    Important: call this BEFORE adding the threshold constraint.
    """
    original_cats = {}
    for v in ILP.variables():
        original_cats[v.name] = v.cat
        v.cat = pulp.LpContinuous

    # Use CBC silently for the relaxation unless options override it.
    lp_solver_options = dict(solver_options)
    lp_solver_options.setdefault("msg", False)
    sol = pulp.getSolver(solver="PULP_CBC_CMD", **lp_solver_options)

    ILP.solve(sol)
    lp_status = ILP.status
    lp_value = pulp.value(ILP.objective)

    for v in ILP.variables():
        v.cat = original_cats[v.name]

    return lp_status, lp_value


def apply_warm_start(y, c, G1, G2):
    """
    Simple warm start: no nodes mapped, all edges initially unmatched.
    This is feasible with the edge-coverage constraints.
    """
    for var in y.values():
        var.setInitialValue(0)
    for var in c.values():
        var.setInitialValue(0)

    for i in G1.edges:
        c[tuple([i, -1])].setInitialValue(1)
    for j in G2.edges:
        c[tuple([-1, j])].setInitialValue(1)


def MCES_ILP(G1, G2, threshold, threshold_mode="dynamic", solver='default', solver_options={}, no_ilp_threshold=False):
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

    # Dynamic threshold
    if threshold_mode == "dynamic":
        max_edges = max(G1.number_of_edges(), G2.number_of_edges())
        threshold = max(1, min(10, int(0.1 * max_edges)))

    print(f"Threshold: {threshold}")
    actual_threshold = threshold


    # Cheap structural lower bound.
    # Respect no_ilp_threshold: if exact mode is requested, do not stop early.
    lb_structural = structural_lower_bound(G1, G2)

    skipped_by_structural_lb = 0

    if threshold != -1 and not no_ilp_threshold and lb_structural > threshold:
        skipped_by_structural_lb = 1

        print("Structural LB exceeds threshold — skipping ILP")

        return (
            threshold,
            2,
            actual_threshold,
            lb_structural,
            skipped_by_structural_lb
        )

    ILP = pulp.LpProblem("MCES", pulp.LpMinimize)

    # Variables for nodepairs
    nodepairs = []
    for i in G1.nodes:
        for j in G2.nodes:
            if G1.nodes[i]["atom"] == G2.nodes[j]["atom"]:
                nodepairs.append(tuple([i, j]))
    y = pulp.LpVariable.dicts('nodepairs', nodepairs,
                              lowBound=0,
                              upBound=1,
                              cat=pulp.LpInteger)

    # Variables for edgepairs and weight
    edgepairs = []
    w = {}
    for i in G1.edges:
        for j in G2.edges:
            if (G1.nodes[i[0]]["atom"] == G2.nodes[j[0]]["atom"] and G1.nodes[i[1]]["atom"] == G2.nodes[j[1]]["atom"]) or \
               (G1.nodes[i[1]]["atom"] == G2.nodes[j[0]]["atom"] and G1.nodes[i[0]]["atom"] == G2.nodes[j[1]]["atom"]):
                edgepairs.append(tuple([i, j]))
                w[tuple([i, j])] = max(G1[i[0]][i[1]]["weight"], G2[j[0]][j[1]]["weight"]) - \
                                   min(G1[i[0]][i[1]]["weight"], G2[j[0]][j[1]]["weight"])

    # Variables for not mapping an edge
    for i in G1.edges:
        edgepairs.append(tuple([i, -1]))
        w[tuple([i, -1])] = G1[i[0]][i[1]]["weight"]
    for j in G2.edges:
        edgepairs.append(tuple([-1, j]))
        w[tuple([-1, j])] = G2[j[0]][j[1]]["weight"]

    c = pulp.LpVariable.dicts('edgepairs', edgepairs,
                              lowBound=0,
                              upBound=1,
                              cat=pulp.LpInteger)

    # Objective function
    objective_expr = pulp.lpSum([w[i] * c[i] for i in edgepairs])
    ILP += objective_expr

    # Every node in G1 can only be mapped to at most one in G2
    for i in G1.nodes:
        h = []
        for j in G2.nodes:
            if G1.nodes[i]["atom"] == G2.nodes[j]["atom"]:
                h.append(tuple([i, j]))
        ILP += pulp.lpSum([y[k] for k in h]) <= 1

    # Every node in G2 can only be mapped to at most one in G1
    for i in G2.nodes:
        h = []
        for j in G1.nodes:
            if G1.nodes[j]["atom"] == G2.nodes[i]["atom"]:
                h.append(tuple([j, i]))
        ILP += pulp.lpSum([y[k] for k in h]) <= 1

    # Every edge in G1 has to be mapped to an edge in G2 or not mapped
    for i in G1.edges:
        ls = []
        for j in G2.edges:
            if (G1.nodes[i[0]]["atom"] == G2.nodes[j[0]]["atom"] and G1.nodes[i[1]]["atom"] == G2.nodes[j[1]]["atom"]) or \
               (G1.nodes[i[1]]["atom"] == G2.nodes[j[0]]["atom"] and G1.nodes[i[0]]["atom"] == G2.nodes[j[1]]["atom"]):
                ls.append(tuple([i, j]))
        ILP += pulp.lpSum([c[k] for k in ls]) + c[tuple([i, -1])] == 1

    # Every edge in G2 has to be mapped to an edge in G1 or not mapped
    for i in G2.edges:
        ls = []
        for j in G1.edges:
            if (G1.nodes[j[0]]["atom"] == G2.nodes[i[0]]["atom"] and G1.nodes[j[1]]["atom"] == G2.nodes[i[1]]["atom"]) or \
               (G1.nodes[j[1]]["atom"] == G2.nodes[i[0]]["atom"] and G1.nodes[j[0]]["atom"] == G2.nodes[i[1]]["atom"]):
                ls.append(tuple([j, i]))
        ILP += pulp.lpSum([c[k] for k in ls]) + c[tuple([-1, i])] == 1

    # The mapping of the edges has to match the mapping of the nodes
    for i in G1.nodes:
        for j in G2.edges:
            ls = []
            for k in G1.neighbors(i):
                if tuple([tuple([i, k]), j]) in c:
                    ls.append(tuple([tuple([i, k]), j]))
                else:
                    if tuple([tuple([k, i]), j]) in c:
                        ls.append(tuple([tuple([k, i]), j]))
            rs = []
            if G1.nodes[i]["atom"] == G2.nodes[j[0]]["atom"]:
                rs.append(tuple([i, j[0]]))
            if G1.nodes[i]["atom"] == G2.nodes[j[1]]["atom"]:
                rs.append(tuple([i, j[1]]))
            ILP += pulp.lpSum([c[k] for k in ls]) <= pulp.lpSum([y[k] for k in rs])

    for i in G2.nodes:
        for j in G1.edges:
            ls = []
            for k in G2.neighbors(i):
                if tuple([j, tuple([i, k])]) in c:
                    ls.append(tuple([j, tuple([i, k])]))
                else:
                    if tuple([j, tuple([k, i])]) in c:
                        ls.append(tuple([j, tuple([k, i])]))
            rs = []
            if G2.nodes[i]["atom"] == G1.nodes[j[0]]["atom"]:
                rs.append(tuple([j[0], i]))
            if G2.nodes[i]["atom"] == G1.nodes[j[1]]["atom"]:
                rs.append(tuple([j[1], i]))
            ILP += pulp.lpSum([c[k] for k in ls]) <= pulp.lpSum([y[k] for k in rs])

    # LP relaxation
    #if threshold != -1 and not no_ilp_threshold:

        #lp_status, lp_value = solve_lp_relaxation(ILP, solver_options=solver_options)


        #print("LP relaxation status:", LpStatus.get(lp_status, lp_status))
        #print("LP relaxation value:", lp_value)

        #if lp_status == pulp.LpStatusOptimal and lp_value is not None and lp_value > threshold:
            #print("LP relaxation exceeds threshold — skipping MIP solve")
            #return threshold, 2

    # Constraint for the threshold, added only after LP relaxation pruning.
    if threshold != -1 and not no_ilp_threshold:
        ILP += objective_expr <= threshold

    # Warm start after all variables and constraints are created.

    apply_warm_start(y, c, G1, G2)

    ILP.writeMPS("debug_mces.mps")
    ILP.writeLP("debug_mces.lp")

    # Solve the ILP
    if solver == "default":
        sol = pulp.getSolver(solver="PULP_CBC_CMD", **solver_options)
    elif solver == "HiGHS_CMD":
        sol = pulp.HiGHS(
            msg=True,
            timeLimit=60,
            threads=24
        )
    elif solver == "CPLEX_PY":
        sol = pulp.CPLEX_PY(
            msg=True,
            timeLimit=60,
            threads=1
        )
    else:
        sol = pulp.getSolver(solver, **solver_options)


    solve_status = ILP.solve(sol)


    status_code = ILP.status
    status_name = LpStatus[ILP.status]
    objective_value = ILP.objective.value()

    print("solve() returned:", solve_status)
    print("ILP.status:", status_code)
    print("Status name:", status_name)
    print("Objective value:", objective_value)

    if ILP.status == pulp.LpStatusOptimal:
        return (
            float(objective_value),
            1,
            actual_threshold,
            lb_structural,
            skipped_by_structural_lb
        )
    else:
        return (
            threshold,
            2,
            actual_threshold,
            lb_structural,
            skipped_by_structural_lb
        )
