import pygame as pg
import cv2
import numpy as np
import random
import math

pg.init()
pg.font.init()

class PixelArtEffect:
    def __init__(self, path='./Babe.png', pixel_size=3):  # Taille de pixel réduite
        self.path = path
        self.PIXEL_SIZE = pixel_size
        self.image, self.gray_image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[1], self.image.shape[0]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        # Initialisation des "pixels" comme étoiles
        self.pixels = []
        for x in range(0, self.WIDTH, self.PIXEL_SIZE):
            for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
                block = self.image[y:y+self.PIXEL_SIZE, x:x+self.PIXEL_SIZE]
                avg_color = np.mean(block, axis=(0, 1))  # Moyenne de la couleur dans le bloc
                color = tuple(map(int, avg_color))

                # Ajouter chaque "pixel" comme une étoile à animer
                self.pixels.append({
                    'position': (x + self.PIXEL_SIZE // 2, y + self.PIXEL_SIZE // 2),
                    'color': color,
                    'velocity': [0, 0],  # Pas de mouvement initial
                    'size': random.randint(1, 3),  # Taille aléatoire pour chaque "étoile"
                    'lifetime': 200,  # Durée de vie avant disparition
                    'time_to_move': pg.time.get_ticks() + 10000  # Temps avant le début du mouvement (10 secondes)
                })

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        image = cv2.cvtColor(self.cv2_image, cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Appliquer un masque pour transformer l'arrière-plan en noir (par exemple, tout ce qui est clair devient noir)
        # Ici, nous transformons les pixels qui sont assez proches du blanc (ou une couleur claire) en noir
        lower_bound = np.array([200, 200, 200])  # Limite inférieure de la couleur "blanche"
        upper_bound = np.array([255, 255, 255])  # Limite supérieure de la couleur "blanche"

        # Créer un masque pour les pixels proches du blanc
        mask = cv2.inRange(image, lower_bound, upper_bound)

        # Appliquer ce masque pour remplacer l'arrière-plan par du noir
        image[mask != 0] = [0, 0, 0]  # Remplacer les pixels du masque par du noir

        return image, gray_image


    def draw_firework(self):
        current_time = pg.time.get_ticks()  # Obtenir le temps actuel en millisecondes
        for pixel in self.pixels:
            x, y = pixel['position']
            color = pixel['color']
            velocity = pixel['velocity']
            size = pixel['size']
            lifetime = pixel['lifetime']
            time_to_move = pixel['time_to_move']

            # Si 10 secondes sont écoulées, commencer à déplacer l'étoile
            if current_time >= time_to_move:
                pixel['velocity'] = [random.uniform(-1, 1), random.uniform(-1, 1)]

            # Mise à jour de la position de l'étoile (effet de feu d'artifice)
            pixel['position'] = (x + velocity[0], y + velocity[1])

            # Réduction de la taille de l'étoile avec le temps
            new_size = max(1, size - 0.05)

            # Animation : dégradé de couleur au fil du temps (scintillement)
            color = (
                max(0, min(255, color[0] + random.randint(-5, 5))),
                max(0, min(255, color[1] + random.randint(-5, 5))),
                max(0, min(255, color[2] + random.randint(-5, 5)))
            )

            # Dessiner l'étoile (petit cercle)
            pg.draw.circle(self.surface, color, (int(x), int(y)), int(new_size))

            # Réduire la durée de vie de l'étoile
            pixel['lifetime'] -= 1
            if pixel['lifetime'] <= 0:
                # Réinitialiser les propriétés de l'étoile quand elle "disparaît"
                pixel['position'] = (random.randint(0, self.WIDTH), random.randint(0, self.HEIGHT))
                pixel['velocity'] = [random.uniform(-1, 1), random.uniform(-1, 1)]
                pixel['size'] = random.randint(1, 3)
                pixel['lifetime'] = random.randint(50, 100)
                pixel['time_to_move'] = current_time + 5000  # Reset time to move after reset

    def draw(self):
        self.surface.fill('black')  # Fond noir pour l'effet de feu d'artifice
        self.draw_firework()

    def save_image(self):
        """Sauvegarde l'image affichée par pygame sous forme de fichier PNG"""
        pygame_image = pg.surfarray.array3d(pg.display.get_surface())  # Capturer l’écran
        pygame_image = np.transpose(pygame_image, (1, 0, 2))  # Corriger les axes
        cv2_img = cv2.cvtColor(pygame_image, cv2.COLOR_RGB2BGR)  # Convertir Pygame RGB → OpenCV BGR
        cv2.imwrite('./pixel_art_firework.png', cv2_img)
        print("Image sauvegardée sous 'pixel_art_firework.png'")

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:  # Sauvegarder l'image avec `S`
                        self.save_image()

            self.draw()
            pg.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")
            pg.display.flip()
            self.clock.tick(30)

        pg.quit()

if __name__ == '__main__':
    app = PixelArtEffect(path='./Babe.png', pixel_size=3)  # Réduire la taille des pixels
    app.run()
