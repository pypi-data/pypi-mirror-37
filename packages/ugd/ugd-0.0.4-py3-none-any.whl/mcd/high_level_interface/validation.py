import numpy as np
from ugd.high_level_interface.construct_node_partition import constr_parition
from ugd.help_function.util import one_function,crossarrow_count


def validate_input(adj_m,anz_sim,mixing_time,var_dict,stat_f,controlls,test_variable, is_directed):
    # input validation:
    adj_m = validate_adj_matrix(adj_m, is_directed)

    anz_sim = validate_pos_int(anz_sim)
    if not (mixing_time == None):
        mixing_time = validate_pos_int(mixing_time)
    var_dict = validate_var_dict(var_dict, adj_m.shape[0])
    stat_f = validate_stat_f(stat_f, adj_m=adj_m, var_dict=var_dict)
    controlls = validate_controlls(controlls, var_dict)

    # fixme, testvariable could be non
    test_variable = valdate_test_variable(test_variable, var_dict)


def parse_input(stat_f, test_variable, controlls, var_dict, adj_m):
    'substitution input (which can be of different shape into standard shape'

    # input substitution
    if stat_f == None:
        stat_f = one_function
        if not (test_variable == None):
            def crossarrow_stat(adj_m, v_dict):
                return crossarrow_count(adj_m, v_dict, test_variable)
            stat_f = crossarrow_stat

    # fixme fine with adj
    # creation of setpartition
    nodesetpartition = constr_parition(controls=controlls, var_dict=var_dict)
    validate_nodesetpartition(nodesetpartition, adj_m.shape[0])

    return stat_f, nodesetpartition



def validate_adj_matrix(adj_m, is_directed):
    if not(isinstance(adj_m, np.ndarray)):
        raise ValueError("adjacency matrix must be a numpy array")

    n = adj_m.shape[0]
    if not(adj_m.shape[0]==adj_m.shape[1]):
        ValueError('adjacency matrix must be quadratic (n x n)')

    for i in range(n):
        for j in range(n):
            if not(adj_m[i,j] == 0) and not (adj_m[i,j]== 1):
                raise ValueError('matrix is only allowed to have 0, 1 entries (no double arrow)')

            if not(is_directed): # the plain graph case
                if not(adj_m[j,i]==adj_m[i,j]):
                    raise ValueError('for plain graph adjacency matrix must be symmetric')

    for i in range(n):
        if adj_m[i, i] == 1:
            raise ValueError('diagonal entries of matrix must be 0, (no self loops)')

    return adj_m


def validate_pos_int(anz_sim):
    try:
        anz_sim = int(anz_sim)
    except ValueError:
        print("anz sim must be a integer")
    if anz_sim <= 0:
        raise ValueError("anz_sim must be positive")
    return anz_sim

def validate_var_dict(var_dict, n):
    if var_dict==None:
        return True
    if not(isinstance(var_dict, dict)):
        raise ValueError("var_dict must be a dictionary")

    if not(n==var_dict.__len__()):
        raise ValueError('var_dict must be a dictionary with primary key the integer 1..n, where n is the nodenumbe')

    for i in range(n):
        if not(i in var_dict):
            raise ValueError('var_dict must be a dictionary with primary key the integer 1..n, where n is the nodenumbe')
        if not (isinstance(var_dict[i], dict)):
            raise ValueError("Values of vardict must be a dictionary, with the variable name as key and the varibale value as value")
    # fixme: check that always the same variables are present
    return var_dict



def validate_stat_f(stat_f, adj_m, var_dict):
    if not(stat_f==None):
        try:
            a = stat_f(adj_m,var_dict)
            try:
                b=int(a)
            except:
                raise ValueError('stat_f must be a function of form stat_f(adj_m, var_dict), and return a number')
        except:
            raise ValueError('stat_f must be a function of form stat_f(adj_m, var_dict), and return a number')
    return stat_f



def validate_controlls(controlls, var_dict):
    if controlls==None:
        return controlls
    if not(isinstance(controlls,list)):
        raise ValueError('controlls must be a list of variable names')
    for controll in controlls:
        if not(controll in var_dict[0]):
            raise ValueError('controlls must be a list of variable names, the varible names key in the values of var_dict \n'
                             'controlls[0] in var_dict[0]')
    return controlls

def valdate_test_variable(test_variable,var_dict):
    if not(isinstance(test_variable,tuple)):
        raise ValueError(' test_variable must be a tuple with 3 entries, \n'
        'first variable name of interest \n'
        'second: value of the variable form which the arrow depart \n'
        'third: value of the variable go which the arrow go \n'
                         )
    if not(test_variable[0] in var_dict[0]):
        raise ValueError('test_variable must be a tuple with 3 entries, \n'
                         'first variable name of interest \n'
                         'second: value of the variable form which the arrow depart \n'
                         'third: value of the variable go which the arrow go \n')
    return test_variable


def validate_nodesetpartition(nodesetpartition, n):
    if not(isinstance(nodesetpartition,list)):
        raise ValueError(" nodepartiton must be a list of sets")
    for nodest in nodesetpartition:
        if not(isinstance(nodest,set)):
            raise ValueError(" nodepartiton must be a list of sets")
    set_list = nodesetpartition
    total_Set = set()
    total = 0
    for sub_set in set_list:
        total_Set = total_Set.union(sub_set)
        total += sub_set.__len__()
    if not (total == total_Set.__len__()):
        raise ValueError('restriction sets are not disjoint')
    if not (total_Set == set(range(n))):
        raise ValueError('nodes in set are not the integers {0,..n-1}')
    return nodesetpartition