import main
import numpy as np
from help_functions import draw_plot
from interactive_console import interactive_console

adjacency_matrix = interactive_console()

sensors_count = len(adjacency_matrix) - 1
frame = main.rasp_create(adjacency_matrix, balance=True)
frame_len = len(frame)

step = 1 / sensors_count / 10
probabilities = np.arange(0, 1 / frame_len, step, dtype=float)
probabilities = list(map(float, probabilities))
probabilities.append(0.124)
probabilities.append(0.126)

teor_buff, buffer_mean, buff_adapt, n_avg_exp = [], [], dict(), []
mean_time, mean_time_adapt, mean_time_teor = [], dict(), []

buf = 0
num_of_frames = 1000
for i, prob in enumerate(probabilities):

    # стандартный режим алгоритма
    buffer_mean.append(main.sens_graph_with_prob(adjacency_matrix, prb=prob, num_of_frames=num_of_frames))
    print(prob)
    # адаптивный режим алгоритма
    for adapt_frame in range(1, 8):

        if adapt_frame not in buff_adapt:
            buff_adapt[adapt_frame] = []
        if adapt_frame not in mean_time_adapt:
            mean_time_adapt[adapt_frame] = []

        buff_adapt[adapt_frame].append(main.sens_graph_with_prob(adjacency_matrix,
                                                                 prb=prob,
                                                                 num_of_frames=num_of_frames,
                                                                 adaptation=adapt_frame))
        try:
            mean_time_adapt[adapt_frame].append((buff_adapt[adapt_frame][i] / (prob * sensors_count)))
        except RuntimeWarning:
            mean_time_adapt[adapt_frame].append(0)
        except ZeroDivisionError:
            mean_time_adapt[adapt_frame].append(0)

        print(adapt_frame/10)

    # Теоретический расчет среднего количества сообщений в системе
    lmd = frame_len * prob
    q = 1 - prob

    mean_requests = (lmd * q + lmd * (1 - lmd)) / (2 * (1 - lmd))
    teor_buff.append(mean_requests * sensors_count)

    # "Работающий кодец"
    avg_buf = 0
    n_come = np.random.binomial(frame_len, prob, size=num_of_frames)
    for cn in range(num_of_frames):
        if buf == 0:
            buf += n_come[cn]
        else:
            buf += n_come[cn] - 1
        avg_buf += buf
    avg_buf /= num_of_frames
    n_avg_exp.append(avg_buf * sensors_count)

    try:
        if teor_buff:
            mean_time_teor.append(teor_buff[i] / (prob * sensors_count))
        if buffer_mean:
            mean_time.append(buffer_mean[i] / (prob * sensors_count))

    except RuntimeWarning:
        continue
    except ZeroDivisionError:
        continue

requests_for_plot = dict(x_axis=probabilities, y_type="log")
times_for_plot = requests_for_plot.copy()

if buffer_mean:
    requests_for_plot['Практический результат'] = buffer_mean

if teor_buff:
    requests_for_plot['Теоретический график'] = teor_buff

if n_avg_exp:
    requests_for_plot['"Работающий кодец" :D'] = n_avg_exp

if buff_adapt:
    for key in buff_adapt:
        requests_for_plot["{}".format(key)] = buff_adapt[key]

if mean_time_teor:
    times_for_plot['Среднее время теоретическое'] = mean_time_teor

if mean_time:
    times_for_plot['Среднее время'] = mean_time

if mean_time_adapt:
    for key in buff_adapt:
        times_for_plot["{}".format(key)] = mean_time_adapt[key]

draw_plot(title="Количество сообщений в системе",
          x_title="Вероятность появления сообщения в сенсоре",
          y_title="Среднее количество сообщений в системе",
          file_name="prob_fig.html",
          **requests_for_plot)

draw_plot(title="Среднее время пребывания сообщения в системе",
          x_title="Вероятность появления сообщения в сенсоре",
          y_title="Время",
          file_name="time_fig.html",
          **times_for_plot)
