import random
from collections import deque
from game.config import ONCA, CACHORRO, VAZIO, MATRIZ_JOGO, SALTOS_ONCA
from game.logica.movimentos import (
    condicao_vitoria, gerar_estados_futuros_onca,
    gerar_estados_futuros_cachorros, movimentos_validos_onca
)

# --- Funções de Utilidade (sem alterações) ---

def utilidade_onca_0(estado_atual):
    movimentos = gerar_estados_futuros_onca(estado_atual)
    return random.choice(movimentos) if movimentos else estado_atual

def utilidade_onca_1(estado_atual):
    qnt_cachorros = estado_atual.count(CACHORRO)
    capturas = 14 - qnt_cachorros
    return capturas * 200

def utilidade_onca_2(estado_atual):
    qnt_cachorros = estado_atual.count(CACHORRO)
    capturas = 14 - qnt_cachorros
    posicao_onca = estado_atual.index(ONCA)
    qnt_movimentos = len(movimentos_validos_onca(posicao_onca, estado_atual))
    return capturas * 200 + qnt_movimentos * 10

def utilidade_cachorros_0(estado_atual):
    movimentos = gerar_estados_futuros_cachorros(estado_atual)
    return random.choice(movimentos) if movimentos else estado_atual

def utilidade_cachorros_1(estado_atual):
    t, p = 0, 0
    posicao_onca = estado_atual.index(ONCA)
    for i in range(len(MATRIZ_JOGO)):
        if MATRIZ_JOGO[posicao_onca][i] == 1 and estado_atual[i] == CACHORRO:
            t += 1
            pode_ser_capturado = any(meio == i and estado_atual[destino] == VAZIO for destino, meio in SALTOS_ONCA.get(posicao_onca, []))
            if not pode_ser_capturado:
                p += 1
    return int(1000 * (p / t)) if t > 0 else 0

def utilidade_cachorros_2(estado_atual):
    posicao_onca = estado_atual.index(ONCA)
    visitado = {posicao_onca}
    fila = deque([posicao_onca])
    area = 0
    while fila:
        casa = fila.popleft()
        area += 1
        for vizinha in range(len(MATRIZ_JOGO[casa])):
            if MATRIZ_JOGO[casa][vizinha] == 1 and vizinha not in visitado and estado_atual[vizinha] == VAZIO:
                fila.append(vizinha)
                visitado.add(vizinha)
    valor = 1000 - (area * 100)
    return max(-1000, min(1000, valor))

def utilidade_cachorros_3(estado_atual):
    valor = 0.6 * utilidade_cachorros_1(estado_atual) + 0.4 * utilidade_cachorros_2(estado_atual)
    return int(max(-1000, min(1000, valor)))