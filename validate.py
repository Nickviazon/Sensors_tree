class ValidateError(Exception):
    pass


def validate_func(graph, rasp, log=False):
    # Типо документация
    """
    Процедура проверки правильности расписания
    1) Проверка слотов на конфликты
    2) Проверка передачи всех сообщений на БС по окончанию валидации
    3) Проверка корректной передачи сообщений
    :param graph:  Входной граф сенсорной сети
    :param rasp: Расписание построенное для сенсорной сети
    :param log: Вывод логов
    :return: в случае успешной валидации True, если расписание не правильное выкидывается ошибка
    """
    count_nodes = len(graph)  # Количество сенсоров в сети
    weight_nodes = [1 for _ in range(count_nodes)]  # Сообщения в сенсорах
    len_rasp = len(rasp)
    if log:
        print("Начало валидации расписания")
    for i in range(len_rasp):
        if log:
            print("-------------\nВалидация ", i, " шага расписания")
        weight_nodes = step_validation(graph, rasp[i], weight_nodes, log)
    if max(weight_nodes[1:]) > 0:
        raise ValidateError("Не все сообщения переданы на БС " + str(weight_nodes))
    if log:
        print("Валидация завершена")
    return True


def step_validation(graph, step, weight_nodes, log):
    conflict = []
    len_step = len(step)
    for i in range(len_step):
        if log:
            print("Передатчик ", step[i][0])
            print("Приёмник ", step[i][1])
        if step[i][0] == step[i][1]:  # Проверка на то что приёмник и передатчик не совпадают
            raise ValidateError("Приёмник и передатчик совпадает " + str(step[i][0]))
        if step[i][0] in conflict or step[i][1] in conflict:  # Проверка на конфликты
            raise ValidateError("Возникла коллизия, заблокированные сенсоры " + str(conflict))
        if graph[step[i][0]][step[i][1]] == 0:
            raise ValidateError("Такого маршрута не существует")
        weight_nodes[step[i][0]] -= 1
        weight_nodes[step[i][1]] += 1
        if (weight_nodes[step[i][0]] < 0
           or weight_nodes[step[i][1]] < 0):  # Валидация что бы пустой сенсор не передавал сообщения
            raise ValidateError("Передаёт сообщение пустой сенсор")
        for j in range(len(graph)):  # Матрица конфликтов
            if graph[step[i][0]][j] == 1:
                conflict.append(j)
        if log:
            print(weight_nodes)
    return weight_nodes


if __name__ == "__main__":
    import matrices as m
    list_nodes = m.adjacency_matrices[0]
    route = [[[0, 1], [0, 1], [0, 1]]]
    validate_func(list_nodes, route)
