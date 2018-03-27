import main
import plotly
import plotly.graph_objs as go
import numpy as np
from interactive_console import interactive_console

adjacency_matrix = interactive_console()

frame = main.rasp_create(adjacency_matrix, balance=True)
len_frame = len(frame)


step = 1/(len(adjacency_matrix)-1)/10
probabilities = np.arange(0, 1/len_frame, step, dtype=float)
probabilities = list(map(float, probabilities))
probabilities.append(0.124)
probabilities.append(0.126)
# probabilities.append(0.128)
# probabilities.append(0.13)

# probabilities.append(0.123)
# probabilities.append(0.5)

# probabilities = [0.5]

teor_buff, buffer_avg, n_avg_exp, buff_adapt = [], [], [], []
buf = 0
num_of_frames = 1000
for prob in probabilities:

    # стандартный режим алгоритма
    # buffer_avg.append(main.sens_graph_with_prob(adjacency_matrix, prb=prob, num_of_frames=num_of_frames))

    # адаптивный режим алгоритма
    buff_adapt.append(main.sens_graph_with_prob(adjacency_matrix, prb=prob, num_of_frames=num_of_frames, adaptation=True))
    print(prob)

    # Теоретический расчет среднего количества сообщений в системе
    lmd = len_frame*prob
    q = 1-prob

    mean_requests = (lmd*q+lmd*(1-lmd))/(2*(1-lmd))
    teor_buff.append(mean_requests*(len(adjacency_matrix)-1))

    # "Работающий кодец"
    avg_buf = 0
    n_come = np.random.binomial(len_frame, prob, size=num_of_frames)
    for cn in range(num_of_frames):
        if buf == 0:
            buf += n_come[cn]
        else:
            buf += n_come[cn]-1
        avg_buf += buf
    avg_buf /= num_of_frames
    n_avg_exp.append(avg_buf*(len(adjacency_matrix)-1))

data = []

if buffer_avg:
    trace1 = go.Scatter(
        x=probabilities,
        y=buffer_avg,
        name='Практический результат'

        )
    data.append(trace1)

if teor_buff:
    trace2 = go.Scatter(
        x=probabilities,
        y=teor_buff,
        name='Теоретический график'
        )
    data.append(trace2)

if n_avg_exp:
    trace3 = go.Scatter(
        x=probabilities,
        y=n_avg_exp,
        name='"Работающий кодец" :D'
        )
    data.append(trace3)

if buff_adapt:
    trace4 = go.Scatter(
        x=probabilities,
        y=buff_adapt,
        name='Адаптированный'
    )
    data.append(trace4)

layout = go.Layout(title=u"Количество сообщений в системе от вероятности появления сообщения в сенсоре",
                   xaxis=dict(title=u"Вероятность появления сообщения в сенсоре во время выполнения слота"),
                   yaxis=dict(title=u"Среднее количество сообщений в системе")
                   )

plot = dict(data=data, layout=layout)

plotly.offline.plot(plot, filename='prob.html')
