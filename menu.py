# -*- coding: utf-8 -*-
"""
Módulo de Sistema de Menus (Padrão State e Menu Modular inspirado em tac3)
Rust & Byte: O Despertar da Sucata

Implementa navegação por teclado e mouse com retângulo de seleção translúcido,
ícones e renderização temática.
"""

import pygame
from configuracoes import (
    LARGURA_TELA, ALTURA_TELA, COR_TEXTO, COR_TEXTO_MUTED, COR_DESTAQUE
)


class MenuBase:
    """Classe base reutilizável para telas de menu com seleção e navegação."""
    def __init__(self, titulo, subtitulo, opcoes):
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.opcoes = opcoes  # Lista de strings ou tuplas (chave, texto)
        self.indice_selecionado = 0

        self.fonte_titulo = pygame.font.SysFont("Arial", 28, bold=True)
        self.fonte_subtitulo = pygame.font.SysFont("Arial", 14)
        self.fonte_opcao = pygame.font.SysFont("Arial", 18, bold=True)
        self.fonte_pequena = pygame.font.SysFont("Arial", 12)

        self.rects_opcoes = []
        self._calcular_rects()

    def _calcular_rects(self):
        """Calcula os retângulos de colisão de cada opção para clique do mouse."""
        self.rects_opcoes.clear()
        largura_botao = 380
        altura_botao = 44
        y_inicial = 150
        espacamento = 52

        for i in range(len(self.opcoes)):
            x = LARGURA_TELA // 2 - largura_botao // 2
            y = y_inicial + i * espacamento
            self.rects_opcoes.append(pygame.Rect(x, y, largura_botao, altura_botao))

    def atualizar(self):
        """Atualização lógica do menu (animações de foco ou temporizadores)."""
        pass

    def tratar_evento(self, evento):
        """
        Processa navegação por setas/WASD e seleção por Enter/Espaço/Mouse.
        Retorna o índice selecionado ou None.
        """
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_UP, pygame.K_w):
                self.indice_selecionado = (self.indice_selecionado - 1) % len(self.opcoes)
            elif evento.key in (pygame.K_DOWN, pygame.K_s):
                self.indice_selecionado = (self.indice_selecionado + 1) % len(self.opcoes)
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.indice_selecionado

        elif evento.type == pygame.MOUSEMOTION:
            mx, my = evento.pos
            for idx, r in enumerate(self.rects_opcoes):
                if r.collidepoint(mx, my):
                    self.indice_selecionado = idx
                    break

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                mx, my = evento.pos
                for idx, r in enumerate(self.rects_opcoes):
                    if r.collidepoint(mx, my):
                        return idx

        return None

    def desenhar(self, superficie):
        """Desenha a caixa translúcida, cabeçalho e opções do menu."""
        # Fundo escuro semi-transparente
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((14, 12, 20, 240))
        superficie.blit(overlay, (0, 0))

        # Cabeçalho
        txt_tit = self.fonte_titulo.render(self.titulo, True, COR_DESTAQUE)
        txt_sub = self.fonte_subtitulo.render(self.subtitulo, True, COR_TEXTO_MUTED)
        superficie.blit(txt_tit, (LARGURA_TELA // 2 - txt_tit.get_width() // 2, 55))
        superficie.blit(txt_sub, (LARGURA_TELA // 2 - txt_sub.get_width() // 2, 95))

        # Opções
        for idx, opcao in enumerate(self.opcoes):
            texto = opcao if isinstance(opcao, str) else opcao[1]
            r = self.rects_opcoes[idx]
            selecionado = (idx == self.indice_selecionado)

            cor_bg = (40, 36, 54) if selecionado else (22, 20, 30)
            cor_borda = COR_DESTAQUE if selecionado else (55, 60, 75)
            cor_txt = (255, 255, 255) if selecionado else COR_TEXTO_MUTED

            pygame.draw.rect(superficie, cor_bg, r, border_radius=6)
            pygame.draw.rect(superficie, cor_borda, r, 2 if selecionado else 1, border_radius=6)

            # Indicador de seleção à esquerda
            if selecionado:
                pygame.draw.rect(superficie, COR_DESTAQUE, (r.left + 8, r.top + 10, 6, r.height - 20), border_radius=2)

            img_txt = self.fonte_opcao.render(texto, True, cor_txt)
            superficie.blit(img_txt, (r.centerx - img_txt.get_width() // 2, r.centery - img_txt.get_height() // 2))

        # Rodapé de Ajuda
        txt_ajuda = self.fonte_pequena.render("Navegue com [Setas / WASD] e confirme com [ENTER] ou [Clique do Mouse]", True, (120, 125, 140))
        superficie.blit(txt_ajuda, (LARGURA_TELA // 2 - txt_ajuda.get_width() // 2, ALTURA_TELA - 35))


class MenuPrincipal(MenuBase):
    """Menu Inicial de opções do jogo."""
    def __init__(self):
        super().__init__(
            titulo="RUST & BYTE: O DESPERTAR DA SUCATA",
            subtitulo="Trabalho 2 - TAC (Prof. Vanderson) | Ação, Multiplayer e Level Maker",
            opcoes=[
                "1. NOVO JOGO (CAMPANHA SOLO)",
                "2. MULTIPLAYER EM LAN",
                "3. EDITOR DE FASES (LEVEL MAKER)",
                "4. CONFIGURAÇÕES",
                "5. SAIR DO JOGO"
            ]
        )


class MenuMultiplayer(MenuBase):
    """Submenu de conexão em rede local para 2 jogadores."""
    def __init__(self, ip_atual="127.0.0.1"):
        self.ip_atual = ip_atual
        super().__init__(
            titulo="MULTIPLAYER EM REDE LOCAL (LAN)",
            subtitulo="Conecte 2 jogadores via UDP na mesma rede ou localhost",
            opcoes=[
                "1. HOSPEDAR PARTIDA (SERVIDOR LAN)",
                "2. ENTRAR EM PARTIDA (CLIENTE LAN)",
                f"3. IP DO SERVIDOR: [{self.ip_atual}]",
                "4. VOLTAR AO MENU PRINCIPAL"
            ]
        )

    def alternar_ip(self):
        """Alterna entre 127.0.0.1 (local) e detecção de IP de rede."""
        if self.ip_atual == "127.0.0.1":
            import socket
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                self.ip_atual = s.getsockname()[0]
                s.close()
            except Exception:
                self.ip_atual = "192.168.1.100"
        else:
            self.ip_atual = "127.0.0.1"

        self.opcoes[2] = f"3. IP DO SERVIDOR: [{self.ip_atual}]"


class MenuConfiguracoes(MenuBase):
    """Menu de preferências audiovisuais e técnicas."""
    def __init__(self):
        self.volume_sfx = 100
        self.tela_cheia = False
        super().__init__(
            titulo="CONFIGURAÇÕES DO SISTEMA",
            subtitulo="Ajuste volumes de áudio e preferências de exibição",
            opcoes=[
                f"1. EFEITOS SONOROS (SFX): [ {self.volume_sfx}% ]",
                f"2. MODO DE TELA: [ {'TELA CHEIA' if self.tela_cheia else 'JANELA'} ]",
                "3. REDEFINIR CONTROLES PADRÃO",
                "4. VOLTAR AO MENU PRINCIPAL"
            ]
        )

    def alternar_volume(self):
        self.volume_sfx = (self.volume_sfx + 25) % 125
        self.opcoes[0] = f"1. EFEITOS SONOROS (SFX): [ {self.volume_sfx}% ]"

    def alternar_tela(self):
        self.tela_cheia = not self.tela_cheia
        self.opcoes[1] = f"2. MODO DE TELA: [ {'TELA CHEIA' if self.tela_cheia else 'JANELA'} ]"


class MenuPausa(MenuBase):
    """Menu suspenso ao pausar o gameplay."""
    def __init__(self):
        super().__init__(
            titulo="JOGO PAUSADO",
            subtitulo="A simulação física está suspensa",
            opcoes=[
                "1. CONTINUAR PARTIDA",
                "2. REINICIAR FASE",
                "3. VOLTAR AO MENU PRINCIPAL"
            ]
        )
