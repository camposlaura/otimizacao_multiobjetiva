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

def solucaoAleatoria(n, q, valores, pesos):
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

def solucaoInteligente(n, q, valores, pesos):
    solucao = [0] * n
    pesoMochila = 0
    valorMochila = 0
    
    proporcao = sorted([(valores[i] / pesos[i], i) for i in range(n)], reverse=True)
    
    for _, i in proporcao:
        if pesoMochila + pesos[i] <= q:
            solucao[i] = 1
            valorMochila += valores[i]
            pesoMochila += pesos[i]
    
    return solucao

def comparacao(n, Q, valores, pesos):
    avalSolucoesAleatorias = []
    avalSolucoesInteligentes = []

    solucoesAleatorias = []
    solucoesInteligentes = []

    for _ in range(10):
        aleatoria = solucaoAleatoria(n, Q, valores, pesos)
        inteligente = solucaoInteligente(n, Q, valores, pesos)

        solucoesAleatorias.append(aleatoria)
        solucoesInteligentes.append(inteligente)
        
        avalSolucoesAleatorias.append(avaliaSolucao(aleatoria, valores, pesos, Q)[0])
        avalSolucoesInteligentes.append(avaliaSolucao(inteligente, valores, pesos, Q)[0])

    # calcula a media dos valores obtidos pelas soluções
    mediaAleatoria = sum(avalSolucoesAleatorias) / len(avalSolucoesAleatorias)
    media_inteligente = sum(avalSolucoesInteligentes) / len(avalSolucoesInteligentes)

    print('\n\n')

    print('A:', solucoesAleatorias)
    print('I:', solucoesInteligentes)

    print('Avaliações Soluções Aleatórias: ', avalSolucoesAleatorias)
    print('Avaliações Soluções Inteligentes: ', avalSolucoesInteligentes)

    print('Média Soluções Aleatórias: ', mediaAleatoria)
    print('Média Soluções Inteligentes: ', media_inteligente)

    print('\n\n')

    
limite_tempo = 2
with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(comparacao, qtdItens, capacidadeMochila, valores, pesos)
    
    try:
        resultado = future.result(timeout=limite_tempo)
        
    except concurrent.futures.TimeoutError:
        resultado = []
        print('Tempo limite excedido')