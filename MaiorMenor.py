import random
import numpy as np
import matplotlib.pyplot as plt


def povoar(qnt_individuos, qnt_caracteristicas, menor_caracteristica=0, maior_caracteristica=9, repeticao=1):
    """
    Inicia a população de individuos, conforme as caracteristicas passadas.
    :param qnt_individuos: é a quantidade de individuos que a população irá gerar.
    :param qnt_caracteristicas: é a caracteristica de cada um dos individuos.
    :param menor_caracteristica: é o valor mínimo que cada indivíduo poderá ter como caracteristica.
    :param maior_caracteristica: é o valor máximo que cada indivíduo poderá ter como caracteristica.
    :param repeticao: opção para o usuario decidir se as caracteristicas se repetem ou não, 1 — repete. 0 — não repete.

    :return: populacao: é uma matriz de individuos contendo os individuos e as suas caracteristicas.
    """
    populacao = []

    # caso o usuario opite por NÃO repetir os valores
    if repeticao == 0:
        for elemento in range(qnt_individuos):
            populacao.append(random.sample(range(menor_caracteristica, maior_caracteristica), qnt_caracteristicas))
    # caso o usuario opite por repetir os valores
    if repeticao == 1:
        populacao = np.random.randint(menor_caracteristica, maior_caracteristica + 1, size=(qnt_individuos,
                                                                                            qnt_caracteristicas))
    return populacao


def fitDistancia(matrizElementos):
    """
   Função que faz o cálculo da distância percorrida por cada um dos elementos.
   :param matrizElementos: é a matriz onde estão elencados os elementos(individuos, população)
   :return: uma matriz com o resultado desse cálculo
   """
    # cria uma lista vazia
    matrizResultadoSoma = []

    # for para colocar na lista vazia a caracteristica de todos os individuos
    for elemento in range(len(matrizElementos)):
        for caracteristica in range(len(matrizElementos[elemento])):
            matrizResultadoSoma.append(matrizElementos[elemento][caracteristica])
    # retorna o valor da soma de todos as caracteristicas dessa população
    return sum(matrizResultadoSoma)


def cruzamento(matrizElemento, cruzamentoTaxa, repeticao=1):
    """
    Programa que faz o cruzamento de "genes" entre duas populaçoes, conforme a taxa de cruzamento, sendo uma porcentagem
    da quantidade de caracteristicas do elemento. Ou seja, se for setada em 0.5, 50% das caracteristicas
    de ambos os elementos serão cruzadas.
    :param matrizElemento: é a matriz que possui os elementos, a população.
    :param cruzamentoTaxa: é a porcentagem de caracteristicas que serão cruzadas.
    :param repeticao: opção para o usuario decidir se as caracteristicas se repetem ou não, 1 — repete. 0 — não repete.
    :return: retorna uma matriz com novos elementos cruzados.
    """

    # gera um array de zeros
    matrizGeracaoNova = np.zeros((len(matrizElemento), (len(matrizElemento[0]))))

    # for para a criação da nova matriz de cruzamento
    for elementos in range(len(matrizElemento)):
        for caracteristica in range(len(matrizElemento[elementos])):
            # condição para selecionar quais caracteristicas serão cruzadas, conforme a taxa
            if caracteristica < cruzamentoTaxa * len(matrizElemento[elementos]):
                # as primeiras caracteristicas até a taxa não mudam. Então iguala-se as caracteristicas
                matrizGeracaoNova[elementos][caracteristica] = matrizElemento[elementos][caracteristica]
            else:
                # try para previnir que o programa pare, quando chegar no ultimo individuo
                try:
                    # caso o usuario decida que não haverá repetição
                    if repeticao == 0:
                        # programa verifica se há numeros repetidos entre os individuos
                        if int(matrizElemento[elementos + 1][caracteristica]) not in (matrizGeracaoNova[elementos]):
                            # se não existe numero repetido, faz o cruzamento, entre individuos
                            matrizGeracaoNova[elementos][caracteristica] = matrizElemento[elementos + 1][caracteristica]
                        # se existe numero repetido, não há cruzamento, apenas se iguala as caracteristicas
                        else:
                            matrizGeracaoNova[elementos][caracteristica] = matrizElemento[elementos][caracteristica]
                    # caso o usuario decida que haverá repetição. Há cruzamento.
                    else:
                        matrizGeracaoNova[elementos][caracteristica] = matrizElemento[elementos + 1][caracteristica]
                # exceção para evitar que o programa pare, pois, o cruzamento é sempre com um indivíduo + 1, e isso
                # causa erro quando chegar no último individuo.
                except IndexError:
                    # mesma logica acima, porém ao invés de ir para o individui + 1, o último individuo faz cruzamento
                    # com o indivíduo 0.
                    if repeticao == 0:
                        if int(matrizElemento[0][caracteristica]) not in matrizGeracaoNova[elementos]:
                            matrizGeracaoNova[elementos][caracteristica] = matrizElemento[0][caracteristica]
                        else:
                            matrizGeracaoNova[elementos][caracteristica] = matrizElemento[elementos][caracteristica]
                    else:
                        matrizGeracaoNova[elementos][caracteristica] = matrizElemento[0][caracteristica]

    return matrizGeracaoNova


def mutacao(matrizElementos, mutacaoTaxa):
    '''
    Função que faz a "mutação" de caracteristicas de cada individuo, a quantidade de caracteristicas é definido pela taxa
    :param matrizElementos: Matriz que possui a população
    :param mutacaoTaxa: é a taxa de caracteristicas que serão mutacionadas
    :return: uma nova matriz com a nova geração
    '''
    valorMaximo = (max([valor for linha in matrizElementos for valor in linha]))
    qntRandom = round(len(matrizElementos[1]) * mutacaoTaxa)
    matrizGeracaoNova = matrizElementos.copy()
    aux = 1
    contador = 0
    for elementos in range(len(matrizElementos)):
        for caracteristica in range(len(matrizElementos[elementos])):
            if caracteristica < qntRandom:
                ValorCaracteristicaRandom = random.randint(0, 9)
                PosicaoCaracteristicaRandom = random.randint(0, len(matrizElementos[1]) - 1)
                matrizGeracaoNova[elementos][PosicaoCaracteristicaRandom] = ValorCaracteristicaRandom
    return matrizGeracaoNova


def aplicacao(geracoes, matrizElementos):
    '''
    É o programa principal, que faz a passagem das gerações
    :param geracoes:
    :param matrizElementos:
    :return:
    '''
    matrizFit = list()
    try:
        for linhagem in range(geracoes):
            novosElementos = matrizElementos.copy()
            print(fitDistancia(novosElementos))
            print(f"Geração: {linhagem}")
            matrizFit.append(int(sum(fitDistancia(novosElementos))))
            novosElementos = cruzamento(novosElementos, cruzamentoTaxa)
            novosElementos = mutacao(novosElementos, mutacaoTaxa)
            if fitDistancia(novosElementos) > fitDistancia(matrizElementos):
                matrizElementos = novosElementos.copy()
            else:
                matrizElementos = matrizElementos.copy()
    except:

        return matrizElementos, matrizFit

    return matrizElementos, matrizFit


povoacao = povoar(5, 6, 0, 10, 1)
print(povoacao)
print(fitDistancia(povoacao))
povoacao = cruzamento(povoacao, 0.5,0)
print(povoacao)
print(fitDistancia(povoacao))

'''# Parametros iniciais
pessoas = 2  # População
viagens = 5  # Caracteristicas
geracoes = 5000000

# Parametors para criação de novos individuos
cruzamentoTaxa = 0.25
mutacaoTaxa = 0.15

matrizElementos = populacao(pessoas, viagens)




resultado, matrizfit = aplicacao(geracoes, matrizElementos)
print(matrizElementos)
print(resultado)

plt.plot( matrizfit )
plt.title("Caixeiro Viajante por Evolucao Diferencial")
plt.grid(True)
plt.xlabel("GERAÇÕES")
plt.ylabel("SOMA DAS DISTANCIAS")
plt.show()

'''
