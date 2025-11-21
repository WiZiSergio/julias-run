import pygame
import random
from settings import *

class EnemigoEspecial:
    """
    Un enemigo especial con movimiento en zigzag.

    Se adapta para ser compatible con la interfaz usada por el juego:
    - __init__(player_x, difficulty)
    - update(player_x) -> bool
    - draw(screen)
    - take_damage()
    """

    def __init__(self, player_x, difficulty_multiplier=1.0):
        # Aparecer ligeramente alejado del jugador en X
        start_x = max(10, min(WINDOW_WIDTH - 50, player_x + random.randint(-120, 120)))
        start_y = -50
        self.rect = pygame.Rect(start_x, start_y, 60, 60)
        self.speed_x = random.choice([-2, 2])
        # Velocidad vertical escala con la dificultad
        self.speed_y = int(3 * max(1.0, difficulty_multiplier))
        self.color = (255, 100, 255)
        self.lives = 2
        self.pulse_timer = 0

    def update(self, player_x=None):
        """
        Movimiento zigzag; acepta player_x opcional para compatibilidad.

        Returns:
            bool: True si sigue visible, False si salió de pantalla
        """
        # Movimiento zigzag
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Rebotar en bordes
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.speed_x *= -1

        # Si se pasa abajo, ya no está visible
        return self.rect.top < WINDOW_HEIGHT

    def draw(self, screen):
        # Pulsing visual
        self.pulse_timer += 1
        pulse_offset = int(abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 4).x) * 20)
        pulse_color = tuple(min(255, max(0, c + pulse_offset)) for c in self.color)
        pygame.draw.rect(screen, pulse_color, self.rect)
        # Indicador de vidas arriba
        for i in range(self.lives):
            pygame.draw.circle(screen, WHITE, (self.rect.centerx - 10 + i * 10, self.rect.top - 5), 3)

    def take_damage(self):
        self.lives -= 1
        return self.lives > 0
