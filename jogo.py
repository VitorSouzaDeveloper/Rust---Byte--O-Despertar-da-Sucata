# -*- coding: utf-8 -*-
"""
Módulo Principal de Controle do Jogo (State Pattern e Ciclo de Execução)
Rust & Byte: O Despertar da Sucata - Trabalho 2 (TAC)

Orquestra os estados da aplicação:
- Menu Principal
- Lobby Multiplayer em LAN (UDP)
- Editor de Fases (Level Maker) e Modo Playtest
- Configurações
- Gameplay Solo e Cooperativo
"""

import sys
import pygame

from configuracoes import (
    LARGURA_TELA, ALTURA_TELA, TITULO_JOGO, FPS
)
from audio import GerenciadorAudio
from fase import GerenciadorFase
from interface import InterfaceHUD
from editor import EditorFases
from rede import ServidorLAN, ClienteLAN
from menu import MenuPrincipal, MenuMultiplayer, MenuConfiguracoes, MenuPausa
from notify import notify, EVENTO_FASE_CONCLUIDA, EVENTO_DANO_JOGADOR


# Constantes de Estado do Jogo (Padrão State)
ESTADO_MENU_PRINCIPAL = "MENU_PRINCIPAL"
ESTADO_LOBBY_MULTI = "LOBBY_MULTI"
ESTADO_EDITOR = "EDITOR"
ESTADO_PLAYTEST = "PLAYTEST"
ESTADO_CONFIGURACOES = "CONFIGURACOES"
ESTADO_JOGANDO_SOLO = "JOGANDO_SOLO"
ESTADO_JOGANDO_MULTI = "JOGANDO_MULTI"
ESTADO_PAUSADO = "PAUSADO"
ESTADO_DERROTA = "DERROTA"
ESTADO_VITORIA = "VITORIA"


class Jogo:
    """Controlador mestre do jogo (Padrão Singleton e State Pattern)."""
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Jogo, cls).__new__(cls)
        return cls._instancia

    def __init__(self):
        if hasattr(self, "_inicializado") and self._inicializado:
            return
        self._inicializado = True

        pygame.init()
        pygame.display.set_caption(TITULO_JOGO)
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.relogio = pygame.time.Clock()

        # Subsistemas Core
        self.audio = GerenciadorAudio()
        self.hud = InterfaceHUD()
        self.editor = EditorFases()

        # Menus
        self.menu_principal = MenuPrincipal()
        self.menu_multi = MenuMultiplayer()
        self.menu_config = MenuConfiguracoes()
        self.menu_pausa = MenuPausa()

        # Aplica configurações salvas no startup
        self.aplicar_configuracoes()

        # Rede LAN
        self.servidor_lan = None
        self.cliente_lan = None
        self.tipo_jogador_local = "scrappy"

        # Fase e Execução
        self.estado = ESTADO_MENU_PRINCIPAL
        self.estado_anterior = ESTADO_MENU_PRINCIPAL
        self.fase = GerenciadorFase(self.audio, tipo_jogador="scrappy")
        self.executando = True

        # Inscrição no barramento de eventos
        notify.inscrever(EVENTO_FASE_CONCLUIDA, self._ao_concluir_fase)

    def _ao_concluir_fase(self, pontos=0):
        """Callback acionado pelo EventBus ao cruzar o portal."""
        self.estado = ESTADO_VITORIA

    def iniciar_partida_solo(self):
        """Inicia uma nova campanha individual no Setor 01."""
        self.tipo_jogador_local = "scrappy"
        self.fase = GerenciadorFase(self.audio, tipo_jogador="scrappy")
        self.estado = ESTADO_JOGANDO_SOLO

    def iniciar_hospedagem_lan(self):
        """Inicia servidor LAN e conecta o host localmente como Scrappy (P1)."""
        if self.servidor_lan:
            self.servidor_lan.parar()
        self.servidor_lan = ServidorLAN(porta=5555)
        self.servidor_lan.iniciar()

        if self.cliente_lan:
            self.cliente_lan.desconectar()
        self.cliente_lan = ClienteLAN(player_id="scrappy")
        self.cliente_lan.conectar(ip_servidor="127.0.0.1", porta=5555)

        self.tipo_jogador_local = "scrappy"
        self.fase = GerenciadorFase(self.audio, tipo_jogador="scrappy")
        self.fase.configurar_multiplayer(remoto_tipo="byte")
        self.estado = ESTADO_JOGANDO_MULTI

    def conectar_cliente_lan(self):
        """Conecta a um servidor LAN existente como Byte (P2)."""
        ip = self.menu_multi.ip_atual
        if self.cliente_lan:
            self.cliente_lan.desconectar()
        self.cliente_lan = ClienteLAN(player_id="byte")
        self.cliente_lan.conectar(ip_servidor=ip, porta=5555)

        self.tipo_jogador_local = "byte"
        self.fase = GerenciadorFase(self.audio, tipo_jogador="byte")
        self.fase.configurar_multiplayer(remoto_tipo="scrappy")
        self.estado = ESTADO_JOGANDO_MULTI

    def iniciar_playtest_editor(self):
        """Compila os dados da grade do editor e entra em modo de teste."""
        linhas = self.editor.obter_linhas_mapa()
        self.fase = GerenciadorFase(self.audio, linhas_mapa=linhas, tipo_jogador="scrappy")
        self.estado = ESTADO_PLAYTEST

    def encerrar_conexoes_rede(self):
        """Desconecta clientes e desliga o servidor UDP com segurança."""
        if self.cliente_lan:
            self.cliente_lan.desconectar()
            self.cliente_lan = None
        if self.servidor_lan:
            self.servidor_lan.parar()
            self.servidor_lan = None

    def aplicar_configuracoes(self):
        """Aplica modo de exibição (janela/tela cheia) e volume dos efeitos sonoros."""
        if hasattr(self, "menu_config"):
            # Ajusta áudio
            if hasattr(self, "audio") and hasattr(self.audio, "definir_volume"):
                self.audio.definir_volume(self.menu_config.volume_sfx)

            # Ajusta modo de tela (janela ou fullscreen nativo escalado)
            try:
                if self.menu_config.tela_cheia:
                    self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.FULLSCREEN | pygame.SCALED)
                else:
                    self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
            except Exception:
                # Fallback caso o driver de vídeo ou ambiente dummy não suporte SCALED
                try:
                    flags = pygame.FULLSCREEN if self.menu_config.tela_cheia else 0
                    self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), flags)
                except Exception:
                    self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    def reiniciar_fase(self):
        """Reinicia a fase ativa mantendo o modo solo, playtest ou multi."""
        if self.estado in (ESTADO_PLAYTEST, ESTADO_DERROTA) and self.estado_anterior == ESTADO_PLAYTEST:
            self.iniciar_playtest_editor()
        elif self.estado_anterior == ESTADO_JOGANDO_MULTI:
            self.fase = GerenciadorFase(self.audio, tipo_jogador=self.tipo_jogador_local)
            parc = "byte" if self.tipo_jogador_local == "scrappy" else "scrappy"
            self.fase.configurar_multiplayer(remoto_tipo=parc)
            self.estado = ESTADO_JOGANDO_MULTI
        else:
            self.iniciar_partida_solo()

    def tratar_eventos(self):
        """Distribui o processamento de eventos conforme o estado atual."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.executando = False
                return

            # 1. MENU PRINCIPAL
            if self.estado == ESTADO_MENU_PRINCIPAL:
                escolha = self.menu_principal.tratar_evento(evento)
                if escolha == 0:  # Novo Jogo Solo
                    self.iniciar_partida_solo()
                elif escolha == 1:  # Multiplayer LAN
                    self.estado = ESTADO_LOBBY_MULTI
                elif escolha == 2:  # Editor de Fases
                    self.estado = ESTADO_EDITOR
                elif escolha == 3:  # Configurações
                    self.estado = ESTADO_CONFIGURACOES
                elif escolha == 4:  # Sair
                    self.executando = False

            # 2. LOBBY MULTIPLAYER LAN
            elif self.estado == ESTADO_LOBBY_MULTI:
                escolha = self.menu_multi.tratar_evento(evento)
                if escolha == 0:  # Hospedar Servidor
                    self.iniciar_hospedagem_lan()
                elif escolha == 1:  # Conectar Cliente
                    self.conectar_cliente_lan()
                elif escolha == 2:  # Alternar IP
                    self.menu_multi.alternar_ip()
                elif escolha == 3 or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                    self.estado = ESTADO_MENU_PRINCIPAL

            # 3. EDITOR DE FASES
            elif self.estado == ESTADO_EDITOR:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.estado = ESTADO_MENU_PRINCIPAL
                        return
                    elif evento.key == pygame.K_t:
                        self.estado_anterior = ESTADO_EDITOR
                        self.iniciar_playtest_editor()
                        return

                # Checa botão "Testar [T]" nos botões de ação do editor
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    mx, my = evento.pos
                    for btn in self.editor.botoes_acao:
                        if btn["id"] == "testar" and btn["rect"].collidepoint(mx, my):
                            self.estado_anterior = ESTADO_EDITOR
                            self.iniciar_playtest_editor()
                            return

                self.editor.tratar_evento(evento)

            # 4. CONFIGURAÇÕES
            elif self.estado == ESTADO_CONFIGURACOES:
                escolha = self.menu_config.tratar_evento(evento)
                if escolha == 0:
                    self.menu_config.alternar_volume()
                    self.aplicar_configuracoes()
                elif escolha == 1:
                    self.menu_config.alternar_tela()
                    self.aplicar_configuracoes()
                elif escolha == 2:
                    # Redefinir controles ou opções
                    self.menu_config.volume_sfx = 100
                    self.menu_config.tela_cheia = False
                    self.menu_config.opcoes[0] = "1. EFEITOS SONOROS (SFX): [ 100% ]"
                    self.menu_config.opcoes[1] = "2. MODO DE TELA: [ JANELA ]"
                    self.menu_config.salvar_configuracoes()
                    self.aplicar_configuracoes()
                elif escolha == 3 or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                    self.estado = ESTADO_MENU_PRINCIPAL

            # 5. GAMEPLAY (SOLO, MULTI OU PLAYTEST)
            elif self.estado in (ESTADO_JOGANDO_SOLO, ESTADO_JOGANDO_MULTI, ESTADO_PLAYTEST):
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if self.estado == ESTADO_PLAYTEST:
                            self.estado = ESTADO_EDITOR
                        else:
                            self.estado_anterior = self.estado
                            self.estado = ESTADO_PAUSADO
                    elif evento.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                        self.fase.jogador.pular()
                    elif evento.key in (pygame.K_k, pygame.K_LSHIFT, pygame.K_RSHIFT):
                        self.fase.jogador.executar_dash()
                    elif evento.key in (pygame.K_j, pygame.K_x):
                        self.fase.jogador.atirar(self.fase.projeteis_jogador)

                elif evento.type == pygame.KEYUP:
                    if evento.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                        self.fase.jogador.cortar_pulo()

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        self.fase.jogador.atirar(self.fase.projeteis_jogador)

            # 6. MENU DE PAUSA
            elif self.estado == ESTADO_PAUSADO:
                escolha = self.menu_pausa.tratar_evento(evento)
                if escolha == 0 or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                    self.estado = self.estado_anterior
                elif escolha == 1 or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_r):
                    self.reiniciar_fase()
                elif escolha == 2 or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_m):
                    self.encerrar_conexoes_rede()
                    self.estado = ESTADO_MENU_PRINCIPAL

            # 7. DERROTA OU VITÓRIA
            elif self.estado in (ESTADO_DERROTA, ESTADO_VITORIA):
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        self.reiniciar_fase()
                    elif evento.key == pygame.K_ESCAPE:
                        if self.estado_anterior == ESTADO_PLAYTEST:
                            self.estado = ESTADO_EDITOR
                        else:
                            self.encerrar_conexoes_rede()
                            self.estado = ESTADO_MENU_PRINCIPAL

    def atualizar(self):
        """Atualização de lógica e sincronização em tempo real."""
        if self.estado in (ESTADO_JOGANDO_SOLO, ESTADO_JOGANDO_MULTI, ESTADO_PLAYTEST):
            teclas = pygame.key.get_pressed()
            self.fase.atualizar(teclas)

            # Sincronização de Rede no modo Multiplayer LAN
            if self.estado == ESTADO_JOGANDO_MULTI and self.cliente_lan and self.fase.jogador:
                # 1. Enviar estado do jogador local
                p = self.fase.jogador
                estado_str = "run" if abs(p.vel_x) > 0.5 else ("jump" if not p.no_chao else "idle")
                self.cliente_lan.enviar_estado(
                    p.pos_x, p.pos_y, p.vel_x, p.vel_y,
                    estado_str, p.olhando_direita, 0, p.vida
                )

                # 2. Interpolar movimento dos parceiros recebidos (LERP)
                self.cliente_lan.atualizar_lerp(fator_lerp=0.25)
                remotos = self.cliente_lan.obter_jogadores()

                if remotos and self.fase.jogador_remoto:
                    for r_id, dados in remotos.items():
                        self.fase.jogador_remoto.atualizar_dados(
                            dados["x"], dados["y"], dados["olhando_dir"], dados["vida"]
                        )
                        break

            # Transições de Estado de Fim de Fase
            if self.fase.derrota:
                self.estado = ESTADO_DERROTA
            elif self.fase.fase_concluida:
                self.estado = ESTADO_VITORIA

    def desenhar(self):
        """Renderiza a camada visual correspondente ao estado ativo."""
        if self.estado in (ESTADO_JOGANDO_SOLO, ESTADO_JOGANDO_MULTI, ESTADO_PLAYTEST, ESTADO_PAUSADO, ESTADO_DERROTA, ESTADO_VITORIA):
            self.fase.desenhar(self.tela)
            self.hud.desenhar_hud(self.tela, self.fase.jogador, self.fase.jogador_remoto)

        # Telas e Menus
        if self.estado == ESTADO_MENU_PRINCIPAL:
            self.fase.desenhar(self.tela)
            self.menu_principal.desenhar(self.tela)

        elif self.estado == ESTADO_LOBBY_MULTI:
            self.fase.desenhar(self.tela)
            self.menu_multi.desenhar(self.tela)

        elif self.estado == ESTADO_EDITOR:
            self.editor.desenhar(self.tela)

        elif self.estado == ESTADO_CONFIGURACOES:
            self.fase.desenhar(self.tela)
            self.menu_config.desenhar(self.tela)

        elif self.estado == ESTADO_PAUSADO:
            self.menu_pausa.desenhar(self.tela)

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

        self.encerrar_conexoes_rede()
        pygame.quit()
        sys.exit()
