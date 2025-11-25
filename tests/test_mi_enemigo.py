import pygame
from src.mi_enemigo import EnemigoEspecial

pygame.init()
screen = pygame.display.set_mode((800, 200))
clock = pygame.time.Clock()

mi_enemigo = EnemigoEspecial(400, 50)

running = True
frames = 0
while running and frames < 300:  # Run a short demo for ~5 seconds at 60fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mi_enemigo.update()
    screen.fill((0, 0, 0))
    mi_enemigo.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    frames += 1

pygame.quit()
print("Demo finished.")
