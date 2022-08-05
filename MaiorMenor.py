import random
import numpy as np
import matplotlib.pyplot as plt


def povoar(qnt_individuos, qnt_caracteristicas, menor_caracteristica=0, maior_caracteristica=9):
    '''
    Inicia a população de individuos, conforme as caracteristicas passadas.
    :param qnt_individuos: é a quantidade de individuos que a população irá gerar.
    :param qnt_caracteristicas: é a caracteristica de cada um dos individuos.
    :param menor_caracteristica: é o valor mínimo que cada indivíduo poderá ter como caracteristica.
    :param maior_caracteristica: é o valor máximo que cada indivíduo poderá ter como caracteristica.

    :return: populacao: é uma matriz de individuos contendo os individuos e suas caracteristicas.
    '''

    populacao = np.random.randint(menor_caracteristica, maior_caracteristica+1,  size=(qnt_individuos, qnt_caracteristicas))
    return populacao


def fitDistancia(matrizElementos, matrizCidades=4):
    '''
   Função que faz o calculo da distancia percorrida por cada um dos elementos
   :param matrizCidades: No momento, não é util essa função
   :param matrizElementos: é a matriz onde estão elencados os elementos(individuos, população)
   :return: uma matriz com o resultado desse calculo
   '''
    matrizResultadoDistancia = np.zeros((len(matrizElementos), 1))

    for elemento in range(len(matrizElementos)):
        for caracteristica in range(len(matrizElementos[elemento])):
            matrizResultadoDistancia[elemento] += matrizElementos[elemento][caracteristica]
    return sum(matrizResultadoDistancia)


def cruzamento(matrizElementos, cruzamentoTaxa):
    '''
    Programa que faz o cruzamento de "genes" entre duas populaçoes, de acordo com a taxa de cruzamento
    a taxa de cruzamento é uma porcentagem da quantidade de caracteristicas do elemento. ou seja, se for setada
    em 0.5, 50% das caracteristicas de ambos os elementos serão cruzadas
    :param matrizElementos: é a matriz que possui os elementos, a população
    :param cruzamentoTaxa: é a porcentagem de caracteristicas que serão cruzadas
    :return: retorna uma matriz com novos elementos cruzados
    '''
    matrizGeracaoNova = matrizElementos.copy()
    # matrizGeracaoNova = np.zeros((len(matrizElementos), len(matrizElementos[1])))
    for elementos in range(len(matrizElementos)):
        for caracteristica in range(len(matrizElementos[elementos])):
            if caracteristica < cruzamentoTaxa * len(matrizElementos[elementos]):
                if (int(matrizElementos[elementos][caracteristica]) not in (matrizGeracaoNova[elementos])):
                    matrizGeracaoNova[elementos][caracteristica] = matrizElementos[elementos][caracteristica]
            else:
                try:
                    if (int(matrizElementos[elementos + 1][caracteristica]) not in (matrizGeracaoNova[elementos])):
                        matrizGeracaoNova[elementos][caracteristica] = matrizElementos[elementos + 1][caracteristica]
                except:
                    if (int(matrizElementos[0][caracteristica]) not in matrizGeracaoNova[elementos]):
                        matrizGeracaoNova[elementos][caracteristica] = matrizElementos[0][caracteristica]

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


teste = np.random.randint(0,99,  size=(1, 15))
resposta = sum(teste[0])

print(resposta)
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
