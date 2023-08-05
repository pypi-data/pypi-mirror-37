import numpy as np
import pytest

from ugd.high_level_interface.draw_simulations import gen_draws, digraph_hyp_test
from test.test_resources.graphs_two_restriction_sets import graph1_adj_m, graph2_adj_m, var_dict2

var_dict1 = {
    0: {'gender': 'm', 'age': 50},
    1: {'gender': 'm', 'age': 50},
    2: {'gender': 'f', 'age': 51},
    3: {'gender': 'f', 'age': 51},
}


def test_graph_no_rstrc():
    graphs, stats_list = digraph_hyp_test(adj_m=graph1_adj_m, var_dict=var_dict1, test_variable=('gender', 'm', 'f'),
                                          anz_sim=1000, show_polt=True)
    mue = np.mean(stats_list)
    assert mue > 0.45 and mue < 5.5


def teste_graph_with_rstrc():
    with pytest.raises(ValueError):
        graphs, stats_list = digraph_hyp_test(adj_m=graph1_adj_m, var_dict=var_dict1, test_variable=('gender', 'm', 'f'),
                                              anz_sim=1000, controlls=['age'])

# machen

def test_graph2_with_rstrc():
    graphs, stats_list = digraph_hyp_test(adj_m=graph2_adj_m, var_dict=var_dict2, test_variable=('gender', 'm', 'f'),
                                          anz_sim=1000)
    mue = np.mean(stats_list)
    assert mue > 0.33333-0.05 and mue < 0.33333+0.05

def test_graph2_no_rstrc():
     graphs, stats_list = digraph_hyp_test(adj_m=graph2_adj_m, var_dict=var_dict2, test_variable=('gender', 'm', 'f'),
                                              anz_sim=1000, controlls=['age'])
     mue = np.mean(stats_list)
     assert mue > 0.45 and mue < 5.5



