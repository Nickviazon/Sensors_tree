from help_functions import indexes
from random import uniform


def graph_generator(n):
    """
    Generates sensor network
    :param n - number of sensors without base station
    """
    def in_circle(x0, y0, x, y, r):
        """
        Checks that the point with coordinates
         (x,y) is in the circle
        :param x0: x coordinate of center of radius
        :param y0: y coordinate of center of radius
        :param x: x coordinate of consider point
        :param y: y coordinate of consider point
        :param r: radius of circle
        :return: True if point in radius, else False
        """
        return ((x - x0) ** 2 + (y - y0) ** 2) <= (r ** 2)

    def bfs(start_node, goal_node, adj_matrix):
        """
        Breadth first search
        :param start_node:
        :param goal_node:
        :param adj_matrix: adjacency matrix
        :return: True if start node has path with goal node, else False
        """
        queue = []
        visited = [False for _ in range(len(adj_matrix))]
        visited[start_node] = True
        queue.append(start_node)
        while queue:
            node = queue.pop()
            if node == goal_node:
                return True

            for child in indexes(adj_matrix[node], 1):
                if visited[child] is False:
                    queue.append(child)
                    visited[child] = True
        return False

    # инициализируем матрицу смежности с 1 по главной диоганали
    adjacency_matrix = [[0 if k != j else 1 for k in range(n + 1)]
                        for j in range(n + 1)]

    # определяем координаты сенсоров и радиус их действия
    senosrs_coords = [(0.5, 0.5)] + [(uniform(0, 1), uniform(0, 1)) for _ in range(n)]
    radius = 0.2

    for i in range(len(adjacency_matrix)):

        while True:

            x0, y0 = senosrs_coords[i]
            sens_in_circle = [j for j, (x, y) in enumerate(senosrs_coords)
                              if in_circle(x0, y0, x, y, radius) and (x, y) != (x0, y0)]

            for j in sens_in_circle:
                adjacency_matrix[j][i] = 1
                adjacency_matrix[i][j] = 1

            path_to_bs = bfs(i, 0, adjacency_matrix)
            # если у сенсора нет пути до бс
            if i != 0 and not path_to_bs:
                senosrs_coords[i] = (uniform(0, 1), uniform(0, 1))
                for j in sens_in_circle:
                    adjacency_matrix[j][i] = 0
                    adjacency_matrix[i][j] = 0
            else:
                break

    return adjacency_matrix


if __name__ == '__main__':
    while True:
        try:
            N = int(input('Введите число сенсоров в сети: '))
            break
        except ValueError:
            print('Вы ввели некоректное число, попробуйте снова!')

    adj = graph_generator(N)
    for l in adj:
        print(l)

    import networkx as nx
    import matplotlib.pyplot as plt
    import numpy as np
    g1 = nx.from_numpy_matrix(np.matrix(adj))
    nx.draw(g1, with_labels=True)
    plt.show()
