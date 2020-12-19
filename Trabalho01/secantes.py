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
    output = open("./secantes_saída<%d>.txt" % i,"w") # Abre o arquivo de saída

    # Este e todos os outros output.write() vão escrever dados no arquivo de saída
    output.write("\n {:^15} {:^30} {:^30} {:^30} \n".format("k", "x_k", "f(x_k)", "e_k"))

    # Apenas três valores x_k serão armazenados por vez, o atual e os dois anteriores
    x = [a[i]+0.5, b[i], 0] # Neste caso, x_0 foi escolhido como a + 0.5 pois, do contrário, o algoritmo calcula a mesma raiz nas duas execuções

    # Índice auxiliar que será utilizado para acessar o valor atual de x
    j = 0 

    output.write(" {:^15} {: ^ 30.8f} {: ^ 30.8e} {: ^ 30.8e} \n".format("0", x[j], float(f(x[j])), float(abs(x[j] - sol[i]))))

    j = 1
    output.write(" {:^15} {: ^ 30.8f} {: ^ 30.8e} {: ^ 30.8e} \n".format("0", x[j], float(f(x[j])), float(abs(x[j] - sol[i]))))

    # Loop pelo processo de cálculo até que o número máximo de iterações sera atingido
    for k in range(2,MAXITER+2):
        j += 1 if j < 2 else -j # j = 0 --> j = 1 --> j = 2 --> j = 0 --> j = 1 ...

        x[j] = (f(x[j-1])*x[j-2] - f(x[j-2])*x[j-1])/(f(x[j-1]) - f(x[j-2])) # Valor do x atual

        e = abs(x[j] - sol[i]) # Erro em relação à raiz exata

        output.write(" {:^15} {: ^ 30.8f} {: ^ 30.8e} {: ^ 30.8e} \n".format(k, x[j], float(f(x[j])), float(e)))

        # Checa se uma aproximação satisfatória foi encontrada
        isGoodApprox = ( f(x[j]) == 0 ) or ( abs(x[j] - x[j-1]) < epsilon * max(1,abs(x[j])) )
        if isGoodApprox: break # Se sim, encerra o cálculo neste intervalo

    output.write("\n")
    output.close() # Fecha o arquivo de saída

    # Se sair do 'for', significa que chegou-se a uma aproximação satisfatória ou que o número máximo de iterações foi atingido
    if isGoodApprox: continue
    else: raise Exception("The maximum number of iterations was met and no root was found.")
