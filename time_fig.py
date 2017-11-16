import graph_gen
import main  # Фундовой
import plotly
import plotly.graph_objs as go
import timeit


def wat_time(func):
    a = timeit.default_timer()
    func
    return timeit.default_timer() - a


Rezault_Matr = [0] * 11

for i in range(1, 11):  # Количество сенсоров (деленное на 10)
    for j in range(10):  # 10 раз генерируем дерево с одинковым количеством сенсоров

        input_tree = graph_gen.graph_generator(i * 10)

        Rezault_Matr[i] += wat_time(main.rasp_create(input_tree)) * 10 ** 6
        print(i, j)

for i in range(1, 11):
    Rezault_Matr[i] /= 10

x = list(range(10, 110, 10))

alg_names = ['Фундовой - Сергеев']

data = go.Scatter(x=x, y=Rezault_Matr, name=alg_names[1])


layout = go.Layout(title=u"График зависимости времени выполнения алгоритма от количества сенсоров в сети",
                   xaxis=dict(title=u"Количество сенсоров в сети"),
                   yaxis=dict(title=u"Время")
                   )

plot = dict(data=data, layout=layout)

plotly.offline.plot(plot, filename='time.html')
