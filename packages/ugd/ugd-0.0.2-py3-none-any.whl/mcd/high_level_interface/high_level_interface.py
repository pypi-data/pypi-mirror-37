

'''costum function'''
from ugd.help_function.graph_creation import generate_graph, graph_to_adj_m
from ugd.high_level_interface.construct_node_partition import constr_parition
from ugd.high_level_interface.output_processing import postprocess
from ugd.high_level_interface.time_mixing_evaluation import evaluate_mixing_time
from ugd.high_level_interface.validation import validate_adj_matrix, validate_nodesetpartition, validate_pos_int, \
    validate_var_dict, valdate_test_variable, validate_controlls, validate_stat_f
from ugd.markov_walk.markov_walk import markov_walk


def digraph_hyp_test(adj_m, var_dict = None, stat_f = None, test_variable= None, controlls=None,  mixing_time=None ,anz_sim = 1000, show_polt = False):
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

    # input validation:
    adj_m = validate_adj_matrix(adj_m)
    anz_sim = validate_pos_int(anz_sim)
    if not(mixing_time==None):
        mixing_time = validate_pos_int(mixing_time)
    var_dict = validate_var_dict(var_dict, adj_m.shape[0])
    stat_f = validate_stat_f(stat_f,adj_m=adj_m,var_dict=var_dict)
    controlls = validate_controlls(controlls, var_dict)
    test_variable = valdate_test_variable(test_variable,var_dict)


    # input substitution
    if stat_f == None:
        stat_f = one_function
        if not(test_variable == None):
            def crossarrow_stat(adj_m, v_dict):
                return crossarrow_count(adj_m,v_dict, test_variable)
            stat_f = crossarrow_stat

    # creation of setpartition
    nodesetpartition = constr_parition(controls=controlls, var_dict = var_dict)


    # determination of mixing time:
    mixing_time = evaluate_mixing_time(adj_m, nodesetpartition, mixing_time, anz_sim)


    # running statistics
    graphs, stats_list = gen_draws(adj_m=adj_m, var_dict =var_dict, stat_f=stat_f,nodesetpartition=nodesetpartition,
                                   anz_sim =anz_sim, mixing_time= mixing_time)

    # post processing, estimating the distribution, plotting
    postprocess(adj_m_original=adj_m, stats_list=stats_list,var_dict =var_dict, stat_f=stat_f, show_polt = show_polt)

    return graphs, stats_list



def gen_draws(adj_m,nodesetpartition, mixing_time=1000 ,anz_sim = 1000, var_dict = None, stat_f = None):
    '''
    Generates Random Digraphs with in- and outdegee equal to the input adjancy matrix

    :param adj_m:   2 dimensional numpy array with only 0 and 1 entries (0 on the diagonal) representing
                    an adjancy matrix.
           anz_sim: positive integer, number of output simulations.


    :return adj_m_list:  list of 2 dimensional numpy array represinting the simulated digraphs
    :return weight_list: a list of the graphweights, the weights are tuples of a (a,b) float and int,
                         representing the number a*10^b
    '''

    if stat_f == None:
        stat_f = one_function

    # input validation:
    n = adj_m.shape[0]
    validate_nodesetpartition(nodesetpartition, n)

    # Transform to graph
    graph = generate_graph(adj_m, nodesetpartition)

    graph_list = []
    stat_list = []
    # a random draw
    for i in range(anz_sim):
        graph = markov_walk(graph, mixing_time)
        graph_list.append(graph_to_adj_m(graph))
        adj_m_generated = graph_to_adj_m(graph)
        stat_list.append(stat_f(adj_m_generated, var_dict))
        # postprocessing (generate statistics) stat_f

    return graph_list, stat_list

def one_function(adj_m, var_dict):
    return None

def crossarrow_count(adj_m, var_dict, test_border):
    key, from_value, to_value = test_border
    count = 0;
    n = adj_m.shape[0]
    for i in range(n):
        for j in range(n):
            if adj_m[i,j]==1 and var_dict[i][key]== from_value and var_dict[j][key]==to_value:
                count += 1
    return count



