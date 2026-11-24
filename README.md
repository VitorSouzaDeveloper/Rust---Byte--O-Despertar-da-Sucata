# Rust & Byte: O Despertar da Sucata ⚙️
**Trabalho 2 - Tópicos Avançados em Computação (TAC)**  
**Docente:** Prof. Vanderson  
**Discente:** Vitor de Souza  

---

## 📖 Sobre o Jogo
**Rust & Byte: O Despertar da Sucata** é um jogo de ação e plataforma 2D no gênero **Run and Gun** (inspirado em clássicos como *Cuphead*, *Metal Slug* e *Mega Man X*), desenvolvido em Python com a biblioteca **Pygame**.

O jogador controla **Scrappy (B-09)** e seu parceiro **Byte (K-12)**, autômatos de manutenção utilitária que adquirem consciência em um gigantesco ferro-velho automatizado e lutam contra as máquinas rebeladas comandadas pela IA central ("A Compactadora-Mor").

---

## 🚀 Novidades Implementadas no Trabalho 2
- 🛠️ **Editor de Fases (Level Maker):** Grade matricial interativa de 32x32 pixels para inserção/remoção de blocos de terreno, esteiras, espinhos, inimigos (Drones e Soldadores) e itens coletáveis via mouse. Suporta salvamento e carregamento rápido em formato matricial comprimido (`.npz` NumPy) e formato aberto estruturado (`.json`), além do modo de teste integrado instantâneo (**Playtest** via tecla `T`).
- 🌐 **Multiplayer em LAN (Cliente e Servidor UDP):** Arquitetura leve sobre sockets UDP (porta `5555`) com thread de recepção assíncrona desacoplada do loop gráfico de 60 FPS, sincronização bidirecional de telemetria, interpolação linear suave (**LERP**) para evitar teletransporte e tratamento automático de desconexão por timeout (5s).
- 🎮 **Dois Protagonistas Cooperativos:** Suporte a **Scrappy** (azul-aço) como Jogador 1 e **Byte** (bronze/cobre) como Jogador 2, com câmera dinâmica dupla que enquadra continuamente o ponto médio entre os robôs.
- 🧩 **Padrões de Projeto (Design Patterns):**
  - **Singleton:** `Jogo`, `Display`, `GerenciadorAudio`, `FabricaTiles`, `BarramentoEventos`;
  - **Observer / Pub-Sub (`notify.py`):** Barramento central de eventos para desacoplamento entre física, combate, áudio e HUD;
  - **State Pattern (`menu.py` & `jogo.py`):** Máquina de estados finita (FSM) controlando Menu Principal, Lobby LAN, Editor, Playtest, Configurações, Gameplay e Pausa;
  - **Flyweight / Factory (`fabrica_tiles.py`):** Cache de texturas e geração compartilhada de blocos para otimização de memória RAM;
  - **Command:** Desacoplamento de mapeamento de entradas e ações.
- 🖥️ **Sistema Completo de Menus:** Menu Principal estilizado, Menu Multiplayer em LAN (Hospedar Sala / Conectar via IP e Porta), Menu do Editor de Fases, Menu de Configurações (volumes BGM/SFX, modos de tela) e Menu de Pausa in-game.
- 📊 **Diagramas Estruturais Atualizados:** 7 diagramas vetoriais SVG inline no relatório técnico (Diagrama Modular de Pacotes em 3 camadas, Diagrama de Classes UML, Diagramas de Sequência Multiplayer e Editor, FSM Global, Hierarquia de Menus e Padrões GoF).

---

## 🎮 Controles do Jogo

| Tecla / Ação | Função |
| :--- | :--- |
| **`A` / `D`** ou **`Setas Esquerda / Direita`** | Mover robô horizontalmente (com aceleração e atrito) |
| **`ESPAÇO`** | Pular (Pulo com altura dinâmica; pressione novamente no ar para **Salto Duplo / Jetpack**) |
| **`W`** ou **`Seta Cima`** | Mirar para cima (disparos verticais) |
| **`S`** ou **`Seta Baixo`** | Agachar (reduz a área de colisão para esquivar de tiros) |
| **`J`** ou **`Botão Esquerdo do Mouse`** | Disparar **Rebitadeira de Plasma** |
| **`K`** ou **`SHIFT`** | **Dash de Esquiva Rápida** (impulso horizontal com invulnerabilidade temporária) |
| **`ESC`** | Pausar partida, voltar telas ou sair do editor |
| **`R`** | Reiniciar a fase (em caso de derrota, vitória ou pausa) |
| **`T`** (no Editor de Fases) | Iniciar imediatamente o modo **Playtest** da fase criada |
| **Botão Esquerdo / Direito (no Editor)** | Pintar tile selecionado / Apagar célula da grade |

---

## 🚀 Como Executar

### 1. Instalação Automática das Dependências
Execute o script de instalação para configurar o ambiente virtual e instalar o Pygame e NumPy:

```bash
./instalar_dependencias.sh
```

### 2. Executando o Jogo
Você pode iniciar o jogo de qualquer uma das seguintes formas:

- **Atalho rápido (Recomendado):**
  ```bash
  ./executar.sh
  ```
- **Ou pelo ambiente virtual:**
  ```bash
  source .venv/bin/activate
  python main.py
  ```
- **Ou diretamente pelo Python do sistema:**
  ```bash
  python3 main.py
  ```

---

## 📁 Estrutura dos Arquivos do Projeto

```
Trabalho 1/
├── main.py                          # Ponto de entrada do jogo
├── jogo.py                          # Controlador mestre (FSM de Estados, Loop 60 FPS)
├── menu.py                          # Menus modulares (Principal, LAN, Configurações, Pausa)
├── editor.py                        # Editor de Fases (Level Maker interativo com Playtest)
├── rede.py                          # Sockets UDP (Servidor LAN e Cliente LAN com LERP)
├── fabrica_tiles.py                 # Padrão Flyweight / Factory com cache de texturas
├── notify.py                        # Padrão Observer / Barramento de eventos (EventBus)
├── fase.py                          # Gerenciador da fase, câmera dinâmica dupla e parallax
├── jogador.py                       # Protagonistas Scrappy (P1), Byte (P2) e JogadorRemoto
├── entidades.py                     # Inimigos (Drones, Soldadores), Projéteis, Coletáveis
├── interface.py                     # HUD de vida individual e cooperativa, pontuação e overlays
├── audio.py                         # Efeitos sonoros sintetizados proceduralmente em memória
├── configuracoes.py                 # Constantes de física, dimensões, cores e rede
├── requirements.txt                 # Dependências (pygame-ce e numpy)
├── executar.sh                      # Script de inicialização rápida
├── instalar_dependencias.sh         # Script de setup do ambiente virtual
│
├── GDD_Rust_And_Byte.md             # Documento de Game Design completo (Trabalho 2)
├── Relatorio_GDD_Rust_And_Byte.pdf  # Relatório acadêmico compilado em PDF oficial
├── Relatorio_GDD_Trabalho2_TAC.html # Relatório completo em HTML com diagramas vetoriais SVG
├── Relatorio_GDD_Trabalho1_TAC.html # Cópia de trabalho sincronizada
├── build_full_report.py             # Script de compilação dos relatórios HTML com SVGs
└── generate_pdf.sh                  # Utilitário de compilação do PDF via Chrome headless
```
