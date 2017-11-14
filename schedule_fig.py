import graph_gen
import main
import plotly
import plotly.graph_objs as go

# Фундовой - Сергеев
Fundovoy = [0] * 10
FundovoyValid = [True] * 10

x = list(range(10, 110, 10))

percent = 0
for KolSens in range(1, 11):
    for i in range(10):
        root = graph_gen.graph_generator(KolSens * 10)
        resault = main.rasp_create(root, balance=True)
        Fundovoy[KolSens - 1] += len(resault)
        percent += 0.01
        print('{:.2%}, Fundovoy'.format(percent))

for i in range(len(Fundovoy)):
    Fundovoy[i] = Fundovoy[i] / 10


print('Закончили')

data = []
if all(FundovoyValid):
    trace1 = go.Scatter(
        x=x,
        y=Fundovoy,
        name='Фундовой - Сергеев'
    )
    data.append(trace1)

layout = go.Layout(title=u"График зависимости длины расписания от количества сенсоров в сети",
                   xaxis=dict(title=u"Количество сенсоров в сети"),
                   yaxis=dict(title=u"Длина распсания")
                   )

plot = dict(data=data, layout=layout)

plotly.offline.plot(plot, filename='schedule.html')
