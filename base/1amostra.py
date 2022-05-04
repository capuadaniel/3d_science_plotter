import math
import numpy as np
from scipy.stats import rankdata

#importa tabelas de referencia para os testes estatísticos e seu kit de conversões
import tabelas
import tabelastoolkit

def combinations(lista, r):
    # Copiado do itertools
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(lista)
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


def t_binomial(N, k, alfa = 0.05, uni_bi = 2, p = 0.5 ):
    '''
    :param N: total amostral
    :param k: menor grupo amonstral
    :param alfa: valor de significancia adotado, 0.05 por padrão
    :param uni_bi: Define se o teste deve ser testado unilateralmente ou bilateralmente multiplicando o valor da tabela A
    :param p: valor de frenquancia esperada, por padrão 0.5
    :return:
    eg. Numa amostra de 18 pessoas investigou-se se o estresse as faria voltar a usar a tecnica de dar nó primeiro
    aprendida ou a tecnica aprendida depois. 2 pessoas apenas usaram a segunda tecnica o que para um nivel de
    significancia 0,01 no teste bonomial seria uma chamada da função dessa forma: print(t_binomial(18,2,0.01))
    O resultado favorece H1, de que p > q, ou seja, o estresse inferiorluenciou as pessoas a voltarem para a técnica
    primeiro aprendida.
    '''
    q = 1 - p
    h = z =  0.5

    if N > 25 and N*p*q >= 9:
        z = (k + 0.5) - (N * p) / math.sqrt(N * p * q)
    elif N <= 35:
        z = float('0.'+tabelas.D[N][k])
    else:
        if k > N*p:
            h = -0.5

        z = ((k + h) - (N * p)) / math.sqrt(N * p * q)
        z = tabelastoolkit.alfaconvert(z,'a') * uni_bi
        p = alfa

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
    alf = tabelastoolkit.alfaconvert(alfa, 'c' )
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
        sigi = tabelastoolkit.calcLIII(alfa)
        z = sigi/ math.sqrt(l_o[-1])
    else:
        alf = tabelastoolkit.alfaconvert(alfa, 'f')
        z = float(tabelas.F[N][alf])
    if z >= alfa:
        return f'O valor Dmax = {Dmax} é maior ou igual a z = {z}, para alfa = {alfa}. Favorecendo H0'
    else:
        return f'O valor Dmax = {Dmax} é menor a z = {z}, para alfa = {alfa}. Favorecendo H1'


def t_infsimetria(lista, alfa = 0.05, uni_bi = 2):
    """
    Teste de inferencia de Simetria de uma amostra
    :param lista: lista com os dados a serem analisados
    :param alfa: valor de significancia deejado padrão 0.05
    :param uni_bi: determina se o teste é uni ou bilateral e se o valor buscado na tabela A deve ser dobrado ou não.
    :return: Zc e sua comparação com a tabela de referência
    exemplo: para os dados e = (13.53,28.42,48.11,48.64,51.40,59.91,67.98,79.13,103.05) Zc retorna ~0.154, que é
    menor do que o valor z=0.4443 (para alfa 0.05), favorecendo H0, a amostra é simetrica.
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
    z = tabelastoolkit.alfaconvert(Zc, 'a') * uni_bi

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
        z = float(tabelas.Anorm[1][tabelastoolkit.alfaconvert(alfa, 'anorm')])

        if Z > z:
            return f'O valor Z calculado {Z} é maior que o valor crítico de z = {z}, para alfa = {alfa}. Favorecendo H1. A amostra não é aleatória.'
        else:
            return f'O valor Z calculado {Z} é menor que o valor crítico de z = {z}, para alfa = {alfa}. Favorecendo H0. A amostra é aleatória.'


def t_pontomudanca(lista, alfa=0.05):
    '''
    O teste de ponto mudança serve para desocobrir se há uma alteração suficientemente grande numa serie de valores a ponto
    de ser razoavel assumir que essa variação não é aleatória, geralmente associada a uma mudança de desempenho ou no comportamento
    descrito pela variável.
    :param lista: lista de valores binarios (sucesso/fracasso) ou ordinais a serem avaliados
    :param alfa: nivel de confiança do teste, por padrão 0.05
    :return: o valor z calculado, sua referência na tabela e a hipótese favorecida.
    '''
    N = len(lista)  # tamanho da amostra
    m = sum(lista)  # n sucessos
    n = N - m  # n fracassos
    Zc = z = 0

    avalia = []
    for e in lista:
        if e not in avalia:
            avalia.append(e)
    if len(avalia) == 2:
        tipodeamostra = 'binomial'
    else:
        tipodeamostra = 'ordenado'

    if tipodeamostra == 'binomial':
        Sj = maior = 0
        for j,v in enumerate(lista,1):
            if v == 1:
                Sj += 1
            Dmn = abs((N/(m * n)) * (Sj - ((j * m / N))))

            if Dmn > maior:
                maior = Dmn

        Zc = maior # define z a maior diferença

        sigi = tabelastoolkit.calcLIII(alfa)
        z = sigi*(math.sqrt(N/(m*n)))

    elif tipodeamostra == 'ordenado':
        lista = rankdata(lista,  method='average')
        Wj = maior = Wassociado = 0
        for j,c in enumerate(lista):
            Wj += c
            Kmn = abs(((2 * Wj)) - ((j+1) * (N + 1)))
            if Kmn > maior:
                Wassociado =Wj
                maior = Kmn
                m = j+1

        Zc = maior # define Zc como a maior diferença
        n = N - m

        if m <= 10 and n <= 10: # pequenas amostras vão comparar Zc com a tabela J
            try:
                print(tabelas.J[m][n][maior])
            except:
                print(f'os valores de m e n foram {m} e {n}, e o Cl = {maior} mas não foi possivel resgatar um valor da tabela J, consulte a tabela')

        else: # grandes amostras vão calcular outro Zc e comparar o valor com a tabela A
            h = 0.5
            if Wassociado > m*(N+1)/2:
                h = -0.5
            Zc = (Wassociado + h - m * (N + 1) / 2) / math.sqrt(m * n * (N + 1) / 12)
            z = tabelas.Anorm[1][tabelastoolkit.alfaconvert(alfa, 'anorm')]

    if Zc > z:
        return f'O valor Zc = {Zc} é maior do que z = {z}, para alfa = {alfa}. Favorecendo H1.\n Se for de interesse o ponto de mudança foi no posto {m}'
    else:
        return f'O valor Zc = {Zc} é menor ou igual a z = {z}, para alfa = {alfa}. Favorecendo H0'



#valores de teste
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
j = (112,102,112,120,105,105,100,105,97,102,91,97,89,85,101,98,102,99,102,110,97,88,107,98,104)
k = (97,102,98,102,99,102,110,97,88,107,98,104)


#print(t_binomial(18,2))
#print(t_quiquadrado(a, 0.01))
#print(t_kolmogorovsmirnov(c,d,0.05, True))
#print(t_infsimetria(e,0.05,1))
#print(t_aleatoriedade(h))
#print(t_pontomudanca(i,0.01))
