# Assets - Recursos del Juego 🎨

Esta carpeta contiene todos los recursos visuales de **Julia's Run**.

## 📁 Estructura

```
assets/
└── sprites/         # Imágenes pixel art del juego
    ├── julia_pixelart.jpg      # Personaje principal
    ├── cachopo_pixelart.jpg    # Obstáculos (cachopos)
    ├── knife__pixelart.jpg     # Proyectiles
    └── vodka_pixelart.jpg      # Power-ups
```

## 🎯 Propósito Educativo

Los sprites están en formato **.jpg** y el juego incluye un **sistema de fallback automático**:
- Si una imagen no se encuentra, se dibuja un rectángulo de color
- Esto enseña **gestión de errores** y **robustez del código**

## 💡 Ideas para Mejoras (Alumnado)

### 🟢 Nivel Básico
- Cambiar los colores de los fallbacks en `settings.py`
- Crear nuevos sprites y reemplazar los existentes
- Añadir más variedad visual

### 🟡 Nivel Intermedio
- Implementar animaciones sprite (múltiples frames)
- Añadir efectos de partículas
- Crear sprites para diferentes tipos de obstáculos

### 🔴 Nivel Avanzado
- Sistema de tilesets para fondos
- Efectos de iluminación y shaders
- Animaciones procedurales

## 📝 Formato de Sprites

- **Resolución recomendada**: 32x32 a 64x64 píxeles
- **Formato**: JPG o PNG (el juego soporta ambos)
- **Estilo**: Pixel art para mantener coherencia visual

¡Experimenta creando tus propios sprites!