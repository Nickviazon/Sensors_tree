from typing import Any, List
from random import choices
from numpy import array
import networkx as nx


def tree_generator(n: int = 1) -> List:
    """Генерирует сенсорное дерево на основе количества сеноров"""
    sensors_tree = [0, ]
    adjacency_matrix = [[0 if i != j else 1 for i in range(n + 1)]
                        for j in range(n + 1)]

    prob_for_sensors = [1 if i == 0 else 0 for i in sensors_tree]
    for i in range(1, n+1):
        index_for_concat = choices(sensors_tree, prob_for_sensors)[0]
        adjacency_matrix[index_for_concat][i] = 1
        adjacency_matrix[i][index_for_concat] = 1
        sensors_tree.append(i)
        count_elem = []
        for sensor in sensors_tree:
            count_elem.append(adjacency_matrix[sensor].count(1) - 1)
        prob_for_sensors = [(sum(count_elem) / 2) / elem for elem in count_elem]
    return adjacency_matrix


if __name__ == '__main__':
    while True:
        try:
            N = int(input('Введите число сенсоров в сети: '))
            break
        except ValueError:
            print('Вы ввели некоректное число, попробуйте снова!')

    adj = tree_generator(N)

