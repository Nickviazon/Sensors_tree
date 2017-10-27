# from help_functions import indexes
import numpy as np
import networkx as nx

# Функция Виталия была временно закомментирована
# def sensors_tree(adj_matrix):
    # def dfs(node_index):
    #     """
    #     Обход дерева в глубину.
    #     При обходе сенсор сразу пытается отдать сообщение
    #     """
    #     from_sensor = node_index
    #     visited_sensors.append(from_sensor)
    #     to_sensor = (adjacency_matrix[from_sensor].index(1)
    #                  if adjacency_matrix[from_sensor].index(1) != from_sensor
    #                  else adjacency_matrix[from_sensor].index(1, from_sensor + 1))
    #     if (blocked_sensors[to_sensor] is not True  # если сенсор получатель не блокирован
    #         and blocked_sensors[from_sensor] is not True  # и сенсор отправитель не блокирован
    #         and need_send_msg[from_sensor]  # и сенсору необходимо послать сообщение:
    #         and from_sensor != 0):
    #         # определяем каким сенсорам необходимо блокировать передачу сообщений во избежания коллизий
    #         indexes_for_block = indexes(adjacency_matrix[from_sensor], 1)
    #         # добавляем в расписание сенсоры отправителя и получателя
    #         schedule[slot_num].append((from_sensor, to_sensor))
    #         # добавляем в очередь сообщений сенсора получателя(если не БС),
    #         # если БС увеличиваем количество полученных сообщений на 1
    #         if to_sensor != 0:
    #             need_send_msg[to_sensor].append(from_sensor)
    #         else:
    #             need_send_msg[to_sensor] += 1
    #         # блокируем сенсоры
    #         for i in indexes_for_block:
    #             blocked_sensors[i] = True
    #         # удаляем сообщение из очереди сообщений сенсора отправителя
    #         del need_send_msg[from_sensor][0]
    #
    #     for i, edge in enumerate(adjacency_matrix[from_sensor]):
    #         if i not in visited_sensors and edge == 1:
    #             dfs(i)
    #
    # adjacency_matrix = adj_matrix
    # need_send_msg = [[i] if i != 0 else 0 for i in range(len(adjacency_matrix))]
    # schedule = []
    # slot_num = 0
    # while need_send_msg[0] != len(adjacency_matrix) - 1:
    #     blocked_sensors = [False for _ in range(len(adjacency_matrix))]
    #     visited_sensors = []
    #     schedule.append([])
    #     dfs(0)
    #     slot_num += 1
    # return schedule


def rasp_create(adj_matrix, balance=False):
    """
    Функция для составления расписания передачи сообщений от передатчиков к Базовой Станции (БС) в случайно
    связанной сети.
    :param adj_matrix: Матрица смежности. лист листов с описанием связей графового представления системы.
    :param balance: Бинарная опция включения/отключения балансировки
    :return: результат в формате расписания: [фрейм]
    """
    result_way = []                             # Список передач за фрейм
    trans_num = len(adj_matrix)                 # Число передатчиков
    bs_buf = 0                                  # Количество сообщений на БС
    graph = nx.from_numpy_matrix(np.matrix(adj_matrix))
    if balance:
        routes_p_node = np.zeros((trans_num,), dtype=np.int)
        trans_routes = [[] for _ in range(trans_num)]
        for i in range(trans_num):
            trans_routes[i] = nx.shortest_path(graph, 0, i)
            routes_p_node[trans_routes[i]] += 1
            routes_p_node[0] = 0
            for j in trans_routes[i]:
                for e_num in graph[j]:
                    graph[j][e_num]['weight'] += routes_p_node[j] * trans_num ** -2
                    graph[e_num][j]['weight'] += routes_p_node[j] * trans_num ** -2
    else:
        trans_routes = nx.shortest_path(graph, 0)

    while bs_buf < trans_num - 1:                       # Пока все заявки не попадут на БС,...
        cur_transmission = []                           # Список передач за слот
        trans_lock = [False for _ in range(trans_num)]  # Список заблокированных для передачи и приёма передатчиков

        # В цикле исключена возможность передачи сообщения из БС (т.к. начинаем с 1)
        # Проходимся по сенсорам, проверяем возможность передачи и передаём
        for i in range(1, trans_num):
            # Проверка возможности передачи сообщения
            if len(trans_routes[i]) > 1:
                source = trans_routes[i][-1]        # откуда передавать
                receive = trans_routes[i][-2]       # куда передавать
                trans_allowed = True
                for j in range(trans_num):
                    if adj_matrix[source][j] == 1 and trans_lock[j]:
                        trans_allowed = False
                if trans_allowed:
                    # Добавление новой передачи в слот
                    cur_transmission.append([source, receive])
                    # Блокировка ближайших передатчиков
                    for j in range(trans_num):
                        if adj_matrix[source][j] == 1:
                            trans_lock[j] = True
                    trans_lock[source] = True
                    trans_routes[i].pop()
                    if len(trans_routes[i]) == 1:
                        bs_buf += 1
        result_way.append(cur_transmission)  # Добавления слота во фрейм
    return result_way  # , len(result_way)                          # Вывод результата в формате [фрейм], число_слотов


def show_graph(graph):
    """
    Функция для отображения графа
    :param graph: матрица смежности (лист листов) или объект графа из библиотеки networkX
    :return:
    """
    import matplotlib.pyplot as plt

    if type(graph) == list:
        graph = nx.from_numpy_matrix(np.matrix(graph))
    nx.draw_networkx(graph, with_labels=True)
    plt.show()


if __name__ == '__main__':
    from graph_gen import graph_generator
    import validate     # Будет добавлено после тестирования корректности работы валидатора.

    # while True:
    #     try:
    #         N = int(input('Введите число сенсоров в сети: '))
    #         break
    #     except ValueError:
    #         print('Вы ввели некоректное число, попробуйте снова!')
    # adjacency_matrix = graph_generator(N)
    # adjacency_matrix = [
    #     [0, 1, 1, 1, 1, 0, 0, 0, 0],
    #     [1, 0, 0, 0, 0, 1, 0, 1, 0],
    #     [1, 0, 0, 0, 0, 1, 1, 0, 0],
    #     [1, 0, 0, 0, 0, 0, 1, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 1, 1],
    #     [0, 1, 1, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 1, 1, 0, 0, 0, 0, 0],
    #     [0, 1, 0, 0, 1, 0, 0, 0, 0],
    #     [0, 0, 0, 1, 1, 0, 0, 0, 0]
    # ]
    adjacency_matrix = [[1, 1, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 1, 1, 1, 0, 0, 1],
                        [0, 0, 1, 1, 0, 1, 0, 1, 1],
                        [0, 1, 1, 1, 1, 1, 0, 0, 1],
                        [0, 1, 0, 1, 1, 1, 1, 0, 1],
                        [0, 1, 1, 1, 1, 1, 0, 0, 1],
                        [0, 0, 0, 0, 1, 0, 1, 1, 1],
                        [0, 0, 1, 0, 0, 0, 1, 1, 0],
                        [0, 1, 1, 1, 1, 1, 1, 0, 1]]

    import time

    start_time = time.time()
    schedule = rasp_create(adjacency_matrix)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(schedule)
    print('Длина расписания равна {}'.format(len(schedule)))
    start_time = time.time()
    schedule1 = rasp_create(adjacency_matrix, balance=True)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(schedule1)
    print('Длина расписания равна {}'.format(len(schedule1)))
    show_graph(adjacency_matrix)
