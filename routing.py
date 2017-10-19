from math import inf
import help_functions


def dijkstra(adj_matrix):
    """
    Calculates minimum paths from base station to all sensors
    :param adj_matrix - adjacency matrix
    """

    node_weight = [inf if i != 0 else 0 for i, elem in enumerate(adj_matrix)]
    paths = [[] for _ in adj_matrix]
    marker = [False for _ in range(len(adj_matrix))]

    for node in adj_matrix:
        if list(filter(lambda x: x < 0, node)):
            raise ValueError('Negative edges weight in the graph')

    stack = [0]
    for node in stack:
        itr = [j for j in help_functions.indexes(adj_matrix[node], 0, 'grt') if j != node and j not in stack]
        for itr_elem in itr:
            stack.append(itr_elem)

    for i in stack:
        for j in help_functions.indexes(adj_matrix[i], 0, 'grt'):
            if (i != j
                and node_weight[j] > node_weight[i] + adj_matrix[i][j]  # the old path are longer then new
                and marker[i] is False):
                node_weight[j] = node_weight[i] + adj_matrix[i][j]
                paths[j] = paths[i] + [i]
        marker[i] = True
    return paths


if __name__ == '__main__':
    from graph_gen import graph_generator

    a = [[1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
         [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
         [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
         [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1],
         [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
         [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
         [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0],
         [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1],
         [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1]]

    b = dijkstra(a)
    print(b)
    for row in a:
        print(row)

    import networkx as nx
    import matplotlib.pyplot as plt
    import numpy as np
    g1 = nx.from_numpy_matrix(np.matrix(a))
    nx.draw(g1, with_labels=True)
    plt.show()
