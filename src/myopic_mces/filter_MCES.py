# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 17:59:05 2020

@author: seipp
"""

import networkx as nx
from collections import Counter





# ============================================================
# Bond inventory filter
# ============================================================

def bond_signature(G, u, v):
    """
    Return the labeled signature of one bond.

    The endpoint atom labels are sorted so that:
        C-O
    and:
        O-C

    are treated as the same bond type.
    """
    atom_u = G.nodes[u]["atom"]
    atom_v = G.nodes[v]["atom"]

    atom1, atom2 = sorted((atom_u, atom_v))

    bond_weight = G[u][v]["weight"]

    return atom1, atom2, bond_weight


def filter3_bond_inventory(G1, G2):
    """
    Safe lower bound based on labeled bond inventories.

    The filter compares how many bonds of every type occur
    in the two molecules.

    A bond type contains:
    - first endpoint atom type
    - second endpoint atom type
    - bond weight

    Connectivity between different bonds is ignored, making
    this a relaxation of the exact MCES problem.
    """

    bonds1 = Counter(
        bond_signature(G1, u, v)
        for u, v in G1.edges()
    )

    bonds2 = Counter(
        bond_signature(G2, u, v)
        for u, v in G2.edges()
    )

    difference = 0.0

    all_signatures = bonds1.keys() | bonds2.keys()

    for signature in all_signatures:
        bond_weight = signature[2]
        count_difference = abs(bonds1[signature] - bonds2[signature])
        difference += bond_weight * count_difference

    # The distance definition counts the difference between
    # the two total bond inventories and divides it by two.
    return difference / 2.0





# ============================================================
# Original filter 1
# ============================================================

def filter1(G1, G2):
    """
    Find a lower bound for the distance based on weighted degree.

    Parameters
    ----------
    G1 : networkx.Graph
        Graph representing the first molecule.

    G2 : networkx.Graph
        Graph representing the second molecule.

    Returns
    -------
    float
        Lower bound for the distance between the molecules.
    """

    atom_types1 = []

    for node in G1.nodes:
        atom_type = G1.nodes[node]["atom"]

        if atom_type not in atom_types1:
            atom_types1.append(atom_type)

    type_map1 = {}

    for atom_type in atom_types1:
        type_map1[atom_type] = [
            node
            for node in G1.nodes
            if G1.nodes[node]["atom"] == atom_type]

    atom_types2 = []

    for node in G2.nodes:
        atom_type = G2.nodes[node]["atom"]
        if atom_type not in atom_types2:
            atom_types2.append(atom_type)

    type_map2 = {}

    for atom_type in atom_types2:
        type_map2[atom_type] = [
            node
            for node in G2.nodes
            if G2.nodes[node]["atom"] == atom_type
        ]

    difference = 0.0

    for atom_type in atom_types1:

        if atom_type in atom_types2:

            number_mapped = min( len(type_map1[atom_type]), len(type_map2[atom_type]))

            degree_list1 = sorted(
                type_map1[atom_type],
                key=lambda node: sum(
                    G1[node][neighbour]["weight"]
                    for neighbour in G1.neighbors(node)
                ),
                reverse=True
            )

            degree_list2 = sorted(
                type_map2[atom_type],
                key=lambda node: sum(
                    G2[node][neighbour]["weight"]
                    for neighbour in G2.neighbors(node)
                ),
                reverse=True
            )

            for index in range(number_mapped):

                degree1 = sum(
                    G1[degree_list1[index]][neighbour]["weight"]
                    for neighbour
                    in G1.neighbors(degree_list1[index])
                )

                degree2 = sum(
                    G2[degree_list2[index]][neighbour]["weight"]
                    for neighbour
                    in G2.neighbors(degree_list2[index])
                )

                difference += abs(degree1 - degree2)

            if len(degree_list1) > number_mapped:

                for index in range(
                    number_mapped,
                    len(degree_list1)
                ):

                    difference += sum(
                        G1[degree_list1[index]][neighbour]["weight"]
                        for neighbour
                        in G1.neighbors(degree_list1[index])
                    )

            if len(degree_list2) > number_mapped:

                for index in range(number_mapped, len(degree_list2)):
                    difference += sum(
                        G2[degree_list2[index]][neighbour]["weight"]
                        for neighbour
                        in G2.neighbors(degree_list2[index]))

        else:

            for node in type_map1[atom_type]:

                difference += sum( G1[node][neighbour]["weight"]
                    for neighbour in G1.neighbors(node) )

    for atom_type in atom_types2:

        if atom_type not in atom_types1:

            for node in type_map2[atom_type]:

                difference += sum(G2[node][neighbour]["weight"]
                    for neighbour in G2.neighbors(node)
                )

    return difference / 2.0


# ============================================================
# Original neighborhood-matching cost
# ============================================================

def get_cost(G1, G2, i, j):
    """
    Calculate the cost of mapping node i from G1 to node j from G2
    based on their immediate neighborhoods.
    """

    atom_types1 = []

    for neighbour in G1.neighbors(i):
        atom_type = G1.nodes[neighbour]["atom"]

        if atom_type not in atom_types1:
            atom_types1.append(atom_type)

    type_map1 = {}

    for atom_type in atom_types1:
        type_map1[atom_type] = [
            neighbour
            for neighbour in G1.neighbors(i)
            if G1.nodes[neighbour]["atom"] == atom_type
        ]

    atom_types2 = []

    for neighbour in G2.neighbors(j):
        atom_type = G2.nodes[neighbour]["atom"]

        if atom_type not in atom_types2:
            atom_types2.append(atom_type)

    type_map2 = {}

    for atom_type in atom_types2:
        type_map2[atom_type] = [
            neighbour
            for neighbour in G2.neighbors(j)
            if G2.nodes[neighbour]["atom"] == atom_type
        ]

    difference = 0.0

    for atom_type in atom_types1:

        if atom_type in atom_types2:

            number_mapped = min(
                len(type_map1[atom_type]),
                len(type_map2[atom_type])
            )

            edge_list1 = sorted(
                type_map1[atom_type],
                key=lambda neighbour: G1[i][neighbour]["weight"],
                reverse=True
            )

            edge_list2 = sorted(
                type_map2[atom_type],
                key=lambda neighbour: G2[j][neighbour]["weight"],
                reverse=True
            )

            for index in range(number_mapped):

                weight1 = G1[i][edge_list1[index]]["weight"]
                weight2 = G2[j][edge_list2[index]]["weight"]

                difference += abs(weight1 - weight2) / 2.0

            if len(edge_list1) > number_mapped:

                for index in range(
                    number_mapped,
                    len(edge_list1)
                ):

                    difference += (
                        G1[i][edge_list1[index]]["weight"] / 2.0
                    )

            if len(edge_list2) > number_mapped:

                for index in range(
                    number_mapped,
                    len(edge_list2)
                ):

                    difference += (
                        G2[j][edge_list2[index]]["weight"] / 2.0
                    )

        else:

            for neighbour in type_map1[atom_type]:
                difference += G1[i][neighbour]["weight"] / 2.0

    for atom_type in atom_types2:
        if atom_type not in atom_types1:
            for neighbour in type_map2[atom_type]:
                difference += G2[j][neighbour]["weight"] / 2.0

    return difference


# ============================================================
# Greedy RASCAL-style clique search
# ============================================================
def incident_signature(G, node):
    """
    Return the multiset of labeled bonds incident to one atom.

    Each incident bond is represented by:
    - neighbouring atom type
    - bond weight

    The central atom type does not need to be included because
    atoms are already matched only within the same atom type.
    """

    incident_bonds = []

    for neighbour in G.neighbors(node):
        neighbour_atom = G.nodes[neighbour]["atom"]
        bond_weight = G[node][neighbour]["weight"]

        incident_bonds.append(
            (neighbour_atom, bond_weight)
        )

    return Counter(incident_bonds)

def incident_signature_cost(signature1, signature2):
    """
    Calculate the relaxed cost between two incident-bond
    signatures.

    Each unmatched incident bond contributes half its weight
    because every molecular bond is observed from both of its
    endpoint atoms.
    """

    cost = 0.0

    all_codes = signature1.keys() | signature2.keys()

    for code in all_codes:
        bond_weight = code[1]

        difference = abs(
            signature1[code] - signature2[code]
        )

        cost += difference * bond_weight / 2.0

    return cost

def unmatched_node_cost(signature):
    """
    Cost of leaving one atom unmatched.

    All bonds incident to the atom are considered unmatched.
    Each contributes half its weight.
    """

    return sum(
        count * code[1] / 2.0
        for code, count in signature.items()
    )

def filter_rascal_second_tier(G1, G2):
    """
    RASCAL-inspired second-tier lower bound.

    Atoms are separated by atom type. For each atom type,
    a minimum-cost bipartite assignment is solved.

    Matching costs are based on the complete multiset of
    neighboring atom types and bond weights.

    Dummy nodes represent atoms that cannot be matched because
    one molecule has more atoms of a given type.
    """

    atom_types1 = { data["atom"]
        for _, data in G1.nodes(data=True)}

    atom_types2 = {data["atom"]
      for _, data in G2.nodes(data=True)
    }

    atom_types = atom_types1 | atom_types2

    signatures1 = {
        node: incident_signature(G1, node)
        for node in G1.nodes()
    }

    signatures2 = {
        node: incident_signature(G2, node)
        for node in G2.nodes()
    }

    total_bound = 0.0

    for atom_type in atom_types:

        nodes1 = [
            node
            for node in G1.nodes()
            if G1.nodes[node]["atom"] == atom_type
        ]

        nodes2 = [
            node
            for node in G2.nodes()
            if G2.nodes[node]["atom"] == atom_type
        ]

        # Nothing to process for this atom type.
        if not nodes1 and not nodes2:
            continue

        assignment_graph = nx.Graph()

        left_nodes = [
            ("g1", atom_type, node)
            for node in nodes1
        ]

        right_nodes = [
            ("g2", atom_type, node)
            for node in nodes2
        ]

        assignment_graph.add_nodes_from(
            left_nodes,
            bipartite=0
        )

        assignment_graph.add_nodes_from(
            right_nodes,
            bipartite=1
        )

        # ----------------------------------------------------
        # Add real atom-to-atom mapping possibilities.
        # ----------------------------------------------------

        for node1 in nodes1:
            left_node = ("g1", atom_type, node1)

            for node2 in nodes2:
                right_node = ("g2", atom_type, node2)
                cost = incident_signature_cost( signatures1[node1],signatures2[node2])
                assignment_graph.add_edge(
                    left_node,
                    right_node,
                    weight=cost
                )

        # ----------------------------------------------------
        # Add dummy atoms when G1 has fewer atoms.
        # ----------------------------------------------------

        if len(nodes1) < len(nodes2):
            number_of_dummies = len(nodes2) - len(nodes1)
            for dummy_id in range(number_of_dummies):
                dummy = ( "g1_dummy",  atom_type,  dummy_id)
                assignment_graph.add_node( dummy, bipartite=0)

                for node2 in nodes2:
                    right_node = (  "g2", atom_type,  node2)
                    deletion_cost = unmatched_node_cost(signatures2[node2])

                    assignment_graph.add_edge(  dummy, right_node, weight=deletion_cost)

        # ----------------------------------------------------
        # Add dummy atoms when G2 has fewer atoms.
        # ----------------------------------------------------

        elif len(nodes2) < len(nodes1):

            number_of_dummies = len(nodes1) - len(nodes2)
            for dummy_id in range(number_of_dummies):
                dummy = ( "g2_dummy", atom_type, dummy_id)
                assignment_graph.add_node(  dummy, bipartite=1)
                for node1 in nodes1:
                    left_node = ( "g1",  atom_type, node1)
                    deletion_cost = unmatched_node_cost( signatures1[node1])
                    assignment_graph.add_edge(left_node,  dummy, weight=deletion_cost)

        left_partition = {
            node
            for node, data
            in assignment_graph.nodes(data=True)
            if data.get("bipartite") == 0
        }

        right_partition = {
            node
            for node, data
            in assignment_graph.nodes(data=True)
            if data.get("bipartite") == 1
        }

        if not left_partition or not right_partition:
            continue

        matching = (
            nx.algorithms.bipartite.minimum_weight_full_matching(
                assignment_graph,
                top_nodes=left_partition,
                weight="weight"
            )
        )

        # The returned dictionary contains every match twice:
        #
        # left -> right
        # right -> left
        #
        # Therefore, only entries belonging to the left
        # partition are counted.
        for left_node in left_partition:

            matched_node = matching.get(left_node)

            if matched_node is None:
                continue

            total_bound += assignment_graph[ left_node  ][ matched_node]["weight"]

    # we don't  divide by two again here
    # incident_signature_cost() already assigns half of each
    # bond mismatch to each endpoint.
    return total_bound





# ============================================================
# Original filter 2
# ============================================================

def filter2(G1, G2):
    """
    Find a lower bound based on minimum-cost neighborhood matching.
    """

    atom_types1 = []

    for node in G1.nodes:

        atom_type = G1.nodes[node]["atom"]

        if atom_type not in atom_types1:
            atom_types1.append(atom_type)

    atom_types2 = []

    for node in G2.nodes:

        atom_type = G2.nodes[node]["atom"]

        if atom_type not in atom_types2:
            atom_types2.append(atom_type)

    # Create a copy instead of assigning atom_types = atom_types1,
    # which would modify atom_types1 when new elements are appended.
    atom_types = list(atom_types1)
    for atom_type in atom_types2:
        if atom_type not in atom_types:
            atom_types.append(atom_type)

    result = 0.0

    for atom_type in atom_types:

        nodes1 = [
            node
            for node in G1.nodes
            if G1.nodes[node]["atom"] == atom_type
        ]

        nodes2 = [
            node
            for node in G2.nodes
            if G2.nodes[node]["atom"] == atom_type
        ]

        if not nodes1 and not nodes2:
            continue

        matching_graph = nx.Graph()

        left_nodes = [  ("g1", atom_type, node)
            for node in nodes1 ]

        right_nodes = [  ("g2", atom_type, node)
            for node in nodes2
        ]

        matching_graph.add_nodes_from( left_nodes,  bipartite=0)
        matching_graph.add_nodes_from( right_nodes, bipartite=1)

        for node1 in nodes1:

            left_node = ( "g1", atom_type,node1)

            for node2 in nodes2:

                right_node = ( "g2", atom_type,node2)

                matching_graph.add_edge(
                    left_node,
                    right_node,
                    weight=get_cost( G1,  G2, node1,node2 )
                )

        if len(nodes1) < len(nodes2):

            number_of_dummies = len(nodes2) - len(nodes1)
            for dummy_id in range(number_of_dummies):
                dummy = ( "g1_dummy", atom_type, dummy_id)
                matching_graph.add_node(  dummy,    bipartite=0)
                for node2 in nodes2:
                    right_node = ("g2",  atom_type, node2)

                    deletion_cost = sum( G2[neighbour][node2]["weight"]
                        for neighbour in G2.neighbors(node2)) / 2.0

                    matching_graph.add_edge( dummy, right_node,  weight=deletion_cost)

        elif len(nodes2) < len(nodes1):

            number_of_dummies = len(nodes1) - len(nodes2)
            for dummy_id in range(number_of_dummies):
                dummy = (  "g2_dummy", atom_type, dummy_id)

                matching_graph.add_node(
                    dummy,
                    bipartite=1
                )

                for node1 in nodes1:

                    left_node = (
                        "g1",
                        atom_type,
                        node1
                    )

                    deletion_cost = sum(
                        G1[neighbour][node1]["weight"]
                        for neighbour in G1.neighbors(node1)
                    ) / 2.0

                    matching_graph.add_edge(
                        left_node,
                        dummy,
                        weight=deletion_cost
                    )

        left_partition = {
            node
            for node, data
            in matching_graph.nodes(data=True)
            if data.get("bipartite") == 0
        }

        right_partition = {
            node
            for node, data
            in matching_graph.nodes(data=True)
            if data.get("bipartite") == 1
        }

        if not left_partition or not right_partition:
            continue

        matching = (
            nx.algorithms.bipartite.minimum_weight_full_matching(
                matching_graph,
                top_nodes=left_partition,
                weight="weight"
            )
        )

        for left_node in left_partition:

            matched_node = matching.get(left_node)

            if matched_node is None:
                continue

            result += matching_graph[
                left_node
            ][
                matched_node
            ]["weight"]

    return result

def filter3_improved_bond_inventory(G1, G2):

    # -----------------------------------------
    # Existing bond inventory bound
    # -----------------------------------------

    d_bond = filter3_bond_inventory(
        G1,
        G2
    )

    # -----------------------------------------
    # Weighted-degree distribution bound
    # -----------------------------------------

    def degree_inventory(G):

        inventory = Counter()

        for node in G.nodes():

            atom = G.nodes[node]["atom"]

            weighted_degree = sum(
                G[node][neighbour]["weight"]
                for neighbour in G.neighbors(node)
            )

            inventory[
                (
                    atom,
                    weighted_degree
                )
            ] += 1

        return inventory

    inv1 = degree_inventory(G1)
    inv2 = degree_inventory(G2)

    degree_difference = 0.0

    all_signatures = (
        inv1.keys()
        |
        inv2.keys()
    )

    for signature in all_signatures:

        weighted_degree = signature[1]

        count_difference = abs(
            inv1[signature]
            -
            inv2[signature]
        )

        degree_difference += (
            weighted_degree
            *
            count_difference
        )

    d_degree_inventory = (
        degree_difference
        / 4.0
    )

    # Both are candidate lower bounds.
    # Take whichever is stronger.
    return max(
        d_bond,
        d_degree_inventory
    )

def filter4_two_hop_assignment(G1, G2):

    def signature(G, node):

        result = []

        for neighbour in G.neighbors(node):

            neighbour_atom = (
                G.nodes[neighbour]["atom"]
            )

            bond_weight = (
                G[node][neighbour]["weight"]
            )

            second_level = []

            for second in G.neighbors(neighbour):

                if second == node:
                    continue

                second_level.append(
                    (
                        G.nodes[second]["atom"],
                        G[neighbour][second]["weight"]
                    )
                )

            result.append(
                (
                    neighbour_atom,
                    bond_weight,
                    tuple(sorted(second_level))
                )
            )

        return tuple(sorted(result))


    sig1 = {
        node: signature(G1, node)
        for node in G1.nodes()
    }

    sig2 = {
        node: signature(G2, node)
        for node in G2.nodes()
    }


    def signature_cost(s1, s2):

        c1 = Counter(s1)
        c2 = Counter(s2)

        difference = 0.0

        for item in c1.keys() | c2.keys():

            weight = item[1]

            difference += (
                abs(
                    c1[item]
                    -
                    c2[item]
                )
                *
                weight
            )

        return difference / 4.0


    atom_types = {
        G1.nodes[n]["atom"]
        for n in G1.nodes()
    } | {
        G2.nodes[n]["atom"]
        for n in G2.nodes()
    }


    total = 0.0


    for atom_type in atom_types:

        nodes1 = [
            n for n in G1.nodes()
            if G1.nodes[n]["atom"] == atom_type
        ]

        nodes2 = [
            n for n in G2.nodes()
            if G2.nodes[n]["atom"] == atom_type
        ]


        if not nodes1 or not nodes2:
            continue


        B = nx.Graph()


        left = [
            ("g1", n)
            for n in nodes1
        ]

        right = [
            ("g2", n)
            for n in nodes2
        ]


        B.add_nodes_from(
            left,
            bipartite=0
        )

        B.add_nodes_from(
            right,
            bipartite=1
        )


        for n1 in nodes1:

            for n2 in nodes2:

                cost = signature_cost(
                    sig1[n1],
                    sig2[n2]
                )

                B.add_edge(
                    ("g1", n1),
                    ("g2", n2),
                    weight=cost
                )


        matching = (
            nx.algorithms.matching
            .min_weight_matching(
                B,
                weight="weight"
            )
        )


        for a, b in matching:

            total += B[a][b]["weight"]


    return total


# ============================================================
# Filter cascade
# ============================================================

def apply_filter(
    G1,
    G2,
    threshold,
    always_stronger_bound=True
):

    # 1. Cheap weighted-degree bound
    d1 = filter1(G1, G2)

    if d1 > threshold:
        return (
            d1,
            None,
            None,
            None,
            0.0,
            d1,
            2
        )

    # 2. Cheap bond inventory
    #d_bond = filter3_bond_inventory(
    #    G1,
    #    G2
    #)

    current_bound = max(
        d1,
        0
    )

    if current_bound > threshold:
        return (
            d1,
            0,
            None,
            None,
            0.0,
            current_bound,
            2
        )

    # 3. More expensive neighborhood assignment
    d2 = filter2(
        G1,
        G2
    )

    current_bound = max(
        current_bound,
        d2
    )

    if current_bound > threshold:
        return (
            d1,
            0,
            None,
            d2,
            0.0,
            current_bound,
            2
        )

    # 4. Most expensive structural filter
    d_path = filter4_two_hop_assignment(
        G1,
        G2
    )

    current_bound = max(
        current_bound,
        d_path
    )

    if current_bound > threshold:
        return (
            d1,
            0,
            d_path,
            d2,
            0.0,
            current_bound,
            2
        )


    return (
        d1,
        0,
        d_path,
        d2,
        0,
        current_bound,
        1
    )