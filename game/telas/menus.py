# game/telas/menus.py
import pygame
from game.config import *
from game.telas.tela_base import Tela
from game.telas.tela_regras import TelaRegras
from game.telas.tela_creditos import TelaCreditos
from game.telas.tela_jogo import TelaJogo
from game.logica.utilidades import *

UTILIDADES = {
    "utilidade_onca_0": utilidade_onca_0, "utilidade_onca_1": utilidade_onca_1, "utilidade_onca_2": utilidade_onca_2,
    "utilidade_cachorro_0": utilidade_cachorros_0, "utilidade_cachorro_1": utilidade_cachorros_1,
    "utilidade_cachorro_2": utilidade_cachorros_2, "utilidade_cachorro_3": utilidade_cachorros_3
}

class MenuPrincipal(Tela):
    def desenhar(self):
        screen = self.jogo.screen
        screen.blit(self.recursos.fundo_menu, (0, 0))
        screen.blit(self.recursos.logo, (325, 0))
        self.botoes = []
        opcoes = ["Jogar", "Regras", "Creditos"]
        mouse = pygame.mouse.get_pos()
        for i, texto in enumerate(opcoes):
            rect = self.recursos.font.render(texto, True, CREME).get_rect(center=(625, 350 + i * 80))
            cor = VERDE_CLARO if rect.collidepoint(mouse) else CREME
            txt = self.recursos.font.render(texto, True, cor)
            screen.blit(txt, rect)
            self.botoes.append((texto, rect))

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for texto, rect in self.botoes:
                    if rect.collidepoint(event.pos):
                        if texto == "Jogar": self.jogo.mudar_estado(MenuJogar(self.jogo))
                        elif texto == "Regras": self.jogo.mudar_estado(TelaRegras(self.jogo))
                        elif texto == "Creditos": self.jogo.mudar_estado(TelaCreditos(self.jogo))

class MenuJogar(Tela):
    def desenhar(self):
        screen = self.jogo.screen
        screen.blit(self.recursos.fundo_menu, (0, 0))
        screen.blit(self.recursos.logo, (325, 0))
        self.botoes = []
        opcoes = ["Player vs Player", "Player vs Comp", "Comp vs Comp"]
        mouse = pygame.mouse.get_pos()
        for i, texto in enumerate(opcoes):
            rect = self.recursos.font_pequena.render(texto, True, CREME).get_rect(center=(625, 350 + i * 80))
            cor = VERDE_CLARO if rect.collidepoint(mouse) else CREME
            txt = self.recursos.font_pequena.render(texto, True, cor)
            screen.blit(txt, rect)
            self.botoes.append((texto, rect))

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.jogo.mudar_estado(MenuPrincipal(self.jogo))
            if event.type == pygame.MOUSEBUTTONDOWN:
                for texto, rect in self.botoes:
                    if rect.collidepoint(event.pos):
                        if texto == "Player vs Player":
                            self.jogo.mudar_estado(TelaJogo(self.jogo, modo_jogo='pvp'))
                        elif texto == "Player vs Comp":
                            self.jogo.mudar_estado(MenuSelecaoPlayervsComp(self.jogo))
                        elif texto == "Comp vs Comp":
                            self.jogo.mudar_estado(MenuSelecaoCompvsComp(self.jogo))

class MenuSelecaoPlayervsComp(Tela):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.input_rect = pygame.Rect(1000, 490, 40, 40)
        self.active = False
        self.text = "3" # Profundidade padrão

    def desenhar(self):
        screen = self.jogo.screen
        screen.blit(self.recursos.fundo_menu, (0, 0))
        screen.blit(self.recursos.logo, (325, 0))
        self.botoes = []
        opcoes = ["Jogar como Onca", "Jogar como Cachorros", "Nivel de profundidade:"]
        mouse = pygame.mouse.get_pos()
        for i, texto in enumerate(opcoes):
            rect = self.recursos.font.render(texto, True, CREME).get_rect(center=(625, 350 + i * 80))
            cor = VERDE_CLARO if rect.collidepoint(mouse) and i < 2 else CREME
            txt = self.recursos.font.render(texto, True, cor)
            screen.blit(txt, rect)
            if i < 2: self.botoes.append((texto, rect))

        pygame.draw.rect(screen, VERDE_CLARO if self.active else CINZA, self.input_rect, border_radius=5)
        txt_surface = self.recursos.font_dropdown.render(self.text, True, PRETO)
        screen.blit(txt_surface, (self.input_rect.x + 10, self.input_rect.y + 10))

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.jogo.mudar_estado(MenuJogar(self.jogo))
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.input_rect.collidepoint(event.pos)
                for texto, rect in self.botoes:
                    if rect.collidepoint(event.pos):
                        try:
                            profundidade = int(self.text)
                            if profundidade > 0:
                                if texto == "Jogar como Onca":
                                    self.jogo.mudar_estado(TelaJogo(self.jogo, modo_jogo='p_vs_c', profundidade_ia=profundidade, jogador_ia=CACHORRO))
                                elif texto == "Jogar como Cachorros":
                                    self.jogo.mudar_estado(TelaJogo(self.jogo, modo_jogo='p_vs_o', profundidade_ia=profundidade, jogador_ia=ONCA))
                        except ValueError:
                            pass
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
                elif event.unicode.isdigit(): self.text += event.unicode
                if len(self.text) > 2: self.text = self.text[:2]

class MenuSelecaoCompvsComp(Tela):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.input_onca_text, self.input_cachorro_text = "3", "3"
        self.input_onca_rect = pygame.Rect(450, 535, 120, 40)
        self.input_cachorro_rect = pygame.Rect(1130, 535, 120, 40)
        self.active_onca, self.active_cachorro = False, False
        self.utilidade_onca_nome = "utilidade_onca_2"
        self.utilidade_cachorro_nome = "utilidade_cachorro_3"
        
    def desenhar(self):
        screen = self.jogo.screen
        screen.blit(self.recursos.fundo_menu, (0, 0))
        screen.blit(self.recursos.logo, (325, 0))
        mouse = pygame.mouse.get_pos()
        fonte = self.recursos.font
        fonte_celula = self.recursos.font_dropdown

        screen.blit(fonte.render("Onca", True, CREME), (256, 250))
        screen.blit(fonte.render("Cachorro", True, CREME), (800, 250))
        pygame.draw.line(screen, CREME, (640, 250), (640, 600), 3)

        self.retangulos_onca, self.retangulos_cachorro = [], []

        # Opções Onça
        for i, nome in enumerate(["utilidade_onca_0", "utilidade_onca_1", "utilidade_onca_2"]):
            rect = pygame.Rect(150 + i * 120, 350, 100, 40)
            cor = VERDE_CLARO if self.utilidade_onca_nome == nome else CINZA
            pygame.draw.rect(screen, cor, rect, border_radius=5)
            texto = fonte_celula.render(nome.split('_')[-1], True, PRETO)
            screen.blit(texto, texto.get_rect(center=rect.center))
            self.retangulos_onca.append((nome, rect))
        
        # Opções Cachorro
        for i, nome in enumerate(["utilidade_cachorro_0", "utilidade_cachorro_1", "utilidade_cachorro_2", "utilidade_cachorro_3"]):
            x = 830 + (i % 2) * 120
            y = 350 + (i // 2) * 50
            rect = pygame.Rect(x, y, 100, 40)
            cor = VERDE_CLARO if self.utilidade_cachorro_nome == nome else CINZA
            pygame.draw.rect(screen, cor, rect, border_radius=5)
            texto = fonte_celula.render(nome.split('_')[-1], True, PRETO)
            screen.blit(texto, texto.get_rect(center=rect.center))
            self.retangulos_cachorro.append((nome, rect))

        # Inputs de Profundidade
        screen.blit(fonte.render("Profundidade:", True, CREME), self.input_onca_rect.move(-280, 0))
        pygame.draw.rect(screen, VERDE_CLARO if self.active_onca else CINZA, self.input_onca_rect, border_radius=5)
        screen.blit(fonte_celula.render(self.input_onca_text, True, PRETO), self.input_onca_rect.move(10, 10))
        
        screen.blit(fonte.render("Profundidade:", True, CREME), self.input_cachorro_rect.move(-290, 0))
        pygame.draw.rect(screen, VERDE_CLARO if self.active_cachorro else CINZA, self.input_cachorro_rect, border_radius=5)
        screen.blit(fonte_celula.render(self.input_cachorro_text, True, PRETO), self.input_cachorro_rect.move(10, 10))

        # Botão Iniciar
        self.botao_iniciar_rect = fonte.render("Iniciar Jogo", True, CREME).get_rect(center=(625, 660))
        cor = VERDE_CLARO if self.botao_iniciar_rect.collidepoint(mouse) else CREME
        screen.blit(fonte.render("Iniciar Jogo", True, cor), self.botao_iniciar_rect)

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.jogo.mudar_estado(MenuJogar(self.jogo))
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active_onca = self.input_onca_rect.collidepoint(event.pos)
                self.active_cachorro = self.input_cachorro_rect.collidepoint(event.pos)
                
                for nome, rect in self.retangulos_onca:
                    if rect.collidepoint(event.pos): self.utilidade_onca_nome = nome
                for nome, rect in self.retangulos_cachorro:
                    if rect.collidepoint(event.pos): self.utilidade_cachorro_nome = nome
                
                if self.botao_iniciar_rect.collidepoint(event.pos):
                    try:
                        p_onca = int(self.input_onca_text)
                        p_cachorro = int(self.input_cachorro_text)
                        if p_onca > 0 and p_cachorro > 0:
                            self.jogo.mudar_estado(TelaJogo(self.jogo, modo_jogo='cvc',
                                                            profundidade_onca=p_onca,
                                                            profundidade_cachorros=p_cachorro,
                                                            utilidade_onca=UTILIDADES[self.utilidade_onca_nome],
                                                            utilidade_cachorro=UTILIDADES[self.utilidade_cachorro_nome]))
                    except ValueError: pass

            if event.type == pygame.KEYDOWN:
                if self.active_onca: self.input_onca_text = self._handle_text_input(event, self.input_onca_text)
                elif self.active_cachorro: self.input_cachorro_text = self._handle_text_input(event, self.input_cachorro_text)

    def _handle_text_input(self, event, text):
        if event.key == pygame.K_BACKSPACE: return text[:-1]
        if event.unicode.isdigit() and len(text) < 2: return text + event.unicode
        return text