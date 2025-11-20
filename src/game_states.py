"""
game_states.py - Estados del juego Julia's Run

Este archivo gestiona los diferentes estados o pantallas del juego:
- Menú principal
- Jugando
- Game Over
- Pausa (TODO)

Conceptos de programación cubiertos:
- Máquina de estados
- Gestión de eventos
- Renderizado condicional
- Flujo de control del programa

Referencias útiles:
- pygame.font: https://www.pygame.org/docs/ref/font.html
- pygame.event: https://www.pygame.org/docs/ref/event.html
"""

import pygame
from settings import *
from utils import get_input_icon_surface, get_current_input

class GameStateManager:
    """
    Esta clase gestiona los diferentes estados del juego.
    
    Un juego típicamente tiene varios estados o pantallas:
    - Menú principal
    - Gameplay
    - Game Over
    - Pausa
    
    Esta clase se encarga de cambiar entre estos estados y
    asegurarse de que solo uno esté activo a la vez.
    """
    
    def __init__(self):
        """Constructor del gestor de estados."""
        self.current_state = STATE_MENU
        self.next_state = None
        
        # Inicializar fuentes para texto
        pygame.font.init()
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
    
    def change_state(self, new_state):
        """
        Cambia a un nuevo estado.
        
        Args:
            new_state: El nuevo estado (ver constantes en settings.py)
        """
        self.next_state = new_state
    
    def update_state(self):
        """Actualiza el estado actual si hay un cambio pendiente."""
        if self.next_state:
            self.current_state = self.next_state
            self.next_state = None
    
    def get_current_state(self):
        """Obtiene el estado actual."""
        return self.current_state


class MenuState:
    """
    Estado del menú principal.
    
    Muestra el título del juego, instrucciones básicas y
    espera a que el jugador presione una tecla para empezar.
    """
    
    def __init__(self, state_manager):
        """
        Constructor del estado de menú.
        
        Args:
            state_manager: Referencia al gestor de estados
        """
        self.state_manager = state_manager
        # 0 = Start, 1 = Exit
        self.selection = 0
    
    def handle_events(self, events):
        """
        Maneja los eventos del menú.
        
        Args:
            events: Lista de eventos de pygame
        """
        # Ensure rects exist even if draw() hasn't been called yet this frame
        if not hasattr(self, 'start_button_rect') or not hasattr(self, 'exit_button_rect'):
            try:
                self._compute_menu_button_rects()
            except Exception:
                pass

        # Ensure restart/exit rects exist before handling mouse events
        if not hasattr(self, 'restart_rect') or not hasattr(self, 'exit_rect'):
            try:
                self._compute_gameover_rects()
            except Exception:
                pass

        # Ensure yes/no rects exist for mouse handling
        if not hasattr(self, 'yes_rect') or not hasattr(self, 'no_rect'):
            try:
                self._compute_confirm_rects()
            except Exception:
                pass

        for event in events:
            # Keyboard navigation
            if event.type == pygame.KEYDOWN:
                if event.key in (KEY_LEFT, pygame.K_a):
                    self.selection = max(0, self.selection - 1)
                elif event.key in (KEY_RIGHT, pygame.K_d):
                    self.selection = min(1, self.selection + 1)
                elif event.key == KEY_SPACE or event.key == KEY_ENTER:
                    # Activate based on current selection
                    if self.selection == 0:
                        self.state_manager.change_state(STATE_PLAYING)
                    else:
                        self.state_manager.change_state(STATE_CONFIRM_EXIT)
                        return True
                elif event.key == KEY_ESCAPE:
                    # Abrir diálogo de confirmación antes de salir
                    self.state_manager.change_state(STATE_CONFIRM_EXIT)
                    return True

            # Joystick navigation (hat/axes)
            elif event.type == pygame.JOYHATMOTION:
                try:
                    hat_x, hat_y = event.value
                    if hat_x < 0:
                        self.selection = 0
                    elif hat_x > 0:
                        self.selection = 1
                except Exception:
                    pass
            elif event.type == pygame.JOYAXISMOTION:
                try:
                    if event.axis == 0:
                        if event.value < -JOYSTICK_DEADZONE:
                            self.selection = 0
                        elif event.value > JOYSTICK_DEADZONE:
                            self.selection = 1
                except Exception:
                    pass

            # Joystick buttons: A / primary to activate, Pause/Start to open confirm
            elif event.type == pygame.JOYBUTTONDOWN:
                try:
                    button = event.button
                except AttributeError:
                    button = None

                try:
                    from settings import JOYSTICK_BUTTON_SHOOT, JOYSTICK_BUTTON_PAUSE
                except Exception:
                    JOYSTICK_BUTTON_SHOOT = None
                    JOYSTICK_BUTTON_PAUSE = None

                if button == JOYSTICK_BUTTON_SHOOT:
                    # Activate current selection
                    if self.selection == 0:
                        self.state_manager.change_state(STATE_PLAYING)
                    else:
                        self.state_manager.change_state(STATE_CONFIRM_EXIT)
                        return True
                elif button == JOYSTICK_BUTTON_PAUSE:
                    # Treat pause/options button as "open confirm exit" from menu
                    self.state_manager.change_state(STATE_CONFIRM_EXIT)
                    return True

            # Mouse: hover changes selection, click activates
            elif event.type == pygame.MOUSEMOTION:
                try:
                    pos = event.pos
                except Exception:
                    pos = pygame.mouse.get_pos()
                # compute rects if missing
                if not hasattr(self, 'start_button_rect') or not hasattr(self, 'exit_button_rect'):
                    try:
                        self._compute_menu_button_rects()
                    except Exception:
                        pass
                if self.start_button_rect.collidepoint(pos):
                    self.selection = 0
                elif self.exit_button_rect.collidepoint(pos):
                    self.selection = 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    pos = event.pos
                except Exception:
                    pos = pygame.mouse.get_pos()

                # ensure rects
                if not hasattr(self, 'start_button_rect') or not hasattr(self, 'exit_button_rect'):
                    try:
                        self._compute_menu_button_rects()
                    except Exception:
                        pass

                if self.start_button_rect.collidepoint(pos):
                    self.state_manager.change_state(STATE_PLAYING)
                if self.exit_button_rect.collidepoint(pos):
                    self.state_manager.change_state(STATE_CONFIRM_EXIT)
                    return True
        
        return True  # Continuar ejecutando
    
    def update(self):
        """Actualiza la lógica del menú (no hay mucho que hacer aquí)."""
        pass
    
    def draw(self, screen):
        """
        Dibuja el menú principal.
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        
        # Limpiar pantalla con color de fondo
        screen.fill(LIGHT_BLUE)
        
        # Título del juego
        title_text = self.state_manager.font_large.render("Julia's Run", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, 150))
        screen.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = self.state_manager.font_medium.render("🏃‍♀️🔪 Aventura Épica", True, PURPLE)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH//2, 200))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Modern instructions panel
        panel_w = 560
        panel_h = 160
        panel_x = WINDOW_WIDTH // 2 - panel_w // 2
        panel_y = 260

        # Panel shadow
        try:
            panel_shadow = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel_shadow.fill(BUTTON_SHADOW_COLOR)
            screen.blit(panel_shadow, (panel_x + BUTTON_SHADOW_OFFSET, panel_y + BUTTON_SHADOW_OFFSET))
        except Exception:
            pass

        # Panel background (translucent white with rounded corners)
        try:
            panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel_surf.fill((250, 250, 250, 230))
            screen.blit(panel_surf, (panel_x, panel_y))
        except Exception:
            pygame.draw.rect(screen, WHITE, pygame.Rect(panel_x, panel_y, panel_w, panel_h))

        # Panel border
        pygame.draw.rect(screen, BLACK, pygame.Rect(panel_x, panel_y, panel_w, panel_h), BUTTON_BORDER_WIDTH, BUTTON_RADIUS)

        # Header
        header = self.state_manager.font_medium.render("Controles", True, BLACK)
        header_rect = header.get_rect(topleft=(panel_x + 20, panel_y + 12))
        screen.blit(header, header_rect)

        # Icon representing current input method (controller / keyboard / mouse)
        try:
            inp = get_current_input()
            icon = get_input_icon_surface(inp.get('type'), inp.get('controller_name'), size=40)
            if icon:
                icon_x = panel_x + panel_w - 20 - icon.get_width()
                icon_y = panel_y + 12
                screen.blit(icon, (icon_x, icon_y))
            else:
                # Fallback: render small label indicating input
                label = inp.get('type', 'teclado')
                name_txt = self.state_manager.font_small.render(label.upper(), True, GRAY)
                name_rect = name_txt.get_rect(topright=(panel_x + panel_w - 12, panel_y + 14))
                screen.blit(name_txt, name_rect)
        except Exception:
            pass

        # Modern bullet list of controls
        controls = [
            ("Flechas / A D", "Mover"),
            ("Espacio", "Lanzar cuchillo"),
            ("Esquiva", "Obstáculos rojos"),
            ("Recoge", "Power-ups de colores"),
        ]

        for idx, (left, right) in enumerate(controls):
            y = panel_y + 50 + idx * 26
            # small colored icon
            icon_x = panel_x + 28
            icon_y = y + 8
            pygame.draw.circle(screen, PURPLE, (icon_x, icon_y), 6)

            left_text = self.state_manager.font_small.render(left, True, BLACK)
            right_text = self.state_manager.font_small.render(right, True, GRAY)

            screen.blit(left_text, (icon_x + 16, y))
            screen.blit(right_text, (panel_x + panel_w - 20 - right_text.get_width(), y))

        # Set start_y for buttons below the panel
        start_y = panel_y + panel_h + 20
        # Ensure rects are computed for use by events
        try:
            self._compute_menu_button_rects(start_y=start_y)
        except Exception:
            pass
        # Draw Start and Exit buttons below the panel
        start_w, start_h = 300, 44
        exit_w, exit_h = 160, 44
        spacing = 28

        total_w = start_w + spacing + exit_w
        start_x = WINDOW_WIDTH // 2 - total_w // 2
        exit_x = start_x + start_w + spacing

        start_btn = pygame.Rect(start_x, start_y, start_w, start_h)
        exit_btn = pygame.Rect(exit_x, start_y, exit_w, exit_h)

        # Shadows
        try:
            s1 = pygame.Surface((start_w, start_h), pygame.SRCALPHA)
            s1.fill(BUTTON_SHADOW_COLOR)
            screen.blit(s1, (start_x + BUTTON_SHADOW_OFFSET, start_y + BUTTON_SHADOW_OFFSET))
            s2 = pygame.Surface((exit_w, exit_h), pygame.SRCALPHA)
            s2.fill(BUTTON_SHADOW_COLOR)
            screen.blit(s2, (exit_x + BUTTON_SHADOW_OFFSET, start_y + BUTTON_SHADOW_OFFSET))
        except Exception:
            pass

        # Backgrounds and borders
        if getattr(self, 'selection', 0) == 0:
            start_bg = BUTTON_HOVER_COLOR
            start_text_color = BLACK
            start_border = YELLOW
        else:
            start_bg = BLACK
            start_text_color = WHITE
            start_border = WHITE

        if getattr(self, 'selection', 0) == 1:
            exit_bg = BUTTON_HOVER_COLOR
            exit_text_color = BLACK
            exit_border = YELLOW
        else:
            exit_bg = BLACK
            exit_text_color = WHITE
            exit_border = WHITE

        pygame.draw.rect(screen, start_bg, start_btn, 0, BUTTON_RADIUS)
        pygame.draw.rect(screen, start_border, start_btn, BUTTON_BORDER_WIDTH, BUTTON_RADIUS)
        pygame.draw.rect(screen, exit_bg, exit_btn, 0, BUTTON_RADIUS)
        pygame.draw.rect(screen, exit_border, exit_btn, BUTTON_BORDER_WIDTH, BUTTON_RADIUS)

        # Labels
        start_label = self.state_manager.font_small.render("COMENZAR", True, start_text_color)
        exit_label = self.state_manager.font_small.render("SALIR", True, exit_text_color)

        screen.blit(start_label, start_label.get_rect(center=start_btn.center))
        screen.blit(exit_label, exit_label.get_rect(center=exit_btn.center))

        # Save rects for interaction
        self.start_button_rect = start_btn
        self.exit_button_rect = exit_btn

        # Update selection from current mouse position (so hover works even without motion events)
        try:
            mpos = pygame.mouse.get_pos()
            if self.start_button_rect.collidepoint(mpos):
                self.selection = 0
            elif self.exit_button_rect.collidepoint(mpos):
                self.selection = 1
        except Exception:
            pass
    def _compute_menu_button_rects(self, start_y=None):
        """Compute and store menu button rects deterministically for event handling.

        If start_y is provided it will use that vertical position; otherwise
        it will recompute based on the same panel layout used in draw().
        """
        panel_w = 560
        panel_h = 160
        panel_x = WINDOW_WIDTH // 2 - panel_w // 2
        panel_y = 260
        if start_y is None:
            start_y = panel_y + panel_h + 20

        start_w, start_h = 300, 44
        exit_w, exit_h = 160, 44
        spacing = 28
        total_w = start_w + spacing + exit_w
        start_x = WINDOW_WIDTH // 2 - total_w // 2
        exit_x = start_x + start_w + spacing

        self.start_button_rect = pygame.Rect(start_x, start_y, start_w, start_h)
        self.exit_button_rect = pygame.Rect(exit_x, start_y, exit_w, exit_h)
        
    # TODO 9: Añadir demo visual o animación de fondo
    # self.draw_background_animation(screen)


class PlayingState:
    """
    Estado principal del juego.
    
    Este es el estado donde ocurre toda la acción:
    - El jugador se mueve y lanza cuchillos
    - Aparecen obstáculos y power-ups
    - Se detectan colisiones
    - Se actualiza la puntuación
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de juego."""
        self.state_manager = state_manager
    
    def handle_events(self, events, player, knife_cooldown):
        """
        Maneja los eventos durante el juego.
        
        Args:
            events: Lista de eventos de pygame
            player: Instancia del jugador
            knife_cooldown: Timer de cooldown para cuchillos
            
        Returns:
            list: Lista de nuevos cuchillos creados (si se lanzó alguno)
        """
        
        new_knives = []
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_SPACE:
                    # Lanzar cuchillo si no hay cooldown
                    if knife_cooldown.is_ready():
                        from entities import Knife  # Import local para evitar circular
                        new_knife = Knife(player.rect)
                        new_knives.append(new_knife)
                        knife_cooldown.start_cooldown()
                        
                        # TODO 4: Añadir sonido de lanzamiento
                        # pygame.mixer.Sound(SOUND_THROW).play()
                
                elif event.key == KEY_P:
                    # ✅ IMPLEMENTADO: Implementar pausa
                    self.state_manager.change_state(STATE_PAUSED)
                    print("Juego pausado")  # Debug
                elif event.key == KEY_ESCAPE:
                    # No cerrar el juego al pulsar ESC durante la partida: abrir pausa
                    self.state_manager.change_state(STATE_PAUSED)
                    print("Juego pausado (ESC)")
                    # Seguir ejecutando (no salir)
                    
            # Soporte de joystick: botones que emulan KEYDOWN
            elif event.type == pygame.JOYBUTTONDOWN:
                # Mapear botón de joystick a acciones
                try:
                    button = event.button
                except AttributeError:
                    button = None

                # Disparar con el botón configurado
                from settings import JOYSTICK_BUTTON_SHOOT, JOYSTICK_BUTTON_PAUSE
                if button == JOYSTICK_BUTTON_SHOOT:
                    if knife_cooldown.is_ready():
                        from entities import Knife
                        new_knife = Knife(player.rect)
                        new_knives.append(new_knife)
                        knife_cooldown.start_cooldown()

                # Pausar con el botón configurado
                if button == JOYSTICK_BUTTON_PAUSE:
                    self.state_manager.change_state(STATE_PAUSED)
                    print("Juego pausado (joystick)")
        
        return new_knives, True  # Continuar jugando
    
    def update(self, player, obstacles, knives, powerups, effects, knife_cooldown):
        """
        Actualiza toda la lógica del juego.
        
        Args:
            player: Instancia del jugador
            obstacles: Lista de obstáculos
            knives: Lista de cuchillos
            powerups: Lista de power-ups
            effects: Sistema de efectos de power-ups
            knife_cooldown: Timer de cooldown
            
        Returns:
            bool: True si el jugador sigue vivo, False si Game Over
        """
        
        # Actualizar timers
        knife_cooldown.update()
        effects.update(player)
        
        # Mover jugador según teclas presionadas
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # Actualizar obstáculos
        for obstacle in obstacles[:]:  # [:] crea una copia para iterar seguro
            if not obstacle.update():
                # Obstáculo salió de pantalla - dar puntos por esquivar
                obstacles.remove(obstacle)
                player.score += POINTS_PER_OBSTACLE_AVOIDED
        
        # Actualizar cuchillos
        for knife in knives[:]:
            if not knife.update():
                knives.remove(knife)
        
        # Actualizar power-ups
        for powerup in powerups[:]:
            if not powerup.update():
                powerups.remove(powerup)
        
        # Detectar colisiones jugador-obstáculos
        for obstacle in obstacles[:]:
            if player.rect.colliderect(obstacle.rect):
                obstacles.remove(obstacle)
                if not player.take_damage():
                    # Game Over
                    return False
                
                # TODO 4: Añadir sonido de daño
                # pygame.mixer.Sound(SOUND_HIT).play()
        
        # Detectar colisiones cuchillo-obstáculos
        for knife in knives[:]:
            for obstacle in obstacles[:]:
                if knife.rect.colliderect(obstacle.rect):
                    # Destruir ambos y dar puntos
                    knives.remove(knife)
                    obstacles.remove(obstacle)
                    player.score += POINTS_PER_OBSTACLE_DESTROYED
                    
                    # TODO 7: Crear efecto de explosión
                    # explosion = Explosion(obstacle.rect.center)
                    break
        
        # Detectar colisiones jugador-power-ups
        for powerup in powerups[:]:
            if player.rect.colliderect(powerup.rect):
                powerups.remove(powerup)
                player.score += POINTS_PER_POWERUP
                
                # Activar efecto según el tipo
                if powerup.type == 'vodka':
                    effects.activate_vodka_boost(player)
                elif powerup.type == 'tea':
                    effects.activate_tea_shield(player)
        
        return True  # Jugador sigue vivo
    
    def draw(self, screen, player, obstacles, knives, powerups, effects, knife_cooldown):
        """
        Dibuja todo el estado del juego.
        
        Args:
            screen: Superficie donde dibujar
            player: Instancia del jugador
            obstacles: Lista de obstáculos
            knives: Lista de cuchillos
            powerups: Lista de power-ups
            effects: Sistema de efectos
            knife_cooldown: Timer de cooldown
        """
        
        # Limpiar pantalla
        screen.fill(BLACK)
        
        # Dibujar todas las entidades
        player.draw(screen)
        
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        for knife in knives:
            knife.draw(screen)
        
        for powerup in powerups:
            powerup.draw(screen)
        
        # Dibujar HUD (Heads-Up Display)
        self.draw_hud(screen, player, effects, knife_cooldown)
    
    def draw_hud(self, screen, player, effects, knife_cooldown):
        """
        Dibuja la interfaz de usuario (puntuación, vidas, etc.).
        
        Args:
            screen: Superficie donde dibujar
            player: Instancia del jugador
            effects: Sistema de efectos
            knife_cooldown: Timer de cooldown
        """
        
        # Puntuación
        score_text = self.state_manager.font_medium.render(f"Puntuación: {player.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Vidas
        lives_text = self.state_manager.font_medium.render(f"Vidas: {player.lives}", True, WHITE)
        screen.blit(lives_text, (10, 40))
        
        # Estado del escudo
        if player.has_shield:
            shield_text = self.state_manager.font_small.render("🛡️ ESCUDO ACTIVO", True, TEA_COLOR)
            screen.blit(shield_text, (10, 70))
        
        # ✅ IMPLEMENTADO: Barra de cooldown visual
        knife_cooldown.draw_cooldown_bar(screen)
        
        # ✅ IMPLEMENTADO: Efectos activos
        effects.draw_active_effects(screen, self.state_manager.font_small)


class GameOverState:
    """
    Estado de Game Over.
    
    Muestra la puntuación final, el récord y permite
    reiniciar el juego o volver al menú.
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de Game Over."""
        self.state_manager = state_manager
        self.final_score = 0
        self.best_score = 0
        self.is_new_record = False
    
    def set_scores(self, final_score, best_score):
        """
        Establece las puntuaciones para mostrar.
        
        Args:
            final_score: Puntuación de la partida actual
            best_score: Mejor puntuación histórica
        """
        self.final_score = final_score
        self.best_score = best_score
        self.is_new_record = final_score > best_score
    
    def handle_events(self, events):
        """
        Maneja los eventos en la pantalla de Game Over.
        
        Args:
            events: Lista de eventos de pygame
        """
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_ENTER:
                    self.state_manager.change_state(STATE_PLAYING)
                elif event.key == KEY_ESCAPE:
                    # No cerrar el juego desde Game Over con ESC: volver al menú
                    self.state_manager.change_state(STATE_MENU)
                    print("Volviendo al menú desde Game Over")
                    # Continuar ejecutando
            # Soporte de joystick: botones para reiniciar o volver al menú
            elif event.type == pygame.JOYBUTTONDOWN:
                try:
                    button = event.button
                except AttributeError:
                    button = None

                try:
                    from settings import JOYSTICK_BUTTON_SHOOT, JOYSTICK_BUTTON_PAUSE
                except Exception:
                    JOYSTICK_BUTTON_SHOOT = None
                    JOYSTICK_BUTTON_PAUSE = None

                if button == JOYSTICK_BUTTON_SHOOT:
                    self.state_manager.change_state(STATE_PLAYING)
                elif button == JOYSTICK_BUTTON_PAUSE:
                    self.state_manager.change_state(STATE_MENU)
                    print("Volviendo al menú desde Game Over (joystick)")
            # Soporte ratón: click en restart/exit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    pos = event.pos
                except Exception:
                    pos = pygame.mouse.get_pos()

                # compute rects if missing
                if not hasattr(self, 'restart_rect') or not hasattr(self, 'exit_rect'):
                    try:
                        self._compute_gameover_rects()
                    except Exception:
                        pass

                if self.restart_rect.collidepoint(pos):
                    self.state_manager.change_state(STATE_PLAYING)
                if self.exit_rect.collidepoint(pos):
                    self.state_manager.change_state(STATE_MENU)
                    print("Volviendo al menú desde Game Over (ratón)")
        
        return True
    
    def update(self):
        """Actualiza la lógica del Game Over."""
        pass
    
    def draw(self, screen):
        """
        Dibuja la pantalla de Game Over.
        
        Args:
            screen: Superficie donde dibujar
        """
        
        # Fondo semi-transparente
        screen.fill(BLACK)
        
        # Título
        game_over_text = self.state_manager.font_large.render("GAME OVER", True, RED)
        title_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, 150))
        screen.blit(game_over_text, title_rect)
        
        # Puntuación final
        score_text = self.state_manager.font_medium.render(f"Tu puntuación: {self.final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, 220))
        screen.blit(score_text, score_rect)
        
        # Récord
        if self.is_new_record:
            record_text = self.state_manager.font_medium.render("¡NUEVO RÉCORD!", True, YELLOW)
        else:
            record_text = self.state_manager.font_medium.render(f"Récord: {self.best_score}", True, GRAY)
        
        record_rect = record_text.get_rect(center=(WINDOW_WIDTH//2, 260))
        screen.blit(record_text, record_rect)
        
        # Instrucciones
        restart_text = self.state_manager.font_small.render("Presiona ENTER para jugar de nuevo", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, 350))
        restart_bg = restart_text_rect.inflate(20, 10)
        try:
            s = pygame.Surface((restart_bg.width, restart_bg.height), pygame.SRCALPHA)
            s.fill(BUTTON_SHADOW_COLOR)
            screen.blit(s, (restart_bg.x + BUTTON_SHADOW_OFFSET, restart_bg.y + BUTTON_SHADOW_OFFSET))
        except Exception:
            pass
        pygame.draw.rect(screen, BLACK, restart_bg, 0, BUTTON_RADIUS)
        pygame.draw.rect(screen, WHITE, restart_bg, BUTTON_BORDER_WIDTH, BUTTON_RADIUS)
        screen.blit(restart_text, restart_text_rect)
        self.restart_rect = restart_bg

        exit_text = self.state_manager.font_small.render("ESC para salir", True, WHITE)
        exit_text_rect = exit_text.get_rect(center=(WINDOW_WIDTH//2, 380))
        exit_bg = exit_text_rect.inflate(20, 10)
        try:
            s2 = pygame.Surface((exit_bg.width, exit_bg.height), pygame.SRCALPHA)
            s2.fill(BUTTON_SHADOW_COLOR)
            screen.blit(s2, (exit_bg.x + BUTTON_SHADOW_OFFSET, exit_bg.y + BUTTON_SHADOW_OFFSET))
        except Exception:
            pass
        pygame.draw.rect(screen, BLACK, exit_bg, 0, BUTTON_RADIUS)
        pygame.draw.rect(screen, WHITE, exit_bg, BUTTON_BORDER_WIDTH, BUTTON_RADIUS)
        screen.blit(exit_text, exit_text_rect)
        self.exit_rect = exit_bg

        # Update selection based on mouse position so hover highlights work immediately
        try:
            mpos = pygame.mouse.get_pos()
            if self.restart_rect.collidepoint(mpos):
                # treat restart as selection 0
                pass
            elif self.exit_rect.collidepoint(mpos):
                # treat exit as selection 1
                pass
        except Exception:
            pass

    def _compute_gameover_rects(self):
        """Compute restart and exit rects deterministically for GameOverState."""
        restart_text = self.state_manager.font_small.render("Presiona ENTER para jugar de nuevo", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, 350))
        restart_bg = restart_text_rect.inflate(20, 10)

        exit_text = self.state_manager.font_small.render("ESC para salir", True, WHITE)
        exit_text_rect = exit_text.get_rect(center=(WINDOW_WIDTH//2, 380))
        exit_bg = exit_text_rect.inflate(20, 10)

        self.restart_rect = restart_bg
        self.exit_rect = exit_bg


# ✅ IMPLEMENTADO: Estado de pausa
class PausedState:
    """
    Estado cuando el juego está pausado.
    
    En este estado el juego se detiene pero se mantiene visible
    en el fondo con una indicación de pausa superpuesta.
    """
    
    def __init__(self, state_manager):
        """Constructor del estado de pausa."""
        self.state_manager = state_manager
        
        # ✅ IMPLEMENTADO: Efecto visual de pausa
        self.pulse_timer = 0  # Para efecto de pulso en el texto "PAUSED"
        # Opciones del menú de pausa: 0=Reanudar, 1=Volver al menú, 2=Salir
        self.options = ["Reanudar", "Volver al menú", "Salir"]
        self.selection = 0
    
    def handle_events(self, events):
        """
        Maneja eventos en estado de pausa.
        
        Args:
            events: Lista de eventos de pygame
        """
        # Ensure option rects exist so mouse events work even if draw() hasn't run
        if not hasattr(self, 'option_rects') or not self.option_rects:
            try:
                self._compute_pause_option_rects()
            except Exception:
                self.option_rects = []

        for event in events:
            # Teclado: navegación y selección
            if event.type == pygame.KEYDOWN:
                # Navegar opciones con flechas o W/S
                if event.key in (KEY_UP, pygame.K_w):
                    self.selection = (self.selection - 1) % len(self.options)
                elif event.key in (KEY_DOWN, pygame.K_s):
                    self.selection = (self.selection + 1) % len(self.options)
                # Confirmar selección
                elif event.key in (KEY_ENTER, KEY_SPACE):
                    if self.selection == 0:  # Reanudar
                        self.state_manager.change_state(STATE_PLAYING)
                        print("Juego reanudado")
                    elif self.selection == 1:  # Volver al menú
                        self.state_manager.change_state(STATE_MENU)
                        print("Volviendo al menú desde pausa")
                    elif self.selection == 2:  # Salir -> abrir confirmación
                        self.state_manager.change_state(STATE_CONFIRM_EXIT)
                        print("Abrir confirmación de salida")
                # Atajos para reanudar o volver al menú
                elif event.key == KEY_P:
                    self.state_manager.change_state(STATE_PLAYING)
                    print("Juego reanudado (P)")
                elif event.key == KEY_ESCAPE:
                    self.state_manager.change_state(STATE_MENU)
                    print("Volviendo al menú desde pausa (ESC)")

            # Soporte de ratón: click en opciones
            elif event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    pos = event.pos
                except Exception:
                    pos = pygame.mouse.get_pos()

                # Ensure option rects exist
                if not hasattr(self, 'option_rects') or not self.option_rects:
                    try:
                        self._compute_pause_option_rects()
                    except Exception:
                        self.option_rects = []

                for idx, r in enumerate(self.option_rects):
                    if r.collidepoint(pos):
                        self.selection = idx
                        # Ejecutar acción equivalente a ENTER
                        if self.selection == 0:
                            self.state_manager.change_state(STATE_PLAYING)
                            print("Juego reanudado (ratón)")
                        elif self.selection == 1:
                            self.state_manager.change_state(STATE_MENU)
                            print("Volviendo al menú desde pausa (ratón)")
                        elif self.selection == 2:
                            self.state_manager.change_state(STATE_CONFIRM_EXIT)
                            print("Abrir confirmación de salida (ratón)")
                        break

            # Mouse move: hover updates selection
            elif event.type == pygame.MOUSEMOTION:
                try:
                    pos = event.pos
                except Exception:
                    pos = pygame.mouse.get_pos()
                if not hasattr(self, 'option_rects') or not self.option_rects:
                    try:
                        self._compute_pause_option_rects()
                    except Exception:
                        self.option_rects = []
                for idx, r in enumerate(self.option_rects):
                    if r.collidepoint(pos):
                        self.selection = idx
                        break

            # Joystick/gamepad: navegar y confirmar
            elif event.type == pygame.JOYHATMOTION:
                try:
                    hat_x, hat_y = event.value
                    # horizontal hat: left / right map to selection index changes
                    if hat_x < 0:
                        self.selection = (self.selection - 1) % len(self.options)
                    elif hat_x > 0:
                        self.selection = (self.selection + 1) % len(self.options)
                except Exception:
                    pass

            elif event.type == pygame.JOYAXISMOTION:
                try:
                    if event.axis == 0:
                        if event.value < -JOYSTICK_DEADZONE:
                            self.selection = (self.selection - 1) % len(self.options)
                        elif event.value > JOYSTICK_DEADZONE:
                            self.selection = (self.selection + 1) % len(self.options)
                except Exception:
                    pass

            elif event.type == pygame.JOYBUTTONDOWN:
                try:
                    button = event.button
                except AttributeError:
                    button = None

                try:
                    from settings import JOYSTICK_BUTTON_PAUSE, JOYSTICK_BUTTON_SHOOT
                except Exception:
                    JOYSTICK_BUTTON_PAUSE = None
                    JOYSTICK_BUTTON_SHOOT = None

                # Botón A / principal confirma la opción seleccionada
                if button == JOYSTICK_BUTTON_SHOOT:
                    if self.selection == 0:
                        self.state_manager.change_state(STATE_PLAYING)
                        print("Juego reanudado (joystick)")
                    elif self.selection == 1:
                        self.state_manager.change_state(STATE_MENU)
                        print("Volviendo al menú desde pausa (joystick)")
                    elif self.selection == 2:
                        self.state_manager.change_state(STATE_CONFIRM_EXIT)
                        print("Abrir confirmación de salida (joystick)")
                # Botón de pausa actúa como cancelar/volver al menú
                elif button == JOYSTICK_BUTTON_PAUSE:
                    self.state_manager.change_state(STATE_MENU)
                    print("Volviendo al menú desde pausa (joystick pause)")

        return True
    
    def update(self):
        """Actualizar efectos visuales de la pausa."""
        self.pulse_timer += 1
    
    def draw(self, screen, game_surface=None):
        """
        Dibuja la pantalla de pausa.
        
        Args:
            screen: Superficie donde dibujar
            game_surface: Superficie del juego de fondo (opcional)
        """
        
        # ✅ IMPLEMENTADO: Mostrar el juego de fondo con overlay de pausa
        if game_surface:
            # Dibujar el juego de fondo ligeramente oscurecido
            dark_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            dark_surface.fill((0, 0, 0))
            dark_surface.set_alpha(128)  # Semi-transparente
            
            screen.blit(game_surface, (0, 0))
            screen.blit(dark_surface, (0, 0))
        else:
            # Si no hay superficie de fondo, usar color sólido
            screen.fill((50, 50, 50))  # Gris oscuro
        
        # ✅ IMPLEMENTADO: Texto "PAUSED" con efecto de pulso
        pulse_factor = abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 3).x)
        pulse_size = int(FONT_SIZE_LARGE + pulse_factor * 10)
        
        try:
            pulse_font = pygame.font.Font(None, pulse_size)
        except:
            pulse_font = self.state_manager.font_large
        
        paused_text = pulse_font.render("PAUSA", True, YELLOW)
        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        
        # Sombra del texto para mejor legibilidad
        shadow_text = pulse_font.render("PAUSED", True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(paused_rect.centerx + 3, paused_rect.centery + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(paused_text, paused_rect)
        
        # Opciones del menú de pausa (Reanudar / Volver al menú / Salir)
        opt_y = WINDOW_HEIGHT//2 + 20
        total_opts = len(self.options)
        opt_spacing = 220
        # Guardar rects para interacción con ratón
        self.option_rects = []

        for idx, option in enumerate(self.options):
            is_selected = (idx == self.selection)
            # Use high-contrast text: black on hover (yellow bg) or white on dark bg
            text_color = BLACK if is_selected else WHITE
            text = self.state_manager.font_medium.render(option, True, text_color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2 - opt_spacing + idx * opt_spacing, opt_y))

            # Fondo para cada opción (con sombra y esquinas redondeadas)
            bg_rect = pygame.Rect(text_rect.x - 12, text_rect.y - 6,
                                  text_rect.width + 24, text_rect.height + 12)
            try:
                shadow_s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                shadow_s.fill(BUTTON_SHADOW_COLOR)
                screen.blit(shadow_s, (bg_rect.x + BUTTON_SHADOW_OFFSET, bg_rect.y + BUTTON_SHADOW_OFFSET))
            except Exception:
                pass

            bg_color = BUTTON_HOVER_COLOR if is_selected else BLACK
            border_c = YELLOW if is_selected else WHITE
            pygame.draw.rect(screen, bg_color, bg_rect, 0, BUTTON_RADIUS)
            pygame.draw.rect(screen, border_c, bg_rect, BUTTON_BORDER_WIDTH, BUTTON_RADIUS)

            screen.blit(text, text_rect)
            self.option_rects.append(bg_rect)

        # Update selection from current mouse position so hover highlights even when mouse is still
        try:
            mpos = pygame.mouse.get_pos()
            for idx, r in enumerate(self.option_rects):
                if r.collidepoint(mpos):
                    self.selection = idx
                    break
        except Exception:
            pass

    def _compute_pause_option_rects(self):
        """Compute and store pause menu option rects deterministically.

        This mirrors the positions used in draw() so event handlers can use
        the same rects before the screen has been drawn.
        """
        opt_y = WINDOW_HEIGHT//2 + 20
        opt_spacing = 220
        self.option_rects = []
        for idx, option in enumerate(self.options):
            text = self.state_manager.font_medium.render(option, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2 - opt_spacing + idx * opt_spacing, opt_y))
            bg_rect = pygame.Rect(text_rect.x - 12, text_rect.y - 6,
                                  text_rect.width + 24, text_rect.height + 12)
            self.option_rects.append(bg_rect)


class ConfirmExitState:
    """
    Estado que muestra un diálogo para confirmar salida del juego.
    """

    def __init__(self, state_manager):
        self.state_manager = state_manager
        # 0 = Sí (salir), 1 = No (volver al menú)
        self.selection = 0

    def handle_events(self, events):
        """Maneja eventos del diálogo de confirmación.

        Devuelve False para indicar que el juego debe terminar.
        Devuelve True para continuar la ejecución.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Navegación con flechas
                if event.key == KEY_LEFT:
                    self.selection = max(0, self.selection - 1)
                elif event.key == KEY_RIGHT:
                    self.selection = min(1, self.selection + 1)
                # Confirmar con ENTER
                elif event.key == KEY_ENTER:
                    if self.selection == 0:
                        return False
                    else:
                        self.state_manager.change_state(STATE_MENU)
                        return True
                # ESC cancela (volver al menú)
                elif event.key == KEY_ESCAPE:
                    self.state_manager.change_state(STATE_MENU)
                    return True
                # Atajos: Y/N
                elif event.key == pygame.K_y:
                    return False
                elif event.key == pygame.K_n:
                    self.state_manager.change_state(STATE_MENU)
                    return True

            # Joystick hat/axis: change selection
            elif event.type == pygame.JOYHATMOTION:
                try:
                    hat_x, hat_y = event.value
                    if hat_x < 0:
                        self.selection = max(0, self.selection - 1)
                    elif hat_x > 0:
                        self.selection = min(1, self.selection + 1)
                except Exception:
                    pass

            elif event.type == pygame.JOYAXISMOTION:
                try:
                    if event.axis == 0:
                        if event.value < -JOYSTICK_DEADZONE:
                            self.selection = max(0, self.selection - 1)
                        elif event.value > JOYSTICK_DEADZONE:
                            self.selection = min(1, self.selection + 1)
                except Exception:
                    pass

            # Mouse click: SÍ / NO
            elif event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    pos = event.pos
                except Exception:
                    pos = pygame.mouse.get_pos()

                # Ensure rects
                if not hasattr(self, 'yes_rect') or not hasattr(self, 'no_rect'):
                    try:
                        self._compute_confirm_rects()
                    except Exception:
                        pass

                # Click en SÍ / NO
                if self.yes_rect.collidepoint(pos):
                    return False
                if self.no_rect.collidepoint(pos):
                    self.state_manager.change_state(STATE_MENU)
                    return True

            elif event.type == pygame.JOYBUTTONDOWN:
                try:
                    button = event.button
                except AttributeError:
                    button = None

                try:
                    from settings import JOYSTICK_BUTTON_SHOOT, JOYSTICK_BUTTON_PAUSE
                except Exception:
                    JOYSTICK_BUTTON_SHOOT = None
                    JOYSTICK_BUTTON_PAUSE = None

                # Botón principal confirma salida (A)
                if button == JOYSTICK_BUTTON_SHOOT:
                    return False
                # Botón de pausa / cancelar vuelve al menú
                if button == JOYSTICK_BUTTON_PAUSE:
                    self.state_manager.change_state(STATE_MENU)
                    return True

        return True

    def draw(self, screen):
        """Dibuja el diálogo de confirmación en el centro de la pantalla."""
        # Fondo oscuro semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(160)
        screen.blit(overlay, (0, 0))

        # Dimensiones del diálogo
        w, h = 480, 200
        x = WINDOW_WIDTH // 2 - w // 2
        y = WINDOW_HEIGHT // 2 - h // 2

        # Caja del diálogo
        dialog_rect = pygame.Rect(x, y, w, h)
        # Sombra del diálogo
        try:
            shadow = pygame.Surface((w, h), pygame.SRCALPHA)
            shadow.fill(BUTTON_SHADOW_COLOR)
            screen.blit(shadow, (x + BUTTON_SHADOW_OFFSET, y + BUTTON_SHADOW_OFFSET))
        except Exception:
            pass
        # Caja con esquinas redondeadas
        pygame.draw.rect(screen, WHITE, dialog_rect, 0, BUTTON_RADIUS)
        inner = dialog_rect.inflate(-8, -8)
        pygame.draw.rect(screen, BLACK, inner, 0, BUTTON_RADIUS)

        # Texto principal
        title = self.state_manager.font_large.render("¿Deseas salir?", True, YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, y + 50))
        screen.blit(title, title_rect)

        # Opciones Sí / No
        opt_yes = self.state_manager.font_medium.render("SÍ", True, BLACK if self.selection == 0 else GRAY)
        opt_no = self.state_manager.font_medium.render("NO", True, BLACK if self.selection == 1 else GRAY)

        # Posicionar opciones
        opt_y = y + 130
        opt_spacing = 120
        yes_text_rect = opt_yes.get_rect(center=(WINDOW_WIDTH//2 - opt_spacing, opt_y))
        no_text_rect = opt_no.get_rect(center=(WINDOW_WIDTH//2 + opt_spacing, opt_y))

        # Backgrounds para botones SÍ / NO
        yes_bg = yes_text_rect.inflate(20, 10)
        no_bg = no_text_rect.inflate(20, 10)

        # Sombras
        try:
            s_yes = pygame.Surface((yes_bg.width, yes_bg.height), pygame.SRCALPHA)
            s_yes.fill(BUTTON_SHADOW_COLOR)
            screen.blit(s_yes, (yes_bg.x + BUTTON_SHADOW_OFFSET, yes_bg.y + BUTTON_SHADOW_OFFSET))
            s_no = pygame.Surface((no_bg.width, no_bg.height), pygame.SRCALPHA)
            s_no.fill(BUTTON_SHADOW_COLOR)
            screen.blit(s_no, (no_bg.x + BUTTON_SHADOW_OFFSET, no_bg.y + BUTTON_SHADOW_OFFSET))
        except Exception:
            pass

        # Colores según selección
        yes_bg_color = BUTTON_HOVER_COLOR if self.selection == 0 else BLACK
        no_bg_color = BUTTON_HOVER_COLOR if self.selection == 1 else BLACK
        yes_border = YELLOW if self.selection == 0 else WHITE
        no_border = YELLOW if self.selection == 1 else WHITE

        pygame.draw.rect(screen, yes_bg_color, yes_bg, 0, BUTTON_RADIUS)
        pygame.draw.rect(screen, yes_border, yes_bg, BUTTON_BORDER_WIDTH, BUTTON_RADIUS)
        pygame.draw.rect(screen, no_bg_color, no_bg, 0, BUTTON_RADIUS)
        pygame.draw.rect(screen, no_border, no_bg, BUTTON_BORDER_WIDTH, BUTTON_RADIUS)

        screen.blit(opt_yes, yes_text_rect)
        screen.blit(opt_no, no_text_rect)
        # Guardar rects para interacción con ratón
        self.yes_rect = yes_bg
        self.no_rect = no_bg

        # Update selection from mouse position for immediate hover feedback
        try:
            mpos = pygame.mouse.get_pos()
            if self.yes_rect.collidepoint(mpos):
                self.selection = 0
            elif self.no_rect.collidepoint(mpos):
                self.selection = 1
        except Exception:
            pass

        # Instrucciones
        instr = self.state_manager.font_small.render("ENTER = confirmar · ESC = cancelar", True, WHITE)
        instr_rect = instr.get_rect(center=(WINDOW_WIDTH//2, y + h - 20))
        screen.blit(instr, instr_rect)

    def _compute_confirm_rects(self):
        """Compute yes/no rects deterministically for ConfirmExitState."""
        w, h = 480, 200
        x = WINDOW_WIDTH // 2 - w // 2
        y = WINDOW_HEIGHT // 2 - h // 2
        opt_yes = self.state_manager.font_medium.render("SÍ", True, WHITE)
        opt_no = self.state_manager.font_medium.render("NO", True, WHITE)
        opt_y = y + 130
        opt_spacing = 120
        yes_text_rect = opt_yes.get_rect(center=(WINDOW_WIDTH//2 - opt_spacing, opt_y))
        no_text_rect = opt_no.get_rect(center=(WINDOW_WIDTH//2 + opt_spacing, opt_y))
        yes_bg = yes_text_rect.inflate(20, 10)
        no_bg = no_text_rect.inflate(20, 10)
        self.yes_rect = yes_bg
        self.no_rect = no_bg


# TODO 1: Estado de pausa
# class PausedState:
#     """Estado cuando el juego está pausado."""
#     
#     def __init__(self, state_manager):
#         self.state_manager = state_manager
#     
#     def handle_events(self, events):
#         for event in events:
#             if event.type == pygame.KEYDOWN:
#                 if event.key == KEY_P:
#                     self.state_manager.change_state(STATE_PLAYING)
#         return True
#     
#     def update(self):
#         pass
#     
#     def draw(self, screen):
#         # Dibujar "PAUSED" en el centro
#         pass

# === NOTAS EDUCATIVAS ===
"""
Conceptos importantes sobre máquinas de estados:

1. SEPARACIÓN DE RESPONSABILIDADES:
   Cada estado maneja solo su propia lógica, lo que hace
   el código más organizado y fácil de mantener.

2. TRANSICIONES DE ESTADO:
   Los estados pueden cambiar a otros estados según eventos
   (teclas presionadas, condiciones del juego, etc.).

3. GESTIÓN DE EVENTOS:
   Cada estado decide cómo responder a eventos de teclado
   y ratón de manera apropiada para su contexto.

4. RENDERIZADO CONDICIONAL:
   Solo se dibuja lo que es relevante para el estado actual,
   mejorando el rendimiento y la claridad visual.

5. FLUJO DEL PROGRAMA:
   La máquina de estados define cómo el usuario navega
   por las diferentes pantallas del juego.

Ejercicio para estudiantes:
- Implementar el estado de pausa (TODO 1)
- Añadir un estado de opciones o configuración
- Crear transiciones animadas entre estados
"""