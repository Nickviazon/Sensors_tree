import graph_gen
import main  # Фундовой
import Rodeo3.foreach as foreach # Яковлев
import Rodeo3.Rasp as Rasp # Богданов
import Rodeo3.PiluginAndHabibulin as PiluginAndHabibulin
import plotly
import plotly.graph_objs as go
import timeit


def wat_time(func):
    a = timeit.default_timer()
    func
    return timeit.default_timer() - a

n = 10
faces = 5

Rezault_Matr = [[0] * (n+1) for i in range(faces)]

for i, sens_num in enumerate(range(n, (n+1)*10, n)):  # Количество сенсоров (деленное на 10)
    for j in range(10):  # 10 раз генерируем дерево с одинковым количеством сенсоров

        input_tree = graph_gen.graph_generator(sens_num)

        Rezault_Matr[0][i] += wat_time(main.rasp_create(input_tree, True)) * 10 ** 6

        Rezault_Matr[1][i] += wat_time(foreach.circle(input_tree)) * 10 ** 6

        Rezault_Matr[2][i] += wat_time(Rasp.rasp(input_tree)) * 10 ** 6

        Rezault_Matr[3][i] += wat_time(PiluginAndHabibulin.PiluginAndHabibulin(input_tree)) * 10 ** 6

        Rezault_Matr[4][i] += wat_time(main.rasp_create(input_tree)) * 10 ** 6

        print(i, j)

for i in range(faces):
    for j, elem in enumerate(range(n, (n+1)*10, n)):
        Rezault_Matr[i][j] /= 10

x = list(range(n, (n+1)*10, n))

alg_names = ['Фундовой - Сергеев', 'Яковлев - Лотоцкий',
             'Богданов - Иванова', 'Пилюгин - Хабибулин',
             'Ф-С без балансировки']

data = []
for i, result in enumerate(Rezault_Matr):
    data.append(go.Scatter(
        x=x,
        y=result,
        name=alg_names[i]
        )
    )
layout = go.Layout(title=u"График зависимости времени выполнения алгоритма от количества сенсоров в сети",
                   xaxis=dict(title=u"Количество сенсоров в сети"),
                   yaxis=dict(title=u"Время")
                   )

plot = dict(data=data, layout=layout)

plotly.offline.plot(plot, filename='time.html')
