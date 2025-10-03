# game/logica/estado_jogo.py
from game.config import ONCA, CACHORRO, VAZIO, SALTOS_ONCA
from game.logica.movimentos import movimentos_validos_onca

class Partida:
    def __init__(self):
        self.reiniciar()

    def get_tabuleiro_inicial(self):
        tabuleiro = [VAZIO] * 31
        tabuleiro[12] = ONCA
        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14]:
            tabuleiro[i] = CACHORRO
        return tabuleiro

    def reiniciar(self):
        self.tabuleiro = self.get_tabuleiro_inicial()
        self.turno = ONCA
        self.capturados = 0
        self.fim_de_jogo = False
        self.vencedor = None
        self.cont_turno = 0
        self.historico_onca = []
        self.historico_cachorros = []
        self.historico_partida = []
        self.historico_estados_jogo = []

    def trocar_turno(self):
        self.turno *= -1
        self.cont_turno += 1

    def mover_peca(self, from_idx, to_idx):
        peca = self.tabuleiro[from_idx]

        # Movimento de captura da onça
        if peca == ONCA:
            movimentos_onca = movimentos_validos_onca(from_idx, self.tabuleiro)
            if to_idx in movimentos_onca:
                # Verifica se é um salto (não adjacente)
                is_salto = any(to_idx == destino for destino, _ in SALTOS_ONCA.get(from_idx, []))
                
                if is_salto:
                    for destino, meio in SALTOS_ONCA.get(from_idx, []):
                        if destino == to_idx and self.tabuleiro[meio] == CACHORRO:
                            self.tabuleiro[meio] = VAZIO
                            self.capturados += 1
                            break
        
        # Move a peça para a nova posição
        self.tabuleiro[to_idx] = self.tabuleiro[from_idx]
        self.tabuleiro[from_idx] = VAZIO
        return True