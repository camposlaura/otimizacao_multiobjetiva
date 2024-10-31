import concurrent.futures
import random
import math
import time
import os

# Calibra as meta heurísticas
LIMITE_TEMPO = 10
GRASP_ITERACOES = 1000
SA_ITERACOES = 1000
SA_TEMP_INICIAL = 500
SA_TEMP_FINAL = 1
SA_ALFA = 0.95

MEUS_DADOS = [ './meus_dados/partnum-35-1.txt', './meus_dados/partnum-35-2.txt', './meus_dados/partnum-35-3.txt', './meus_dados/partnum-35-4.txt', './meus_dados/partnum-35-5.txt' ]
DADOS = [ './dados/partnum-15-1.txt', './dados/partnum-15-2.txt', './dados/partnum-15-3.txt', './dados/partnum-15-4.txt', './dados/partnum-15-5.txt', './dados/partnum-35-1.txt', './dados/partnum-35-2.txt', './dados/partnum-35-3.txt', './dados/partnum-35-4.txt', './dados/partnum-35-5.txt', './dados/partnum-55-1.txt', './dados/partnum-55-2.txt', './dados/partnum-55-3.txt', './dados/partnum-55-4.txt', './dados/partnum-55-5.txt', './dados/partnum-75-1.txt', './dados/partnum-75-2.txt', './dados/partnum-75-3.txt', './dados/partnum-75-4.txt', './dados/partnum-75-5.txt', './dados/partnum-95-1.txt', './dados/partnum-95-2.txt', './dados/partnum-95-3.txt', './dados/partnum-95-4.txt', './dados/partnum-95-5.txt' ]

def carregarDados(arquivo_path):
    """
    Carrega o conjunto de números de um arquivo de dados.

    Parâmetros:
    - arquivo_path (str): Caminho para o arquivo de dados.

    Retorna:
    - int[]: Uma lista com os números contidos no arquivo.
    """
    with open(arquivo_path, 'r') as file:
        qtdItens = int(file.readline().strip())
        
        conjunto = []
        for i in range(qtdItens):
            numero = int(file.readline().strip())
            conjunto.append(numero)

        return(conjunto)

def avaliaSolucao(solucao, numeros):
    """
    Avalia uma solução calculando a diferença entre as somas dos subconjuntos.

    Parâmetros:
    - solucao (boolean[]): Lista binária indicando a partição dos números (0 ou 1).
    - numeros (int[]): Lista de números inteiros a serem particionados.

    Retorna:
    - int: Diferença absoluta entre as somas dos subconjuntos.
    """
    soma1 = sum(n for i, n in enumerate(numeros) if solucao[i] == 1)
    soma2 = sum(n for i, n in enumerate(numeros) if solucao[i] == 0)
    return abs(soma1 - soma2)

def geraSolucaoInicial(n):
    """
    Gera uma solução inicial aleatória para o problema.

    Parâmetros:
    - n (int): Número de elementos no conjunto de números.

    Retorna:
    - boolean[]: Solução inicial aleatória representada por uma lista binária.
    """
    return [random.choice([0, 1]) for _ in range(n)]

def perturbaSolucao(solucao):
    """
    Meta Heurística: Simulated Annealing

    Perturba a solução atual alterando aleatoriamente um elemento da partição.

    Parâmetros:
    - solucao (boolean[]): Solução atual representada por uma lista binária.

    Retorna:
    - boolean[]: Nova solução com um elemento alterado.
    """
    nova_solucao = solucao[:]
    indice = random.randint(0, len(solucao) - 1)
    nova_solucao[indice] = 1 - nova_solucao[indice]
    return nova_solucao

def simulatedAnnealing(numeros):
    """
    Meta Heurística: Simulated Annealing

    Aplica SA para encontrar uma partição ótima.

    Parâmetros:
    - numeros (int[]): Lista de números inteiros a serem particionados.

    Retorna:
    - [boolean[], int]: Melhor solução encontrada e a diferença mínima entre as somas dos subconjuntos.
    """
    n = len(numeros)
    solucaoAtual = geraSolucaoInicial(n)
    melhorSolucao = solucaoAtual[:]
    melhorDiferenca = avaliaSolucao(melhorSolucao, numeros)
    temperatura = SA_TEMP_INICIAL

    while temperatura > SA_TEMP_FINAL:
        for _ in range(SA_ITERACOES):
            novaSolucao = perturbaSolucao(solucaoAtual)
            diferencaAtual = avaliaSolucao(solucaoAtual, numeros)
            novaDiferenca = avaliaSolucao(novaSolucao, numeros)
            delta = novaDiferenca - diferencaAtual

            if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
                solucaoAtual = novaSolucao

            if novaDiferenca < melhorDiferenca:
                melhorSolucao = novaSolucao[:]
                melhorDiferenca = novaDiferenca

        temperatura *= SA_ALFA

    return melhorSolucao, melhorDiferenca

def buscaLocal(solucao, numeros):
    """
    Meta Heurística: GRASP

    Realiza busca local para melhorar a solução atual, encontrando uma partição com menor diferença entre as somas.

    Parâmetros:
    - solucao (boolean[]): Solução inicial representada por uma lista binária.
    - numeros (int[]): Lista de números inteiros a serem particionados.

    Retorna:
    - [boolean[], int]: Melhor solução encontrada e a diferença mínima entre as somas dos subconjuntos.
    """
    melhorSolucao = solucao[:]
    melhorDiferenca = avaliaSolucao(melhorSolucao, numeros)

    for i in range(len(solucao)):
        novaSolucao = solucao[:]
        novaSolucao[i] = 1 - novaSolucao[i]
        novaDiferenca = avaliaSolucao(novaSolucao, numeros)

        if novaDiferenca < melhorDiferenca:
            melhorSolucao = novaSolucao[:]
            melhorDiferenca = novaDiferenca

    return melhorSolucao, melhorDiferenca

def grasp(numeros):
    """
    Meta Heurística: GRASP

    Aplica GRASP para encontrar uma partição ótima.

    Parâmetros:
    - numeros (int[]): Lista de números inteiros a serem particionados.

    Retorna:
    - [boolean[], int]: Melhor solução encontrada e a diferença mínima entre as somas dos subconjuntos.
    """
    melhorSolucao = geraSolucaoInicial(len(numeros))
    melhorDiferenca = avaliaSolucao(melhorSolucao, numeros)

    for _ in range(GRASP_ITERACOES):
        solucao = geraSolucaoInicial(len(numeros))
        solucao, diferenca = buscaLocal(solucao, numeros)

        if diferenca < melhorDiferenca:
            melhorSolucao = solucao[:]
            melhorDiferenca = diferenca

    return melhorSolucao, melhorDiferenca

def comparacao(numeros):
    """
    Compara o desempenho das meta heurísticas Simulated Annealing e GRASP no problema.

    Parâmetros:
    - numeros (int[]): Lista de números inteiros a serem particionados.

    Exibe os tempos médios e as diferenças médias entre as somas dos subconjuntos para cada meta heurística.
    """
    tempoSA, tempoGRASP = 0, 0
    resultadosSA, resultadosGRASP = [], []

    # Simulated Annealing
    inicioSA = time.time()
    solucaoSA, diferencaSA = simulatedAnnealing(numeros)
    tempoSA += time.time() - inicioSA
    resultadosSA.append(diferencaSA)

    # GRASP
    inicioGRASP = time.time()
    solucaoGRASP, diferencaGRASP = grasp(numeros)
    tempoGRASP += time.time() - inicioGRASP
    resultadosGRASP.append(diferencaGRASP)

    mediaSA = sum(resultadosSA) / len(resultadosSA)
    mediaGRASP = sum(resultadosGRASP) / len(resultadosGRASP)

    print(f'\nMédia Simulated Annealing: {mediaSA}')
    print(f'Tempo Médio Simulated Annealing: {tempoSA:.6f} segundos')
    print(f'Média GRASP: {mediaGRASP}')
    print(f'Tempo Médio GRASP: {tempoGRASP:.6f} segundos\n')

# Carrega os dados e executa as meta heurísticas
conjuntos = [carregarDados(caminho) for caminho in MEUS_DADOS]
for numeros in conjuntos:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(comparacao, numeros)
        try:
            resultado = future.result(timeout=LIMITE_TEMPO)
        except concurrent.futures.TimeoutError:
            print('Tempo limite excedido')