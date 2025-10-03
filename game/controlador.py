# game/controlador.py
import pygame
from game.config import LARGURA, ALTURA, IMG_ICONE
from game.recursos import Recursos
from game.telas.menus import MenuPrincipal

class Jogo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Jogo da Onça")
        
        try:
            icone = pygame.image.load(IMG_ICONE)
            pygame.display.set_icon(icone)
        except pygame.error as e:
            print(f"Erro ao carregar ícone: {e}")
        
        self.clock = pygame.time.Clock()
        self.recursos = Recursos()
        self.estado_atual = MenuPrincipal(self)

    def mudar_estado(self, novo_estado):
        self.estado_atual = novo_estado

    def run(self):
        while True:
            eventos = pygame.event.get()
            
            self.estado_atual.eventos(eventos)
            self.estado_atual.desenhar()
            
            pygame.display.flip()
            self.clock.tick(60)