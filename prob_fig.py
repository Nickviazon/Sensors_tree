import main
import numpy as np
from help_functions import draw_plot, key_init
from interactive_console import interactive_console


def avg_messages_calc(p, len_frame, sens_count):
    
    lmd = len_frame * p
    q = 1 - p
    mean_requests = (lmd * q + lmd * (1 - lmd)) / (2 * (1 - lmd))
    return mean_requests * sens_count
    

if __name__ == "__main__":

    adjacency_matrix = interactive_console()

    sensors_count = len(adjacency_matrix) - 1
    frame = main.rasp_create(adjacency_matrix, balance=True)
    frame_len = len(frame)

    num_of_points = 15
    step = 1 / sensors_count / num_of_points
    probabilities = np.arange(0, 1 / frame_len+step, step, dtype=float)
    probabilities = list(map(float, probabilities))
    probabilities.insert(1, step/2)
    probabilities.insert(1, step/2/2)
    prob_for_teor = list(map(float, np.arange(0, 1 / frame_len, 1 / sensors_count / 1000, dtype=float)))

    teor_buff, buffer_mean, buff_adapt, n_avg_exp = [], [], dict(), []
    mean_time, mean_time_adapt, mean_time_teor = [], dict(), []

    overflow_point = {"": dict(value=[])}
    adaptation_frames = [2**i for i in [0, 1, 2, 3]]
    checked = [False] * len(adaptation_frames)
    adaptation_skip = []

    buf = 0
    num_of_frames = 1000

    # Теоретический расчет среднего количества сообщений в системе
    for i, prob in enumerate(prob_for_teor):
        if prob < 1 / sensors_count:
            teor_buff.append(avg_messages_calc(prob, frame_len, sensors_count))
            try:
                mean_time_teor.append(teor_buff[i] / (prob * sensors_count))
            except ZeroDivisionError:
                mean_time_teor.append(0)

    for i, prob in enumerate(probabilities):

        # стандартный режим алгоритма
        buffer_mean.append(main.sens_graph_with_prob(adjacency_matrix, prb=prob, num_of_frames=num_of_frames))
        print(prob)

        # адаптивный режим алгоритма
        for j, adapt_frame in enumerate(adaptation_frames):
            key_init(buff_adapt, adapt_frame, [])
            key_init(mean_time_adapt, adapt_frame, [])
            if adapt_frame not in adaptation_skip:
                mean_reqests_adapt = main.sens_graph_with_prob(adjacency_matrix,
                                                               prb=prob,
                                                               num_of_frames=num_of_frames,
                                                               adaptation=adapt_frame)

                if mean_reqests_adapt > 200:
                    adaptation_skip.append(adapt_frame)
                else:
                    buff_adapt[adapt_frame].append(mean_reqests_adapt)

                try:
                    mean_time_adapt[adapt_frame].append((buff_adapt[adapt_frame][i] / (prob * sensors_count)))
                except RuntimeWarning:
                    mean_time_adapt[adapt_frame].append(0)
                except ZeroDivisionError:
                    mean_time_adapt[adapt_frame].append(0)
                except IndexError:
                    pass


                try:
                    if (prob < 1 / sensors_count and
                            buff_adapt[adapt_frame][i] > avg_messages_calc(prob, frame_len, sensors_count) and
                            i > 0 and not checked[j]):
                        overflow_point[""]["value"].append(prob)
                        checked[j] = True
                except IndexError:
                    pass

                print(adapt_frame/10)

        try:
            if buffer_mean:
                mean_time.append(buffer_mean[i] / (prob * sensors_count))

        except RuntimeWarning:
            continue
        except ZeroDivisionError:
            pass
        except IndexError:
            pass

    requests_for_plot = dict(y_type="log")
    times_for_plot = dict(y_type="log")

    if buffer_mean:
        requests_for_plot['Не адаптивный'] = dict()
        requests_for_plot['Не адаптивный']['value'] = buffer_mean
        requests_for_plot['Не адаптивный']['x_axis'] = probabilities

    if teor_buff:
        requests_for_plot['Теоретический график'] = dict()
        requests_for_plot['Теоретический график']['value'] = teor_buff
        requests_for_plot['Теоретический график']['x_axis'] = prob_for_teor

    if n_avg_exp:

        requests_for_plot['"Работающий кодец" :D'] = dict()
        requests_for_plot['"Работающий кодец" :D']['value'] = n_avg_exp
        requests_for_plot['"Работающий кодец" :D']['x_axis'] = probabilities

    if buff_adapt:
        for key in buff_adapt:
            requests_for_plot["{}".format(key)] = dict()
            requests_for_plot["{}".format(key)]['value'] = buff_adapt[key]
            requests_for_plot["{}".format(key)]["x_axis"] = probabilities

    if mean_time_teor:
        times_for_plot['Среднее время теоретическое'] = dict()
        times_for_plot['Среднее время теоретическое']['value'] = mean_time_teor
        times_for_plot['Среднее время теоретическое']["x_axis"] = prob_for_teor

    if mean_time:
        times_for_plot['Среднее время'] = dict()
        times_for_plot['Среднее время']['value'] = mean_time
        times_for_plot['Среднее время']['x_axis'] = probabilities

    if mean_time_adapt:
        for key in buff_adapt:
            times_for_plot["{}".format(key)] = dict()
            times_for_plot["{}".format(key)]['value'] = mean_time_adapt[key]
            times_for_plot["{}".format(key)]["x_axis"] = probabilities

    if overflow_point:
        # key_init(overflow_point, key="x_axis", data=adaptation_frames)
        overflow_point[""]["value"] = [1/sensors_count, 0.0938, 0.03898, 0.0108]

        # overflow_point[""]["value"] = list(reversed(overflow_point[""]["value"]))
        # overflow_point[""]["x_axis"] = adaptation_frames

    draw_plot(title="Среднее количество сообщений в системе",
              x_title="Вероятность появления сообщения в сенсоре, p",
              y_title="Количество сообщений в системе, Q",
              file_name="prob_fig.html",
              save_image=True,
              **requests_for_plot)

    draw_plot(title="Среднее время пребывания сообщения в системе",
              x_title="Вероятность появления сообщения в сенсоре",
              y_title="Время",
              file_name="time_fig.html",
              save_image=True,
              **times_for_plot)

    draw_plot(title="Значение точки переполнения от порядка адаптации",
              x_title="Номер фрейма",
              y_title="Вероятность возникновения сообщения, p",
              file_name="overflow.html",
              save_image=True,
              **overflow_point)
