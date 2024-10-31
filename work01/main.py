import concurrent.futures
import random
import math
import time
import os

TEMP_INICIAL = 500
TEMP_FINAL = 1
ALFA = 0.95
ITERACOES_SA = 1000
ITERACOES_GRASP = 1000
LIMITE_TEMPO = 10

DADOS = [ 'partnum-15-1.txt', 'partnum-15-2.txt', 'partnum-15-3.txt', 'partnum-15-4.txt', 'partnum-15-5.txt', 'partnum-35-1.txt', 'partnum-35-2.txt', 'partnum-35-3.txt', 'partnum-35-4.txt', 'partnum-35-5.txt', 'partnum-55-1.txt', 'partnum-55-2.txt', 'partnum-55-3.txt', 'partnum-55-4.txt', 'partnum-55-5.txt', 'partnum-75-1.txt', 'partnum-75-2.txt', 'partnum-75-3.txt', 'partnum-75-4.txt', 'partnum-75-5.txt', 'partnum-95-1.txt', 'partnum-95-2.txt', 'partnum-95-3.txt', 'partnum-95-4.txt', 'partnum-95-5.txt' ]

def carregarDados(arquivo_path):
    with open(arquivo_path, 'r') as file:
        qtdItens = int(file.readline().strip())
        
        conjunto = []
        for i in range(qtdItens):
            numero = int(file.readline().strip())
            conjunto.append(numero)

        return(conjunto)

def avaliaSolucao(solucao, numeros):
    soma1 = sum(n for i, n in enumerate(numeros) if solucao[i] == 1)
    soma2 = sum(n for i, n in enumerate(numeros) if solucao[i] == 0)
    return abs(soma1 - soma2)

def geraSolucaoInicial(n):
    return [random.choice([0, 1]) for _ in range(n)]

def perturbaSolucao(solucao):
    nova_solucao = solucao[:]
    indice = random.randint(0, len(solucao) - 1)
    nova_solucao[indice] = 1 - nova_solucao[indice]
    return nova_solucao

def simulatedAnnealing(numeros):
    n = len(numeros)
    solucaoAtual = geraSolucaoInicial(n)
    melhorSolucao = solucaoAtual[:]
    melhorDiferenca = avaliaSolucao(melhorSolucao, numeros)
    temperatura = TEMP_INICIAL

    while temperatura > TEMP_FINAL:
        for _ in range(ITERACOES_SA):
            novaSolucao = perturbaSolucao(solucaoAtual)
            diferencaAtual = avaliaSolucao(solucaoAtual, numeros)
            novaDiferenca = avaliaSolucao(novaSolucao, numeros)
            delta = novaDiferenca - diferencaAtual

            if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
                solucaoAtual = novaSolucao

            if novaDiferenca < melhorDiferenca:
                melhorSolucao = novaSolucao[:]
                melhorDiferenca = novaDiferenca

        temperatura *= ALFA

    return melhorSolucao, melhorDiferenca

def buscaLocal(solucao, numeros):
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
    melhorSolucao = geraSolucaoInicial(len(numeros))
    melhorDiferenca = avaliaSolucao(melhorSolucao, numeros)

    for _ in range(ITERACOES_GRASP):
        solucao = geraSolucaoInicial(len(numeros))
        solucao, diferenca = buscaLocal(solucao, numeros)

        if diferenca < melhorDiferenca:
            melhorSolucao = solucao[:]
            melhorDiferenca = diferenca

    return melhorSolucao, melhorDiferenca

def comparacao(numeros):
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

conjuntos = [carregarDados(f'./dados/{caminho}') for caminho in DADOS]
for numeros in conjuntos:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(comparacao, numeros)
        try:
            resultado = future.result(timeout=LIMITE_TEMPO)
        except concurrent.futures.TimeoutError:
            print('Tempo limite excedido')