import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

def image_to_points(image_path, threshold=100):
    # Charger l'image en niveaux de gris
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (300, 300))  # Redimensionner pour simplifier

    # Détection des contours
    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extraction des points
    points = []
    for contour in contours:
        for pt in contour:
            points.append((pt[0][0], pt[0][1]))

    points = np.array(points, dtype=np.float32)
    points -= np.mean(points, axis=0)  # Centrer l'image

    return points

# --- Affichage scintillant ---
def animate_sparkling(points, frames=50):
    fig, ax = plt.subplots()
    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)
    scatter = ax.scatter([], [], s=5, c=[])

    def update(frame):
        colors = [(random.random(), random.random(), random.random()) for _ in points]
        scatter.set_offsets(points)
        scatter.set_color(colors)
        return scatter,

    from matplotlib.animation import FuncAnimation
    ani = FuncAnimation(fig, update, frames=frames, interval=100)
    plt.show()

# --- Exécution ---
points = image_to_points("Babe.png")
animate_sparkling(points)
