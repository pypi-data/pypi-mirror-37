import matplotlib.pyplot as plt


def postprocess(adj_m_original, stats_list, stat_f, var_dict, show_polt=False):
    '''
    General output porcessing and plotting, this part is convenient for experimenting with graph
    However can be easaly cosumized by using the output graph sequence of the algorithm
    '''

    org_value = stat_f(adj_m_original, var_dict)

    min_value  = min(stats_list)
    max_value =max(stats_list)
    y = [0] * (max_value-min_value+1)
    x= list(range(min_value,max_value+1))
    for i in stats_list:
        y[i-min_value] += 1/stats_list.__len__()


    width = 1 / 1.5
    plt.bar(x, y, width, color="blue")

    plt.axvline(x=org_value, color = 'red')
    if show_polt:
        plt.show()
    print('output')

