# -*- coding: utf-8 -*-
"""
Módulo de Interface do Usuário (HUD, Overlays e Telas de Status)
Rust & Byte: O Despertar da Sucata

Gerencia o HUD durante a partida (incluindo painel cooperativo em LAN),
e telas de fim de jogo (derrota e vitória).
"""

import pygame
from configuracoes import (
    LARGURA_TELA, ALTURA_TELA, COR_TEXTO, COR_TEXTO_MUTED, COR_DESTAQUE,
    COR_TIRO_PLASMA, COR_BATERIA
)


class InterfaceHUD:
    """Gerencia overlays visuais da partida e telas de fim de jogo."""
    def __init__(self):
        self.fonte_grande = pygame.font.SysFont("Arial", 28, bold=True)
        self.fonte_media = pygame.font.SysFont("Arial", 18, bold=True)
        self.fonte_pequena = pygame.font.SysFont("Arial", 13)

    def desenhar_hud(self, superficie, jogador, jogador_remoto=None):
        """Renderiza o HUD fixo durante a jogatina."""
        # 1. Painel do Jogador Local (Canto Superior Esquerdo)
        painel_rect = pygame.Rect(10, 10, 280, 52)
        pygame.draw.rect(superficie, (18, 16, 24, 220), painel_rect, border_radius=6)
        pygame.draw.rect(superficie, (60, 65, 80), painel_rect, 1, border_radius=6)

        nome_local = "P1: SCRAPPY" if getattr(jogador, "tipo", "scrappy") == "scrappy" else "P2: BYTE"
        cor_tag = (50, 180, 240) if getattr(jogador, "tipo", "scrappy") == "scrappy" else (225, 140, 60)
        txt_nome = self.fonte_pequena.render(nome_local, True, cor_tag)
        superficie.blit(txt_nome, (18, 15))

        # Ícones de Bateria de Vida
        for i in range(3):
            bat_x = 110 + i * 24
            bat_y = 15
            pygame.draw.rect(superficie, (40, 45, 55), (bat_x, bat_y, 18, 11), border_radius=2)
            pygame.draw.rect(superficie, (80, 90, 110), (bat_x, bat_y, 18, 11), 1, border_radius=2)
            pygame.draw.rect(superficie, (80, 90, 110), (bat_x + 18, bat_y + 3, 2, 5))

            if i < jogador.vida:
                cor_hp = (50, 220, 120) if jogador.vida > 1 else (255, 60, 60)
                pygame.draw.rect(superficie, cor_hp, (bat_x + 2, bat_y + 2, 14, 7), border_radius=1)

        # Pontuação
        txt_pontos = self.fonte_media.render(f"PONTOS: {jogador.pontos:05d}", True, COR_DESTAQUE)
        superficie.blit(txt_pontos, (18, 33))

        # 2. Painel do Jogador Remoto (se em cooperativo LAN)
        if jogador_remoto and getattr(jogador_remoto, "ativo", False):
            painel_remoto = pygame.Rect(300, 10, 240, 52)
            pygame.draw.rect(superficie, (18, 16, 24, 220), painel_remoto, border_radius=6)
            pygame.draw.rect(superficie, (80, 100, 70), painel_remoto, 1, border_radius=6)

            nome_remoto = "PARCEIRO: BYTE" if jogador_remoto.tipo == "byte" else "PARCEIRO: SCRAPPY"
            cor_remoto = (225, 140, 60) if jogador_remoto.tipo == "byte" else (50, 180, 240)
            txt_rem = self.fonte_pequena.render(nome_remoto, True, cor_remoto)
            superficie.blit(txt_rem, (310, 15))

            for i in range(3):
                bat_x = 440 + i * 22
                bat_y = 15
                pygame.draw.rect(superficie, (40, 45, 55), (bat_x, bat_y, 16, 11), border_radius=2)
                pygame.draw.rect(superficie, (80, 90, 110), (bat_x, bat_y, 16, 11), 1, border_radius=2)
                if i < jogador_remoto.vida:
                    pygame.draw.rect(superficie, (50, 220, 120), (bat_x + 2, bat_y + 2, 12, 7), border_radius=1)

            txt_lan = self.fonte_pequena.render("REDE: CONECTADO (LAN UDP)", True, (100, 240, 160))
            superficie.blit(txt_lan, (310, 33))

        # 3. Painel da Arma Atual (Canto Superior Direito)
        arma_rect = pygame.Rect(LARGURA_TELA - 230, 10, 220, 52)
        pygame.draw.rect(superficie, (18, 16, 24, 220), arma_rect, border_radius=6)
        pygame.draw.rect(superficie, (60, 65, 80), arma_rect, 1, border_radius=6)

        if jogador.tempo_tiro_triplo > 0:
            txt_arma = self.fonte_media.render("ARMA: TIRO TRIPLO", True, COR_BATERIA)
            superficie.blit(txt_arma, (LARGURA_TELA - 218, 15))
            porcentagem = jogador.tempo_tiro_triplo / 600.0
            largura_barra = int(196 * porcentagem)
            pygame.draw.rect(superficie, (40, 45, 55), (LARGURA_TELA - 218, 38, 196, 8), border_radius=2)
            pygame.draw.rect(superficie, COR_BATERIA, (LARGURA_TELA - 218, 38, largura_barra, 8), border_radius=2)
        else:
            txt_arma = self.fonte_media.render("ARMA: REBITADEIRA", True, COR_TIRO_PLASMA)
            superficie.blit(txt_arma, (LARGURA_TELA - 218, 15))

            if jogador.recarga_dash <= 0:
                txt_dash = self.fonte_pequena.render("DASH: PRONTO [SHIFT/K]", True, (80, 230, 150))
            else:
                txt_dash = self.fonte_pequena.render("DASH: RECARREGANDO...", True, (200, 120, 100))
            superficie.blit(txt_dash, (LARGURA_TELA - 218, 36))

    def desenhar_tela_pausa(self, superficie):
        """Overlay rápido de pausa."""
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((10, 10, 16, 180))
        superficie.blit(overlay, (0, 0))

        txt = self.fonte_grande.render("JOGO PAUSADO", True, COR_DESTAQUE)
        sub = self.fonte_media.render("Pressione [ESC] para Continuar | [R] Reiniciar | [M] Menu", True, COR_TEXTO)
        superficie.blit(txt, (LARGURA_TELA // 2 - txt.get_width() // 2, 200))
        superficie.blit(sub, (LARGURA_TELA // 2 - sub.get_width() // 2, 245))

    def desenhar_tela_derrota(self, superficie, pontos):
        """Tela de Game Over quando a vida zera ou cai no abismo."""
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((28, 12, 16, 235))
        superficie.blit(overlay, (0, 0))

        txt = self.fonte_grande.render("SISTEMA COMPACTADO (FIM DE JOGO)", True, (255, 70, 70))
        pontos_txt = self.fonte_media.render(f"Pontuação Alcançada: {pontos} pontos", True, COR_DESTAQUE)
        reinicio = self.fonte_media.render("Pressione [R] para Reiniciar ou [ESC] para Menu", True, (100, 240, 180))

        superficie.blit(txt, (LARGURA_TELA // 2 - txt.get_width() // 2, 170))
        superficie.blit(pontos_txt, (LARGURA_TELA // 2 - pontos_txt.get_width() // 2, 220))
        superficie.blit(reinicio, (LARGURA_TELA // 2 - reinicio.get_width() // 2, 280))

    def desenhar_tela_vitoria(self, superficie, pontos):
        """Tela de Conclusão do Setor com Sucesso."""
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((12, 28, 20, 235))
        superficie.blit(overlay, (0, 0))

        txt = self.fonte_grande.render("SETOR LIMPO! MISSÃO CUMPRIDA!", True, (80, 255, 160))
        desc = self.fonte_media.render("Os heróis desativaram as esteiras e avançaram para a próxima zona!", True, COR_TEXTO)
        pontos_txt = self.fonte_media.render(f"Pontuação Final: {pontos} pontos", True, COR_DESTAQUE)
        reinicio = self.fonte_media.render("Pressione [R] para Jogar Novamente ou [ESC] para Menu", True, (220, 230, 255))

        superficie.blit(txt, (LARGURA_TELA // 2 - txt.get_width() // 2, 150))
        superficie.blit(desc, (LARGURA_TELA // 2 - desc.get_width() // 2, 195))
        superficie.blit(pontos_txt, (LARGURA_TELA // 2 - pontos_txt.get_width() // 2, 240))
        superficie.blit(reinicio, (LARGURA_TELA // 2 - reinicio.get_width() // 2, 300))
