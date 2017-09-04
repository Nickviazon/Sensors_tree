from typing import Any, List
import matrices


def _indexes(lst: List[Any], element: int)->list:
    """Возвращает все индексы элемента в списке"""
    return [i for i, elem in enumerate(lst) if element == elem]


def _create_tree(num_of_sensors: int)->list:
    """Функция для инициализации сенсорного дерева"""
    sensor_list = [Sensor(i) for i in range(0, num_of_sensors)]
    return sensor_list


class Sensor:
    """Сенсор для сенсорного дерева"""
    def __init__(self, sensor_num: int):
        self.blocked = False
        self.sensor_num = sensor_num  # порядковый номер сенсора
        self.need_send_msg = [sensor_num]  # хранится ли в сенсоре сообщение


class SensorTree:
    """Сенсорное дерево"""
    def __init__(self, c_matrix: List[List[int]]):
        self.c_matrix = c_matrix  # Матрица смежности
        self.num_of_sensors = len(self.c_matrix)  # количество сенсоров в дереве
        self.sensor_list = _create_tree(self.num_of_sensors)  # список всех сенсоров
        self.bs_is_not_full = True  # истинно когда все сенсоры передали сообщения

    def sensors_update(self)->None:
        """Убирает блокировку передачи"""
        for sensor in self.sensor_list:
            if sensor is not None:
                sensor.blocked = False

if __name__ == '__main__':
    schedules = []
    for matrix in matrices.test_matrices:
        sensor_tree = SensorTree(matrix)
        del matrix
        sensors = sensor_tree.sensor_list
        schedule = []
        slot_num = 0
        while sensor_tree.bs_is_not_full:
            schedule.append([])  # создаем слот
            for sensor in sensors:
                sensor_num = sensor.sensor_num
                if sensor_num > 0:  # если сенсор не БС
                    to_sensor = sensor_tree.c_matrix[sensor_num].index(1)  # определяем сенсор получатель
                    if (not sensors[to_sensor].blocked  # если сенсор получатель не блокирован
                       and not sensor.blocked           # и сенсор отправитель не блокирован
                       and sensor.need_send_msg):       # и сенсору необходимо послать сообщение:
                        # определяем каким сенсорам необходимо блокировать передачу сообщений во избежания коллизий
                        indexes_for_block = _indexes(sensor_tree.c_matrix[sensor_num], 1)
                        # добавляем в расписания сенсоры отправителя и получателя
                        schedule[slot_num].append((sensor_num, to_sensor))
                        # добавляем в очередь сообщений сенсора получателя(если не БС)
                        if sensors[to_sensor].sensor_num > 0:
                            sensors[to_sensor].need_send_msg.append(sensor_num)
                        # блокируем сенсоры
                        for i in indexes_for_block:
                            sensors[i].blocked = True
                        # для сенсора отправителя убираем необходимость передачи сообщения
                        del sensor.need_send_msg[0]
                # для БС отсутствует необходимость в передаче сообщения
                elif sensor.sensor_num == 0:
                    sensor.need_send_msg = []
            else:
                # закрываем слот и убираем блокировки сенсоров
                slot_num += 1
                sensor_tree.sensors_update()
                # если пустой слот, значит конец фрейма и расписание составлено
                if not schedule[-1]:
                    schedule.remove([])
                    sensor_tree.bs_is_not_full = False
        schedules += [(schedule, len(schedule))]
    print(*schedules, sep='\n')
