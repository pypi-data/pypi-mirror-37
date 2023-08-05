'''User Interface with documentation '''

from ugd.high_level_interface.draw_simulations import hyp_test

def digraph_hyp_test(adj_m, var_dict = None, stat_f = None, test_variable= None, controlls=None,  mixing_time=None ,
                     anz_sim = 1000, show_polt = False):
    '''
    PURPUSE: gerneration of random Digraphs wich a given degreesequenz and "crossarrow" restrictions, in order to estimate
             the distribution of a teststatistic under the 0 Hypotheses. Futher explanation on methods is given in
             paper : ........

    INPUT:
    :param adj_m: a numpy array containing 0 and 1s as elements, representing ajdancy matrix of the Digraph
    :param var_dict: A dictionary with the interger 1..n as primary key, where n is the number of nodes,
                     the Values are dictionaries as well with the variable names as key and the variable value as value
                     the values have to be numbers or strings
    :param stat_f:  a function which maps the adj_m and var_dict to a number "The statistic of interest".
    :param test_variable: alternative to stat_f, creating a statistic which counts arf form a nodesubses into another:
                     a triple with first element variable name, second the value of the variable for the set where the
                     arcs leave and third the value of the subset where the arrow go to
    :param controlls: list of variable names of controlls
    :param mixing_time: number of runs (stepps in the markov graph) before a the graph is considered random
    :param anz_sim: number of simulations
    :param show_polt: Boolean whether a plot is desired
    :return:
    graph_list: list of random adjacency matrices with the given degreeserie and the crossarrow
    stats_list: list of the statistics stat_f evaluated for the random graphs

    USAGE:
    import numpy
    adj_m = numpy.zeros((4,4))
    adj_m[0,1] = 1
    adj_m[2,3] = 1
    var_dict ={
        0: {'gender': 'm'},
        1: {'gender': 'm'},
        2: {'gender': 'f'},
        3: {'gender': 'f'},
    }
    graphs, stats_list = digraph_hyp_test(adj_m=adj_m, var_dict = var_dict, test_variable= ('gender','m','f'),mixing_time=10000, anz_sim=100, show_polt=True)

    AUTORS:
    Andrin Pelican, andrin.pelican@unisg.ch

    '''

    return hyp_test(adj_m, var_dict, stat_f, test_variable, controlls, mixing_time, anz_sim, show_polt, is_directed=True)


def graph_hyp_test(adj_m, var_dict = None, stat_f = None, test_variable= None, controlls=None,  mixing_time=None ,
                   anz_sim = 1000, show_polt = False):
    # fixme rewrite the comments
    '''
    PURPUSE: gerneration of random Graphs wich a given degreesequenz and "crossarrow" restrictions, in order to estimate
             the distribution of a teststatistic under the 0 Hypotheses. Futher explanation on methods is given in
             paper : ........

    INPUT:
    :param adj_m: a numpy array containing 0 and 1s as elements, representing ajdancy matrix of the graph
    :param var_dict: A dictionary with the interger 1..n as primary key, where n is the number of nodes,
                     the Values are dictionaries as well with the variable names as key and the variable value as value
                     the values have to be numbers or strings
    :param stat_f:  a function which maps the adj_m and var_dict to a number "The statistic of interest".
    :param test_variable: alternative to stat_f, creating a statistic which counts arf form a nodesubses into another:
                     a triple with first element variable name, second the value of the variable for the set where the
                     arcs leave and third the value of the subset where the arrow go to
    :param controlls: list of variable names of controlls
    :param mixing_time: number of runs (stepps in the markov graph) before a the graph is considered random
    :param anz_sim: number of simulations
    :param show_polt: Boolean whether a plot is desired
    :return:
    graph_list: list of random adjacency matrices with the given degreeserie and the crossarrow
    stats_list: list of the statistics stat_f evaluated for the random graphs

    USAGE:
    import numpy
    adj_m = numpy.zeros((4,4))
    adj_m[0,1] = 1
    adj_m[1,0] = 1
    adj_m[3,2] = 1
    adj_m[2,3] = 1
    var_dict ={
        0: {'gender': 'm'},
        1: {'gender': 'm'},
        2: {'gender': 'f'},
        3: {'gender': 'f'},
    }
    graphs, stats_list = graph_hyp_test(adj_m=adj_m, var_dict = var_dict, test_variable= ('gender','m','f'),mixing_time=10000, anz_sim=100, show_polt=True)

    AUTORS:
    Andrin Pelican, andrin.pelican@bluewin.ch

    '''

    return hyp_test(adj_m, var_dict, stat_f, test_variable, controlls, mixing_time, anz_sim, show_polt, is_directed=False)
