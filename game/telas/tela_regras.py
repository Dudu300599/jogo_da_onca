# game/telas/tela_regras.py
import pygame
from game.config import *
# NÃO importe menus.py aqui no topo do arquivo
from game.telas.tela_base import Tela

class TelaRegras(Tela):
    def desenhar(self):
        self.jogo.screen.blit(self.recursos.regras, (0, 0))
        txt = pygame.font.Font(FONTE_PRINCIPAL, 24).render("Pressione ESC para voltar", True, LARANJA)
        self.jogo.screen.blit(txt, (LARGURA - txt.get_width() - 20, ALTURA - txt.get_height() - 20))

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # CORREÇÃO: Importe o MenuPrincipal exatamente quando for necessário, dentro do método.
                from game.telas.menus import MenuPrincipal
                self.jogo.mudar_estado(MenuPrincipal(self.jogo))

