import numpy as np
import networkx as nx

def routes_balance(graph):
    """
    Пытается найти наилучший путь для каждого сообщения в сенсорной сети изменяя веса ребер
    :param graph: граф сенсорной сети построенный с помощью networkx
    :return: список передач для каждого сенсора
    """
    sens_num = len(graph)
    routes_p_node = np.zeros((sens_num,), dtype=np.int)
    routes = [[] for _ in range(sens_num)]

    for i in range(sens_num):
        routes[i] = nx.shortest_path(graph, 0, i)
        routes_p_node[routes[i]] += 1
        routes_p_node[0] = 0
        for j in routes[i]:
            for e_num in graph[j]:
                graph[j][e_num]['weight'] += routes_p_node[j] * sens_num ** -2
                graph[e_num][j]['weight'] += routes_p_node[j] * sens_num ** -2

    return routes

def rasp_create(adj_matrix, sens_buf=[], balance=False):
    """
    Функция для составления расписания передачи сообщений от передатчиков к Базовой Станции (БС) в случайно
    связанной сети.

    :adj_matrix: Матрица смежности. лист листов с описанием связей графового представления системы.
    :balance: Бинарная опция включения/отключения балансировки
    :return: длину расписания, максимальное количество сообщений которые могут уйти из фрейма
    """

    frame_len, num_req_to_exit = 0, [0] * len(adj_matrix)
    sens_num = len(adj_matrix)  # Число передатчиков
    if not sens_buf:
        sens_buf = [0 if i == 0 else 1 for i in range(sens_num)]# Количество сообщений на БС
    graph = nx.from_numpy_matrix(np.matrix(adj_matrix))

    if balance:
        trans_routes = routes_balance(graph)
    else:
        trans_routes = nx.shortest_path(graph, 0)

    for i, sens_route in enumerate(trans_routes):
        if sens_buf[i] > 1:
            trans_routes[i] = [[sens_route[:], tuple([i])] for j in range(sens_buf[i])]
        elif sens_buf[i] == 1:
            trans_routes[i] = [[trans_routes[i], (i,)]]
        else:
            trans_routes[i] = []


    while any(sens_buf[1:]):  # Пока все заявки не попадут на БС,...
        # Список передач за слот
        trans_lock = [False] * sens_num  # Список заблокированных для передачи передатчиков
        receive_lock = [False] * sens_num  # Список заблокированных для приёма  передатчиков

        # В цикле исключена возможность передачи сообщения из БС (т.к. начинаем с 1)
        # Проходимся по сенсорам, проверяем возможность передачи и передаём
        for i in range(1, sens_num):
            for message_route in trans_routes[i]:
                # Проверка возможности передачи сообщения
                if len(message_route) > 1 and sens_buf[i] > 0:
                    source = message_route[0][-1]  # откуда передавать
                    receive = message_route[0][-2]  # куда передавать

                    # Проверка возможности передачи сообщения
                    trans_allowed = True
                    if trans_lock[source] or receive_lock[receive]:
                        trans_allowed = False
                    if trans_allowed:
                        # Добавление новой передачи в слот
                        # cur_transmission.append([source, receive])
                        # Блокировка на передачу ближайших передатчиков
                        for j, neighbor in enumerate(adj_matrix[source]):
                            if neighbor == 1 or j == source:
                                receive_lock[j] = True
                        for j, neighbor in enumerate(adj_matrix[receive]):
                            if neighbor == 1 or j == receive:
                                trans_lock[j] = True
                        trans_lock[receive] = True
                        trans_lock[source] = True
                        sens_buf[receive] += 1
                        sens_buf[source] -= 1
                        message_route[0].pop()
                        if len(message_route[0]) == 1:
                            num_req_to_exit[message_route[1][0]] += 1
                        route = trans_routes[source].pop(trans_routes[source].index(message_route))
                        trans_routes[receive].append(route)
        frame_len += 1
        # result_way.append(cur_transmission)  # Добавления слота во фрейм
    return frame_len, num_req_to_exit   #result_way


def sens_graph_with_prob(adj, prb=None, num_of_frames=1000, adaptation=False):
    """
    Моделирует буфер сенсоров в сенорной сети

    :adj: Матрица смежности сенсорной сети
    :sch: Расписание работы сенсорной сети
    :prb: Вероятность появления сообщения в кажом слоте для всех сенсоров
    :num_of_frames: Количество фреймов для моделирования сенсорной сети
    :adaptation: Изменять ли расписание на каждом фрейме
    :return: среднее количество сообщений в буфере каждого сенсора
    """
    assert type(prb) is float or 0 <= prb <= 1
    sensors_buffer = [1 if i > 0 else 0 for i, _ in enumerate(range(len(adj)))]
    # buff_count = len(adj)-1
    frame_len, req_num_to_exit = rasp_create(adj_matrix=adj, balance=True)
    avg_buff = 0

    # количество пришедших сообщений в слот
    count_come = np.random.binomial(frame_len, prb, size=[num_of_frames, len(adj)-1])
    for frame_num, sens_come in enumerate(count_come):

        if adaptation and frame_num > 0 and frame_num%10 == 0:
            # print(frame_num, sensors_buffer)
            _, req_num_to_exit = rasp_create(adj_matrix=adj, sens_buf=sensors_buffer, balance=True)

        sensors_buffer = [0 if i == 0 or sensor + sens_come[i-1] - req_num_to_exit[i] <= 0
                          else sensor + sens_come[i-1] - req_num_to_exit[i]
                          for i, sensor in enumerate(sensors_buffer)]
        avg_buff += sum(sensors_buffer)

    avg_buff /= num_of_frames

    return avg_buff


def show_graph(graph):
    """
    Функция для отображения графа

    :graph: матрица смежности (лист листов) или объект графа из библиотеки networkX
    :return: None
    """
    import matplotlib.pyplot as plt

    if type(graph) == list:
        graph = nx.from_numpy_matrix(np.matrix(graph))
    nx.draw_networkx(graph, with_labels=True)
    plt.show()
