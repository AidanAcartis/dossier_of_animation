import pygame as pg
import cv2
import numpy as np

pg.init()
pg.font.init()

class ArtConverter:
    def __init__(self, path='./Oreki.jpg', pixel_size=7, color_lvl=8):
        self.path = path
        self.PIXEL_SIZE = pixel_size
        self.COLOR_LVL = color_lvl
        self.image, self.gray_image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[1], self.image.shape[0]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        image = cv2.cvtColor(self.cv2_image, cv2.COLOR_BGR2RGB)
        
        # Convertir l'image en niveaux de gris
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        return image, gray_image  # Retourne les deux images

    def draw_cv2_image(self):
        # Redimensionner l’image pour affichage OpenCV
        resized_cv2_image = cv2.resize(self.cv2_image, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.imshow('Image en Niveaux de Gris', resized_cv2_image)
        self.surface.fill('black')
        self.draw_converted_image()

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
        color_palette = [np.array([r,g,b]) for r in colors for g in colors for b in colors]
        palette = {}
        color_coeff = int(color_coeff)
        for color in color_palette:
            color_key = tuple(color // color_coeff)
            palette[color_key] = color

        return palette, color_coeff

    def draw_converted_image(self):
        color_indices = np.floor_divide(self.image, self.COLOR_COEFF)

        for x in range(0, self.WIDTH, self.PIXEL_SIZE):
            for y in range(0, self.HEIGHT, self.PIXEL_SIZE):
                color_key = tuple(color_indices[y, x])  # Correction ici (x,y)->(y,x)
                if sum(color_key):
                    color = self.PALETTE[color_key]
                    pg.draw.rect(self.surface, color, (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE))  # Use pg.draw.rect here

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
