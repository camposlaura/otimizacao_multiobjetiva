import concurrent.futures
import random
import math
import time

TEMP_INICIAL = 500
TEMP_FINAL = 1
ALFA = 0.95
ITERACOES_SA = 1000

ITERACOES_GRASP = 1000

LIMITE_TEMPO = 10

with open('./dados.txt', 'r') as file:
    qtdItens = int(file.readline().strip())
    capacidade = int(file.readline().strip())
    valores = list(map(int, file.readline().strip().split()))
    pesos = list(map(int, file.readline().strip().split()))

def avaliaSolucaoMochila(solucao, valores, pesos, capacidade):
    valorMochila = 0
    pesoMochila = 0
    for i in range(len(solucao)):
        if solucao[i]:
            valorMochila += valores[i]
            pesoMochila += pesos[i]
    if pesoMochila > capacidade:
        return 0
    return valorMochila

def geraSolucaoInicialMochila(n, capacidade, pesos):
    solucao = [0] * n
    for i in range(n):
        if random.randint(0, 1) and sum([solucao[j] * pesos[j] for j in range(n)]) + pesos[i] <= capacidade:
            solucao[i] = 1
    return solucao

def perturbaSolucaoMochila(solucao):
    nova_solucao = solucao[:]
    indice = random.randint(0, len(solucao) - 1)
    nova_solucao[indice] = 1 - nova_solucao[indice]
    return nova_solucao

def simulatedAnnealingMochila(valores, pesos, capacidade):
    n = len(valores)
    solucaoAtual = geraSolucaoInicialMochila(n, capacidade, pesos)
    melhorSolucao = solucaoAtual[:]
    melhorValor = avaliaSolucaoMochila(melhorSolucao, valores, pesos, capacidade)
    temperatura = TEMP_INICIAL

    while temperatura > TEMP_FINAL:
        for _ in range(ITERACOES_SA):
            novaSolucao = perturbaSolucaoMochila(solucaoAtual)
            valorAtual = avaliaSolucaoMochila(solucaoAtual, valores, pesos, capacidade)
            novoValor = avaliaSolucaoMochila(novaSolucao, valores, pesos, capacidade)
            delta = novoValor - valorAtual

            if delta > 0 or random.uniform(0, 1) < math.exp(delta / temperatura):
                solucaoAtual = novaSolucao

            if novoValor > melhorValor:
                melhorSolucao = novaSolucao[:]
                melhorValor = novoValor

        temperatura *= ALFA

    return melhorSolucao, melhorValor

def construirSolucaoGRASP(valores, pesos, capacidade):
    n = len(valores)
    solucao = [0] * n
    for i in range(n):
        if random.randint(0, 1) and sum([solucao[j] * pesos[j] for j in range(n)]) + pesos[i] <= capacidade:
            solucao[i] = 1
    return solucao

def buscaLocalMochila(solucao, valores, pesos, capacidade):
    melhorSolucao = solucao[:]
    melhorValor = avaliaSolucaoMochila(melhorSolucao, valores, pesos, capacidade)

    for i in range(len(solucao)):
        novaSolucao = solucao[:]
        novaSolucao[i] = 1 - novaSolucao[i]
        novoValor = avaliaSolucaoMochila(novaSolucao, valores, pesos, capacidade)

        if novoValor > melhorValor:
            melhorSolucao = novaSolucao[:]
            melhorValor = novoValor

    return melhorSolucao, melhorValor

def graspMochila(valores, pesos, capacidade):
    melhorSolucao = construirSolucaoGRASP(valores, pesos, capacidade)
    melhorValor = avaliaSolucaoMochila(melhorSolucao, valores, pesos, capacidade)

    for _ in range(ITERACOES_GRASP):
        solucao = construirSolucaoGRASP(valores, pesos, capacidade)
        solucao, valor = buscaLocalMochila(solucao, valores, pesos, capacidade)

        if valor > melhorValor:
            melhorSolucao = solucao[:]
            melhorValor = valor

    return melhorSolucao, melhorValor

def comparacaoMochila(valores, pesos, capacidade):
    tempoSA, tempoGRASP = 0, 0
    resultadosSA, resultadosGRASP = [], []

    # Simulated Annealing
    inicioSA = time.time()
    solucaoSA, valorSA = simulatedAnnealingMochila(valores, pesos, capacidade)
    tempoSA += time.time() - inicioSA
    resultadosSA.append(valorSA)

    # GRASP
    inicioGRASP = time.time()
    solucaoGRASP, valorGRASP = graspMochila(valores, pesos, capacidade)
    tempoGRASP += time.time() - inicioGRASP
    resultadosGRASP.append(valorGRASP)

    mediaSA = sum(resultadosSA) / len(resultadosSA)
    mediaGRASP = sum(resultadosGRASP) / len(resultadosGRASP)

    print(f'\nMédia Simulated Annealing: {mediaSA}')
    print(f'Tempo Médio Simulated Annealing: {tempoSA:.6f} segundos')
    print(f'Média GRASP: {mediaGRASP}')
    print(f'Tempo Médio GRASP: {tempoGRASP:.6f} segundos\n')

with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(comparacaoMochila, valores, pesos, capacidade)

    try:
        resultado = future.result(timeout=LIMITE_TEMPO)
    except concurrent.futures.TimeoutError:
        print('Tempo limite excedido')
