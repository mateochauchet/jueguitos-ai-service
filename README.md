# ⚽ Jueguitos.AI - Microservicio de IA

Este módulo en Python forma parte de una aplicación que analiza videos de fútbol para contar jueguitos realizados por un usuario.

## 🎯 Funcionalidad

- Detectar la pelota de fútbol en cada frame del video.
- Trackear el movimiento de la pelota.
- Contar cuántos toques se hicieron.
- Devolver un JSON con los resultados.
- (Opcional) Generar un nuevo video con overlay de contador.

## 🚀 Cómo correr el servidor

```bash
uvicorn api.main:app --reload
```

### Visitar:

- http://localhost:8000/ping — para testear si está vivo

- http://localhost:8000/docs — para ver y probar la API

---

### ✅ `models/` (recordatorio)

Voy a colocar acá el modelo de YOLOv8 (ej: `yolov8n.pt` o entrenado custom `pelota.pt`).

---

### ✅ `config.yaml` (opcional)

Más adelante, cuando empiece a meter parámetros como umbrales, paths de modelos, flags para overlay, etc., crear un `config.yaml` con los parámetros del microservicio y centralizar todo ahí.

---
