'''
implements Algoritmus ... in paper:



'''
import numpy as np

'''costum functions'''
from ugd.help_function.util import rand_choise
from ugd.schlaufen_construction.schlaufen import add_random_schleife
from ugd.markov_walk.markov_walk_util import swich_cycles,  del_makations,update_violation_matrix
from ugd.markov_walk.constraint_violation_check import no_violations



def markov_walk(graph, mixing_time):
    '''
    :param graph: RstDiGraph or RstGraph class
    :param mixing_time: integer
    :return: randomly modified  RstDiGraph or RstGraph class, if mixing time is sufficiency big it is a uniform sample
    '''
    for i in range(mixing_time):
        graph = do_random_step(graph)
    return graph


def do_random_step(graph):
    q =0.05
    if rand_choise(q): # selfloop
        return graph
    else:
        graph, is_violated, start_nodes, cycle_start_nodes, active_startnodes = create_schlaufen_sequence(graph)
        if is_violated == 0: # feasable scoulafen sequence found
            swich_cycles(graph, cycle_start_nodes, active_startnodes)
            del_makations(graph, start_nodes)
            return graph
        else: # selfloop
            del_makations(graph, start_nodes)
            return graph


def create_schlaufen_sequence(graph):
    ''' creates iterativly a schlaufenseire according to step 3 in Algoritm'''
    violation_matrix = np.zeros((graph.restriction_set_list.__len__(),graph.restriction_set_list.__len__()))
    ad_schlaufen = True
    start_nodes = []
    cycle_start_nodes = []
    active_cyclenodes = []

    ind = 0
    while ad_schlaufen:
        start_node, cycle_start_node, active_cyclenode =  add_random_schleife(graph, ind)
        start_nodes.append(start_node)
        cycle_start_nodes.append(cycle_start_node)
        active_cyclenodes.append(active_cyclenode)
        violation_matrix = update_violation_matrix(graph, cycle_start_node, active_cyclenode, ind, violation_matrix)
        if no_violations(violation_matrix):
            is_violated = False
            return graph, is_violated, start_nodes, cycle_start_nodes, active_cyclenodes
        else:
            if rand_choise(0.5):
                is_violated = True
                return graph, is_violated, start_nodes, cycle_start_nodes, active_cyclenodes
        ind += 1

