# -*- coding: utf-8 -*-
"""
Módulo de Gerenciamento da Fase, Câmera e Parallax
Rust & Byte: O Despertar da Sucata
"""

import pygame
from configuracoes import (
    TAMANHO_BLOCO, LARGURA_TELA, ALTURA_TELA, COR_FUNDO, COR_FUNDO_DISTANTE
)
from entidades import (
    Plataforma, EsteiraRolante, ArmadilhaEspinho, DroneParafuso,
    RoboSoldador, ItemOleo, ItemParafuso, ItemBateria, PortalFinal
)
from jogador import Jogador


# Mapa do Setor 01: "As Esteiras Infernais"
# Legenda:
# '#' = Bloco Sólido de Metal
# '=' = Esteira Rolante Motorizada
# '^' = Armadilha de Espinhos
# 'D' = Drone Parafuso (Aéreo)
# 'S' = Robô Soldador (Terrestre)
# 'O' = Frasco de Óleo (Cura HP)
# 'P' = Parafuso Dourado (+100 Pts)
# 'B' = Bateria de Plasma (Tiro Triplo)
# '@' = Ponto de Início de Scrappy
# 'E' = Portal de Saída do Setor (Vitória)

MAPA_SETOR_01 = [
    "####################################################################################################",
    "#                                                                                                  #",
    "#                                            D                                                     #",
    "#                                         P  P  P                  D                     P P P     #",
    "#                                      #######                   ######                 #######    #",
    "#                                                                                                  #",
    "#                    P P P                                   P                                     #",
    "#                 ###########                             #######                                  #",
    "#                                   B                                         B                    #",
    "#        O                       #######                   S                #######                #",
    "#      #####          D                                 =======                                    #",
    "#                  =======                                                                       E #",
    "#   @         S               S                 D                    S                         #####",
    "################   ^^^^^   #######   =======   ###   ^^^^^^^   #############   ^^^^^   #############",
    "################   ^^^^^   #######   =======   ###   ^^^^^^^   #############   ^^^^^   #############",
]


class Camera2D:
    """Câmera de rolagem lateral suave (Lerp) com confinamento no mapa."""
    def __init__(self, largura_mapa, altura_mapa):
        self.x = 0.0
        self.y = 0.0
        self.largura_mapa = largura_mapa
        self.altura_mapa = altura_mapa

    def atualizar(self, alvo_rect):
        # Centralizar a câmera no alvo
        destino_x = alvo_rect.centerx - LARGURA_TELA // 2
        destino_y = alvo_rect.centery - ALTURA_TELA // 2

        # Interpolação linear suave (Lerp)
        self.x += (destino_x - self.x) * 0.1
        self.y += (destino_y - self.y) * 0.1

        # Limitar dentro das bordas da fase
        self.x = max(0.0, min(self.largura_mapa - LARGURA_TELA, self.x))
        self.y = max(0.0, min(self.altura_mapa - ALTURA_TELA, self.y))


class GerenciadorFase:
    """Carrega elementos da fase, processa colisões e gerencia entidades."""
    def __init__(self, gerenciador_audio):
        self.audio = gerenciador_audio

        # Grupos de Sprites
        self.plataformas = pygame.sprite.Group()
        self.esteiras = pygame.sprite.Group()
        self.armadilhas = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.itens = pygame.sprite.Group()
        self.projeteis_jogador = pygame.sprite.Group()
        self.projeteis_inimigos = pygame.sprite.Group()
        self.portais = pygame.sprite.Group()

        self.jogador = None
        self.largura_mapa = len(MAPA_SETOR_01[0]) * TAMANHO_BLOCO
        self.altura_mapa = len(MAPA_SETOR_01) * TAMANHO_BLOCO
        self.camera = Camera2D(self.largura_mapa, self.altura_mapa)

        self.fase_concluida = False
        self.derrota = False

        self._carregar_mapa()

    def _carregar_mapa(self):
        """Instancia os blocos e entidades de acordo com a matriz do mapa."""
        for l_idx, linha in enumerate(MAPA_SETOR_01):
            for c_idx, char in enumerate(linha):
                x = c_idx * TAMANHO_BLOCO
                y = l_idx * TAMANHO_BLOCO

                if char == "#":
                    self.plataformas.add(Plataforma(x, y))
                elif char == "=":
                    # Esteira que empurra para a direita
                    esteira = EsteiraRolante(x, y, largura=TAMANHO_BLOCO, velocidade=1.6)
                    self.esteiras.add(esteira)
                    self.plataformas.add(esteira)
                elif char == "^":
                    self.armadilhas.add(ArmadilhaEspinho(x, y))
                elif char == "D":
                    self.inimigos.add(DroneParafuso(x, y))
                elif char == "S":
                    self.inimigos.add(RoboSoldador(x, y))
                elif char == "O":
                    self.itens.add(ItemOleo(x + 16, y + 16))
                elif char == "P":
                    self.itens.add(ItemParafuso(x + 16, y + 16))
                elif char == "B":
                    self.itens.add(ItemBateria(x + 16, y + 16))
                elif char == "@":
                    self.jogador = Jogador(x, y, self.audio)
                elif char == "E":
                    self.portais.add(PortalFinal(x, y))

        if not self.jogador:
            self.jogador = Jogador(100, 300, self.audio)

    def atualizar(self, teclas):
        """Atualiza a lógica de jogo, física e colisões da fase."""
        if self.fase_concluida or self.derrota:
            return

        # 1. Atualizar comandos e física do jogador
        self.jogador.atualizar_entradas(teclas)
        self.jogador.atualizar_fisica(self.plataformas, self.esteiras)

        # Checar queda fora do mapa
        if self.jogador.rect.top > self.altura_mapa + 50:
            self.jogador.vida = 0

        if self.jogador.vida <= 0:
            self.derrota = True
            return

        # 2. Atualizar projéteis
        self.projeteis_jogador.update(self.plataformas)
        self.projeteis_inimigos.update(self.plataformas)

        # 3. Atualizar esteiras rolantes e itens
        self.esteiras.update()
        self.itens.update()

        # 4. Atualizar inimigos
        for inimigo in list(self.inimigos):
            if isinstance(inimigo, DroneParafuso):
                inimigo.update(self.jogador, self.projeteis_inimigos, self.audio)
            elif isinstance(inimigo, RoboSoldador):
                inimigo.update(self.plataformas)

        # 5. Colisões: Projéteis do Jogador vs Inimigos
        for proj in list(self.projeteis_jogador):
            colisoes = pygame.sprite.spritecollide(proj, self.inimigos, False)
            if colisoes:
                proj.kill()
                for inimigo in colisoes:
                    morreu = inimigo.receber_tiro(self.audio)
                    if morreu:
                        self.jogador.pontos += 150

        # 6. Colisões: Projéteis Inimigos vs Jogador
        colisoes_tiro = pygame.sprite.spritecollide(self.jogador, self.projeteis_inimigos, True)
        if colisoes_tiro:
            self.jogador.receber_dano(1)

        # 7. Colisões: Inimigos de contato vs Jogador
        colisoes_contato = pygame.sprite.spritecollide(self.jogador, self.inimigos, False)
        if colisoes_contato:
            self.jogador.receber_dano(1)

        # 8. Colisões: Armadilhas (Espinhos) vs Jogador
        for espinho in self.armadilhas:
            if self.jogador.rect.colliderect(espinho.rect):
                self.jogador.receber_dano(1)

        # 9. Coleta de Itens
        itens_coletados = pygame.sprite.spritecollide(self.jogador, self.itens, True)
        for item in itens_coletados:
            self.audio.tocar("som_item")
            if isinstance(item, ItemOleo):
                if self.jogador.vida < 3:
                    self.jogador.vida += 1
                self.jogador.pontos += 50
            elif isinstance(item, ItemParafuso):
                self.jogador.pontos += 100
            elif isinstance(item, ItemBateria):
                self.jogador.tempo_tiro_triplo = 600  # 10 segundos
                self.jogador.pontos += 200

        # 10. Checagem de Vitória (Portal de Saída)
        for portal in self.portais:
            if self.jogador.rect.colliderect(portal.rect):
                self.fase_concluida = True
                self.audio.tocar("som_vitoria")
                break

        # 11. Atualizar Câmera
        self.camera.atualizar(self.jogador.rect)

    def desenhar_parallax(self, superficie):
        """Renderiza camadas de fundo com rolagem paralaxe para sensação de profundidade."""
        superficie.fill(COR_FUNDO)

        # Camada distante: silhuetas de chaminés industriais (fator de scroll 0.25x)
        camada_dist_x = int(self.camera.x * 0.25)
        for i in range(-1, LARGURA_TELA // 160 + 2):
            base_x = (i * 160) - (camada_dist_x % 160)
            # Chaminé piramidal ao longe
            pygame.draw.rect(superficie, COR_FUNDO_DISTANTE, (base_x, 180, 40, 300))
            pygame.draw.rect(superficie, (35, 28, 42), (base_x + 60, 240, 50, 240))
            # Fumaça estilizada no topo da chaminé
            pygame.draw.circle(superficie, (55, 45, 65), (base_x + 20, 165), 18)
            pygame.draw.circle(superficie, (50, 40, 60), (base_x + 30, 145), 14)

    def desenhar(self, superficie):
        """Desenha todas as entidades respeitando o deslocamento da câmera."""
        cam_x = int(self.camera.x)
        cam_y = int(self.camera.y)

        # 1. Fundo com Parallax
        self.desenhar_parallax(superficie)

        # 2. Elementos de Cenário e Portais
        for sprite in self.portais:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        for sprite in self.plataformas:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        for sprite in self.armadilhas:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        # 3. Itens
        for sprite in self.itens:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        # 4. Inimigos
        for sprite in self.inimigos:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        # 5. Projéteis
        for sprite in self.projeteis_jogador:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        for sprite in self.projeteis_inimigos:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        # 6. Jogador
        self.jogador.desenhar(superficie, cam_x, cam_y)
