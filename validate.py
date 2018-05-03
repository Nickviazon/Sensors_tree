import unittest


class CreateBalanceScheduleTestCase(unittest.TestCase):

    def __init__(self, adj_matrix, schedule):
        super(CreateBalanceScheduleTestCase, self).__init__()
        self.adj_matrix = adj_matrix
        self.schedule = schedule

    def test_len_slot(self):
        for slot in self.schedule:
            self.assertLessEqual(len(slot), 1, "Length of slot can't be more than 1")

    def test_direct_path_from_sensor_to_base_station(self):
        for slot in self.schedule:
            if slot:
                self.assertEqual(self.adj_matrix[slot[0]][0], 1,
                                 "Direct path is not exists for the {} sensor ").format(slot[0])
                self.assertEqual(self.adj_matrix[0][slot[0]], 1,
                                 "Direct path is not exists for the {} sensor ").format(slot[0])

    def test_messages_count_to_base_station(self):
        count = 0
        for slot in self.schedule:
            if slot:
                count += 1
        self.assertLessEqual(count, len(self.adj_matrix), "Too many recieves to the base station")



# class validateError(Exception):
#     pass
#
#
# def validateFunc(graph, rasp, log=False):
#     # Типо документация
#     """
#     Процедура проверки правильности расписания
#     1) Проверка слотов на конфликты
#     2) Проверка передачи всех сообщений на БС по окончанию валидации
#     3) Проверка корректной передачи сообщений
#     :param graph:  Входной граф сенсорной сети
#     :param rasp: Расписание построенное для сенсорной сети
#     :param log: Вывод логов
#     :return: в случае успешной валидации True, если расписание не правильное выкидывается ошибка
#     """
#     count_nodes = len(graph)  # Количество сенсоров в сети
#     weight_nodes = [1 for i in range(count_nodes)]  # Сообщения в сенсорах
#     len_rasp = len(rasp)
#     if log:
#         print("Начало валидации расписания")
#     for i in range(len_rasp):
#         if log:
#             print("-------------\nВалидация ", i, " шага расписания")
#         weight_nodes = stepValidation(graph, rasp[i], weight_nodes, log)
#         if weight_nodes is False:
#             print(graph)
#             raise validateError("Произошла ошибка на " + str(i) + " шаге")
#     if max(weight_nodes[1:]) > 0:
#         return False
#         # raise validateError("Не все сообщения переданы на БС "+str(weight_nodes))
#     if log:
#         print("Валидация завершена")
#     return True
#
#
# def stepValidation(graph, step, weight_nodes, log):
#     blocked_transmit = []  # заблокированные перeдатчики
#     blocked_receive = []  # заблокированные приёмники
#     len_step = len(step)
#     for i in range(len_step):
#         if log:
#             print("Передатчик ", step[i][0])
#             print("Приёмник ", step[i][1])
#         if step[i][0] == step[i][1]:  # Проверка на то что приёмник и передатчик не совпадают
#             return False
#             # raise validateError("Приёмник и передатчик совпадает "+str(step[i][0]))
#         if step[i][0] in blocked_transmit or step[i][1] in blocked_receive:  # Проверка на конфликты
#             return False
#             # raise validateError("Возникла коллизия, заблокированные сенсоры "+str(conflict))
#         if graph[step[i][0]][step[i][1]] == 0:
#             return False
#             # raise validateError("Такого маршрута не существует")
#         weight_nodes[step[i][0]] -= 1
#         weight_nodes[step[i][1]] += 1
#         blocked_receive.append(step[i][0])  # Блокируем текущие ноды на приём и передачу
#         blocked_receive.append(step[i][1])
#         blocked_transmit.append(step[i][0])
#         blocked_transmit.append(step[i][1])
#         if weight_nodes[step[i][0]] < 0 or weight_nodes[
#             step[i][1]] < 0:  # Валидация что бы пустой сенсор не передавал сообщения
#             # raise validateError("Передаёт сообщение пустой сенсор")
#             return False
#         # for j in range(len(graph)): #Матрица конфликтов
#         #     if (graph[step[i][0]][j]==1):
#         #         conflict.append(j)
#         for j in range(len(graph)):  # Блокировки
#             if graph[step[i][1]][j] > 0:  # блокируем передатчики
#                 blocked_transmit.append(j)
#             if graph[step[i][0]][j] > 0:  # блокируем приёмники
#                 blocked_receive.append(j)
#         if log:
#             print(weight_nodes)
#     return weight_nodes

if __name__ == "__main__":
    from main import rasp_create
    from graph_gen import graph_generator

    adj = graph_generator(100)
    sch = rasp_create(adj, balance=True)

    suite = unittest.TestSuite()
    suite.addTest(CreateBalanceScheduleTestCase(adj, sch))

    unittest.TextTestRunner.run(suite)
