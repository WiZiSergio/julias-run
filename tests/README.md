# Tests - Pruebas del Juego 🧪

Esta carpeta está preparada para **pruebas básicas** de Julia's Run usando **pytest**.

## 🎯 Propósito Educativo

Los tests enseñan:
- **Validación de funcionalidad** sin romper el juego
- **Desarrollo dirigido por pruebas** (TDD básico)
- **Casos límite** y manejo de errores
- **Refactoring seguro** con tests como red de seguridad

## 📝 Ideas para Tests (Alumnado)

### 🟢 Tests Básicos
```python
# test_entities.py
def test_player_creation():
    """El jugador se crea con valores iniciales correctos"""
    
def test_obstacle_movement():
    """Los obstáculos se mueven hacia abajo"""
    
def test_collision_detection():
    """Las colisiones se detectan correctamente"""
```

### 🟡 Tests Intermedios
```python
def test_powerup_effects():
    """Los power-ups aplican efectos correctamente"""
    
def test_score_calculation():
    """La puntuación se calcula según las reglas"""
    
def test_game_state_transitions():
    """Los cambios de estado funcionan bien"""
```

### 🔴 Tests Avanzados
```python
def test_performance_with_many_objects():
    """El juego mantiene FPS con muchos objetos"""
    
def test_memory_usage():
    """No hay memory leaks en sesiones largas"""
```

## 🚀 Cómo Empezar

1. **Instalar pytest**:
   ```bash
   pip install pytest
   ```

2. **Crear tu primer test**:
   ```python
   # test_basic.py
   from src.entities import Player
   
   def test_player_starts_with_three_lives():
       player = Player()
       assert player.lives == 3
   ```

3. **Ejecutar tests**:
   ```bash
   pytest tests/
   ```

## 💡 Beneficios del Testing

- **Confianza** para hacer cambios
- **Documentación** de cómo funciona el código
- **Detección temprana** de bugs
- **Mejor diseño** de código (testeable = bien diseñado)

## 🎓 Conexión con la Industria

El testing es **fundamental** en desarrollo profesional. Aquí practicas con un proyecto real pero manejable.

¡Empieza con tests simples y ve creciendo! 🌱