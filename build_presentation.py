#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador da Apresentação de Slides Acadêmica - Rust & Byte (TAC - Prof. Vanderson)
Gera:
  1. Apresentacao_Rust_And_Byte.html (Apresentação interativa com navegação, fullscreen, grid e atalhos)
  2. Apresentacao_Rust_And_Byte.pdf  (Versão PDF compilada em formato 16:9 widescreen para entrega)
"""

import os
import subprocess

DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAMAS_DIR = os.path.join(DIR, "diagramas")

def carregar_svg(nome):
    path = os.path.join(DIAGRAMAS_DIR, f"{nome}.svg")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            svg = f.read()
            # Garante que o SVG seja responsivo dentro do slide
            return f'<div class="svg-wrapper">{svg}</div>'
    return f"<p style='color:red;'>[Diagrama {nome}.svg não encontrado]</p>"

SVG_PAC = carregar_svg("diag0")
SVG_UML = carregar_svg("diag1")
SVG_SEQ = carregar_svg("diag2")
SVG_FSM = carregar_svg("diag3")
SVG_ENG = carregar_svg("diag4")
SVG_MEN = carregar_svg("diag_menus")
SVG_PAT = carregar_svg("diag_patterns")

HTML_SLIDES = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apresentação: Rust & Byte - TAC (Prof. Vanderson)</title>
    <style>
        :root {{
            --bg-dark: #0a0e17;
            --bg-card: rgba(18, 25, 41, 0.95);
            --bg-card-border: #23314d;
            --accent-amber: #f59e0b;
            --accent-cyan: #06b6d4;
            --accent-purple: #a855f7;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            --font-mono: "Fira Code", Menlo, Monaco, Consolas, "Courier New", monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: var(--font-sans);
            overflow: hidden;
            width: 100vw;
            height: 100vh;
            user-select: none;
        }}

        /* Barra de Progresso Superior */
        #progress-bar {{
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent-amber), var(--accent-cyan), var(--accent-purple));
            width: 0%;
            transition: width 0.3s ease;
            z-index: 1000;
        }}

        /* Contêiner de Slides */
        #slides-container {{
            position: relative;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
        }}

        .slide {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            padding: 3rem 4rem 4.5rem 4rem;
            display: flex;
            flex-direction: column;
            opacity: 0;
            visibility: hidden;
            transform: scale(0.98);
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            background: radial-gradient(circle at 85% 15%, rgba(6, 182, 212, 0.08) 0%, transparent 45%),
                        radial-gradient(circle at 15% 85%, rgba(245, 158, 11, 0.06) 0%, transparent 45%),
                        var(--bg-dark);
        }}

        .slide.active {{
            opacity: 1;
            visibility: visible;
            transform: scale(1);
            z-index: 10;
        }}

        /* Cabeçalho do Slide */
        .slide-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 2px solid var(--bg-card-border);
            padding-bottom: 0.75rem;
            margin-bottom: 1.5rem;
            flex-shrink: 0;
        }}

        .slide-title-group {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .slide-tag {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 700;
            color: var(--accent-amber);
        }}

        .slide-title {{
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .slide-number-badge {{
            font-size: 0.85rem;
            font-family: var(--font-mono);
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.05);
            padding: 0.3rem 0.7rem;
            border-radius: 6px;
            border: 1px solid var(--bg-card-border);
        }}

        /* Corpo do Slide */
        .slide-body {{
            flex: 1;
            display: flex;
            gap: 2rem;
            min-height: 0; /* Previne overflow vertical */
            align-items: stretch;
        }}

        /* Grid de Colunas */
        .col-half {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            min-height: 0;
        }}

        .col-third {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            min-height: 0;
        }}

        /* Cards Estilizados */
        .card {{
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }}

        .card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--accent-cyan);
        }}

        .card.card-amber::before {{ background: var(--accent-amber); }}
        .card.card-purple::before {{ background: var(--accent-purple); }}
        .card.card-green::before {{ background: var(--accent-green); }}

        .card-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .card-text {{
            font-size: 0.95rem;
            color: var(--text-muted);
            line-height: 1.5;
        }}

        .card-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            font-size: 0.92rem;
            color: var(--text-main);
        }}

        .card-list li {{
            display: flex;
            align-items: flex-start;
            gap: 0.5rem;
            line-height: 1.4;
        }}

        .card-list li::before {{
            content: "▸";
            color: var(--accent-amber);
            font-weight: bold;
        }}

        /* Badges de Destaque */
        .pill {{
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            background: rgba(6, 182, 212, 0.15);
            color: var(--accent-cyan);
            border: 1px solid rgba(6, 182, 212, 0.3);
        }}

        .pill-amber {{
            background: rgba(245, 158, 11, 0.15);
            color: var(--accent-amber);
            border-color: rgba(245, 158, 11, 0.3);
        }}

        .pill-purple {{
            background: rgba(168, 85, 247, 0.15);
            color: var(--accent-purple);
            border-color: rgba(168, 85, 247, 0.3);
        }}

        .pill-green {{
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-green);
            border-color: rgba(16, 185, 129, 0.3);
        }}

        /* Diagramas SVG nos Slides */
        .svg-wrapper {{
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(10, 14, 23, 0.85);
            border: 1px solid var(--bg-card-border);
            border-radius: 12px;
            padding: 1rem;
            overflow: hidden;
        }}

        .svg-wrapper svg {{
            max-width: 100%;
            max-height: 100%;
            width: auto;
            height: auto;
            object-fit: contain;
        }}

        /* Slide 1 - Capa Especial */
        .slide-cover {{
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 2rem 4rem;
            position: relative;
        }}

        .cover-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(245, 158, 11, 0.1);
            color: var(--accent-amber);
            border: 1px solid rgba(245, 158, 11, 0.3);
            padding: 0.4rem 1.25rem;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 1.5rem;
        }}

        .cover-title {{
            font-size: 4rem;
            font-weight: 900;
            line-height: 1.1;
            letter-spacing: -1.5px;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #ffffff 30%, var(--accent-amber) 70%, var(--accent-cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .cover-subtitle {{
            font-size: 1.4rem;
            color: var(--text-muted);
            max-width: 850px;
            line-height: 1.5;
            margin-bottom: 2.5rem;
        }}

        .cover-meta-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            width: 100%;
            max-width: 980px;
            text-align: left;
        }}

        .cover-meta-card {{
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            border-radius: 10px;
            padding: 1rem 1.25rem;
        }}

        .cover-meta-label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--accent-cyan);
            font-weight: 700;
            margin-bottom: 0.25rem;
        }}

        .cover-meta-val {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #ffffff;
        }}

        /* Tabelas Compactas */
        .slide-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }}

        .slide-table th {{
            background: rgba(255, 255, 255, 0.05);
            color: var(--accent-cyan);
            font-weight: 700;
            text-align: left;
            padding: 0.5rem 0.75rem;
            border-bottom: 1px solid var(--bg-card-border);
        }}

        .slide-table td {{
            padding: 0.5rem 0.75rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-main);
            vertical-align: top;
        }}

        .slide-table tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}

        /* Código e Destaques */
        code {{
            font-family: var(--font-mono);
            background: rgba(0, 0, 0, 0.4);
            color: var(--accent-amber);
            padding: 0.15rem 0.35rem;
            border-radius: 4px;
            font-size: 0.85em;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        /* Barra de Controle Inferior */
        #toolbar {{
            position: fixed;
            bottom: 1rem;
            right: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            background: rgba(18, 25, 41, 0.9);
            backdrop-filter: blur(8px);
            border: 1px solid var(--bg-card-border);
            padding: 0.4rem 0.75rem;
            border-radius: 30px;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }}

        .btn-ctrl {{
            background: none;
            border: none;
            color: var(--text-main);
            font-size: 1rem;
            cursor: pointer;
            padding: 0.35rem 0.6rem;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }}

        .btn-ctrl:hover {{
            background: rgba(255, 255, 255, 0.1);
            color: var(--accent-cyan);
        }}

        #counter {{
            font-size: 0.85rem;
            font-family: var(--font-mono);
            font-weight: 700;
            color: var(--text-muted);
            padding: 0 0.5rem;
        }}

        /* Painel de Visão Geral (Grid) */
        #overview-modal {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(10, 14, 23, 0.95);
            backdrop-filter: blur(12px);
            z-index: 2000;
            padding: 3rem;
            display: none;
            flex-direction: column;
            overflow-y: auto;
        }}

        #overview-modal.open {{
            display: flex;
        }}

        .overview-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }}

        .overview-title {{
            font-size: 1.8rem;
            font-weight: 800;
            color: #ffffff;
        }}

        .overview-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 1.5rem;
        }}

        .overview-thumb {{
            background: var(--bg-card);
            border: 2px solid var(--bg-card-border);
            border-radius: 8px;
            padding: 1rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            min-height: 130px;
        }}

        .overview-thumb:hover, .overview-thumb.active {{
            border-color: var(--accent-cyan);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(6, 182, 212, 0.2);
        }}

        .overview-thumb-num {{
            font-size: 0.75rem;
            font-family: var(--font-mono);
            color: var(--accent-amber);
            font-weight: 700;
        }}

        .overview-thumb-title {{
            font-size: 0.95rem;
            font-weight: 700;
            color: #ffffff;
            line-height: 1.3;
        }}

        /* Dicas de Teclado no Rodapé */
        .keyboard-hint {{
            position: fixed;
            bottom: 1.25rem;
            left: 1.5rem;
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.3);
            display: flex;
            gap: 1rem;
            z-index: 900;
        }}

        /* Estilos de Impressão e Conversão PDF (16:9 Widescreen) */
        @media print {{
            @page {{
                size: 297mm 167mm; /* 16:9 Landscape */
                margin: 0;
            }}

            body, html {{
                width: 100%;
                height: 100%;
                overflow: visible !important;
                background-color: #0a0e17 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}

            #progress-bar, #toolbar, .keyboard-hint, #overview-modal {{
                display: none !important;
            }}

            #slides-container {{
                display: block !important;
                height: auto !important;
                overflow: visible !important;
            }}

            .slide {{
                position: relative !important;
                display: flex !important;
                opacity: 1 !important;
                visibility: visible !important;
                transform: none !important;
                page-break-after: always !important;
                break-after: page !important;
                width: 100vw !important;
                height: 100vh !important;
                padding: 2.5rem 3.5rem !important;
                box-sizing: border-box !important;
            }}

            .card {{
                box-shadow: none !important;
                border: 1px solid #23314d !important;
            }}
        }}
    </style>
</head>
<body>

    <div id="progress-bar"></div>

    <div id="slides-container">

        <!-- ==========================================
             SLIDE 1: CAPA OFICIAL
             ========================================== -->
        <section class="slide slide-cover active" id="slide-1">
            <div class="cover-badge">
                <span>⚡</span> Tópicos Avançados em Computação (TAC)
            </div>
            <h1 class="cover-title">RUST & BYTE</h1>
            <p class="cover-subtitle">
                O Despertar da Sucata: Desenvolvimento de Jogo 2D, Editor de Fases Matricial, Multiplayer LAN Cooperativo e Padrões de Projeto GoF
            </p>

            <div class="cover-meta-grid">
                <div class="cover-meta-card">
                    <div class="cover-meta-label">Discente / Autor</div>
                    <div class="cover-meta-val">Vitor de Souza</div>
                </div>
                <div class="cover-meta-card">
                    <div class="cover-meta-label">Orientador</div>
                    <div class="cover-meta-val">Prof. Vanderson</div>
                </div>
                <div class="cover-meta-card">
                    <div class="cover-meta-label">Etapas Integradas</div>
                    <div class="cover-meta-val">Trabalho 1 &amp; 2</div>
                </div>
                <div class="cover-meta-card">
                    <div class="cover-meta-label">Stack Tecnológica</div>
                    <div class="cover-meta-val">Python / Pygame-CE / UDP</div>
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 2: CONTEXTO E PROPOSTA DO JOGO
             ========================================== -->
        <section class="slide" id="slide-2">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Visão do Produto</span>
                    <h2 class="slide-title">1. Proposta, Sinopse e Pilares de Design</h2>
                </div>
                <span class="slide-number-badge">02 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half">
                    <div class="card card-amber">
                        <div class="card-title">
                            <span>🎮</span> Gênero e Universo Narrativo
                        </div>
                        <p class="card-text">
                            <strong>Rust &amp; Byte</strong> é um jogo de ação e plataforma 2D (<em>Run and Gun</em>) ambientado em um ferro-velho autônomo pós-apocalíptico onde autômatos descartados lutam contra a obsolescência forçada imposta pela megacorporação <em>Apex Robotics</em>.
                        </p>
                    </div>
                    <div class="card card-purple">
                        <div class="card-title">
                            <span>🤖</span> Dupla Cooperativa de Protagonistas
                        </div>
                        <ul class="card-list">
                            <li><strong>Scrappy (Jogador 1):</strong> Robô operário rústico com chassi de ferro fundido e canhão de rebites; foco em agilidade, saltos dinâmicos e ataque de precisão.</li>
                            <li><strong>Byte (Jogador 2):</strong> Unidade médica de suporte cibernético com revestimento de neon ciano; equipada com emissor de plasma e baterias sobressalentes.</li>
                        </ul>
                    </div>
                </div>
                <div class="col-half">
                    <div class="card card-green" style="height: 100%;">
                        <div class="card-title">
                            <span>🎯</span> 4 Pilares Fundamentais de Jogabilidade
                        </div>
                        <ul class="card-list" style="gap: 0.85rem;">
                            <li>
                                <strong>Física Precisa com Tolerância Motora:</strong>
                                Gravidade assimétrica, controle dinâmico de salto e janelas de tolerância (<em>Coyote Time</em> e <em>Jump Buffer</em>) que eliminam frustrações mecânicas.
                            </li>
                            <li>
                                <strong>Telegrafia Visual Estrita:</strong>
                                Inimigos possuem padrões claros de antecipação (mudança de cor e recuo pré-ataque), garantindo combate justo e tático.
                            </li>
                            <li>
                                <strong>Liberdade Criativa (Level Maker):</strong>
                                Editor gráfico matricial em tempo real integrado diretamente ao jogo, permitindo construir e testar fases personalizadas.
                            </li>
                            <li>
                                <strong>Multiplayer Cooperativo Fluido:</strong>
                                Arquitetura cliente-servidor em rede local (LAN) com protocolo UDP leve, interpolação LERP e respawn contínuo.
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 3: ARQUITETURA DO MOTOR E GAME LOOP
             ========================================== -->
        <section class="slide" id="slide-3">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Engenharia de Software</span>
                    <h2 class="slide-title">2. Arquitetura do Motor &amp; Game Loop 60 FPS</h2>
                </div>
                <span class="slide-number-badge">03 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half" style="flex: 0.95;">
                    <div class="card card-cyan">
                        <div class="card-title"><span>⚙️</span> Ciclo de Atualização Tripartite</div>
                        <p class="card-text">
                            O motor implementa a arquitetura canônica de jogos digitais, garantindo 60 Hz cravados via <code>pygame.time.Clock</code>:
                        </p>
                        <ul class="card-list">
                            <li><strong>1. Processamento de Eventos (Poll):</strong> Captura inputs de teclado/mouse e mensagens assíncronas dos sockets UDP.</li>
                            <li><strong>2. Atualização Física (Update):</strong> Integração de Euler semi-implícita, detecção e resolução de colisões AABB desacopladas por eixo.</li>
                            <li><strong>3. Renderização (Draw &amp; Flip):</strong> Desenho de parallax em 4 camadas, tiles via matriz, sprites de entidades e HUD.</li>
                        </ul>
                    </div>
                    <div class="card card-amber">
                        <div class="card-title"><span>📦</span> Desacoplamento Modular</div>
                        <p class="card-text">
                            A estrutura é distribuída em 5 pacotes autônomos: <code>Core</code> (orquestração), <code>Entities</code> (física e combate), <code>Level</code> (tiles e câmera), <code>Network</code> (LAN UDP) e <code>UI/Editor</code> (menus e grid).
                        </p>
                    </div>
                </div>
                <div class="col-half" style="flex: 1.05;">
                    {SVG_ENG}
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 4: PADRÕES DE PROJETO (VISÃO GERAL)
             ========================================== -->
        <section class="slide" id="slide-4">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Padrões de Projeto (GoF)</span>
                    <h2 class="slide-title">3. Padrões de Projeto Criacionais, Comportamentais e Arquiteturais</h2>
                </div>
                <span class="slide-number-badge">04 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half" style="flex: 0.85;">
                    <div class="card card-purple">
                        <div class="card-title"><span>🏛️</span> Fundamentação Teórica</div>
                        <p class="card-text">
                            O Trabalho 2 exigiu a aplicação formal dos Padrões de Projeto consagrados (GoF) para garantir manutenibilidade, baixo acoplamento e alta coesão:
                        </p>
                        <ul class="card-list">
                            <li><strong>Padrões Criacionais:</strong> Centralizam instâncias globais e gerenciam ciclo de vida de recursos pesados.</li>
                            <li><strong>Padrões Comportamentais:</strong> Estruturam a comunicação intermodular sem acoplamento direto e gerenciam máquinas de estado.</li>
                            <li><strong>Padrões Arquiteturais:</strong> Desacoplam operações de I/O de rede e preservam a fluidez de 60 quadros por segundo.</li>
                        </ul>
                    </div>
                    <div class="card card-green">
                        <div class="card-title"><span>✅</span> Benefícios Práticos</div>
                        <p class="card-text">
                            Zero vazamento de memória em fases gigantescas, facilidade de expansão de inimigos e replicação em rede limpa.
                        </p>
                    </div>
                </div>
                <div class="col-half" style="flex: 1.15;">
                    {SVG_PAT}
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 5: DETALHAMENTO DOS PADRÕES NO CÓDIGO
             ========================================== -->
        <section class="slide" id="slide-5">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Implementação Técnica</span>
                    <h2 class="slide-title">4. Padrões de Projeto: Detalhamento nos Módulos</h2>
                </div>
                <span class="slide-number-badge">05 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half">
                    <div class="card card-cyan">
                        <div class="card-title">
                            <span class="pill">Criacional</span> <strong>Flyweight / Factory</strong>
                        </div>
                        <p class="card-text">
                            <strong>Módulo:</strong> <code>fabrica_tiles.py</code><br>
                            Em fases com mais de 3.000 blocos de grade, cada superfície gráfica de textura é sintetizada uma única vez na memória de vídeo. A matriz armazena apenas IDs numéricos inteiros (0, 1, 2, ...), compartilhando os mesmos ponteiros de textura.
                        </p>
                    </div>
                    <div class="card card-amber">
                        <div class="card-title">
                            <span class="pill pill-amber">Criacional</span> <strong>Singleton</strong>
                        </div>
                        <p class="card-text">
                            <strong>Módulos:</strong> <code>audio.py</code>, <code>configuracoes.py</code>, <code>jogo.py</code><br>
                            Garante ponto de acesso único e global para o sintetizador procedural de áudio e as configurações do display, evitando recriações desnecessárias de mixers.
                        </p>
                    </div>
                </div>
                <div class="col-half">
                    <div class="card card-purple">
                        <div class="card-title">
                            <span class="pill pill-purple">Comportamental</span> <strong>Observer / Pub-Sub</strong>
                        </div>
                        <p class="card-text">
                            <strong>Módulo:</strong> <code>notify.py</code> (Barramento <code>EventBus</code>)<br>
                            Desacopla eventos do jogo. Quando um autômato é destruído ou um parafuso é coletado, a física emite um evento (<code>emitir("inimigo_morto", ...)</code>), notificando o HUD e o áudio sem que a classe de física conheça quem desenha a interface.
                        </p>
                    </div>
                    <div class="card card-green">
                        <div class="card-title">
                            <span class="pill pill-green">Comportamental</span> <strong>State Pattern (FSM)</strong>
                        </div>
                        <p class="card-text">
                            <strong>Módulos:</strong> <code>jogo.py</code> e <code>jogador.py</code><br>
                            Gerencia estados da aplicação (<code>MENU</code>, <code>EDITOR</code>, <code>PLAYTEST</code>, <code>MULTI</code>, <code>PAUSE</code>) e mecânicas do robô (<code>IDLE</code>, <code>RUN</code>, <code>JUMP</code>, <code>DASH</code>, <code>HURT</code>), eliminando condicionais aninhadas confusas.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 6: SUBSISTEMA 1 - EDITOR DE FASES
             ========================================== -->
        <section class="slide" id="slide-6">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Trabalho 2 — Subsistema 1</span>
                    <h2 class="slide-title">5. Editor de Fases Interativo (Level Maker)</h2>
                </div>
                <span class="slide-number-badge">06 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half">
                    <div class="card card-amber">
                        <div class="card-title"><span>🛠️</span> Especificações Técnicas da Ferramenta</div>
                        <ul class="card-list">
                            <li><strong>Resolução da Grade:</strong> Matriz matricial de 70 colunas × 15 linhas (2.240 × 480 pixels), blocos com padrão didático de 32×32px.</li>
                            <li><strong>Paleta de Construção Completa:</strong> Ar/Borracha, Chão de Sucata, Parede de Concreto, Plataforma Unidirecional (Jump-through), Espinhos Tóxicos, Checkpoints, Drones Voadores, Torretas, Boss e Baterias.</li>
                            <li><strong>Navegação e Câmera no Editor:</strong> Rolagem suave lateral via teclas <code>A</code>/<code>D</code> ou setas do teclado.</li>
                        </ul>
                    </div>
                    <div class="card card-cyan">
                        <div class="card-title"><span>💾</span> Persistência Dupla: .NPZ e .JSON</div>
                        <p class="card-text">
                            Salva e carrega mapas instantaneamente em dois formatos complementares:
                        </p>
                        <ul class="card-list">
                            <li><code>fase_customizada.npz</code>: Matriz comprimida com NumPy, compacta e ultraveloz para gravação/leitura direta.</li>
                            <li><code>fase_customizada.json</code>: Representação legível para inspeção humana, versionamento no Git e interoperabilidade.</li>
                        </ul>
                    </div>
                </div>
                <div class="col-half">
                    <div class="card card-green" style="height: 100%;">
                        <div class="card-title"><span>⚡</span> Modo Playtest Instantâneo (Tecla [T])</div>
                        <p class="card-text" style="font-size: 1.05rem; line-height: 1.6;">
                            O grande diferencial pedagógico e prático do editor é o <strong>Playtest em Tempo Real</strong>:
                        </p>
                        <ul class="card-list" style="gap: 1rem; margin-top: 0.5rem;">
                            <li>
                                Ao pressionar a tecla <strong>[T]</strong> ou clicar no botão <em>Testar</em>, o motor compila a matriz do editor em uma instância viva da classe <code>Fase</code> e inicia o gameplay imediatamente.
                            </li>
                            <li>
                                O desenvolvedor/jogador pode pular, atirar e verificar a jogabilidade da fase personalizada em segundos.
                            </li>
                            <li>
                                Ao pressionar <strong>[ESC]</strong>, o motor encerra a simulação de teste e retorna exatamente ao modo de edição com todo o mapa, histórico e paleta intactos.
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 7: SUBSISTEMA 2 - MULTIPLAYER EM LAN
             ========================================== -->
        <section class="slide" id="slide-7">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Trabalho 2 — Subsistema 2</span>
                    <h2 class="slide-title">6. Arquitetura Multiplayer em LAN (Cliente e Servidor)</h2>
                </div>
                <span class="slide-number-badge">07 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half">
                    <div class="card card-cyan">
                        <div class="card-title"><span>🌐</span> Protocolo de Transporte: UDP na Porta 5555</div>
                        <p class="card-text">
                            Inspirado na implementação didática de <code>server.py</code> e <code>client.py</code> (repositório <code>tac3</code>):
                        </p>
                        <ul class="card-list">
                            <li><strong>Por que UDP em vez de TCP?</strong> Datagramas leves sem a sobrecarga de <em>handshakes</em> de 3 vias e retransmissões do TCP. Para jogos de ação 2D frenéticos, a perda pontual de um pacote de posição é irrelevante, pois o próximo quadro já traz a posição mais recente.</li>
                            <li><strong>Descoberta e Conexão Rápida:</strong> O servidor exibe o IP local da máquina na tela do menu; o cliente digita o IP de destino e conecta instantaneamente.</li>
                        </ul>
                    </div>
                    <div class="card card-purple">
                        <div class="card-title"><span>🧵</span> Multithreading Desacoplado (Thread Worker)</div>
                        <p class="card-text">
                            A escuta dos sockets UDP é delegada a uma <strong>ReceiverThread</strong> assíncrona secundária:
                        </p>
                        <ul class="card-list">
                            <li>O loop principal de desenho do Pygame nunca é bloqueado por chamadas de rede de I/O (<code>recvfrom</code>).</li>
                            <li>A sincronização de leitura e escrita das entidades remotas é resguardada por primitivas <code>threading.Lock</code> (Thread-Safe).</li>
                        </ul>
                    </div>
                </div>
                <div class="col-half">
                    <div class="card card-amber">
                        <div class="card-title"><span>📡</span> Protocolo CSV de Datagramas Compactos</div>
                        <p class="card-text">
                            Mensagens serializadas em strings curtas separadas por vírgula, minimizando a largura de banda na rede local:
                        </p>
                        <table class="slide-table" style="margin-top: 0.5rem;">
                            <thead>
                                <tr>
                                    <th>Mensagem</th>
                                    <th>Formato / Payload</th>
                                    <th>Finalidade</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Posição</strong></td>
                                    <td><code>id,x,y,estado,dir</code></td>
                                    <td>Telemetria contínua a cada frame</td>
                                </tr>
                                <tr>
                                    <td><strong>Disparo</strong></td>
                                    <td><code>id,shoot,dx,dy,arma</code></td>
                                    <td>Replicação instantânea de tiros</td>
                                </tr>
                                <tr>
                                    <td><strong>Dano</strong></td>
                                    <td><code>id,hit,dano,hp</code></td>
                                    <td>Sincronização de vida e impacto</td>
                                </tr>
                                <tr>
                                    <td><strong>Saída</strong></td>
                                    <td><code>id,quit</code></td>
                                    <td>Desconexão graciosa do cliente</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="card card-green">
                        <div class="card-title"><span>⏱️</span> Detecção de Timeout (5.0s)</div>
                        <p class="card-text">
                            O servidor monitora o timestamp de cada jogador. Caso não receba datagramas por mais de 5 segundos, remove a entidade e notifica a sala, evitando robôs fantasmas na sessão.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 8: LERP E RESPAWN COOPERATIVO
             ========================================== -->
        <section class="slide" id="slide-8">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Sincronização e Experiência</span>
                    <h2 class="slide-title">7. Interpolação LERP &amp; Respawn Cooperativo Contínuo</h2>
                </div>
                <span class="slide-number-badge">08 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half">
                    <div class="card card-cyan">
                        <div class="card-title"><span>〰️</span> Interpolação Linear (LERP)</div>
                        <p class="card-text">
                            Devido a pequenas oscilações de latência em redes Wi-Fi, a posição do parceiro remoto recebida em pacotes UDP discretos poderia gerar travamentos visuais ("stuttering") ou teletransporte.
                        </p>
                        <ul class="card-list" style="margin-top: 0.5rem;">
                            <li>O motor aplica suavização contínua a cada quadro de renderização:
                                <br><code>pos_atual += (pos_alvo - pos_atual) * 0.3</code>
                            </li>
                            <li>O robô remoto desliza suavemente até as novas coordenadas, mantendo a animação natural a 60 FPS.</li>
                            <li><strong>Snap Inteligente de Posição:</strong> Caso a distância acumulada seja superior a 160 pixels (indicando teletransporte ou renascimento), o LERP faz o salto instantâneo sem animação de arraste.</li>
                        </ul>
                    </div>
                </div>
                <div class="col-half">
                    <div class="card card-green" style="height: 100%;">
                        <div class="card-title"><span>✨</span> Mecânica de Respawn Cooperativo (Sem Derrota Isolada)</div>
                        <p class="card-text" style="font-size: 1.05rem; line-height: 1.6;">
                            Um dos maiores desafios de UX em jogos multiplayer de plataforma é o tratamento da morte:
                        </p>
                        <ul class="card-list" style="gap: 1rem; margin-top: 0.5rem;">
                            <li>
                                <strong>No Modo Single Player:</strong> A morte ou queda em abismo aciona imediatamente a tela de Game Over e interrompe o progresso.
                            </li>
                            <li>
                                <strong>No Modo Multiplayer LAN:</strong> O jogador derrotado <strong>não</strong> é enviado à tela de derrota e nem perde a conexão com a sessão!
                            </li>
                            <li>
                                Seu robô renasce automaticamente ao lado do parceiro sobrevivente com <strong>3 pontos de vida cheios</strong> e <strong>120 frames (2 segundos) de invulnerabilidade temporária</strong> com efeito visual piscante.
                            </li>
                            <li>
                                Uma notificação em destaque (<em>"P1/P2 REAPARECEU NA FASE!"</em>) avisa a sala e a partida prossegue de forma cooperativa ininterrupta.
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 9: DIAGRAMA DE SEQUÊNCIA MULTIPLAYER
             ========================================== -->
        <section class="slide" id="slide-9">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Diagrama Estrutural de Apoio</span>
                    <h2 class="slide-title">8. Diagrama de Sequência: Ciclo de Sincronização UDP</h2>
                </div>
                <span class="slide-number-badge">09 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half" style="flex: 0.75;">
                    <div class="card card-purple">
                        <div class="card-title"><span>🔄</span> Fluxo Temporal de Mensagens</div>
                        <p class="card-text">
                            O diagrama ilustra o ciclo completo de comunicação entre as entidades de rede:
                        </p>
                        <ul class="card-list">
                            <li><strong>1. Envio UDP:</strong> Cliente 1 envia coordenadas e comandos para o Servidor via socket local.</li>
                            <li><strong>2. Processamento do Host:</strong> Servidor recebe pacote e atualiza tabela de participantes ativos.</li>
                            <li><strong>3. Broadcast da Sessão:</strong> Servidor replica os dados instantaneamente para o Cliente 2.</li>
                            <li><strong>4. Recepção Assíncrona:</strong> Thread de escuta do Cliente 2 captura o pacote com <code>Lock</code>.</li>
                            <li><strong>5. Aplicação LERP:</strong> No loop principal de renderização, o robô remoto tem sua posição suavizada na tela.</li>
                        </ul>
                    </div>
                </div>
                <div class="col-half" style="flex: 1.25;">
                    {SVG_SEQ}
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 10: SISTEMA DE MENUS E TRANSIÇÕES
             ========================================== -->
        <section class="slide" id="slide-10">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Interface do Usuário (UI)</span>
                    <h2 class="slide-title">9. Sistema de Menus e Diagrama de Transição de Telas</h2>
                </div>
                <span class="slide-number-badge">10 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half" style="flex: 0.85;">
                    <div class="card card-amber">
                        <div class="card-title"><span>🧭</span> Hierarquia Modular de Menus</div>
                        <ul class="card-list">
                            <li><strong>Menu Principal:</strong> Novo Jogo Solo, Multiplayer LAN, Editor de Fases, Configurações e Sair.</li>
                            <li><strong>Lobby Multiplayer:</strong> Hospedar sala (Host) ou Conectar como Cliente digitando IP/Porta.</li>
                            <li><strong>Menu de Configurações:</strong> Alternância de volume do áudio sintetizado e modo de janela/tela cheia.</li>
                            <li><strong>Menu de Pausa:</strong> Retomar jogo, reiniciar fase ou voltar ao menu principal.</li>
                        </ul>
                    </div>
                    <div class="card card-cyan">
                        <div class="card-title"><span>🖱️</span> Navegação Dual</div>
                        <p class="card-text">
                            Suporte simultâneo a navegação por teclado (Setas/WASD + Enter/Espaço/ESC) e detecção de hover e clique do mouse.
                        </p>
                    </div>
                </div>
                <div class="col-half" style="flex: 1.15;">
                    {SVG_MEN}
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 11: FÍSICA, COLISÕES E COMBATE
             ========================================== -->
        <section class="slide" id="slide-11">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Mecânicas Centrais (Trabalho 1)</span>
                    <h2 class="slide-title">10. Física Newtoniana, Colisões AABB e Inimigos</h2>
                </div>
                <span class="slide-number-badge">11 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half">
                    <div class="card card-green">
                        <div class="card-title"><span>📐</span> Resolução de Colisão AABB Desacoplada</div>
                        <p class="card-text">
                            Para prevenir o clássico bug de atravessamento (<em>tunneling</em>) em cantos de blocos:
                        </p>
                        <ul class="card-list">
                            <li><strong>1º Passo:</strong> Aplica deslocamento horizontal <code>dx = vx * dt</code> e resolve colisões apenas no eixo X.</li>
                            <li><strong>2º Passo:</strong> Aplica deslocamento vertical <code>dy = vy * dt</code> e resolve colisões no eixo Y, detectando solo (<code>no_chao = True</code>) ou impacto com teto.</li>
                        </ul>
                    </div>
                    <div class="card card-amber">
                        <div class="card-title"><span>🦘</span> Plataforma Responsiva</div>
                        <ul class="card-list">
                            <li><strong>Pulo Dinâmico:</strong> Soltar a tecla de salto antes do ápice reduz a velocidade vertical instantaneamente pela metade.</li>
                            <li><strong>Coyote Time (5 frames):</strong> Permite pular mesmo após deixar a borda da plataforma.</li>
                            <li><strong>Dash com I-Frames:</strong> Deslocamento rápido de 12 frames com invulnerabilidade total.</li>
                        </ul>
                    </div>
                </div>
                <div class="col-half">
                    <div class="card card-purple" style="height: 100%;">
                        <div class="card-title"><span>👾</span> Tipologia de Inimigos Telegrafados</div>
                        <table class="slide-table" style="margin-top: 0.5rem;">
                            <thead>
                                <tr>
                                    <th>Inimigo</th>
                                    <th>Comportamento</th>
                                    <th>Telegrafia</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Drone Sucata</strong></td>
                                    <td>Patrulha aérea senoidal com detecção do jogador</td>
                                    <td>Lente pisca em vermelho 0.5s antes da investida</td>
                                </tr>
                                <tr>
                                    <td><strong>Torreta Estática</strong></td>
                                    <td>Disparo balístico periódico em linha de visada</td>
                                    <td>Carregamento com faíscas elétricas visíveis</td>
                                </tr>
                                <tr>
                                    <td><strong>Mecha Sucateiro (Boss)</strong></td>
                                    <td>Movimentação pesada, salto esmagador e rajadas de rebites</td>
                                    <td>Aviso visual na tela, tremor de câmera e animação de pré-impacto</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 12: DIAGRAMA DE CLASSES UML COMPLETO
             ========================================== -->
        <section class="slide" id="slide-12">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Modelagem Orientada a Objetos</span>
                    <h2 class="slide-title">11. Diagrama de Classes UML Abrangente</h2>
                </div>
                <span class="slide-number-badge">12 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half" style="flex: 0.75;">
                    <div class="card card-cyan">
                        <div class="card-title"><span>🏗️</span> Estrutura das Classes</div>
                        <p class="card-text">
                            O diagrama ilustra o relacionamento formal entre os componentes do jogo:
                        </p>
                        <ul class="card-list">
                            <li><code>Jogo</code>: Fachada e controladora do loop principal.</li>
                            <li><code>Fase</code>: Gerencia o mapa, colisão e lista de entidades.</li>
                            <li><code>Jogador</code> e <code>JogadorRemoto</code>: Entidades polimórficas de controle local e representação em rede.</li>
                            <li><code>EditorFases</code>: Ferramenta de manipulação de grade matricial e serialização <code>.npz</code>.</li>
                            <li><code>LanServer</code> &amp; <code>LanClient</code>: Camada de comunicação UDP com threads dedicadas.</li>
                            <li><code>FabricaTiles</code> &amp; <code>BarramentoEventos</code>: Serviços de apoio e padrões de projeto.</li>
                        </ul>
                    </div>
                </div>
                <div class="col-half" style="flex: 1.25;">
                    {SVG_UML}
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 13: GUIA PRÁTICO E EXECUÇÃO
             ========================================== -->
        <section class="slide" id="slide-13">
            <div class="slide-header">
                <div class="slide-title-group">
                    <span class="slide-tag">Demonstração ao Vivo</span>
                    <h2 class="slide-title">12. Guia de Execução e Teste Prático</h2>
                </div>
                <span class="slide-number-badge">13 / 14</span>
            </div>
            <div class="slide-body">
                <div class="col-half">
                    <div class="card card-green">
                        <div class="card-title"><span>🚀</span> Inicialização e Scripts Utilitários</div>
                        <p class="card-text">
                            O projeto inclui scripts bash completos prontos para uso:
                        </p>
                        <ul class="card-list" style="margin-top: 0.5rem;">
                            <li><code>./instalar_dependencias.sh</code>: Instala dependências (<code>pygame-ce</code>, <code>numpy</code>).</li>
                            <li><code>./executar.sh</code> ou <code>python3 main.py</code>: Inicia o jogo diretamente.</li>
                            <li><code>./generate_pdf.sh</code>: Recompila a documentação formal em PDF.</li>
                        </ul>
                    </div>
                    <div class="card card-purple">
                        <div class="card-title"><span>👥</span> Como Testar o Multiplayer em 1 Computador</div>
                        <ol class="card-list" style="margin-top: 0.5rem;">
                            <li><strong>Instância 1 (Host):</strong> Iniciar jogo -> <em>Multiplayer LAN</em> -> <em>Hospedar Sala</em>.</li>
                            <li><strong>Instância 2 (Client):</strong> Em outro terminal, executar <code>python3 main.py</code> -> <em>Multiplayer LAN</em> -> <em>Entrar na Sala</em> (informar IP <code>127.0.0.1</code> e porta <code>5555</code>).</li>
                            <li>Ambos os jogadores (Scrappy e Byte) entram na mesma fase com sincronização de tiros e respawn contínuo!</li>
                        </ol>
                    </div>
                </div>
                <div class="col-half">
                    <div class="card card-amber" style="height: 100%;">
                        <div class="card-title"><span>🎮</span> Mapeamento de Controles no Teclado</div>
                        <table class="slide-table" style="margin-top: 0.5rem;">
                            <thead>
                                <tr>
                                    <th>Ação</th>
                                    <th>Jogador 1 (Scrappy)</th>
                                    <th>Jogador 2 (Byte)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Movimento</strong></td>
                                    <td><code>A</code> / <code>D</code></td>
                                    <td><code>Seta Esquerda</code> / <code>Direita</code></td>
                                </tr>
                                <tr>
                                    <td><strong>Pulo</strong></td>
                                    <td><code>W</code> ou <code>Espaço</code></td>
                                    <td><code>Seta Cima</code></td>
                                </tr>
                                <tr>
                                    <td><strong>Dash</strong></td>
                                    <td><code>K</code> ou <code>Shift Esq</code></td>
                                    <td><code>Shift Dir</code> / <code>Ctrl</code></td>
                                </tr>
                                <tr>
                                    <td><strong>Tiro</strong></td>
                                    <td><code>J</code> ou <code>F</code></td>
                                    <td><code>Enter</code> ou <code>Keypad 0</code></td>
                                </tr>
                                <tr>
                                    <td><strong>Editor de Fases</strong></td>
                                    <td colspan="2">Botão Esquerdo (Desenhar), Botão Direito (Apagar), Tecla <code>T</code> (Playtest), <code>ESC</code> (Voltar)</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

        <!-- ==========================================
             SLIDE 14: CONCLUSÃO E RESULTADOS
             ========================================== -->
        <section class="slide slide-cover" id="slide-14">
            <div class="cover-badge" style="background: rgba(16, 185, 129, 0.1); color: var(--accent-green); border-color: rgba(16, 185, 129, 0.3);">
                <span>🏆</span> Conclusão dos Trabalhos Acadêmicos
            </div>
            <h2 class="cover-title" style="font-size: 3.2rem;">RESULTADOS ALCANÇADOS</h2>
            <p class="cover-subtitle" style="font-size: 1.25rem; margin-bottom: 2rem;">
                Entrega integral dos requisitos dos Trabalhos 1 e 2 da disciplina de Tópicos Avançados em Computação (TAC - Prof. Vanderson)
            </p>

            <div class="cover-meta-grid" style="grid-template-columns: repeat(3, 1fr); max-width: 900px; margin-bottom: 2rem;">
                <div class="cover-meta-card">
                    <div class="cover-meta-label">Level Maker Didático</div>
                    <div class="cover-meta-val">Editor 70×15 c/ Playtest Instantâneo</div>
                </div>
                <div class="cover-meta-card">
                    <div class="cover-meta-label">Multiplayer LAN UDP</div>
                    <div class="cover-meta-val">Assíncrono, LERP e Respawn Contínuo</div>
                </div>
                <div class="cover-meta-card">
                    <div class="cover-meta-label">Engenharia e Padrões</div>
                    <div class="cover-meta-val">Singleton, Observer, State, Flyweight</div>
                </div>
            </div>

            <p style="font-size: 1.1rem; color: var(--text-muted); font-weight: 500;">
                Obrigado pela atenção! Espaço aberto para dúvidas e demonstração prática do código.
            </p>
        </section>

    </div>

    <!-- Dicas de Teclado -->
    <div class="keyboard-hint">
        <span>[← / → / Espaço] Navegar</span>
        <span>[F] Tela Cheia</span>
        <span>[O / G] Visão Geral</span>
        <span>[Home / End] Início / Fim</span>
    </div>

    <!-- Barra de Ferramentas / Controles -->
    <div id="toolbar">
        <button class="btn-ctrl" id="btn-prev" title="Slide Anterior (←)">◀</button>
        <span id="counter">01 / 14</span>
        <button class="btn-ctrl" id="btn-next" title="Próximo Slide (→)">▶</button>
        <button class="btn-ctrl" id="btn-grid" title="Visão Geral (O)">☵</button>
        <button class="btn-ctrl" id="btn-fs" title="Tela Cheia (F)">⛶</button>
    </div>

    <!-- Modal de Visão Geral (Grid) -->
    <div id="overview-modal">
        <div class="overview-header">
            <h2 class="overview-title">Índice da Apresentação</h2>
            <button class="btn-ctrl" id="btn-close-overview" style="font-size: 1.5rem;">✕</button>
        </div>
        <div class="overview-grid" id="overview-grid-container"></div>
    </div>

    <script>
        const slides = Array.from(document.querySelectorAll('.slide'));
        const totalSlides = slides.length;
        let currentSlide = 0;

        const progressBar = document.getElementById('progress-bar');
        const counter = document.getElementById('counter');
        const overviewModal = document.getElementById('overview-modal');
        const overviewGrid = document.getElementById('overview-grid-container');

        // Cria miniaturas na visão geral
        slides.forEach((slide, idx) => {{
            const titleEl = slide.querySelector('.slide-title') || slide.querySelector('.cover-title');
            const titleText = titleEl ? titleEl.innerText.replace(/^[0-9.]+\s*/, '') : `Slide ${{idx + 1}}`;
            
            const thumb = document.createElement('div');
            thumb.className = `overview-thumb ${{idx === 0 ? 'active' : ''}}`;
            thumb.innerHTML = `
                <span class="overview-thumb-num">SLIDE ${{String(idx + 1).padStart(2, '0')}}</span>
                <span class="overview-thumb-title">${{titleText}}</span>
            `;
            thumb.addEventListener('click', () => {{
                irParaSlide(idx);
                fecharOverview();
            }});
            overviewGrid.appendChild(thumb);
        }});

        function atualizarSlide() {{
            slides.forEach((slide, idx) => {{
                if (idx === currentSlide) {{
                    slide.classList.add('active');
                }} else {{
                    slide.classList.remove('active');
                }}
            }});

            const pct = ((currentSlide) / (totalSlides - 1)) * 100;
            progressBar.style.width = `${{pct}}%`;

            counter.innerText = `${{String(currentSlide + 1).padStart(2, '0')}} / ${{String(totalSlides).padStart(2, '0')}}`;

            // Atualiza destaque na grade
            const thumbs = document.querySelectorAll('.overview-thumb');
            thumbs.forEach((th, idx) => {{
                if (idx === currentSlide) th.classList.add('active');
                else th.classList.remove('active');
            }});
        }}

        function proximoSlide() {{
            if (currentSlide < totalSlides - 1) {{
                currentSlide++;
                atualizarSlide();
            }}
        }}

        function slideAnterior() {{
            if (currentSlide > 0) {{
                currentSlide--;
                atualizarSlide();
            }}
        }}

        function irParaSlide(index) {{
            if (index >= 0 && index < totalSlides) {{
                currentSlide = index;
                atualizarSlide();
            }}
        }}

        function alternarFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen().catch(() => {{}});
            }} else {{
                if (document.exitFullscreen) {{
                    document.exitFullscreen();
                }}
            }}
        }}

        function abrirOverview() {{
            overviewModal.classList.add('open');
        }}

        function fecharOverview() {{
            overviewModal.classList.remove('open');
        }}

        function alternarOverview() {{
            if (overviewModal.classList.contains('open')) {{
                fecharOverview();
            }} else {{
                abrirOverview();
            }}
        }}

        // Listeners de Botões
        document.getElementById('btn-next').addEventListener('click', proximoSlide);
        document.getElementById('btn-prev').addEventListener('click', slideAnterior);
        document.getElementById('btn-fs').addEventListener('click', alternarFullscreen);
        document.getElementById('btn-grid').addEventListener('click', alternarOverview);
        document.getElementById('btn-close-overview').addEventListener('click', fecharOverview);

        // Atalhos de Teclado
        window.addEventListener('keydown', (e) => {{
            if (overviewModal.classList.contains('open')) {{
                if (e.key === 'Escape' || e.key === 'o' || e.key === 'O' || e.key === 'g' || e.key === 'G') {{
                    fecharOverview();
                }}
                return;
            }}

            switch(e.key) {{
                case 'ArrowRight':
                case 'Space':
                case 'PageDown':
                case 'Enter':
                case 'n':
                case 'N':
                    e.preventDefault();
                    proximoSlide();
                    break;
                case 'ArrowLeft':
                case 'PageUp':
                case 'Backspace':
                case 'p':
                case 'P':
                    e.preventDefault();
                    slideAnterior();
                    break;
                case 'Home':
                    e.preventDefault();
                    irParaSlide(0);
                    break;
                case 'End':
                    e.preventDefault();
                    irParaSlide(totalSlides - 1);
                    break;
                case 'f':
                case 'F':
                    e.preventDefault();
                    alternarFullscreen();
                    break;
                case 'o':
                case 'O':
                case 'g':
                case 'G':
                    e.preventDefault();
                    alternarOverview();
                    break;
                case 'Escape':
                    fecharOverview();
                    break;
            }}
        }});

        // Inicia no primeiro slide
        atualizarSlide();
    </script>
</body>
</html>
"""

def main():
    html_output = os.path.join(DIR, "Apresentacao_Rust_And_Byte.html")
    pdf_output = os.path.join(DIR, "Apresentacao_Rust_And_Byte.pdf")
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    print("==========================================================")
    print("  Gerador de Apresentação de Slides (TAC - Prof. Vanderson) ")
    print("==========================================================")

    # 1. Grava o arquivo HTML da apresentação
    with open(html_output, "w", encoding="utf-8") as f:
        f.write(HTML_SLIDES)
    print(f"[✓] Apresentação HTML gerada com sucesso:")
    print(f"    Caminho: {html_output}")

    # 2. Gera a versão PDF se o Chrome estiver disponível
    if os.path.exists(chrome_path):
        print("\n[+] Renderizando versão PDF (Widescreen 16:9)...")
        cmd = [
            chrome_path,
            "--headless=new",
            "--disable-gpu",
            "--virtual-time-budget=8000",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_output}",
            f"file://{html_output}"
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(pdf_output):
                size_mb = os.path.getsize(pdf_output) / (1024 * 1024)
                print(f"[✓] Arquivo PDF dos Slides gerado com sucesso!")
                print(f"    Caminho: {pdf_output}")
                print(f"    Tamanho: {size_mb:.2f} MB")
            else:
                print("[!] Falha ao gravar PDF.")
        except Exception as e:
            print(f"[!] Erro ao invocar Chrome: {e}")
    else:
        print("[i] Chrome não encontrado no caminho padrão. Você pode abrir o HTML e exportar para PDF via Ctrl+P.")

if __name__ == "__main__":
    main()
