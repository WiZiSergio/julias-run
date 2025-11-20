import pygame
import random
from settings import *

class EnemigoEspecial:
    """
    Un enemigo que se mueve de forma diferente a los obstáculos normales.
    """

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed_x = random.choice([-2, 2])
        self.speed_y = 3
        self.color = (255, 100, 255)
        self.lives = 2

    def update(self):
        # Movimiento zigzag
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Rebotar en bordes
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.speed_x *= -1

        # Devolver si sigue visible
        return self.rect.top < WINDOW_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Indicador de vidas arriba
        for i in range(self.lives):
            pygame.draw.circle(screen, WHITE, (self.rect.centerx - 10 + i*10, self.rect.top - 5), 3)

    def take_damage(self):
        self.lives -= 1
        return self.lives > 0
