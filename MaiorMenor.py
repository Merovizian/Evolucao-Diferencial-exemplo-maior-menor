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
        try:
            for elemento in range(qnt_individuos):
                populacao.append(random.sample(range(menor_caracteristica, maior_caracteristica), qnt_caracteristicas))
        except ValueError:
            print("Impossível gerar essa população. A quantidade de caracteristicas supera o maior valor delas,"
                  "tente aumentar o valor maximo das caracteristicas ou diminuir a quantidade de caracteristicas")
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


def mutacao(matrizElementos, mutacaoTaxa, repeticao=1):
    """
    Função que faz a "mutação" de caracteristicas de cada indivíduo, ou seja, pega uma ou mais caractetistica desse
    indivíduo e transforma em outro valor aleatoriamente a quantidade de caracteristicas é definido pela taxa.
    :param matrizElementos: Matriz que possui a população.
    :param mutacaoTaxa: é a taxa de caracteristicas que serão mutacionadas.
    :param repeticao: opção para o usuario decidir se as caracteristicas se repetem ou não, 1 — repete. 0 — não repete.
    :return: uma nova matriz com a nova geração.
    """

    matrizGeracaoNova = matrizElementos.copy()
    aux = 1
    contador = 0

    # Variavel que armazena a quantidades de caracteristicas que serão modificadas com a mutação. Conforme a taxa.
    qntRandom = round(len(matrizElementos[1]) * mutacaoTaxa)
    # Determinação dos valores maximos e minimos das caracteristicas que serão geradas aleatorimamente
    valorMaximo = (max([valor for linha in matrizElementos for valor in linha]))
    valorMinimo = (min([valor for linha in matrizElementos for valor in linha]))

    # variavel que armazena as posições das caracteristicas que irão sofrer a mutação
    posRandom = random.sample(range(0, len(matrizElementos[1])), qntRandom)

    # Copia-se a matriz de individuos para uma nova matriz.
    matrizGeracaoNova = matrizElementos.copy()
    contador = 0

    # ‘Loop’ que percorre cada indivíduo da população
    for elemento in matrizGeracaoNova:
        aux = 1

        # 'Loop' que percorre cada posição das caracteristica de cada indivíduo
        for contCaracteristica in range(len(elemento)):

            # Se a posição da caracteristica estiver nas posições randomicas há a mutação naquela posição
            if int(contCaracteristica) in posRandom:
                # É gerado então um valor aleatório para substituir uma caracteristica (Mutação)
                ValorCaracteristicaRandom = random.randint(valorMinimo, valorMaximo)
                # Faz a checagem para não repetir
                if repeticao == 0:
                    while not (ValorCaracteristicaRandom not in elemento):
                        contador += 1
                        # Como o valor aleatorio coincidiu com um já existente, repete-se o 'random'
                        ValorCaracteristicaRandom = random.randint(valorMinimo, valorMaximo)
                        # Faz a tentativa 50 vezes.
                        if contador >= 50:
                            aux = 0
                            contador = 0
                            break
                    if aux == 1:
                        elemento[contCaracteristica] = ValorCaracteristicaRandom
                else:
                    elemento[contCaracteristica] = random.randint(valorMinimo, valorMaximo)

    return matrizGeracaoNova


def aplicacao(geracoes, cruzamentoTaxa, mutacaoTaxa, matrizElementos, repeticao=1, comparacao='maior'):
    """
    É o programa principal, que faz a passagem das gerações.
    :param mutacaoTaxa: é a taxa de caracteristicas que serão mutacionadas.
    :param cruzamentoTaxa: é a porcentagem de caracteristicas que serão cruzadas.
    :param geracoes: quantidades de filhos que o sistema terá.
    :param matrizElementos: é a matriz que tem os individuos.
    :param repeticao: opção para o usuario decidir se as caracteristicas se repetem ou não, 1 — repete. 0 — não repete.
    :param comparacao: verifica se o usuario quer o maior fit ou menor fit entre as gerações.
    :return: retorna uma nova matriz com os individuos otimizados e também a matriz de distância.
    """
    matrizFit = list()
    try:
        for linhagem in range(geracoes):
            novosElementos = matrizElementos.copy()
            print(fitDistancia(novosElementos))
            print(f"Geração: {linhagem}")
            matrizFit.append((fitDistancia(novosElementos)))
            #novosElementos = cruzamento(novosElementos, cruzamentoTaxa, repeticao)
            novosElementos = mutacao(novosElementos, mutacaoTaxa, repeticao)
            if comparacao.lower() == "maior":
                if fitDistancia(novosElementos) > fitDistancia(matrizElementos):
                    matrizElementos = novosElementos.copy()
                else:
                    matrizElementos = matrizElementos.copy()
            else:
                if fitDistancia(novosElementos) < fitDistancia(matrizElementos):
                    matrizElementos = novosElementos.copy()
                else:
                    matrizElementos = matrizElementos.copy()
    except KeyboardInterrupt:

        return matrizElementos, matrizFit

    return matrizElementos, matrizFit


# EXEMPLO:
# Parametros iniciais
qntPessoas = 10 # População
qntCaracteristicas = 5 # Caracteristicas
menorCaracteristica = 0  # Menor Valor Caracteristicas
maiorCaracteristica = 10  # Maior Valor Caracteristica
repetir = 0  # 1 — repete. 0 — não repete. as caracteristicas
comparacao = "menor"  # A comparação será por maior ou menor fit entre as geraçoes?

# Filhos, gerações
geracoes = 50000

# Parametors para criação de novos individuos
cruzamentoTaxa = 0.26
mutacaoTaxa = 0.16

matrizElementos = povoar(qntPessoas, qntCaracteristicas, menorCaracteristica, maiorCaracteristica, repetir)


resultado, matrizfit = aplicacao(geracoes, cruzamentoTaxa, mutacaoTaxa, matrizElementos, repetir, comparacao)
print("PRIMEIRA POPULACAO")
print(matrizElementos)

print("ULTIMA POPULACAO")
print(resultado)

plt.plot(matrizfit)
plt.title(f"OTIMIZAÇÃO PARA A {comparacao.upper()} POPULAÇÂO")
plt.grid(True)
plt.xlabel("GERAÇÕES")
plt.ylabel("SOMA DAS CARACTERISTICAS")
plt.show()
