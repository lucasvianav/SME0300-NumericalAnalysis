# AUTORES:
# Ana Beatriz Popazoglo 9806892
# Lucas Viana Vilela 10748409
# Murilo Ramos Botto  9288561 

from sympy import * # Biblioteca para trabalhar com variáveis simbólicas
from sympy.abc import _clash1 # Reconhecimento de 'x' como uma variável na função sympify()
from statistics import mean # Função que calcula a média entre uma lista de valores

expr_f = sympify("21*x**4 - 11*x**3 + 19*x**2 - 11*x - 2") # Expressão de f(x)

# Intervalos: [a[0], b[0]] = [-1, 0] e [a[1], b[1]] = [0, 1]
a = [-1, 0]
b = [0, 1]

sol = [-1/7, 2/3] # Raízes exatas nos respectivos intervalos

epsilon = 10**-6 # Precisão
MAXITER = 10**3 # Máximo de iterações


def f(value: float): # f(x) = expr_f - Função que vai avaliar f(x) em um determinado ponto
    variable = sympify('x')
    return (expr_f.subs(variable,value)).evalf()



for i in range(2): # Loop que vai fazer os cálculos para ambos os intervalos
    output = open("./bissecção_saída<%d>.txt" % i,"w") # Abre o arquivo de saída

    # Este e todos os outros output.write() vão escrever dados no arquivo de saída
    output.write("\n {:^15} {:^30} {:^30} {:^30} {:^30} {:^30} \n".format("k", "a_k", "b_k", "x_k", "f(x_k)", "e_k"))

    # Checa se os extremos do intervalo são raízes
    if f(a[i]) == 0: 
        output.write(" {:^15} {: ^ 30.8f} {: ^ 30.8f} {: ^ 30.8f} {: ^ 30.8e} {: ^ 30.8e} \n".format("00", a[i], b[i], a[i], f(a[i]), abs(a[i] - sol[i])))
        continue # Se sim, encerra o cálculo neste intervalo
    elif f(b[i]) == 0: 
        output.write(" {:^15} {: ^ 30.8f} {: ^ 30.8f} {: ^ 30.8f} {: ^ 30.8e} {: ^ 30.8e} \n".format("00", a[i], b[i], b[i], f(b[i]), abs(b[i] - sol[i])))
        continue # Se sim, encerra o cálculo neste intervalo

    # Checa se é possível garantir que há pelo menos uma raiz no intervalo
    elif f(a[i]) * f(b[i]) > 0: raise Exception("Não se pode garantir que há uma raiz nesse intervalo.")

    output.write(" {:^15} {: ^ 30.8f} {: ^ 30.8f} {: ^ 30.8f} {: ^ 30.8e} {: ^ 30.8e} \n".format("00", a[i], b[i], a[i], f(a[i]), abs(a[i] - sol[i])))

    # Apenas dois valores x_k serão armazenados por vez, o atual e o anterior
    x = [a[i], 0]

    # Inicializa em 0 o índice auxiliar que será utilizado para acessar o valor atual de x
    j = 0 

    # Loop pelo processo de cálculo até que o número máximo de iterações sera atingido
    for k in range(1,MAXITER+1):
        j += 1 if j < 1 else -j # j = 0 --> j = 1 --> j = 0 --> j = 1 ...

        x[j] = mean([a[i],b[i]]) # Valor do x atual

        e = abs(x[j] - sol[i]) # Erro em relação à raiz exata

        output.write(" {:^15} {: ^ 30.8f} {: ^ 30.8f} {: ^ 30.8f} {: ^ 30.8e} {: ^ 30.8e} \n".format(str(k).zfill(2), a[i], b[i], x[j], f(x[j]), e))

        # Checa se uma aproximação satisfatória foi encontrada
        isGoodApprox = ( f(x[j]) == 0 ) or ( abs(x[j] - x[j-1]) < epsilon * max(1,abs(x[j])) )
        if isGoodApprox: break # Se sim, encerra o cálculo neste intervalo

        # Define um novo intervalo
        elif f(a[i]) * f(x[j]) < 0:
            b[i] = x[j]
        elif f(x[j]) * f(b[i]) < 0:
            a[i] = x[j]

    output.write("\n")
    output.close() # Fecha o arquivo de saída

    # Se sair do 'for', significa que chegou-se a uma aproximação satisfatória ou que o número máximo de iterações foi atingido
    if isGoodApprox: continue
    else: raise Exception("The maximum number of iterations was met and no root was found.")
