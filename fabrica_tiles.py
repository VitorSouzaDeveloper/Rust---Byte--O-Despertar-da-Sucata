# -*- coding: utf-8 -*-
"""
Módulo de Fábrica de Tiles (Padrão Flyweight / Factory)
Rust & Byte: O Despertar da Sucata

Compartilha instâncias únicas de texturas e sprites de blocos e entidades,
evitando alocações redundantes na memória gráfica ao renderizar o mapa e o editor.
"""

import pygame
from configuracoes import (
    TAMANHO_BLOCO, COR_PLATAFORMA, COR_PLATAFORMA_BORDA, COR_ESTEIRA,
    COR_ESTEIRA_LISTRA, COR_ESPINHO, COR_PORTAL, COR_DRONE, COR_SOLDADOR,
    COR_OLEO, COR_PARAFUSO, COR_BATERIA, COR_JOGADOR_CHASSI, COR_DESTAQUE
)


class FabricaTiles:
    """Fábrica Flyweight com cache de superfícies pré-renderizadas de blocos."""
    _instancia = None
    _cache = {}

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(FabricaTiles, cls).__new__(cls)
            cls._instancia._inicializar_cache()
        return cls._instancia

    def _inicializar_cache(self):
        """Gera as texturas padrão de cada elemento."""
        # 1. Plataforma de Aço ('#')
        surf_plat = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO))
        surf_plat.fill(COR_PLATAFORMA)
        pygame.draw.rect(surf_plat, COR_PLATAFORMA_BORDA, (0, 0, TAMANHO_BLOCO, TAMANHO_BLOCO), 2)
        pygame.draw.line(surf_plat, (90, 95, 110), (0, 0), (TAMANHO_BLOCO, TAMANHO_BLOCO), 1)
        pygame.draw.circle(surf_plat, (40, 45, 55), (6, 6), 2)
        pygame.draw.circle(surf_plat, (40, 45, 55), (TAMANHO_BLOCO - 6, 6), 2)
        pygame.draw.circle(surf_plat, (40, 45, 55), (6, TAMANHO_BLOCO - 6), 2)
        pygame.draw.circle(surf_plat, (40, 45, 55), (TAMANHO_BLOCO - 6, TAMANHO_BLOCO - 6), 2)
        self._cache['#'] = surf_plat

        # 2. Esteira Rolante ('=')
        surf_est = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO))
        surf_est.fill(COR_ESTEIRA)
        for i in range(0, TAMANHO_BLOCO, 8):
            pts = [(i, 0), (i + 4, 0), (i, TAMANHO_BLOCO), (i - 4, TAMANHO_BLOCO)]
            pygame.draw.polygon(surf_est, COR_ESTEIRA_LISTRA, pts)
        pygame.draw.rect(surf_est, (230, 160, 60), (0, 0, TAMANHO_BLOCO, TAMANHO_BLOCO), 2)
        self._cache['='] = surf_est

        # 3. Armadilha de Espinho ('^')
        surf_esp = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        esp_larg = TAMANHO_BLOCO // 4
        for i in range(4):
            x_ini = i * esp_larg
            pts = [
                (x_ini, TAMANHO_BLOCO),
                (x_ini + esp_larg // 2, 4),
                (x_ini + esp_larg, TAMANHO_BLOCO)
            ]
            pygame.draw.polygon(surf_esp, COR_ESPINHO, pts)
            pygame.draw.polygon(surf_esp, (255, 120, 120), pts, 1)
        self._cache['^'] = surf_esp

        # 4. Portal Final ('E')
        surf_port = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        pygame.draw.rect(surf_port, (50, 20, 70), (2, 2, TAMANHO_BLOCO - 4, TAMANHO_BLOCO - 4), border_radius=4)
        pygame.draw.ellipse(surf_port, COR_PORTAL, (4, 4, TAMANHO_BLOCO - 8, TAMANHO_BLOCO - 8))
        pygame.draw.ellipse(surf_port, (230, 180, 255), (8, 8, TAMANHO_BLOCO - 16, TAMANHO_BLOCO - 16))
        self._cache['E'] = surf_port

        # 5. Spawn P1 Scrappy ('@')
        surf_sp1 = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        pygame.draw.circle(surf_sp1, (50, 160, 220), (TAMANHO_BLOCO // 2, TAMANHO_BLOCO // 2), 12)
        pygame.draw.circle(surf_sp1, (255, 255, 255), (TAMANHO_BLOCO // 2, TAMANHO_BLOCO // 2), 12, 2)
        self._cache['@'] = surf_sp1

        # 6. Spawn P2 Byte ('2')
        surf_sp2 = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        pygame.draw.circle(surf_sp2, (205, 120, 50), (TAMANHO_BLOCO // 2, TAMANHO_BLOCO // 2), 12)
        pygame.draw.circle(surf_sp2, (255, 255, 255), (TAMANHO_BLOCO // 2, TAMANHO_BLOCO // 2), 12, 2)
        self._cache['2'] = surf_sp2

        # 7. Inimigo Drone ('D')
        surf_dro = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        pygame.draw.ellipse(surf_dro, COR_DRONE, (4, 8, TAMANHO_BLOCO - 8, TAMANHO_BLOCO - 16))
        pygame.draw.circle(surf_dro, (255, 240, 60), (TAMANHO_BLOCO // 2, TAMANHO_BLOCO // 2), 4)
        self._cache['D'] = surf_dro

        # 8. Inimigo Soldador ('S')
        surf_sol = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        pygame.draw.rect(surf_sol, COR_SOLDADOR, (6, 6, TAMANHO_BLOCO - 12, TAMANHO_BLOCO - 10), border_radius=3)
        pygame.draw.line(surf_sol, (255, 140, 20), (TAMANHO_BLOCO - 6, TAMANHO_BLOCO // 2), (TAMANHO_BLOCO, TAMANHO_BLOCO // 2), 3)
        self._cache['S'] = surf_sol

        # 9. Coletável Óleo ('O')
        surf_ole = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        pygame.draw.rect(surf_ole, COR_OLEO, (10, 10, TAMANHO_BLOCO - 20, TAMANHO_BLOCO - 16), border_radius=3)
        pygame.draw.rect(surf_ole, (255, 255, 200), (12, 6, 8, 4))
        self._cache['O'] = surf_ole

        # 10. Coletável Parafuso ('P')
        surf_par = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        pygame.draw.circle(surf_par, COR_PARAFUSO, (TAMANHO_BLOCO // 2, TAMANHO_BLOCO // 2), 8)
        pygame.draw.line(surf_par, (160, 120, 0), (TAMANHO_BLOCO // 2 - 5, TAMANHO_BLOCO // 2), (TAMANHO_BLOCO // 2 + 5, TAMANHO_BLOCO // 2), 2)
        self._cache['P'] = surf_par

        # 11. Coletável Bateria ('B')
        surf_bat = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        pygame.draw.rect(surf_bat, COR_BATERIA, (8, 6, 16, 20), border_radius=2)
        pygame.draw.rect(surf_bat, (200, 255, 230), (12, 3, 8, 3))
        self._cache['B'] = surf_bat

    def obter_tile(self, char_id):
        """Retorna a superfície Flyweight compartilhada do tile solicitado."""
        return self._cache.get(char_id, None)

    def obter_icone_redimensionado(self, char_id, tamanho=24):
        """Retorna uma versão em miniatura do tile para a barra de ferramentas."""
        surf = self.obter_tile(char_id)
        if surf:
            return pygame.transform.smoothscale(surf, (tamanho, tamanho))
        vazia = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        return vazia


# Instância global da fábrica Flyweight
fabrica_tiles = FabricaTiles()
