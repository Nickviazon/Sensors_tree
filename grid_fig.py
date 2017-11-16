import graph_gen
import main
import plotly
import plotly.graph_objs as go
import validate

# Фундовой - Сергеев
n = 19
Fundovoy = [0] * n
FundovoyValid = [True] * n
without_balance = [0] * n
without_balance_Valid = [True] * n

# x = list(range(3, n+1, 2))
x = [i**2 for i in range(3, n+1, 2)]

percent = 0
for j, KolSens in enumerate(range(3, n+1, 2)):
    for i in range(10):
        root = graph_gen.grid_generator(KolSens)
        result = main.rasp_create(root, balance=True)
        if not validate.validateFunc(root, result):
            FundovoyValid[j] = False
        Fundovoy[j] += len(result)
        percent += 1/(10*len(x)*2)
        print('{:.2%}, Fundovoy'.format(percent))

        result = main.rasp_create(root)
        if not validate.validateFunc(root, result):
            without_balance_Valid[j] = False
        without_balance[j] += len(result)
        percent += 1/(10*len(x)*2)
        print('{:.2%}, without balance'.format(percent))

for i in range(len(Fundovoy)):
    Fundovoy[i] = Fundovoy[i] / 10
    without_balance[i] /= 10


print('Закончили')

data = []
if all(FundovoyValid):
    trace1 = go.Scatter(
        x=x,
        y=Fundovoy,
        name='С балансировкой'
    )
    data.append(trace1)
if all(without_balance_Valid):
        trace2 = go.Scatter(
            x=x,
            y=without_balance,
            name='Без балансировки'
        )
        data.append(trace2)

layout = go.Layout(title=u"График зависимости длины расписания от количества сенсоров в сети",
                   xaxis=dict(title=u"Количество сенсоров в сети"),
                   yaxis=dict(title=u"Длина распсания")
                   )

plot = dict(data=data, layout=layout)

plotly.offline.plot(plot, filename='grid.html')
