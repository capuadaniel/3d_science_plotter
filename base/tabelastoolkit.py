import tabelas

def calcLIII(alfa):
    '''
    adaptado de Smirnov,N(1948). Tables for estimating the goodness of fit of empirical distributions.
    Annals of mathematical statistics, 19, 280-281.
    :param alfa: nivel de confiança
    :return: resultado da tabela Liii que deve ser multiplicado por raiz de m+n/m*n
    '''
    if alfa == 0.20:
        Liii = 1.07
    elif alfa == 0.15:
        Liii = 1.14
    elif alfa == 0.10:
        Liii = 1.22
    elif alfa == 0.05:
        Liii = 1.36
    elif alfa == 0.025:
        Liii = 1.48
    elif alfa == 0.01:
        Liii = 1.63
    elif alfa == 0.005:
        Liii = 1.73
    elif alfa == 0.001:
        Liii = 1.95
    else:
        return('Alpha Error, escolha 0.20, 0.15, 0.10, 0.05, 0.25, 0.1, 0.005  ou  0.001')

    return Liii

def alfaconvert(alfa, tabela):
    tabela = str(tabela.upper())
    if tabela == 'A':
        alf_str = str(abs(alfa))
        alf_A = int(alf_str[0:3].replace('.',''))
        alf_B = int(alf_str[3])
        c = tabelas.A[alf_A][alf_B]
        if c == '':
            return tabelas.A[alf_A][0]
        else:
            return c

    elif tabela.upper() == 'ANORM':
        # traduz o valor de significancia alfa para um inteiro utilizavel para a tabela C
        if alfa == 0.20:
            return 1
        elif alfa == 0.10:
            return 2
        elif alfa == 0.05:
            return 3
        elif alfa == 0.02:
            return 4
        elif alfa == 0.01:
            return 5
        elif alfa == 0.002:
            return 6
        elif alfa == 0.001:
            return 7
        elif alfa == 0.0001:
            return 8
        elif alfa == 0.00001:
            return 9

        else:
            print('Alpha Error, escolha 0.001, 0.01, 0.025, 0.05 ou 0.10')

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