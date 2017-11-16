import numpy as np
import networkx as nx


def rasp_create(adj_matrix, balance=False):
    """
    Функция для составления расписания передачи сообщений от передатчиков к Базовой Станции (БС) в случайно
    связанной сети.
    :param adj_matrix: Матрица смежности. лист листов с описанием связей графового представления системы.
    :param balance: Бинарная опция включения/отключения балансировки
    :return: результат в формате расписания: [фрейм]
    """
    result_way = []  # Список передач за фрейм
    trans_num = len(adj_matrix)  # Число передатчиков
    bs_buf = 0  # Количество сообщений на БС
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

    while bs_buf < trans_num - 1:  # Пока все заявки не попадут на БС,...
        cur_transmission = []  # Список передач за слот
        trans_lock = [False] * trans_num  # Список заблокированных для передачи передатчиков
        receive_lock = [False] * trans_num  # Список заблокированных для приёма  передатчиков

        # В цикле исключена возможность передачи сообщения из БС (т.к. начинаем с 1)
        # Проходимся по сенсорам, проверяем возможность передачи и передаём
        for i in range(1, trans_num):
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
                    cur_transmission.append([source, receive])
                    # Блокировка на передачу ближайших передатчиков
                    for j, neighbor in enumerate(adj_matrix[source]):
                        if neighbor == 1 or j == source:
                            receive_lock[j] = True
                    trans_lock[receive] = True
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
    from graph_gen import graph_generator, tree_generator, grid_generator
    import validate  # Будет добавлено после тестирования корректности работы валидатора.

    while True:
        try:
            method = int(input('''Выберите метод генерации
            1 - дерево;
            2 - решетка;
            3 - случайный граф
            
            '''))
            if method in [1, 2, 3]:
                if method == 1 :
                    N = int(input('Введите число сенсоров в сети: '))
                    adjacency_matrix = tree_generator(N)
                elif method == 3:
                    N = int(input('Введите число сенсоров в сети: '))
                    adjacency_matrix = graph_generator(N)
                elif method == 2:
                    N = int(input('Введите длину стороны решетки: '))
                    if N % 2 == 0:
                        raise ValueError
                    else:
                        adjacency_matrix = grid_generator(N)
                break
            else:
                raise ValueError
        except ValueError:
            print('Вы ввели некоректное число, попробуйте снова!')

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
