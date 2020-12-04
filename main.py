from statistics import mean

import matplotlib.pyplot as plt
from sympy.plotting import plot
from pandas import read_csv
from sympy import pi, pprint, Symbol
from lsq import trigLSQ

rawData = read_csv('data/data.csv', header=0, names=['x', 'y'])
x = rawData['x']; y = rawData['y']

noMonths = len(rawData)
noYears = int(noMonths/12)

data60 = {
    'x': [noMonths*k/(2*pi) for k in range(1, noMonths+1)],
    'y': [p for p in y]
}

data12 = {
    'x': [12*k/(2*pi) for k in range(1, 12+1)],
    'y': [mean([y[i + n*12] for n in range(noYears)]) for i in range(12)]
}

F60 = trigLSQ(data60).subs(Symbol('x'), (2*pi/noMonths)*Symbol('t'))
F12 = trigLSQ(data12).subs(Symbol('x'), (2*pi/12)*Symbol('t'))

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

# plt.plot(rawData['x'], rawData['y'], '--')
# plt.scatter(rawData['x'], rawData['y'])
# plt.ylabel('Precipitação')
# plt.xlabel('Meses')
# plt.show()
# plt.cla()

# plt.plot(data60['x'], data60['y'], '--')
# plt.scatter(data60['x'], data60['y'])
# plt.scatter(data60['x'], data60['y'])
# plt.ylabel('Precipitação')
# plt.xlabel('Meses * 2pi/60')
# plt.savefig('output/60-month_period.png')

plot(F60, (Symbol('t'), 0, 60))
plot(F60, (Symbol('t'), 0, 12))
print(F60.subs(Symbol('t'), 72).evalf())

plot(F12, (Symbol('t'), 0, 12))
plot(F12, (Symbol('t'), 0, 60))
print(F12.subs(Symbol('t'), 72).evalf())

# print('\nFunção considerando período de 5 anos:')
# pprint(F60)

# print('\nFunção considerando período de 1 ano médio:')
# pprint(F12)
# print()
