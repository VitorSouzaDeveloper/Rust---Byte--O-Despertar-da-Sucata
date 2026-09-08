import pygame

# Inicializa o Pygame
pygame.init()
tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Exemplo de Máscara no Pygame")

# Cria superfícies de exemplo (substitua por imagens reais com .png transparente)
surf1 = pygame.Surface((50, 50), pygame.SRCALPHA)
rect1 = surf1.get_frect()
#pygame.draw.rect(surf1, (0,0,0), rect1, 5)
pygame.draw.circle(surf1, (255, 0, 0), (25, 25), 25)  # Círculo vermelho

surf2 = pygame.Surface((50, 50), pygame.SRCALPHA)
#pygame.draw.rect(surf2, (0, 0, 255), (0, 0, 50, 50))  # Retângulo azul
rect2 = surf2.get_frect()
#pygame.draw.rect(surf2, (0,0,0), rect2, 5)
pygame.draw.circle(surf2, (0, 0, 255), (25, 25), 25)  # Círculo azul

# Posições iniciais
pos1 = pygame.math.Vector2(100, 100)
pos2 = pygame.math.Vector2(120, 120)

# Cria as máscaras a partir das superfícies
mascara1 = pygame.mask.from_surface(surf1)
mascara2 = pygame.mask.from_surface(surf2)

# Loop principal do jogo
rodando = True
relogio = pygame.time.Clock()

while rodando:
  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      rodando = False

  # Movimenta o primeiro objeto com as setas do teclado
  teclas = pygame.key.get_pressed()
  if teclas[pygame.K_LEFT]:
    pos1.x -= 3
  if teclas[pygame.K_RIGHT]:
    pos1.x += 3
  if teclas[pygame.K_UP]:
    pos1.y -= 3
  if teclas[pygame.K_DOWN]:
    pos1.y += 3

  # Calcula o deslocamento (offset) entre as duas posições
  deslocamento = (int(pos2.x - pos1.x), int(pos2.y - pos1.y))

  # Verifica a colisão pixel a pixel usando overlap
  # Retorna um ponto de colisão se houver interseção, ou None caso contrário
  colisao = mascara1.overlap(mascara2, deslocamento)
  
  if colisao:
    cor_fundo = (50, 0, 0)  # Vermelho escuro se colidir
  else:
    cor_fundo = (30, 30, 30)  # Cinza normal

  # Atualiza a tela
  tela.fill(cor_fundo)
  tela.blit(surf1, pos1)
  tela.blit(surf2, pos2)

  pygame.display.flip()
  relogio.tick(60)

pygame.quit()
