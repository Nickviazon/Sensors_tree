from numpy.random import choice
from random import randint, uniform


def graph_generator(n):
    """
    Generates sensor network
    :param n - number of sensors without base station
    """
    def in_circle(x0, y0, x, y, r):
        return ((x - x0) ** 2 + (y - y0) ** 2) <= (r ** 2)

    def prob_recalc(tree):
        """Перерасчитывает вероятность с кем будет связан новый сенсор"""
        edges_from_node = []
        for sensor in tree:
            edges_from_node.append(adjacency_matrix[sensor].count(1) - 1)

        if not all(edges_from_node):
            return [1 / len(tree) for _ in tree]

        edges_num = sum(edges_from_node) / 2
        prb = [edges_num/(edges_num*elem*2) if elem != 0 else 1 for elem in edges_from_node]

        if prb == [1 for _ in tree]:
            return [1/len(tree) for _ in tree]
        else:
            prb = [prob / edges_num for prob in prb]
            sum_prb = sum(prb)
            prb = [prob / sum_prb for prob in prb]
            return prb

    # инициализируем матрицу смежности с 1 по главной диоганали
    adjacency_matrix = [[0 if i != j else 1 for i in range(n + 1)]
                        for j in range(n + 1)]
    # определяем координаты сенсоров и радиус их действия
    senosrs_coords = [(0, 0)] + [(uniform(-10, 10), uniform(-10, 10)) for _ in range(n)]
    radius = 5

    for i in range(len(adjacency_matrix)):
        while True:
            x0, y0 = senosrs_coords[i]
            sens_in_circle = [j for j, (x, y) in enumerate(senosrs_coords)
                              if in_circle(x0, y0, x, y, radius) and (x, y) != (x0, y0)]
            if len(sens_in_circle) < 2:
                senosrs_coords[i] = (uniform(-10, 10), uniform(-10, 10))
            else:
                break

        if len(sens_in_circle) <= 3:
            sample = len(sens_in_circle)
        else:
            sample = randint(2, len(sens_in_circle))
        index_for_concat = choice(sens_in_circle, sample, p=prob_recalc(sens_in_circle))

        for j in index_for_concat:
            adjacency_matrix[j][i] = 1
            adjacency_matrix[i][j] = 1
        # выбираем сенсор для соединения и вносим информацию о связи в матрицу смежности
        # index_for_concat = choice(in_circle[i],p=prob_recalc(in_circle[i]))
    return adjacency_matrix


if __name__ == '__main__':
    while True:
        try:
            N = int(input('Введите число сенсоров в сети: '))
            break
        except ValueError:
            print('Вы ввели некоректное число, попробуйте снова!')

    adj = graph_generator(N)
    for i in adj:
        print(i)

    import networkx as nx
    import matplotlib.pyplot as plt
    import numpy as np
    g1 = nx.from_numpy_matrix(np.matrix(adj))
    nx.draw(g1, with_labels=True)
    plt.show()



