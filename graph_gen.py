from numpy.random import choice
from random import randint


def graph_generator(n):
    """
    Generates sensor network
    :param n - number of sensors without base station
    """
    def prob_recalc(tree):
        """Перерасчитывает вероятность с кем будет связан новый сенсор"""
        edges_from_node = []
        for sensor in tree:
            edges_from_node.append(adjacency_matrix[sensor].count(1) - 1)
        edges_num = sum(edges_from_node) / 2
        prb = [edges_num/(edges_num*elem*2) if elem != 0 else 1 for elem in edges_from_node]
        prb = [prob / edges_num for prob in prb]
        sum_prb = sum(prb)
        prb = [prob / sum_prb for prob in prb]
        return prb

    sensors_tree = [i for i in range(n+1)]  # инициализируем дерево
    # инициализируем матрицу смежности с 1 по главной диоганали
    adjacency_matrix = [[0 if i != j else 1 for i in range(n + 1)]
                        for j in range(n + 1)]
    prob_for_sensors = [1/(n+1) for _ in range(n + 1)]
    for i in sensors_tree:
        # выбираем сенсор для соединения и вносим информацию о связи в матрицу смежности
        index_for_concat = choice(sensors_tree, randint(1, n//3), p=prob_for_sensors)
        for j in index_for_concat:
            adjacency_matrix[j][i] = 1
            adjacency_matrix[i][j] = 1
        # sensors_tree.append(i)
        # перерасчитываем вероятности с учетом добавленного сенсора в сеть
        prob_for_sensors = prob_recalc(sensors_tree)
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

