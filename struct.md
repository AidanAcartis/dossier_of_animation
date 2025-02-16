Voici les étapes détaillées pour intégrer ton animation **Pygame** dans une interface web avec **Django**.  

### 📌 **Objectif**  
Créer une application Django qui héberge une page web contenant un **div** dans lequel la fenêtre **Pygame** s'affiche.

---

## 🏗 **1. Installation et Configuration de Django**
### 🔹 **1.1 Créer et configurer un projet Django**  
Dans un terminal, installe Django et crée un projet :

```bash
# Installer Django si ce n'est pas déjà fait
pip install django

# Créer un projet Django nommé "pygame_web"
django-admin startproject pygame_web

# Aller dans le projet
cd pygame_web

# Créer une application Django pour gérer Pygame
python manage.py startapp game
```

---

## 📂 **2. Organisation des fichiers**
Voici la structure du projet :

```
pygame_web/
├── game/                # Application Django pour gérer Pygame
│   ├── migrations/
│   ├── static/          # Dossier pour les fichiers statiques (JS, CSS)
│   ├── templates/       # Dossier pour les templates HTML
│   │   └── index.html   # Page web principale
│   ├── views.py         # Logique de la vue Django
│   ├── urls.py          # Routes spécifiques à l'application
│   ├── video_stream.py  # Script pour exécuter Pygame et envoyer le rendu en vidéo
├── pygame_web/          # Projet Django principal
│   ├── settings.py      # Configuration Django
│   ├── urls.py          # Routes principales du projet
```

---

## 📝 **3. Configuration Django**
### 🔹 **3.1 Ajouter l’application à `settings.py`**
Dans **`pygame_web/settings.py`**, ajoute **game** dans `INSTALLED_APPS` :

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'game',  # Ajout de l'application
]
```

### 🔹 **3.2 Configurer les fichiers statiques**
Toujours dans **`settings.py`**, ajoute :

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "game/static",
]
```

---

## 📄 **4. Création des Fichiers Django**
### 🔹 **4.1 Création du Template HTML**
Dans **`game/templates/index.html`**, crée la page d'affichage :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Firework Pixel Art</title>
    <style>
        body { text-align: center; }
        video { width: 80%; border: 2px solid black; }
    </style>
</head>
<body>
    <h1>Firework Pixel Art Effect</h1>
    <video id="pygame_stream" autoplay></video>

    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const video = document.getElementById("pygame_stream");
            video.src = "/game/video_feed";
        });
    </script>
</body>
</html>
```
👉 **Ce fichier affiche la vidéo streamée par Pygame.**

---

### 🔹 **4.2 Création des Routes**
Dans **`game/urls.py`**, ajoute :

```python
from django.urls import path
from .views import index, video_feed

urlpatterns = [
    path('', index, name='index'),
    path('video_feed', video_feed, name='video_feed'),
]
```

Dans **`pygame_web/urls.py`**, inclure les URLs de l'application **game** :

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')),  # Inclure les routes de l'application
]
```

---

### 🔹 **4.3 Création des Vues**
Dans **`game/views.py`**, ajoute :

```python
from django.shortcuts import render
from django.http import StreamingHttpResponse
from .video_stream import generate_frames

def index(request):
    return render(request, 'index.html')

def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace; boundary=frame")
```

---

## 🎥 **5. Création du Stream Pygame en OpenCV**
On va utiliser **OpenCV** pour capturer l’image Pygame et l’envoyer sous forme de **flux vidéo**.

Crée **`game/video_stream.py`** et ajoute :

```python
import pygame as pg
import cv2
import numpy as np
import random
import math

class FireworkPixelArtEffect:
    def __init__(self, path='./game/static/Babe.png', pixel_size=3, scale=2):
        self.path = path
        self.PIXEL_SIZE = pixel_size
        self.SCALE = scale  
        self.image, self.gray_image = self.get_image()
        self.WIDTH, self.HEIGHT = self.image.shape[1], self.image.shape[0]
        self.SCALED_RES = (self.WIDTH * self.SCALE, self.HEIGHT * self.SCALE)
        self.surface = pg.Surface(self.SCALED_RES)  

        self.clock = pg.time.Clock()
        self.center = [self.WIDTH // 2, self.HEIGHT - 50]  
        self.phase = "propulsion"
        self.start_time = pg.time.get_ticks()
        self.explosion_height = self.HEIGHT // 3 
        self.gravity = 0.05
        self.explosion_time = None
        
        self.pixels = []
        for x in range(0, self.WIDTH, self.PIXEL_SIZE):
            for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
                block = self.image[y:y+self.PIXEL_SIZE, x:x+self.PIXEL_SIZE]
                avg_color = np.mean(block, axis=(0, 1))
                color = tuple(map(int, avg_color))
                self.pixels.append({'position': list(self.center), 'final_position': (x, y), 'color': color})

    def get_image(self):
        cv2_image = cv2.imread(self.path)
        image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        return image, cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    def draw(self):
        self.surface.fill('black')
        for pixel in self.pixels:
            x, y = pixel['position']
            pg.draw.circle(self.surface, pixel['color'], (int(x * self.SCALE), int(y * self.SCALE)), 2)

    def get_frame(self):
        self.draw()
        frame = pg.surfarray.array3d(self.surface)
        frame = np.transpose(frame, (1, 0, 2))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame

def generate_frames():
    app = FireworkPixelArtEffect()
    while True:
        frame = app.get_frame()
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
```

---

## 🚀 **6. Lancer le serveur Django**
Démarrer le serveur Django :

```bash
python manage.py runserver
```

Accéder à **http://127.0.0.1:8000/** et voir le Pygame affiché 🎆🚀

---

## ✅ **Résumé**
1. Installation de Django et création du projet 🏗
2. Configuration des fichiers Django 📂
3. Création d’une page HTML avec un `<video>` 🎥
4. Capture du rendu Pygame et envoi en streaming via OpenCV 🖼
5. Affichage du rendu en temps réel sur Django 🌐

🔹 **Résultat :** Une interface web qui affiche l’animation Pygame en continu via Django ! 🚀🔥