# -*- coding: utf-8 -*-
"""
Módulo de Gerenciamento da Fase, Câmera e Parallax
Rust & Byte: O Despertar da Sucata

Suporta carregamento dinâmico de mapas (Setor Padrão ou Criado pelo Editor),
câmera dinâmica dupla para modo cooperativo e renderização de parceiro remoto.
"""

import pygame
from configuracoes import (
    TAMANHO_BLOCO, LARGURA_TELA, ALTURA_TELA, COR_FUNDO, COR_FUNDO_DISTANTE
)
from entidades import (
    Plataforma, EsteiraRolante, ArmadilhaEspinho, DroneParafuso,
    RoboSoldador, ItemOleo, ItemParafuso, ItemBateria, PortalFinal
)
from jogador import Jogador, JogadorRemoto
from notify import notify, EVENTO_INIMIGO_DERROTADO, EVENTO_ITEM_COLETADO, EVENTO_FASE_CONCLUIDA


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
    """Câmera suave com suporte a rastreamento de 1 ou 2 jogadores (câmera dupla)."""
    def __init__(self, largura_mapa, altura_mapa):
        self.x = 0.0
        self.y = 0.0
        self.largura_mapa = largura_mapa
        self.altura_mapa = altura_mapa

    def atualizar(self, alvo_rect, parceiro_x=None, parceiro_y=None):
        if parceiro_x is not None and parceiro_y is not None:
            # Ponto médio dinâmico entre os dois heróis
            centro_x = (alvo_rect.centerx + parceiro_x) / 2.0
            centro_y = (alvo_rect.centery + parceiro_y) / 2.0
        else:
            centro_x = alvo_rect.centerx
            centro_y = alvo_rect.centery

        destino_x = centro_x - LARGURA_TELA // 2
        destino_y = centro_y - ALTURA_TELA // 2

        self.x += (destino_x - self.x) * 0.1
        self.y += (destino_y - self.y) * 0.1

        max_x = max(0.0, self.largura_mapa - LARGURA_TELA)
        max_y = max(0.0, self.altura_mapa - ALTURA_TELA)
        self.x = max(0.0, min(max_x, self.x))
        self.y = max(0.0, min(max_y, self.y))


class GerenciadorFase:
    """Carrega elementos da fase, processa colisões e gerencia entidades."""
    def __init__(self, gerenciador_audio, linhas_mapa=None, tipo_jogador="scrappy"):
        self.audio = gerenciador_audio
        self.tipo_jogador = tipo_jogador
        self.linhas_mapa = linhas_mapa if linhas_mapa else MAPA_SETOR_01

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
        self.jogador_remoto = None  # Proxy do parceiro LAN

        self.pos_spawn_p1 = (100, 300)
        self.pos_spawn_p2 = (140, 300)
        self.pos_spawn_local = (100, 300)
        self.mensagem_respawn = ""
        self.timer_mensagem_respawn = 0
        self.fonte_notif = pygame.font.SysFont("Arial", 14, bold=True)

        self.largura_mapa = len(self.linhas_mapa[0]) * TAMANHO_BLOCO
        self.altura_mapa = len(self.linhas_mapa) * TAMANHO_BLOCO
        self.camera = Camera2D(self.largura_mapa, self.altura_mapa)

        self.fase_concluida = False
        self.derrota = False

        self._carregar_mapa()

    def configurar_multiplayer(self, remoto_tipo="byte"):
        """Ativa o parceiro remoto para o modo cooperativo."""
        self.jogador_remoto = JogadorRemoto(tipo=remoto_tipo)

    def _carregar_mapa(self):
        """Instancia os blocos e entidades de acordo com a matriz do mapa."""
        self.pos_spawn_p1 = (100, 300)
        self.pos_spawn_p2 = (140, 300)

        for l_idx, linha in enumerate(self.linhas_mapa):
            for c_idx, char in enumerate(linha):
                x = c_idx * TAMANHO_BLOCO
                y = l_idx * TAMANHO_BLOCO

                if char == "#":
                    self.plataformas.add(Plataforma(x, y))
                elif char == "=":
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
                    self.pos_spawn_p1 = (x, y)
                elif char == "2":
                    self.pos_spawn_p2 = (x, y)
                elif char == "E":
                    self.portais.add(PortalFinal(x, y))

        self.pos_spawn_local = self.pos_spawn_p2 if self.tipo_jogador == "byte" else self.pos_spawn_p1
        self.jogador = Jogador(self.pos_spawn_local[0], self.pos_spawn_local[1], self.audio, tipo=self.tipo_jogador)

    def atualizar(self, teclas):
        """Atualiza a lógica de jogo, física e colisões da fase."""
        if self.fase_concluida or self.derrota:
            return

        # 1. Comandos e física do jogador local
        self.jogador.atualizar_entradas(teclas)
        self.jogador.atualizar_fisica(self.plataformas, self.esteiras)

        caiu_abismo = self.jogador.rect.top > self.altura_mapa + 50
        sem_vida = self.jogador.vida <= 0

        if caiu_abismo or sem_vida:
            if self.jogador_remoto is not None:
                # MULTIPLAYER COOPERATIVO: O jogador reaparece continuamente (respawn)
                # Mantém ambos os jogadores na mesma sessão em vez de entrar em tela solo
                if (self.jogador_remoto.ativo and self.jogador_remoto.vida > 0
                        and 0 <= self.jogador_remoto.y <= self.altura_mapa):
                    rx = self.jogador_remoto.x
                    ry = max(50.0, self.jogador_remoto.y - 32.0)
                else:
                    rx, ry = self.pos_spawn_local

                self.jogador.respawn(rx, ry)
                nome = "P1 (Scrappy)" if self.tipo_jogador == "scrappy" else "P2 (Byte)"
                self.mensagem_respawn = f"{nome} REAPARECEU NA FASE!"
                self.timer_mensagem_respawn = 150
            else:
                self.jogador.vida = 0
                self.derrota = True
                return

        # 2. Atualizar projéteis
        self.projeteis_jogador.update(self.plataformas)
        self.projeteis_inimigos.update(self.plataformas)

        # 3. Esteiras e itens
        self.esteiras.update()
        self.itens.update()

        # 4. Inimigos
        for inimigo in list(self.inimigos):
            if isinstance(inimigo, DroneParafuso):
                inimigo.update(self.jogador, self.projeteis_inimigos, self.audio)
            elif isinstance(inimigo, RoboSoldador):
                inimigo.update(self.plataformas)

        # 5. Projéteis vs Inimigos
        for proj in list(self.projeteis_jogador):
            colisoes = pygame.sprite.spritecollide(proj, self.inimigos, False)
            if colisoes:
                proj.kill()
                for inimigo in colisoes:
                    morreu = inimigo.receber_tiro(self.audio)
                    if morreu:
                        self.jogador.pontos += 150
                        notify.emit(EVENTO_INIMIGO_DERROTADO, pontos=150)

        # 6. Projéteis vs Jogador
        colisoes_tiro = pygame.sprite.spritecollide(self.jogador, self.projeteis_inimigos, True)
        if colisoes_tiro:
            self.jogador.receber_dano(1)

        # 7. Inimigos vs Jogador
        colisoes_contato = pygame.sprite.spritecollide(self.jogador, self.inimigos, False)
        if colisoes_contato:
            self.jogador.receber_dano(1)

        # 8. Espinhos vs Jogador
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
                notify.emit(EVENTO_ITEM_COLETADO, item="oleo", pontos=50)
            elif isinstance(item, ItemParafuso):
                self.jogador.pontos += 100
                notify.emit(EVENTO_ITEM_COLETADO, item="parafuso", pontos=100)
            elif isinstance(item, ItemBateria):
                self.jogador.tempo_tiro_triplo = 600
                self.jogador.pontos += 200
                notify.emit(EVENTO_ITEM_COLETADO, item="bateria", pontos=200)

        # 10. Vitória
        for portal in self.portais:
            if self.jogador.rect.colliderect(portal.rect):
                self.fase_concluida = True
                self.audio.tocar("som_vitoria")
                notify.emit(EVENTO_FASE_CONCLUIDA, pontos=self.jogador.pontos)
                break

        # 11. Câmera
        parc_x = self.jogador_remoto.x if (self.jogador_remoto and self.jogador_remoto.ativo) else None
        parc_y = self.jogador_remoto.y if (self.jogador_remoto and self.jogador_remoto.ativo) else None
        self.camera.atualizar(self.jogador.rect, parceiro_x=parc_x, parceiro_y=parc_y)

    def desenhar_parallax(self, superficie):
        """Renderiza camadas de fundo com rolagem paralaxe."""
        superficie.fill(COR_FUNDO)
        camada_dist_x = int(self.camera.x * 0.25)
        for i in range(-1, LARGURA_TELA // 160 + 2):
            base_x = (i * 160) - (camada_dist_x % 160)
            pygame.draw.rect(superficie, COR_FUNDO_DISTANTE, (base_x, 180, 40, 300))
            pygame.draw.rect(superficie, (35, 28, 42), (base_x + 60, 240, 50, 240))
            pygame.draw.circle(superficie, (55, 45, 65), (base_x + 20, 165), 18)
            pygame.draw.circle(superficie, (50, 40, 60), (base_x + 30, 145), 14)

    def desenhar(self, superficie):
        """Desenha todas as entidades respeitando o deslocamento da câmera."""
        cam_x = int(self.camera.x)
        cam_y = int(self.camera.y)

        self.desenhar_parallax(superficie)

        for sprite in self.portais:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        for sprite in self.plataformas:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        for sprite in self.armadilhas:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        for sprite in self.itens:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        for sprite in self.inimigos:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        for sprite in self.projeteis_jogador:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        for sprite in self.projeteis_inimigos:
            superficie.blit(sprite.image, (sprite.rect.x - cam_x, sprite.rect.y - cam_y))

        # Jogador Remoto (se ativo em LAN)
        if self.jogador_remoto:
            self.jogador_remoto.desenhar(superficie, cam_x, cam_y)

        # Jogador Local
        self.jogador.desenhar(superficie, cam_x, cam_y)

        # 7. Banner de Notificação de Respawn Cooperativo
        if self.timer_mensagem_respawn > 0:
            self.timer_mensagem_respawn -= 1
            larg_b = 320
            alt_b = 30
            bx = LARGURA_TELA // 2 - larg_b // 2
            by = 68
            pygame.draw.rect(superficie, (18, 16, 24, 220), (bx, by, larg_b, alt_b), border_radius=6)
            pygame.draw.rect(superficie, (80, 240, 160), (bx, by, larg_b, alt_b), 1, border_radius=6)
            txt_aviso = self.fonte_notif.render(self.mensagem_respawn, True, (80, 240, 160))
            superficie.blit(txt_aviso, (bx + (larg_b - txt_aviso.get_width()) // 2, by + (alt_b - txt_aviso.get_height()) // 2))
