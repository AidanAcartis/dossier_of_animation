import pygame as pg
import cv2
import numpy as np

pg.init()
pg.font.init()

class ArtConverter:
    def __init__(self, path='./Oreki.jpg', font_size=12):
        self.path = path
        self.cv2_image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        if self.cv2_image is None:
            raise ValueError("L'image n'a pas pu être chargée. Vérifie le chemin du fichier.")

        self.WIDTH, self.HEIGHT = self.cv2_image.shape[1], self.cv2_image.shape[0]
        self.RES = (self.WIDTH, self.HEIGHT)
        self.surface = pg.display.set_mode(self.RES)

        self.clock = pg.time.Clock()

        self.ASCII_CHARS = '.",:;!~+-xmo*#w&$@'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pg.font.SysFont('Courier', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]

        self.image = self.get_image()

    def get_image(self):
        # Redimensionner l'image en niveaux de gris
        return cv2.resize(self.cv2_image, (self.WIDTH, self.HEIGHT))

    def draw_cv2_image(self):
        # Redimensionner l’image pour affichage OpenCV
        resized_cv2_image = cv2.resize(self.cv2_image, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.imshow('Image en Niveaux de Gris', resized_cv2_image)
        self.surface.fill('black')
        self.draw_converted_image()

    def draw_converted_image(self):
        # Convertir les valeurs des pixels en indices ASCII
        char_indices = self.image // self.ASCII_COEFF
        for y in range(0, self.HEIGHT, self.CHAR_STEP):
            for x in range(0, self.WIDTH, self.CHAR_STEP):
                char_index = char_indices[y, x]  # Correction de l'indexation
                if 0 <= char_index < len(self.RENDERED_ASCII_CHARS):
                    self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))

    def draw(self):
        self.draw_cv2_image()

    def save_image(self):
        """Sauvegarde l'image affichée par pygame sous forme de fichier PNG"""
        pygame_image = pg.surfarray.array3d(pg.display.get_surface())  # Capturer l’écran
        pygame_image = np.transpose(pygame_image, (1, 0, 2))  # Corriger les axes
        cv2_img = cv2.cvtColor(pygame_image, cv2.COLOR_RGB2BGR)  # Convertir Pygame RGB → OpenCV BGR
        cv2.imwrite('./converted_image.png', cv2_img)
        print("Image sauvegardée sous 'converted_image.png'")

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:  # `pg.K_S` en minuscule ne fonctionne pas
                        self.save_image()

            self.draw()
            pg.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")
            pg.display.flip()
            self.clock.tick(30)

        pg.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    app = ArtConverter()
    app.run()
