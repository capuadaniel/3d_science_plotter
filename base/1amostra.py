import math

import numpy as np

import tabelas

def combinations(iterable, r):
    # Copiado do itertools
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def alfaconvert(alfa, tabela):
    tabela = str(tabela.upper())
    if tabela == 'A':
        # traduz o valor de significancia alfa para um inteiro utilizavel para a tabela A
        if alfa == 0.990:
            return 1
        elif alfa == 0.950:
            return 2
        elif alfa == 0.500:
            return 3
        elif alfa == 0.100:
            return 4
        elif alfa == 0.050:
            return 5
        elif alfa == 0.025:
            return 6
        elif alfa == 0.010:
            return 7
        elif alfa == 0.001:
            return 8

        else:
            print('Alpha Error, escolha 0.001, 0.01, 0.025, 0.05, 0.10, 0.5, 0.95 ou 0.90')

    elif tabela.upper() == 'C':
        # traduz o valor de significancia alfa para um inteiro utilizavel para a tabela C

        if alfa == 0.10:
            return 1
        elif alfa == 0.05:
            return 2
        elif alfa == 0.025:
            return 3
        elif alfa == 0.01:
            return 4
        elif alfa == 0.001:
            return 5
        else:
            print('Alpha Error, escolha 0.001, 0.01, 0.025, 0.05 ou 0.10')

    elif tabela.upper() == 'F':
        # traduz o valor de significancia alfa para um inteiro utilizavel para a tabela C

        if alfa == 0.20:
            return 1
        elif alfa == 0.15:
            return 2
        elif alfa == 0.10:
            return 3
        elif alfa == 0.05:
            return 4
        elif alfa == 0.01:
            return 5
        else:
            print('Alpha Error, escolha 0.20, 0.15,  0.10,  0.05 ou  0.01')

    else:
        print('Tabela não inferiorormada, chame a função alfaconvert(alfa, tabela): ')


def t_binomial(amostra, k, p = 0.500, bilateral = False):
    '''
    O teste binomial calcula a probabilidade de uma frequencia de objetos estar dentro de um conjunto A ou B
    exclusivamente.
    :param amostra: n total da população
    :param k: n da amostra menos frequente ou menor
    :param p: nivel de significancia previamente estabelecido
    :param bilateral: Se o teste for bilateral a margem esquerda e direita das areas de rejeição devem ser somadas
    na prática z é multiplicado por 2 quando a amostra é >35 e pretende-se usar a Tabela A. Por padrão False.
    :return: valor do teste binomial e valor z da significancia tabelada
    eg. Numa amostra de 18 pessoas investgou-se se o estresse as faria voltar a usar a tecnica de dar nó primeiro
    aprendida ou a tecnica aprendida depois. 2 pessoas apenas usaram a segunda tecnica o que para um nivel de
    significancia 0,01 no teste bonomial seria uma chamada da função dessa forma: print(t_binomial(18,2,0.01))
    O resultado favorece H1, de que p > q, ou seja, o estresse inferiorluenciou as pessoas a voltarem para a técnica
    primeiro aprendida.
    '''
    z = 0
    q = 1 - p
    coef_bi = (math.factorial(amostra) / (math.factorial(k) * math.factorial(amostra-k)))
    if amostra > 25 and amostra*p*q >= 9:
        z = (k + 0.5) - (amostra * p) / math.sqrt(amostra * p * q)
    elif amostra <= 35:
        z = float('0.'+tabelas.D[amostra][k])
    else:
        try:
            z = float(tabelas.A[1][int(p * 100)])
            if bilateral == True:
                z = z * 2
        except:
            return'Não foi encontrado um valor p valido na tabela, tente 0.01, 0.02 ... 0.09'

    if z < p:
        return f'z= {z} é menor que o nivel de significancia p={p} estabelecido, favorecendo H1'
    else:
        return f'z= {z} é maior que o nivel de significancia p={p} estabelecido, favorecendo H0'



def t_quiquadrado(l, alfa = 0.001, e = 0 ):
    """
    Teste de X² de aderência.
    :param l: lista de frequencias observadas na amostra
    :param alfa: nivel de significância do teste, 0.001 se não inferiorormado
    :param e: frequencia esperada, se deixada em branco é considerada disctribuição aleatória
    :return: valor de X² e comparação com a tabela de referência
    Exemplo: Numa corrida de cavalos acredita-se que quem corre na raia interna (posição 0 na lista) tem vantagem
    sobre quem corre nas raias externas. Portanto observaram-se quantas vitórias ocorreram em cada raia durante um mês
    em 144 corridas. H0 = a distribuição das vitórias nas raias é igual (18 em cada) e H1 = há diferenças entre as raias.
    As vitórias de 144 corridas formam a lista A = (29,19,18,25,17,10,15,11), que pode ser testada com t_quiquadrado(A)
    """
    # avisos sobre aplicação do teste
    if len(l) <= 2:
        for elem in l:
            if elem < 5:
                return 'Quando k = 2 (GL = 1) e os valores das frequencias que compoem as variaveis passadas em l devem ser pelo menos 5.'
    else:
        maior = menor = 0
        for elem in l:
            if elem > 5:
                maior += 1
            else:
                menor += 1
        if menor >= (.2*(maior+menor)):
            return 'Quando 20% das frequencias observadas for menor que 5 X² não é um bom teste de aderência'

    # calcula X²
    if e == 0:e = sum(l)/len(l) #define 'e' caso não inferiorormado
    l = np.array(l)
    quiquadrado = (sum((l - e) ** 2))/e

    # compara X² com a tabela C
    gl = len(l)-1
    alf = alfaconvert(alfa, 'c' )
    z = float(tabelas.C[gl][alf])

    #retorna o valor e a comparação
    if quiquadrado <= z:
        return f'X² = {quiquadrado} é menor ou igual a z = {z}, para alfa = {alfa}. Favorecendo H1'
    else:
        return f'X² = {quiquadrado} é maior que z = {z}, para alfa = {alfa}. Favorecendo H0'



def t_kolmogorovsmirnov(l_o, l_e, alfa, frAcumulada = False):
    """
    Teste de aderencia de Kolmogorov-Smirnov
    :param l_o: Lista de frequencias observadas
    :param l_e: Lista de frequencias esperadas ou preditas por um modelo
    :param alfa: significancia estatistica
    :param frAcumulada: True para frequencias acumuladas (soma(1,2,3,4,5) = 5) e False para não (soma(1,1,1,1,1) = 5 )
    nas listas observada e esperada.
    :return: valor do maximo desvio entre as listas Dmax e comparação com a tabela de referência
    exemplo: para as listas
    Observada = (203,352,452,523,572,605,634,660,683,697,709,718729,744,750,757,763,767,771,788,804,812,820,832,840)
    Predita = (212.81,348.26,442.06,510.45,562.15,602.34,634.27,660.10,681.32,698.97,713.82,726.44,737.26,746.61,754.74,761.86,768.13,773.68,778.62,796.68,807.86,815.25,820.39,826.86,840.01)
    t_kolmogorovsmirnov(Observada, Esperada,0.05, True ) o valor Dmax = 0.014947710373062417 é maior ou igual a z = 33.1962,
    para alfa = 0.05. Favorecendo H0, os valores observados devem pertencer à distribuição esperada/predita.
    """
    if frAcumulada == False:
        N = sum(l_o)
    else:
        N = l_o[-1]
    if len(l_o) != len(l_e):
        return 'O numero de elementos na amostra observada deve ser igual ao da amostra esperada/predita'
    l_o = np.array(l_o)/l_o[-1]
    l_e = np.array(l_e)/l_e[-1]
    Dmax = max(l_o - l_e)

    if N > 35:
        if alfa == 0.20:
            sigi = 1.07
        elif alfa == 0.15:
            sigi = 1.14
        elif alfa == 0.10:
            sigi = 1.22
        elif alfa == 0.05:
            sigi = 1.36
        elif alfa == 0.01:
            sigi = 1.63
        else:
            return('Alpha Error, escolha 0.20, 0.15,  0.10,  0.05 ou  0.01')
        z = sigi/ math.sqrt(l_o[-1])
    else:
        alf = alfaconvert(alfa, 'f')
        z = float(tabelas.F[N][alf])
    if z >= alfa:
        return f'O valor Dmax = {Dmax} é maior ou igual a z = {z}, para alfa = {alfa}. Favorecendo H0'
    else:
        return f'O valor Dmax = {Dmax} é menor a z = {z}, para alfa = {alfa}. Favorecendo H1'



def t_infsimetria(lista, alfa = 0.05):
    """
    Teste de inferiorerencia de Simetria de uma amostra
    :param lista: lista com os dados a serem analisados
    :param alfa: valor de significancia deejado padrão 0.05
    :return: Zc e sua comparação com a tabela de referência
    exemplo: para os dados e = (13.53,28.42,48.11,48.64,51.40,59.91,67.98,79.13,103.05) Zc retorna ~0.154, que é
    menor do que o valor z=0.4801 (para alfa 0.05), favorecendo H0, a amostra é simetrica.
    """
    N = len(lista)
    if N < 20:
        print('Este teste é recomendado para amostras maiores que 20. Prosseguindo com os calculos. \n')
    lista = sorted(lista)
    direita = []
    esquerda = []
    for h in combinations(lista, 3):
        mediana = sum(h) - max(h) - min(h)
        media = sum(h) /3
        if media > mediana:
            direita.append(h)
        if media < mediana:
            esquerda.append(h)

    tvalor = len(direita) - len(esquerda)

    b1 = (len(direita) * tvalor - tvalor ** 2) * 2
    b2 = b1 + len(direita)
    variancia = ((((N-3)*(N-4))/((N-1)*(N-2))) * b1) + (((N-3)/(N-4)) *b2) + (((N*(N-1)*(N-2))/6) - ((1-(((N-3)*(N-4)*(N-5))/(N*(N-1)*(N-2)))) * (tvalor ** 2)) )
    Zc = tvalor / math.sqrt(variancia)
    z = float(tabelas.A[1][int(alfa * 100)])

    if Zc > z:
        return f'O valor Zc = {Zc} é maior do que z = {z}, para alfa = {alfa}. Favorecendo H1, assimetria.'
    else:
        return f'O valor Zc = {Zc} é menor ou igual a z = {z}, para alfa = {alfa}. Favorecendo H0, simetria.'

def t_aleatoriedade(lista, alfa = 0.05):
    """
    Teste de aleatoriedade de uma amostra
    :param lista: lista de valores não ordenados a ser analizada. Para valores numéricos a mediana é tomada para definir grupos
    acima e abaixo dela, para listas de tipos definidos é necessario definir apenas duas letras diferentes representando as observações
    na ordem em que ocorreram.
    :return: R chance de uma lista ser aelatória.
    exemplo 1: o lançamento de 1 dado 18 vezes gerando a lista g = (1,5,3,2,4,6,2,3,3,5,2,1,6,4,6,3,5,2) que será classificada
    com valores maiores que 3 ou menores ou iguais a 3.
    exemplo 2: 12 pessoas formam fila e são classificadas como altas e baixas gerando a lista h = ('h','l','h','h','l','l','l','l','h','h','l','l')
    essa lista deve ser convertida para 0 e 1 antes de ser enviada à função.
    Em ambos casos R = ao numero de grupos formados continuamente e comparados coma tabela de referencia.
    """
    conta = valor = superior = inferior = 0
    mediana = (max(lista)+0.0001)/2
    n_lista = []
    for i in lista:
        if i > mediana:
            n_lista.append('m')
        elif i < mediana:
            n_lista.append('n')
        else:
            return 'Pode haver um erro com a mediana se algum dos vaores for igual a ela por 4 casas decimais'
    for i in n_lista:
        if valor != i:
            valor = i
            conta += 1
    n = n_lista.count('n')
    m = n_lista.count('m')
    rvalor = conta
    N = (len(n_lista))

    #para amostrsa pequenas usamos a tabela G
    if m <= 20 and n <=20:
        mn = tabelas.G[m][n]
        if max(mn) != 0:
            superior = max(mn)
        else:
            superior = max(m,n)

        if min(mn) != 0:
            inferior = min(mn)
        else:
            inferior = 0

        if rvalor < superior and rvalor > inferior:
            return f'O valor r = {rvalor} estando dentro do intervalo {inferior}:{superior} favorecendo h0 a alfa = 0.05, a amostra é aleatória.'
        else:
            return f'O valor r = {rvalor} estando fora do intervalo {inferior}:{superior} favorece h1 a alfa = 0.05, a amostra não é aleatória.'
    #para amostras grande usamos z calculado
    else:
        if rvalor <= (2*m*n)/N+1:
            h = 0.5
        else:
            h = -0.5

        Z = (rvalor + h - (2*m*n)/(N-1)) / math.sqrt((2*m*n*((2*m*n)-N))/((N ** 2) * (N - 1)))

        z = float(tabelas.A[1][int(alfa * 100)])

        if Z > z:
            return f'O valor Z calculado {Z} é maior que o valor crítico de z = {z}, para alfa = {alfa}. Favorecendo H1. A ordem dos dados não é aleatória'
        else:
            return f'O valor Z calculado {Z} é menor que o valor crítico de z = {z}, para alfa = {alfa}. Favorecendo H0. A ordem dos dados é aleatória'


def t_pontomudanca(lista, alfa):
    N = len(lista) #tamanho da amostra
    m = sum(lista) #n sucessos
    n = N - m #n fracassos
    Sj = maior = 0
    for j,v in enumerate(lista,1):
        if v == 1:
            Sj += 1
        Dmn = abs((N/(m * n)) * (Sj - ((j * m / N))))
        if Dmn > maior:
            maior = Dmn

    dmax = 0.096
    print('valores', N,n,m,Sj)
    return f'{maior} devia ser {dmax}'


a = (29,19,18,25,17,10,15,11)
b = (8,10,13,15,10,14,12,8,7,6)
c = (203,352,452,523,572,605,634,660,683,697,709,718,729,744,750,757,763,767,771,788,804,812,820,832,840)
d = (212.81,348.26,442.06,510.45,562.15,602.34,634.27,660.10,681.32,698.97,713.82,726.44,737.26,746.61,754.74,761.86,768.13,773.68,778.62,796.68,807.86,815.25,820.39,826.86,840.01)
e = (13.53,28.42,48.11,48.64,51.40,59.91,67.98,79.13,103.05)
f = (3,0,5,6,1)
g = (1,5,3,2,4,6,2,3,3,5,6,6,2,1,6,4,6,3,1,5)
h = (1,0,1,0,1,1,1,0,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1,1,0,0,0,1,0,1,0,1,0,1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1)
i = (1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,1,1,1,0,0,1,1,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,0,0,1,1,
     0,1,1,0,1,1,1,1,0,0,1,0,1,1,1,1,0,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,0,0,0,1,1,1,1,0,1,1,
     0,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,0,1,1,0,1,
     0,0,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0,0,1,1)


print('**-**-'*10, '\n')
#print(t_binomial(40,19,0.01))
#print(t_quiquadrado(a, 0.01))
#print(t_kolmogorovsmirnov(c,d,0.05, True))
#print(t_infsimetria(e,0.05))
#print(t_aleatoriedade(h))
print(t_pontomudanca(i,0.05))
