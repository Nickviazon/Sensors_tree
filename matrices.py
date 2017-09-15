from tree_gen import tree_generator

while True:
    try:
        N = int(input('Введите число сенсоров в сети: '))
        break
    except ValueError:
        print('Вы ввели некоректное число, попробуйте снова!')

adjacency_matrix = tree_generator(N)
