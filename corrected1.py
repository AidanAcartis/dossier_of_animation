import pygame as pg
import cv2

class ArtConverter:

    def __init__(self, path='./Babe.png', font_size=12):
        self.path = path
        self.image = cv2.imread(self.path)  # Charger l'image
        if self.image is None:
            raise ValueError("L'image n'a pas pu être chargée. Vérifie le chemin du fichier.")
        
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # Convertir BGR -> RGB
        #self.image = self.get_image
        # Redimensionner l'image pour qu'elle corresponde à la taille de la fenêtre
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[1], self.image.shape[0]
        self.surface = pg.display.set_mode(self.RES)
        
        # Redimensionner une fois pour la surface (au lieu de chaque appel à draw)
        self.image_resized = cv2.resize(self.image, (self.WIDTH, self.HEIGHT))

        self.clock = pg.time.Clock()

    def get_image(self):
        pass

    def draw(self):
        # Assurez-vous que l'image est redimensionnée uniquement une fois, sinon vous pouvez omettre cela ici
        self.image_resized = self.image_resized.astype('uint8')

        # Transposer l'image pour correspondre à l'ordre attendu par Pygame (hauteur, largeur, canaux)
        # Pygame attend l'ordre (hauteur, largeur, canaux) pour la surface
        image_to_blit = self.image_resized.transpose(1, 0, 2)

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
    app = ArtConverter()  # Correct : on crée une instance de la classe
    app.run()
