import pygame as pg
import cv2

class ArtConverter:
    def __init__(self, path='./Babe.png', font_size=12):
        self.path = path
        self.image = cv2.imread(self.path)  # Charger l'image
        if self.image is None:
            raise ValueError("L'image n'a pas pu être chargée. Vérifie le chemin du fichier.")
        
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # Convertir BGR -> RGB

        # Vérification du nombre de canaux
        if self.image.shape[2] != 3:
            raise ValueError("L'image doit avoir 3 canaux (RGB).")
        
        # Afficher la description des propriétés de l'image
        self.describe_image()

        # Redimensionner l'image pour qu'elle corresponde à la taille de la fenêtre
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[1], self.image.shape[0]
        self.surface = pg.display.set_mode(self.RES)
        
        self.clock = pg.time.Clock()

    def describe_image(self):
        # Afficher les propriétés de l'image
        print("Propriétés de l'image :")
        print(f"Dimensions de l'image (largeur x hauteur) : {self.image.shape[1]} x {self.image.shape[0]}")
        print(f"Nombre de canaux (RGB) : {self.image.shape[2]}")
        print(f"Type de données de l'image : {self.image.dtype}")
        print(f"Type de l'image (avant redimensionnement) : {self.image.shape}")

    def draw(self):
        # Redimensionner l'image pour qu'elle corresponde exactement aux dimensions de la fenêtre
        image_resized = cv2.resize(self.image, (self.WIDTH, self.HEIGHT))
        
        # Vérifier les dimensions de l'image redimensionnée
        if image_resized.shape[0] != self.HEIGHT or image_resized.shape[1] != self.WIDTH:
            raise ValueError("Les dimensions de l'image redimensionnée ne correspondent pas à celles de la surface.")
        
        # S'assurer que l'image redimensionnée est dans le bon format
        image_resized = image_resized.astype('uint8')

        # Transposer l'image pour correspondre à l'ordre attendu par Pygame (hauteur, largeur, canaux)
        image_resized = image_resized.transpose(1, 0, 2)

        # Vérifier que les dimensions de l'image redimensionnée correspondent à la surface
        pg.surfarray.blit_array(self.surface, image_resized)

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
