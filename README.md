# 🐒 Monitos IA — Visión Artificial con Manos

Proyecto de visión por computadora que detecta gestos con tu mano usando la cámara web y muestra un monito dependiendo del gesto. Hecho en Python con MediaPipe y OpenCV.

---

## 📸 Demo

> *Coloca tus manos frente a la cámara y mira cómo aparece un monito en tiempo real c:*

| Gesto                         | Monito              |
|-------------------------------|---------------------|
| Mano abierta                  | 👋 Mono saludando   |
| Puño cerrado                  | ✊ Mono serio       |
| Solo índice                   | 💡 Mono con idea    |
| Pulgar + índice               | 🤔 Mono pensando    |
| Dos manos arriba de la cabeza | 😲 Mono sorprendido |

---

## 🚀 Instalación

**Requisitos:** Python 3.8 o superior

```bash
# 1. Clona el repositorio
git clone https://github.com/JustBetLogs/monitos_ia.git
cd monitos-ia

# 2. Instala las dependencias
pip install -r requirements.txt

# 3. Ejecuta el proyecto
python main.py
```

Presiona `ESC` para salir.

## 🛠️ Tecnologías usadas

- **Python** — lenguaje principal
- **OpenCV** — captura y visualización de video
- **MediaPipe** — detección de manos en tiempo real
- **NumPy** — procesamiento de imágenes

---

## 🧠 ¿Cómo funciona?

1. La cámara captura el video en tiempo real
2. MediaPipe detecta los puntos de la mano (21 landmarks)
3. Se analiza la posición de cada dedo para identificar el gesto
4. Se muestra el monito correspondiente al lado de la cámara

## 👤 Autor

Hecho por **[Bet]** aún hace falta mucho por mejorar, pero vamos aprendiendo juntos c:
📸 Instagram: [@bet_logs_](https://instagram.com/bet_logs_)

---

> Si te gustó el proyecto, dale una ⭐ — significa mucho para mí ^^