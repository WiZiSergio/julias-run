import pygame
from src.entities import Player, Obstacle

pygame.init()

print("Creando dos jugadores para demostrar objetos:")
david = Player()
wizi = Player()
print(f"David vidas: {david.lives}")
print(f"Wizi vidas: {wizi.lives}")

# Simular daño en uno
if hasattr(david, 'take_damage'):
    david.take_damage()
    print("Después de take_damage() en david:")
    print(f"david vidas: {david.lives}")
    print(f"wizi vidas: {wizi.lives}")
else:
    print("El método take_damage() no existe en Player en esta versión.")

# Crear obstáculos de diferente dificultad
obs1 = Obstacle(1.0)
obs2 = Obstacle(2.0)
print(f"Obstacle1 speed (approx): {getattr(obs1, 'speed', 'n/a')}")
print(f"Obstacle2 speed (approx): {getattr(obs2, 'speed', 'n/a')}")

pygame.quit()
