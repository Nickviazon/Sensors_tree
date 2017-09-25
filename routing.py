from math import inf

def dijkstra(adj_matrix, start=None, end=None):
    """
    Расчитывает расстояния от БС до всех серсоров
    :param adj_matrix - матрица смежности
    :param start - начальный сенсор
    :param end - конечный сенсор
    :todo: использовать параметр start
    """
    path = [inf if i != 0 else 0 for i, elem in enumerate(adj_matrix)]
    marker = [False for _ in range(len(adj_matrix))]

    for i, node in enumerate(adj_matrix):
        for j, edge_weight in enumerate(node):
            if edge_weight >= 0:
                if (i != j and edge_weight > 0
                     and path[j] > path[i] + edge_weight  # старый путь длинее нового
                     and marker[i] is False):
                    path[j] = path[i] + edge_weight
            else:
                raise ValueError('Отрицательные веса ребер в графе')
        marker[i] = True
    return path

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