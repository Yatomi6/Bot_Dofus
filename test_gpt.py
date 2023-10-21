import cv2
from PIL import Image
import numpy as np

# Charger l'image
image = Image.open(r"C:\Users\tomde\Documents\python\Dofus\testo.png")

# Convertir en niveaux de gris
image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

# Appliquer un filtre de contour
edges = cv2.Canny(image_gray, threshold1=90, threshold2=60)  # Utiliser la détection de contours de OpenCV

# Fermeture morphologique pour reconnecter les lignes
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
edges_closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# Convertir en image PIL
edges_pil = Image.fromarray(edges_closed)

# Afficher l'image
edges_pil.show()

# Enregistrer l'image
edges_pil.save("chemin_vers_sortie.png")