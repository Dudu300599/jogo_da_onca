# game/recursos.py
import pygame
from game.config import FONTE_PRINCIPAL, IMG_FUNDO_MENU, LARGURA, ALTURA, IMG_LOGO, IMG_REGRAS, IMG_PECA_ONCA, IMG_PECA_CACHORRO, IMG_FUNDO_JOGO


class Recursos:
    def __init__(self):
        # --- Carregar Fontes ---
        self.font = pygame.font.Font(FONTE_PRINCIPAL, 60)
        self.font_pequena = pygame.font.Font(FONTE_PRINCIPAL, 45)
        self.font_creditos = pygame.font.Font(FONTE_PRINCIPAL, 35)
        self.fonte_grande = pygame.font.Font(FONTE_PRINCIPAL, 90)
        self.font_dropdown = pygame.font.SysFont(None, 28)
        self.font_sys_36 = pygame.font.SysFont(None, 36)
        self.font_sys_40 = pygame.font.SysFont(None, 40)

        # --- Carregar Imagens ---
        self.fundo_menu = pygame.transform.scale(pygame.image.load(IMG_FUNDO_MENU), (LARGURA, ALTURA))
        self.logo = pygame.transform.scale(pygame.image.load(IMG_LOGO), (600, 337))
        self.regras = pygame.transform.scale(pygame.image.load(IMG_REGRAS), (LARGURA, ALTURA))

        # --- Recursos do Jogo ---
        self.peca_onca = pygame.transform.scale(pygame.image.load(IMG_PECA_ONCA), (50, 50))
        self.peca_cachorro = pygame.transform.scale(pygame.image.load(IMG_PECA_CACHORRO), (50, 50))
        self.fundo_jogo = pygame.transform.scale(pygame.image.load(IMG_FUNDO_JOGO).convert(), (LARGURA, ALTURA))