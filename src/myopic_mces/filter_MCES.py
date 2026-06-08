# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 17:59:05 2020

@author: seipp
"""

import networkx as nx

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

def filter3_rascal(G1, G2):
    # Step 1: compatibility nodes
    compat_nodes = []
    for u in G1.nodes:
        for v in G2.nodes:
            if G1.nodes[u]["atom"] == G2.nodes[v]["atom"]:
                compat_nodes.append((u, v))

    if not compat_nodes:
        total = (sum(G1[u][v]["weight"] for u, v in G1.edges)
                 + sum(G2[u][v]["weight"] for u, v in G2.edges))
        return total / 2

    # Step 2: compatibility edges (edge-presence must agree AND weights match)
    compat_adj = {node: set() for node in compat_nodes}
    for idx1 in range(len(compat_nodes)):
        u1, v1 = compat_nodes[idx1]
        for idx2 in range(idx1 + 1, len(compat_nodes)):
            u2, v2 = compat_nodes[idx2]
            if u1 == u2 or v1 == v2:
                continue
            e1 = G1.has_edge(u1, u2)
            e2 = G2.has_edge(v1, v2)
            if e1 and e2:
                if abs(G1[u1][u2]["weight"] - G2[v1][v2]["weight"]) < 0.01:
                    compat_adj[(u1, v1)].add((u2, v2))
                    compat_adj[(u2, v2)].add((u1, v1))
            elif not e1 and not e2:
                compat_adj[(u1, v1)].add((u2, v2))
                compat_adj[(u2, v2)].add((u1, v1))

    # Step 3: greedy clique — return the actual clique, not just size
    def greedy_clique(adj, nodes):
        if not nodes:
            return []
        best_clique = []
        start_candidates = sorted(nodes, key=lambda x: len(adj[x]), reverse=True)
        start_candidates = start_candidates[:min(5, len(start_candidates))]
        for start in start_candidates:
            clique = [start]
            candidates = adj[start].copy()
            while candidates:
                next_node = max(candidates, key=lambda x: len(adj[x] & candidates))
                clique.append(next_node)
                candidates = candidates & adj[next_node]
            if len(clique) > len(best_clique):
                best_clique = clique
        return best_clique

    best_clique = greedy_clique(compat_adj, set(compat_nodes))

    # Step 4: count ACTUAL shared edge weight induced by the clique in G1
    common_edge_weight = 0.0
    for idx1 in range(len(best_clique)):
        u1, _ = best_clique[idx1]
        for idx2 in range(idx1 + 1, len(best_clique)):
            u2, _ = best_clique[idx2]
            if G1.has_edge(u1, u2):
                common_edge_weight += G1[u1][u2]["weight"]

    total_edge_weight = (sum(G1[u][v]["weight"] for u, v in G1.edges)
                         + sum(G2[u][v]["weight"] for u, v in G2.edges))

    return max(0.0, total_edge_weight / 2 - common_edge_weight)


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

def apply_filter(G1,G2,threshold,always_stronger_bound=True):
    """
     Finds a lower bound for the distance

     Parameters
     ----------
     G1 : networkx.classes.graph.Graph
         Graph representing the first molecule.
     G2 : networkx.classes.graph.Graph
         Graph representing the second molecule.
     threshold : int
         Threshold for the comparison. We want to find a lower bound that is higher than the threshold
     always_stronger_bound : bool
         if true, always compute and use the second stronger bound



     Returns:
     -------
     float
         Lower bound for the distance between the molecules
     int
         Which lower bound was chosen: 2 - depending on threshold, 4 - second lower bound

    """
    if always_stronger_bound:
        # Original behaviour: filter2 is always used (status 4)
        d = filter2(G1, G2)
        # NEW: if filter2 still doesn't exceed threshold, try RASCAL
        if d <= threshold:
            d_rascal = filter3_rascal(G1, G2)
            d = max(d, d_rascal)  # take the tighter (higher) bound
        return d, 4

    else:
        # Dynamic path: cheapest filter first
        d = filter1(G1, G2)
        if d > threshold:
            return d, 2

        d = filter2(G1, G2)
        if d > threshold:
            return d, 2

        # NEW: RASCAL bound as last resort before ILP
        d_rascal = filter3_rascal(G1, G2)
        d = max(d, d_rascal)
        if d > threshold:
            return d, 2

        return d, 2
