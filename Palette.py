import pygame as pg
import cv2
import numpy as np

pg.init()
pg.font.init()

class ArtConverter:
    def __init__(self, path='./Oreki.jpg', font_size=12, color_lvl=8):
        self.path = path
        self.COLOR_LVL = color_lvl
        self.cv2_image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        if self.cv2_image is None:
            raise ValueError("L'image n'a pas pu être chargée. Vérifie le chemin du fichier.")

        self.WIDTH, self.HEIGHT = self.cv2_image.shape[1], self.cv2_image.shape[0]
        self.RES = (self.WIDTH, self.HEIGHT)
        self.surface = pg.display.set_mode(self.RES)

        self.clock = pg.time.Clock()

        self.ASCII_CHARS = 'ixzao*uMk&8%B#$'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pg.font.SysFont('Courier', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

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

    # def draw_converted_image(self):
    #     # Convertir les valeurs des pixels en indices ASCII
    #     char_indices = self.image // self.ASCII_COEFF
    #     color_indices = self.gray_image // self.COLOR_COEFF
    #     # for y in range(0, self.HEIGHT, self.CHAR_STEP):
    #     #     for x in range(0, self.WIDTH, self.CHAR_STEP):
    #     #         char_index = char_indices[y, x]  # Correction de l'indexation
    #     #         if 0 <= char_index < len(self.RENDERED_ASCII_CHARS):
    #     #             self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))
    #     for x in range (0, self.WIDTH, self.CHAR_STEP):
    #         for y in range(0, self.HEIGHT, self.CHAR_STEP):
    #             char_index = char_indices[x,y]
    #             if char_index:
    #                 char = self.ASCII_CHARS[char_index]
    #                 color = tuple(color_indices[x,y])
    #                 self.surface.blit(self.PALETTE[char], [color], (x,y))

    def draw_converted_image(self):
        # Convertir les valeurs des pixels en indices ASCII
        char_indices = self.image // self.ASCII_COEFF
        color_indices = self.cv2_image // self.COLOR_COEFF  # Remplace self.gray_image par self.cv2_image
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[y, x]  # Correction de l'indexation
                if 0 <= char_index < len(self.RENDERED_ASCII_CHARS):
                    char = self.ASCII_CHARS[char_index]
                    color_value = color_indices[y, x]  # Gray value for color
                    color = (color_value, color_value, color_value)  # Make it grayscale RGB
                    
                    # Retrieve the correct rendered ASCII surface based on the char and color
                    rendered_char_surface = self.PALETTE[char].get(tuple(color), None)

                    if rendered_char_surface:
                        self.surface.blit(rendered_char_surface, (x, y))

    def draw(self):
        self.draw_cv2_image()

    def save_image(self):
        """Sauvegarde l'image affichée par pygame sous forme de fichier PNG"""
        pygame_image = pg.surfarray.array3d(pg.display.get_surface())  # Capturer l’écran
        pygame_image = np.transpose(pygame_image, (1, 0, 2))  # Corriger les axes
        cv2_img = cv2.cvtColor(pygame_image, cv2.COLOR_RGB2BGR)  # Convertir Pygame RGB → OpenCV BGR
        cv2.imwrite('./converted_image.png', cv2_img)
        print("Image sauvegardée sous 'converted_image.png'")

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = {char: {} for char in self.ASCII_CHARS}
        color_coeff = int(color_coeff)

        for char in self.ASCII_CHARS:
            for color in color_palette:
                color_key = tuple(color // color_coeff)
                palette[char][color_key] = self.font.render(char, False, tuple(color))  # Correction ici

        return palette, color_coeff

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
