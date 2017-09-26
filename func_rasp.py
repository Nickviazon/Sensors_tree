import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from validate import validateFunc


def show_graph(graph):
    '''
    Функция для отображения графа
    :param graph: матрица смежности (лист листов) или объект графа из библиотеки networkX
    :return:
    '''
    if type(graph) == list:
        graph = nx.from_numpy_matrix(np.matrix(graph))
    nx.draw_networkx(graph, with_labels=True)
    plt.show()


def rasp_create(adj_matrix):
    trans_num = len(adj_matrix)                 # Число передатчиков
    trans_buf = [1 for _ in range(trans_num)]   # Число сообщений в буфере
    trans_buf[0] = 0                            # Количество сообщений на БС
    graph = nx.from_numpy_matrix(np.matrix(adj_matrix))
    # Список следующих приёмников в маршруте
    trans_next = [nx.shortest_path(graph, i, 0)[1] if i != 0 else 0 for i in range(trans_num)]

    result_way = []  # Список передач за фрейм

    while trans_buf[0] != trans_num - 1:    # Пока все заявки не попадут на БС,...
        cur_transmission = []               # Список передач за слот
        trans_lock = [False for _ in range(trans_num)]  # Список заблокированных для передачи и приёма передатчиков

        # # Часть для выбора элемента с наиболее забитым буфером
        # trans_buf_sorted_zip = sorted(zip(trans_buf, range(len(trans_buf))), reverse=True)
        # trans_buf_sorted = [srt[1] for srt in trans_buf_sorted_zip if srt[1] != 0]
        # # /\ сюда можно добавить нужный порядок обхода
        for i in range(1, len(trans_buf)):
            transfer_elem = trans_next[i]  # Номер передатчика, который принимает сообщение
            # Проверка возможности передачи сообщения
            trans_allowed = True
            for j in range(trans_num):
                if adj_matrix[i][j] == 1 and trans_lock[j]:
                    trans_allowed = False
            # Если нет блокировок и есть что передавать...
            if trans_allowed and trans_buf[i] > 0:
                cur_transmission.append([i, transfer_elem])  # Добавление новой передачи в слот
                # Передача заявки принимающему передатчику
                trans_buf[i] -= 1
                trans_buf[transfer_elem] += 1
                # Блокировка ближайших передатчиков
                for j in range(trans_num):
                    if adj_matrix[i][j] == 1:
                        trans_lock[j] = True
                trans_lock[i] = True
        result_way.append(cur_transmission)  # Добавления слота во фрейм
    return result_way  # , len(result_way)                          # Вывод результата в формате [фрейм], число_слотов


if __name__ == '__main__':

    test_graph = [
        [0, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0]
    ]

    rasp = rasp_create(test_graph)
    print(rasp)
    print('Длина расписания равна', str(len(rasp)))
    show_graph(test_graph)  # Для просмотра вида графа
    if validateFunc(test_graph, rasp):
        print('Correct rasp')
    else:
        print('Bugs are closer than you can think it about')
