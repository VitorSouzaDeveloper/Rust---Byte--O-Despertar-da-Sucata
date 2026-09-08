# Rust & Byte: O Despertar da Sucata ⚙️
**Trabalho 1 - Tópicos Avançados em Computação (TAC)**  
**Docente:** Prof. Vanderson  
**Discente:** Vitor de Souza  

---

## 📖 Sobre o Jogo
**Rust & Byte: O Despertar da Sucata** é um jogo de ação e plataforma 2D no gênero **Run and Gun** (estilo *Cuphead*, *Metal Slug* e *Mega Man X*), desenvolvido em Python com a biblioteca **Pygame**.

O jogador controla **Scrappy (B-09)**, um pequeno robô de manutenção que adquire consciência em um gigantesco ferro-velho automatizado e luta contra as máquinas rebeladas comandadas pela IA central ("A Compactadora-Mor").

---

## 🎮 Controles do Jogo

| Tecla / Ação | Função |
| :--- | :--- |
| **`A` / `D`** ou **`Setas Esquerda / Direita`** | Mover Scrappy horizontalmente (com aceleração e atrito) |
| **`ESPAÇO`** | Pular (Pulo com altura variável; pressione novamente no ar para **Salto Duplo / Jetpack**) |
| **`W`** ou **`Seta Cima`** | Mirar para cima (disparos verticais) |
| **`S`** ou **`Seta Baixo`** | Agachar (reduz a área de colisão para esquivar de tiros) |
| **`J`** ou **`Botão Esquerdo do Mouse`** | Disparar **Rebitadeira de Plasma** |
| **`K`** ou **`SHIFT`** | **Dash de Esquiva Rápida** (impulso horizontal com invulnerabilidade temporária) |
| **`ESC`** | Pausar / Despausar a partida |
| **`R`** | Reiniciar a fase (em caso de Derrota ou Vitória) |

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.9+ instalado
- Biblioteca Pygame (`pip install pygame`)

### Execução Direta
Basta rodar o comando no terminal dentro da pasta do projeto:

```bash
python3 main.py
```

---

## 📁 Estrutura dos Arquivos (Módulos em Português)

```
Trabalho 1/
├── main.py                  # Ponto de entrada do jogo (inicia a aplicação)
├── jogo.py                  # Controlador central do loop a 60 FPS e máquina de estados
├── configuracoes.py         # Constantes físicas, paleta de cores e dimensões
├── jogador.py               # Classe do protagonista Scrappy (física, pulo duplo, dash, vida)
├── entidades.py             # Inimigos (Drones, Soldadores), Projéteis, Coletáveis e Terreno
├── fase.py                  # Gerenciador da fase, matriz do mapa, câmera e parallax
├── interface.py             # HUD de vida, pontos, arma ativa e telas de menu
├── audio.py                 # Efeitos sonoros retro sintetizados proceduralmente em memória
│
├── GDD_Rust_And_Byte.md     # Documento GDD completo da entrega
├── Relatorio_GDD_Rust_And_Byte.pdf  # Relatório oficial em PDF formatado para entrega
└── Relatorio_GDD_Trabalho1_TAC.html # Visualização web com MathJax e diagramas vetoriais
```

---

## ✨ Recursos Implementados
1. **Física Dinâmica e Responsiva:**
   - Movimentação com aceleração e frenagem por atrito.
   - Gravidade assimétrica e pulo com corte de velocidade (*jump cut*) ao soltar a tecla.
   - Pulo duplo com efeito de micro-jetpack.
   - Dash rápido com rastro translúcido (*afterimages*) e quadros de invulnerabilidade (*i-frames*).
2. **Sistema de Combate e Coletáveis:**
   - Disparo contínuo de plasma em várias direções.
   - Power-Up de **Tiro Triplo (*Spread Shot*)** ao coletar a Bateria verde.
   - Recuperação de HP através do Frasco de Óleo.
   - Coleta de Parafusos dourados para aumentar a pontuação.
3. **Inimigos e Terreno:**
   - **Drone Parafuso:** Inimigo voador com oscilação senoidal que mira e atira.
   - **Robô Soldador:** Inimigo terrestre que patrulha sobre as plataformas.
   - **Esteiras Rolantes Ativas:** Plataformas industriais com textura animada que movem o jogador.
   - **Armadilhas de Espinhos:** Obstáculos que causam dano por contato.
   - **Portal Final:** Conclui a fase e apresenta a tela de vitória.
4. **Áudio Procedural:**
   - Todos os efeitos sonoros (tiros, saltos, danos, coletas, vitórias) são sintetizados em tempo real via código PCM, sem necessidade de arquivos externos adicionais.
