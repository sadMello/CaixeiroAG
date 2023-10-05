#%%
import random
import math
import matplotlib.pyplot as plt

# Obter informações das cidades
def obterCidades(): # Função para obter as cidades do arquivo TSP51.txt
    cidades = []
    f = open("TSP51.txt") # Abrir o arquivo TSP51.txt
    for i in f.readlines(): # Ler as linhas do arquivo
        node_city_val = i.split() # Separar as linhas do arquivo
        cidades.append(
            [node_city_val[0], float(node_city_val[1]), float(node_city_val[2])] # Adicionar as cidades na lista
        )

    return cidades

# Calcular a distância entre as cidades
def calcularDistancia(cidades): # Função para calcular a distância entre as cidades
    total_soma = 0
    for i in range(len(cidades) - 1):
        cidadeA = cidades[i]
        cidadeB = cidades[i + 1]

        d = math.sqrt(
            math.pow(cidadeB[1] - cidadeA[1], 2) + math.pow(cidadeB[2] - cidadeA[2], 2) # Calcular a distância entre as cidades
        )

        total_soma += d

    cidadeA = cidades[0]
    cidadeB = cidades[-1]
    d = math.sqrt(math.pow(cidadeB[1] - cidadeA[1], 2) + math.pow(cidadeB[2] - cidadeA[2], 2)) # Calcular a distância entre as cidades

    total_soma += d

    return total_soma

# Seleção da população
def selecionarPopulacao(cidades, tamanho): # Função para selecionar a população
    populacao = []

    for i in range(tamanho):
        c = cidades.copy()
        random.shuffle(c)
        distancia = calcularDistancia(c) # Calcular a distância entre as cidades
        populacao.append([distancia, c]) # Adicionar a distância e as cidades na lista
    maisApto = sorted(populacao)[0]

    return populacao, maisApto

# O algoritmo genético
def algoritmoGenetico(populacao, lenCidades, TAMANHO_SELECAO_TORNEIO, TAXA_MUTACAO, TAXA_CRUZAMENTO, OBJETIVO):
    numero_geracoes = 0
    for i in range(200):
        nova_populacao = []

        # Selecionando duas das melhores opções que temos (elitismo)
        nova_populacao.append(sorted(populacao)[0])
        nova_populacao.append(sorted(populacao)[1])

        for i in range(int((len(populacao) - 2) / 2)): # Loop para o cruzamento
            # CRUZAMENTO
            numero_aleatorio = random.random()
            if numero_aleatorio < TAXA_CRUZAMENTO:
                cromossomo_pai1 = sorted(
                    random.choices(populacao, k=TAMANHO_SELECAO_TORNEIO) # Selecionar o cromossomo pai 1
                )[0]

                cromossomo_pai2 = sorted(
                    random.choices(populacao, k=TAMANHO_SELECAO_TORNEIO) # Selecionar o cromossomo pai 2
                )[0]

                ponto = random.randint(0, lenCidades - 1) # Ponto de cruzamento

                cromossomo_filho1 = cromossomo_pai1[1][0:ponto] # Filho 1
                for j in cromossomo_pai2[1]:
                    if (j in cromossomo_filho1) == False: # Se o cruzamento ocorrer
                        cromossomo_filho1.append(j)

                cromossomo_filho2 = cromossomo_pai2[1][0:ponto] # Filho 2
                for j in cromossomo_pai1[1]:
                    if (j in cromossomo_filho2) == False:
                        cromossomo_filho2.append(j)

            # Se o cruzamento não ocorrer
            else:
                cromossomo_filho1 = random.choices(populacao)[0][1] # Filho 1
                cromossomo_filho2 = random.choices(populacao)[0][1] # Filho 2

            # MUTAÇÃO
            if random.random() < TAXA_MUTACAO: # Se a mutação ocorrer
                ponto1 = random.randint(0, lenCidades - 1) # Ponto de mutação
                ponto2 = random.randint(0, lenCidades - 1)
                cromossomo_filho1[ponto1], cromossomo_filho1[ponto2] = ( # Filho 1
                    cromossomo_filho1[ponto2],
                    cromossomo_filho1[ponto1],
                )

                ponto1 = random.randint(0, lenCidades - 1)
                ponto2 = random.randint(0, lenCidades - 1)
                cromossomo_filho2[ponto1], cromossomo_filho2[ponto2] = ( # Filho 2
                    cromossomo_filho2[ponto2],
                    cromossomo_filho2[ponto1],
                )

            # Adicionar os filhos na nova população
            nova_populacao.append([calcularDistancia(cromossomo_filho1), cromossomo_filho1]) 
            nova_populacao.append([calcularDistancia(cromossomo_filho2), cromossomo_filho2])

        populacao = nova_populacao

        numero_geracoes += 1
        
        # Imprimir a geração e a distância do cromossomo mais apto
        if numero_geracoes % 10 == 0:
            print(numero_geracoes, sorted(populacao)[0][0])

        # Se a distância do cromossomo mais apto for menor que o objetivo
        if sorted(populacao)[0][0] < OBJETIVO:
            break

    resposta = sorted(populacao)[0] 

    return resposta, numero_geracoes

# Desenhar o mapa das cidades e da resposta
def desenharMapa(cidade, resposta):
    for j in cidade:
        plt.plot(j[1], j[2], "ro")
        plt.annotate(j[0], (j[1], j[2])) # Anotar as cidades

    # Desenhar as linhas entre as cidades
    for i in range(len(resposta[1])):
        try:
            primeiro = resposta[1][i]
            segundo = resposta[1][i + 1]
            # Desenhar as linhas entre as cidades
            plt.plot([primeiro[1], segundo[1]], [primeiro[2], segundo[2]], "gray")
        except:
            continue

    primeiro = resposta[1][0]
    segundo = resposta[1][-1]
    plt.plot([primeiro[1], segundo[1]], [primeiro[2], segundo[2]], "gray") 

    plt.show()

def main():
    # Valores iniciais
    print("Algoritmo Genético para o Problema do Caixeiro Viajante")
    print("----------------------------------------------------------------")

    TAMANHO_POPULACAO = int(input("Digite o tamanho da população: "))
    TAMANHO_SELECAO_TORNEIO = int(input("Digite o tamanho da seleção do torneio: "))
    TAXA_MUTACAO = float(input("Digite a taxa de mutação (ex: 0.1): "))
    TAXA_CRUZAMENTO = float(input("Digite a taxa de cruzamento (ex: 0.9): "))
    OBJETIVO = float(input("Digite a distância alvo: "))

    # Executar o algoritmo genético
    cidades = obterCidades()
    # Selecionar a população
    primeiraPopulacao, primeiroMaisApto = selecionarPopulacao(cidades, TAMANHO_POPULACAO)
    resposta, numeroGeracoes = algoritmoGenetico( primeiraPopulacao, len(cidades), TAMANHO_SELECAO_TORNEIO, TAXA_MUTACAO, TAXA_CRUZAMENTO, OBJETIVO)

    print("\n----------------------------------------------------------------")
    print("Geração: " + str(numeroGeracoes))
    print("Distância do cromossomo mais apto antes do treinamento: " + str(primeiroMaisApto[0]))
    print("Distância do cromossomo mais apto após o treinamento: " + str(resposta[0]))
    print("Distância alvo: " + str(OBJETIVO))
    print("----------------------------------------------------------------\n")

    desenharMapa(cidades, resposta)

if __name__ == "__main__":
    main()

# %%
