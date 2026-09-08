# -*- coding: utf-8 -*-
"""
Módulo do Jogador Principal (Scrappy - Robô B-09)
Rust & Byte: O Despertar da Sucata
"""

import pygame
from configuracoes import (
    TAMANHO_BLOCO, GRAVIDADE, VELOCIDADE_MAX_QUEDA, VELOCIDADE_CORRIDA,
    ACELERACAO_CHAO, ATRITO_CHAO, ATRITO_AR, FORCA_PULO, CORTE_PULO,
    FORCA_PULO_DUPLO, VELOCIDADE_DASH, DURACAO_DASH_FRAMES, RECARGA_DASH_FRAMES,
    VIDA_MAX_JOGADOR, FRAMES_INVULNERABILIDADE, CADENCIA_TIRO_NORMAL,
    DURACAO_TIRO_TRIPLO_FRAMES, COR_JOGADOR_CHASSI, COR_JOGADOR_OLHO
)


def _criar_superficie_scrappy(olhando_direita=True, agachado=False, atirando_cima=False):
    """
    Desenha programaticamente o sprite do robô B-09 (Scrappy) em Pixel Art.
    Retorna uma pygame.Surface com canal alfa (transparência).
    """
    largura = 28
    altura = 18 if agachado else 32
    surf = pygame.Surface((largura, altura), pygame.SRCALPHA)

    # Cores
    cor_corpo = COR_JOGADOR_CHASSI
    cor_chapa_escura = (30, 90, 140)
    cor_visor = (20, 25, 35)
    cor_olho = COR_JOGADOR_OLHO
    cor_detalhe = (200, 210, 225)
    cor_antena = (240, 160, 30)

    if not agachado:
        # Antena / Parafuso no topo
        pygame.draw.line(surf, cor_antena, (14, 0), (14, 4), 2)
        pygame.draw.circle(surf, cor_antena, (14, 1), 2)

        # Cabeça / Chassi Superior
        pygame.draw.rect(surf, cor_corpo, (4, 4, 20, 16), border_radius=4)
        pygame.draw.rect(surf, cor_chapa_escura, (4, 4, 20, 16), 1, border_radius=4)

        # Visor frontal escuro
        offset_olho = 2 if olhando_direita else -2
        visor_rect = pygame.Rect(7 + offset_olho, 7, 12, 7)
        pygame.draw.rect(surf, cor_visor, visor_rect, border_radius=2)

        # Olho de plasma brilhante
        if atirando_cima:
            pygame.draw.rect(surf, cor_olho, (11 + offset_olho, 8, 4, 2))
        else:
            olho_x = (13 + offset_olho) if olhando_direita else (9 + offset_olho)
            pygame.draw.rect(surf, cor_olho, (olho_x, 9, 3, 3))

        # Tronco / Compartimento de Bateria
        pygame.draw.rect(surf, cor_chapa_escura, (6, 20, 16, 7))
        pygame.draw.rect(surf, cor_detalhe, (8, 22, 12, 3))

        # Pernas / Esteiras mecânicas
        pygame.draw.rect(surf, (40, 45, 55), (5, 27, 7, 5), border_radius=2)
        pygame.draw.rect(surf, (40, 45, 55), (16, 27, 7, 5), border_radius=2)
    else:
        # Versão agachada (perfil rebaixado para esquiva de tiros)
        pygame.draw.rect(surf, cor_corpo, (4, 2, 20, 12), border_radius=3)
        pygame.draw.rect(surf, cor_visor, (8, 4, 12, 6), border_radius=2)
        pygame.draw.rect(surf, cor_olho, (12, 6, 4, 3))
        pygame.draw.rect(surf, (40, 45, 55), (4, 14, 20, 4), border_radius=2)

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
    """Entidade do jogador principal (Scrappy)."""

    def __init__(self, pos_x, pos_y, gerenciador_audio):
        super().__init__()
        self.audio = gerenciador_audio

        # Estados de pose e direção
        self.olhando_direita = True
        self.agachado = False
        self.mirando_cima = False

        # Gerar superfícies de animação básicas
        self.surf_normal = _criar_superficie_scrappy(olhando_direita=True, agachado=False)
        self.surf_agachado = _criar_superficie_scrappy(olhando_direita=True, agachado=True)
        self.surf_cima = _criar_superficie_scrappy(olhando_direita=True, agachado=False, atirando_cima=True)

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
        self.tempo_tiro_triplo = 0  # Duração do power-up

    def atualizar_entradas(self, teclas):
        """Lê comandos do teclado e aplica intenção de movimento."""
        if self.no_dash:
            return  # Durante o dash, a movimentação é guiada pelo impulso

        # Direção de mira e postura
        self.agachado = teclas[pygame.K_s] or teclas[pygame.K_DOWN]
        self.mirando_cima = teclas[pygame.K_w] or teclas[pygame.K_UP]

        # Movimento Horizontal
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
            # Desaceleração / Atrito suave
            atrito = ATRITO_CHAO if self.no_chao else ATRITO_AR
            if self.vel_x > 0:
                self.vel_x = max(0.0, self.vel_x - atrito)
            elif self.vel_x < 0:
                self.vel_x = min(0.0, self.vel_x + atrito)

        # Se estiver agachado no chão, desacelera mais rápido
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
        elif self.pulos_restantes > 0:
            # Salto duplo (micro-jetpack de CO2)
            self.vel_y = FORCA_PULO_DUPLO
            self.pulos_restantes -= 1
            self.audio.tocar("som_pulo_duplo")

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
            self.vel_y = 0.0  # Anula gravidade no dash
            self.audio.tocar("som_dash")

    def atirar(self, grupo_projeteis):
        """Gera projéteis conforme o cooldown e a arma atual."""
        if self.cooldown_tiro > 0:
            return

        self.cooldown_tiro = CADENCIA_TIRO_NORMAL
        from entidades import Projetil

        # Ponto de origem do disparo (cano da arma de Scrappy)
        origem_x = self.rect.right if self.olhando_direita else self.rect.left
        origem_y = self.rect.centery

        # Define ângulo/direção do projétil
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

        # Arma Normal ou Tiro Triplo (Spread Shot)
        if self.tempo_tiro_triplo > 0:
            self.audio.tocar("som_tiro_triplo")
            # Disparo central
            grupo_projeteis.add(Projetil(origem_x, origem_y, dir_x, dir_y, e_do_jogador=True))
            # Disparo inclinado para cima
            grupo_projeteis.add(Projetil(origem_x, origem_y, dir_x, dir_y - 0.35, e_do_jogador=True))
            # Disparo inclinado para baixo
            grupo_projeteis.add(Projetil(origem_x, origem_y, dir_x, dir_y + 0.35, e_do_jogador=True))
        else:
            self.audio.tocar("som_tiro")
            grupo_projeteis.add(Projetil(origem_x, origem_y, dir_x, dir_y, e_do_jogador=True))

    def receber_dano(self, quantidade=1):
        """Aplica dano e aciona o período de invulnerabilidade."""
        if self.timer_invulnerabilidade <= 0 and not self.no_dash:
            self.vida -= quantidade
            self.timer_invulnerabilidade = FRAMES_INVULNERABILIDADE
            # Recuo (Knockback)
            self.vel_y = -4.0
            self.vel_x = -3.0 if self.olhando_direita else 3.0
            self.audio.tocar("som_dano_jogador")
            return True
        return False

    def atualizar_fisica(self, plataformas, esteiras):
        """Integração numérica da física com resolução AABB de colisões."""
        # 1. Atualizar contadores de cooldown
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1
        if self.recarga_dash > 0:
            self.recarga_dash -= 1
        if self.timer_invulnerabilidade > 0:
            self.timer_invulnerabilidade -= 1
        if self.tempo_tiro_triplo > 0:
            self.tempo_tiro_triplo -= 1

        # 2. Controle do estado de Dash
        if self.no_dash:
            self.timer_dash -= 1
            # Criar rastro fantasma a cada 2 frames
            if self.timer_dash % 2 == 0:
                self.rastros_dash.append(RastroFantasma(self.rect.x, self.rect.y, self.image))
            if self.timer_dash <= 0:
                self.no_dash = False
                self.vel_x *= 0.4
        else:
            # Gravidade convencional
            self.vel_y += GRAVIDADE
            if self.vel_y > VELOCIDADE_MAX_QUEDA:
                self.vel_y = VELOCIDADE_MAX_QUEDA

        # Atualizar e limpar rastros
        self.rastros_dash = [r for r in self.rastros_dash if r.atualizar()]

        # 3. Movimento Horizontal e Colisões
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

        # 4. Movimento Vertical e Colisões
        self.pos_y += self.vel_y
        self.rect.y = int(self.pos_y)
        self.no_chao = False

        for plat in plataformas:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:  # Caindo no chão
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0.0
                    self.no_chao = True
                    self.pulos_restantes = 2
                elif self.vel_y < 0:  # Batendo no teto
                    self.rect.top = plat.rect.bottom
                    self.vel_y = 0.0
                self.pos_y = float(self.rect.y)

        # 5. Influência das Esteiras Rolantes
        for esteira in esteiras:
            if self.rect.colliderect(esteira.rect_gatilho):
                self.pos_x += esteira.velocidade_esteira
                self.rect.x = int(self.pos_x)

        # 6. Atualizar sprite visual correto
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
        # Desenha rastros fantasma do dash
        for rastro in self.rastros_dash:
            rastro.desenhar(superficie, deslocamento_camera_x, deslocamento_camera_y)

        # Efeito de piscar quando invulnerável
        if self.timer_invulnerabilidade > 0 and (self.timer_invulnerabilidade // 4) % 2 == 0:
            return  # Frame invisível do piscar

        pos_tela = (self.rect.x - deslocamento_camera_x, self.rect.y - deslocamento_camera_y)
        superficie.blit(self.image, pos_tela)
