# game/telas/telas_creditos.py
import pygame
from game.config import *
# NÃO importe menus.py aqui no topo do arquivo
from game.telas.tela_base import Tela


class TelaCreditos(Tela):
    def desenhar(self):
        screen = self.jogo.screen
        screen.blit(self.recursos.fundo_menu, (0, 0))
        screen.blit(self.recursos.logo, (325, 0))
        linhas = [
            "Desenvolvido por:", "Carlos Santos e Willian Gomes", "",
            "Diretor de Arte:", "Gabriel Ferrari", "",
            "Pressione ESC para voltar ao menu"
        ]
        for i, linha in enumerate(linhas):
            txt = self.recursos.font_creditos.render(linha, True, CREME)
            rect = txt.get_rect(center=(LARGURA / 2, 350 + i * 50))
            screen.blit(txt, rect)

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # CORREÇÃO: Importe o MenuPrincipal exatamente quando for necessário, dentro do método.
                from game.telas.menus import MenuPrincipal
                self.jogo.mudar_estado(MenuPrincipal(self.jogo))