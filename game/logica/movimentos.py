# game/logica/movimentos.py
import random
from game.config import MATRIZ_JOGO, SALTOS_ONCA, ONCA, CACHORRO, VAZIO

def movimentos_validos_onca(posicao_onca, estado_atual):
    movimentos_possiveis = []
    # Movimentos normais
    for i in range(len(MATRIZ_JOGO)):
        if MATRIZ_JOGO[posicao_onca][i] == 1 and estado_atual[i] == VAZIO:
            movimentos_possiveis.append(i)

    # Saltos (capturas)
    for destino, meio in SALTOS_ONCA.get(posicao_onca, []):
        if estado_atual[meio] == CACHORRO and estado_atual[destino] == VAZIO:
            movimentos_possiveis.append(destino)
    return movimentos_possiveis

def movimentos_validos_cachorros(posicao_cachorro, estado_atual):
    movimentos_possiveis = []
    for i in range(len(MATRIZ_JOGO)):
        if MATRIZ_JOGO[posicao_cachorro][i] == 1 and estado_atual[i] == VAZIO:
            movimentos_possiveis.append(i)
    return movimentos_possiveis

def condicao_vitoria(estado_atual):
    posicao_onca = estado_atual.index(ONCA)
    qnt_cachorros = estado_atual.count(CACHORRO)
    
    if qnt_cachorros <= 9:
        return "Vitória da Onça"
    if not movimentos_validos_onca(posicao_onca, estado_atual):
        return "Vitória dos Cachorros"
    return None

def gerar_estados_futuros_onca(estado_atual):
    filhos = []
    posicao_onca = estado_atual.index(ONCA)
    movimentos = movimentos_validos_onca(posicao_onca, estado_atual)

    for pos_destino in movimentos:
        novo_estado = list(estado_atual)
        novo_estado[posicao_onca] = VAZIO
        novo_estado[pos_destino] = ONCA

        # Se for um salto, remove o cachorro do meio
        is_salto = any(pos_destino == d for d, _ in SALTOS_ONCA.get(posicao_onca, []))
        if is_salto:
            for destino, meio in SALTOS_ONCA.get(posicao_onca, []):
                if destino == pos_destino and estado_atual[meio] == CACHORRO:
                    novo_estado[meio] = VAZIO
                    break
        filhos.append(novo_estado)
    return filhos

def gerar_estados_futuros_cachorros(estado_atual):
    filhos = []
    for posicao, peca in enumerate(estado_atual):
        if peca == CACHORRO:
            destinos_validos = movimentos_validos_cachorros(posicao, estado_atual)
            for destino in destinos_validos:
                novo_estado = list(estado_atual)
                novo_estado[posicao] = VAZIO
                novo_estado[destino] = CACHORRO
                filhos.append(novo_estado)
    return filhos

def falta_de_combatividade(historico_movimentos):
    C = set()
    p = 0
    for movimento in historico_movimentos:
        movimento_tupla = tuple(sorted(movimento)) # (origem, destino)
        if movimento_tupla in C:
            p += 1
        else:
            C.add(movimento_tupla)
    return p >= len(C) / 2