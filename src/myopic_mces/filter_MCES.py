# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 17:59:05 2020

@author: seipp
"""

import networkx as nx
from collections import Counter

def bond_signature(G, u, v):
    atom_u = G.nodes[u]["atom"]
    atom_v = G.nodes[v]["atom"]

    # sort atom types so C-O and O-C are treated the same
    a1, a2 = sorted([atom_u, atom_v])

    weight = G[u][v]["weight"]

    return (a1, a2, weight)


def filter3_bond_inventory(G1, G2):
    bonds1 = Counter()
    bonds2 = Counter()

    for u, v in G1.edges():
        bonds1[bond_signature(G1, u, v)] += 1

    for u, v in G2.edges():
        bonds2[bond_signature(G2, u, v)] += 1

    all_bond_types = set(bonds1.keys()) | set(bonds2.keys())

    difference = 0

    for bond_type in all_bond_types:
        difference += abs(bonds1[bond_type] - bonds2[bond_type])

    return difference

def filter1(G1,G2):
    """
     Finds a lower bound for the distance based on degree

     Parameters
     ----------
     G1 : networkx.classes.graph.Graph
         Graph representing the first molecule.
     G2 : networkx.classes.graph.Graph
         Graph representing the second molecule.

     Returns:
     -------
     float
         Lower bound for the distance between the molecules

    """
    #Find all occuring atom types and partition by type
    atom_types1=[]
    for i in G1.nodes:
        if G1.nodes[i]["atom"] not in atom_types1:
            atom_types1.append(G1.nodes[i]["atom"])
    type_map1={}
    for i in atom_types1:
        type_map1[i]=list(filter(lambda x: i==G1.nodes[x]["atom"],G1.nodes))

    atom_types2=[]
    for i in G2.nodes:
        if G2.nodes[i]["atom"] not in atom_types2:
            atom_types2.append(G2.nodes[i]["atom"])
    type_map2={}
    for i in atom_types2:
        type_map2[i]=list(filter(lambda x: i==G2.nodes[x]["atom"],G2.nodes))

    #calculate lower bound
    difference=0
    #Every atom type is done seperately
    for i in atom_types1:
        if i in atom_types2:
            #number of nodes that can be mapped
            n=min(len(type_map1[i]),len(type_map2[i]))
            #sort by degree
            degreelist1=sorted(type_map1[i],key=lambda x:sum([G1[x][j]["weight"] for j in G1.neighbors(x)]),reverse=True)
            degreelist2=sorted(type_map2[i],key=lambda x:sum([G2[x][j]["weight"] for j in G2.neighbors(x)]),reverse=True)
            #map in order of sorted lists
            for j in range(n):
                deg1=sum([G1[degreelist1[j]][k]["weight"] for k in G1.neighbors(degreelist1[j])])
                deg2=sum([G2[degreelist2[j]][k]["weight"] for k in G2.neighbors(degreelist2[j])])
                difference+= abs(deg1-deg2)
            #nodes that are not mapped
            if len(degreelist1)>n:
                for j in range(n,len(degreelist1)):
                    difference+=sum([G1[degreelist1[j]][k]["weight"] for k in G1.neighbors(degreelist1[j])])
            if len(degreelist2)>n:
                for j in range(n,len(degreelist2)):
                    difference+=sum([G2[degreelist2[j]][k]["weight"] for k in G2.neighbors(degreelist2[j])])
        #atom type only in one of the graphs
        else:
            for j in type_map1[i]:
                difference+=sum([G1[j][k]["weight"] for k in G1.neighbors(j)])
    for i in atom_types2:
        if i not in atom_types1:
            for j in type_map2[i]:
                difference+=sum([G2[j][k]["weight"] for k in G2.neighbors(j)])
    return difference/2



def get_cost(G1,G2,i,j):
    """
     Calculates the cost for mapping node i to j based on neighborhood

     Parameters
     ----------
     G1 : networkx.classes.graph.Graph
         Graph representing the first molecule.
     G2 : networkx.classes.graph.Graph
         Graph representing the second molecule.
     i : int
         Node of G1
     j : int
         Node of G2

     Returns:
     -------
     float
         Cost of mapping i to j

    """
    #Find all occuring atom types in neighborhood
    atom_types1=[]
    for k in G1.neighbors(i):
        if G1.nodes[k]["atom"] not in atom_types1:
            atom_types1.append(G1.nodes[k]["atom"])
    type_map1={}
    for k in atom_types1:
        type_map1[k]=list(filter(lambda x: k==G1.nodes[x]["atom"],G1.neighbors(i)))


    atom_types2=[]
    for k in G2.neighbors(j):
        if G2.nodes[k]["atom"] not in atom_types2:
            atom_types2.append(G2.nodes[k]["atom"])
    type_map2={}
    for k in atom_types2:
        type_map2[k]=list(filter(lambda x: k==G2.nodes[x]["atom"],G2.neighbors(j)))

    #calculate cost
    difference=0.
    #Every atom type is handled seperately
    for k in atom_types1:
        if k in atom_types2:
            n=min(len(type_map1[k]),len(type_map2[k]))
            #sort by incident edges by weight
            edgelist1=sorted(type_map1[k],key=lambda x:G1[i][x]["weight"],reverse=True)
            edgelist2=sorted(type_map2[k],key=lambda x:G2[j][x]["weight"],reverse=True)
            #map in order of sorted lists
            for l in range(n):
                difference+=(max(G1[i][edgelist1[l]]["weight"],G2[j][edgelist2[l]]["weight"])-min(G1[i][edgelist1[l]]["weight"],G2[j][edgelist2[l]]["weight"]))/2
            #cost for not mapped edges
            if len(edgelist1)>n:
                for l in range(n,len(edgelist1)):
                    difference+=G1[i][edgelist1[l]]["weight"]/2
            if len(edgelist2)>n:
                for l in range(n,len(edgelist2)):
                    difference+=G2[j][edgelist2[l]]["weight"]/2
        else:
            for l in type_map1[k]:
                difference+=G1[i][l]["weight"]/2
    for k in atom_types2:
        if k not in atom_types1:
            for l in type_map2[k]:
                difference+=G2[j][l]["weight"]/2

    return difference

import networkx as nx
from collections import defaultdict


def filter3_rascal_fast(G1, G2, tol=0.01, max_starts=5):
    """
    Faster RASCAL-style lower-bound filter.

    Main optimization:
    - Avoid building the full compatibility graph.
    - Check compatibility only when needed during greedy clique search.
    """

    # ------------------------------------------------------------
    # 1. Read atom labels once
    # ------------------------------------------------------------
    atom1 = nx.get_node_attributes(G1, "atom")
    atom2 = nx.get_node_attributes(G2, "atom")

    # ------------------------------------------------------------
    # 2. Group nodes by atom type
    #    Example:
    #    C -> [1, 3, 5]
    #    O -> [2, 4]
    # ------------------------------------------------------------
    groups1 = defaultdict(list)
    groups2 = defaultdict(list)

    for u, atom in atom1.items():
        groups1[atom].append(u)

    for v, atom in atom2.items():
        groups2[atom].append(v)

    # ------------------------------------------------------------
    # 3. Create possible atom mappings
    #    Only atoms with the same type can be matched.
    #
    #    Example:
    #    Carbon in G1 can match Carbon in G2.
    #    Carbon cannot match Oxygen.
    # ------------------------------------------------------------
    compat_nodes = []

    for atom in groups1.keys() & groups2.keys():
        for u in groups1[atom]:
            for v in groups2[atom]:
                compat_nodes.append((u, v))

    # ------------------------------------------------------------
    # 4. Compute total bond weight of both molecules
    # ------------------------------------------------------------
    total_edge_weight = (
        sum(data["weight"] for _, _, data in G1.edges(data=True))
        +
        sum(data["weight"] for _, _, data in G2.edges(data=True))
    )

    # ------------------------------------------------------------
    # 5. If no atoms can be matched, return maximum difference
    # ------------------------------------------------------------
    if not compat_nodes:
        return total_edge_weight / 2

    # ------------------------------------------------------------
    # 6. Compatibility test between two atom mappings
    #
    #    pair1 = (u1, v1)
    #    pair2 = (u2, v2)
    #
    #    They are compatible if:
    #    - they do not reuse the same atom
    #    - the bond relation is the same in both graphs
    #    - if both bonds exist, their weights are almost equal
    # ------------------------------------------------------------
    def compatible(pair1, pair2):
        u1, v1 = pair1
        u2, v2 = pair2

        # Same atom from G1 or G2 cannot be used twice
        if u1 == u2 or v1 == v2:
            return False

        # Check whether the corresponding atoms are connected
        e1 = G1.has_edge(u1, u2)
        e2 = G2.has_edge(v1, v2)

        # One graph has a bond but the other does not
        if e1 != e2:
            return False

        # If both have a bond, compare bond weights
        if e1:
            w1 = G1[u1][u2]["weight"]
            w2 = G2[v1][v2]["weight"]
            return abs(w1 - w2) < tol

        # If neither has a bond, they are compatible
        return True

    # ------------------------------------------------------------
    # 7. Score possible matches
    #    We prefer nodes with higher local structure.
    # ------------------------------------------------------------
    def node_score(pair):
        u, v = pair
        return min(G1.degree(u), G2.degree(v))

    # ------------------------------------------------------------
    # 8. Pick only a few good starting points
    #    This keeps the method fast.
    # ------------------------------------------------------------
    starts = sorted(
        compat_nodes,
        key=node_score,
        reverse=True
    )[:max_starts]

    best_clique = []

    # ------------------------------------------------------------
    # 9. Greedy clique search
    #
    #    A clique is a set of mutually compatible atom mappings.
    #    We build it one match at a time.
    # ------------------------------------------------------------
    for start in starts:
        clique = [start]

        # Track already used atoms to keep one-to-one mapping
        used_g1 = {start[0]}
        used_g2 = {start[1]}

        # Initial candidates cannot reuse atoms from the start pair
        candidates = [
            p for p in compat_nodes
            if p != start
            and p[0] not in used_g1
            and p[1] not in used_g2
        ]

        while candidates:
            # Keep only candidates compatible with every node
            # already inside the clique
            valid_candidates = [
                p for p in candidates
                if all(compatible(p, q) for q in clique)
            ]

            if not valid_candidates:
                break

            # Choose the structurally strongest next mapping
            next_node = max(valid_candidates, key=node_score)

            # Add selected mapping to clique
            clique.append(next_node)

            # Mark atoms as already used
            used_g1.add(next_node[0])
            used_g2.add(next_node[1])

            # Remove candidates that reuse atoms
            candidates = [
                p for p in valid_candidates
                if p != next_node
                and p[0] not in used_g1
                and p[1] not in used_g2
            ]

        # Save the largest clique found
        if len(clique) > len(best_clique):
            best_clique = clique

    # ------------------------------------------------------------
    # 10. Count common bond weight inside the clique
    #
    #     If two matched atoms are bonded in G1, then because of
    #     compatibility, the corresponding atoms are also bonded in G2
    #     with almost the same weight.
    # ------------------------------------------------------------
    common_edge_weight = 0.0

    for i in range(len(best_clique)):
        u1, _ = best_clique[i]

        for j in range(i + 1, len(best_clique)):
            u2, _ = best_clique[j]

            if G1.has_edge(u1, u2):
                common_edge_weight += G1[u1][u2]["weight"]

    # ------------------------------------------------------------
    # 11. RASCAL lower bound
    #
    #     total_edge_weight / 2:
    #         approximate total bond structure
    #
    #     common_edge_weight:
    #         shared bond structure
    #
    #     difference:
    #         non-shared structure
    # ------------------------------------------------------------
    lower_bound = total_edge_weight / 2 - common_edge_weight

    return max(0.0, lower_bound)


def filter2(G1,G2):
    """
     Finds a lower bound for the distance based on neighborhood

     Parameters
     ----------
     G1 : networkx.classes.graph.Graph
         Graph representing the first molecule.
     G2 : networkx.classes.graph.Graph
         Graph representing the second molecule.

     Returns:
     -------
     float
         Lower bound for the distance between the molecules

    """
    # Find all occuring atom types
    atom_types1=[]
    for i in G1.nodes:
        if G1.nodes[i]["atom"] not in atom_types1:
            atom_types1.append(G1.nodes[i]["atom"])

    atom_types2=[]
    for i in G2.nodes:
        if G2.nodes[i]["atom"] not in atom_types2:
            atom_types2.append(G2.nodes[i]["atom"])

    atom_types=atom_types1

    for i in atom_types2:
        if i not in atom_types:
            atom_types.append(i)
    #calculate distance
    res=0
    #handle every atom type seperately
    for i in atom_types:
        #filter by atom type
        nodes1=list(filter(lambda x: i==G1.nodes[x]["atom"],G1.nodes))
        nodes2=list(filter(lambda x: i==G2.nodes[x]["atom"],G2.nodes))
        #Create new graph for and solve minimum weight full matching
        G=nx.Graph()
        #Add node for every node of type i in G1 and G2
        for j in nodes1:
            G.add_node(tuple([1,j]))
        for j in nodes2:
            G.add_node(tuple([2,j]))
        #Add edges between all nodes of G1 and G2
        for j in nodes1:
            for k in nodes2:
                if G1.nodes[j]["atom"]==G2.nodes[k]["atom"]:
                    G.add_edge(tuple([1,j]),tuple([2,k]),weight=get_cost(G1,G2,j,k))
        #Add nodes if one graph has more nodes of type i than the other
        if len(nodes1)<len(nodes2):
            diff=len(nodes2)-len(nodes1)
            for j in range(1,diff+1):
                G.add_node(tuple([1,-j]))
                for k in nodes2:
                    G.add_edge(tuple([1,-j]),tuple([2,k]),weight=sum([G2[l][k]["weight"] for l in G2.neighbors(k)])/2)
        if len(nodes2)<len(nodes1):
            diff=len(nodes1)-len(nodes2)
            for j in range(1,diff+1):
                G.add_node(tuple([2,-j]))
                for k in nodes1:
                    G.add_edge(tuple([1,k]),tuple([2,-j]),weight=sum([G1[l][k]["weight"] for l in G1.neighbors(k)])/2)
        #Solve minimum weight full matching
        h=nx.bipartite.minimum_weight_full_matching(G)
        #Add weight of the matching
        for k in h:
            if k[0]==1:
                res=res+G[k][h[k]]["weight"]

    return res

def apply_filter(G1, G2, threshold, always_stronger_bound=True):
    """
    Apply filters from cheap to expensive.

    filter1:
        Fastest, weakest lower bound.

    filter2:
        Stronger, but slower.

    filter3_rascal_fast:
        Most expensive, so we only run it when filter2
        still does not pass the threshold.
    """

    # ------------------------------------------------------------
    # 1. First try the cheap degree-based filter
    # ------------------------------------------------------------
    d = filter1(G1, G2)

    if d > threshold:
        return d, 2

    # ------------------------------------------------------------
    # 2. Then try the stronger neighborhood-based filter
    # ------------------------------------------------------------
    d2 = filter2(G1, G2)
    d = max(d, d2)

    if d > threshold:
        return d, 2


    # ------------------------------------------------------------
    # 3. Run RASCAL as the strongest filter
    # ------------------------------------------------------------
    #d3 = filter3_rascal_fast(G1, G2)
    #print("RASCAL")
    #d = max(d, d3)

    d3 = filter3_bond_inventory(G1, G2)
    d = max(d, d3)

    if d > threshold:
        return d, 2

    return d, 1

    return d, 2
