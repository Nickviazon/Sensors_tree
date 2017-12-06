import main
import plotly
import plotly.graph_objs as go
import numpy as np
from help_functions import frange

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

schedule1 = main.rasp_create(adjacency_matrix, balance=True)

buffer_mean = []
# num_of_exp =
probabilities = list(np.arange(0, 1/(len(adjacency_matrix)-1)+0.001, 0.0005, dtype=float))
probabilities = list(map(float, probabilities))
frame_num = 1000

for prob in probabilities:
    buffer_mean.append(main.sens_graph_with_prob(adjacency_matrix,
                                         schedule1,
                                         prb=prob))
    # buffer_mean.append(acc / frame_num)
    # buffer_mean.append(acc)

data = []
trace1 = go.Scatter(
    x=probabilities,
    y=buffer_mean,
    name='С балансировкой'
 )
data.append(trace1)


layout = go.Layout(title=u"График зависимости количества сообщений в системе сенсорном буфере от вероятности",
                   xaxis=dict(title=u"Вероятность появления сообщения в сенсоре во время выполнения слота"),
                   yaxis=dict(title=u"Среднее количество сообщений в системе")
                   )

plot = dict(data=data, layout=layout)

plotly.offline.plot(plot, filename='prob.html')
