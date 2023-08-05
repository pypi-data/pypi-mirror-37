import copy

import pytest
from ugd.schlaufen_construction.di_schlaufen_construction_util import feasable_outnodes
from test.test_resources.graphs_two_restriction_sets import graph1



testdata = [
    (graph1, 0, False, set([3]) ),
    (graph1, 1, True, set([0]) ),
    (graph1, 0, True, set([]) ),

]


@pytest.mark.parametrize("graph, node, is_aktive, outnodes", testdata)
def test_feasable_outnodes(graph, node, is_aktive, outnodes):
    graph_copy = copy.deepcopy(graph)
    outnodes_computed = feasable_outnodes(graph_copy,node,is_aktive)
    assert outnodes_computed == outnodes
