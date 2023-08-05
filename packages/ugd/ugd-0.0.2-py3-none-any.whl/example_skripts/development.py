from ugd import digraph_hyp_test
from ugd import graph_hyp_test

import numpy as np
adj_m = np.zeros((4,4))
adj_m[0,1] = 1
adj_m[2,3] = 1
var_dict ={
    0: {'gender': 'm'},
    1: {'gender': 'm'},
    2: {'gender': 'f'},
    3: {'gender': 'f'},
}

graphs, stats_list = digraph_hyp_test(adj_m=adj_m, var_dict = var_dict, test_variable= ('gender','m','f'), mixing_time=1000, anz_sim=10, show_polt=False)


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

# fixme _noch_falsch
graphs, stats_list = graph_hyp_test(adj_m=adj_m, var_dict=var_dict, test_variable=('gender', 'm', 'f'),
                                    mixing_time=1000, anz_sim=500, show_polt=True)
