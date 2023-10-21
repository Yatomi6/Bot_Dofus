import cv2
import numpy as np
import win32api
import win32con
import win32ui
import os
import win32gui
from pynput.keyboard import Controller

hwnd = win32gui.FindWindow(None, 'Karie-Rose - Dofus 2.68.5.6')

def background_screenshot(hwnd, width, height):
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, r"C:\Users\tomde\Documents\python\Dofus\testo.png")
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

#background_screenshot(hwnd, 1920, 1080)

image = r"C:\Users\tomde\Documents\python\Dofus\testo.png"

# Charger l'image
image_path = image  # Remplacez par le chemin de votre image
image = cv2.imread(image_path)

# Convertir l'image en noir et blanc
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Utiliser l'algorithme de Canny pour détecter les contours
edges = cv2.Canny(gray_image, 0, 1)

# Trouver les lignes dans l'image à l'aide de la transformée de Hough
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=10, maxLineGap=14)

black = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\blackscreen.png")

# Dessiner les lignes détectées sur une copie de l'image originale
image_with_lines = black.copy()
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(image_with_lines, (x1, y1), (x2, y2), (0, 0, 255), 7)

cv2.imwrite(r"C:\Users\tomde\Documents\python\Dofus\testo_set.png", image_with_lines)

x1, y1 = 349, 35    # Coordonnées du coin supérieur gauche
x2, y2 = 1588, 894    # Coordonnées du coin inférieur droit

nouvelle_largeur = 1588-349
nouvelle_hauteur = 894-40

def matching_templates_folder(dossier):
    liste_positions = []
    x = 0; y = 0; Z = 0
    # Chargement des images
    images_folder = r"C:\Users\tomde\Documents\python\Dofus\{}".format(dossier)
    templates = []
    for filename in os.listdir(images_folder):
        template = cv2.imread(os.path.join(images_folder, filename))
        templates.append(template)
    # Chargement de l'image de la fenêtre
    img = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\testo.png")

    # Définition d'un seuil de correspondance
    threshold = 0.89

    # Boucle pour rechercher les correspondances de chaque template dans l'image
    for template in templates:
        # Récupération de la taille de l'image template
        w, h = template.shape[:-1]

        # Recherche du template dans l'image
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        
        # Récupération des positions des correspondances
        positions = np.where(result >= threshold)

        if len(positions[0]) > 0:
            # Boucle pour dessiner des rectangles autour des correspondances
            for pt in zip(*positions[::-1]):
                # Calcul du centre du rectangle dessiné
                x = round(pt[0] + w/2)
                y = round(pt[1] + h/2)
                liste_positions.append(x), liste_positions.append(y)
                Z+=1
    return x, y, Z, liste_positions # x et y sont les pos de la derniere image trouvée et Z le nombre d'images trouvées

def matching_templates_file(fichier):
    x = 0; y = 0 
    # Chargement des images
    img = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\testo.png")
    template = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\utility_images\{}".format(fichier))

    # Récupération de la taille de l'image template
    w, h = template.shape[:-1]

    # Recherche du template dans l'image
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # Définition d'un seuil de correspondance
    threshold = 0.92

    
    # Récupération des positions des correspondances
    positions = np.where(result >= threshold)

    if len(positions[0]) > 0:
        # Boucle pour dessiner des rectangles autour des correspondances
        for pt in zip(*positions[::-1]):
            # Calcul du centre du rectangle dessiné
            x = round(pt[0] + w/2)
            y = round(pt[1] + h/2)
    
    return x, y

x1, y1, Z, liste_positions = matching_templates_folder("images_mobs_perso\mobs")
print(liste_positions, len(liste_positions), len(liste_positions) / 2 - 1)

i=-1

while i <= len(liste_positions) / 2 - 1:
    i += 1
    k = 0 + i

    while k < len(liste_positions) / 2 - 1:
        k+=1
        if abs(int(liste_positions[2 * i]-int(liste_positions[2*k]))) <= 60 and abs(int(liste_positions[2 * i + 1]-int(liste_positions[2*k+1]))) <= 30:
            del(liste_positions[2*k]); del(liste_positions[2*k])
            k -= 1
print("liste_positions", liste_positions)

real_liste_positions = []
k = 0

for i in liste_positions:
    if k % 2 == 0:
        i -= 349
        real_liste_positions.append(i)
    else:
        i -= 35
        real_liste_positions.append(i)
    k += 1
print("liste_positions reel", real_liste_positions)

if x1 != 0:
    print(int(len(real_liste_positions) / 2), "mobs identifiés")
for i in range (0, int(len(real_liste_positions) / 2)):
    if abs(round(real_liste_positions[2 * i] / 85.62, 3) - round(real_liste_positions[2 * i] / 85.62)) < 0.25:
        case_x = round(real_liste_positions[2 * i] / 85.62)
    else:
        case_x = round(real_liste_positions[2 * i] / 85.62) + 0.5

    if abs(round(real_liste_positions[2 * i + 1] / 42.95 + 0.15, 3) - round(real_liste_positions[2 * i + 1] / 42.95 + 0.15)) < 0.25:
        case_y = round(real_liste_positions[2 * i + 1] / 42.95)
    else:
        case_y = round(real_liste_positions[2 * i + 1] / 42.95) + 0.5

    print("case", case_x, case_y)