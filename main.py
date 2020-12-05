from statistics import mean

import matplotlib.pyplot as plt
from sympy.plotting import plot
from pandas import read_csv
from sympy import pi, pprint, Symbol
import numpy as np
from lsq import trigLSQ

rawData = read_csv('data/data.csv', header=0, names=['x', 'y'])
x = rawData['x']; y = rawData['y']

noMonths = len(rawData)
noYears = int(noMonths/12)

data60 = {
    'x': [(2*pi*k)/noMonths for k in range(1, noMonths+1)],
    'y': [p for p in y]
}

data12 = {
    'x': [(2*pi*k)/12 for k in range(1, 12+1)],
    'y': [mean([y[i + n*12] for n in range(noYears)]) for i in range(12)]
}

order60 = 11; order12 = 4
F60, aux60 = trigLSQ(data60, order60); F60 = F60.subs(Symbol('x'), (2*pi/noMonths)*Symbol('t'))
F12, aux12 = trigLSQ(data12, order12); F12 = F12.subs(Symbol('x'), (2*pi/12)*Symbol('t'))

f60 = lambda x: float(F60.subs(Symbol('t'), x).evalf())
f12 = lambda x: float(F12.subs(Symbol('t'), x).evalf())

x12 = np.linspace(0, 12, 100); y12 = 0
for j, i in aux12[0]: y12 += aux12[1][j][0] * (np.cos(i['index'] * 2*np.pi/12 * x12) if i['cos'] else np.sin(i['index'] * 2*np.pi/12 * x12))

x60 = np.linspace(0, noMonths, 100); y60 = 0
for j, i in aux60[0]: y60 += aux60[1][j][0] * (np.cos(i['index'] * 2*np.pi/noMonths * x60) if i['cos'] else np.sin(i['index'] * 2*np.pi/noMonths * x60))

with open('./output/60-month_period.out', 'w') as f:
    f.write(f't: {list(range(1, noMonths+1))}\n\n')
    f.write(f'x: {data60["x"]}\n\n')
    f.write(f'y: {data60["y"]}\n\n')
    f.write(f'F(t) = {F60}\n\n')
    f.write(f'F(72) = {f60(72)}')

with open('./output/12-month_period.out', 'w') as f:
    f.write(f't: {list(range(1, 12+1))}\n\n')
    f.write(f'x: {data12["x"]}\n\n')
    f.write(f'y: {data12["y"]}\n\n')
    f.write(f'F(t) = {F12}\n\n')
    f.write(f'F(72) = {f12(72)}')

print('\nFunção considerando período de 5 anos: \nF(t) = ')
pprint(F60)
print(f'\nF(72) = {f60(72)}', end='\n\n')

print('\nFunção considerando período de 1 ano médio: \nF(t) = ')
pprint(F12)
print(f'\nF(72) = {f12(72)}')

plt.figure(1)
plt.title('Sobreposição da função aproximada com os pontos resultantes da média entre 5 anos')
plt.scatter(range(1, 13), data12['y'], label='Pontos fornecidos')
plt.plot(range(1, 12+1), data12['y'], '--', label='Ligação entre os pontos')
plt.plot(x12, y12, '-', lw=2.5, label=f'Função aproximada F(t) (ordem {order12})')
plt.legend(loc='upper right')
plt.ylabel('Precipitação')
plt.xlabel('Mês (t)')
plt.gcf().set_size_inches(9,6)
plt.savefig('output/12-month_period.png', dpi=100)

plt.figure(2)
plt.title('Sobreposição da função aproximada com os pontos fornecidos')
plt.scatter(range(1, noMonths+1), data60['y'], label='Pontos fornecidos')
plt.plot(range(1, noMonths+1), data60['y'], '--', label='Ligação entre os pontos')
plt.plot(x60, y60, '-', lw=2.5, label=f'Função aproximada F(t) (ordem {order60})')
plt.legend(loc='upper left')
plt.ylabel('Precipitação')
plt.xlabel('Mês (t)')
plt.gcf().set_size_inches(9,6)
plt.savefig('output/60-month_period.png', dpi=100)
plt.show()