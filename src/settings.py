"""
settings.py - Configuración del juego Julia's Run

📚 PROPÓSITO EDUCATIVO:
Este archivo demuestra la importancia de la ORGANIZACIÓN DEL CÓDIGO.
En lugar de números "mágicos" dispersos por todo el código, 
centralizamos toda la configuración en un solo lugar.

🎯 CONCEPTOS QUE APRENDERÁS:
1. CONSTANTES: Variables que no cambian durante la ejecución
2. NOMBRES DESCRIPTIVOS: PLAYER_SPEED vs speed o s
3. ORGANIZACIÓN: Agrupación lógica por categorías
4. MANTENIMIENTO: Un solo lugar para cambiar configuraciones

💡 VENTAJAS DE ESTA ORGANIZACIÓN:
- ✅ Fácil ajustar velocidades y tamaños
- ✅ No hay números mágicos en el código
- ✅ Otros programadores entienden qué hace cada valor
- ✅ Cambios centralizados afectan todo el juego

🔍 EXPERIMENTO SUGERIDO:
Cambia algunos valores aquí y observa cómo afecta al juego:
- Aumenta PLAYER_SPEED para un juego más rápido
- Cambia OBSTACLE_SPEED para hacerlo más fácil/difícil
- Modifica colores para personalizar el aspecto visual

🤔 PREGUNTA CLAVE:
¿Por qué no poner estos valores directamente en entities.py?
Respuesta: Separación de responsabilidades y facilidad de mantenimiento.
"""

import pygame

# === CONFIGURACIÓN DE VENTANA ===
# 🔍 Mejora sugerida: Estos valores podrían leerse de un archivo de configuración
# Detectar automáticamente la resolución del monitor y ajustar la ventana
# Estrategia (por orden):
# 1. Windows via ctypes GetSystemMetrics (mejor para DPI en Windows)
# 2. Tkinter (multiplataforma, si está disponible)
# 3. pygame.display.Info() (si pygame puede inicializarse)
# 4. Fallback a valores por defecto

# Escala de ventana respecto a la resolución del monitor (para no tapar la barra)
WINDOW_SCALE = 0.95

# Multiplicador global para ajustar la velocidad de todas las entidades
# Úsalo para acelerar/desacelerar el ritmo del juego de forma centralizada
SPEED_MULTIPLIER = 1.5

def _detect_screen_size():
	# 1) Windows via ctypes
	try:
		from ctypes import windll
		user32 = windll.user32
		# Intentar obtener la resolución real en pantallas con DPI scaling
		try:
			user32.SetProcessDPIAware()
		except Exception:
			pass
		w = int(user32.GetSystemMetrics(0))
		h = int(user32.GetSystemMetrics(1))
		if w and h:
			return w, h
	except Exception:
		pass

	# 2) Tkinter
	try:
		import tkinter as tk
		root = tk.Tk()
		root.withdraw()
		w = root.winfo_screenwidth()
		h = root.winfo_screenheight()
		root.destroy()
		if w and h:
			return int(w), int(h)
	except Exception:
		pass

	# 3) pygame
	try:
		import pygame as _pygame
		# Initialize display module temporarily if needed
		if not _pygame.display.get_init():
			_pygame.display.init()
			_inited = True
		else:
			_inited = False
		info = _pygame.display.Info()
		w, h = info.current_w, info.current_h
		if _inited:
			try:
				_pygame.display.quit()
			except Exception:
				pass
		if w and h:
			return int(w), int(h)
	except Exception:
		pass

	# 4) Fallback
	return 800, 600


# Detect and scale
_det_w, _det_h = _detect_screen_size()
WINDOW_WIDTH = max(640, int(_det_w * WINDOW_SCALE))      # Ancho de la ventana en píxeles
WINDOW_HEIGHT = max(480, int(_det_h * WINDOW_SCALE))     # Alto de la ventana en píxeles
FPS = 300               # Cuadros por segundo - ¡Prueba cambiar a 30 o 120!

# === COLORES (formato RGB) ===
# 📚 Los colores se definen como tuplas de 3 valores (Red, Green, Blue)
# Cada valor va de 0 (ausencia) a 255 (máximo)
# 💡 Tip: Usa un color picker online para encontrar nuevos colores
BLACK = (0, 0, 0)          # Ausencia total de color
WHITE = (255, 255, 255)    # Máximo de todos los colores
RED = (255, 0, 0)          # Solo rojo al máximo
GREEN = (0, 255, 0)        # Solo verde al máximo
BLUE = (0, 0, 255)         # Solo azul al máximo
YELLOW = (255, 255, 0)     # Rojo + Verde = Amarillo
GRAY = (128, 128, 128)     # Valor medio de todos
LIGHT_BLUE = (173, 216, 230) # Combinación personalizada
PURPLE = (128, 0, 128)
# Color sangriento para títulos/estética (rojo más oscuro)
BLOOD_RED = (170, 10, 20)

# === CONFIGURACIÓN DEL JUGADOR ===
PLAYER_WIDTH = 40      # Ancho del sprite del jugador
PLAYER_HEIGHT = 60     # Alto del sprite del jugador
PLAYER_SPEED = int(5 * SPEED_MULTIPLIER)       # Velocidad normal de movimiento (píxeles por frame)
PLAYER_LIVES = 3       # Número de vidas iniciales
PLAYER_COLOR = BLUE    # Color del rectángulo del jugador (placeholder)

# Límite máximo de vidas que el jugador puede tener (cap al recoger vida_extra)
MAX_PLAYER_LIVES = 5

# === SISTEMA DE NIVELES ===
# Puntos necesarios para subir un nivel
LEVEL_UP_SCORE = 100
# Máximo nivel alcanzable
MAX_LEVEL = 20
# Bonus de dificultad por nivel (se suma a difficulty multiplier por nivel)
LEVEL_DIFFICULTY_BONUS = 0.1

# Posición inicial del jugador (centrado en la parte inferior)
PLAYER_START_X = WINDOW_WIDTH // 2 - PLAYER_WIDTH // 2
PLAYER_START_Y = WINDOW_HEIGHT - PLAYER_HEIGHT - 20

# === CONFIGURACIÓN DE CUCHILLOS ===
KNIFE_WIDTH = 8        # Ancho del cuchillo
KNIFE_HEIGHT = 20      # Alto del cuchillo
KNIFE_SPEED = int(10 * SPEED_MULTIPLIER)       # Velocidad del cuchillo (píxeles por frame)
KNIFE_COLOR = YELLOW   # Color del cuchillo
KNIFE_COOLDOWN = 30    # Tiempo de cooldown en frames (0.5 segundos a 60 FPS)

# === CONFIGURACIÓN DE OBSTÁCULOS ===
OBSTACLE_WIDTH = 30    # Ancho del obstáculo
OBSTACLE_HEIGHT = 30   # Alto del obstáculo
OBSTACLE_SPEED = int(3 * SPEED_MULTIPLIER)     # Velocidad de caída (píxeles por frame)
OBSTACLE_COLOR = RED   # Color del obstáculo
OBSTACLE_SPAWN_RATE = 60  # Frames entre spawn de obstáculos (1 segundo a 60 FPS)

# === CONFIGURACIÓN DE POWER-UPS ===
POWERUP_WIDTH = 25     # Ancho del power-up
POWERUP_HEIGHT = 25    # Alto del power-up
POWERUP_SPEED = int(2 * SPEED_MULTIPLIER)      # Velocidad de caída (más lento que obstáculos)
POWERUP_SPAWN_RATE = 300  # Frames entre spawn de power-ups (5 segundos a 60 FPS)

# Colores de power-ups
VODKA_COLOR = PURPLE   # Vodka Boost - color morado
TEA_COLOR = GREEN      # Té Mágico - color verde

# Duración de efectos (en frames)
VODKA_DURATION = 180   # 3 segundos a 60 FPS
TEA_DURATION = 240     # 4 segundos a 60 FPS

# Multiplicadores de efectos
VODKA_SPEED_MULTIPLIER = 1.5  # El jugador se mueve 50% más rápido

# === CONFIGURACIÓN DE PUNTUACIÓN ===
POINTS_PER_OBSTACLE_AVOIDED = 1    # Puntos por esquivar obstáculo
POINTS_PER_OBSTACLE_DESTROYED = 5  # Puntos por destruir obstáculo con cuchillo
POINTS_PER_POWERUP = 10           # Puntos por recoger power-up

# === CONFIGURACIÓN DE ARCHIVOS ===
SCORE_FILE = "best_score.json"    # Archivo donde se guarda el récord

# === TECLAS DEL JUEGO ===
# Estas constantes se usan para hacer el código más legible
# En lugar de usar números mágicos, usamos nombres descriptivos
# Constantes de teclas
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
KEY_UP = pygame.K_UP
KEY_DOWN = pygame.K_DOWN
KEY_SPACE = pygame.K_SPACE
KEY_ENTER = pygame.K_RETURN
KEY_ESCAPE = pygame.K_ESCAPE
KEY_P = pygame.K_p

# WASD keys (alternative movement keys)
KEY_W = pygame.K_w
KEY_A = pygame.K_a
KEY_S = pygame.K_s
KEY_D = pygame.K_d

# === CONFIGURACIÓN DE ESTADOS DEL JUEGO ===
# Estos son los diferentes estados o pantallas del juego
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_PAUSED = "paused"  # ✅ IMPLEMENTADO: Estado de pausa
STATE_CONFIRM_EXIT = "confirm_exit"  # Estado para confirmar salida

# === CONFIGURACIÓN DE FUENTES ===
FONT_SIZE_LARGE = 48   # Tamaño de fuente para títulos
FONT_SIZE_MEDIUM = 24  # Tamaño de fuente para texto normal
FONT_SIZE_SMALL = 16   # Tamaño de fuente para detalles

# === CONFIGURACIÓN DE BOTONES / UI ===
# Estética de los botones: radio, sombra, grosor del borde
BUTTON_RADIUS = 8                  # Radio de las esquinas redondeadas
BUTTON_SHADOW_COLOR = (30, 30, 30, 120)  # Sombra (RGBA), usaremos solo RGB al dibujar
BUTTON_SHADOW_OFFSET = 4           # Offset de la sombra en píxeles
BUTTON_BORDER_WIDTH = 2            # Ancho del borde del botón
BUTTON_PADDING_X = 12              # Padding horizontal para el texto dentro del botón
BUTTON_PADDING_Y = 6               # Padding vertical para el texto dentro del botón
BUTTON_HOVER_COLOR = (255, 250, 140)  # Color de fondo al hacer hover/seleccionar (ligeramente más suave que YELLOW)

# ✅ IMPLEMENTADO: Configuración para barra de cooldown
COOLDOWN_BAR_WIDTH = 100   # Ancho de la barra de cooldown en píxeles
COOLDOWN_BAR_HEIGHT = 10   # Alto de la barra de cooldown en píxeles
COOLDOWN_BAR_X = 10        # Posición X de la barra de cooldown
COOLDOWN_BAR_Y = 100       # Posición Y de la barra de cooldown

# ✅ IMPLEMENTADO: Configuración para dificultad progresiva
DIFFICULTY_INCREASE_INTERVAL = 10  # Cada cuántos puntos aumenta la dificultad
MAX_OBSTACLE_SPEED = 8             # Velocidad máxima de obstáculos
SPEED_INCREASE_RATE = 0.5          # Cuánto aumenta la velocidad por nivel
MAX_SPAWN_RATE_REDUCTION = 30      # Máxima reducción en frames de spawn

# ✅ IMPLEMENTADO: Configuración de efectos visuales
PARTICLE_COUNT = 15                # Número de partículas en explosión
PARTICLE_LIFE = 30                 # Vida de partículas en frames
SCREEN_SHAKE_INTENSITY = 5         # Intensidad del screen shake
SCREEN_SHAKE_DURATION = 10         # Duración del screen shake en frames

# ✅ IMPLEMENTADO: Configuración de animaciones
SPRITE_ANIMATION_SPEED = 8         # Frames entre cambios de sprite
POWERUP_PULSE_SPEED = 4           # Velocidad del efecto de pulso en power-ups

# TODO 4: Añadir rutas de assets cuando estén disponibles
# SPRITE_JULIA = "assets/sprites/julia.png"
# SPRITE_KNIFE = "assets/sprites/knife.png"
# SPRITE_POWERUP = "assets/sprites/powerup.png"
# SOUND_THROW = "assets/sounds/throw.wav"
# SOUND_HIT = "assets/sounds/hit.wav"
# SOUND_POWERUP = "assets/sounds/powerup.wav"

# === RUTAS DE ASSETS PARA ICONOS DE CONTROLES ===
# Carpeta donde poner iconos opcionales (PNG). Ejemplos de nombres esperados:
# - assets/icons/controller_xbox.png
# - assets/icons/controller_playstation.png
# - assets/icons/controller_generic.png
# - assets/icons/keyboard_arrows.png
# - assets/icons/mouse.png
INPUT_ICON_DIR = "assets/icons"
# Tamaño por defecto para los iconos (píxeles)
INPUT_ICON_SIZE = 48

# === NOTAS EDUCATIVAS ===
"""
¿Por qué usar constantes?
1. Facilita el ajuste de valores sin buscar en todo el código
2. Evita errores por escribir mal un número
3. Hace el código más legible y mantenible
4. Permite experimentar con diferentes valores fácilmente

Ejemplo: Si queremos hacer el juego más difícil, solo cambiamos
OBSTACLE_SPEED de 3 a 4, en lugar de buscar todos los lugares
donde aparece el número 3 en el código.

Convenciones de nombres:
- MAYÚSCULAS_CON_GUIONES_BAJOS para constantes
- minúsculas_con_guiones_bajos para variables
- CamelCase para nombres de clases
"""

# === CONFIGURACIÓN DE JOYSTICK / GAMEPAD ===
# Valores por defecto para soporte de gamepad/joystick
JOYSTICK_DEADZONE = 0.3          # Zona muerta para ejes Analógicos
JOYSTICK_BUTTON_SHOOT = 0        # Botón por defecto para disparo (A en muchos pads)
JOYSTICK_BUTTON_PAUSE = 7        # Botón por defecto para pausa (Start / Options)

# === OPCIONES DE RATÓN ===
# Habilita control del jugador con el ratón (mover hacia la posición X del cursor)
MOUSE_CONTROL_ENABLED = False
# Distancia mínima para considerar que el ratón está a la izquierda/derecha
MOUSE_MOVE_THRESHOLD = 8

# === CONFIGURACIÓN DE FONDO ===
# 'cover' hace crop para llenar la ventana sin estirar
# 'contain' ajusta la imagen al tamaño sin recortar (añade letterbox)
BACKGROUND_MODE = 'cover'  # 'cover' | 'contain'

# === CONFIGURACIÓN DE SONIDOS (RUTAS Y VOLUMEN POR DEFECTO) ===
# Usar archivos reales .wav/.ogg cuando estén disponibles; por ahora placeholders
SFX_VOLUME = 0.9
SOUND_THROW = "assets/sounds/throw_placeholder.txt"
SOUND_HIT = "assets/sounds/hit_placeholder.txt"
SOUND_POWERUP = "assets/sounds/powerup_placeholder.txt"
