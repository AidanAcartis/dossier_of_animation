from PIL import Image

def remove_background(input_image_path, output_image_path, bg_color=(255, 255, 255)):
    # Ouvrir l'image
    img = Image.open(input_image_path).convert("RGBA")
    
    # Obtenir les données de l'image
    data = img.getdata()
    
    # Liste pour stocker les nouveaux pixels
    new_data = []
    
    for item in data:
        # Vérifier si le pixel est de la couleur de l'arrière-plan
        if item[:3] == bg_color:
            # Si c'est la couleur de fond, rendre le pixel transparent
            new_data.append((255, 255, 255, 0))
        else:
            # Sinon, garder le pixel original
            new_data.append(item)
    
    # Appliquer les nouveaux pixels à l'image
    img.putdata(new_data)
    
    # Sauvegarder l'image modifiée
    img.save(output_image_path)

# Exemple d'utilisation
remove_background("heart.png", "image_no_background.png", bg_color=(255, 255, 255))  # Suppression du fond blanc
