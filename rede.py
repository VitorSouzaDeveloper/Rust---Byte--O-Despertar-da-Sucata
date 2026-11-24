# -*- coding: utf-8 -*-
"""
Módulo de Rede LAN Multiplayer (Cliente e Servidor UDP com LERP)
Rust & Byte: O Despertar da Sucata

Implementa arquitetura Client-Server sobre protocolo UDP não-bloqueante
com sincronização leve em thread dedicada e interpolação linear (LERP).
"""

import socket
import threading
import time


PORTA_PADRAO_LAN = 5555
TIMEOUT_JOGADOR_SEGUNDOS = 5.0


class ServidorLAN:
    """Servidor UDP leve para hospedar partidas de 2 jogadores em rede local."""
    def __init__(self, porta=PORTA_PADRAO_LAN):
        self.porta = porta
        self.socket_udp = None
        self.executando = False
        self.thread_servidor = None
        self.lock = threading.Lock()
        
        # Estrutura: { endereco_tuple: {'id': str, 'x': float, 'y': float, 'vel_x': float,
        #                               'vel_y': float, 'estado': str, 'olhando_dir': int,
        #                               'atirando': int, 'vida': int, 'ultimo_sinal': float} }
        self.clientes = {}

    def iniciar(self):
        """Inicia o socket e a thread de escuta UDP."""
        if self.executando:
            return True

        try:
            self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_udp.bind(("0.0.0.0", self.porta))
            self.socket_udp.settimeout(0.5)
            self.executando = True

            self.thread_servidor = threading.Thread(target=self._loop_recepcao, daemon=True)
            self.thread_servidor.start()
            print(f"[Servidor LAN] Hospedado com sucesso na porta {self.porta}.")
            return True
        except Exception as e:
            print(f"[Servidor LAN] Falha ao iniciar: {e}")
            self.executando = False
            return False

    def _loop_recepcao(self):
        """Thread secundária que processa datagramas UDP e faz broadcast."""
        while self.executando:
            try:
                dados, endereco = self.socket_udp.recvfrom(256)
                msg = dados.decode("utf-8").strip()
                agora = time.time()

                partes = msg.split(";")
                if len(partes) >= 8:
                    p_id = partes[0]
                    x = float(partes[1])
                    y = float(partes[2])
                    vel_x = float(partes[3])
                    vel_y = float(partes[4])
                    estado = partes[5]
                    olhando_dir = int(partes[6])
                    atirando = int(partes[7])
                    vida = int(partes[8]) if len(partes) > 8 else 3

                    with self.lock:
                        self.clientes[endereco] = {
                            "id": p_id,
                            "x": x,
                            "y": y,
                            "vel_x": vel_x,
                            "vel_y": vel_y,
                            "estado": estado,
                            "olhando_dir": olhando_dir,
                            "atirando": atirando,
                            "vida": vida,
                            "ultimo_sinal": agora
                        }

                        # Limpeza de jogadores inativos (Timeout 5s)
                        inativos = [
                            end for end, info in self.clientes.items()
                            if agora - info["ultimo_sinal"] > TIMEOUT_JOGADOR_SEGUNDOS
                        ]
                        for inativo in inativos:
                            del self.clientes[inativo]

                        # Prepara pacote de broadcast combinando os jogadores ativos
                        pacotes = []
                        for info in self.clientes.values():
                            pacotes.append(
                                f"{info['id']};{info['x']:.1f};{info['y']:.1f};"
                                f"{info['vel_x']:.1f};{info['vel_y']:.1f};"
                                f"{info['estado']};{info['olhando_dir']};"
                                f"{info['atirando']};{info['vida']}"
                            )
                        msg_broadcast = "|".join(pacotes)

                        # Envia estado do mundo para todos os clientes conectados
                        for dest in self.clientes.keys():
                            try:
                                self.socket_udp.sendto(msg_broadcast.encode("utf-8"), dest)
                            except Exception:
                                pass

            except socket.timeout:
                continue
            except Exception:
                if not self.executando:
                    break

    def parar(self):
        """Encerra o servidor e libera o socket."""
        self.executando = False
        if self.socket_udp:
            try:
                self.socket_udp.close()
            except Exception:
                pass
        print("[Servidor LAN] Finalizado.")


class ClienteLAN:
    """Cliente UDP que se comunica com o Servidor LAN em background."""
    def __init__(self, player_id="byte"):
        self.player_id = player_id
        self.socket_udp = None
        self.ip_servidor = "127.0.0.1"
        self.porta_servidor = PORTA_PADRAO_LAN
        self.conectado = False
        self.executando = False
        self.thread_cliente = None
        self.lock = threading.Lock()
        
        # Dados mais recentes dos jogadores remotos: { 'p_id': {x, y, target_x, target_y, ...} }
        self.jogadores_remotos = {}

    def conectar(self, ip_servidor="127.0.0.1", porta=PORTA_PADRAO_LAN):
        """Inicializa o cliente UDP e conecta ao servidor informado."""
        self.ip_servidor = ip_servidor if ip_servidor.strip() else "127.0.0.1"
        self.porta_servidor = porta

        try:
            self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket_udp.settimeout(0.5)
            self.executando = True
            self.conectado = True

            self.thread_cliente = threading.Thread(target=self._loop_recepcao, daemon=True)
            self.thread_cliente.start()
            print(f"[Cliente LAN] Conectado ao servidor {self.ip_servidor}:{self.porta_servidor} como '{self.player_id}'.")
            return True
        except Exception as e:
            print(f"[Cliente LAN] Erro ao conectar: {e}")
            self.conectado = False
            self.executando = False
            return False

    def enviar_estado(self, x, y, vel_x, vel_y, estado, olhando_dir, atirando, vida):
        """Envia o datagrama de telemetria do jogador local para o servidor."""
        if not self.conectado or not self.socket_udp:
            return

        msg = (
            f"{self.player_id};{x:.1f};{y:.1f};{vel_x:.1f};{vel_y:.1f};"
            f"{estado};{1 if olhando_dir else 0};{1 if atirando else 0};{vida}"
        )
        try:
            self.socket_udp.sendto(msg.encode("utf-8"), (self.ip_servidor, self.porta_servidor))
        except Exception:
            pass

    def _loop_recepcao(self):
        """Thread de escuta que recebe os broadcasts de estado global."""
        while self.executando:
            try:
                dados, _ = self.socket_udp.recvfrom(512)
                msg = dados.decode("utf-8").strip()
                if not msg:
                    continue

                agora = time.time()
                jogadores_str = msg.split("|")

                with self.lock:
                    for j_str in jogadores_str:
                        partes = j_str.split(";")
                        if len(partes) >= 8:
                            remoto_id = partes[0]
                            # Ignora o próprio jogador no pacote de broadcast
                            if remoto_id == self.player_id:
                                continue

                            tx = float(partes[1])
                            ty = float(partes[2])
                            vel_x = float(partes[3])
                            vel_y = float(partes[4])
                            estado = partes[5]
                            olhando_dir = int(partes[6]) == 1
                            atirando = int(partes[7]) == 1
                            vida = int(partes[8]) if len(partes) > 8 else 3

                            if remoto_id not in self.jogadores_remotos:
                                self.jogadores_remotos[remoto_id] = {
                                    "x": tx,
                                    "y": ty,
                                    "target_x": tx,
                                    "target_y": ty,
                                    "vel_x": vel_x,
                                    "vel_y": vel_y,
                                    "estado": estado,
                                    "olhando_dir": olhando_dir,
                                    "atirando": atirando,
                                    "vida": vida,
                                    "ultimo_sinal": agora
                                }
                            else:
                                rem = self.jogadores_remotos[remoto_id]
                                rem["target_x"] = tx
                                rem["target_y"] = ty
                                rem["vel_x"] = vel_x
                                rem["vel_y"] = vel_y
                                rem["estado"] = estado
                                rem["olhando_dir"] = olhando_dir
                                rem["atirando"] = atirando
                                rem["vida"] = vida
                                rem["ultimo_sinal"] = agora

            except socket.timeout:
                continue
            except Exception:
                if not self.executando:
                    break

    def atualizar_lerp(self, fator_lerp=0.25):
        """
        Aplica interpolação linear (LERP) nas posições dos jogadores remotos
        para garantir movimento suave a 60 FPS sem teletransporte.
        """
        agora = time.time()
        with self.lock:
            # Remove parceiros que caíram em timeout
            inativos = [
                r_id for r_id, dados in self.jogadores_remotos.items()
                if agora - dados["ultimo_sinal"] > TIMEOUT_JOGADOR_SEGUNDOS
            ]
            for inativo in inativos:
                del self.jogadores_remotos[inativo]

            # Interpolação suave com teletransporte instantâneo em caso de respawn
            for dados in self.jogadores_remotos.values():
                dx = dados["target_x"] - dados["x"]
                dy = dados["target_y"] - dados["y"]
                if (dx * dx + dy * dy) > 160 * 160:
                    # Salto de respawn: posiciona imediatamente sem deslizar a tela toda
                    dados["x"] = dados["target_x"]
                    dados["y"] = dados["target_y"]
                else:
                    dados["x"] += dx * fator_lerp
                    dados["y"] += dy * fator_lerp

    def obter_jogadores(self):
        """Retorna uma cópia segura dos dados dos jogadores remotos."""
        with self.lock:
            return dict(self.jogadores_remotos)

    def desconectar(self):
        """Finaliza a conexão e fecha a thread."""
        self.executando = False
        self.conectado = False
        if self.socket_udp:
            try:
                self.socket_udp.close()
            except Exception:
                pass
        print("[Cliente LAN] Desconectado.")
