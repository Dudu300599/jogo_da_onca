# game/utils/logger.py
import os
from datetime import datetime

def salvar_log(historico_partida, modo_jogo, historico_estados, vencedor):
    pasta_logs = os.path.join("logs", modo_jogo)
    os.makedirs(pasta_logs, exist_ok=True)
    nome_arquivo = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    caminho_arquivo = os.path.join(pasta_logs, nome_arquivo)

    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(f"===== RESULTADO: {vencedor} =====\n\n")
            f.write("===== HISTÓRICO DE JOGADAS =====\n")
            for i, jogada in enumerate(historico_partida):
                f.write(f"Turno {i+1}: {jogada['turno']}: {jogada['origem']} -> {jogada['destino']}\n")
                f.write(f"  Tempo: {jogada['tempo']:.4f}s | Nós avaliados: {jogada['nos_avaliados']}\n")
                if i < len(historico_estados):
                    f.write(f"  Estado do Tabuleiro: {historico_estados[i]}\n\n")
    except Exception as e:
        print(f"Erro ao salvar log: {e}")