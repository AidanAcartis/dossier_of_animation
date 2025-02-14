import pygame as pg
import cv2

class ArtConverter:
    def __init__(self, path='./Babe.png', font_size=12):
        self.path = path
        # Charger l'image initialement sans redimensionnement
        self.cv2_image = cv2.imread(self.path)
        if self.cv2_image is None:
            raise ValueError("L'image n'a pas pu être chargée. Vérifie le chemin du fichier.")
        
        # Initialiser les dimensions de l'image après la lecture
        self.WIDTH, self.HEIGHT = self.cv2_image.shape[1], self.cv2_image.shape[0]
        
        # Maintenant on peut redimensionner l'image
        self.image = self.get_image()

        # Redimensionner pour la surface Pygame
        self.RES = self.WIDTH, self.HEIGHT
        self.surface = pg.display.set_mode(self.RES)
        
        self.clock = pg.time.Clock()

    def get_image(self):
        # Convertir l'image de BGR à RGB
        rgb_image = cv2.cvtColor(self.cv2_image, cv2.COLOR_BGR2RGB)
        
        # Redimensionner l'image pour correspondre aux dimensions de la fenêtre
        resized_image = cv2.resize(rgb_image, (self.WIDTH, self.HEIGHT))
        
        return resized_image

    def draw(self):
        # Convertir l'image en uint8 et la transposer pour Pygame
        image_to_blit = self.image.astype('uint8').transpose(1, 0, 2)

        # Blitter l'image sur la surface Pygame
        pg.surfarray.blit_array(self.surface, image_to_blit)

    def run(self):
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(30)

if __name__ == '__main__':
    app = ArtConverter()  # Créer une instance de la classe
    app.run()


        # self.surface.fill('black')
        # self.draw_converted_image()

    # def draw_converted_image(self):
    #     char_indices = self.image // self.ASCII_COEFF
    #     for x in range (0, self.WIDTH, self.CHAR_STEP):
    #         for y in range (0, self.HEIGHT, self.CHAR_STEP):
    #             char_index = char_indices[x,y]
    #             if char_index:
    #                 self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x,y))