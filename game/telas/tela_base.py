# game/telas/tela_base.py
import pygame

class Tela:
    def __init__(self, jogo):
        self.jogo = jogo
        self.recursos = jogo.recursos

    def desenhar(self):
        raise NotImplementedError

    def eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()