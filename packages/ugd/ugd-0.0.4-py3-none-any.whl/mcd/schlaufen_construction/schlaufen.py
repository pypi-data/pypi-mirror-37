
from ugd.schlaufen_construction.schlaufen_construction import add_plain_random_schleife
from ugd.schlaufen_construction.di_schlaufen_construction import add_di_random_schleife

def add_random_schleife(graph, schleifen_number):
    if graph.is_directed:
        return add_di_random_schleife(graph, schleifen_number)
    else:
        return add_plain_random_schleife(graph, schleifen_number)