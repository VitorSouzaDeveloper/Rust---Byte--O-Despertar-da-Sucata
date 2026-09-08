# -*- coding: utf-8 -*-
"""
Módulo de Entidades do Jogo (Inimigos, Projéteis, Coletáveis e Cenário)
Rust & Byte: O Despertar da Sucata
"""

import math
import pygame
from configuracoes import (
    TAMANHO_BLOCO, COR_PLATAFORMA, COR_PLATAFORMA_BORDA, COR_ESTEIRA,
    COR_ESTEIRA_LISTRA, COR_TIRO_PLASMA, COR_TIRO_INIMIGO, COR_DRONE,
    COR_SOLDADOR, COR_OLEO, COR_PARAFUSO, COR_BATERIA, COR_ESPINHO,
    COR_PORTAL, VELOCIDADE_PROJETIL, DURACAO_TIRO_TRIPLO_FRAMES
)


# ==============================================================================
# PROJÉTEIS
# ==============================================================================

class Projetil(pygame.sprite.Sprite):
    """Projétil de plasma disparado por Scrappy ou pelos inimigos."""
    def __init__(self, x, y, dir_x, dir_y, e_do_jogador=True):
        super().__init__()
        self.e_do_jogador = e_do_jogador
        self.largura = 12 if e_do_jogador else 10
        self.altura = 6 if dir_y == 0 else 10
        
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        cor = COR_TIRO_PLASMA if e_do_jogador else COR_TIRO_INIMIGO
        cor_brilho = (255, 255, 255)

        # Desenha o projétil ovalado de alta energia
        pygame.draw.ellipse(self.image, cor, (0, 0, self.largura, self.altura))
        pygame.draw.ellipse(self.image, cor_brilho, (2, 2, self.largura - 4, max(2, self.altura - 4)))

        self.rect = self.image.get_rect(center=(int(x), int(y)))
        
        # Normalização do vetor de direção
        mag = math.hypot(dir_x, dir_y)
        if mag == 0:
            dir_x, dir_y = 1.0, 0.0
            mag = 1.0
            
        vel = VELOCIDADE_PROJETIL if e_do_jogador else 4.5
        self.vel_x = (dir_x / mag) * vel
        self.vel_y = (dir_y / mag) * vel
        
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.tempo_vida = 100  # Frames até sumir

    def update(self, plataformas):
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        self.tempo_vida -= 1
        if self.tempo_vida <= 0:
            self.kill()
            return

        # Colisão com blocos sólidos de terreno destrói o tiro
        for plat in plataformas:
            if self.rect.colliderect(plat.rect):
                self.kill()
                break


# ==============================================================================
# INIMIGOS
# ==============================================================================

class DroneParafuso(pygame.sprite.Sprite):
    """Inimigo aéreo com voo senoidal que atira esferas de energia."""
    def __init__(self, x, y):
        super().__init__()
        self.largura = 28
        self.altura = 26
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)

        # Chassi do drone
        pygame.draw.rect(self.image, COR_DRONE, (4, 8, 20, 14), border_radius=4)
        # Olho de mira vermelho
        pygame.draw.circle(self.image, (255, 255, 100), (14, 14), 4)
        # Hélice superior
        pygame.draw.line(self.image, (180, 190, 200), (4, 4), (24, 4), 2)
        pygame.draw.line(self.image, (60, 60, 70), (14, 4), (14, 8), 2)

        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos_base_y = float(y)
        self.pos_x = float(x)
        self.tempo = 0.0

        self.velocidade_x = -1.2
        self.limite_esquerda = x - 120
        self.limite_direita = x + 120
        self.vida = 2
        self.cooldown_tiro = 90  # Atira a cada ~1.5 segundos

    def update(self, jogador, grupo_projeteis_inimigos, audio):
        self.tempo += 0.05
        # Flutuação senoidal vertical
        self.rect.y = int(self.pos_base_y + math.sin(self.tempo) * 16)

        # Patrulha horizontal
        self.pos_x += self.velocidade_x
        if self.pos_x < self.limite_esquerda:
            self.velocidade_x = abs(self.velocidade_x)
        elif self.pos_x > self.limite_direita:
            self.velocidade_x = -abs(self.velocidade_x)
        self.rect.x = int(self.pos_x)

        # Mira e atira no jogador se estiver próximo
        self.cooldown_tiro -= 1
        distancia = math.hypot(jogador.rect.centerx - self.rect.centerx, jogador.rect.centery - self.rect.centery)
        if distancia < 360 and self.cooldown_tiro <= 0:
            self.cooldown_tiro = 110
            dir_x = jogador.rect.centerx - self.rect.centerx
            dir_y = jogador.rect.centery - self.rect.centery
            grupo_projeteis_inimigos.add(Projetil(self.rect.centerx, self.rect.centery, dir_x, dir_y, e_do_jogador=False))
            audio.tocar("som_tiro")

    def receber_tiro(self, audio):
        self.vida -= 1
        audio.tocar("som_impacto_inimigo")
        if self.vida <= 0:
            self.kill()
            return True  # Morreu
        return False


class RoboSoldador(pygame.sprite.Sprite):
    """Inimigo terrestre blindado que patrulha sobre plataformas."""
    def __init__(self, x, y):
        super().__init__()
        self.largura = 28
        self.altura = 34
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)

        # Desenhar corpo robótico pesado
        pygame.draw.rect(self.image, COR_SOLDADOR, (4, 6, 20, 20), border_radius=4)
        # Máscara de solda escura com fresta alaranjada
        pygame.draw.rect(self.image, (25, 25, 30), (6, 9, 16, 8), border_radius=2)
        pygame.draw.line(self.image, (255, 140, 20), (9, 13), (19, 13), 2)
        # Pernas de ferro
        pygame.draw.rect(self.image, (50, 50, 60), (5, 26, 7, 8))
        pygame.draw.rect(self.image, (50, 50, 60), (16, 26, 7, 8))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos_x = float(x)
        self.velocidade_x = 1.0
        self.vida = 3
        self.limite_esquerda = x - 80
        self.limite_direita = x + 80

    def update(self, plataformas):
        # Patrulha de plataforma
        self.pos_x += self.velocidade_x
        self.rect.x = int(self.pos_x)

        if self.pos_x < self.limite_esquerda:
            self.velocidade_x = abs(self.velocidade_x)
        elif self.pos_x > self.limite_direita:
            self.velocidade_x = -abs(self.velocidade_x)

        # Inverte se colidir lateralmente com parede
        for plat in plataformas:
            if self.rect.colliderect(plat.rect):
                self.velocidade_x *= -1
                self.pos_x += self.velocidade_x * 2
                self.rect.x = int(self.pos_x)
                break

    def receber_tiro(self, audio):
        self.vida -= 1
        audio.tocar("som_impacto_inimigo")
        if self.vida <= 0:
            self.kill()
            return True
        return False


# ==============================================================================
# ITENS E COLETÁVEIS
# ==============================================================================

class ItemOleo(pygame.sprite.Sprite):
    """Recupera 1 ponto de vida de Scrappy."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((18, 22), pygame.SRCALPHA)
        # Frasco de vidro vintage
        pygame.draw.rect(self.image, (180, 220, 240, 160), (4, 6, 10, 14), border_radius=2)
        # Óleo lubrificante dourado
        pygame.draw.rect(self.image, COR_OLEO, (5, 10, 8, 9))
        # Tampa
        pygame.draw.rect(self.image, (210, 80, 30), (6, 2, 6, 4), border_radius=1)

        self.rect = self.image.get_rect(center=(x, y))
        self.pos_base_y = float(y)
        self.tempo = 0.0

    def update(self):
        self.tempo += 0.07
        self.rect.y = int(self.pos_base_y + math.sin(self.tempo) * 4)


class ItemParafuso(pygame.sprite.Sprite):
    """Moeda de pontuação (+100 pontos)."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, COR_PARAFUSO, [
            (8, 0), (14, 4), (14, 12), (8, 16), (2, 12), (2, 4)
        ])
        pygame.draw.circle(self.image, (255, 255, 255), (8, 8), 3)

        self.rect = self.image.get_rect(center=(x, y))
        self.pos_base_y = float(y)
        self.tempo = 0.0

    def update(self):
        self.tempo += 0.09
        self.rect.y = int(self.pos_base_y + math.sin(self.tempo) * 3)


class ItemBateria(pygame.sprite.Sprite):
    """Power-Up de Tiro Triplo (Spread Shot) temporário."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((18, 24), pygame.SRCALPHA)
        # Corpo da bateria
        pygame.draw.rect(self.image, COR_BATERIA, (2, 4, 14, 18), border_radius=3)
        # Polo positivo
        pygame.draw.rect(self.image, (240, 240, 240), (6, 1, 6, 3))
        # Raio luminoso central
        pygame.draw.polygon(self.image, (255, 255, 255), [
            (10, 7), (6, 13), (9, 13), (8, 19), (13, 12), (10, 12)
        ])

        self.rect = self.image.get_rect(center=(x, y))
        self.pos_base_y = float(y)
        self.tempo = 0.0

    def update(self):
        self.tempo += 0.08
        self.rect.y = int(self.pos_base_y + math.sin(self.tempo) * 4)


# ==============================================================================
# ELEMENTOS DE TERRENO E CENÁRIO
# ==============================================================================

class Plataforma(pygame.sprite.Sprite):
    """Bloco sólido de metal industrial para colisão do terreno."""
    def __init__(self, x, y, largura=TAMANHO_BLOCO, altura=TAMANHO_BLOCO):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(COR_PLATAFORMA)

        # Borda superior e rebites decorativos
        pygame.draw.line(self.image, COR_PLATAFORMA_BORDA, (0, 0), (largura, 0), 2)
        pygame.draw.line(self.image, (30, 32, 40), (0, altura - 1), (largura, altura - 1), 2)
        if largura >= 24 and altura >= 24:
            pygame.draw.circle(self.image, (40, 45, 55), (6, 6), 2)
            pygame.draw.circle(self.image, (40, 45, 55), (largura - 6, 6), 2)

        self.rect = self.image.get_rect(topleft=(x, y))


class EsteiraRolante(pygame.sprite.Sprite):
    """Plataforma industrial móvel que empurra o jogador enquanto estiver sobre ela."""
    def __init__(self, x, y, largura=TAMANHO_BLOCO * 3, altura=20, velocidade=1.8):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.velocidade_esteira = velocidade
        self.animacao_offset = 0

        self.image = pygame.Surface((largura, altura))
        self.rect = self.image.get_rect(topleft=(x, y))
        # Gatilho de detecção (área imediatamente acima da esteira)
        self.rect_gatilho = pygame.Rect(x, y - 4, largura, 6)

        self._desenhar_esteira()

    def _desenhar_esteira(self):
        self.image.fill(COR_ESTEIRA)
        # Listras pretas de advertência industrial em diagonal
        largura_listra = 12
        for i in range(-largura_listra, self.largura + largura_listra, largura_listra * 2):
            x1 = i + int(self.animacao_offset)
            x2 = x1 + largura_listra
            pontos = [(x1, 0), (x2, 0), (x2 - 8, self.altura), (x1 - 8, self.altura)]
            pygame.draw.polygon(self.image, COR_ESTEIRA_LISTRA, pontos)
        # Bordas metálicas
        pygame.draw.rect(self.image, (60, 60, 70), (0, 0, self.largura, self.altura), 2)

    def update(self):
        self.animacao_offset = (self.animacao_offset + self.velocidade_esteira) % 24
        self._desenhar_esteira()


class ArmadilhaEspinho(pygame.sprite.Sprite):
    """Armadilha de solo que causa dano ao jogador se pisar."""
    def __init__(self, x, y, largura=TAMANHO_BLOCO, altura=18):
        super().__init__()
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
        # Desenhar pontas de serra / metal cortante
        passo = 8
        for i in range(0, largura, passo):
            pontos = [(i, altura), (i + passo // 2, 0), (i + passo, altura)]
            pygame.draw.polygon(self.image, COR_ESPINHO, pontos)
            pygame.draw.polygon(self.image, (255, 180, 180), pontos, 1)

        self.rect = self.image.get_rect(bottomleft=(x, y + TAMANHO_BLOCO))


class PortalFinal(pygame.sprite.Sprite):
    """Portão de transição de fase que conclui a missão com vitória."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((36, 56), pygame.SRCALPHA)
        # Estrutura do portal
        pygame.draw.rect(self.image, (60, 65, 80), (0, 0, 36, 56), border_radius=6)
        # Vórtice de luz de saída
        pygame.draw.rect(self.image, COR_PORTAL, (6, 6, 24, 44), border_radius=4)
        pygame.draw.circle(self.image, (255, 255, 255), (18, 28), 7)

        self.rect = self.image.get_rect(topleft=(x, y))
