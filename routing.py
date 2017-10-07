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

    for i, node in enumerate(adj_matrix):
        for j in help_functions.indexes(node, 0, 'grt'):
            if (i != j
                and node_weight[j] > node_weight[i] + node[j]  # the old path are longer then new
                and marker[i] is False):
                node_weight[j] = node_weight[i] + node[j]
                paths[j] = paths[i] + [i]
        marker[i] = True
    return paths


if __name__ == '__main__':
    __doc__ = """
    вид тестового графа:
            БС
           | 
           1
          | | \
          2 3 5
            |
            4
    """

    a = [[1, 1, 0, 0, 0, 0],
         [1, 1, 1, 1, 0, 1],
         [0, 1, 1, 0, 0, 0],
         [0, 1, 0, 1, 1, 0],
         [0, 0, 0, 1, 1, 0],
         [0, 1, 0, 0, 0, 1]]
    b = dijkstra(a)
    print(b)
