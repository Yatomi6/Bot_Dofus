import cv2
import numpy as np
from PIL import Image
import os
import win32gui
import win32ui
import win32con
import win32api
import time

hwnd = win32gui.FindWindow(None, 'Karie-Rose - Dofus 2.68.5.9')
facteur_click = 0.8

def laby(liste_real_cases_mobs, liste_real_cases_wakable, liste_real_cases_perso):
    import heapq
    import pygame

    class Node:
        def __init__(self, position, parent=None):
            self.position = position
            self.parent = parent
            self.g = 0
            self.h = 0

        def __lt__(self, other):
            return (self.g + self.h) < (other.g + other.h)

    def astar(maze, start, end):
        open_list = []
        closed_set = set()
        start_node = Node(start)
        end_node = Node(end)
        
        open_list.append(start_node)
        
        while open_list:
            current_node = min(open_list, key=lambda node: node.g + node.h)
            open_list.remove(current_node)
            
            if current_node.position == end_node.position:
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]
            
            closed_set.add(current_node.position)
            
            neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in neighbors:
                new_position = (current_node.position[0] + dx, current_node.position[1] + dy)
                
                if new_position[0] < 0 or new_position[0] >= len(maze) or new_position[1] < 0 or new_position[1] >= len(maze[0]):
                    continue
                if maze[new_position[0]][new_position[1]] == 1:
                    continue
                if new_position in closed_set:
                    continue
                
                new_node = Node(new_position, current_node)
                new_node.g = current_node.g + 1
                new_node.h = abs(new_position[0] - end_node.position[0]) + abs(new_position[1] - end_node.position[1])
                
                existing_open_node = next((node for node in open_list if node.position == new_node.position), None)
                if existing_open_node:
                    if new_node.g < existing_open_node.g:
                        existing_open_node.g = new_node.g
                        existing_open_node.parent = new_node.parent
                else:
                    open_list.append(new_node)
        
        return None


    def draw_maze_with_pygame(maze, path=None, other_ends=None):
        pygame.init()

        TILE_SIZE = 20  # Modifiez cette valeur pour ajuster la taille des cases
        WIDTH = len(maze[0]) * TILE_SIZE
        HEIGHT = len(maze) * TILE_SIZE

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Labyrinthe Solver")

        clock = pygame.time.Clock()

        wall_color = (0, 0, 0)
        path_color = (0, 0, 255)
        start_color = (0, 255, 0)
        end_color = (255, 0, 0)
        other_ends_color = (255, 0, 0)  # Couleur pour les autres ends

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            screen.fill((255, 255, 255))

            # Dessiner les obstacles
            for y, row in enumerate(maze):
                for x, tile in enumerate(row):
                    if tile == 1:
                        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, wall_color, tile_rect)

            if path:
                # Dessiner le chemin
                for y, x in path:
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, path_color, tile_rect)

            # Dessiner le point de départ et d'arrêt
            start_rect = pygame.Rect(start[1] * TILE_SIZE, start[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, start_color, start_rect)

            end_rect = pygame.Rect(end[1] * TILE_SIZE, end[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, end_color, end_rect)

            # Dessiner les autres ends en carrés rouges
            if other_ends:
                for end_position in other_ends:
                    tile_rect = pygame.Rect(end_position[1] * TILE_SIZE, end_position[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, other_ends_color, tile_rect)

            # Dessiner le quadrillage en dernier
            for y in range(len(maze)):
                for x in range(len(maze[0])):
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, (0, 0, 0), tile_rect, 1)

            pygame.display.flip()
            clock.tick(30)

    # Définir les coordonnées du départ, de l'arrivée et des obstacles
    start = liste_real_cases_perso[0]
    ends = liste_real_cases_mobs

    obstacles = []
    cases_good = []

    for i in range (0, 32):
        for k in range (0, 33):
            obstacles.append((i, k))

    for i in liste_real_cases_wakable:
        cases_good.append(i)

    # Trouver le chemin vers la destination la plus proche
    shortest_path = None
    shortest_distance = float('inf') 

    for end in ends:
 
        maze = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # Placer les obstacles et les cases traversables dans la grille du labyrinthe
        for obstacle in obstacles:
            if 0 <= obstacle[0] < len(maze) and 0 <= obstacle[1] < len(maze[0]):
                maze[obstacle[0]][obstacle[1]] = 1

        for good in cases_good:
            if 0 <= good[0] < len(maze) and 0 <= good[1] < len(maze[0]):
                maze[good[0]][good[1]] = 0

        for good in liste_real_cases_mobs:
            if 0 <= good[0] < len(maze) and 0 <= good[1] < len(maze[0]):
                maze[good[0]][good[1]] = 0
        for good in liste_real_cases_wakable:
            if 0 <= good[0] < len(maze) and 0 <= good[1] < len(maze[0]):
                maze[good[0]][good[1]] = 0
  

        # Trouver le chemin vers la destination actuelle
        path = astar(maze, start, end)

        if path and len(path) < shortest_distance:
            shortest_distance = len(path)
            shortest_path = path

    # Afficher le chemin le plus court trouvé dans la fenêtre pygame
    if shortest_path:
        #supprimer la case de départ de la liste
        del shortest_path[0]

        print("Chemin le plus court trouvé:", shortest_path)
        other_ends = [end_position for end_position in ends if end_position != shortest_path[-1]]
        other_ends.append(shortest_path[-1])  # Ajouter la fin la plus courte à la liste des autres ends
        #draw_maze_with_pygame(maze, shortest_path, other_ends)
        return(shortest_path)
    else:
        print("Aucun chemin trouvé")
        return None


def main(position_personnage):

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

    hwnd = win32gui.FindWindow(None, 'Karie-Rose - Dofus 2.68.5.9')
    background_screenshot(hwnd, 1920, 1080)


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


    # repérage mobs
    #---------------------------------------------------------------------------------------------

    # Charger l'image modèle (template)
    template_folder = r"C:\Users\tomde\Documents\python\Dofus\images_mobs_perso\mobs"
    template_files = os.listdir(template_folder)

    # Stocker les positions trouvées
    liste_positions_mobs = []

    for template_file in template_files:
        template_path = os.path.join(template_folder, template_file)
        template = cv2.imread(template_path)

        # Effectuer la correspondance de modèle
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Stocker les positions des correspondances avec une certaine valeur de seuil
        threshold = 0.9
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
            liste_positions_mobs.append(pt)

    liste_positions_rearangement = []
    p = 0

    for i in liste_positions_mobs:
        x, y = liste_positions_mobs[p]
        liste_positions_rearangement.append(x)
        liste_positions_rearangement.append(y)
        p += 1

    i=-1

    while i <= len(liste_positions_rearangement) / 2 - 1:
        i += 1
        k = 0 + i

        while k < len(liste_positions_rearangement) / 2 - 1:
            k+=1
            if abs(int(liste_positions_rearangement[2 * i]-int(liste_positions_rearangement[2*k]))) <= 60 and abs(int(liste_positions_rearangement[2 * i + 1]-int(liste_positions_rearangement[2*k+1]))) <= 30:
                del(liste_positions_rearangement[2*k]); del(liste_positions_rearangement[2*k])
                k -= 1

    liste_positions_mobs = []

    for i in range(0, len(liste_positions_rearangement), 2):
        if i + 1 < len(liste_positions_rearangement):
            liste_positions_mobs.append((liste_positions_rearangement[i], liste_positions_rearangement[i + 1]))

    #---------------------------------------------------------------------------------------------

    # repérage perso
    #---------------------------------------------------------------------------------------------
    
    # Charger l'image modèle (template)
    template_folder = r"C:\Users\tomde\Documents\python\Dofus\images_mobs_perso\perso"
    template_files = os.listdir(template_folder)

    # Stocker les positions trouvées
    liste_positions_perso = []

    for template_file in template_files:
        template_path = os.path.join(template_folder, template_file)
        template = cv2.imread(template_path)

        # Effectuer la correspondance de modèle
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Stocker les positions des correspondances avec une certaine valeur de seuil
        threshold = 0.93
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
            liste_positions_perso.append(pt)

    if len(liste_positions_perso) != 0:

        liste_positions_rearangement = []
        p = 0

        for i in liste_positions_perso:
            x, y = liste_positions_perso[p]
            liste_positions_rearangement.append(x)
            liste_positions_rearangement.append(y)
            p += 1

        i=-1

        while i <= len(liste_positions_rearangement) / 2 - 1:
            i += 1
            k = 0 + i

            while k < len(liste_positions_rearangement) / 2 - 1:
                k+=1
                if abs(int(liste_positions_rearangement[2 * i]-int(liste_positions_rearangement[2*k]))) <= 60 and abs(int(liste_positions_rearangement[2 * i + 1]-int(liste_positions_rearangement[2*k+1]))) <= 30:
                    del(liste_positions_rearangement[2*k]); del(liste_positions_rearangement[2*k])
                    k -= 1

        liste_positions_perso = []

        for i in range(0, len(liste_positions_rearangement), 2):
            if i + 1 < len(liste_positions_rearangement):
                liste_positions_perso.append((liste_positions_rearangement[i], liste_positions_rearangement[i + 1]))

    else :
        liste_positions_perso = []
        liste_positions_perso.append(position_personnage)


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

    liste_positions_mobss = []
    print("list mob", liste_positions_mobs)
    for x, y in liste_positions_mobs:

        case_x = (x) // 42.81
        case_y = (y) // 21.475
        

        print("case_x et case_y test paire",case_x, case_y)
        # si les deux cases additionnées ne sont pas parires (mauvais palcements) alors baisser la case verticale de 1 (problème observé souvent, reconnaissance d'image trop haute)
        if (case_x + case_y) // 2 == 1:
            case_y += 1

        x = (round(case_x * 42.81 + 42.81)); y = (round(case_y * 21.475 + 21.475))

        # Dessiner un cercle marron
        cv2.circle(image_vierge, (x, y), 10, (0, 100, 200), -1)  # Utiliser la couleur marron en BGR

        liste_positions_mobss.append((round(case_x * 42.81), round(case_y * 21.475)))


    liste_positions_persos = []
    print("list perso", liste_positions_perso)
    for x, y in liste_positions_perso:

        case_x = (x) // 42.81
        case_y = (y) // 21.475

        x = (round(case_x * 42.81 + 42.81)); y = (round(case_y * 21.475 + 21.475))

        # Dessiner un cercle blanc
        cv2.circle(image_vierge, (x, y), 10, (255, 255, 200), -1)  # Utiliser la couleur blanc en BGR

        liste_positions_persos.append((round(case_x * 42.81), round(case_y * 21.475)))


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
    #combined_pil.show()

    # Ouvrir l'image avec le lecteur de photos par défaut
    #combined_pil_vierge.show()

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
            liste_real_cases.append((real_y, real_x))
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

    liste_real_cases_non_wakable = converter_cases(trouvage_cases(liste_positions_non_wakable))

    liste_real_cases_non_wakable = process_tuples(liste_real_cases_non_wakable)

    liste_real_cases_wakable = converter_cases(trouvage_cases(liste_positions_wakable))

    liste_real_cases_wakable = process_tuples(liste_real_cases_wakable)


    liste_real_cases_mobs = converter_cases(trouvage_cases(liste_positions_mobss))

    liste_real_cases_mobs = process_tuples(liste_real_cases_mobs)

    liste_real_cases_perso = converter_cases(trouvage_cases(liste_positions_persos))

    liste_real_cases_perso = process_tuples(liste_real_cases_perso)

    # Nom du fichier
    file_name = "start.txt"

    # Écriture dans le fichier
    with open(file_name, "w") as file:
        file.write(str(liste_real_cases_perso[0]))

    print("Positions Mobs:",liste_positions_mobs , ". Cases des mobs", liste_real_cases_mobs)
    #print("Liste des cases walkables:", liste_real_cases_wakable)
    print("Positions Perso", liste_positions_perso,". Case du personnage", liste_real_cases_perso)

    shortest_path = laby(liste_real_cases_mobs, liste_real_cases_wakable, liste_real_cases_perso)

    if shortest_path != None:

        def inverse_converter_cases(shortest_path):
            liste_cases_deplacements = []
            for i in range (0, len(shortest_path)):
                x, y = shortest_path[i]
                real_y = y - 18 + x
                real_x = 22 - y + x
                liste_cases_deplacements.append((real_y, real_x))
            return liste_cases_deplacements

        def cases_to_coords(liste_cases_deplacements):
            liste_positions_deplacements = []
            for i in range (0, len(liste_cases_deplacements)):
                x, y = liste_cases_deplacements[i]
                real_x = round(x * 42.81 - 42.81 / 2 + 349); real_y = round(y * 21.475 - 21.475 / 2 + 35)
                liste_positions_deplacements.append((real_x, real_y))
            return liste_positions_deplacements

            
        liste_cases_deplacements = inverse_converter_cases(shortest_path)

        liste_positions_deplacements = cases_to_coords(liste_cases_deplacements)
        #faire en sorte que si case pas dans les 33*34, tuple supprimé

        if len(shortest_path) >= 3:
            screen_x, screen_y = facteur_click * liste_positions_deplacements[2][0], facteur_click * liste_positions_deplacements[2][1]
        elif len(shortest_path) == 2:
            screen_x, screen_y = facteur_click * liste_positions_deplacements[1][0], facteur_click * liste_positions_deplacements[1][1]
        elif len(shortest_path) == 1:
            screen_x, screen_y = facteur_click * liste_positions_deplacements[0][0], facteur_click * liste_positions_deplacements[0][1]
        point = (round(screen_x), round(screen_y))

        print((round(screen_x), round(screen_y)))

        
        client_point = win32gui.ScreenToClient(hwnd, point)

        lParam = win32api.MAKELONG(client_point[0], client_point[1])

        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.1)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)

        return round(facteur_click * liste_positions_deplacements[-1][0]), round(facteur_click * liste_positions_deplacements[-1][1]), (screen_x, screen_y)
    
    else:
        if globals().get("screen_x") is not None:
            return 1, 1, (screen_x, screen_y)
        else:
            return 1, 1, (1, 2)
        
main((1,2))