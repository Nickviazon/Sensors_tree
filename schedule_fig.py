import graph_gen
import main
import plotly
import plotly.graph_objs as go

# Фундовой - Сергеев
n = 10
Fundovoy = [0] * n
FundovoyValid = [True] * n

x = list(range(n, (n+1)*10, n))

percent = 0
for j, KolSens in enumerate(range(n, (n+1)*10, n)):
    for i in range(10):
        root = graph_gen.graph_generator(KolSens)
        resault = main.rasp_create(root, balance=True)
        Fundovoy[j] += len(resault)
        percent += 1/(10*len(x))
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
