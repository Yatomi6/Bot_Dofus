import cv2
import numpy as np

# Chargement des images
img = cv2.imread(r"C:\Users\tomde\Desktop\test.png")
template = cv2.imread(r"C:\Users\tomde\Desktop\feca.png")

# Récupération de la taille de l'image template
w, h = template.shape[:-1]

# Recherche du template dans l'image
result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

# Définition d'un seuil de correspondance
threshold = 0.8

# Récupération des positions des correspondances
positions = np.where(result >= threshold)

# Boucle pour dessiner des rectangles autour des correspondances
for pt in zip(*positions[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

# Affichage de l'image avec les rectangles dessinés
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
