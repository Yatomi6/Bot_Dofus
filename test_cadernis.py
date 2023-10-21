import cv2
import numpy as np
from PIL import Image
from statistics import mean
import os

x1, y1 = 349, 35    # Coordonnées du coin supérieur gauche
x2, y2 = 1588, 894    # Coordonnées du coin inférieur droit

nouvelle_largeur = 1588 - x1
nouvelle_hauteur = 894 - y1

test = []

# Chargement de l'image
image = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\testo.png")
image_vierge = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\fond_noir.png")
image = image[y1:y2, x1:x2]
image_vierge = cv2.resize(image_vierge, (nouvelle_largeur, nouvelle_hauteur))
#---------------------------------------------------------------------------------------------

# Charger l'image modèle (template)
template_folder = r"C:\Users\tomde\Documents\python\Dofus\images_mobs_perso\mobs"
template_files = os.listdir(template_folder)

# Stocker les positions trouvées
liste_positions_templates = []

for template_file in template_files:
    template_path = os.path.join(template_folder, template_file)
    template = cv2.imread(template_path)

    # Effectuer la correspondance de modèle
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Stocker les positions des correspondances avec une certaine valeur de seuil
    threshold = 0.8
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        liste_positions_templates.append(pt)
print(liste_positions_templates)

liste_positions_test = []
p = 0

for i in liste_positions_templates:
    x, y = liste_positions_templates[p]
    liste_positions_test.append(x)
    liste_positions_test.append(y)
    p += 1

i=-1

while i <= len(liste_positions_test) / 2 - 1:
    i += 1
    k = 0 + i

    while k < len(liste_positions_test) / 2 - 1:
        k+=1
        if abs(int(liste_positions_test[2 * i]-int(liste_positions_test[2*k]))) <= 60 and abs(int(liste_positions_test[2 * i + 1]-int(liste_positions_test[2*k+1]))) <= 30:
            del(liste_positions_test[2*k]); del(liste_positions_test[2*k])
            k -= 1

liste_positions_templates = []

for i in range(0, len(liste_positions_test), 2):
    if i + 1 < len(liste_positions_test):
        liste_positions_templates.append((liste_positions_test[i], liste_positions_test[i + 1]))

print(liste_positions_templates)
#---------------------------------------------------------------------------------------------


# Convertir les couleurs en valeurs numériques BGR
non_walkable_colors_1 = [(52, 75, 79), (57, 82, 87)]
non_walkable_colors_2 = [(104, 98, 68), (71, 101, 106)]
non_walkable_colors_3 = [(40, 58, 61), (40, 59, 61)]

walkable_colors_1 = [(103, 142, 150), (94, 134, 142)]
walkable_colors_2 = [(62, 125, 90), (56, 121, 85)]

# Plage de couleurs autour des couleurs spécifiées
color_tolerance_non_walkable_1 = 14
color_tolerance_non_walkable_2 = 14
color_tolerance_non_walkable_3 = 1
color_tolerance_wakable_1 = 1
color_tolerance_wakable_2 = 1

non_walkable_masks_1 = []
for color in non_walkable_colors_1:
    lower_bound = np.array([max(0, c - color_tolerance_non_walkable_1) for c in color])
    upper_bound = np.array([min(255, c + color_tolerance_non_walkable_1) for c in color])
    mask = cv2.inRange(image, lower_bound, upper_bound)
    non_walkable_masks_1.append(mask)

non_walkable_masks_2 = []
for color in non_walkable_colors_2:
    lower_bound = np.array([max(0, c - color_tolerance_non_walkable_2) for c in color])
    upper_bound = np.array([min(255, c + color_tolerance_non_walkable_2) for c in color])
    mask = cv2.inRange(image, lower_bound, upper_bound)
    non_walkable_masks_2.append(mask)

non_walkable_masks_3 = []
for color in non_walkable_colors_3:
    lower_bound = np.array([max(0, c - color_tolerance_non_walkable_3) for c in color])
    upper_bound = np.array([min(255, c + color_tolerance_non_walkable_3) for c in color])
    mask = cv2.inRange(image, lower_bound, upper_bound)
    non_walkable_masks_3.append(mask)

walkable_masks_1 = []
for color in walkable_colors_1:
    lower_bound = np.array([max(0, c - color_tolerance_wakable_1) for c in color])
    upper_bound = np.array([min(255, c + color_tolerance_wakable_1) for c in color])
    mask = cv2.inRange(image, lower_bound, upper_bound)
    walkable_masks_1.append(mask)

walkable_masks_2 = []
for color in walkable_colors_2:
    lower_bound = np.array([max(0, c - color_tolerance_wakable_2) for c in color])
    upper_bound = np.array([min(255, c + color_tolerance_wakable_2) for c in color])
    mask = cv2.inRange(image, lower_bound, upper_bound)
    walkable_masks_2.append(mask)
    
# Combinaison des masques pour les cases non-marchables et marchables
non_walkable_mask_1 = cv2.bitwise_or(*non_walkable_masks_1)
non_walkable_mask_2 = cv2.bitwise_or(*non_walkable_masks_2)
non_walkable_mask_3 = cv2.bitwise_or(*non_walkable_masks_3)
walkable_mask_1 = cv2.bitwise_or(*walkable_masks_1)
walkable_mask_2 = cv2.bitwise_or(*walkable_masks_2)

# Fusionner les masques des cases non-marchables et marchables
non_walkable_mask_2 = cv2.bitwise_or(non_walkable_mask_3, non_walkable_mask_2)
non_walkable_mask = cv2.bitwise_or(non_walkable_mask_1, non_walkable_mask_2)
walkable_mask = cv2.bitwise_or(walkable_mask_1, walkable_mask_2)
combined_mask = cv2.bitwise_or(non_walkable_mask, walkable_mask)

# Appliquer le masque à l'image pour obtenir les cases non-marchables et marchables
combined_cases = cv2.bitwise_and(image, image, mask=combined_mask)

# Trouver les contours des cases marchables
contours, _ = cv2.findContours(walkable_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

liste_positions_non_wakable = []
liste_positions_wakable = []



# Dessiner les contours en bleu autour des cases marchables
for contour in contours:
    # Récupérer le rectangle englobant (bounding rectangle) du contour
    x, y, w, h = cv2.boundingRect(contour)

    if w > 40 and h > 22:
        # Calculer les coordonnées du losange centré à l'intérieur du rectangle englobant
        diamond_width = 85
        diamond_height = 42
        diamond_x = x + (w - diamond_width) // 2
        diamond_y = y + (h - diamond_height) // 2
        
        # Ajuster les coordonnées x pour qu'elles soient alignées sur des multiples de 42.8
        x_coords = [diamond_x, diamond_x + diamond_width // 2, diamond_y + diamond_width]
        x_aligned = np.round(np.array(x_coords) / 42.81) * 42.81
        diamond_x, _, _ = x_aligned

        # Ajuster les coordonnées y pour qu'elles soient alignées sur des multiples de 21.475
        y_coords = [diamond_y, diamond_y + diamond_height // 2, diamond_y + diamond_height]
        y_aligned = np.round(np.array(y_coords) / 21.475) * 21.475
        diamond_y, _, _ = y_aligned

        liste_positions_wakable.append((diamond_x, diamond_y))
        
        # Dessiner un losange de 85x41 centré à l'intérieur du rectangle englobant
        diamond_points = np.array([
            [diamond_x + diamond_width // 2, diamond_y],
            [diamond_x + diamond_width, diamond_y + diamond_height // 2],
            [diamond_x + diamond_width // 2, diamond_y + diamond_height],
            [diamond_x, diamond_y + diamond_height // 2]
        ], dtype=np.int32)  # Utiliser le dtype=np.int32 pour spécifier le format des coordonnées
        cv2.polylines(combined_cases, [diamond_points], isClosed=True, color=(0, 0, 255), thickness=1)
        cv2.polylines(image_vierge, [diamond_points], isClosed=True, color=(0, 0, 255), thickness=1)

# Trouver les contours des cases non-marchables
contours, _ = cv2.findContours(non_walkable_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:

    cv2.drawContours(combined_cases, [contour], -1, (255, 255, 0), 1)  # Contour bleu
    x, y, w, h = cv2.boundingRect(contour)
    
    if w > 40 and h > 18:

        

        diamond_width = 85
        diamond_height = 42
        diamond_x = x + (w - diamond_width) // 2
        diamond_y = y + (h - diamond_height) // 2

        
        
        x_coords = [diamond_x, diamond_x + diamond_width // 2, diamond_y + diamond_width]
        x_aligned = np.round(np.array(x_coords) / 42.81) * 42.81
        diamond_x, _, _ = x_aligned

        # Ajuster les coordonnées y pour qu'elles soient alignées sur des multiples de 21.475,
        # vers le multiple le plus haut (arrondi vers le haut)
        y_coords = [diamond_y, diamond_y + diamond_height // 2, diamond_y + diamond_height]
        y_aligned = np.ceil(np.array(y_coords)/ 21.475) * 21.475
        diamond_y, _, _ = y_aligned
        
        liste_positions_non_wakable.append((diamond_x, diamond_y))

        diamond_points = np.array([
            [diamond_x + diamond_width // 2, diamond_y],
            [diamond_x + diamond_width, diamond_y + diamond_height // 2],
            [diamond_x + diamond_width // 2, diamond_y + diamond_height],
            [diamond_x, diamond_y + diamond_height // 2]
        ], dtype=np.int32)
        cv2.polylines(combined_cases, [diamond_points], isClosed=True, color=(0, 255, 255), thickness=1)
        cv2.polylines(image_vierge, [diamond_points], isClosed=True, color=(0, 255, 255), thickness=1)

cv2.imwrite('image_contours.png', combined_cases)
cv2.imwrite('image_vierge.png', image_vierge)

# Convertir l'image de format OpenCV à PIL
combined_pil = Image.fromarray(cv2.cvtColor(combined_cases, cv2.COLOR_BGR2RGB))
combined_pil_vierge = Image.fromarray(cv2.cvtColor(image_vierge, cv2.COLOR_BGR2RGB))

# Enregistrer l'image au format PNG
combined_pil.save('image_contours_pil.png')
combined_pil_vierge.save('image_vierge_pil.png')

# Ouvrir l'image avec le lecteur de photos par défaut
combined_pil_vierge.show()

def trouvage_cases(liste_positions):

    liste_positions = list(set(liste_positions))

    liste_cases = []

    for i in range (0, len(liste_positions)):
        x, y = liste_positions[i]
        case_x = round(x / 42.81)
        case_y = round(y / 21.475)
        liste_cases.append((case_x, case_y))
    return liste_cases
    
def converter_cases(liste_cases):
    liste_real_cases = []
    for i in range (0, len(liste_cases)):
        x, y = liste_cases[i]
        real_x = 20 + (x - y) / 2
        real_y = (x - y) / 2 + y -1
        liste_real_cases.append((real_x, real_y))
    return liste_real_cases

def process_tuples(liste_real_cases):
    liste_real_cases_true = []
    for tup in liste_real_cases:
        transformed_tuple = ()
        for item in tup:
            if item.is_integer():
                transformed_tuple += (int(item),)
            else:
                transformed_tuple = None
                break
        if transformed_tuple is not None:
            liste_real_cases_true.append(transformed_tuple)
    
    return liste_real_cases_true

liste_real_cases = converter_cases(trouvage_cases(liste_positions_non_wakable))

liste_real_cases = process_tuples(liste_real_cases)

liste_real_cases = converter_cases(trouvage_cases(liste_positions_wakable))

liste_real_cases = process_tuples(liste_real_cases)
