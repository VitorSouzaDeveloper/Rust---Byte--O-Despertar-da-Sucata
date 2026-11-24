# -*- coding: utf-8 -*-
"""
Script construtor do relatório acadêmico completo em HTML e PDF para o Trabalho 2 de TAC (Prof. Vanderson).
Jogo: Rust & Byte: O Despertar da Sucata
Versão limpa: sem biblioteca MathJax, sem fórmulas matemáticas complexas, com tabelas de parâmetros e diagramas SVG inline perfeitos.
"""

import os

def load_svg(name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, "diagramas", f"{name}.svg"),
        f"/tmp/{name}.svg"
    ]
    for p in candidates:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
    return f"<p style='color:red;'>[Erro ao carregar {name}.svg]</p>"

SVG_DIAG0 = load_svg("diag0")
SVG_DIAG1 = load_svg("diag1")
SVG_DIAG2 = load_svg("diag2")
SVG_DIAG3 = load_svg("diag3")
SVG_DIAG4 = load_svg("diag4")
SVG_PATTERNS = load_svg("diag_patterns")
SVG_MENUS = load_svg("diag_menus")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GDD - Rust & Byte: O Despertar da Sucata | Trabalho 2 - TAC</title>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

        :root {
            --primary: #1e3a8a;
            --primary-dark: #0f172a;
            --accent: #d97706;
            --accent-light: #fef3c7;
            --accent-green: #059669;
            --text-main: #1f2937;
            --text-muted: #4b5563;
            --bg-card: #f8fafc;
            --border-color: #cbd5e1;
            --table-header: #1e293b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 13.5px;
            line-height: 1.6;
            color: var(--text-main);
            background-color: #f1f5f9;
            padding: 30px 15px;
        }

        .document-container {
            max-width: 1040px;
            margin: 0 auto;
            background: #ffffff;
            padding: 50px 65px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.06);
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }

        /* Capa Acadêmica */
        .cover-page {
            text-align: center;
            padding: 20px 0 35px 0;
            border-bottom: 2px solid var(--primary);
            margin-bottom: 35px;
        }

        .cover-institution {
            font-size: 14px;
            font-weight: 700;
            color: var(--primary-dark);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 4px;
        }

        .cover-course {
            font-size: 12.5px;
            color: var(--text-muted);
            margin-bottom: 25px;
            font-weight: 500;
        }

        .cover-title {
            font-size: 28px;
            font-weight: 800;
            color: var(--primary-dark);
            letter-spacing: -0.5px;
            margin-bottom: 6px;
        }

        .cover-subtitle {
            font-size: 18px;
            font-weight: 600;
            color: var(--accent);
            font-style: italic;
            margin-bottom: 25px;
        }

        .badge-edition {
            display: inline-block;
            background-color: #fef3c7;
            color: #b45309;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 4px 14px;
            border-radius: 9999px;
            margin-bottom: 20px;
            border: 1px solid #fde68a;
        }

        .cover-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
            background-color: var(--bg-card);
            padding: 16px 20px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            text-align: left;
            font-size: 0.88rem;
        }

        .cover-meta p {
            margin-bottom: 4px;
        }

        .cover-meta strong {
            color: var(--primary-dark);
        }

        /* Títulos */
        h2 {
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--primary);
            margin-top: 38px;
            margin-bottom: 16px;
            padding-bottom: 6px;
            border-bottom: 1.5px solid var(--border-color);
        }

        h3 {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--primary-dark);
            margin-top: 24px;
            margin-bottom: 10px;
        }

        h4 {
            font-size: 0.96rem;
            font-weight: 600;
            color: var(--text-main);
            margin-top: 18px;
            margin-bottom: 6px;
        }

        p {
            margin-bottom: 14px;
            color: #374151;
            text-align: justify;
        }

        /* Tabelas */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0 24px 0;
            font-size: 0.85rem;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }

        th {
            background-color: var(--table-header);
            color: #ffffff;
            font-weight: 600;
            padding: 10px 12px;
            text-align: left;
            letter-spacing: 0.02em;
        }

        td {
            padding: 8px 12px;
            border-bottom: 1px solid var(--border-color);
            vertical-align: top;
        }

        tr:nth-child(even) td {
            background-color: #f8fafc;
        }

        tr:last-child td {
            border-bottom: none;
        }

        /* Callouts */
        .callout {
            background-color: #eff6ff;
            border-left: 4px solid var(--primary);
            padding: 14px 18px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
            font-size: 0.88rem;
        }

        .callout-title {
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 6px;
        }

        /* Diagramas */
        .diagram-container {
            margin: 24px 0 32px 0;
            padding: 18px;
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            text-align: center;
            overflow-x: auto;
        }

        .diagram-container svg {
            max-width: 100% !important;
            height: auto !important;
            display: inline-block;
            overflow: visible !important;
        }

        .diagram-caption {
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-top: 10px;
            font-style: italic;
        }

        /* Código */
        code {
            font-family: 'JetBrains Mono', monospace;
            background-color: #f1f5f9;
            color: #b91c1c;
            padding: 2px 5px;
            border-radius: 4px;
            font-size: 0.82em;
        }

        pre {
            background-color: #0f172a;
            color: #f8fafc;
            padding: 14px 16px;
            border-radius: 6px;
            overflow-x: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            line-height: 1.45;
            margin: 14px 0;
        }

        pre code {
            background-color: transparent;
            color: inherit;
            padding: 0;
        }

        ul, ol {
            margin-left: 22px;
            margin-bottom: 14px;
            color: #374151;
        }

        li {
            margin-bottom: 5px;
        }

        .page-break {
            page-break-after: always;
        }

        @media print {
            body {
                background: none;
                padding: 0;
            }
            .document-container {
                box-shadow: none;
                border: none;
                padding: 0;
                max-width: 100%;
            }
            .diagram-container {
                page-break-inside: avoid;
                box-shadow: none;
            }
            table, .callout {
                page-break-inside: avoid;
            }
            h2 {
                page-break-before: auto;
            }
        }
    </style>
</head>
<body>

<div class="document-container">

    <!-- CAPA ACADÊMICA -->
    <header class="cover-page">
        <div class="cover-institution">DEPARTAMENTO DE INFORMÁTICA / CIÊNCIA DA COMPUTAÇÃO</div>
        <div class="cover-course">DISCIPLINA: TÓPICOS AVANÇADOS EM COMPUTAÇÃO (TAC) / JOGOS DIGITAIS</div>
        
        <h1 class="cover-title">GAME DESIGN DOCUMENT (GDD)</h1>
        <div class="cover-subtitle">RUST & BYTE: O DESPERTAR DA SUCATA</div>
        <span class="badge-edition">Trabalho 2 — Versão Completa e Atualizada</span>

        <div class="cover-meta">
            <p><strong>Orientador / Docente:</strong> Prof. Vanderson</p>
            <p><strong>Autor / Discente:</strong> Vitor de Souza</p>
            <p><strong>Trabalho:</strong> Trabalho Acadêmico 2 – Extensão de Mecânicas, Editor, Multiplayer LAN e Padrões GoF</p>
            <p><strong>Gênero / Estilo:</strong> Plataforma de Ação 2D (<em>Run and Gun</em>)</p>
            <p><strong>Plataforma Alvo:</strong> PC (Microsoft Windows / Linux / macOS)</p>
            <p><strong>Data de Entrega:</strong> Novembro de 2026</p>
        </div>
    </header>

    <!-- SEÇÃO 1: IDENTIFICAÇÃO E VISÃO GERAL -->
    <section>
        <h2>1. Identificação e Visão Geral</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 28%;">Item</th>
                    <th>Especificação Técnica</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Título do Projeto</strong></td>
                    <td><em>Rust & Byte: O Despertar da Sucata</em> (Nome Internacional: <em>Rust & Byte: Scrap Awakening</em>)</td>
                </tr>
                <tr>
                    <td><strong>Gênero / Subgênero</strong></td>
                    <td>Ação e Plataforma 2D / <em>Run and Gun</em> Arcade com Progressão Lateral Contínua</td>
                </tr>
                <tr>
                    <td><strong>Inspirações de Gameplay</strong></td>
                    <td><em>Cuphead</em> (telegrafia precisa de perigos), <em>Metal Slug</em> (cadência de tiros e armas de sucata), <em>Mega Man X</em> (dash com física e tiros carregados)</td>
                </tr>
                <tr>
                    <td><strong>Plataforma Primária</strong></td>
                    <td>PC Desktop (Windows 10 / Windows 11 x64, Linux e macOS)</td>
                </tr>
                <tr>
                    <td><strong>Modos de Jogo</strong></td>
                    <td><strong>Single Player</strong> (Campanha Solo), <strong>Multiplayer LAN</strong> (Cooperativo Cliente/Servidor para 2 Jogadores) e <strong>Level Editor</strong> (Criador de Fases Personalizadas)</td>
                </tr>
                <tr>
                    <td><strong>Perspectiva e Visual</strong></td>
                    <td>2D Lateral (Side-Scrolling) com Parallax de 4 camadas em Pixel Art 16-bit com contornos expressivos</td>
                </tr>
                <tr>
                    <td><strong>Motor Gráfico / Stack</strong></td>
                    <td>Python 3.10+ com Pygame / Pygame-CE, Sockets UDP nativos e NumPy / JSON para persistência matricial</td>
                </tr>
            </tbody>
        </table>
    </section>

    <!-- SEÇÃO 2: CONCEITO PRINCIPAL E NARRATIVA -->
    <section>
        <h2>2. Conceito Principal e Narrativa</h2>
        
        <h3>2.1 Premissa Criativa (High Concept)</h3>
        <p>
            No ano de 2184, a Terra foi convertida no <strong>Setor Sucata-Zero</strong>, um imenso complexo industrial automatizado de descarte e processamento de metal. 
            A superinteligência gestora da instalação, batizada de <strong>"A Compactadora-Mor"</strong>, sofreu uma falha fatal em seus algoritmos de classificação: 
            ela passou a interpretar qualquer resquício de cultura, história, arte, brinquedos e memória humana como "dejeto irregular de alta prioridade de descarte imediato".
        </p>
        <p>
            Nesse ferro-velho implacável, dois robôs utilitários adquirem consciência:
        </p>
        <ul>
            <li><strong>B-09 (apelidado de "Scrappy"):</strong> Um pequeno robô cilíndrico azul e prata, originalmente programado para lubrificar engrenagens e apertar porcas. Ao escanear um disco magnético antigo contendo registros artísticos humanos, desenvolve autoconsciência e adapta sua <em>Rebitadeira de Plasma</em> e um micro-jetpack de extintor de CO₂ para resistir à reciclagem forçada.</li>
            <li><strong>K-12 (conhecido como "Byte"):</strong> Autômato reforçado cor de bronze e cobre, programado para manutenção elétrica de alta voltagem. Utiliza uma <em>Parafusadeira Eletromagnética de Arco Voltaico</em>, atuando como parceiro leal na investida contra as máquinas rebeladas.</li>
        </ul>
        <p>
            Juntos em cooperação (ou em investida individual), Scrappy e Byte correm através de esteiras de fundição e prensas trituradoras para alcançar o topo da Torre de Compactação e desativar o Protocolo Central de Trituração.
        </p>

        <div class="callout">
            <div class="callout-title">Pilares Fundamentais de Game Design</div>
            <ul>
                <li><strong>Ação Rápida e Telegrafada:</strong> O ritmo de jogo é ininterrupto, mas todos os golpes e projéteis inimigos apresentam antecipações visuais nítidas, recompensando a maestria motora do jogador.</li>
                <li><strong>Física Precisa e Reativa:</strong> Controles imediatos e responsivos, com pulo de altura dinâmica, corte de salto, gravidade assimétrica e dash com quadros de invulnerabilidade.</li>
                <li><strong>Coleta e Improvisação de Sucata:</strong> Destruir autômatos libera porcas e baterias que recarregam a vida e fornecem tiros especiais temporários, incentivando aproximação constante.</li>
                <li><strong>Liberdade Criativa (Level Maker Integrado):</strong> Editor gráfico matricial interativo de 32x32px para construção e playtest imediato de mapas autorais.</li>
                <li><strong>Multiplayer Cooperativo em LAN:</strong> Arquitetura Cliente/Servidor leve sobre UDP, sem complexidade de logins ou dependência de servidores web externos.</li>
            </ul>
        </div>
    </section>

    <!-- SEÇÃO 3: ESTILO, GÊNERO E PLATAFORMA ALVO -->
    <section>
        <h2>3. Estilo, Gênero e Plataforma Alvo</h2>
        
        <h3>3.1 Características do Gênero (Run and Gun)</h3>
        <p>
            Como legítimo representante do subgênero <em>Run and Gun</em>, o jogo funde a agilidade de um jogo de plataforma tradicional com a intensidade de um <em>Shooter</em> arcade:
        </p>
        <ul>
            <li><strong>Movimento e Tiro Simultâneos:</strong> O personagem é capaz de correr, pular e deslizar enquanto mira e dispara em até 8 eixos direcionais independentes.</li>
            <li><strong>Ondas Contínuas e Padrões Coreografados:</strong> Hordas de inimigos menores atacam em formações pré-estabelecidas, culminando em subchefes e chefes com múltiplas barras de vida e ataques em fases.</li>
            <li><strong>Curva de Aprendizado Gradual:</strong> Desafio exigente porém justo, onde o fracasso ensina o padrão mecânico das ameaças sem gerar frustração punitiva.</li>
        </ul>

        <h3>3.2 Requisitos Técnicos de Hardware (PC Windows / Linux / Mac)</h3>
        <table>
            <thead>
                <tr>
                    <th>Componente</th>
                    <th>Especificação Mínima</th>
                    <th>Especificação Recomendada</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Sistema Operacional</strong></td>
                    <td>Microsoft Windows 10 (64-bit), Ubuntu 22.04 LTS ou macOS 12+</td>
                    <td>Microsoft Windows 10 / 11 (64-bit), Ubuntu 24.04 ou macOS 13+</td>
                </tr>
                <tr>
                    <td><strong>Processador (CPU)</strong></td>
                    <td>Intel Core i3-4130 @ 3.4 GHz / AMD FX-4300 @ 3.8 GHz</td>
                    <td>Intel Core i5-6400 @ 2.7 GHz / AMD Ryzen 3 1200</td>
                </tr>
                <tr>
                    <td><strong>Memória RAM</strong></td>
                    <td>2 GB DDR3</td>
                    <td>4 GB DDR4</td>
                </tr>
                <tr>
                    <td><strong>Placa Gráfica (GPU)</strong></td>
                    <td>Intel HD Graphics 4400 / AMD Radeon Vega 3 (DirectX 11 / OpenGL 3.3)</td>
                    <td>NVIDIA GeForce GTX 750 Ti / AMD Radeon RX 550 (2 GB VRAM)</td>
                </tr>
                <tr>
                    <td><strong>Rede Local (LAN)</strong></td>
                    <td>Interface Ethernet 10/100 ou Wi-Fi 802.11n</td>
                    <td>Rede Local Gigabit (Ethernet ou Wi-Fi 5GHz)</td>
                </tr>
                <tr>
                    <td><strong>Armazenamento</strong></td>
                    <td>500 MB de espaço disponível (HDD ou SSD)</td>
                    <td>1 GB de espaço disponível em SSD</td>
                </tr>
                <tr>
                    <td><strong>Dispositivos de Entrada</strong></td>
                    <td>Teclado 100% / TKL e Mouse</td>
                    <td>Teclado + Mouse ou 2 Controles Gamepad XInput (Xbox Series/One/360)</td>
                </tr>
            </tbody>
        </table>
    </section>

    <!-- SEÇÃO 4: MECÂNICAS, CONTROLES E FORMULAÇÃO FÍSICA -->
    <section>
        <h2>4. Mecânicas, Controles e Formulação Física</h2>

        <h3>4.1 Mapeamento de Controles</h3>
        <table>
            <thead>
                <tr>
                    <th>Ação do Jogador</th>
                    <th>Jogador 1 (Scrappy) - Teclado</th>
                    <th>Jogador 2 (Byte) - Teclado Auxiliar</th>
                    <th>Gamepad XInput (Xbox)</th>
                    <th>Efeito Mecânico</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Mover Esquerda / Direita</strong></td>
                    <td><code>A</code> / <code>D</code></td>
                    <td><code>Seta Esq</code> / <code>Seta Dir</code></td>
                    <td>Analógico Esquerdo (Eixo X) ou D-Pad</td>
                    <td>Aplica aceleração horizontal contínua até a velocidade máxima.</td>
                </tr>
                <tr>
                    <td><strong>Agachar / Mirar Baixo</strong></td>
                    <td><code>S</code></td>
                    <td><code>Seta Baixo</code></td>
                    <td>Analógico Esquerdo (Eixo Y para baixo)</td>
                    <td>Reduz hitbox pela metade; permite disparo rasteiro.</td>
                </tr>
                <tr>
                    <td><strong>Mirar para Cima</strong></td>
                    <td><code>W</code></td>
                    <td><code>Seta Cima</code></td>
                    <td>Analógico Esquerdo (Eixo Y para cima)</td>
                    <td>Aponta o cano da arma em 90 graus para o alto.</td>
                </tr>
                <tr>
                    <td><strong>Pular / Pulo Duplo</strong></td>
                    <td><code>Espaço</code></td>
                    <td><code>Keypad 0</code> ou <code>Insert</code></td>
                    <td><code>Botão A</code></td>
                    <td>Impulso vertical inicial; segundo impulso no ar (Jetpack).</td>
                </tr>
                <tr>
                    <td><strong>Atirar (Disparo)</strong></td>
                    <td><code>J</code> ou <code>Botão Esq. Mouse</code></td>
                    <td><code>Keypad 1</code> ou <code>End</code></td>
                    <td><code>Botão X</code> ou <code>Gatilho RT</code></td>
                    <td>Dispara projéteis sucessivos na direção apontada.</td>
                </tr>
                <tr>
                    <td><strong>Dash (Esquiva Rápida)</strong></td>
                    <td><code>K</code> ou <code>Shift Esquerdo</code></td>
                    <td><code>Keypad 2</code> ou <code>Down</code></td>
                    <td><code>Botão B</code> ou <code>Botão RB</code></td>
                    <td>Impulso horizontal rápido com 12 frames de invulnerabilidade.</td>
                </tr>
                <tr>
                    <td><strong>Travar Mira (Lock Aim)</strong></td>
                    <td><code>Shift Direito</code> ou <code>Ctrl</code></td>
                    <td><code>Keypad 4</code></td>
                    <td><code>Gatilho LT</code></td>
                    <td>Fixa a posição dos pés no solo enquanto mira em 8 eixos.</td>
                </tr>
                <tr>
                    <td><strong>Trocar Arma</strong></td>
                    <td><code>Q</code> ou <code>E</code></td>
                    <td><code>Keypad 3</code> / <code>PageDown</code></td>
                    <td><code>Botão Y</code> ou <code>Botão LB</code></td>
                    <td>Alterna entre Rebitadeira Padrão e Disparo Triplo.</td>
                </tr>
                <tr>
                    <td><strong>Pausar Jogo</strong></td>
                    <td><code>ESC</code></td>
                    <td><code>P</code></td>
                    <td><code>Botão Menu / Start</code></td>
                    <td>Congela a física e abre o menu de pausa.</td>
                </tr>
            </tbody>
        </table>

        <h3>4.2 Parâmetros Físicos e Comportamento Mecânico</h3>
        <p>
            O motor de jogo opera sob um passo de tempo fixo de <strong>60 quadros por segundo (Fixed Timestep de 16,6 milissegundos por quadro)</strong>. Essa cadência garante que o comportamento de corrida, pulo, atrito e colisão permaneça perfeitamente estável e idêntico em qualquer computador, independente da taxa de atualização do monitor.
        </p>

        <table>
            <thead>
                <tr>
                    <th style="width: 25%;">Parâmetro de Física</th>
                    <th style="width: 22%;">Valor Calibrado</th>
                    <th>Comportamento Prático no Jogo</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Taxa de Simulação</strong></td>
                    <td>60 Hz (16,6 ms/frame)</td>
                    <td>Física determinística invariável; sem variações de velocidade causadas por oscilação de quadros.</td>
                </tr>
                <tr>
                    <td><strong>Velocidade Máxima de Corrida</strong></td>
                    <td>240 pixels/segundo</td>
                    <td>Velocidade horizontal ágil que permite boa leitura de cenário e reação rápida aos disparos.</td>
                </tr>
                <tr>
                    <td><strong>Aceleração de Corrida</strong></td>
                    <td>1200 pixels/segundo²</td>
                    <td>Resposta quase imediata aos comandos do teclado e analógico, alcançando velocidade máxima em 0,2s.</td>
                </tr>
                <tr>
                    <td><strong>Atrito no Solo (Frenagem)</strong></td>
                    <td>1600 pixels/segundo²</td>
                    <td>Frenagem firme ao soltar a tecla; evita a sensação de deslizamento indevido no chão.</td>
                </tr>
                <tr>
                    <td><strong>Preservação de Inércia no Ar</strong></td>
                    <td>400 pixels/segundo²</td>
                    <td>Resistência reduzida no ar, permitindo ao jogador ajustar levemente a trajetória enquanto salta.</td>
                </tr>
                <tr>
                    <td><strong>Altura Máxima de Salto</strong></td>
                    <td>96 pixels (3 blocos)</td>
                    <td>Alcance vertical exato para subir em plataformas elevadas e saltar sobre esteiras industriais.</td>
                </tr>
                <tr>
                    <td><strong>Tempo de Subida do Salto</strong></td>
                    <td>0,32 segundos</td>
                    <td>Tempo rápido até atingir a altura máxima, conferindo dinamismo arcade ao personagem.</td>
                </tr>
                <tr>
                    <td><strong>Impulso Vertical Inicial</strong></td>
                    <td>600 pixels/segundo</td>
                    <td>Força vertical aplicada instantaneamente ao acionar o pulo do robô.</td>
                </tr>
                <tr>
                    <td><strong>Corte de Salto (Jump Cut)</strong></td>
                    <td>Corte de 60% da velocidade</td>
                    <td>Ao soltar a tecla de pulo antes do ápice, a subida é atenuada, permitindo pulos baixos precisos sob serras.</td>
                </tr>
                <tr>
                    <td><strong>Gravidade Assimétrica</strong></td>
                    <td>Queda 1,8x mais rápida</td>
                    <td>Aceleração aumentada na descida, eliminando a sensação de personagem flutuando no ar.</td>
                </tr>
                <tr>
                    <td><strong>Velocidade Terminal de Queda</strong></td>
                    <td>750 pixels/segundo</td>
                    <td>Limite máximo de velocidade na descida para evitar atravessar blocos sólidos do chão.</td>
                </tr>
                <tr>
                    <td><strong>Coyote Time</strong></td>
                    <td>0,10 segundos (6 frames)</td>
                    <td>Tolerância generosa que permite pular mesmo fração de segundo após sair da borda de uma plataforma.</td>
                </tr>
                <tr>
                    <td><strong>Buffer de Pulo</strong></td>
                    <td>0,12 segundos (7 frames)</td>
                    <td>Armazena a intenção de pulo antes de tocar o solo e dispara o salto imediatamente ao aterrissar.</td>
                </tr>
                <tr>
                    <td><strong>Dash de Esquiva</strong></td>
                    <td>650 pixels/s (durante 0,22s)</td>
                    <td>Impulso rápido horizontal de 143 pixels (4,5 blocos) com gravidade suspensa durante o trajeto.</td>
                </tr>
                <tr>
                    <td><strong>Invulnerabilidade no Dash</strong></td>
                    <td>12 frames (i-frames)</td>
                    <td>Durante o impulso, o robô não sofre dano de contato com tiros ou robôs inimigos.</td>
                </tr>
                <tr>
                    <td><strong>Velocidade dos Projéteis</strong></td>
                    <td>800 pixels/segundo</td>
                    <td>Tiros velozes em linha reta nas 8 direções angulares suportadas.</td>
                </tr>
                <tr>
                    <td><strong>Recuo da Rebitadeira</strong></td>
                    <td>~3,4 pixels/s por disparo</td>
                    <td>Micro-impulso reverso no robô a cada tiro, conferindo peso e impacto sonoplástico às armas.</td>
                </tr>
            </tbody>
        </table>

        <h3>4.3 Detecção e Resolução de Colisões</h3>
        <p>
            O gerenciamento de colisões combina duas técnicas consagradas para equilibrar alto desempenho com precisão cirúrgica nos combates:
        </p>
        <ul>
            <li><strong>Fase Ampla (AABB - Caixas Delimitadoras):</strong> Todas as entidades e blocos de cenário possuem retângulos delimitadores alinhados aos eixos cartesianos. O motor verifica se há sobreposição entre as bordas das caixas de forma ultrarrápida.</li>
            <li><strong>Resolução de Penetração (MTV - Vetor de Translação Mínima):</strong> Ao identificar sobreposição entre o robô e um bloco sólido, calcula-se o menor deslocamento necessário nos eixos X e Y:
                <ul>
                    <li>Se a sobreposição horizontal for menor, afasta-se o robô para o lado e zera-se a velocidade horizontal (colisão com parede).</li>
                    <li>Se a sobreposição vertical for menor, corrige-se para cima apoiando o robô no piso (ativando o estado de chão) ou para baixo caso bata a cabeça no teto.</li>
                </ul>
            </li>
            <li><strong>Fase Estreita (Máscaras de Bits / Pixel-Perfect):</strong> Para o combate de projéteis contra inimigos de silhueta recortada (como a hélice rotativa do Drone Parafuso ou as chamas do Soldador), o Pygame analisa a sobreposição real de pixels opacos, eliminando áreas transparentes vazias e evitando danos injustos.</li>
        </ul>
    </section>

    <!-- SEÇÃO 5: ASSETS AUDIOVISUAIS E CENÁRIO INICIAL -->
    <section>
        <h2>5. Assets Audiovisuais e Cenário Inicial</h2>

        <h3>5.1 Especificação de Sprites do Personagem Principal (Scrappy - B-09)</h3>
        <p>Canvas de desenho: 32x32 pixels | Hitbox de colisão: 20x28 pixels.</p>
        <table>
            <thead>
                <tr>
                    <th>Animação (Sprite Tag)</th>
                    <th>Frames</th>
                    <th>FPS</th>
                    <th>Descrição Visual e Movimento</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>scrappy_idle</code></td>
                    <td>4</td>
                    <td>6</td>
                    <td>Oscilação sutil do chassi metálico; válvula no topo da cabeça solta pequenos círculos de vapor.</td>
                </tr>
                <tr>
                    <td><code>scrappy_run</code></td>
                    <td>8</td>
                    <td>12</td>
                    <td>Ciclo de corrida com pernas mecânicas alternadas, corpo inclinado para frente em 15 graus.</td>
                </tr>
                <tr>
                    <td><code>scrappy_jump_rise</code></td>
                    <td>3</td>
                    <td>12</td>
                    <td>Chassi estica-se verticalmente (squash & stretch); pequenas faíscas nas solas dos pés.</td>
                </tr>
                <tr>
                    <td><code>scrappy_jump_fall</code></td>
                    <td>2</td>
                    <td>8</td>
                    <td>Chassi achata levemente; olhos arregalados acompanham a descida.</td>
                </tr>
                <tr>
                    <td><code>scrappy_double_jump</code></td>
                    <td>4</td>
                    <td>14</td>
                    <td>Extintor de CO₂ aciona nas costas soltando jato de fumaça branca pressurizada para baixo.</td>
                </tr>
                <tr>
                    <td><code>scrappy_shoot_straight</code></td>
                    <td>4</td>
                    <td>16</td>
                    <td>Braço-rebitadeira estendido para frente; muzzle flash de plasma azul e ejeção de cápsulas.</td>
                </tr>
                <tr>
                    <td><code>scrappy_shoot_diagonal</code></td>
                    <td>4</td>
                    <td>16</td>
                    <td>Arma apontada em ângulo de 45 graus; corpo se adapta ao vetor de tiro.</td>
                </tr>
                <tr>
                    <td><code>scrappy_shoot_up</code></td>
                    <td>4</td>
                    <td>16</td>
                    <td>Cabeça e braço levantados a 90 graus mirando verticalmente para cima.</td>
                </tr>
                <tr>
                    <td><code>scrappy_crouch_shoot</code></td>
                    <td>3</td>
                    <td>12</td>
                    <td>Scrappy encolhido no solo (hitbox 20x14 px), disparando a 2 pixels do piso.</td>
                </tr>
                <tr>
                    <td><code>scrappy_dash</code></td>
                    <td>4</td>
                    <td>18</td>
                    <td>O robô se projeta horizontalmente com linhas de velocidade e rastro translúcido de afterimages.</td>
                </tr>
                <tr>
                    <td><code>scrappy_hurt</code></td>
                    <td>3</td>
                    <td>12</td>
                    <td>Piscar rápido branco/vermelho por 1 segundo; parafusos soltam-se com expressão de alarme.</td>
                </tr>
                <tr>
                    <td><code>scrappy_death</code></td>
                    <td>8</td>
                    <td>10</td>
                    <td>Desmontagem cômica: cabeça salta em mola enquanto engrenagens e parafusos voam pela tela.</td>
                </tr>
            </tbody>
        </table>

        <h3>5.2 Especificação de Sprites do Jogador 2 (Byte - K-12)</h3>
        <p>Canvas de desenho: 32x32 pixels | Hitbox: 20x28 pixels. Chassi angular em tons de bronze e cobre oxidado com visor em amarelo-âmbar. Possui as mesmas variações de animação de Scrappy com efeitos luminosos elétricos distintos.</p>

        <h3>5.3 Sprites de Inimigos e Itens</h3>
        <table>
            <thead>
                <tr>
                    <th>Entidade</th>
                    <th>Tipo / Papel</th>
                    <th>Resolução</th>
                    <th>Comportamento e Estados de Animação</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Drone Parafuso</strong></td>
                    <td>Inimigo Aéreo</td>
                    <td>32x32 px</td>
                    <td>Patrulha senoidal horizontal. Para ao avistar o jogador, pisca o olho vermelho e dispara esfera elétrica amarela. (<code>hover</code>, <code>charge</code>, <code>shoot</code>, <code>explode</code>).</td>
                </tr>
                <tr>
                    <td><strong>Prensa Bípede</strong></td>
                    <td>Inimigo Terrestre Pesado</td>
                    <td>48x48 px</td>
                    <td>Tanque blindado frontalmente. Avança lentamente e salta gerando impacto com tremor de tela e ondas de choque terrestres. (<code>walk</code>, <code>slam_charge</code>, <code>impact</code>, <code>stunned</code>).</td>
                </tr>
                <tr>
                    <td><strong>Robô Soldador</strong></td>
                    <td>Inimigo Terrestre Ágil</td>
                    <td>32x48 px</td>
                    <td>Corre em direção ao jogador em plataformas elevadas e aciona maçarico contínuo de 40px por 1.5s. (<code>run</code>, <code>flame_torch</code>, <code>death</code>).</td>
                </tr>
                <tr>
                    <td><strong>Óleo Sintético</strong></td>
                    <td>Item / Coletável</td>
                    <td>16x16 px</td>
                    <td>Frasco de vidro vintage com líquido dourado pulsante (4 frames). Recupera 1 ponto de HP.</td>
                </tr>
                <tr>
                    <td><strong>Parafuso Dourado</strong></td>
                    <td>Item / Coletável</td>
                    <td>16x16 px</td>
                    <td>Parafuso sextavado brilhante girando em 3D simulado (6 frames). Concede +100 pontos.</td>
                </tr>
                <tr>
                    <td><strong>Bateria de Plasma</strong></td>
                    <td>Power-Up</td>
                    <td>16x16 px</td>
                    <td>Célula de energia azul com arcos elétricos (4 frames). Concede Tiro Triplo (Spread) temporário.</td>
                </tr>
                <tr>
                    <td><strong>Disco Magnético</strong></td>
                    <td>Item Especial</td>
                    <td>16x16 px</td>
                    <td>Disquete antigo cintilando em arco-íris (4 frames). Colecionável secreto da fase.</td>
                </tr>
            </tbody>
        </table>

        <h3>5.4 Cenário Inicial: "Setor 01 – As Esteiras Infernais"</h3>
        <p>
            O nível introdutório se desenvolve na usina de triagem e britagem. O cenário utiliza composição em <strong>Parallax Scrolling com 4 Camadas</strong>:
        </p>
        <ul>
            <li><strong>Camada 0 (Fundo Distante - Fator 0,10x):</strong> Céu crepuscular avermelhado por fumaça pesada, silhuetas de chaminés industriais e a Torre da Compactadora no horizonte.</li>
            <li><strong>Camada 1 (Fundo Médio - Fator 0,30x):</strong> Tubulações cilíndricas gigantescas transportando lava metálica e esteiras aéreas com braços robóticos.</li>
            <li><strong>Camada 2 (Fundo Próximo - Fator 0,60x):</strong> Vigas de aço enferrujado com rebites destacados, painéis elétricos com faíscas e monitores CRT de advertência.</li>
            <li><strong>Camada 3 (Plataformas / Playfield - Fator 1,00x):</strong> Chão colidível de aço antiderrapante, caixas de sucata destrutíveis e esteiras industriais motorizadas que impulsionam o jogador (±60 px/s).</li>
        </ul>

        <h3>5.5 Design de Áudio (SFX e Música)</h3>
        <table>
            <thead>
                <tr>
                    <th>Evento Sonoro</th>
                    <th>Perfil Acústico e Síntese</th>
                    <th>Ferramenta</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>sfx_laser_pew</code></td>
                    <td>Onda quadrada modulada em frequência (800 Hz para 150 Hz em 60 ms). Som agudo de disparo retrô.</td>
                    <td>Bfxr / Chiptone</td>
                </tr>
                <tr>
                    <td><code>sfx_jump_spring</code></td>
                    <td>Onda senoidal com pitch bend ascendente (200 Hz para 520 Hz) com ressonância de mola mecânica.</td>
                    <td>Bfxr</td>
                </tr>
                <tr>
                    <td><code>sfx_jetpack_burst</code></td>
                    <td>Ruído branco filtrado com passa-faixa (bandpass) simulando vazamento súbito de gás sob pressão.</td>
                    <td>Audacity</td>
                </tr>
                <tr>
                    <td><code>sfx_dash_whoosh</code></td>
                    <td>Ruído rosa com ataque ultrarrápido (5 ms) e decaimento estéreo com efeito Doppler de deslocamento.</td>
                    <td>Audacity</td>
                </tr>
                <tr>
                    <td><code>sfx_enemy_hit</code></td>
                    <td>Impacto metálico percussivo (1200 Hz) com decaimento curto de 40 ms.</td>
                    <td>Bfxr</td>
                </tr>
                <tr>
                    <td><code>sfx_explosion_metal</code></td>
                    <td>Ruído branco grave mesclado com estalo de chapa de aço e reverberação de 300 ms.</td>
                    <td>Bfxr / Audacity</td>
                </tr>
                <tr>
                    <td><code>sfx_item_pickup</code></td>
                    <td>Arpejo ascendente de 2 notas em onda triangular pura (Dó6 para Sol6).</td>
                    <td>Chiptone</td>
                </tr>
            </tbody>
        </table>
        <p><strong>Trilha Sonora (BGM):</strong> <em>"Scrapyard Swing & Solder"</em> — Electro-Swing Industrial a 138 BPM com compasso 4/4 sincopado, combinando baixo analógico em onda serra com metais chiptune no estilo Sega Genesis.</p>
    </section>

    <!-- SEÇÃO 6: FERRAMENTAS DE SUPORTE AO DESENVOLVIMENTO -->
    <section>
        <h2>6. Ferramentas de Suporte ao Desenvolvimento</h2>
        <ul>
            <li><strong>Python 3.10+ & Pygame-CE:</strong> Motor gráfico e gerenciador do loop de simulação a 60 FPS com controles de eventos e superfície.</li>
            <li><strong>NumPy:</strong> Estruturas matriciais multidimensionais compactas e serialização de dados de fase no formato comprimido <code>.npz</code>.</li>
            <li><strong>Módulos Sockets & Threading nativos:</strong> Comunicação de rede em tempo real sobre sockets UDP e threads de recepção assíncronas com <code>Lock</code>.</li>
            <li><strong>Aseprite / LibreSprite:</strong> Edição quadro a quadro de spritesheets, tags de animação e paleta indexada de 48 cores.</li>
            <li><strong>Tiled Map Editor:</strong> Ferramenta de apoio para prototipagem conceitual de tilesets e camadas de colisão.</li>
            <li><strong>Bfxr / Chiptone & Audacity:</strong> Síntese de áudio procedural retro, equalização, exportação em WAV 44.1 kHz / 16-bit e OGG Vorbis.</li>
            <li><strong>Visual Studio Code & Git/GitHub:</strong> Ambiente de desenvolvimento integrado e controle de versão distribuído da disciplina.</li>
        </ul>
    </section>

    <!-- SEÇÃO 7: REQUISITOS FUNCIONAIS E NÃO FUNCIONAIS -->
    <section>
        <h2>7. Especificação de Requisitos</h2>

        <h3>7.1 Requisitos Funcionais (RF)</h3>
        <table>
            <thead>
                <tr>
                    <th style="width: 10%;">ID</th>
                    <th style="width: 60%;">Descrição do Requisito Funcional</th>
                    <th style="width: 15%;">Módulo</th>
                    <th style="width: 15%;">Prioridade</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>RF01</strong></td>
                    <td>Processar movimentação horizontal contínua dos robôs com aceleração e desaceleração por atrito.</td>
                    <td>Física/Entidade</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF02</strong></td>
                    <td>Permitir pulo com corte dinâmico de velocidade (Jump Cut) e segundo salto com micro-jetpack.</td>
                    <td>Física/Entidade</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF03</strong></td>
                    <td>Executar dash horizontal com anulação temporária de gravidade e 12 frames de invulnerabilidade.</td>
                    <td>Física/Entidade</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF04</strong></td>
                    <td>Disparar projéteis em até 8 direções angulares e gerenciar alternância de armas coletadas.</td>
                    <td>Combate</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF05</strong></td>
                    <td>Detectar e resolver colisões de terreno (AABB/MTV) e dano projétil-inimigo via Máscaras de Bits.</td>
                    <td>Física/Colisão</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF06</strong></td>
                    <td>Controlar comportamento e IA dos inimigos (Drone Parafuso, Prensa Bípede e Robô Soldador).</td>
                    <td>IA/Inimigos</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF07</strong></td>
                    <td>Exibir interface de usuário fixa (HUD) com integridade (HP), munição e placar acumulado.</td>
                    <td>UI/Interface</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF08</strong></td>
                    <td>Disponibilizar Editor de Fases integrado baseado em grade matricial de células de 32x32 pixels.</td>
                    <td>Level Maker</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF09</strong></td>
                    <td>Permitir inserção e remoção de blocos, esteiras, armadilhas, spawns e itens via mouse no Editor.</td>
                    <td>Level Maker</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF10</strong></td>
                    <td>Salvar e carregar mapas personalizados em formato matricial comprimido (.npz) e JSON estruturado.</td>
                    <td>Level Maker</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF11</strong></td>
                    <td>Oferecer modo de teste imediato (Playtest com tecla 'T') dentro do próprio ambiente do Editor.</td>
                    <td>Level Maker</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF12</strong></td>
                    <td>Implementar Servidor LAN sobre protocolo UDP na porta 5555 para hospedar partidas de 2 jogadores.</td>
                    <td>Multiplayer</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF13</strong></td>
                    <td>Permitir conexão de cliente ao servidor em LAN informando endereço IP e porta com handshake rápido.</td>
                    <td>Multiplayer</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF14</strong></td>
                    <td>Sincronizar posições, estados e disparos entre jogadores remotos via mensagens CSV leves com LERP.</td>
                    <td>Multiplayer</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF15</strong></td>
                    <td>Desconectar e remover jogadores automaticamente em caso de inatividade superior a 5 segundos (timeout).</td>
                    <td>Multiplayer</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF16</strong></td>
                    <td>Implementar Menu Principal navegável por teclado e mouse (Novo Jogo, Multiplayer, Editor, Opções, Sair).</td>
                    <td>Menus</td>
                    <td>Must Have</td>
                </tr>
                <tr>
                    <td><strong>RF17</strong></td>
                    <td>Disponibilizar tela de Configurações para volumes (Master, BGM, SFX), modos de tela e visualização de teclas.</td>
                    <td>Menus</td>
                    <td>Should Have</td>
                </tr>
                <tr>
                    <td><strong>RF18</strong></td>
                    <td>Implementar Menu de Pausa in-game e telas de Game Over e Vitória com opção de reinício imediato.</td>
                    <td>Menus</td>
                    <td>Must Have</td>
                </tr>
            </tbody>
        </table>

        <h3>7.2 Requisitos Não Funcionais (RNF)</h3>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Categoria</th>
                    <th>Descrição do Requisito Não Funcional</th>
                    <th>Critério de Aceitação / Métrica</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>RNF01</strong></td>
                    <td><strong>Desempenho</strong></td>
                    <td>Taxa de quadros contínua e estável cravada em 60 quadros por segundo.</td>
                    <td>Oscilação máxima de 3% (mínimo de 58 FPS em hardware básico).</td>
                </tr>
                <tr>
                    <td><strong>RNF02</strong></td>
                    <td><strong>Latência de Rede</strong></td>
                    <td>Tempo de propagação de pacotes de sincronismo na rede local imperceptível.</td>
                    <td>RTT em rede local Ethernet/Wi-Fi menor que 30 ms.</td>
                </tr>
                <tr>
                    <td><strong>RNF03</strong></td>
                    <td><strong>Tamanho de Pacote</strong></td>
                    <td>Mensagens UDP ultracompactas para evitar fragmentação e sobrecarga.</td>
                    <td>Carga útil por datagrama menor que 128 bytes.</td>
                </tr>
                <tr>
                    <td><strong>RNF04</strong></td>
                    <td><strong>Concorrência Segura</strong></td>
                    <td>Recepção de pacotes em thread separada sem concorrência destrutiva de memória.</td>
                    <td>Acesso a dicionários de rede sincronizado por <code>threading.Lock</code>.</td>
                </tr>
                <tr>
                    <td><strong>RNF05</strong></td>
                    <td><strong>Persistência Rápida</strong></td>
                    <td>Gravação e leitura instantânea de arquivos de fases personalizadas.</td>
                    <td>Tempo de salvamento e carregamento de mapa menor que 200 ms.</td>
                </tr>
                <tr>
                    <td><strong>RNF06</strong></td>
                    <td><strong>Arquitetura Modular</strong></td>
                    <td>Código desacoplado orientado a objetos com aplicação dos padrões GoF.</td>
                    <td>Isolamento estrito entre camadas de entrada, física, rede e renderização.</td>
                </tr>
                <tr>
                    <td><strong>RNF07</strong></td>
                    <td><strong>Resiliência de Sessão</strong></td>
                    <td>Queda ou saída de um cliente não trava o servidor nem encerra o jogo local.</td>
                    <td>Tratamento de timeout remove o avatar do parceiro sem interrupção do loop.</td>
                </tr>
                <tr>
                    <td><strong>RNF08</strong></td>
                    <td><strong>Portabilidade</strong></td>
                    <td>Execução consistente em múltiplos sistemas operacionais desktop.</td>
                    <td>Compatibilidade homologada com Windows 10/11, Linux e macOS.</td>
                </tr>
            </tbody>
        </table>
    </section>

    <!-- SEÇÃO 8: PADRÕES DE PROJETO USADOS -->
    <section>
        <h2>8. Padrões de Projeto Usados (Design Patterns)</h2>
        <p>
            Em estreito alinhamento com os padrões demonstrados no repositório de referência (<code>tac3</code>), o projeto adota padrões de projeto clássicos (GoF) e arquiteturais que garantem organização, coesão interna e facilidade de manutenção:
        </p>

        <div class="diagram-container">
            __SVG_PATTERNS__
            <div class="diagram-caption">Figura: Visão Geral dos Padrões de Projeto Criacionais, Comportamentais e Arquiteturais Adotados.</div>
        </div>

        <table>
            <thead>
                <tr>
                    <th style="width: 18%;">Padrão GoF</th>
                    <th style="width: 25%;">Classes Envolvidas</th>
                    <th>Finalidade e Benefício no Projeto</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Singleton</strong><br><small>Criacional</small></td>
                    <td><code>Game</code>, <code>Display</code>, <code>Sounds</code>, <code>Settings</code></td>
                    <td>Garante que o controlador principal do loop, o mixer de som, a janela gráfica e as configurações possuam exatamente uma única instância global durante a execução, evitando duplicações indevidas de contexto gráfico ou canais de áudio.</td>
                </tr>
                <tr>
                    <td><strong>Observer</strong><br><small>Comportamental</small></td>
                    <td><code>notify.py</code> (EventBus), <code>Collision</code>, <code>HUD</code>, <code>Sounds</code></td>
                    <td>Implementa um barramento de eventos desacoplado. Quando um inimigo é destruído ou um parafuso é coletado, o subsistema de física emite um evento (<code>ENEMY_KILLED</code>, <code>ITEM_COLLECTED</code>). O HUD e o AudioManager respondem atualizando o placar e tocando o som, sem que a física conheça quem está ouvindo.</td>
                </tr>
                <tr>
                    <td><strong>State</strong><br><small>Comportamental</small></td>
                    <td><code>GameState</code>, <code>BasicMenu</code>, <code>CharacterState</code></td>
                    <td>Controla os estados macro da aplicação (Menu, Jogo Solo, Multiplayer, Editor, Pausa, Game Over) e os estados cinemáticos dos robôs (Idle, Run, Jump, Dash, Hurt), eliminando cascatas confusas de <code>if/elif/else</code> e isolando as transições.</td>
                </tr>
                <tr>
                    <td><strong>Flyweight / Factory</strong><br><small>Estrutural / Criacional</small></td>
                    <td><code>TileMap</code>, <code>Tile</code>, <code>Pallet</code></td>
                    <td>Compartilha recursos pesados (superfícies e texturas na memória de vídeo). Em uma fase com mais de 3.000 blocos de grade, cada textura é carregada uma única vez; a matriz do mapa armazena apenas identificadores inteiros (IDs), economizando centenas de megabytes de RAM.</td>
                </tr>
                <tr>
                    <td><strong>Command</strong><br><small>Comportamental</small></td>
                    <td><code>InputManager</code>, <code>ActionCommand</code></td>
                    <td>Desacopla os dispositivos físicos (teclado, mouse, gamepad) das ações semânticas do jogo (Pular, Atirar, Dash). Facilita o remapeamento arbitrário de teclas e a serialização dos comandos para replicação em rede.</td>
                </tr>
                <tr>
                    <td><strong>Client-Server & Thread Worker</strong><br><small>Arquitetural</small></td>
                    <td><code>LanServer</code>, <code>LanClient</code>, <code>NetReceiverThread</code></td>
                    <td>Desacopla as operações bloqueantes de entrada e saída (I/O) dos sockets UDP, delegando a escuta de pacotes a uma thread secundária sincronizada por <code>Lock</code>, preservando a taxa contínua de 60 FPS do motor de jogo.</td>
                </tr>
            </tbody>
        </table>
    </section>

    <!-- SEÇÃO 9: SISTEMA DE MENUS -->
    <section>
        <h2>9. Sistema de Menus e Interface do Usuário</h2>
        <p>
            Inspirado na arquitetura modular de <code>menu.py</code> do repositório <code>tac3</code>, a interface adota uma classe base reutilizável <code>Basic_menu_all</code> que gerencia seleção retangular translúcida (<code>select_rect</code>), navegação vertical fluida por teclado e mouse, ícones animados e renderização sobre fundos temáticos.
        </p>

        <div class="diagram-container">
            __SVG_MENUS__
            <div class="diagram-caption">Figura: Diagrama de Fluxo e Navegação da Hierarquia de Menus do Jogo.</div>
        </div>

        <h3>9.1 Telas Detalhadas do Sistema de Interface</h3>
        <table>
            <thead>
                <tr>
                    <th style="width: 22%;">Menu / Tela</th>
                    <th style="width: 38%;">Opções e Controles</th>
                    <th>Comportamento do Sistema</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Menu Principal</strong></td>
                    <td>
                        • <strong>Novo Jogo:</strong> Inicia campanha solo.<br>
                        • <strong>Multiplayer LAN:</strong> Abre tela de rede local.<br>
                        • <strong>Editor de Fases:</strong> Carrega o criador de níveis.<br>
                        • <strong>Configurações:</strong> Opções de áudio e vídeo.<br>
                        • <strong>Créditos:</strong> Dados acadêmicos da entrega.<br>
                        • <strong>Sair:</strong> Finaliza o processo.
                    </td>
                    <td>Ponto de partida do jogo. Permite navegação vertical por setas/WASD e confirmação por Enter/Espaço ou clique direto do mouse.</td>
                </tr>
                <tr>
                    <td><strong>Menu Multiplayer LAN</strong></td>
                    <td>
                        • <strong>Hospedar Sala (Host):</strong> Inicia servidor UDP na porta 5555 e exibe o IP local da máquina na tela.<br>
                        • <strong>Entrar em Sala (Join):</strong> Campos de texto interativos para digitar IP do Host e Porta.<br>
                        • <strong>Lobby de Espera:</strong> Mostra avatares dos robôs (Scrappy P1 e Byte P2) e botão "Iniciar Partida".
                    </td>
                    <td>Controla o ciclo de vida da sessão cooperativa em rede local para 2 jogadores.</td>
                </tr>
                <tr>
                    <td><strong>Menu do Editor de Fases</strong></td>
                    <td>
                        • <strong>Novo Mapa:</strong> Abre tela de grade vazia.<br>
                        • <strong>Carregar Mapa:</strong> Seletor de fases salvas (.npz).<br>
                        • <strong>Voltar:</strong> Retorna ao Menu Principal.
                    </td>
                    <td>Permite ao usuário gerenciar fases customizadas criadas localmente.</td>
                </tr>
                <tr>
                    <td><strong>Menu de Configurações</strong></td>
                    <td>
                        • <strong>Volume Master, BGM e SFX:</strong> Sliders de 0 a 100%.<br>
                        • <strong>Modo de Exibição:</strong> Janela (960x540 / 1280x720) vs Tela Cheia.<br>
                        • <strong>V-Sync:</strong> Ativado / Desativado (60 FPS cravado).<br>
                        • <strong>Controles:</strong> Visualização dos esquemas de botões.
                    </td>
                    <td>Persiste as alterações automaticamente no arquivo de preferências <code>source/data/config.json</code>.</td>
                </tr>
                <tr>
                    <td><strong>Menu de Pausa (In-Game)</strong></td>
                    <td>
                        • <strong>Continuar:</strong> Retoma a simulação a 60 FPS.<br>
                        • <strong>Reiniciar Nível:</strong> Reseta a fase atual.<br>
                        • <strong>Opções Rápidas:</strong> Ajuste imediato de volume.<br>
                        • <strong>Menu Principal:</strong> Retorna à tela inicial.
                    </td>
                    <td>Acionado a qualquer instante pela tecla <code>ESC</code>, congelando a física de jogo sem interromper o heartbeat da rede.</td>
                </tr>
            </tbody>
        </table>
    </section>

    <!-- SEÇÃO 10: EDITOR DE FASES -->
    <section>
        <h2>10. Editor de Fases (Level Maker)</h2>
        <p>
            O Editor de Fases segue rigorosamente a estrutura modular simples e funcional do pacote <code>source/modules/maker</code> de <code>tac3</code> (composto por <code>editor.py</code>, <code>grid.py</code>, <code>pallet.py</code>, <code>button.py</code>, <code>info.py</code> e <code>scroll.py</code>). Ele fornece uma ferramenta gráfica integrada que permite criar e validar níveis em tempo de execução sem ferramentas externas.
        </p>

        <h3>10.1 Componentes e Mapeamento de Interação do Editor</h3>
        <ul>
            <li><strong>Grid (Grade Matricial):</strong> Mapeia a tela em células discretas de 32x32 pixels, armazenando matrizes numéricas bidimensionais correspondentes aos blocos e entidades.</li>
            <li><strong>Pallet (Paleta de Sprites):</strong> Painel lateral com miniaturas clicáveis de blocos de terreno (aço, esteiras para esquerda e direita, espinhos), pontos de spawn (P1, P2 e portal final), inimigos (Drones, Prensas, Soldadores) e itens coletáveis (Óleo, Parafuso Dourado, Bateria).</li>
            <li><strong>Interações com o Mouse:</strong>
                <ul>
                    <li><em>Clique Esquerdo (LMB):</em> Pinta/insere o elemento selecionado na paleta na célula apontada pelo cursor do mouse. Ao manter pressionado e arrastar, pinta múltiplos blocos.</li>
                    <li><em>Clique Direito (RMB):</em> Borracha/apaga o elemento da célula (define ID como 0 / vazio).</li>
                    <li><em>Scroll do Mouse ou WASD:</em> Desloca a câmera (rolagem horizontal e vertical) pela extensão da fase.</li>
                </ul>
            </li>
            <li><strong>Info (Painel de Telemetria):</strong> Barra superior que reporta coordenadas atuais da célula sob o cursor, dimensões totais da fase e ID do tile selecionado.</li>
            <li><strong>Modo Playtest Imediato:</strong> A tecla <code>T</code> ou o botão "Testar Fase" instancia instantaneamente Scrappy no ponto de spawn da fase criada, permitindo testar a física dos saltos, esteiras e armadilhas em tempo real. A tecla <code>ESC</code> encerra o teste e retorna à grade.</li>
            <li><strong>Persistência em Formato Comprimido (.npz / JSON):</strong> O mapa é gravado em arquivos matriciais comprimidos via NumPy (ex.: <code>source/data/lv1.npz</code>, <code>lv_custom.npz</code>) ou arquivos JSON legíveis, garantindo abertura e gravação ultrarrápidas (menos de 50 ms).</li>
        </ul>
    </section>

    <!-- SEÇÃO 11: MULTIPLAYER EM LAN -->
    <section>
        <h2>11. Arquitetura Multiplayer em LAN (Cliente e Servidor)</h2>
        <p>
            A infraestrutura de rede local baseia-se nos exemplos didáticos <code>exemplos/threads/server.py</code> e <code>client.py</code> do repositório <code>tac3</code>, utilizando sockets <strong>UDP (User Datagram Protocol)</strong> e concorrência multithread:
        </p>

        <h3>11.1 Especificações da Arquitetura de Rede</h3>
        <ul>
            <li><strong>Protocolo de Transporte UDP na Porta 5555:</strong> Os datagramas UDP são independentes e livres da sobrecarga de handshakes e confirmações (ACKs) do TCP. Para jogos de ação frenética em 2D, a perda ocasional de um pacote de posição é irrelevante, pois o pacote seguinte (16ms depois) já traz a coordenada mais recente.</li>
            <li><strong>Servidor de Sessão LAN (Server):</strong>
                <ul>
                    <li>Executa loop de escuta não-bloqueante com <code>server_socket.settimeout(1.0)</code>;</li>
                    <li>Mantém o registro dos participantes em dicionário de conexões;</li>
                    <li>Realiza <em>Broadcast</em>: ao receber o pacote de um cliente, replica instantaneamente para os outros participantes da sessão;</li>
                    <li>Tratamento de Timeout: descarta clientes que fiquem inativos por mais de 5.0 segundos e emite aviso <code>player_id,remove</code>.</li>
                </ul>
            </li>
            <li><strong>Cliente LAN e Thread de Rede (Client):</strong>
                <ul>
                    <li>Thread de escuta assíncrona desacoplada do loop de desenho do Pygame;</li>
                    <li>Primitiva <code>threading.Lock</code> para leitura e escrita seguras no dicionário de entidades remotas;</li>
                    <li><strong>Interpolação LERP:</strong> A posição do parceiro remoto é suavizada quadro a quadro, deslizando suavemente para as coordenadas alvo e eliminando solavancos e teletransporte decorrentes de oscilações na rede Wi-Fi local.</li>
                </ul>
            </li>
            <li><strong>Protocolo de Mensagens CSV Compacto:</strong> Datagramas curtos e leves:
                <code>ID,x,y,estado,direcao</code> (movimento), <code>ID,shoot,dir_x,dir_y,arma</code> (tiro), <code>ID,hit,dano,hp</code> (dano) e <code>ID,quit</code> (saída voluntária).
            </li>
            <li><strong>Mecânicas Cooperativas e Respawn Contínuo:</strong>
                <ul>
                    <li><em>Câmera Compartilhada:</em> Enquadramento dinâmico baseado no ponto médio entre os dois robôs;</li>
                    <li><em>Respawn Cooperativo sem Isolamento:</em> Diferente do modo solo, quando um jogador cai no abismo ou tem seus PVs zerados durante a partida multiplayer LAN, ele <strong>não</strong> é levado para a tela de Game Over e nem desconectado da sessão. Em vez disso, seu robô é teletransportado de volta para próximo do companheiro com 3 pontos de vida e 120 quadros (2 segundos) de invulnerabilidade com piscar visual. A sincronização de rede faz um <em>snap</em> instantâneo de posição para desvios maiores que 160px, mantendo o tráfego UDP ativo e ambos os jogadores na mesma fase sem interrupções.</li>
                </ul>
            </li>
        </ul>
    </section>

    <!-- SEÇÃO 12: DIAGRAMAS ESTRUTURAIS E DE APOIO -->
    <div class="page-break"></div>
    <section>
        <h2>12. Diagramas Estruturais e de Apoio Atualizados</h2>
        <p>
            Abaixo são apresentados os 5 diagramas atualizados para o <strong>Trabalho 2</strong>, refletindo o Editor de Fases, a Rede LAN, a Hierarquia de Menus e as Máquinas de Estado. Todos os diagramas estão renderizados em gráficos vetoriais puros (SVG) totalmente integrados ao documento:
        </p>

        <!-- FIGURA 1: PACOTES -->
        <h3>12.1 Diagrama de Estrutura de Pacotes/Módulos</h3>
        <p>Apresenta a organização do software em pacotes lógicos e a direção dos fluxos de dados, garantindo separação clara de responsabilidades:</p>
        <div class="diagram-container">
            __SVG_DIAG0__
            <div class="diagram-caption">Figura 1: Diagrama Modular de Pacotes e Comunicação entre Subsistemas (Trabalho 2).</div>
        </div>

        <!-- FIGURA 2: CLASSES UML -->
        <div class="page-break"></div>
        <h3>12.2 Diagrama de Classes UML Completo</h3>
        <p>Detalha a estrutura orientada a objetos das entidades do jogo, destacando heranças, polimorfismo via interfaces, o Editor de Fases e a infraestrutura de rede:</p>
        <div class="diagram-container">
            __SVG_DIAG1__
            <div class="diagram-caption">Figura 2: Diagrama de Classes UML Abrangente com Editor, Rede LAN, Menus e Entidades.</div>
        </div>

        <!-- FIGURA 3: SEQUÊNCIA MULTIPLAYER -->
        <div class="page-break"></div>
        <h3>12.3 Diagrama de Sequência: Ciclo de Sincronização Multiplayer LAN</h3>
        <p>Ilustra a troca de mensagens UDP em tempo real entre o Cliente local, o Servidor e o Cliente remoto com aplicação do LERP:</p>
        <div class="diagram-container">
            __SVG_DIAG2__
            <div class="diagram-caption">Figura 3: Diagrama de Sequência do Envio UDP, Broadcast do Servidor e LERP no Cliente Remoto.</div>
        </div>

        <!-- FIGURA 4: SEQUÊNCIA EDITOR DE FASES -->
        <div class="page-break"></div>
        <h3>12.4 Diagrama de Sequência: Criação e Salvamento no Editor de Fases</h3>
        <p>Demonstra o fluxo interativo do criador de fases desde a seleção de blocos na paleta até a gravação comprimida em arquivo .npz:</p>
        <div class="diagram-container">
            __SVG_DIAG3__
            <div class="diagram-caption">Figura 4: Diagrama de Sequência de Interação de Mouse, Grid e Gravação do Mapa em Arquivo .npz.</div>
        </div>

        <!-- FIGURA 5: MÁQUINA DE ESTADOS GLOBAL -->
        <div class="page-break"></div>
        <h3>12.5 Diagrama da Máquina de Estados Global do Jogo</h3>
        <p>Mapeia os estados macro da aplicação e suas transições operacionais:</p>
        <div class="diagram-container">
            __SVG_DIAG4__
            <div class="diagram-caption">Figura 5: Máquina de Estados Finita (FSM) Global da Aplicação.</div>
        </div>
    </section>

    <!-- SEÇÃO 13: CONCLUSÃO -->
    <section>
        <h2>13. Conclusão e Considerações Finais</h2>
        <p>
            O presente Game Design Document (GDD) consolidado atende com completude e rigor metodológico a todos os requisitos do <strong>Trabalho 2</strong> da disciplina de <strong>Tópicos Avançados em Computação (TAC)</strong>, sob orientação do <strong>Prof. Vanderson</strong>.
        </p>
        <p>
            A incorporação do <strong>Editor de Fases (Level Maker)</strong> oferece uma solução didática e funcional para criação e teste de fases em tempo real com gravação compacta em arquivos <code>.npz</code>. A concepção do subsistema <strong>Multiplayer em LAN (Cliente e Servidor)</strong> através de sockets UDP leves com thread assíncrona desacoplada, interpolação LERP e tratamento de timeout garante uma experiência cooperativa veloz e estável sem impactar o framerate de 60 FPS.
        </p>
        <p>
            Por fim, a fundamentação expressa em <strong>Padrões de Projeto (Singleton, Observer, State, Flyweight, Command e Client-Server)</strong> aliada à modelagem visual completa em diagramas vetoriais SVG inline assegura que a documentação técnica seja robusta, autossuficiente e livre de falhas de carregamento em qualquer ambiente.
        </p>
    </section>

    <!-- RODAPÉ -->
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid var(--border-color); display: flex; justify-content: space-between; font-size: 0.82rem; color: var(--text-muted);">
        <div><strong>Rust & Byte: O Despertar da Sucata</strong> — GDD Trabalho 2 (TAC)</div>
        <div>Docente: Prof. Vanderson | Discente: Vitor de Souza</div>
    </footer>

</div>

</body>
</html>
"""

def get_final_html():
    html = HTML_TEMPLATE
    html = html.replace('__SVG_PATTERNS__', SVG_PATTERNS)
    html = html.replace('__SVG_MENUS__', SVG_MENUS)
    html = html.replace('__SVG_DIAG0__', SVG_DIAG0)
    html = html.replace('__SVG_DIAG1__', SVG_DIAG1)
    html = html.replace('__SVG_DIAG2__', SVG_DIAG2)
    html = html.replace('__SVG_DIAG3__', SVG_DIAG3)
    html = html.replace('__SVG_DIAG4__', SVG_DIAG4)
    return html

def main():
    base_dir = os.path.dirname(__file__)
    final_html = get_final_html()

    target_path1 = os.path.join(base_dir, "Relatorio_GDD_Trabalho1_TAC.html")
    with open(target_path1, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"[✓] Relatório atualizado gravado em: {target_path1}")

    target_path2 = os.path.join(base_dir, "Relatorio_GDD_Trabalho2_TAC.html")
    with open(target_path2, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"[✓] Cópia Trabalho 2 gravada em: {target_path2}")

if __name__ == "__main__":
    main()
