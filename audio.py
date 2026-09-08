# -*- coding: utf-8 -*-
"""
Módulo de Áudio e Efeitos Sonoros Retro
Rust & Byte: O Despertar da Sucata

Sintetiza efeitos sonoros retro proceduralmente em tempo de execução,
eliminando dependência de arquivos WAV/MP3 externos para máxima portabilidade.
"""

import io
import math
import struct
import wave
import random
import pygame


class SomDummy:
    """Objeto substituto silencioso caso o áudio do sistema não inicialize."""
    def play(self):
        pass


def _gerar_onda_wav(freq_inicio, freq_fim, duracao_seg, tipo_onda="square", volume=0.4, ruido=False):
    """
    Sintetiza dados de áudio em formato PCM 16-bit Mono e retorna um pygame.mixer.Sound.
    """
    taxa_amostragem = 22050
    total_amostras = int(taxa_amostragem * duracao_seg)
    buffer = io.BytesIO()

    try:
        with wave.open(buffer, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(taxa_amostragem)

            dados = bytearray()
            for i in range(total_amostras):
                t = i / taxa_amostragem
                progresso = i / total_amostras
                freq = freq_inicio + (freq_fim - freq_inicio) * progresso
                envelope = 1.0 - progresso  # Decaimento linear simples

                if ruido:
                    amostra_bruta = random.uniform(-1.0, 1.0)
                elif tipo_onda == "square":
                    fase = math.sin(2 * math.pi * freq * t)
                    amostra_bruta = 0.6 if fase > 0 else -0.6
                elif tipo_onda == "sine":
                    amostra_bruta = math.sin(2 * math.pi * freq * t)
                elif tipo_onda == "saw":
                    fase = (t * freq) % 1.0
                    amostra_bruta = (fase * 2.0) - 1.0
                else:
                    amostra_bruta = 0.0

                valor_final = int(amostra_bruta * envelope * volume * 32767)
                valor_final = max(-32768, min(32767, valor_final))
                dados += struct.pack("<h", valor_final)

            wav.writeframes(dados)

        buffer.seek(0)
        return pygame.mixer.Sound(buffer)
    except Exception:
        return SomDummy()


class GerenciadorAudio:
    """Centralizador de efeitos sonoros do jogo."""
    def __init__(self):
        self.disponivel = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.disponivel = True
        except Exception:
            self.disponivel = False

        if self.disponivel:
            # Sintetiza os sons característicos do GDD
            self.som_pulo = _gerar_onda_wav(220, 520, 0.12, tipo_onda="sine", volume=0.35)
            self.som_pulo_duplo = _gerar_onda_wav(300, 700, 0.14, tipo_onda="saw", volume=0.3)
            self.som_tiro = _gerar_onda_wav(850, 200, 0.08, tipo_onda="square", volume=0.25)
            self.som_tiro_triplo = _gerar_onda_wav(950, 350, 0.09, tipo_onda="saw", volume=0.28)
            self.som_dash = _gerar_onda_wav(180, 80, 0.16, tipo_onda="saw", volume=0.35, ruido=True)
            self.som_impacto_inimigo = _gerar_onda_wav(600, 150, 0.07, tipo_onda="square", volume=0.3)
            self.som_dano_jogador = _gerar_onda_wav(120, 40, 0.25, tipo_onda="saw", volume=0.4, ruido=True)
            self.som_item = _gerar_onda_wav(523, 784, 0.14, tipo_onda="sine", volume=0.35)
            self.som_vitoria = _gerar_onda_wav(440, 880, 0.35, tipo_onda="square", volume=0.35)
        else:
            dummy = SomDummy()
            self.som_pulo = dummy
            self.som_pulo_duplo = dummy
            self.som_tiro = dummy
            self.som_tiro_triplo = dummy
            self.som_dash = dummy
            self.som_impacto_inimigo = dummy
            self.som_dano_jogador = dummy
            self.som_item = dummy
            self.som_vitoria = dummy

    def tocar(self, nome_som):
        """Reproduz um som pelo nome do atributo."""
        som = getattr(self, nome_som, None)
        if som:
            try:
                som.play()
            except Exception:
                pass
