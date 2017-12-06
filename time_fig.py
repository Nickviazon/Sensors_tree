import graph_gen
import main  # Фундовой
import plotly
import plotly.graph_objs as go

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

prob = 0.2
buffer_mean = main.sens_graph_with_prob(adjacency_matrix,
                                        schedule1,
                                        prb=prob)

data = []
trace1 = go.Scatter(
    x=[i for i in range(1, 1001)],
    y=buffer_mean,
 )
data.append(trace1)

layout = go.Layout(title=u"График зависимости количества сообщений в системе сенсорном буфере от вероятности",
                   xaxis=dict(title=u"Номер фрейма"),
                   yaxis=dict(title=u"сообщений в буфере первого сенсора")
                   )

plot = dict(data=data, layout=layout)

plotly.offline.plot(plot, filename='frame.html')
