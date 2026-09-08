# -*- coding: utf-8 -*-
"""
Módulo de Configurações e Constantes do Jogo
Rust & Byte: O Despertar da Sucata
"""

# Dimensões da Janela e Display
LARGURA_TELA = 840
ALTURA_TELA = 480
TITULO_JOGO = "Rust & Byte: O Despertar da Sucata"
FPS = 60

# Tamanho padrão dos blocos (Tiles)
TAMANHO_BLOCO = 32

# Paleta de Cores Industriais (RGB)
COR_FUNDO = (24, 20, 32)            # Roxo escuro industrial / fumaça
COR_FUNDO_DISTANTE = (45, 34, 54)   # Silhueta ao longe
COR_PLATAFORMA = (70, 75, 88)       # Metal escuro
COR_PLATAFORMA_BORDA = (120, 130, 145) # Aço escovado
COR_ESTEIRA = (180, 120, 40)        # Amarelo ocre industrial
COR_ESTEIRA_LISTRA = (30, 30, 30)   # Listras pretas de advertência

COR_TEXTO = (240, 240, 245)
COR_TEXTO_MUTED = (160, 165, 180)
COR_DESTAQUE = (245, 160, 30)       # Âmbar / Alerta

# Cores de Entidades e Efeitos
COR_JOGADOR_CHASSI = (50, 160, 220)  # Azul metálico / Ciano
COR_JOGADOR_OLHO = (255, 240, 60)    # Amarelo neon
COR_TIRO_PLASMA = (0, 230, 255)      # Ciano brilhante
COR_TIRO_INIMIGO = (255, 80, 60)     # Laranja avermelhado

COR_DRONE = (190, 60, 60)           # Vermelho alerta
COR_SOLDADOR = (150, 140, 60)        # Bronze oxidado
COR_OLEO = (255, 190, 20)           # Dourado óleo
COR_PARAFUSO = (255, 215, 0)        # Ouro
COR_BATERIA = (40, 220, 140)        # Verde elétrico
COR_ESPINHO = (210, 40, 40)         # Vermelho perigo
COR_PORTAL = (180, 80, 255)         # Púrpura de transição

# Física do Jogador
GRAVIDADE = 0.65
VELOCIDADE_MAX_QUEDA = 12.0
VELOCIDADE_CORRIDA = 4.2
ACELERACAO_CHAO = 0.8
ATRITO_CHAO = 0.5
ATRITO_AR = 0.15

FORCA_PULO = -10.5
CORTE_PULO = 0.5                     # Redução de impulso se soltar a tecla prematuramente
FORCA_PULO_DUPLO = -9.0              # Impulso do micro-jetpack

VELOCIDADE_DASH = 10.0
DURACAO_DASH_FRAMES = 12             # ~0.2 segundos a 60 FPS
RECARGA_DASH_FRAMES = 40             # ~0.66 segundos de cooldown

# Combate
VIDA_MAX_JOGADOR = 3
FRAMES_INVULNERABILIDADE = 70        # Tempo de piscar após sofrer dano (~1.15s)
CADENCIA_TIRO_NORMAL = 14            # Frames entre tiros (~4.2 tiros por seg)
DURACAO_TIRO_TRIPLO_FRAMES = 600     # 10 segundos de Power-Up
VELOCIDADE_PROJETIL = 9.0
