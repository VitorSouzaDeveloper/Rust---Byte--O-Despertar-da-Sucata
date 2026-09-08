# -*- coding: utf-8 -*-
"""
Módulo Principal de Controle do Jogo (Loop de Execução e Estados)
Rust & Byte: O Despertar da Sucata
"""

import sys
import pygame
from configuracoes import (
    LARGURA_TELA, ALTURA_TELA, TITULO_JOGO, FPS
)
from audio import GerenciadorAudio
from fase import GerenciadorFase
from interface import InterfaceHUD


# Estados do Jogo
ESTADO_MENU = "menu"
ESTADO_JOGANDO = "jogando"
ESTADO_PAUSADO = "pausado"
ESTADO_DERROTA = "derrota"
ESTADO_VITORIA = "vitoria"


class Jogo:
    """Controlador central do ciclo de vida e renderização do jogo."""
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITULO_JOGO)
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.relogio = pygame.time.Clock()

        self.audio = GerenciadorAudio()
        self.hud = InterfaceHUD()

        self.estado = ESTADO_MENU
        self.fase = GerenciadorFase(self.audio)
        self.executando = True

    def reiniciar_fase(self):
        """Reinicia os dados da fase atual."""
        self.fase = GerenciadorFase(self.audio)
        self.estado = ESTADO_JOGANDO

    def tratar_eventos(self):
        """Captura inputs globais de sistema e ações discretas."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.executando = False

            elif evento.type == pygame.KEYDOWN:
                # Comandos na Tela Inicial de Menu
                if self.estado == ESTADO_MENU:
                    if evento.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.estado = ESTADO_JOGANDO
                    elif evento.key == pygame.K_ESCAPE:
                        self.executando = False

                # Comandos Durante a Partida
                elif self.estado == ESTADO_JOGANDO:
                    if evento.key == pygame.K_ESCAPE:
                        self.estado = ESTADO_PAUSADO
                    elif evento.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                        self.fase.jogador.pular()
                    elif evento.key in (pygame.K_k, pygame.K_LSHIFT, pygame.K_RSHIFT):
                        self.fase.jogador.executar_dash()
                    elif evento.key in (pygame.K_j, pygame.K_x):
                        self.fase.jogador.atirar(self.fase.projeteis_jogador)

                # Comandos no Menu de Pausa
                elif self.estado == ESTADO_PAUSADO:
                    if evento.key == pygame.K_ESCAPE:
                        self.estado = ESTADO_JOGANDO
                    elif evento.key == pygame.K_r:
                        self.reiniciar_fase()

                # Comandos na Tela de Derrota ou Vitória
                elif self.estado in (ESTADO_DERROTA, ESTADO_VITORIA):
                    if evento.key == pygame.K_r:
                        self.reiniciar_fase()
                    elif evento.key == pygame.K_ESCAPE:
                        self.estado = ESTADO_MENU

            elif evento.type == pygame.KEYUP:
                # Corte de pulo ao soltar a tecla de salto antes do ápice
                if self.estado == ESTADO_JOGANDO:
                    if evento.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                        self.fase.jogador.cortar_pulo()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Disparo com clique esquerdo do mouse
                if self.estado == ESTADO_JOGANDO and evento.button == 1:
                    self.fase.jogador.atirar(self.fase.projeteis_jogador)

    def atualizar(self):
        """Atualiza a lógica correspondente ao estado ativo."""
        if self.estado == ESTADO_JOGANDO:
            teclas = pygame.key.get_pressed()
            self.fase.atualizar(teclas)

            # Transição para Derrota ou Vitória
            if self.fase.derrota:
                self.estado = ESTADO_DERROTA
            elif self.fase.fase_concluida:
                self.estado = ESTADO_VITORIA

    def desenhar(self):
        """Renderiza a cena na tela e apresenta o quadro atual."""
        if self.estado in (ESTADO_JOGANDO, ESTADO_PAUSADO, ESTADO_DERROTA, ESTADO_VITORIA):
            # Desenha a fase com câmera e parallax
            self.fase.desenhar(self.tela)
            # Desenha o HUD de vida, pontos e arma
            self.hud.desenhar_hud(self.tela, self.fase.jogador)

        if self.estado == ESTADO_MENU:
            # Fundo suave no menu
            self.fase.desenhar(self.tela)
            self.hud.desenhar_tela_inicio(self.tela)

        elif self.estado == ESTADO_PAUSADO:
            self.hud.desenhar_tela_pausa(self.tela)

        elif self.estado == ESTADO_DERROTA:
            self.hud.desenhar_tela_derrota(self.tela, self.fase.jogador.pontos)

        elif self.estado == ESTADO_VITORIA:
            self.hud.desenhar_tela_vitoria(self.tela, self.fase.jogador.pontos)

        pygame.display.flip()

    def executar(self):
        """Loop principal do jogo (Fixed 60 FPS)."""
        while self.executando:
            self.tratar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)

        pygame.quit()
        sys.exit()
