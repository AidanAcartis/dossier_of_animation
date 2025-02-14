import pygame as pg
import cv2
import numpy as np

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

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        image = cv2.cvtColor(self.cv2_image, cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image, gray_image

    def draw_pixel_art(self):
        # Réduire l'image à une faible résolution
        for x in range(0, self.WIDTH, self.PIXEL_SIZE):
            for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
                # Extraire la couleur moyenne du bloc de pixels
                block = self.image[y:y+self.PIXEL_SIZE, x:x+self.PIXEL_SIZE]
                avg_color = np.mean(block, axis=(0, 1))  # Moyenne de la couleur dans le bloc

                # Convertir la couleur moyenne en couleur RGB
                color = tuple(map(int, avg_color))
                
                # Dessiner un cercle (point) avec la couleur moyenne
                center = (x + self.PIXEL_SIZE // 2, y + self.PIXEL_SIZE // 2)
                pg.draw.circle(self.surface, color, center, self.PIXEL_SIZE // 2)  # Rayon plus petit pour ressembler à un point

    def draw(self):
        self.surface.fill('black')
        self.draw_pixel_art()

    def save_image(self):
        """Sauvegarde l'image affichée par pygame sous forme de fichier PNG"""
        pygame_image = pg.surfarray.array3d(pg.display.get_surface())  # Capturer l’écran
        pygame_image = np.transpose(pygame_image, (1, 0, 2))  # Corriger les axes
        cv2_img = cv2.cvtColor(pygame_image, cv2.COLOR_RGB2BGR)  # Convertir Pygame RGB → OpenCV BGR
        cv2.imwrite('./pixel_art_image.png', cv2_img)
        print("Image sauvegardée sous 'pixel_art_image.png'")

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
