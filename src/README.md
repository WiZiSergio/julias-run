# Código Fuente - src/ 💻

Esta carpeta contiene todo el **código principal** de Julia's Run, organizado de forma modular y educativa.

## 📁 Estructura del Código

```
src/
├── main.py          # 🎮 Punto de entrada y game loop principal
├── entities.py      # 👾 Clases de entidades (Player, Obstacle, etc.)
├── abilities.py     # ⚡ Sistema de habilidades y efectos
├── game_states.py   # 🎯 Gestión de estados del juego
├── settings.py      # ⚙️ Configuración y constantes
└── utils.py         # 🛠️ Funciones auxiliares
```

## 🎯 Conceptos de POO por Archivo

### 📄 `entities.py` - **Clases y Objetos**
- **Clase `Player`**: Encapsula estado y comportamiento del jugador
- **Clase `Obstacle`**: Modela enemigos con diferentes tipos
- **Clase `PowerUp`**: Implementa items especiales
- **Herencia**: `Enemy` extiende `Obstacle`

### 📄 `abilities.py` - **Composición y Delegación**
- **Clase `CooldownTimer`**: Maneja tiempos de espera
- **Clase `ParticleEffect`**: Efectos visuales modulares
- **Clase `ComboSystem`**: Lógica de combos separada

### 📄 `game_states.py` - **Polimorfismo**
- **Patrón State**: Diferentes estados con misma interfaz
- **Método `update()`**: Cada estado se actualiza diferente
- **Método `draw()`**: Cada estado se dibuja diferente

### 📄 `settings.py` - **Constantes y Configuración**
- **Separación de responsabilidades**: Configuración centralizada
- **Mantenimiento**: Fácil cambiar parámetros del juego
- **Legibilidad**: Nombres descriptivos vs números mágicos

## 🔍 Explorando el Código

### Para Entender POO:
1. **Empieza con `entities.py`** - Ve las clases principales
2. **Sigue con `main.py`** - Observa cómo se usan los objetos
3. **Explora `game_states.py`** - Estudia el polimorfismo
4. **Revisa `settings.py`** - Entiende la organización

### Para Mejorar el Código:
- 🔍 **Busca comentarios con "Mejora sugerida"**
- 📝 **Añade docstrings donde falten**
- 🧹 **Refactoriza funciones largas**
- ✨ **Mejora nombres de variables**

## 💡 Preguntas para Reflexionar

1. **¿Por qué `Player` es una clase y no solo funciones?**
2. **¿Qué ventajas tiene separar `abilities.py`?**
3. **¿Cómo añadirías un nuevo tipo de power-up?**
4. **¿Qué patrones de diseño reconoces en el código?**

## 🚀 Próximos Pasos

Una vez entiendas la estructura:
1. **Modifica parámetros** en `settings.py`
	- Ahora puedes forzar un tamaño de ventana manual desde `settings.py` estableciendo `MANUAL_WINDOW_SIZE = True` y ajustando `MANUAL_WINDOW_WIDTH` / `MANUAL_WINDOW_HEIGHT`.
	- Para hacer que las entidades caigan más lentas (obstáculos y power-ups) edita `FALL_SPEED_MULTIPLIER` en `settings.py`. Valores entre 0.0 y 1.0 reducen la velocidad; por ejemplo `0.6` hace que caigan al ~60% de la velocidad base.
2. **Añade features simples** siguiendo patrones existentes
3. **Refactoriza código** para mejorar claridad
4. **Documenta** tus cambios y aprendizajes

¡El código es tu laboratorio de POO! 🧪