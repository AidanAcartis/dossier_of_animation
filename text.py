import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def text_to_points(text, font_scale=2, thickness=3):
    img = np.zeros((200, 600), dtype=np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, (50, 150), font, font_scale, 255, thickness, cv2.LINE_AA)

    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    points = []
    for contour in contours:
        for pt in contour:
            points.append((pt[0][0], pt[0][1]))

    points = np.array(points, dtype=np.float32)
    points -= np.mean(points, axis=0)

    return points

def animate_points(points):
    fig, ax = plt.subplots()
    ax.set_facecolor('black')
    ax.set_xlim(-300, 300)
    ax.set_ylim(-100, 100)
    ax.axis("off")
    
    scatter = ax.scatter([], [], s=2, color='white', alpha=0.5)

    def update(frame):
        alphas = np.random.uniform(0.2, 1, len(points))  # Variation de la transparence pour l'effet scintillant
        scatter.set_offsets(points)
        scatter.set_alpha(alphas)
        return scatter,

    ani = FuncAnimation(fig, update, frames=100, interval=100, blit=True)
    plt.show()

# --- Exécution ---
points = text_to_points("Hello")
animate_points(points)
