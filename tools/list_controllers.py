"""List controllers debug tool.

Detecta joysticks vía pygame.joystick y también intenta listar controladores
usando pygame._sdl2.controller cuando esté disponible (pygame-ce). Imprime
información detallada para diagnosticar por qué un mando Xbox/USB no aparece.

Ejecutar:
    python tools/list_controllers.py
"""
import pygame
import sys

pygame.init()
print("Pygame:", pygame)
print("SDL version:", pygame.get_sdl_version())

# Joysticks (legacy SDL_Joystick)
pygame.joystick.init()
count = pygame.joystick.get_count()
print(f"pygame.joystick.get_count() = {count}")
for i in range(count):
    j = pygame.joystick.Joystick(i)
    j.init()
    try:
        num_buttons = j.get_numbuttons()
    except Exception:
        try:
            num_buttons = j.get_button_count()
        except Exception:
            num_buttons = '?'
    try:
        num_axes = j.get_numaxes()
    except Exception:
        num_axes = '?'
    try:
        num_hats = j.get_numhats()
    except Exception:
        num_hats = '?'
    print(f"  #{i}: name={j.get_name()}, buttons={num_buttons}, axes={num_axes}, hats={num_hats}")

# Try SDL2 controller API (pygame-ce)
print("\nIntentando pygame._sdl2.controller (GameController API) ...")
try:
    from pygame._sdl2 import controller as sdl2controller
    try:
        # Algunos builds requieren inicializar explicitamente el subsistema de controllers
        if hasattr(sdl2controller, 'init'):
            try:
                sdl2controller.init()
            except Exception:
                pass
    except Exception:
        pass
    s_count = sdl2controller.get_count()
    print(f"sdl2 controller count = {s_count}")
    for i in range(s_count):
        try:
            c = sdl2controller.Controller(i)
            print(f"  #{i}: name={c.name}, id={c.get_id()}, type={c.get_type() if hasattr(c,'get_type') else 'N/A'}")
        except Exception as e:
            print(f"  error listing sdl2 controller #{i}: {e}")
except Exception as e:
    print("  pygame._sdl2.controller unavailable or error:", e)

pygame.quit()

print('\nDone')

if __name__ == '__main__':
    pass
