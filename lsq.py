import numpy as np
import sympy as sp

# (index: int, cos: bool)
# 0 1 1 2 2 3 3 4 4 5 5 ...
# {0, cos}, {1, cos}, {1, sen}, {2, cos}, {2, sen}, ...
alternatingRange = lambda m : [{'index': j, 'cos': True if k == 0 else False} for j in range(m + 1) for k in range(2 if j != 0 else 1)]

# data: "dict"
# data = {'x': [x-points], 'y': [y-points]}
def trigLSQ(data):
    noPoints = len(data['x']) # N
    order = int(noPoints/2) if int(noPoints/2) < noPoints/2 else int(noPoints/2)-1 # m

    c = lambda a : np.array([np.cos(a * float(data['x'][i])) for i in range(noPoints)])
    s = lambda a : np.array([np.sin(a * float(data['x'][i])) for i in range(noPoints)])

    y = np.array([p for p in data['y']])

    # diagMatrix * sol = res

    diagMatrix = np.array(
        [[(noPoints/(1 if j == 0 else 2) if i == j else 0) for i in range(2*order + 1)] for j in range(2*order + 1)]
    )
    res = [[np.dot(y, c(i['index']) if i['cos'] else s(i['index']))] for i in alternatingRange(order)]
    sol = np.linalg.solve(diagMatrix, res)

    # F is the function approximation
    F = 0
    for j, i in enumerate(alternatingRange(order)): F += sol[j][0] * sp.sympify(('cos(' if i['cos'] else 'sin(') + str(i['index']) + ' * x)')

    return F

# x = 2kpi/N --> k = xN/2pi