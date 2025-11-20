"""
Monitor simple de joysticks usando pygame.
Muestra el conteo actual y cualquier evento JOYDEVICEADDED / JOYDEVICEREMOVED en tiempo real.

Ejecuta en PowerShell:
    python tools/monitor_joysticks.py

Mientras el script corre, conecta o desconecta el mando USB y observa la salida.
"""
import time
import pygame

pygame.init()
pygame.joystick.init()

print("Starting joystick monitor. Press Ctrl+C to stop.")
try:
    last_count = -1
    while True:
        # Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                print(f"Event: JOYDEVICEADDED - device_index={getattr(event, 'device_index', 'N/A')}")
            elif event.type == pygame.JOYDEVICEREMOVED:
                print(f"Event: JOYDEVICEREMOVED - joy={getattr(event, 'joy', 'N/A')}")
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Event: JOYBUTTONDOWN - joy={event.joy} button={event.button}")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Event: JOYBUTTONUP - joy={event.joy} button={event.button}")

        count = pygame.joystick.get_count()
        if count != last_count:
            print(f"Joystick count: {count}")
            for i in range(count):
                j = pygame.joystick.Joystick(i)
                try:
                    name = j.get_name()
                except Exception:
                    name = '<unknown>'
                try:
                    axes = j.get_numaxes()
                except Exception:
                    axes = '?'
                try:
                    buttons = j.get_numbuttons()
                except Exception:
                    buttons = '?'
                try:
                    hats = j.get_numhats()
                except Exception:
                    hats = '?'
                print(f"  #{i}: name={name}, axes={axes}, buttons={buttons}, hats={hats}")
            last_count = count

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopped by user")
finally:
    pygame.quit()
