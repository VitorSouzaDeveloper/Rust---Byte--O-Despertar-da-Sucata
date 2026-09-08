#!/usr/bin/env bash
# ==============================================================================
# Script Utilitário de Geração de PDF - Trabalho 1 (TAC - Prof. Vanderson)
# Jogo: Rust & Byte: O Despertar da Sucata (GDD)
# ==============================================================================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HTML_PATH="$DIR/Relatorio_GDD_Trabalho1_TAC.html"
OUTPUT_PDF="$DIR/Relatorio_GDD_Rust_And_Byte.pdf"

echo "=========================================================="
echo "  Gerador de Relatório PDF - Game Design Document (TAC)  "
echo "=========================================================="

if [ -f "$CHROME_PATH" ]; then
    echo "[+] Localizado: $CHROME_PATH"
    echo "[+] Renderizando HTML e convertendo para PDF..."
    "$CHROME_PATH" --headless=new --disable-gpu --virtual-time-budget=6000 --print-to-pdf="$OUTPUT_PDF" "file://$HTML_PATH" 2>/dev/null
    
    if [ -f "$OUTPUT_PDF" ]; then
        SIZE=$(du -h "$OUTPUT_PDF" | cut -f1)
        echo "[✓] Sucesso! Arquivo PDF gerado:"
        echo "    Caminho: $OUTPUT_PDF"
        echo "    Tamanho: $SIZE"
    else
        echo "[!] Falha ao gerar o arquivo PDF."
    fi
else
    echo "[!] Google Chrome não encontrado no caminho padrão do macOS."
    echo "[i] Para gerar o PDF manualmente:"
    echo "    1. Abra o arquivo: $HTML_PATH no seu navegador (Chrome, Edge ou Safari);"
    echo "    2. Pressione Ctrl+P (ou Cmd+P no Mac);"
    echo "    3. Em 'Destino', selecione 'Salvar como PDF';"
    echo "    4. Certifique-se de marcar 'Gráficos de segundo plano' nas opções avançadas."
fi
