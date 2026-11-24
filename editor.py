# -*- coding: utf-8 -*-
"""
Módulo do Editor de Fases (Level Maker)
Rust & Byte: O Despertar da Sucata

Permite criar, modificar, salvar e testar fases customizadas usando
uma grade matricial interativa de 32x32 pixels, paleta de tiles
e persistência em arquivos .npz (NumPy comprimido) e .json.
"""

import os
import json
import pygame
import numpy as np

from configuracoes import (
    TAMANHO_BLOCO, LARGURA_TELA, ALTURA_TELA, COR_FUNDO,
    COR_TEXTO, COR_TEXTO_MUTED, COR_DESTAQUE
)
from fabrica_tiles import fabrica_tiles


# Lista de tiles disponíveis na paleta com seus nomes descritivos
TILES_PALETA = [
    ('#', "Bloco Sólido"),
    ('=', "Esteira Rolante"),
    ('^', "Armadilha Espinho"),
    ('@', "Spawn Scrappy (P1)"),
    ('2', "Spawn Byte (P2)"),
    ('D', "Drone Parafuso"),
    ('S', "Robô Soldador"),
    ('O', "Óleo (+1 HP)"),
    ('P', "Parafuso (+100)"),
    ('B', "Bateria (Arma)"),
    ('E', "Portal de Saída"),
]

LARGURA_GRID_PADRAO = 70
ALTURA_GRID_PADRAO = 15


class EditorFases:
    """Interface do criador de fases com manipulação de grade e paleta."""
    def __init__(self):
        self.colunas = LARGURA_GRID_PADRAO
        self.linhas = ALTURA_GRID_PADRAO
        self.scroll_x = 0
        self.tile_selecionado = '#'
        self.mensagem_status = "Clique com botão esquerdo para pintar, direito para apagar. [T] para Testar."
        self.tempo_status = 0

        self.fonte = pygame.font.SysFont("Arial", 13, bold=True)
        self.fonte_pequena = pygame.font.SysFont("Arial", 11)

        # Matriz de caracteres do mapa
        self.grid = [[' ' for _ in range(self.colunas)] for _ in range(self.linhas)]
        self._inicializar_chao_basico()

        # Botões de ação
        self.botoes_acao = [
            {"id": "salvar", "texto": "Salvar (.npz)", "rect": pygame.Rect(LARGURA_TELA - 310, 10, 95, 26)},
            {"id": "limpar", "texto": "Limpar Grid", "rect": pygame.Rect(LARGURA_TELA - 205, 10, 85, 26)},
            {"id": "testar", "texto": "Testar [T]", "rect": pygame.Rect(LARGURA_TELA - 110, 10, 80, 26)},
        ]

        # Áreas da paleta
        self.botoes_paleta = []
        self._configurar_paleta()

    def _inicializar_chao_basico(self):
        """Cria um chão padrão de início e os pontos de spawn."""
        for c in range(self.colunas):
            self.grid[self.linhas - 1][c] = '#'
            self.grid[self.linhas - 2][c] = '#'
        self.grid[self.linhas - 3][2] = '@'
        self.grid[self.linhas - 3][4] = '2'
        self.grid[self.linhas - 3][self.colunas - 3] = 'E'

    def _configurar_paleta(self):
        """Monta as caixas clicáveis dos tiles na barra inferior."""
        largura_item = 58
        altura_item = 48
        y_painel = ALTURA_TELA - 58

        for idx, (char_id, nome) in enumerate(TILES_PALETA):
            x = 15 + idx * (largura_item + 6)
            if x + largura_item < LARGURA_TELA - 10:
                rect = pygame.Rect(x, y_painel, largura_item, altura_item)
                self.botoes_paleta.append({
                    "char": char_id,
                    "nome": nome,
                    "rect": rect
                })

    def atualizar(self):
        """Atualização periódica do editor (animações, timers de status)."""
        pass

    def tratar_evento(self, evento):
        """Processa interações de mouse e teclado no editor."""
        # Rolagem horizontal via teclas A/D ou Setas
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_RIGHT, pygame.K_d):
                self.scroll_x = min((self.colunas * TAMANHO_BLOCO) - LARGURA_TELA, self.scroll_x + TAMANHO_BLOCO * 2)
            elif evento.key in (pygame.K_LEFT, pygame.K_a):
                self.scroll_x = max(0, self.scroll_x - TAMANHO_BLOCO * 2)
            elif evento.key == pygame.K_s:
                self.salvar_fase()

        # Cliques do Mouse
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = evento.pos

            # Rolagem por roda do mouse (botões 4 e 5)
            if evento.button == 4:
                self.scroll_x = max(0, self.scroll_x - TAMANHO_BLOCO * 2)
                return
            elif evento.button == 5:
                self.scroll_x = min((self.colunas * TAMANHO_BLOCO) - LARGURA_TELA, self.scroll_x + TAMANHO_BLOCO * 2)
                return

            # Checar clique nos botões de ação superiores
            for btn in self.botoes_acao:
                if btn["rect"].collidepoint(mx, my):
                    if btn["id"] == "salvar":
                        self.salvar_fase()
                    elif btn["id"] == "limpar":
                        self.limpar_grid()
                    return

            # Checar clique na paleta inferior
            for btn in self.botoes_paleta:
                if btn["rect"].collidepoint(mx, my):
                    self.tile_selecionado = btn["char"]
                    self.definir_status(f"Selecionado: {btn['nome']}")
                    return

            # Clique na grade de tiles
            if my < ALTURA_TELA - 65 and my > 45:
                col = (mx + self.scroll_x) // TAMANHO_BLOCO
                lin = (my - 45) // TAMANHO_BLOCO

                if 0 <= lin < self.linhas and 0 <= col < self.colunas:
                    if evento.button == 1:  # Botão esquerdo: Pintar
                        self.grid[lin][col] = self.tile_selecionado
                    elif evento.button == 3:  # Botão direito: Apagar
                        self.grid[lin][col] = ' '

        # Pintura contínua arrastando o mouse com botão pressionado
        elif evento.type == pygame.MOUSEMOTION:
            botoes = pygame.mouse.get_pressed()
            mx, my = evento.pos
            if my < ALTURA_TELA - 65 and my > 45:
                col = (mx + self.scroll_x) // TAMANHO_BLOCO
                lin = (my - 45) // TAMANHO_BLOCO
                if 0 <= lin < self.linhas and 0 <= col < self.colunas:
                    if botoes[0]:  # Esquerdo
                        self.grid[lin][col] = self.tile_selecionado
                    elif botoes[2]:  # Direito
                        self.grid[lin][col] = ' '

    def definir_status(self, texto):
        """Atualiza a mensagem de feedback do rodapé."""
        self.mensagem_status = texto
        self.tempo_status = 180

    def limpar_grid(self):
        """Reseta as células da grade com chão mínimo."""
        self.grid = [[' ' for _ in range(self.colunas)] for _ in range(self.linhas)]
        self._inicializar_chao_basico()
        self.definir_status("Grade limpa com chão padrão.")

    def salvar_fase(self, caminho_npz="fase_customizada.npz", caminho_json="fase_customizada.json"):
        """Salva a matriz de dados em formato .npz comprimido e .json aberto."""
        try:
            # 1. Salvar no formato binário comprimido NumPy (.npz)
            char_array = np.array(self.grid, dtype='<U1')
            np.savez_compressed(caminho_npz, mapa=char_array)

            # 2. Salvar cópia em JSON estruturado
            linhas_str = ["".join(linha) for linha in self.grid]
            dados_json = {
                "titulo": "Fase Customizada - Rust & Byte",
                "colunas": self.colunas,
                "linhas": self.linhas,
                "mapa": linhas_str
            }
            with open(caminho_json, "w", encoding="utf-8") as f:
                json.dump(dados_json, f, indent=2, ensure_ascii=False)

            self.definir_status(f"Fase salva com sucesso em '{caminho_npz}' e '{caminho_json}'!")
            print(f"[Editor] Fase salva em {caminho_npz}")
            return True
        except Exception as e:
            self.definir_status(f"Erro ao salvar fase: {e}")
            return False

    def carregar_fase(self, caminho_npz="fase_customizada.npz", caminho_json="fase_customizada.json"):
        """Carrega dados salvos em .npz ou .json para a grade do editor."""
        if os.path.exists(caminho_npz):
            try:
                dados = np.load(caminho_npz)
                matriz = dados['mapa']
                self.linhas, self.colunas = matriz.shape
                self.grid = [list(linha) for linha in matriz]
                self.definir_status("Fase carregada com sucesso do arquivo .npz!")
                return True
            except Exception as e:
                print(f"[Editor] Falha ao carregar .npz: {e}")

        if os.path.exists(caminho_json):
            try:
                with open(caminho_json, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                linhas_str = dados["mapa"]
                self.grid = [list(linha) for linha in linhas_str]
                self.linhas = len(self.grid)
                self.colunas = len(self.grid[0]) if self.linhas > 0 else self.colunas
                self.definir_status("Fase carregada com sucesso do JSON!")
                return True
            except Exception as e:
                print(f"[Editor] Falha ao carregar JSON: {e}")

        return False

    def obter_linhas_mapa(self):
        """Retorna as linhas no formato de lista de strings para o GerenciadorFase."""
        return ["".join(linha) for linha in self.grid]

    def desenhar(self, superficie):
        """Renderiza a interface do editor, a grade e as barras de ferramentas."""
        superficie.fill(COR_FUNDO)

        # 1. Desenhar a Grade de Blocos
        inicio_y = 45
        col_ini = max(0, self.scroll_x // TAMANHO_BLOCO)
        col_fim = min(self.colunas, (self.scroll_x + LARGURA_TELA) // TAMANHO_BLOCO + 2)

        for l in range(self.linhas):
            for c in range(col_ini, col_fim):
                x = c * TAMANHO_BLOCO - self.scroll_x
                y = inicio_y + l * TAMANHO_BLOCO

                # Linhas da Grade de Guia
                pygame.draw.rect(superficie, (35, 32, 45), (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

                char = self.grid[l][c]
                if char != ' ':
                    tile_surf = fabrica_tiles.obter_tile(char)
                    if tile_surf:
                        superficie.blit(tile_surf, (x, y))

        # 2. Barra Superior de Controle
        barra_topo = pygame.Rect(0, 0, LARGURA_TELA, 42)
        pygame.draw.rect(superficie, (18, 16, 26), barra_topo)
        pygame.draw.line(superficie, (60, 65, 80), (0, 42), (LARGURA_TELA, 42), 1)

        txt_titulo = self.fonte.render("EDITOR DE FASES (LEVEL MAKER)", True, COR_DESTAQUE)
        superficie.blit(txt_titulo, (15, 12))

        txt_scroll = self.fonte_pequena.render(f"Posição: {self.scroll_x}px | Teclas: [A/D/Setas] Rolar | [ESC] Menu", True, COR_TEXTO_MUTED)
        superficie.blit(txt_scroll, (260, 15))

        # Botões de Ação
        for btn in self.botoes_acao:
            cor_btn = (45, 50, 65) if btn["id"] != "testar" else (30, 140, 80)
            pygame.draw.rect(superficie, cor_btn, btn["rect"], border_radius=4)
            pygame.draw.rect(superficie, (90, 100, 125), btn["rect"], 1, border_radius=4)
            t = self.fonte.render(btn["texto"], True, COR_TEXTO)
            superficie.blit(t, (btn["rect"].centerx - t.get_width() // 2, btn["rect"].centery - t.get_height() // 2))

        # 3. Barra Inferior da Paleta
        barra_base = pygame.Rect(0, ALTURA_TELA - 64, LARGURA_TELA, 64)
        pygame.draw.rect(superficie, (18, 16, 26), barra_base)
        pygame.draw.line(superficie, (60, 65, 80), (0, ALTURA_TELA - 64), (LARGURA_TELA, ALTURA_TELA - 64), 1)

        for btn in self.botoes_paleta:
            selecionado = (btn["char"] == self.tile_selecionado)
            cor_borda = COR_DESTAQUE if selecionado else (60, 65, 80)
            cor_fundo = (45, 42, 60) if selecionado else (28, 26, 36)

            pygame.draw.rect(superficie, cor_fundo, btn["rect"], border_radius=4)
            pygame.draw.rect(superficie, cor_borda, btn["rect"], 2 if selecionado else 1, border_radius=4)

            # Ícone
            icone = fabrica_tiles.obter_icone_redimensionado(btn["char"], 24)
            superficie.blit(icone, (btn["rect"].centerx - 12, btn["rect"].top + 4))

            # Nome curto
            nome_curto = btn["nome"][:8]
            t_nome = self.fonte_pequena.render(nome_curto, True, COR_TEXTO if selecionado else COR_TEXTO_MUTED)
            superficie.blit(t_nome, (btn["rect"].centerx - t_nome.get_width() // 2, btn["rect"].top + 30))

        # 4. Mensagem de Feedback / Status
        if self.mensagem_status:
            t_status = self.fonte_pequena.render(self.mensagem_status, True, (100, 240, 180))
            superficie.blit(t_status, (15, ALTURA_TELA - 82))
