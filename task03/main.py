import random
import concurrent.futures
import time

with open('./dados.txt', 'r') as file:
    qtdItens = int(file.readline().strip())
    capacidadeMochila = int(file.readline().strip())
    valores = list(map(int, file.readline().strip().split()))
    pesos = list(map(int, file.readline().strip().split()))

def avaliaSolucao(solucao, valores, pesos, q):
    valorMochila = 0
    pesoMochila = 0
    for i in range(len(solucao)):
        if solucao[i]:
            valorMochila += valores[i]
            pesoMochila += pesos[i]
    if pesoMochila > q:
        return 0, pesoMochila
    return valorMochila, pesoMochila

def geraSolucaoInicial(n, q, valores, pesos):
    solucao = [0] * n
    pesoMochila = 0
    valorMochila = 0
    
    for i in range(n):
        adiciona = random.randint(0, 1)
        if adiciona and pesoMochila + pesos[i] <= q:
            solucao[i] = 1
            valorMochila += valores[i]
            pesoMochila += pesos[i]
    
    return solucao

def gerarVizinhanca(solucao):
    vizinhanca = []
    for i in range(len(solucao)):
        vizinho = solucao[:]
        vizinho[i] = 1 - solucao[i]
        vizinhanca.append(vizinho)
    return vizinhanca

def hillClimbingBest(Q, valores, pesos, solucaoInicial):
    solucaoAtual = solucaoInicial
    valorAtual, _ = avaliaSolucao(solucaoAtual, valores, pesos, Q)

    while True:
        vizinhanca = gerarVizinhanca(solucaoAtual)
        melhorVizinho = None
        melhorValor = valorAtual

        for vizinho in vizinhanca:
            valorVizinho, _ = avaliaSolucao(vizinho, valores, pesos, Q)
            if valorVizinho > melhorValor:
                melhorValor = valorVizinho
                melhorVizinho = vizinho

        if melhorVizinho is None:
            break

        solucaoAtual = melhorVizinho
        valorAtual = melhorValor

    return solucaoAtual, valorAtual

def hillClimbingFirst(Q, valores, pesos, solucaoInicial):
    solucaoAtual = solucaoInicial
    valorAtual, _ = avaliaSolucao(solucaoAtual, valores, pesos, Q)

    while True:
        vizinhanca = gerarVizinhanca(solucaoAtual)
        melhorou = False

        for vizinho in vizinhanca:
            valorVizinho, _ = avaliaSolucao(vizinho, valores, pesos, Q)
            if valorVizinho > valorAtual:
                solucaoAtual = vizinho
                valorAtual = valorVizinho
                melhorou = True
                break

        if not melhorou:
            break

    return solucaoAtual, valorAtual

def comparacao(n, Q, valores, pesos):
    avalBest = []
    avalFirst = []

    tempoBest = 0
    tempoFirst = 0

    for _ in range(1000):
        solucaoInicial = geraSolucaoInicial(n, Q, valores, pesos)

        inicioBest = time.time()
        _, valorBest = hillClimbingBest(Q, valores, pesos, solucaoInicial)
        fimBest = time.time()
        tempoBest += (fimBest - inicioBest)
        avalBest.append(valorBest)

        inicioFirst = time.time()
        _, valorFirst = hillClimbingFirst(Q, valores, pesos, solucaoInicial)
        fimFirst = time.time()
        tempoFirst += (fimFirst - inicioFirst)
        avalFirst.append(valorFirst)

    mediaBest = sum(avalBest) / len(avalBest)
    mediaFirst = sum(avalFirst) / len(avalFirst)

    print(f'\nMédia Best Improvement: {mediaBest}')
    print(f'Tempo Médio Best Improvement: {tempoBest / 1000:.6f} segundos')
    print(f'Média First Improvement: {mediaFirst}')
    print(f'Tempo Médio First Improvement: {tempoFirst / 1000:.6f} segundos\n')

limite_tempo = 2

with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(comparacao, qtdItens, capacidadeMochila, valores, pesos)

    try:
        resultado = future.result(timeout=limite_tempo)
    except concurrent.futures.TimeoutError:
        print('Tempo limite excedido')
