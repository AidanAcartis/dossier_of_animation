import numpy as np
import matplotlib.pyplot as plt
import cv2

# --- Étape 1 : Convertir un texte en ensemble de points ---
def text_to_points(text, font_scale=1, thickness=2):
    # Création d'une image temporaire pour dessiner le texte
    img = np.zeros((200, 600), dtype=np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, (50, 150), font, font_scale, 255, thickness, cv2.LINE_AA)
    
    # Extraction des contours du texte
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    points = []
    for contour in contours:
        for pt in contour:
            points.append((pt[0][0], pt[0][1]))
    
    # Normalisation des points pour recentrer l'image
    points = np.array(points, dtype=np.float32)
    points -= np.mean(points, axis=0)  # Centrer autour de (0,0)
    
    return points

# --- Étape 2 : Simulation du feu d’artifice ---
def simulate_firework(points, height=100, duration=100):
    num_particles = len(points)
    
    # Initialisation des particules
    positions = np.zeros((num_particles, 2))  # Toutes les particules commencent au même point (0,0)
    velocities = np.random.uniform(-1, 1, (num_particles, 2)) * 2  # Effet aléatoire initial
    velocities[:, 1] += np.random.uniform(8, 12, num_particles)  # Impulsion verticale
    
    # Gravité
    g = 0.2
    
    frames = []
    for t in range(duration):
        # Mise à jour des positions (Lancement + Expansion)
        velocities[:, 1] -= g  # Gravité
        positions += velocities * 0.5  # Mise à jour
        
        # Expansion une fois la hauteur atteinte
        if np.max(positions[:, 1]) > height:
            expansion_factor = 1 - np.exp(-0.05 * (t - duration // 2))
            positions = positions * (1 - expansion_factor) + points * expansion_factor
        
        frames.append(positions.copy())
    
    return frames

# --- Étape 3 : Animation ---
def animate_firework(frames):
    fig, ax = plt.subplots()
    ax.set_xlim(-100, 100)
    ax.set_ylim(0, 150)
    scatter = ax.scatter([], [])
    
    def update(frame):
        scatter.set_offsets(frame)
        return scatter,
    
    from matplotlib.animation import FuncAnimation
    ani = FuncAnimation(fig, update, frames=frames, interval=50)
    plt.show()

# --- Exécution ---
points = text_to_points("Hi!")  # Convertit le texte en points
frames = simulate_firework(points, height=100, duration=100)  # Simule le feu d'artifice
animate_firework(frames)  # Affiche l'animation