from graph_gen import graph_generator, tree_generator, grid_generator

def interactive_console():
    while True:
        try:
            method = int(input('''Выберите метод генерации
            1 - дерево;
            2 - решетка;
            3 - случайный граф
            4 - тестовый случай
            '''))
            if method in [1, 2, 3, 4]:
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
                elif method == 4:
                    adjacency_matrix = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
                break
            else:
                raise ValueError
        except ValueError:
            print('Вы ввели некоректное число, попробуйте снова!')
    return adjacency_matrix