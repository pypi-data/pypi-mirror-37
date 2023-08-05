import numpy as np

from mcd import graph_hyp_test





adj_m = np.zeros((4, 4))
adj_m[0, 1] = 1
adj_m[1, 0] = 1
adj_m[3, 2] = 1
adj_m[2, 3] = 1
var_dict = {
    0: {'gender': 'm'},
    1: {'gender': 'm'},
    2: {'gender': 'f'},
    3: {'gender': 'f'},
}

def test_graph_no_rstrc():
    graphs, stats_list = graph_hyp_test(adj_m=adj_m, var_dict=var_dict, test_variable=('gender', 'm', 'f'), mixing_time=10000, anz_sim=100, show_polt=False)
    mue = np.mean(stats_list)
    true_mean = 0*1/3+ 2/3 * 2
    assert mue > true_mean - 0.15 and mue < true_mean + 0.15

