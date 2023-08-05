'''
This file implements the ... algoritm in ....

'''

from ugd.schlaufen_construction.di_schlaufen_construction_util import  mark_edge, mark_node, cycle_found, random_draw
from ugd.help_function.util import rand_element_of_set, del_nodes_mark

def add_di_random_schleife(graph, schleifen_number):

    # random draw of initial node
    found_feasable_startnode = False
    while not(found_feasable_startnode): # draw startnode with already a aktive outedge (smallers overhead)
	    # fixme: consider the case of no feasable startnode(eg. in empty graph)
        startnode = rand_element_of_set(range(graph.node_number))
        if not(graph.nodes[startnode].outnodes == set([])):
            found_feasable_startnode = True

    cyclenode = None
    active_cyclenode = None
    working_node = startnode

    is_active = True
    is_schlaufe = False
    while not(is_schlaufe):
         mark_node(graph,working_node, is_active)
         found, out_node = random_draw(graph,working_node, is_active)
         if found:
             mark_edge(graph, working_node, out_node, is_active, schleifen_number)
             working_node = out_node
             if cycle_found(graph, out_node, is_active):
                 active_cyclenode = not (is_active)  # outnode is one step ahead
                 cyclenode = out_node
                 is_schlaufe = True
             else:
                 is_active = not(is_active)
         else:
             is_schlaufe = True

    del_nodes_mark(graph, startnode) # but not edge markations
    return startnode, cyclenode, active_cyclenode



