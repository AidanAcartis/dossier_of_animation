import pygame as pg
import cv2
import numpy as np
import random
import math

pg.init()
pg.font.init()

class FireworkPixelArtEffect:
    def __init__(self, path='./Babe.png', pixel_size=3, scale=2):
        self.path = path
        self.PIXEL_SIZE = pixel_size
        self.SCALE = scale  # Facteur d'agrandissement
        self.image, self.gray_image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[1], self.image.shape[0]
        
        # Nouvelle résolution de la fenêtre
        self.SCALED_RES = (self.WIDTH * self.SCALE, self.HEIGHT * self.SCALE)
        self.surface = pg.display.set_mode(self.SCALED_RES)

        self.clock = pg.time.Clock()
        self.center = (self.WIDTH // 2, self.HEIGHT - 50)  # Point de départ du feu d'artifice
        self.phase = "propulsion"  # On démarre directement par la propulsion  
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
                self.pixels.append({
                    'position': list(self.center),  # Commence au centre  
                    'final_position': (x, y),  # Objectif après explosion  
                    'color': color,
                    'velocity': [0, 0],
                    'size': random.randint(1, 2) * self.SCALE,  # Ajuster la taille des particules
                    'exploded': False
                })
    
    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        image = cv2.cvtColor(self.cv2_image, cv2.COLOR_BGR2RGB)
        return image, cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    def update_pixels(self):
        current_time = pg.time.get_ticks()
        
        if self.phase == "propulsion":
            if self.center[1] < self.explosion_height:
                self.phase = "explosion"
                self.explosion_time = current_time
            else:
                self.center = (self.center[0], self.center[1] - 5)
        
        elif self.phase == "explosion":
            if current_time - self.explosion_time > 2000:
                self.phase = "reconstruction"
            else:
                for pixel in self.pixels:
                    if not pixel['exploded']:
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(2, 5)
                        pixel['velocity'] = [speed * math.cos(angle), speed * math.sin(angle)]
                        pixel['exploded'] = True
                    else:
                        pixel['position'][0] += pixel['velocity'][0]
                        pixel['position'][1] += pixel['velocity'][1]
                        pixel['velocity'][1] += self.gravity

        elif self.phase == "reconstruction":
            all_reached = True  # Vérifier si toutes les particules sont en place
            for pixel in self.pixels:
                x, y = pixel['position']
                fx, fy = pixel['final_position']
                
                # Interpolation exponentielle pour un effet plus naturel
                pixel['position'][0] += (fx - x) * 0.1
                pixel['position'][1] += (fy - y) * 0.1

                # Vérification si une particule n'est pas encore assez proche de sa position finale
                if abs(fx - x) > 0.5 or abs(fy - y) > 0.5:
                    all_reached = False

            # Une fois toutes les particules stabilisées, on reste sur la phase finale
            if all_reached:
                self.phase = "final"

    def draw(self):
        self.surface.fill('black')

        if self.phase == "propulsion":
            pg.draw.circle(self.surface, (255, 255, 255), (self.center[0] * self.SCALE, self.center[1] * self.SCALE), 5 * self.SCALE)
        
        if self.phase != "final":  # Continue d'afficher les pixels pendant la propulsion et l'explosion
            for pixel in self.pixels:
                x, y = pixel['position']
                pg.draw.circle(self.surface, pixel['color'], (int(x * self.SCALE), int(y * self.SCALE)), pixel['size'])
        
        if self.phase == "final":  # Après la phase finale, les pixels restent à leur place
            for pixel in self.pixels:
                x, y = pixel['position']
                pg.draw.circle(self.surface, pixel['color'], (int(x * self.SCALE), int(y * self.SCALE)), pixel['size'])

    def save_image(self):
        """Sauvegarde l'image affichée par pygame sous forme de fichier PNG"""
        pygame_image = pg.surfarray.array3d(pg.display.get_surface())  # Capturer l’écran
        pygame_image = np.transpose(pygame_image, (1, 0, 2))  # Corriger les axes
        cv2_img = cv2.cvtColor(pygame_image, cv2.COLOR_RGB2BGR)  # Convertir Pygame RGB → OpenCV BGR
        cv2.imwrite('./final_firework_image.png', cv2_img)
        print("Image sauvegardée sous 'final_firework_image.png'")

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:  # Sauvegarder l'image finale avec `S`
                        self.save_image()

            self.update_pixels()
            self.draw()
            pg.display.flip()

            # L'animation se termine mais on garde la fenêtre ouverte
            if self.phase == "final":  # On laisse l'affichage jusqu'à fermeture manuelle
                pass

            self.clock.tick(30)

        pg.quit()


if __name__ == '__main__':
    app = FireworkPixelArtEffect(path='./Babe.png', pixel_size=1, scale=2)  # Modifier 'scale' pour agrandir/réduire
    app.run()
