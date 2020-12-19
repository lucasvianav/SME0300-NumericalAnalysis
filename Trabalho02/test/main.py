from statistics import mean

import matplotlib.pyplot as plt
from sympy.plotting import plot
from pandas import read_csv
from sympy import pi, pprint, Symbol
from lsq import trigLSQ

rawData = read_csv('../data/data.csv', header=0, names=['x', 'y'])
x = rawData['x']; y = rawData['y']

noMonths = len(rawData)
noYears = int(noMonths/12)

data60 = {
    'x': [2*k*pi/noMonths for k in range(1, noMonths+1)],
    'y': [p for p in y]
}

data12 = {
    'x': [2*k*pi/12 for k in range(1, 12+1)],
    'y': [mean([y[i + n*12] for n in range(noYears)]) for i in range(12)]
}

F60 = trigLSQ(data60)
F12 = trigLSQ(data12)

with open('./output/60-month_period.out', 'w') as f:
    f.write('data:\n')
    f.write('x: ' + str(data60['x']) + '\n\n')
    f.write('y: ' + str(data60['y']) + '\n\n')
    f.write('F(x): ' + str(F60))

with open('./output/12-month_period.out', 'w') as f:
    f.write('data:\n')
    f.write('x: ' + str(data12['x']) + '\n\n')
    f.write('y: ' + str(data12['y']) + '\n\n')
    f.write('F(x): ' + str(F12))

# plt.plot(data60['x'], data60['y'], '--',)
# plt.ylabel('Precipitação')
# plt.xlabel('Meses * 2pi/60')
# plt.savefig('output/60-month_period.png')

plot(F60, (Symbol('x'), 0, 2*pi))
print(F60.subs(Symbol('x'), 2*72*pi/60).evalf())

# print('\nFunção considerando período de 5 anos:')
# pprint(F60)

# print('\nFunção considerando período de 1 ano médio:')
# pprint(F12)
# print()
