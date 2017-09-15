from numpy.random import choice


def tree_generator(n):
    """Генерирует сенсорное дерево на основе количества сеноров"""

    def prob_recalc(tree):
        """Перерасчитывает вероятность с кем будет связан новый сенсор"""
        edges_from_node = []
        for sensor in tree:
            edges_from_node.append(adjacency_matrix[sensor].count(1) - 1)
        edges_num = sum(edges_from_node) / 2
        prb = [edges_num / elem for elem in edges_from_node]
        prb = [prob / edges_num for prob in prb]
        sum_prb = sum(prb)
        prb = [prob / sum_prb for prob in prb]
        return prb

    sensors_tree = [0, ]  # инициализируем дерево
    # инициализируем матрицу смежности с 1 по главной диоганали
    adjacency_matrix = [[0 if i != j else 1 for i in range(n + 1)]
                        for j in range(n + 1)]
    prob_for_sensors = [1 if i == 0 else 0 for i in sensors_tree]
    for i in range(1, n+1):
        # выбираем сенсор для соединения и вносим информацию о связи в матрицу смежности
        index_for_concat = choice(sensors_tree, p=prob_for_sensors)
        adjacency_matrix[index_for_concat][i] = 1
        adjacency_matrix[i][index_for_concat] = 1
        sensors_tree.append(i)
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

    adj = tree_generator(N)

