#!/usr/bin/env bash
# ==============================================================================
# Script de Instalação de Dependências
# Projeto: Rust & Byte: O Despertar da Sucata
# Disciplina: Tópicos Avançados em Computação (TAC)
# ==============================================================================

set -e

# Cores para saída no terminal
VERDE='\033[0;32m'
AZUL='\033[0;34m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
NEGRITO='\033[1m'
SEM_COR='\033[0m'

echo -e "${AZUL}${NEGRITO}======================================================${SEM_COR}"
echo -e "${AZUL}${NEGRITO}  ⚙️  Instalador de Dependências - Rust & Byte  ⚙️  ${SEM_COR}"
echo -e "${AZUL}${NEGRITO}======================================================${SEM_COR}\n"

# 1. Identificar o interpretador Python adequado
PYTHON_CMD=""
for cmd in python3.14 python3.13 python3.12 python3.11 python3.10 python3 python; do
    if command -v "$cmd" &> /dev/null; then
        # Verificar se a versão é pelo menos 3.9
        VER_OK=$("$cmd" -c 'import sys; print(1 if sys.version_info >= (3, 9) else 0)' 2>/dev/null || echo 0)
        if [ "$VER_OK" -eq 1 ]; then
            PYTHON_CMD="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${VERMELHO}❌ Erro: Python 3 (versão 3.9 ou superior) não foi encontrado no sistema.${SEM_COR}"
    echo -e "Por favor, instale o Python 3.9+ e tente novamente."
    exit 1
fi

PYTHON_VERSAO=$("$PYTHON_CMD" -c 'import platform; print(platform.python_version())')
echo -e "${VERDE}✓ Python detectado:${SEM_COR} $PYTHON_CMD ($PYTHON_VERSAO)"

DIRETORIO_PROJETO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIRETORIO_PROJETO"

# 2. Decisão: Ambiente Virtual (.venv) ou Instalação Direta
VENV_DIR="$DIRETORIO_PROJETO/.venv"
USAR_SISTEMA=0

# Checar argumentos
if [[ "$*" == *"--system"* ]] || [[ "$*" == *"--global"* ]]; then
    USAR_SISTEMA=1
fi

if [ -n "$VIRTUAL_ENV" ]; then
    echo -e "${AZUL}ℹ️  Ambiente virtual ativo detectado:${SEM_COR} $VIRTUAL_ENV"
    TARGET_PYTHON="$PYTHON_CMD"
elif [ "$USAR_SISTEMA" -eq 1 ]; then
    echo -e "${AMARELO}ℹ️  Instalando diretamente no ambiente global/sistema...${SEM_COR}"
    TARGET_PYTHON="$PYTHON_CMD"
else
    echo -e "${AZUL}📦 Configurando ambiente virtual isolado (.venv)...${SEM_COR}"
    if [ ! -d "$VENV_DIR" ]; then
        "$PYTHON_CMD" -m venv "$VENV_DIR"
        echo -e "${VERDE}✓ Ambiente virtual criado em:${SEM_COR} $VENV_DIR"
    else
        echo -e "${VERDE}✓ Ambiente virtual existente reutilizado:${SEM_COR} $VENV_DIR"
    fi
    TARGET_PYTHON="$VENV_DIR/bin/python"
fi

# 3. Atualizar pip e instalar dependências
echo -e "\n${AZUL}⬇️  Instalando dependências de 'requirements.txt'...${SEM_COR}"

PIP_FLAGS=""
# Se for ambiente gerenciado fora do venv, permitir flag de override
if [ "$USAR_SISTEMA" -eq 1 ] && [ -z "$VIRTUAL_ENV" ]; then
    PIP_FLAGS="--break-system-packages"
fi

"$TARGET_PYTHON" -m pip install --upgrade pip $PIP_FLAGS > /dev/null 2>&1 || true
# Se o pygame antigo estiver instalado no ambiente, desinstalar para evitar conflitos com pygame-ce
"$TARGET_PYTHON" -m pip uninstall -y $PIP_FLAGS pygame > /dev/null 2>&1 || true
"$TARGET_PYTHON" -m pip install $PIP_FLAGS -r requirements.txt

# 4. Testar importação do Pygame, Font e Mixer
echo -e "\n${AZUL}🔍 Verificando integridade das dependências (Display, Font e Audio)...${SEM_COR}"
CHECK_RESULT=$(SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy "$TARGET_PYTHON" -c "
import pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
print(f'OK:{pygame.__version__}')
" 2>&1 || echo "ERRO")

if [[ "$CHECK_RESULT" == *"OK:"* ]]; then
    VERSAO_INSTALADA=$(echo "$CHECK_RESULT" | grep "OK:" | cut -d':' -f2)
    echo -e "${VERDE}✓ Pygame $VERSAO_INSTALADA validado com sucesso (Módulos de Vídeo, Fontes e Mixer OK)!${SEM_COR}\n"
else
    echo -e "${VERMELHO}❌ Erro ao validar o Pygame:${SEM_COR}"
    echo "$CHECK_RESULT"
    exit 1
fi

# 5. Criar script de atalho para execução fácil (executar.sh)
cat << 'EOF' > "$DIRETORIO_PROJETO/executar.sh"
#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$DIR/.venv/bin/python" ]; then
    exec "$DIR/.venv/bin/python" "$DIR/main.py" "$@"
else
    exec python3 "$DIR/main.py" "$@"
fi
EOF
chmod +x "$DIRETORIO_PROJETO/executar.sh"

echo -e "${VERDE}${NEGRITO}🎉 Tudo pronto para jogar!${SEM_COR}"
echo -e "${NEGRITO}Como executar o jogo:${SEM_COR}"
if [ -d "$VENV_DIR" ] && [ -z "$VIRTUAL_ENV" ]; then
    echo -e "  1. Diretamente pelo atalho:   ${VERDE}./executar.sh${SEM_COR}"
    echo -e "  2. Ou ativando o venv:        ${VERDE}source .venv/bin/activate && python main.py${SEM_COR}"
else
    echo -e "  1. Pelo comando:              ${VERDE}python3 main.py${SEM_COR}"
    echo -e "  2. Ou pelo atalho:            ${VERDE}./executar.sh${SEM_COR}"
fi
echo ""
