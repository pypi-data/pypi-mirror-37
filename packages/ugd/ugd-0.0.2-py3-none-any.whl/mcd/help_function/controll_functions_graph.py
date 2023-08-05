'''
conrol functions:
Performing checks on the Graph, to see whether implicit restrictions (dopple arrow, degree  ect).
'''



import numpy as np

from ugd.help_function.util import all_edges, form_to_set_index

# fixme rewrite for plain graph
def graph_correct(graph):
    restriction(graph)
    graph_nodes_correct(graph)
    return True

def full_graph_correct(graph):
    restriction(graph)
    graph_nodes_correct(graph)
    graph_is_full(graph)
    matrix_consistent(graph)
    return True

def graph_nodes_correct(graph):
    node_id_in_place(graph)
    for node in graph.nodes:
        node_correct(node, graph.node_number)
    return True


def restriction(rstrGraph):
    set_list = rstrGraph.restriction_set_list
    total_Set = set()
    total = 0
    for sub_set in set_list:
        total_Set= total_Set.union(sub_set)
        total += sub_set.__len__()
    if not(total==total_Set.__len__()):
        raise ValueError ('restriction sets are not disjoint')
    if not(total_Set == set(range(rstrGraph.degree_serie.__len__()))):
        raise ValueError ('nodes in set are not the intergers {0,..n-1}')

def graph_is_full(graph):
    for i, node in enumerate(graph.nodes):
        if not (graph.degree_serie[i] == node.degree) :
            raise ValueError('indegree property not fulfielled')
        if not (graph.degree_serie[i] == node.outnodes.__len__())  :
            raise ValueError('indegree property not fulfielled')

def matrix_consistent(rstGraph):
    n = rstGraph.restriction_set_list.__len__()
    controll_matrix = np.zeros((n,n))
    for edge in all_edges(rstGraph):
        from_ind, to_ind = form_to_set_index(rstGraph, edge)

        controll_matrix[from_ind,to_ind] +=1
        controll_matrix[to_ind, from_ind] += 1
    if not(controll_matrix == rstGraph.crossing_matrix).all():
        raise ValueError('Graph has the setrestricions violated')


'''Node'''
def node_id_in_place(graph):
    for i, node in enumerate(graph.nodes):
        if not(i==node.id):
            raise ValueError ('id and node position does not match')

def node_correct(node,n):
    if not(node.degree == node.outnodes.__len__()):
        raise ValueError(' degree violated !!')
    if not(node.degree == n- node.passive_outnodes.__len__()-node.passive_outnodes_removed_selfloop_crossarrow):
        raise ValueError(' degree violated !!')

    for outnode in node.outnodes:
        if outnode == node.id:
            raise ValueError (' self loop')
        if outnode in node.passive_outnodes:
            raise ValueError('active outnode is in possible passive outnodes')
