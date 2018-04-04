import main
import plotly
import plotly.graph_objs as go
import numpy as np
from interactive_console import interactive_console


def draw_plot(title, x_title, y_title, **plot_data):
    if "x_axis" not in plot_data or not data_for_plot["x_axis"]:
        raise KeyError("Dictionary haven't '{0}' key or '{0}' have unexpected value".format("x_axis") )

    data = [
            go.Scatter(x=plot_data["x_axis"], y=plot_data[name], name=name)
            for name in plot_data if name != "x_axis"
    ]

    layout = go.Layout(title=u"{}".format(title),
                       xaxis=dict(title=u"".format(x_title)),
                       yaxis=dict(title=u"".format(y_title)),)

    plot = dict(data=data, layout=layout)
    plotly.offline.plot(plot, filename='prob.html')


adjacency_matrix = interactive_console()

sensors_count = len(adjacency_matrix)-1
frame = main.rasp_create(adjacency_matrix, balance=True)
frame_len = len(frame)


step = 1/sensors_count/10
probabilities = np.arange(0, 1 / frame_len, step, dtype=float)
probabilities = list(map(float, probabilities))
probabilities.append(0.124)
probabilities.append(0.126)


teor_buff, buffer_mean, buff_adapt, n_avg_exp = [], [], [], []
mean_time = []
mean_time_adapt = []

buf = 0
num_of_frames = 1000
for i, prob in enumerate(probabilities):

    # стандартный режим алгоритма
    buffer_mean.append(main.sens_graph_with_prob(adjacency_matrix, prb=prob, num_of_frames=num_of_frames))

    # адаптивный режим алгоритма
    buff_adapt.append(main.sens_graph_with_prob(adjacency_matrix, prb=prob, num_of_frames=num_of_frames, adaptation=True))
    print(prob)

    # Теоретический расчет среднего количества сообщений в системе
    lmd = frame_len * prob
    q = 1-prob

    mean_requests = (lmd*q+lmd*(1-lmd))/(2*(1-lmd))
    teor_buff.append(mean_requests*sensors_count)

    # "Работающий кодец"
    avg_buf = 0
    n_come = np.random.binomial(frame_len, prob, size=num_of_frames)
    for cn in range(num_of_frames):
        if buf == 0:
            buf += n_come[cn]
        else:
            buf += n_come[cn]-1
        avg_buf += buf
    avg_buf /= num_of_frames
    n_avg_exp.append(avg_buf*sensors_count)

    try:
        if buffer_mean:
            mean_time.append(buffer_mean[i]/(prob*sensors_count))
        if buff_adapt:
            mean_time_adapt.append(buff_adapt[i]/(prob*sensors_count))
    except RuntimeWarning:
        continue


data_for_plot = dict(x_axis=probabilities)

if buffer_mean:
    data_for_plot['Практический результат'] = buffer_mean

if teor_buff:
    data_for_plot['Теоретический график'] = teor_buff

if n_avg_exp:
    data_for_plot['"Работающий кодец" :D'] = n_avg_exp

if buff_adapt:
    data_for_plot['Адаптированный'] = buff_adapt

if mean_time:
    data_for_plot['Среднее время'] = mean_time

if mean_time_adapt:
    data_for_plot['Среднее время адаптированное'] = mean_time_adapt

draw_plot(title="Количество сообщений в системе от вероятности появления сообщения в сенсоре",
          x_title="Вероятность появления сообщения в сенсоре во время выполнения слота",
          y_title="Среднее количество сообщений в системе",
          **data_for_plot)

