import numpy as np
import random
from ugd.model.digraph import RstDiGraph

import inspect


' not directed specific'

def one_function(adj_m, var_dict):
    return 1

def crossarrow_count(adj_m, var_dict, test_border):
    key, from_value, to_value = test_border
    count = 0;
    n = adj_m.shape[0]
    for i in range(n):
        for j in range(n):
            if adj_m[i,j]==1 and var_dict[i][key]== from_value and var_dict[j][key]==to_value:
                count += 1
    return count

def rand_choise(q):
    ''' returns true with probability q '''
    event = np.random.binomial(1, q)
    return event == 1

def rand_element_of_set(set):
    return random.sample(set, 1)[0]


''' path specific algoritms'''

# fixme maybe node specific
def get_path(startnode, active_start, graph, pathnumber):
    path = []
    working_node = startnode
    path_continue = True
    is_aktive = active_start
    # fixme check this

    while path_continue:
        path.append(working_node)
        path_continue, working_node = get_next_node(graph, working_node, is_aktive, pathnumber)
        is_aktive = not(is_aktive)

    del_nodes_mark(graph)
    return path


def get_next_node(graph, working_node,is_aktive, pathnumber):
    if is_aktive:
        out_dict = graph.nodes[working_node].active_marked
        for key, value in out_dict.items():
            if value == pathnumber:
                if graph.nodes[working_node].active_visited:
                    return False, key
                else:
                    graph.nodes[working_node].active_visited = True
                    return True, key

    else:
        out_dict = graph.nodes[working_node].passive_marked
        for key, value in out_dict.items():
            if value == pathnumber:
                if graph.nodes[working_node].passive_visited:
                    return False, key
                else:
                    graph.nodes[working_node].passive_visited = True
                    return True, key
    return False, None



def del_nodes_mark(graph, startnode=None):
    for node in range(graph.node_number):
        del_node_mark(graph, node)

def del_node_mark(graph, node):
    graph.nodes[node].active_visited = False
    graph.nodes[node].passive_visited = False



def form_to_set_index(graph, edge):
    for ind, set in enumerate(graph.restriction_set_list):
        if edge[0] in set:
            from_ind = ind
        if edge[1] in set:
            to_ind = ind
    return from_ind, to_ind


def all_edges(graph):
    edges = []
    for from_node in range(graph.node_number):
        for to_node in graph.nodes[from_node].outnodes:
            edges.append((from_node,to_node))
    return list(set(edges))

'''Debuging'''

def isdebugging():
  for frame in inspect.stack():
    if frame[1].endswith("pydevd.py"):
      return True
  return False