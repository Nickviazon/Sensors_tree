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
    # frame- Массив слотов, в каждом слоте указаны все сенсоры, сообщения которых были переданы на БС
    # example:  [[1,2],[4], ...]
    frame = []
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
        frame.append([])
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
                        # Блокировка на передачу и прием ближайших передатчиков
                        receive_lock = [True if neighbor == 1 or j == source
                                        else receive_lock[j]
                                        for j, neighbor in enumerate(adj_matrix[source])]

                        trans_lock = [True if neighbor == 1 or j == receive
                                      else trans_lock[j]
                                      for j, neighbor in enumerate(adj_matrix[receive])]

                        trans_lock[receive] = True
                        trans_lock[source] = True
                        sens_buf[receive] += 1
                        sens_buf[source] -= 1
                        message_route[0].pop()

                        if len(message_route[0]) == 1:
                            num_req_to_exit[message_route[1][0]] += 1
                            frame[-1].append(message_route[1][0])
                        route = trans_routes[source].pop(trans_routes[source].index(message_route))
                        trans_routes[receive].append(route)

        # frame_len += 1
    return frame, num_req_to_exit   #result_way


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

    # сообщения которые уйдут, но еще в системе
    sensors_out = [1 if i > 0 else 0 for i, _ in enumerate(range(len(adj)))]
    sensors_in = [0 for i, _ in enumerate(range(len(adj)))]  # сообщения которые придут на слоте
    frame, req_num_to_exit = rasp_create(adj_matrix=adj, balance=True)
    avg_buff, slot_num, frame_num, new_frame = 0, 0, 0, False

    # количество пришедших сообщений в слот
    count_come = np.random.binomial(1, prb, size=[1000000, len(adj)-1])

    for total_slots, slot_income in enumerate(count_come):  # общее количество слотов, сообщения на каждый сенсор
        if frame_num > num_of_frames:
            break

        if adaptation and new_frame is True:
            frame, _ = rasp_create(adj_matrix=adj, sens_buf=sensors_out[:], balance=True)
            new_frame = False

        sensors_in = [0 if i == 0 else sensors_in[i]+slot_income[i-1] for i in range(len(adj))]
        
#        print(frame)
        if frame:
#            print('slot num = {}; Len frame = {}'.format(slot_num,len(frame)))
#            print('Before: {}'.format(sensors_out))
            sensors_out = [sens-1 if i in frame[slot_num] and sens>0 else sens for i, sens in enumerate(sensors_out)]
#            print('After: {}'.format(sensors_out))
#            input()

        avg_buff += sum(sensors_in)+sum(sensors_out)
        slot_num += 1
        if slot_num >= len(frame):
            # в конце фрейма все приходящие сообщения становятся уходящими на следующем слоте,
            # а все приходящие обнуляются
            sensors_out = [sensors_in[k] + sensors_out[k] for k in range(len(sensors_in)) ]
            sensors_in = [0 for i, _ in enumerate(range(len(adj)))]
            slot_num, new_frame = 0, True
            frame_num += 1

    avg_buff /= total_slots

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


if __name__=="__main__":
    from interactive_console import interactive_console
    adjacency_matrix = interactive_console()
    print(sens_graph_with_prob(adjacency_matrix, prb=0.125, num_of_frames=1000, adaptation=True))