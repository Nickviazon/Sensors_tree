import main
import plotly
import plotly.graph_objs as go
import numpy as np

from graph_gen import graph_generator, tree_generator, grid_generator

while True:
    try:
        method = int(input('''Выберите метод генерации
        1 - дерево;
        2 - решетка;
        3 - случайный граф

        '''))
        if method in [1, 2, 3]:
            if method == 1:
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

schedule = main.rasp_create(adjacency_matrix, balance=True)


step = 1/(len(adjacency_matrix)-1)/100
probabilities = np.arange(0, 1/(len(adjacency_matrix)-1)+step, step, dtype=float)
probabilities = list(map(float, probabilities))
buffer_mean = [main.sens_graph_with_prob(adjacency_matrix, schedule, prb=prob) for prob in probabilities]

teor_buff = []
n = len(schedule)
for prob in probabilities:

    lmd = n*prob
    if lmd == 1:
        lmd = 0.99
    teor_buff.append((lmd*(1-prob)+lmd*(1-lmd))/(2*(1-lmd)))

data = []

trace1 = go.Scatter(
    x=probabilities,
    y=buffer_mean,
    )

data.append(trace1)

if teor_buff:
    trace2 = go.Scatter(
        x=probabilities,
        y=teor_buff,
        )
    data.append(trace2)

layout = go.Layout(title=u"Количество сообщений в системе от вероятности появления сообщения в сенсоре",
                   xaxis=dict(title=u"Вероятность появления сообщения в сенсоре во время выполнения слота"),
                   yaxis=dict(title=u"Среднее количество сообщений в системе")
                   )

plot = dict(data=data, layout=layout)

plotly.offline.plot(plot, filename='prob.html')
