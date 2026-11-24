#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ponto de Entrada Principal - Rust & Byte: O Despertar da Sucata
Trabalho 2 - Disciplina: Tópicos Avançados em Computação (TAC)
Docente: Prof. Vanderson | Discente: Vitor de Souza
"""

from jogo import Jogo


def principal():
    """Inicia e executa a instância do jogo."""
    app = Jogo()
    app.executar()


if __name__ == "__main__":
    principal()
