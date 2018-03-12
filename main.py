import numpy as np
import networkx as nx


# def message_come(prob):
#     return True if uni_random(0, 1) <= prob else False


def rasp_create(adj_matrix, balance=False):
    """
    Функция для составления расписания передачи сообщений от передатчиков к Базовой Станции (БС) в случайно
    связанной сети.

    :adj_matrix: Матрица смежности. лист листов с описанием связей графового представления системы.
    :balance: Бинарная опция включения/отключения балансировки
    :prob: Вероятность появления сообщения в слоте на каждом сенсоре
    :return: длину расписания, максимальное количество сообщений которые могут уйти из фрейма
    """
    # result_way = []  # Список передач за фрейм
    frame_len, num_req_to_exit = 0, 0
    sens_num = len(adj_matrix)  # Число передатчиков
    bs_buf = 0  # Количество сообщений на БС
    graph = nx.from_numpy_matrix(np.matrix(adj_matrix))
    if balance:
        routes_p_node = np.zeros((sens_num,), dtype=np.int)
        trans_routes = [[] for _ in range(sens_num)]
        for i in range(sens_num):
            trans_routes[i] = nx.shortest_path(graph, 0, i)
            routes_p_node[trans_routes[i]] += 1
            routes_p_node[0] = 0
            for j in trans_routes[i]:
                for e_num in graph[j]:
                    graph[j][e_num]['weight'] += routes_p_node[j] * sens_num ** -2
                    graph[e_num][j]['weight'] += routes_p_node[j] * sens_num ** -2
    else:
        trans_routes = nx.shortest_path(graph, 0)

    while bs_buf < sens_num - 1:  # Пока все заявки не попадут на БС,...
        # cur_transmission = []  # Список передач за слот
        trans_lock = [False] * sens_num  # Список заблокированных для передачи передатчиков
        receive_lock = [False] * sens_num  # Список заблокированных для приёма  передатчиков

        # В цикле исключена возможность передачи сообщения из БС (т.к. начинаем с 1)
        # Проходимся по сенсорам, проверяем возможность передачи и передаём
        for i in range(1, sens_num):

            # Проверка возможности передачи сообщения
            if len(trans_routes[i]) > 1:
                source = trans_routes[i][-1]  # откуда передавать
                receive = trans_routes[i][-2]  # куда передавать

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
                    trans_routes[i].pop()
                    if len(trans_routes[i]) == 1:
                        bs_buf += 1
        frame_len += 1
        # result_way.append(cur_transmission)  # Добавления слота во фрейм
    return frame_len, bs_buf   #result_way


def sens_graph_with_prob(adj, prb=None, num_of_frames=1000):
    """
    Моделирует буфер сенсоров в сенорной сети

    :adj: Матрица смежности сенсорной сети
    :sch: Расписание работы сенсорной сети
    :prb: Вероятность появления сообщения в кажом слоте для всех сенсоров
    :num_of_frames: Количество фреймов для моделирования сенсорной сети
    :return: среднее количество сообщений в буфере каждого сенсора
    """
    assert type(prb) is float or 0 <= prb <= 1
    # sensors_buffer = [1 if i != 0 else 0 for i in range(len(adj))]
    buff_count = len(adj)-1
    frame_len, req_num_to_exit = rasp_create(adj_matrix=adj, balance=True)
    avg_buff = 0

    # количество пришедших сообщений в слот
    count_come = np.random.binomial(frame_len, prb, size=[num_of_frames, len(adj)-1])
    for sens_come in count_come:

        comes_sum = np.sum(sens_come)

        if buff_count + comes_sum - req_num_to_exit < 0:
            buff_count = 0  # обнуляем буфер если сообщений уйдет >= количеству сообщений в буфере + количество пришедших
        else:
            buff_count += comes_sum - req_num_to_exit

        avg_buff += buff_count

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
