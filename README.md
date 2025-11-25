# Julia's Run - Aprende POO con un Juego Real 🎮

<div align="center">
  <img src="images/julias_run.png" alt="Julia's Run - Juego educativo de POO" width="300"/>
</div>

> **Un proyecto educativo para aprender Programación Orientada a Objetos de forma práctica**

¡Bienvenido a **Julia's Run**! Este es un juego **completamente funcional** desarrollado en Python con Pygame, diseñado específicamente para enseñar conceptos de **Programación Orientada a Objetos (POO)** de manera práctica y divertida.

## 🎯 ¿Qué hace especial a este proyecto?

**No es un tutorial paso a paso** - Es un **juego real que funciona** donde puedes:
- 🔍 **Explorar** código profesional en funcionamiento
- 🧩 **Entender** cómo se aplica POO en proyectos reales  
- 🚀 **Mejorar** funcionalidades existentes sin partir de cero
- 🎨 **Experimentar** con cambios inmediatos y visibles

## 🎮 El Juego: Julia's Run

Julia debe esquivar **cachopos** (obstáculos) que caen del cielo mientras lanza **cuchillos** para defenderse. Incluye:

- ✨ **Power-ups**: Vodka Boost (velocidad) y Té Mágico (escudo)
- 🎯 **Sistema de combos** y puntuaciones
- 🎨 **Sprites pixel art** con fallbacks automáticos
- 📊 **Persistencia** de estadísticas y récords
- 🎭 **Estados de juego**: Menú, jugando, pausa, game over

### 🎮 Controles
- **⬅️➡️⬆️⬇️** - Mover a Julia
- **ESPACIO** - Lanzar cuchillo  
- **P** - Pausar/reanudar
- **ESC** - Salir

## 🚀 Inicio Rápido

```bash
# 1. Clonar el repositorio (rama dev lista para estudiantes)
git clone -b dev https://github.com/Anais-RV/julias-run.git
cd julias-run

# 2. Instalar dependencias
pip install pygame

# 3. ¡Jugar primero, programar después!
make run
# o alternativamente:
python src/main.py
```

> 💡 **Para Estudiantes**: Usa la rama `dev` que contiene el proyecto educativo optimizado y listo para trabajar.  
> 📚 **Para Profesorado**: La rama `master` contiene la versión estable con documentación adicional.

## 📚 Guía de Aprendizaje POO

### 🏁 Paso 1: Fundamentos POO (45 min)
📓 **`docs/00_poo_introduccion.ipynb`** - **¡Empieza aquí!**
- Conceptos básicos de POO con ejercicios interactivos
- Ejemplos prácticos con nombres de la clase
- Preparación perfecta antes del código del juego

### 🎮 Paso 2: Juega y Observa (15 min)
**Después del notebook**, juega al menos 15 minutos y pregúntate:
- ¿Qué elementos ves en pantalla?
- ¿Cómo interactúan entre sí?
- ¿Reconoces los conceptos del notebook?

### 🔍 Paso 3: Explora la Estructura (30 min)
```
julias_run/
├── src/             # 💻 Código principal → Ahora puedes entenderlo
├── docs/            # 📚 Guías de aprendizaje  
├── assets/          # 🎨 Sprites del juego
└── tests/           # 🧪 Pruebas (para nivel avanzado)
```

**Orden de exploración sugerido:**
1. 📖 `src/README.md` - Mapa del código
2. ⚙️ `src/settings.py` - Configuración del juego
3. 👾 `src/entities.py` - **¡Las clases principales!**
4. 🎮 `src/main.py` - Cómo se ejecuta todo

### 🧩 Paso 4: Identifica Conceptos POO (45 min)

**Abre `src/entities.py` y busca** (¡ahora los reconocerás del notebook!):

#### 🏗️ **Clases (Plantillas)**
```python
class Player:          # Plantilla para el jugador
class Obstacle:        # Plantilla para obstáculos  
class PowerUp:         # Plantilla para power-ups
```

#### 🎭 **Objetos (Instancias)**
```python
player = Player()                    # Crear UN jugador
obstacle = Obstacle('normal')        # Crear UN obstáculo
```

#### 📦 **Atributos (Características)**
```python
self.lives = 3         # Vidas del jugador
self.rect.x = 100      # Posición X
self.speed = 5         # Velocidad
```

#### ⚡ **Métodos (Comportamientos)**
```python
def update(self):      # Actualizar estado
def draw(self, screen): # Dibujar en pantalla
def take_damage(self):  # Recibir daño
```

### 🎓 Paso 5: Sigue las Guías Didácticas
1. 📖 **[docs/01_intro_poo_con_julias_run.md](docs/01_intro_poo_con_julias_run.md)** - Clase guiada con ejercicios
2. 🚀 **[docs/02_reto_mejoras.md](docs/02_reto_mejoras.md)** - Retos y evaluación

## 🔧 ¿Qué Puedes Mejorar?

### 🟢 **Nivel Principiante**
- 🎨 Cambiar colores y velocidades en `settings.py`
- 📝 Añadir comentarios explicativos a las clases
- 🆕 Crear un nuevo tipo de power-up básico
- ✨ Modificar efectos visuales existentes

### 🟡 **Nivel Intermedio** 
- 🧹 Refactorizar funciones largas en partes más pequeñas
- 🏗️ Crear nuevas clases siguiendo los patrones existentes
- 🎯 Implementar sistema de niveles con dificultad creciente
- 📊 Mejorar el sistema de puntuación y estadísticas

### 🔴 **Nivel Avanzado**
- 🎨 Sistema de animaciones para sprites
- 🔊 Integración de audio y efectos de sonido
- 🧪 Suite completa de tests automatizados
- 🌐 Funcionalidades multijugador básicas

## 👩‍🏫 Para Profesorado

### 🎯 **Objetivos de Aprendizaje**
Al completar este proyecto, el alumnado será capaz de:

1. **Identificar** clases, objetos, atributos y métodos en código real
2. **Comprender** encapsulación, herencia y polimorfismo
3. **Aplicar** principios de diseño modular
4. **Refactorizar** código existente sin romper funcionalidad
5. **Conectar** POO con aplicaciones prácticas

### 📋 **Evaluación Sugerida**
| Aspecto | Descripción | Puntuación |
|---------|-------------|------------|
| **Comprensión POO** | Identifica y explica clases, objetos, métodos | **/3** |
| **Refactorización** | Mejora código manteniendo funcionalidad | **/3** |
| **Creatividad** | Añade features originales y bien implementadas | **/2** |
| **Documentación** | Comenta código y documenta cambios | **/2** |

### 🕒 **Temporización Sugerida**
- **Sesión 1** (90 min): Exploración y comprensión del código
- **Sesión 2** (90 min): Identificación de conceptos POO
- **Sesión 3** (90 min): Primeras modificaciones simples
- **Sesión 4** (90 min): Refactorización y mejoras
- **Sesión 5** (90 min): Presentación de mejoras

## 🧠 Filosofía Pedagógica

> **"Aprender haciendo con código que funciona"**

En lugar de ejemplos abstractos, usamos un **juego real** donde:
- ✅ **Cada concepto tiene aplicación práctica**
- ✅ **Los cambios son inmediatamente visibles**
- ✅ **El contexto es motivador y familiar**
- ✅ **Se aprende a trabajar con código existente**

## 🔗 Conexiones Curriculares

### 🔗 **Programación Fundacional**
- Variables, funciones, estructuras de control
- Importación de módulos y organización del código
- Gestión de errores y casos límite

### 🔗 **POO Avanzada**  
- Clases, objetos, encapsulación
- Herencia y composición
- Polimorfismo y abstracción

### 🔗 **Ingeniería de Software**
- Modularidad y separación de responsabilidades
- Documentación y legibilidad del código
- Testing y refactoring

### 🔗 **Desarrollo de Juegos**
- Game loops y gestión de estados
- Renderizado y efectos visuales
- Input handling y física básica

## 🤝 Contribuir y Personalizar

### 💡 **Ideas para Proyectos Derivados**
- 🏥 **Sistema de gestión hospitalaria** (mismas clases, diferente contexto)
- 🛒 **E-commerce básico** (productos = entidades, carrito = jugador)  
- 📱 **App de tareas** (tareas = obstáculos, usuario = jugador)

### 🌟 **Inspiración para Extensiones**
- 🎓 **Portfolio estudiantil**: Documenta tus mejoras
- 🎮 **Game jam**: Usa la base para crear tu propio juego
- 👥 **Proyecto colaborativo**: Cada estudiante mejora una parte

## 📜 Autoría y Licencia

**Desarrollado con ❤️ para la comunidad educativa por:**

🧑‍💻 **Anais Rodríguez Vera**  
🔗 [GitHub: @Anais-RV](https://github.com/Anais-RV)  
🌐 Perfil: [https://github.com/Anais-RV](https://github.com/Anais-RV)

### 📄 **Licencia MIT**
Este proyecto es **open source** bajo licencia MIT. Puedes:
- ✅ Usarlo en clase libremente
- ✅ Modificarlo según tus necesidades
- ✅ Distribuirlo y compartirlo  
- ✅ Crear proyectos derivados

Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🆘 ¿Necesitas Ayuda?

### 📚 **Recursos Adicionales**
- 📖 [Documentación de Pygame](https://www.pygame.org/docs/)
- 🐍 [Tutorial de POO en Python](https://docs.python.org/es/3/tutorial/classes.html)
- 🎮 [Game Programming Patterns](https://gameprogrammingpatterns.com/)

### ❓ **Problemas Comunes**
- **"No carga el juego"** → Verificar instalación de pygame
- **"No entiendo el código"** → Empezar por las guías en `docs/`
- **"Rompí algo"** → `git restore .` para volver al estado original

---

## 🎮 ¡Que comience la aventura del aprendizaje!

**Recuerda**: No se trata de escribir código perfecto desde cero, sino de **entender, mejorar y aprender** con código que ya funciona.

¡Como en el desarrollo profesional real! 🚀

---

*💡 **Tip**: El mejor código es el que otros desarrolladores (incluido tu futuro yo) pueden entender y mejorar fácilmente.*