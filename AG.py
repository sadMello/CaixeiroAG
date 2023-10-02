import random
import math
import matplotlib.pyplot as plt

# Obter informações das cidades
def obterCidades():
    cidades = []
    f = open("TSP51.txt")
    for i in f.readlines():
        node_city_val = i.split()
        cidades.append(
            [node_city_val[0], float(node_city_val[1]), float(node_city_val[2])]
        )

    return cidades

# Calcular a distância entre as cidades
def calcularDistancia(cidades):
    total_soma = 0
    for i in range(len(cidades) - 1):
        cidadeA = cidades[i]
        cidadeB = cidades[i + 1]

        d = math.sqrt(
            math.pow(cidadeB[1] - cidadeA[1], 2) + math.pow(cidadeB[2] - cidadeA[2], 2)
        )

        total_soma += d

    cidadeA = cidades[0]
    cidadeB = cidades[-1]
    d = math.sqrt(math.pow(cidadeB[1] - cidadeA[1], 2) + math.pow(cidadeB[2] - cidadeA[2], 2))

    total_soma += d

    return total_soma

# Seleção da população
def selecionarPopulacao(cidades, tamanho):
    populacao = []

    for i in range(tamanho):
        c = cidades.copy()
        random.shuffle(c)
        distancia = calcularDistancia(c)
        populacao.append([distancia, c])
    maisApto = sorted(populacao)[0]

    return populacao, maisApto

# O algoritmo genético
def algoritmoGenetico(
    populacao,
    lenCidades,
    TAMANHO_SELECAO_TORNEIO,
    TAXA_MUTACAO,
    TAXA_CRUZAMENTO,
    OBJETIVO,
):
    numero_geracoes = 0
    for i in range(200):
        nova_populacao = []

        # Selecionando duas das melhores opções que temos (elitismo)
        nova_populacao.append(sorted(populacao)[0])
        nova_populacao.append(sorted(populacao)[1])

        for i in range(int((len(populacao) - 2) / 2)):
            # CRUZAMENTO
            numero_aleatorio = random.random()
            if numero_aleatorio < TAXA_CRUZAMENTO:
                cromossomo_pai1 = sorted(
                    random.choices(populacao, k=TAMANHO_SELECAO_TORNEIO)
                )[0]

                cromossomo_pai2 = sorted(
                    random.choices(populacao, k=TAMANHO_SELECAO_TORNEIO)
                )[0]

                ponto = random.randint(0, lenCidades - 1)

                cromossomo_filho1 = cromossomo_pai1[1][0:ponto]
                for j in cromossomo_pai2[1]:
                    if (j in cromossomo_filho1) == False:
                        cromossomo_filho1.append(j)

                cromossomo_filho2 = cromossomo_pai2[1][0:ponto]
                for j in cromossomo_pai1[1]:
                    if (j in cromossomo_filho2) == False:
                        cromossomo_filho2.append(j)

            # Se o cruzamento não ocorrer
            else:
                cromossomo_filho1 = random.choices(populacao)[0][1]
                cromossomo_filho2 = random.choices(populacao)[0][1]

            # MUTAÇÃO
            if random.random() < TAXA_MUTACAO:
                ponto1 = random.randint(0, lenCidades - 1)
                ponto2 = random.randint(0, lenCidades - 1)
                cromossomo_filho1[ponto1], cromossomo_filho1[ponto2] = (
                    cromossomo_filho1[ponto2],
                    cromossomo_filho1[ponto1],
                )

                ponto1 = random.randint(0, lenCidades - 1)
                ponto2 = random.randint(0, lenCidades - 1)
                cromossomo_filho2[ponto1], cromossomo_filho2[ponto2] = (
                    cromossomo_filho2[ponto2],
                    cromossomo_filho2[ponto1],
                )

            nova_populacao.append([calcularDistancia(cromossomo_filho1), cromossomo_filho1])
            nova_populacao.append([calcularDistancia(cromossomo_filho2), cromossomo_filho2])

        populacao = nova_populacao

        numero_geracoes += 1

        if numero_geracoes % 10 == 0:
            print(numero_geracoes, sorted(populacao)[0][0])

        if sorted(populacao)[0][0] < OBJETIVO:
            break

    resposta = sorted(populacao)[0]

    return resposta, numero_geracoes

# Desenhar o mapa das cidades e da resposta
def desenharMapa(cidade, resposta):
    for j in cidade:
        plt.plot(j[1], j[2], "ro")
        plt.annotate(j[0], (j[1], j[2]))

    for i in range(len(resposta[1])):
        try:
            primeiro = resposta[1][i]
            segundo = resposta[1][i + 1]

            plt.plot([primeiro[1], segundo[1]], [primeiro[2], segundo[2]], "gray")
        except:
            continue

    primeiro = resposta[1][0]
    segundo = resposta[1][-1]
    plt.plot([primeiro[1], segundo[1]], [primeiro[2], segundo[2]], "gray")

    plt.show()

def main():
    # Valores iniciais
    TAMANHO_POPULACAO = 2000
    TAMANHO_SELECAO_TORNEIO = 4
    TAXA_MUTACAO = 0.1
    TAXA_CRUZAMENTO = 0.9
    OBJETIVO = 450.0

    cidades = obterCidades()
    primeiraPopulacao, primeiroMaisApto = selecionarPopulacao(cidades, TAMANHO_POPULACAO)
    resposta, numeroGeracoes = algoritmoGenetico(
        primeiraPopulacao,
        len(cidades),
        TAMANHO_SELECAO_TORNEIO,
        TAXA_MUTACAO,
        TAXA_CRUZAMENTO,
        OBJETIVO,
    )

    print("\n----------------------------------------------------------------")
    print("Geração: " + str(numeroGeracoes))
    print("Distância do cromossomo mais apto antes do treinamento: " + str(primeiroMaisApto[0]))
    print("Distância do cromossomo mais apto após o treinamento: " + str(resposta[0]))
    print("Distância alvo: " + str(OBJETIVO))
    print("----------------------------------------------------------------\n")

    desenharMapa(cidades, resposta)

if __name__ == "__main__":
    main()
