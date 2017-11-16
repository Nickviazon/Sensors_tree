import graph_gen
import main
import Rodeo3.foreach as foreach
import Rodeo3.Rasp
import Rodeo3.PiluginAndHabibulin as PiluginAndHabibulin
import plotly
import plotly.graph_objs as go
import validate


# Фундовой - Сергеев
n = 10
faces = 5
Fundovoy = [0] * n
FundovoyValid = [True] * n

fun_not_balance = [0] * n
not_balance_valid = [True] * n

#Яковлев -Лотоцкий
Yakovlev = [0] * n
YakovlevValid = [True] * n
#Богданов - Иванова
Bogdanov = [0] * n
BogdanovValid = [True] * n

Pilugin = [0] * n
PiluginValid = [True] * n

x = list(range(n, (n+1)*10, n))

percent = 0
for j, KolSens in enumerate(range(n, (n+1)*10, n)):
    for i in range(10):

        root = graph_gen.graph_generator(KolSens)

        result = main.rasp_create(root, balance=True)
        if not validate.validateFunc(root, result):
            FundovoyValid[j] = False
        Fundovoy[j] += len(result)
        percent += 1/(10*len(x)*faces)
        print('{:.2%}, Fundovoy'.format(percent))

        result = main.rasp_create(root)
        if not validate.validateFunc(root, result):
            not_balance_valid[j] = False
        fun_not_balance[j] += len(result)
        percent += 1/(10*len(x)*faces)
        print('{:.2%}, Fundovoy without balance'.format(percent))

        result = foreach.circle(root)
        if not validate.validateFunc(root, result):
            YakovlevValid[j] = False
        Yakovlev[j] += len(result)
        percent += 1/(10*len(x)*faces)
        print('{:.2%}, Yakovlev'.format(percent))

        result = Rodeo3.Rasp.rasp(root)
        if not validate.validateFunc(root, result):
            BogdanovValid[j] = False
        Bogdanov[j] += len(result)
        percent += 1/(10*len(x)*4)
        print('{:.2%}, Bogdanov'.format(percent))

        result = PiluginAndHabibulin.PiluginAndHabibulin(root)
        if not validate.validateFunc(root, result):
            PiluginValid[j] = False
        Pilugin[j] += len(result)
        percent += 1/(10*len(x)*faces)
        print('{:.2%}, Pilugin'.format(percent))

for i in range(len(Fundovoy)):
    Fundovoy[i] = Fundovoy[i]/10
    fun_not_balance[i] = fun_not_balance[i]/10
    Yakovlev[i] = Yakovlev[i]/10
    Bogdanov[i] = Bogdanov[i]/10
    Pilugin[i] = Pilugin[i]/10



print('Закончили')

data = []
if all(FundovoyValid):
    trace0 = go.Scatter(
        x=x,
        y=Fundovoy,
        name='Фундовой - Сергеев'
    )
    data.append(trace0)

if all(YakovlevValid):
    trace1 = go.Scatter(
        x=x,
        y=Yakovlev,
        name='Яковлев - Лотоцкий'
    )
    data.append(trace1)

if all(BogdanovValid):
    trace2 = go.Scatter(
        x=x,
        y=Bogdanov,
        name='Богданов - Иванова'
    )
    data.append(trace2)

if all(PiluginValid):
    trace3 = go.Scatter(
        x=x,
        y=Pilugin,
        name='Пилюгин - Хабибулин'
    )
    data.append(trace3)

if all(not_balance_valid):
    trace4 = go.Scatter(
        x=x,
        y=fun_not_balance,
        name='Ф - С без балансировки'
    )
    data.append(trace4)

layout = go.Layout(title=u"График зависимости длины расписания от количества сенсоров в сети",
                   xaxis=dict(title=u"Количество сенсоров в сети"),
                   yaxis=dict(title=u"Длина распсания")
                   )

plot = dict(data=data, layout=layout)

plotly.offline.plot(plot, filename='schedule2.html')
