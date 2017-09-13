# c = [[0, 1, 0, 0, 0, 1],
#      [1, 0, 1, 1, 0, 0],
#      [0, 1, 0, 0, 1, 0],
#      [0, 1, 0, 0, 0, 0],
#      [0, 0, 1, 0, 0, 0],
#      [1, 0, 0, 0, 0, 0]]

adjacency_matrices = [

    [[1, 1, 0, 0, 0],
     [1, 1, 1, 0, 0],
     [0, 1, 1, 1, 0],
     [0, 0, 1, 1, 1],
     [0, 0, 0, 1, 1]],


    [[1, 1, 0, 0, 0, 0],
     [1, 1, 1, 0, 0, 0],
     [0, 1, 1, 1, 0, 0],
     [0, 0, 1, 1, 1, 0],
     [0, 0, 0, 1, 1, 1],
     [0, 0, 0, 0, 1, 1]],

    [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]],

    
    [[1, 1, 0, 0, 0, 0],
     [1, 1, 1, 1, 0, 1],
     [0, 1, 1, 0, 0, 0],
     [0, 1, 0, 1, 1, 0],
     [0, 0, 0, 1, 1, 0],
     [0, 1, 0, 0, 0, 1]],

    [[1, 1, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 0, 0, 1, 0, 0, 0],
     [0, 1, 1, 1, 1, 0, 0, 0, 0],
     [0, 0, 1, 1, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 1, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 1, 1, 1, 0],
     [0, 0, 0, 0, 0, 1, 1, 0, 0],
     [0, 0, 0, 0, 0, 1, 0, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 1, 1]],

    [[1, 1, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 0, 0, 0, 1],
     [0, 1, 1, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 1, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 1, 1, 1, 1, 0],
     [0, 0, 0, 0, 1, 1, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 1, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 1, 0],
     [0, 1, 0, 0, 0, 0, 0, 0, 1]],

#    [[1, 1, 0, 0, 0, 1],
#     [1, 1, 1, 1, 0, 0],
#     [0, 1, 1, 0, 1, 0],
#     [0, 1, 0, 1, 0, 0],
#     [0, 0, 1, 0, 1, 0],
#     [1, 0, 0, 0, 0, 1]],
    
    [[1, 1, 0, 0, 0, 1],
     [1, 1, 1, 1, 0, 0],
     [0, 1, 1, 0, 1, 0],
     [0, 1, 0, 1, 0, 0],
     [0, 0, 1, 0, 1, 0],
     [1, 0, 0, 0, 0, 1]],

    [[1, 1, 0, 0, 0, 1, 0, 0, 0],
     [1, 1, 1, 1, 0, 0, 0, 0, 0],
     [0, 1, 1, 0, 1, 0, 0, 0, 0],
     [0, 1, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 1, 1, 1, 0],
     [0, 0, 0, 0, 0, 1, 1, 0, 0],
     [0, 0, 0, 0, 0, 1, 0, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 1, 1]],

    [[1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]],

]
