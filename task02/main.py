import random
import concurrent.futures

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

def solucaoGulosaRandomizada(n, q, valores, pesos, alfa):
    solucao = [0] * n
    pesoMochila = 0
    valorMochila = 0
    
    proporcao = sorted([(valores[i] / pesos[i], i) for i in range(n)], reverse=True)
    itensRestringidos = proporcao[:max(1, int(n * alfa))]

    while itensRestringidos and pesoMochila <= q:
        val, idx = random.choice(itensRestringidos)
        itensRestringidos.remove((val, idx))
        
        if pesoMochila + pesos[idx] <= q:
            solucao[idx] = 1
            pesoMochila += pesos[idx]
            valorMochila += valores[idx]
    
    return solucao

def comparacao(n, Q, valores, pesos):
    avalSolucoes = []

    for a in range(100):
        alfa = a / 100
        inteligente = solucaoGulosaRandomizada(n, Q, valores, pesos, alfa)
        avalSolucoes.append(avaliaSolucao(inteligente, valores, pesos, Q)[0])

    media = sum(avalSolucoes) / len(avalSolucoes)

    print('\n\nAvaliações:', avalSolucoes)
    print('Média das soluções válidas:', media)
    print('\n\n')

limite_tempo = 2
with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(comparacao, qtdItens, capacidadeMochila, valores, pesos)
    
    try:
        resultado = future.result(timeout=limite_tempo)
    except concurrent.futures.TimeoutError:
        resultado = []
        print('Tempo limite excedido')