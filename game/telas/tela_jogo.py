# game/telas/tela_jogo.py
import pygame, sys, time, copy
from game.config import *
from game.telas.tela_base import Tela
from game.logica.estado_jogo import Partida
from game.logica.movimentos import *
# Importa tudo que podemos precisar da IA
from game.utils.logger import salvar_log
from game.logica.utilidades import *
from game.logica.minimax import *

class TelaJogo(Tela):
    def __init__(self, jogo, modo_jogo, **kwargs):
        super().__init__(jogo)
        self.partida = Partida()
        self.modo_jogo = modo_jogo
        self.selected_vertex = None
        self.aguardando_ia = False
        self.tempo_inicio_ia = 0
        
        # Configurações da IA
        self.jogador_ia = kwargs.get('jogador_ia', None)
        self.profundidade_ia = kwargs.get('profundidade_ia', 3)
        self.profundidade_onca = kwargs.get('profundidade_onca', 3)
        self.profundidade_cachorros = kwargs.get('profundidade_cachorros', 3)
        self.utilidade_onca = kwargs.get('utilidade_onca', utilidade_onca_1)
        self.utilidade_cachorro = kwargs.get('utilidade_cachorro', utilidade_cachorros_1)

    def eventos(self, eventos):
        super().eventos(eventos)
        for event in eventos:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from game.telas.menus import MenuPrincipal
                self.jogo.mudar_estado(MenuPrincipal(self.jogo))
                return

            if self.partida.fim_de_jogo: continue

            is_turno_humano = (self.modo_jogo == 'pvp' or
                               (self.modo_jogo in ['p_vs_c', 'p_vs_o'] and self.partida.turno != self.jogador_ia))

            if event.type == pygame.MOUSEBUTTONDOWN and is_turno_humano:
                self.handle_click(pygame.mouse.get_pos())

        is_turno_ia = not self.partida.fim_de_jogo and (self.partida.turno == self.jogador_ia or self.modo_jogo == 'cvc')
        if is_turno_ia:
            self.handle_turno_ia()
            
    def handle_click(self, mouse_pos):
        idx = self.get_vertex_clicked(mouse_pos)
        if idx is None:
            self.selected_vertex = None
            return

        if self.selected_vertex is None:
            if self.partida.tabuleiro[idx] == self.partida.turno:
                self.selected_vertex = idx
        else:
            if self.is_movimento_valido(self.selected_vertex, idx):
                self.executar_movimento(self.selected_vertex, idx, "Humano")
            self.selected_vertex = None

    def handle_turno_ia(self):
        if not self.aguardando_ia:
            self.tempo_inicio_ia = pygame.time.get_ticks()
            self.aguardando_ia = True
        
        if pygame.time.get_ticks() - self.tempo_inicio_ia > 500:
            inicio = time.time()
            nos_visitados_cont = 0
            melhor_jogada = None
            
            # --- LÓGICA DE ESCOLHA: JOGADA ALEATÓRIA (UTILIDADE 0) OU MINIMAX ---
            is_onca_random = (self.partida.turno == ONCA and self.utilidade_onca == utilidade_onca_0)
            is_cachorro_random = (self.partida.turno == CACHORRO and self.utilidade_cachorro == utilidade_cachorros_0)

            if is_onca_random:
                melhor_jogada = utilidade_onca_0(self.partida.tabuleiro)
            elif is_cachorro_random:
                melhor_jogada = utilidade_cachorros_0(self.partida.tabuleiro)
            else:
                # --- COMPORTAMENTO MINIMAX COM TRATAMENTO PARA OPONENTE ALEATÓRIO ---
                
                # 1. Prepara as funções de utilidade para o Minimax
                # Se a função da Onça for aleatória, usa uma padrão. Senão, usa a escolhida.
                onca_func_para_minimax = self.utilidade_onca
                if onca_func_para_minimax == utilidade_onca_0:
                    onca_func_para_minimax = utilidade_onca_1 # Padrão
                
                # Se a função do Cachorro for aleatória, usa uma padrão. Senão, usa a escolhida.
                cachorro_func_para_minimax = self.utilidade_cachorro
                if cachorro_func_para_minimax == utilidade_cachorros_0:
                    cachorro_func_para_minimax = utilidade_cachorros_1 # Padrão

                # 2. Chama o Minimax correto com as funções já tratadas
                if self.partida.turno == ONCA:
                    profundidade = self.profundidade_onca
                    _, melhor_jogada = minimax_onca(
                        self.partida.tabuleiro, True, profundidade, 
                        cachorro_func_para_minimax, onca_func_para_minimax
                    )
                else: # Turno do Cachorro
                    profundidade = self.profundidade_cachorros
                    _, melhor_jogada = minimax_cachorro(
                        self.partida.tabuleiro,True, profundidade, 
                        cachorro_func_para_minimax, onca_func_para_minimax
                    )

            fim = time.time()

            try:
                diff = [i for i, (a, b) in enumerate(zip(self.partida.tabuleiro, melhor_jogada)) if a != b]
                origem = [i for i in diff if self.partida.tabuleiro[i] == self.partida.turno][0]
                destino = [i for i in diff if melhor_jogada[i] == self.partida.turno][0]
                self.executar_movimento(origem, destino, "IA", tempo=fim - inicio, nos=nos_visitados_cont)
            except IndexError:
                print("IA não conseguiu encontrar um movimento válido.")
                self.partida.fim_de_jogo = True
                self.partida.vencedor = "Erro da IA"

            self.aguardando_ia = False

    def executar_movimento(self, origem, destino, jogador_tipo, **kwargs):
        # ... (O resto do arquivo não precisa de alterações)
        estado_antigo = copy.deepcopy(self.partida.tabuleiro)
        self.partida.mover_peca(origem, destino)

        if self.modo_jogo == 'cvc':
            self.partida.historico_partida.append({
                "turno": "Onça" if self.partida.turno == ONCA else "Cachorros",
                "origem": origem, "destino": destino, "tempo": kwargs.get('tempo', 0),
                "nos_avaliados": kwargs.get('nos', 0), "valor_utilidade": 0, "possiveis": []
            })
            self.partida.historico_estados_jogo.append(str(estado_antigo))
        
        self.verificar_fim_de_jogo()
        if not self.partida.fim_de_jogo:
            self.partida.trocar_turno()

    def verificar_fim_de_jogo(self):
        resultado = condicao_vitoria(self.partida.tabuleiro)
        if resultado:
            self.partida.fim_de_jogo = True
            self.partida.vencedor = resultado
        elif self.modo_jogo == 'cvc' and self.partida.cont_turno >= LIMITE_TURNOS:
             self.partida.fim_de_jogo = True
             self.partida.vencedor = "Limite de Turnos"

        if self.partida.fim_de_jogo and self.modo_jogo == 'cvc':
             salvar_log(self.partida.historico_partida, "ia_vs_ia", self.partida.historico_estados_jogo, self.partida.vencedor)

    def is_movimento_valido(self, de, para):
        peca = self.partida.tabuleiro[de]
        if peca == ONCA:
            return para in movimentos_validos_onca(de, self.partida.tabuleiro)
        elif peca == CACHORRO:
            return para in movimentos_validos_cachorros(de, self.partida.tabuleiro)
        return False

    def get_vertex_clicked(self, mouse_pos):
        for i, pos in enumerate(VERTEX_POSITIONS):
            if (mouse_pos[0] - pos[0]) ** 2 + (mouse_pos[1] - pos[1]) ** 2 <= 20 ** 2:
                return i
        return None

    def desenhar(self):
        screen = self.jogo.screen
        screen.blit(self.recursos.fundo_jogo, (0, 0))

        for i in range(31):
            for j in range(i + 1, 31):
                if MATRIZ_JOGO[i][j] == 1:
                    pygame.draw.line(screen, BRANCO, VERTEX_POSITIONS[i], VERTEX_POSITIONS[j], 2)

        for i, pos in enumerate(VERTEX_POSITIONS):
            pygame.draw.circle(screen, CINZA, pos, 20)
            if self.partida.tabuleiro[i] == CACHORRO:
                screen.blit(self.recursos.peca_cachorro, self.recursos.peca_cachorro.get_rect(center=pos))
            elif self.partida.tabuleiro[i] == ONCA:
                screen.blit(self.recursos.peca_onca, self.recursos.peca_onca.get_rect(center=pos))

        if self.selected_vertex is not None:
            pygame.draw.circle(screen, AZUL, VERTEX_POSITIONS[self.selected_vertex], 30, 3)

        font = self.recursos.font_sys_36
        hud_info = [
            f"Turnos: {self.partida.cont_turno}",
            f"Turno: {'Onça' if self.partida.turno == ONCA else 'Cachorros'}",
            f"Capturados: {self.partida.capturados}/5"
        ]
        for i, texto in enumerate(hud_info):
            screen.blit(font.render(texto, True, BRANCO), (20, 20 + i * 40))

        if self.partida.fim_de_jogo:
            fim_texto = [
                f"FIM DE JOGO!",
                f"{self.partida.vencedor}",
                "Pressione ESC para voltar ao menu"
            ]
            for i, linha in enumerate(fim_texto):
                txt_render = font.render(linha, True, BRANCO)
                rect = txt_render.get_rect(center=(LARGURA/2, 300 + i * 50))
                screen.blit(txt_render, rect)