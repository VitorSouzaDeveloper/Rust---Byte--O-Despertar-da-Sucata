# -*- coding: utf-8 -*-
"""
Módulo dos Jogadores (Scrappy - Robô B-09 e Byte - Robô K-12)
Rust & Byte: O Despertar da Sucata

Implementa suporte a modo solo e cooperativo de 2 jogadores (LAN),
além do proxy de interpolação suave (JogadorRemoto) para sincronização UDP.
"""

import pygame
from configuracoes import (
    TAMANHO_BLOCO, GRAVIDADE, VELOCIDADE_MAX_QUEDA, VELOCIDADE_CORRIDA,
    ACELERACAO_CHAO, ATRITO_CHAO, ATRITO_AR, FORCA_PULO, CORTE_PULO,
    FORCA_PULO_DUPLO, VELOCIDADE_DASH, DURACAO_DASH_FRAMES, RECARGA_DASH_FRAMES,
    VIDA_MAX_JOGADOR, FRAMES_INVULNERABILIDADE, CADENCIA_TIRO_NORMAL,
    COR_JOGADOR_CHASSI, COR_JOGADOR_OLHO
)
from notify import (
    notify, EVENTO_DANO_JOGADOR, EVENTO_DISPARO, EVENTO_PULO, EVENTO_DASH
)


def _criar_superficie_scrappy(olhando_direita=True, agachado=False, atirando_cima=False):
    """Desenha programaticamente o sprite do robô B-09 (Scrappy - Azul Aço)."""
    largura = 28
    altura = 18 if agachado else 32
    surf = pygame.Surface((largura, altura), pygame.SRCALPHA)

    cor_corpo = COR_JOGADOR_CHASSI
    cor_chapa_escura = (30, 90, 140)
    cor_visor = (20, 25, 35)
    cor_olho = COR_JOGADOR_OLHO
    cor_detalhe = (200, 210, 225)
    cor_antena = (240, 160, 30)

    if not agachado:
        # Antena no topo
        pygame.draw.line(surf, cor_antena, (14, 0), (14, 4), 2)
        pygame.draw.circle(surf, cor_antena, (14, 1), 2)

        # Cabeça / Chassi Superior
        pygame.draw.rect(surf, cor_corpo, (4, 4, 20, 16), border_radius=4)
        pygame.draw.rect(surf, cor_chapa_escura, (4, 4, 20, 16), 1, border_radius=4)

        # Visor frontal escuro
        offset_olho = 2 if olhando_direita else -2
        visor_rect = pygame.Rect(7 + offset_olho, 7, 12, 7)
        pygame.draw.rect(surf, cor_visor, visor_rect, border_radius=2)

        if atirando_cima:
            pygame.draw.rect(surf, cor_olho, (11 + offset_olho, 8, 4, 2))
        else:
            olho_x = (13 + offset_olho) if olhando_direita else (9 + offset_olho)
            pygame.draw.rect(surf, cor_olho, (olho_x, 9, 3, 3))

        # Tronco
        pygame.draw.rect(surf, cor_chapa_escura, (6, 20, 16, 7))
        pygame.draw.rect(surf, cor_detalhe, (8, 22, 12, 3))

        # Esteiras mecânicas
        pygame.draw.rect(surf, (40, 45, 55), (5, 27, 7, 5), border_radius=2)
        pygame.draw.rect(surf, (40, 45, 55), (16, 27, 7, 5), border_radius=2)
    else:
        pygame.draw.rect(surf, cor_corpo, (4, 2, 20, 12), border_radius=3)
        pygame.draw.rect(surf, cor_visor, (8, 4, 12, 6), border_radius=2)
        pygame.draw.rect(surf, cor_olho, (12, 6, 4, 3))
        pygame.draw.rect(surf, (40, 45, 55), (4, 14, 20, 4), border_radius=2)

    return surf


def _criar_superficie_byte(olhando_direita=True, agachado=False, atirando_cima=False):
    """Desenha programaticamente o sprite do robô K-12 (Byte - Bronze / Cobre Oxidado)."""
    largura = 28
    altura = 18 if agachado else 32
    surf = pygame.Surface((largura, altura), pygame.SRCALPHA)

    cor_corpo = (205, 120, 50)       # Cobre / Bronze
    cor_chapa_escura = (130, 65, 20)  # Cobre escovado escuro
    cor_visor = (25, 20, 15)
    cor_olho = (80, 255, 160)         # Verde Esmeralda Neon
    cor_detalhe = (240, 190, 120)
    cor_antena = (255, 200, 40)

    if not agachado:
        # Tubo de exaustão angular
        pygame.draw.line(surf, cor_antena, (12, 0), (12, 4), 3)
        pygame.draw.circle(surf, cor_antena, (12, 1), 3)

        # Chassi angular de cobre
        pygame.draw.rect(surf, cor_corpo, (4, 4, 20, 16), border_radius=2)
        pygame.draw.rect(surf, cor_chapa_escura, (4, 4, 20, 16), 1, border_radius=2)

        offset_olho = 2 if olhando_direita else -2
        visor_rect = pygame.Rect(7 + offset_olho, 7, 12, 7)
        pygame.draw.rect(surf, cor_visor, visor_rect, border_radius=1)

        if atirando_cima:
            pygame.draw.rect(surf, cor_olho, (11 + offset_olho, 8, 4, 2))
        else:
            olho_x = (13 + offset_olho) if olhando_direita else (9 + offset_olho)
            pygame.draw.rect(surf, cor_olho, (olho_x, 9, 3, 3))

        # Tronco
        pygame.draw.rect(surf, cor_chapa_escura, (6, 20, 16, 7))
        pygame.draw.rect(surf, cor_detalhe, (8, 22, 12, 3))

        # Pernas de pistão hidráulico
        pygame.draw.rect(surf, (60, 40, 30), (5, 27, 7, 5), border_radius=1)
        pygame.draw.rect(surf, (60, 40, 30), (16, 27, 7, 5), border_radius=1)
    else:
        pygame.draw.rect(surf, cor_corpo, (4, 2, 20, 12), border_radius=2)
        pygame.draw.rect(surf, cor_visor, (8, 4, 12, 6), border_radius=1)
        pygame.draw.rect(surf, cor_olho, (12, 6, 4, 3))
        pygame.draw.rect(surf, (60, 40, 30), (4, 14, 20, 4), border_radius=1)

    return surf


class RastroFantasma:
    """Efeito visual de afterimage deixado durante o Dash."""
    def __init__(self, x, y, surf, alfa_inicial=160):
        self.x = x
        self.y = y
        self.surf = surf.copy()
        self.alfa = alfa_inicial

    def atualizar(self):
        self.alfa -= 20
        return self.alfa > 0

    def desenhar(self, superficie, deslocamento_camera_x, deslocamento_camera_y):
        if self.alfa > 0:
            copia = self.surf.copy()
            copia.set_alpha(max(0, int(self.alfa)))
            superficie.blit(copia, (self.x - deslocamento_camera_x, self.y - deslocamento_camera_y))


class Jogador(pygame.sprite.Sprite):
    """Entidade controlável do jogador (Scrappy ou Byte)."""

    def __init__(self, pos_x, pos_y, gerenciador_audio, tipo="scrappy"):
        super().__init__()
        self.audio = gerenciador_audio
        self.tipo = tipo

        # Estados de pose e direção
        self.olhando_direita = True
        self.agachado = False
        self.mirando_cima = False

        # Gerar superfícies de animação básicas pelo tipo
        func_surf = _criar_superficie_byte if tipo == "byte" else _criar_superficie_scrappy
        self.surf_normal = func_surf(olhando_direita=True, agachado=False)
        self.surf_agachado = func_surf(olhando_direita=True, agachado=True)
        self.surf_cima = func_surf(olhando_direita=True, agachado=False, atirando_cima=True)

        self.image = self.surf_normal
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

        # Posição precisa em ponto flutuante
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        # Vetores de velocidade
        self.vel_x = 0.0
        self.vel_y = 0.0

        # Estados de chão e pulo
        self.no_chao = False
        self.pulos_restantes = 2

        # Dash
        self.no_dash = False
        self.timer_dash = 0
        self.recarga_dash = 0
        self.rastros_dash = []

        # Combate e Vida
        self.vida = VIDA_MAX_JOGADOR
        self.pontos = 0
        self.timer_invulnerabilidade = 0
        self.cooldown_tiro = 0
        self.tempo_tiro_triplo = 0

    def atualizar_entradas(self, teclas):
        """Lê comandos do teclado e aplica intenção de movimento."""
        if self.no_dash:
            return

        self.agachado = teclas[pygame.K_s] or teclas[pygame.K_DOWN]
        self.mirando_cima = teclas[pygame.K_w] or teclas[pygame.K_UP]

        mover_esq = teclas[pygame.K_a] or teclas[pygame.K_LEFT]
        mover_dir = teclas[pygame.K_d] or teclas[pygame.K_RIGHT]

        if mover_esq and not mover_dir:
            self.vel_x -= ACELERACAO_CHAO
            if self.vel_x < -VELOCIDADE_CORRIDA:
                self.vel_x = -VELOCIDADE_CORRIDA
            self.olhando_direita = False
        elif mover_dir and not mover_esq:
            self.vel_x += ACELERACAO_CHAO
            if self.vel_x > VELOCIDADE_CORRIDA:
                self.vel_x = VELOCIDADE_CORRIDA
            self.olhando_direita = True
        else:
            atrito = ATRITO_CHAO if self.no_chao else ATRITO_AR
            if self.vel_x > 0:
                self.vel_x = max(0.0, self.vel_x - atrito)
            elif self.vel_x < 0:
                self.vel_x = min(0.0, self.vel_x + atrito)

        if self.agachado and self.no_chao:
            self.vel_x *= 0.5

    def pular(self):
        """Executa salto dinâmico ou salto duplo."""
        if self.no_dash:
            return

        if self.no_chao:
            self.vel_y = FORCA_PULO
            self.no_chao = False
            self.pulos_restantes = 1
            self.audio.tocar("som_pulo")
            notify.emit(EVENTO_PULO, jogador=self.tipo)
        elif self.pulos_restantes > 0:
            self.vel_y = FORCA_PULO_DUPLO
            self.pulos_restantes -= 1
            self.audio.tocar("som_pulo_duplo")
            notify.emit(EVENTO_PULO, jogador=self.tipo, duplo=True)

    def cortar_pulo(self):
        """Permite altura variável de pulo ao soltar a tecla no ar."""
        if self.vel_y < -3.0:
            self.vel_y *= CORTE_PULO

    def executar_dash(self):
        """Dispara impulso horizontal rápido com invulnerabilidade temporária."""
        if self.recarga_dash <= 0 and not self.no_dash:
            self.no_dash = True
            self.timer_dash = DURACAO_DASH_FRAMES
            self.recarga_dash = RECARGA_DASH_FRAMES
            direcao = 1.0 if self.olhando_direita else -1.0
            self.vel_x = direcao * VELOCIDADE_DASH
            self.vel_y = 0.0
            self.audio.tocar("som_dash")
            notify.emit(EVENTO_DASH, jogador=self.tipo)

    def atirar(self, grupo_projeteis):
        """Gera projéteis conforme o cooldown e a arma atual."""
        if self.cooldown_tiro > 0:
            return

        self.cooldown_tiro = CADENCIA_TIRO_NORMAL
        from entidades import Projetil

        origem_x = self.rect.right if self.olhando_direita else self.rect.left
        origem_y = self.rect.centery

        if self.mirando_cima:
            dir_x, dir_y = 0.0, -1.0
            origem_x = self.rect.centerx
            origem_y = self.rect.top
        elif self.agachado:
            dir_x = 1.0 if self.olhando_direita else -1.0
            dir_y = 0.0
            origem_y = self.rect.bottom - 6
        else:
            dir_x = 1.0 if self.olhando_direita else -1.0
            dir_y = 0.0

        notify.emit(EVENTO_DISPARO, jogador=self.tipo)

        if self.tempo_tiro_triplo > 0:
            self.audio.tocar("som_tiro_triplo")
            grupo_projeteis.add(Projetil(origem_x, origem_y, dir_x, dir_y, e_do_jogador=True))
            grupo_projeteis.add(Projetil(origem_x, origem_y, dir_x, dir_y - 0.35, e_do_jogador=True))
            grupo_projeteis.add(Projetil(origem_x, origem_y, dir_x, dir_y + 0.35, e_do_jogador=True))
        else:
            self.audio.tocar("som_tiro")
            grupo_projeteis.add(Projetil(origem_x, origem_y, dir_x, dir_y, e_do_jogador=True))

    def receber_dano(self, quantidade=1):
        """Aplica dano e aciona o período de invulnerabilidade."""
        if self.timer_invulnerabilidade <= 0 and not self.no_dash:
            self.vida -= quantidade
            self.timer_invulnerabilidade = FRAMES_INVULNERABILIDADE
            self.vel_y = -4.0
            self.vel_x = -3.0 if self.olhando_direita else 3.0
            self.audio.tocar("som_dano_jogador")
            notify.emit(EVENTO_DANO_JOGADOR, jogador=self.tipo, vida_restante=self.vida)
            return True
        return False

    def respawn(self, pos_x, pos_y):
        """Ressuscita o jogador nas coordenadas indicadas com invulnerabilidade temporária."""
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)
        self.rect.x = int(pos_x)
        self.rect.y = int(pos_y)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.no_dash = False
        self.timer_dash = 0
        self.recarga_dash = 0
        self.pulos_restantes = 2
        self.vida = VIDA_MAX_JOGADOR
        self.timer_invulnerabilidade = 120  # ~2 segundos piscando com invulnerabilidade
        self.audio.tocar("som_item")

    def atualizar_fisica(self, plataformas, esteiras):
        """Integração numérica da física com resolução AABB de colisões."""
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1
        if self.recarga_dash > 0:
            self.recarga_dash -= 1
        if self.timer_invulnerabilidade > 0:
            self.timer_invulnerabilidade -= 1
        if self.tempo_tiro_triplo > 0:
            self.tempo_tiro_triplo -= 1

        if self.no_dash:
            self.timer_dash -= 1
            if self.timer_dash % 2 == 0:
                self.rastros_dash.append(RastroFantasma(self.rect.x, self.rect.y, self.image))
            if self.timer_dash <= 0:
                self.no_dash = False
                self.vel_x *= 0.4
        else:
            self.vel_y += GRAVIDADE
            if self.vel_y > VELOCIDADE_MAX_QUEDA:
                self.vel_y = VELOCIDADE_MAX_QUEDA

        self.rastros_dash = [r for r in self.rastros_dash if r.atualizar()]

        # Movimento Horizontal
        self.pos_x += self.vel_x
        self.rect.x = int(self.pos_x)

        for plat in plataformas:
            if self.rect.colliderect(plat.rect):
                if self.vel_x > 0:
                    self.rect.right = plat.rect.left
                elif self.vel_x < 0:
                    self.rect.left = plat.rect.right
                self.pos_x = float(self.rect.x)
                self.vel_x = 0.0

        # Movimento Vertical
        self.pos_y += self.vel_y
        self.rect.y = int(self.pos_y)
        self.no_chao = False

        for plat in plataformas:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0.0
                    self.no_chao = True
                    self.pulos_restantes = 2
                elif self.vel_y < 0:
                    self.rect.top = plat.rect.bottom
                    self.vel_y = 0.0
                self.pos_y = float(self.rect.y)

        # Esteiras Rolantes
        for esteira in esteiras:
            if self.rect.colliderect(esteira.rect_gatilho):
                self.pos_x += esteira.velocidade_esteira
                self.rect.x = int(self.pos_x)

        # Atualizar pose visual
        if self.agachado and self.no_chao:
            base = self.surf_agachado
        elif self.mirando_cima:
            base = self.surf_cima
        else:
            base = self.surf_normal

        if not self.olhando_direita:
            self.image = pygame.transform.flip(base, True, False)
        else:
            self.image = base

    def desenhar(self, superficie, deslocamento_camera_x, deslocamento_camera_y):
        """Renderiza o jogador e seus rastros de dash na tela."""
        for rastro in self.rastros_dash:
            rastro.desenhar(superficie, deslocamento_camera_x, deslocamento_camera_y)

        if self.timer_invulnerabilidade > 0 and (self.timer_invulnerabilidade // 4) % 2 == 0:
            return

        pos_tela = (self.rect.x - deslocamento_camera_x, self.rect.y - deslocamento_camera_y)
        superficie.blit(self.image, pos_tela)


class JogadorRemoto:
    """Proxy visual do parceiro cooperativo conectado via rede local (UDP)."""
    def __init__(self, tipo="byte"):
        self.tipo = tipo
        self.x = 100.0
        self.y = 100.0
        self.olhando_direita = True
        self.vida = 3
        self.ativo = True

        func_surf = _criar_superficie_byte if tipo == "byte" else _criar_superficie_scrappy
        self.surf_dir = func_surf(olhando_direita=True)
        self.surf_esq = pygame.transform.flip(self.surf_dir, True, False)
        self.fonte_tag = pygame.font.SysFont("Arial", 10, bold=True)

    def atualizar_dados(self, x, y, olhando_dir, vida):
        """Atualiza a posição interpolada pelo cliente LERP."""
        self.x = x
        self.y = y
        self.olhando_direita = olhando_dir
        self.vida = vida
        self.ativo = True

    def desenhar(self, superficie, deslocamento_camera_x, deslocamento_camera_y):
        if not self.ativo:
            return

        px = int(self.x - deslocamento_camera_x)
        py = int(self.y - deslocamento_camera_y)

        surf = self.surf_dir if self.olhando_direita else self.surf_esq
        superficie.blit(surf, (px, py))

        # Tag de identificação sobre a cabeça
        nome = "P2 (Byte)" if self.tipo == "byte" else "P1 (Scrappy)"
        tag = self.fonte_tag.render(nome, True, (255, 220, 100) if self.tipo == "byte" else (100, 220, 255))
        superficie.blit(tag, (px + 14 - tag.get_width() // 2, py - 14))

        # Mini barra de HP do parceiro
        pygame.draw.rect(superficie, (40, 45, 55), (px + 2, py - 4, 24, 4))
        larg_hp = int(24 * (self.vida / 3.0))
        if larg_hp > 0:
            pygame.draw.rect(superficie, (50, 220, 120), (px + 2, py - 4, larg_hp, 4))
