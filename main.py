from typing import Any, List
from matrices import adjacency_matrices
from tree_gen import tree_generator
import validate


def indexes(lst: List[Any], element: int)->list:
    """Возвращает все индексы элемента в списке"""
    return [i for i, elem in enumerate(lst) if element == elem]


if __name__ == '__main__':
    schedules = []
    # graph = tree
    for adjacency_matrix in adjacency_matrices:
        need_send_msg = [[i] if i != 0 else 0 for i in range(len(adjacency_matrix))]
        schedule = []
        slot_num = 0
        while need_send_msg[0] != len(adjacency_matrix)-1:
            blocked_sensors = [False for _ in range(len(adjacency_matrix))]
            schedule.append([])  # создаем слот
            for from_sensor in range(len(adjacency_matrix)):
                # определяем сенсор получатель
                to_sensor = (adjacency_matrix[from_sensor].index(1)
                             if adjacency_matrix[from_sensor].index(1) != from_sensor
                             else adjacency_matrix[from_sensor].index(1, from_sensor + 1))

                if (blocked_sensors[to_sensor] is not True      # если сенсор получатель не блокирован
                   and blocked_sensors[from_sensor] is not True  # и сенсор отправитель не блокирован
                   and need_send_msg[from_sensor]                # и сенсору необходимо послать сообщение:
                   and from_sensor != 0):                        # и сенсор не БС
                    # определяем каким сенсорам необходимо блокировать передачу сообщений во избежания коллизий
                    indexes_for_block = indexes(adjacency_matrix[from_sensor], 1)
                    # добавляем в расписание сенсоры отправителя и получателя
                    schedule[slot_num].append((from_sensor, to_sensor))
                    # добавляем в очередь сообщений сенсора получателя(если не БС),
                    # если БС увеличиваем количество полученных сообщений на 1
                    if to_sensor != 0:
                        need_send_msg[to_sensor].append(from_sensor)
                    else:
                        need_send_msg[to_sensor] += 1
                    # блокируем сенсоры
                    for i in indexes_for_block:
                        blocked_sensors[i] = True
                    # удаляем сообщение из очереди сообщений сенсора отправителя
                    del need_send_msg[from_sensor][0]
            slot_num += 1
        schedules += [(schedule, len(schedule))]
        print(validate.validate_func(adjacency_matrix, schedule))
    # print(*schedules, sep='\n')
