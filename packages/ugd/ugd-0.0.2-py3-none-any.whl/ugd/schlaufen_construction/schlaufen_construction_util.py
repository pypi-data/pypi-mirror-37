from ugd.help_function.util import rand_element_of_set

''' Random draw functions:'''


def random_draw(graph, working_node, is_active):
    ''' draw out of feasable outnodset'''
    outnodeset = feasable_outnodes(graph, working_node, is_active)
    if len(outnodeset) is 0:
        return False, None
    else:
        return True, rand_element_of_set(outnodeset)


def feasable_outnodes(graph, wokingnode, is_active):
    '''construction of feasible outnodeset '''
    outnode_set = set([])
    if is_active:
        for outnode in graph.nodes[wokingnode].outnodes:
            if is_feasable_outnode(graph, wokingnode, outnode, is_active):
                outnode_set.add(outnode)
    else:
        for outnode in graph.nodes[wokingnode].passive_outnodes:
            if is_feasable_outnode(graph, wokingnode, outnode, is_active):
                outnode_set.add(outnode)
    return outnode_set



# CCC
def is_feasable_outnode(graph, wokingnode, outnode, is_active):
    wokingnode_p = graph.nodes[wokingnode]
    outnode_p = graph.nodes[outnode]
    if is_active:
        if outnode in wokingnode_p.outnodes and not(outnode in wokingnode_p.active_marked)\
                and not(wokingnode in outnode_p.active_marked):
            return True
        else:
            return False
    else:
        if outnode in wokingnode_p.passive_outnodes and not(outnode in wokingnode_p.passive_marked)\
                and not(wokingnode in outnode_p.passive_marked) and not(graph.nodes[outnode].outnodes == set([])):
            return True
        else:
            return False


''' mark functions:'''

def mark_node(graph, working_node, is_active):
    if is_active:
        graph.nodes[working_node].active_visited = True
    else:
        graph.nodes[working_node].passive_visited = True


def mark_edge(graph,working_node, out_node, is_active, schleifennumber):
    if is_active:
        graph.nodes[working_node].active_marked[out_node] = schleifennumber
    else:
        graph.nodes[working_node].passive_marked[out_node] = schleifennumber




''' Control functions'''
def cycle_found(graph, out_node, is_active):
    if not(is_active): # consider that this is the new node, wich is found in an is_active sep but left in not(is_active)
        if graph.nodes[out_node].active_visited == True:
            return True
        else:
            return False
    else:
        if graph.nodes[out_node].passive_visited == True:
            return True
        else:
            return False
