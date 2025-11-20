# Introducción Práctica a POO con Julia's Run 🎮

> **Aprende Programación Orientada a Objetos analizando un juego real**

## 🎯 Objetivos de Esta Guía

Al completar esta guía, serás capaz de:
- 🧩 **Identificar** clases, objetos, atributos y métodos en código real
- 🔍 **Entender** la diferencia entre clase y objeto
- 📦 **Reconocer** encapsulación y modularidad en acción
- 🛠️ **Crear** tu primera clase basada en las existentes

## 🏁 Preparación (5 minutos)

1. **Ejecuta el juego** y juega al menos 5 minutos
2. **Observa** los elementos: Julia, cachopos, cuchillos, power-ups
3. **Piensa**: ¿Qué comportamientos tiene cada elemento?

## Archivos de prueba incluidos

He añadido al repositorio unos archivos de ejemplo que reproducen los ejercicios
del documento para que puedas ejecutar y probar rápidamente:

- `src/mi_enemigo.py` — Clase ejemplo `EnemigoEspecial` (ejercicio).
- `tests/test_objetos.py` — Script que crea instancias de `Player` y `Obstacle` y muestra información básica.
- `tests/test_mi_enemigo.py` — Demo visual corto que muestra `EnemigoEspecial` moviéndose.

Cómo ejecutar los tests de ejemplo:

```powershell
python tests/test_objetos.py
python tests/test_mi_enemigo.py
```

Nota: Los demos usan `pygame` y abrirán una ventana; cierra la ventana o espera el fin del demo.

## 📚 Parte 1: ¿Qué es una Clase? (20 minutos)

### 🏗️ Concepto: Clase = Plantilla/Molde

Imagina una **fábrica de coches**:
- 📋 **Plano del coche** = **Clase**
- 🚗 **Coche específico** = **Objeto**
- 🔧 **Características** (color, modelo) = **Atributos**  
- ⚡ **Acciones** (arrancar, frenar) = **Métodos**

### 🎮 En Julia's Run:

**Abre `src/entities.py` y encuentra la clase `Player`:**

```python
class Player:
    \"\"\"
    Esta clase representa al jugador principal (Julia).
    Es el MOLDE para crear jugadores en el juego.
    \"\"\"
    
    def __init__(self):
        \"\"\"Constructor: cómo se crea un jugador\"\"\"
        self.lives = PLAYER_LIVES      # ⚡ ATRIBUTO: vidas
        self.score = 0                 # ⚡ ATRIBUTO: puntuación  
        self.rect = pygame.Rect(...)   # ⚡ ATRIBUTO: posición
        
    def move(self, keys_pressed):
        \"\"\"MÉTODO: cómo se mueve el jugador\"\"\"
        # Lógica de movimiento
        
    def draw(self, screen):
        \"\"\"MÉTODO: cómo se dibuja el jugador\"\"\"
        # Lógica de dibujo
```

### 🤔 Ejercicio de Reflexión

**Responde estas preguntas:**

1. **¿Cuántas clases `Player` hay en el código?** 
   - Respuesta: Solo UNA (es la plantilla)

2. **¿Cuántos objetos `Player` se crean cuando juegas?**
   - Respuesta: Solo UNO (el personaje que controlas)

3. **¿Qué atributos tiene la clase `Player`?**
   - lives, score, rect, speed, has_shield...

4. **¿Qué métodos (acciones) puede hacer un `Player`?**
   - move(), draw(), take_damage(), reset_position()...

## 📚 Parte 2: Creación de Objetos (15 minutos)

### 🏭 Del Molde al Objeto Real

**En `src/main.py`, busca esta línea:**
```python
self.player = Player()  # ¡Aquí se crea EL objeto jugador!
```

**En `src/entities.py`, busca cómo se crean obstáculos:**
```python
obstacle = Obstacle(difficulty_multiplier)  # Crear UN obstáculo
```

### 🧪 Experimento Práctico

**Crea un archivo `test_objetos.py` y prueba:**

```python
# test_objetos.py
from src.entities import Player, Obstacle

# Crear DOS jugadores diferentes
julia1 = Player()
julia2 = Player()

# Son objetos DIFERENTES aunque usen la misma clase
print(f\"Julia 1 vidas: {julia1.lives}\")  # 3
print(f\"Julia 2 vidas: {julia2.lives}\")  # 3

# Modificar UNO no afecta al OTRO
julia1.take_damage()
print(f\"Julia 1 vidas: {julia1.lives}\")  # 2
print(f\"Julia 2 vidas: {julia2.lives}\")  # 3 (sin cambios)

# Crear obstáculos diferentes
cachopo1 = Obstacle(1.0)  # Normal
cachopo2 = Obstacle(2.0)  # Más difícil

print(f\"Cachopo 1 velocidad: {cachopo1.speed}\")
print(f\"Cachopo 2 velocidad: {cachopo2.speed}\")  # Más rápido
```

**¡Ejecuta el archivo!**
```bash
python test_objetos.py
```

### 💡 Insight Clave
> **UNA clase → MUCHOS objetos**  
> Cada objeto tiene sus **propios valores** de atributos, pero **comparten** los mismos métodos.

## 📚 Parte 3: Atributos vs Métodos (20 minutos)

### 📦 Atributos = Estado/Características

**En la clase `Player`, identifica TODOS los atributos:**

```python
class Player:
    def __init__(self):
        # 📦 ATRIBUTOS (lo que \"ES\" o \"TIENE\" el jugador)
        self.lives = PLAYER_LIVES           # ¿Cuántas vidas tiene?
        self.score = 0                      # ¿Cuántos puntos tiene?
        self.speed = PLAYER_SPEED           # ¿Qué tan rápido se mueve?
        self.has_shield = False             # ¿Tiene escudo activo?
        self.rect = pygame.Rect(...)        # ¿Dónde está en pantalla?
        self.sprite_frame = 0               # ¿Qué frame de animación?
        self.facing_direction = 1           # ¿Hacia dónde mira?
```

### ⚡ Métodos = Comportamiento/Acciones

**Identifica TODOS los métodos de `Player`:**

```python
class Player:
    # ⚡ MÉTODOS (lo que \"HACE\" el jugador)
    
    def move(self, keys_pressed):
        \"\"\"¿Cómo se mueve?\"\"\"
        
    def draw(self, screen):
        \"\"\"¿Cómo se dibuja?\"\"\"
        
    def take_damage(self):
        \"\"\"¿Qué pasa cuando recibe daño?\"\"\"
        
    def reset_position(self):
        \"\"\"¿Cómo vuelve al inicio?\"\"\"
```

### 🔍 Ejercicio: Análisis de Clase

**Completa esta tabla para la clase `Obstacle`:**

| **Atributos (Estado)** | **Métodos (Comportamiento)** |
|------------------------|-------------------------------|
| self.rect (posición)   | update() (moverse)            |
| self.speed (velocidad) | draw() (dibujarse)            |
| self.obstacle_type     | ?                             |
| ?                      | ?                             |
| ?                      | ?                             |

**Pista**: Abre `src/entities.py` y busca la clase `Obstacle`.

## 📚 Parte 4: Encapsulación en Acción (25 minutos)

### 🔒 Concepto: Todo Relacionado Junto

**Encapsulación** = Agrupar datos (atributos) y funciones (métodos) relacionados en una sola unidad (clase).

### 🎮 Ejemplo Real: Clase `Player`

**¿Por qué es buena la encapsulación aquí?**

```python
class Player:
    def __init__(self):
        # Todos los datos del jugador en UN lugar
        self.lives = 3
        self.has_shield = False
        
    def take_damage(self):
        \"\"\"
        MÉTODO que sabe cómo manejar el daño.
        Conoce la lógica del escudo y las vidas.
        \"\"\"
        if self.has_shield:
            self.has_shield = False  # Perder escudo
        else:
            self.lives -= 1          # Perder vida
```

**Sin encapsulación sería así:**
```python
# ❌ MALO: datos y lógica separados
player_lives = 3
player_has_shield = False

# En otra parte del código...
def handle_damage():
    global player_lives, player_has_shield
    if player_has_shield:
        player_has_shield = False
    else:
        player_lives -= 1
```

### 🔍 Ejercicio: Busca Encapsulación

**En `src/entities.py`, busca la clase `PowerUp` y responde:**

1. **¿Qué atributos encapsula?**
   - Pista: Busca `self.` en `__init__()`

2. **¿Qué métodos encapsula?**
   - Pista: Busca `def` dentro de la clase

3. **¿Por qué es mejor tener `PowerUp` como clase vs funciones sueltas?**

### 💡 Beneficios de la Encapsulación

✅ **Organización**: Todo lo del power-up está junto  
✅ **Reutilización**: Puedo crear muchos power-ups  
✅ **Mantenimiento**: Si cambio algo, sé dónde está  
✅ **Entendimiento**: Fácil saber qué hace cada parte  

## 📚 Parte 5: Tu Primera Clase (30 minutos)

### 🚀 Ejercicio Práctico: Crear `EnemigoEspecial`

**Vas a crear una nueva clase basada en `Obstacle` pero con comportamiento especial.**

**Paso 1: Analizar la clase base**
```python
# En src/entities.py, estudia la clase Obstacle
class Obstacle:
    def __init__(self, difficulty_multiplier=1.0):
        # ¿Qué atributos tiene?
        # ¿Cómo se inicializa?
        
    def update(self):
        # ¿Qué hace en cada frame?
        
    def draw(self, screen):
        # ¿Cómo se dibuja?
```

**Paso 2: Crear tu nueva clase**

**Crea un archivo `mi_enemigo.py`:**
```python
# mi_enemigo.py
import pygame
import random
from src.settings import *

class EnemigoEspecial:
    \"\"\"
    Un enemigo que se mueve de forma diferente a los obstáculos normales.
    
    📚 CONCEPTOS POO QUE PRATICAS:
    - Clase propia con atributos y métodos
    - Encapsulación de comportamiento
    - Reutilización de patrones existentes
    \"\"\"
    
    def __init__(self, x, y):
        \"\"\"
        Constructor del enemigo especial.
        
        Args:
            x, y: Posición inicial
        \"\"\"
        # 📦 ATRIBUTOS (Estado del enemigo)
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed_x = random.choice([-2, 2])  # Se mueve horizontal
        self.speed_y = 3                       # También baja
        self.color = (255, 100, 255)          # Color especial
        self.lives = 2                        # Más resistente
        
    def update(self):
        \"\"\"
        ⚡ MÉTODO: Actualizar posición y comportamiento
        \"\"\"
        # Movimiento especial: zigzag
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Rebotar en bordes
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.speed_x *= -1  # Cambiar dirección
            
        # ¿Sigue visible?
        return self.rect.top < WINDOW_HEIGHT
    
    def draw(self, screen):
        \"\"\"
        ⚡ MÉTODO: Dibujar el enemigo
        \"\"\"
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Indicador de vidas
        for i in range(self.lives):
            pygame.draw.circle(screen, (255, 255, 255), 
                             (self.rect.centerx - 10 + i*10, self.rect.top - 5), 3)
    
    def take_damage(self):
        \"\"\"
        ⚡ MÉTODO: Recibir daño
        
        Returns:
            bool: True si sigue vivo, False si muere
        \"\"\"
        self.lives -= 1
        return self.lives > 0
```

**Paso 3: Probar tu clase**

**Crea `test_mi_enemigo.py`:**
```python
# test_mi_enemigo.py
import pygame
from mi_enemigo import EnemigoEspecial

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Crear tu enemigo
mi_enemigo = EnemigoEspecial(400, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Actualizar
    mi_enemigo.update()
    
    # Dibujar
    screen.fill((0, 0, 0))
    mi_enemigo.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

**¡Ejecuta tu test!**
```bash
python test_mi_enemigo.py
```

### 🎯 Preguntas de Reflexión

Después de crear tu clase, responde:

1. **¿Qué atributos decidiste incluir y por qué?**

2. **¿Qué comportamientos (métodos) implementaste?**

3. **¿En qué se parece tu clase a `Obstacle` y en qué se diferencia?**

4. **¿Cómo podrías integrar tu `EnemigoEspecial` en el juego principal?**

## 🔗 Conexión con el Mundo Real

### 🏥 Ejemplo: Sistema Hospitalario

**Si hicieras un sistema de hospital, podrías tener:**

```python
class Paciente:
    def __init__(self, nombre, edad):
        self.nombre = nombre           # Atributo
        self.edad = edad              # Atributo
        self.historiales = []         # Atributo
        
    def agregar_historial(self, registro):  # Método
        self.historiales.append(registro)
        
    def obtener_info(self):              # Método
        return f\"{self.nombre}, {self.edad} años\"
```

**¿Ves las similitudes con `Player`?**
- Ambos tienen **atributos** que guardan información
- Ambos tienen **métodos** que definen comportamientos
- Ambos **encapsulan** datos y funciones relacionadas

### 💼 Ejemplo: E-commerce

```python
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
        self.stock = 0
        
    def aplicar_descuento(self, porcentaje):
        self.precio *= (1 - porcentaje/100)
        
    def actualizar_stock(self, cantidad):
        self.stock += cantidad
```

## 📝 Ejercicios para Casa

### 🟢 **Nivel Básico**

1. **Modifica la clase `EnemigoEspecial`** para que:
   - Cambie de color cuando le queda 1 vida
   - Se mueva más lento cuando está dañado

2. **Crea una clase `PowerUpEspecial`** basada en `PowerUp` que:
   - Tenga un efecto diferente
   - Use un color único
   - Dure más tiempo

### 🟡 **Nivel Intermedio**

3. **Implementa herencia simple**:
   ```python
   class ObstaculoArmado(Obstacle):
       def __init__(self):
           super().__init__()  # Usar constructor padre
           self.puede_disparar = True
   ```

4. **Crea un sistema de `Jefe` (Boss)**:
   - Más grande que obstáculos normales
   - Múltiples vidas
   - Movimiento especial

### 🔴 **Nivel Avanzado**

5. **Diseña un sistema de `Niveles`**:
   ```python
   class Nivel:
       def __init__(self, numero):
           self.numero = numero
           self.velocidad_base = numero * 1.2
           self.spawn_rate = max(30, 60 - numero * 5)
   ```

6. **Implementa un `GestorDeEnemigos`**:
   - Clase que maneja múltiples tipos de enemigos
   - Decide cuándo y qué tipo crear
   - Maneja las interacciones entre ellos

## 🎯 Resumen de Conceptos Aprendidos

### ✅ **Clase vs Objeto**
- **Clase** = Molde/plantilla (código que defines)
- **Objeto** = Instancia específica (lo que se crea en memoria)

### ✅ **Atributos vs Métodos**
- **Atributos** = Características/estado (`self.lives`)
- **Métodos** = Comportamientos/acciones (`def move()`)

### ✅ **Encapsulación**
- Agrupar datos y funciones relacionadas
- Hace el código más organizado y mantenible
- Facilita reutilización y entendimiento

### ✅ **POO en la Práctica**
- No es solo teoría - se usa en proyectos reales
- Ayuda a organizar código complejo
- Facilita trabajo en equipo
- Se aplica en web, móvil, desktop, juegos...

## 🚀 Próximos Pasos

1. **Completa los ejercicios de esta guía**
2. **Continúa con [02_reto_mejoras.md](02_reto_mejoras.md)**
3. **Experimenta modificando el juego original**
4. **Documenta tus aprendizajes**

---

## 🎉 ¡Felicitaciones!

Has dado tus primeros pasos sólidos en **Programación Orientada a Objetos** usando un proyecto real. Los conceptos que aprendiste aquí son **fundamentales** en el desarrollo de software profesional.

**Recuerda**: La POO no es solo sintaxis - es una **forma de pensar** y organizar código para resolver problemas complejos de manera elegante.

¡Sigue practicando! 🚀

---

*💡 Tip: La mejor forma de aprender POO es **practicando con código real**. ¡Este juego es tu laboratorio perfecto!*