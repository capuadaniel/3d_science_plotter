import math
import numpy as np
import tabelas
import tabelastoolkit

def t_mudancaMcNemar(ab, ba, alfa=0.05):
    '''
    Para usar o teste de mudança de McNemar deve-se separar os dados em variaveis de 3 tipos, as que tiveram alteração
    de a para b as que se alteraram no sentido inverso e as que não tiveram alteração.
    :param ab: numero de mudanças na direção a para b
    :param ba: numero de mudanças na direção b para a
    :param alfa: valor de significancia adotado, 0.05 por padrão
    :return: o valor z calculado, sua referencia na tabela e a hipotese favorecida.
    '''
    N = ab + ba
    alf = tabelastoolkit.alfaconvert(alfa, 'C')
    c = tabelas.C[1][alf]
    z = (abs(ab - ba) - 1) **2 /(ab+ba)
    if N/2 <= 5:
        return f'O valor de N {N}/2, ou seja, valor esperado da frenquencia, é muito baixo, considere usar o teste binomial'

    if z < c:
        return f'O valor z = {z} é menor do que o valor crítico {c}, para alfa = {alfa}. Favorecendo H0.'
    else:
        return f'O valor z = {z} é maior ou igual ao valor crítico {c}, para alfa = {alfa}. Favorecendo H1'

def t_sinal(mais,menos, alfa=0.05, uni_bi=2):
    '''
    O teste do sinal recebe valores + e - associados a duplas como casais, ou antes e depois muitas vezes convertendo valores
    de investigação numa variavel mais simples +, - e 0 para empates.
    :param mais: n de sinais +
    :param menos: n de sinais -
    :param alfa: valor de significancia adotado, 0.05 por padrão
    :param uni_bi: Define se o teste deve ser testado unilateralmente ou bilateralmente
    :return:
    exemplo: investigando a tomada de decisão por casais se o casal concordava em ambos terem poder de decisão na compra de uma
    casa era registrado o valor 0, enquanto quando a discordancia ia no sentido de que o marido deveria tomar a decisão era anotado
    o valor - para o casal e quando a tendencia era para a esposa o valor +. Nesse caso tivemos 14 casais discordantes, 3 + e 11 -.
    t_sinal(3,11) como 14 < 35 usamos a função para pequenas amostras indo direto para a tabela D onde um valor critico de 0.029 nos
    mostra que sendo menor que 0.05 (nosso alfa e região de rejeição) devemos rejeitar H0 em favor de H1. Há tendencia entre casais
    de deixar essa decisão analisada mais nas mãos do marido.
    Num estudo com N maior as mudanças foram calculadas t_sinal(26,59), resultando em 0.006 como valor critico dentro do estipulado
    de 0.05, rejeitando H0 em favor de H1.
    '''
    N = mais+menos
    maior = max(mais, menos)
    menor = min(mais, menos)
    uni_bi_valor = 'bilateral'
    if uni_bi == 1: uni_bi_valor = 'unilateral'

    if N < 35:
        z = float(tabelas.D[N][menor])/1000

        if z < alfa:
            return f'O valor z = {z} é menor do que o valor crítico alfa = {alfa}. Favorecendo H0.'
        else:
            return f'O valor z = {z} é maior ou igual ao valor crítico alfa = {alfa}. Favorecendo H1'

    else:
        h = 1
        if N/2 < menor:
            h = -1
        z = abs((2 * menor + h - N) / math.sqrt(N))
        c = tabelastoolkit.alfaconvert(z, 'A') * uni_bi

        if c <= alfa:
            return f'O valor crítico {c} ({uni_bi_valor}) é menor ou igual que o valor de significancia escolhido alfa = {alfa}. Favorecendo H1.'
        else:
            return f'O valor crítico {c} ({uni_bi_valor}) é maior que o valor de significancia escolhido alfa = {alfa}. Favorecendo H0.'




#dados para testes
#print(t_mudancaMcNemar(13,7))
#print(t_sinal(11,3))
#print(t_sinal(26,59))