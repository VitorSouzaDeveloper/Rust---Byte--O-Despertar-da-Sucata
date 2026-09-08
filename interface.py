# -*- coding: utf-8 -*-
"""
Módulo de Interface do Usuário (HUD, Menus e Telas de Status)
Rust & Byte: O Despertar da Sucata
"""

import pygame
from configuracoes import (
    LARGURA_TELA, ALTURA_TELA, COR_TEXTO, COR_TEXTO_MUTED, COR_DESTAQUE,
    COR_JOGADOR_CHASSI, COR_TIRO_PLASMA, COR_BATERIA
)


class InterfaceHUD:
    """Gerencia overlays visuais da partida e telas de menu em português."""
    def __init__(self):
        # Carrega fontes padrão seguras do sistema
        self.fonte_grande = pygame.font.SysFont("Arial", 28, bold=True)
        self.fonte_media = pygame.font.SysFont("Arial", 18, bold=True)
        self.fonte_pequena = pygame.font.SysFont("Arial", 14)

    def desenhar_hud(self, superficie, jogador):
        """Renderiza o HUD fixo durante a jogatina."""
        # 1. Painel de Fundo Superior
        painel_rect = pygame.Rect(10, 10, 320, 52)
        pygame.draw.rect(superficie, (18, 16, 24, 210), painel_rect, border_radius=6)
        pygame.draw.rect(superficie, (60, 65, 80), painel_rect, 1, border_radius=6)

        # 2. Vida de Scrappy (Ícones de Bateria de Vida)
        txt_vida = self.fonte_pequena.render("INTEGRIDADE:", True, COR_TEXTO_MUTED)
        superficie.blit(txt_vida, (18, 15))

        for i in range(3):
            bat_x = 126 + i * 26
            bat_y = 15
            # Contorno da Bateria
            pygame.draw.rect(superficie, (40, 45, 55), (bat_x, bat_y, 20, 12), border_radius=2)
            pygame.draw.rect(superficie, (80, 90, 110), (bat_x, bat_y, 20, 12), 1, border_radius=2)
            pygame.draw.rect(superficie, (80, 90, 110), (bat_x + 20, bat_y + 3, 2, 6))

            # Preenchimento se ativo
            if i < jogador.vida:
                cor_hp = (50, 220, 120) if jogador.vida > 1 else (255, 60, 60)
                pygame.draw.rect(superficie, cor_hp, (bat_x + 2, bat_y + 2, 16, 8), border_radius=1)

        # 3. Pontuação
        txt_pontos = self.fonte_media.render(f"PONTOS: {jogador.pontos:05d}", True, COR_DESTAQUE)
        superficie.blit(txt_pontos, (18, 34))

        # 4. Painel da Arma Atual (Canto Superior Direito)
        arma_rect = pygame.Rect(LARGURA_TELA - 230, 10, 220, 52)
        pygame.draw.rect(superficie, (18, 16, 24, 210), arma_rect, border_radius=6)
        pygame.draw.rect(superficie, (60, 65, 80), arma_rect, 1, border_radius=6)

        if jogador.tempo_tiro_triplo > 0:
            txt_arma = self.fonte_media.render("ARMA: TIRO TRIPLO", True, COR_BATERIA)
            superficie.blit(txt_arma, (LARGURA_TELA - 218, 15))
            # Barra de tempo restante do Power-up
            porcentagem = jogador.tempo_tiro_triplo / 600.0
            largura_barra = int(196 * porcentagem)
            pygame.draw.rect(superficie, (40, 45, 55), (LARGURA_TELA - 218, 38, 196, 8), border_radius=2)
            pygame.draw.rect(superficie, COR_BATERIA, (LARGURA_TELA - 218, 38, largura_barra, 8), border_radius=2)
        else:
            txt_arma = self.fonte_media.render("ARMA: REBITADEIRA", True, COR_TIRO_PLASMA)
            superficie.blit(txt_arma, (LARGURA_TELA - 218, 15))

            # Status do Dash
            if jogador.recarga_dash <= 0:
                txt_dash = self.fonte_pequena.render("DASH: PRONTO [SHIFT/K]", True, (80, 230, 150))
            else:
                txt_dash = self.fonte_pequena.render("DASH: RECARREGANDO...", True, (200, 120, 100))
            superficie.blit(txt_dash, (LARGURA_TELA - 218, 36))

    def desenhar_tela_inicio(self, superficie):
        """Tela de boas-vindas com título e instruções de controle."""
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((16, 14, 22, 235))
        superficie.blit(overlay, (0, 0))

        # Título do Jogo
        titulo = self.fonte_grande.render("RUST & BYTE: O DESPERTAR DA SUCATA", True, COR_DESTAQUE)
        subtitulo = self.fonte_media.render("Trabalho 1 - TAC (Prof. Vanderson) | Ação e Plataforma 2D", True, COR_TEXTO_MUTED)
        
        superficie.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 60))
        superficie.blit(subtitulo, (LARGURA_TELA // 2 - subtitulo.get_width() // 2, 100))

        # Caixa de Comandos
        box = pygame.Rect(LARGURA_TELA // 2 - 270, 145, 540, 215)
        pygame.draw.rect(superficie, (26, 24, 36), box, border_radius=8)
        pygame.draw.rect(superficie, (70, 75, 95), box, 2, border_radius=8)

        comandos = [
            ("COMANDOS DE TECLADO:", COR_DESTAQUE, True),
            ("• [A] e [D] ou [Setas]: Mover Scrappy para Esquerda e Direita", COR_TEXTO, False),
            ("• [ESPAÇO]: Pular (Pressione novamente no ar para Salto Duplo!)", COR_TEXTO, False),
            ("• [J] ou [Botão Esq. Mouse]: Atirar Rebitadeira de Plasma", COR_TEXTO, False),
            ("• [W / Seta Cima]: Mirar para cima | [S / Seta Baixo]: Agachar", COR_TEXTO, False),
            ("• [K] ou [SHIFT]: Dash de Esquiva Rápida (com invulnerabilidade)", COR_TEXTO, False),
            ("• [ESC]: Pausar o Jogo", COR_TEXTO, False),
        ]

        y_offset = 160
        for texto, cor, negrito in comandos:
            f = self.fonte_media if negrito else self.fonte_pequena
            img = f.render(texto, True, cor)
            superficie.blit(img, (box.left + 24, y_offset))
            y_offset += 25

        # Botão de iniciar
        txt_iniciar = self.fonte_media.render(">> PRESSIONE [ESPAÇO] OU [ENTER] PARA JOGAR <<", True, (80, 240, 160))
        superficie.blit(txt_iniciar, (LARGURA_TELA // 2 - txt_iniciar.get_width() // 2, 385))

    def desenhar_tela_pausa(self, superficie):
        """Overlay de jogo pausado."""
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((10, 10, 16, 180))
        superficie.blit(overlay, (0, 0))

        txt = self.fonte_grande.render("JOGO PAUSADO", True, COR_DESTAQUE)
        sub = self.fonte_media.render("Pressione [ESC] para Continuar", True, COR_TEXTO)
        superficie.blit(txt, (LARGURA_TELA // 2 - txt.get_width() // 2, 200))
        superficie.blit(sub, (LARGURA_TELA // 2 - sub.get_width() // 2, 245))

    def desenhar_tela_derrota(self, superficie, pontos):
        """Tela de Game Over quando a vida zera ou cai no abismo."""
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((28, 12, 16, 220))
        superficie.blit(overlay, (0, 0))

        txt = self.fonte_grande.render("SISTEMA COMPACTADO (FIM DE JOGO)", True, (255, 70, 70))
        pontos_txt = self.fonte_media.render(f"Pontuação Alcançada: {pontos} pontos", True, COR_DESTAQUE)
        reinicio = self.fonte_media.render("Pressione [R] para Reiniciar o Setor", True, (100, 240, 180))

        superficie.blit(txt, (LARGURA_TELA // 2 - txt.get_width() // 2, 170))
        superficie.blit(pontos_txt, (LARGURA_TELA // 2 - pontos_txt.get_width() // 2, 220))
        superficie.blit(reinicio, (LARGURA_TELA // 2 - reinicio.get_width() // 2, 280))

    def desenhar_tela_vitoria(self, superficie, pontos):
        """Tela de Conclusão do Setor com Sucesso."""
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((12, 28, 20, 220))
        superficie.blit(overlay, (0, 0))

        txt = self.fonte_grande.render("SETOR 01 LIMPO! MISSÃO CUMPRIDA!", True, (80, 255, 160))
        desc = self.fonte_media.render("Scrappy desativou a esteira e avançou para o próximo setor!", True, COR_TEXTO)
        pontos_txt = self.fonte_media.render(f"Pontuação Final: {pontos} pontos", True, COR_DESTAQUE)
        reinicio = self.fonte_media.render("Pressione [R] para Jogar Novamente ou [ESC] para Sair", True, (220, 230, 255))

        superficie.blit(txt, (LARGURA_TELA // 2 - txt.get_width() // 2, 150))
        superficie.blit(desc, (LARGURA_TELA // 2 - desc.get_width() // 2, 195))
        superficie.blit(pontos_txt, (LARGURA_TELA // 2 - pontos_txt.get_width() // 2, 240))
        superficie.blit(reinicio, (LARGURA_TELA // 2 - reinicio.get_width() // 2, 300))
