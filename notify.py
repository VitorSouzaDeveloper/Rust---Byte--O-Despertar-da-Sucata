# -*- coding: utf-8 -*-
"""
Módulo de Barramento de Eventos (Padrão Observer / Pub-Sub)
Rust & Byte: O Despertar da Sucata

Permite que sistemas desacoplados (física, áudio, HUD, rede) emitam
e escutem eventos sem dependências diretas entre classes.
"""

from collections import defaultdict


class BarramentoEventos:
    """Implementa o padrão Observer como um EventBus centralizado."""
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(BarramentoEventos, cls).__new__(cls)
            cls._instancia._ouvintes = defaultdict(list)
        return cls._instancia

    def inscrever(self, tipo_evento, callback):
        """Registra uma função de callback para um tipo de evento."""
        if callback not in self._ouvintes[tipo_evento]:
            self._ouvintes[tipo_evento].append(callback)

    def subscribe(self, tipo_evento, callback):
        """Alias em inglês para inscrever."""
        self.inscrever(tipo_evento, callback)

    def desinscrever(self, tipo_evento, callback):
        """Remove um callback registrado de um tipo de evento."""
        if callback in self._ouvintes[tipo_evento]:
            self._ouvintes[tipo_evento].remove(callback)

    def unsubscribe(self, tipo_evento, callback):
        """Alias em inglês para desinscrever."""
        self.desinscrever(tipo_evento, callback)

    def emitir(self, tipo_evento, **dados):
        """Notifica todos os ouvintes registrados para o tipo de evento."""
        for callback in list(self._ouvintes[tipo_evento]):
            try:
                callback(**dados)
            except Exception as e:
                print(f"[Aviso EventBus] Erro ao disparar {tipo_evento}: {e}")

    def emit(self, tipo_evento, **dados):
        """Alias em inglês para emitir."""
        self.emitir(tipo_evento, **dados)

    def limpar(self):
        """Remove todos os ouvintes registrados."""
        self._ouvintes.clear()


# Instância global (Singleton) do EventBus
notify = BarramentoEventos()

# Tipos de Eventos Padronizados
EVENTO_DANO_JOGADOR = "DANO_JOGADOR"
EVENTO_INIMIGO_DERROTADO = "INIMIGO_DERROTADO"
EVENTO_ITEM_COLETADO = "ITEM_COLETADO"
EVENTO_FASE_CONCLUIDA = "FASE_CONCLUIDA"
EVENTO_DISPARO = "DISPARO"
EVENTO_PULO = "PULO"
EVENTO_DASH = "DASH"
EVENTO_REDE_PACOTE = "REDE_PACOTE"
