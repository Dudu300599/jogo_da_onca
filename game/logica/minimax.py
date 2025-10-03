# game/logica/minimax.py
import random
from collections import deque
from game.config import ONCA, CACHORRO, VAZIO, MATRIZ_JOGO, SALTOS_ONCA
from game.logica.movimentos import (
    condicao_vitoria, gerar_estados_futuros_onca,
    gerar_estados_futuros_cachorros, condicao_vitoria)
from game.logica.utilidades import *

def minimax_cachorro(estado_atual, maximizador, profundidade,func_utilidade_c, func_utilidade_o, alpha=float('-inf'), beta=float('inf')):


    # Checar condição de parada (profundidade ou vitória)
    # Verifica vitória imediata
    resultado = condicao_vitoria(estado_atual)
    if resultado == "Vitória dos Cachorros":
        # vitória dos cachorros = muito bom para eles, muito ruim para a onça
        return 1000000 + profundidade, estado_atual

    elif resultado == "Vitória da Onça":
        return -1000000 - profundidade, estado_atual
    
    # Caso base: profundidade chegou a 0
    if profundidade == 0:
        if maximizador:
            utilidade = func_utilidade_c(estado_atual)
        else:
            utilidade = func_utilidade_o(estado_atual)
        return utilidade, estado_atual

    
    if maximizador:
        maior_avaliacao = float('-inf')
        melhores_estados = []
        for filho in gerar_estados_futuros_cachorros(estado_atual):
            avaliacao, _ = minimax_cachorro(filho, False, profundidade - 1, func_utilidade_c, func_utilidade_o, alpha, beta)
            if avaliacao > maior_avaliacao:
                maior_avaliacao = avaliacao
                melhores_estados = [filho]
            elif avaliacao == maior_avaliacao:
                melhores_estados.append(filho)
            
            alpha = max(alpha, avaliacao)
            if beta <= alpha:
                break  # poda beta

        melhor_estado = random.choice(melhores_estados)
        #print(f"Valor: {maior_avaliacao}, Melhor Posição: {melhor_estado.index(-1)}, Estado do tabuleiro: {melhor_estado}")
        return maior_avaliacao, melhor_estado

    else:
        menor_avaliacao = float('inf')
        melhores_estados = []
        for filho in gerar_estados_futuros_onca(estado_atual):
            avaliacao, _ = minimax_cachorro(filho, True, profundidade - 1, func_utilidade_c, func_utilidade_o, alpha, beta)
            if avaliacao < menor_avaliacao:
                menor_avaliacao = avaliacao
                melhores_estados = [filho]
            elif avaliacao == menor_avaliacao:
                melhores_estados.append(filho)
            
            beta = min(beta, avaliacao)
            if beta <= alpha:
                break  # poda alfa

        melhor_estado = random.choice(melhores_estados)
        #print(f"Valor: {menor_avaliacao}, Posição: {melhor_estado.index(-1)}, Estado do tabuleiro: {melhor_estado}")
        return menor_avaliacao, melhor_estado
    
    #Função minimax retorna a melhor jogada com base na função objetiva
#Tem como entrada o estado atual do jogo, um booleano para identificar qual jogador será maximizado e a profundidade da árvore gerada.
def minimax_onca(estado_atual, maximizador, profundidade, func_utilidade_c, func_utilidade_o, alpha=float('-inf'), beta=float('inf')):

    # Checar condição de parada (profundidade ou vitória)
    if profundidade == 0 or condicao_vitoria(estado_atual) in ["Vitória dos Cachorros", "Vitória da Onça"]:
        if maximizador:
            utilidade = func_utilidade_o(estado_atual)
        else:
            utilidade = func_utilidade_c(estado_atual)
        return utilidade, estado_atual

    if maximizador:
        maior_avaliacao = float('-inf')
        melhores_estados = []
        for filho in gerar_estados_futuros_onca(estado_atual):
            avaliacao, _ = minimax_onca(filho, False, profundidade - 1, func_utilidade_c, func_utilidade_o, alpha, beta)
            if avaliacao > maior_avaliacao:
                maior_avaliacao = avaliacao
                melhores_estados = [filho]
            elif avaliacao == maior_avaliacao:
                melhores_estados.append(filho)
            
            alpha = max(alpha, avaliacao)
            if beta <= alpha:
                break  # poda beta

        melhor_estado = random.choice(melhores_estados)
        #print(f"Valor: {maior_avaliacao}, Melhor Posição: {melhor_estado.index(-1)}, Estado do tabuleiro: {melhor_estado}")
        return maior_avaliacao, melhor_estado

    else:
        menor_avaliacao = float('inf')
        melhores_estados = []
        for filho in gerar_estados_futuros_cachorros(estado_atual):
            avaliacao, _ = minimax_onca(filho, True, profundidade - 1, func_utilidade_c, func_utilidade_o, alpha, beta)
            if avaliacao < menor_avaliacao:
                menor_avaliacao = avaliacao
                melhores_estados = [filho]
            elif avaliacao == menor_avaliacao:
                melhores_estados.append(filho)
            
            beta = min(beta, avaliacao)
            if beta <= alpha:
                break  # poda alfa

        melhor_estado = random.choice(melhores_estados)
        #print(f"Valor: {menor_avaliacao}, Posição: {melhor_estado.index(-1)}, Estado do tabuleiro: {melhor_estado}")
        return menor_avaliacao, melhor_estado
