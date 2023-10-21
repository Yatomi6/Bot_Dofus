import cv2
import numpy as np
from pynput.keyboard import Controller
import time
import random
from tkinter import *
import win32api
import win32con
import win32gui
import win32ui
import os
from PIL import Image

facteur_click = 0.8

hwnd = win32gui.FindWindow(None, 'Karie-Rose - Dofus 2.69.3.5')
keyboard = Controller()
looping = 0
X = 0
Y = 0
boucles = 0
nb_victoires = 0
en_combat = 0

position_personnage = (1, 2) #par défaut pour initialiser la variable

facteur_click = 0.8

# permet de replacer la souris, de la "réintialiser"
def empty_click():
    # coordonnées de replacement
    point = (round(1475 * facteur_click), round(193 * facteur_click))
    client_point = win32gui.ScreenToClient(hwnd, point)
    lParam = win32api.MAKELONG(client_point[0], client_point[1])
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)

def test_en_combat():
    # prend un screenshot
    background_screenshot(hwnd, 1920, 1080)

    # attribue une valeur à cette variable si l'image en combat est repérée
    x, y = matching_templates_file("en_combat.png")

    # donc si x est différent de None -> je suis en combat
    if x != 0: en_combat = 1
    # sinon je ne suis pas en combat
    else: en_combat = 0
    # je retourne si je suis en combat ou pas
    return en_combat
        
def laby(liste_real_cases_mobs, liste_real_cases_wakable, liste_real_cases_perso):
    import pygame

    class Node:
        def __init__(self, position, parent=None):
            self.position = position
            self.parent = parent
            self.g = 0
            self.h = 0

        def __lt__(self, other):
            return (self.g + self.h) < (other.g + other.h)
    #Algorithme
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

    # Pour rendu visuel
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
     # Mets de base des obstacles partout
    for i in range (0, 32):
        for k in range (0, 33):
            obstacles.append((i, k))

    # Change les cases obstacles concernées en cases wakables
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

        # Placer les obstacles et les cases wakables dans la grille du labyrinthe en faisant attention à ce qu'ils soient bien dans la map 33*34
        for obstacle in obstacles:
            if 0 <= obstacle[0] < len(maze) and 0 <= obstacle[1] < len(maze[0]):
                maze[obstacle[0]][obstacle[1]] = 1

        for good in cases_good:
            if 0 <= good[0] < len(maze) and 0 <= good[1] < len(maze[0]):
                maze[good[0]][good[1]] = 0

        # Placer les monstre et le perso dans la grille du labyrinthe en faisant attention à ce qu'ils soient bien dans la map 33*34
        for good in liste_real_cases_mobs:
            if 0 <= good[0] < len(maze) and 0 <= good[1] < len(maze[0]):
                maze[good[0]][good[1]] = 0
        for good in liste_real_cases_wakable:
            if 0 <= good[0] < len(maze) and 0 <= good[1] < len(maze[0]):
                maze[good[0]][good[1]] = 0
  

        # Trouver le chemin vers la destination actuelle avec l'algorithme
        path = astar(maze, start, end)

        # Choisis le chemin le plus court si plusieurs ennemis
        if path and len(path) < shortest_distance:
            shortest_distance = len(path)
            shortest_path = path

    # Indique dans la console le chemin le plus court trouvé par l'algo
    if shortest_path:

        # Supprimer la case de départ de la liste qui correspond à la position du personnage
        del shortest_path[0]

        print("Chemin le plus court trouvé:", shortest_path)
        other_ends = [end_position for end_position in ends if end_position != shortest_path[-1]]
        other_ends.append(shortest_path[-1])  # Ajouter la fin la plus courte à la liste des autres ends
        #draw_maze_with_pygame(maze, shortest_path, other_ends)
        return(shortest_path)
    else:
        print("Aucun chemin trouvé")
        return None

def path_finding(position_personnage):

    # prend un screenshot de la fenêtre DOFUS
    background_screenshot(hwnd, 1920, 1080)

    # Etablit un cadre de la fenetre de combat
    x1, y1 = 349, 35    # Coordonnées du coin supérieur gauche
    x2, y2 = 1588, 894    # Coordonnées du coin inférieur droit

    # Récupeère les dimensions de cette nouvelle fenetre
    nouvelle_largeur = 1588 - x1
    nouvelle_hauteur = 894 - y1

    # Chargement du screenshot
    image = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\testo.png")
    image_vierge = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\fond_noir.png")
    # Je redimensionne le screenshot
    image = image[y1:y2, x1:x2]
    image_vierge = cv2.resize(image_vierge, (nouvelle_largeur, nouvelle_hauteur))


    # Repérage des mobs
    #---------------------------------------------------------------------------------------------
    # Charge le dossier des images modèles
    template_folder = r"C:\Users\tomde\Documents\python\Dofus\images_mobs_perso\mobs"
    template_files = os.listdir(template_folder)

    # Initialisation de la liste pour stocker les positions trouvées
    liste_positions_mobs = []

    # Fait la reconnaissance d'images
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

    # Change les tuples de positions en 2 valeurs distinctes
    liste_positions_rearangement = []
    for i in liste_positions_mobs:
        liste_positions_rearangement.append(i[0])
        liste_positions_rearangement.append(i[1])

    # Si différentes positions sont trop proches, n'en garde qu'une pour éviter plusieurs coordonnées différentes pour le même monstre
    i=-1
    while i <= len(liste_positions_rearangement) / 2 - 1:
        i += 1
        k = 0 + i

        while k < len(liste_positions_rearangement) / 2 - 1:
            k+=1
            if abs(int(liste_positions_rearangement[2 * i]-int(liste_positions_rearangement[2*k]))) <= 60 and abs(int(liste_positions_rearangement[2 * i + 1]-int(liste_positions_rearangement[2*k+1]))) <= 30:
                del(liste_positions_rearangement[2*k]); del(liste_positions_rearangement[2*k])
                k -= 1

    # Remets les valeurs restantes dans la liste origniale sous forme de tuples
    liste_positions_mobs = []
    for i in range(0, len(liste_positions_rearangement), 2):
        if i + 1 < len(liste_positions_rearangement):
            liste_positions_mobs.append((liste_positions_rearangement[i], liste_positions_rearangement[i + 1]))
    #---------------------------------------------------------------------------------------------

    # repérage perso
    #---------------------------------------------------------------------------------------------
    # Charge le dossier des images modèles
    template_folder = r"C:\Users\tomde\Documents\python\Dofus\images_mobs_perso\perso"
    template_files = os.listdir(template_folder)

    # Initialisation de la liste pour stocker les positions trouvées
    liste_positions_perso = []

    # Fait la reconnaissance d'images
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
            liste_positions_perso.append(pt)

    # Si des coordonnées on effectivement été trouvées:
    if len(liste_positions_perso) != 0:
        # Change les tuples de positions en 2 valeurs distinctes
        liste_positions_rearangement = []
        for i in liste_positions_perso:
            liste_positions_rearangement.append(i[0])
            liste_positions_rearangement.append(i[1] + 5) # + 5 pour éviter des erreurs où le personnage n'est pas vu comme sur une case

        # Si différentes positions sont trop proches, n'en garde qu'une pour éviter plusieurs coordonnées différentes pour le même monstre
        i=-1
        while i <= len(liste_positions_rearangement) / 2 - 1:
            i += 1
            k = 0 + i

            while k < len(liste_positions_rearangement) / 2 - 1:
                k+=1
                if abs(int(liste_positions_rearangement[2 * i]-int(liste_positions_rearangement[2*k]))) <= 60 and abs(int(liste_positions_rearangement[2 * i + 1]-int(liste_positions_rearangement[2*k+1]))) <= 30:
                    del(liste_positions_rearangement[2*k]); del(liste_positions_rearangement[2*k])
                    k -= 1

        # Remets les valeurs restantes dans la liste origniale sous forme de tuples
        liste_positions_perso = []
        for i in range(0, len(liste_positions_rearangement), 2):
            if i + 1 < len(liste_positions_rearangement):
                liste_positions_perso.append((liste_positions_rearangement[i], liste_positions_rearangement[i + 1]))

    # Sinon attribue au perso les coodonnées par défaut ou celle du tour dernier
    else :
        liste_positions_perso = []
        liste_positions_perso.append(position_personnage)
    #---------------------------------------------------------------------------------------------

    # Repérage des différentes cases de la map combat

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

    # Initialisations
    liste_positions_non_wakable = []
    liste_positions_wakable = []

    # Pour avoir un rendu visuel
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
    for x, y in liste_positions_mobs:
        # Attribue une case en fonction de la largeur et de la hauteur de chaque case
        case_x = (x) // 42.81
        case_y = (y) // 21.475
        
        # si les deux cases additionnées ne sont pas paires (mauvais placements) alors baisser la case verticale de 1 (problème observé souvent, reconnaissance d'image trop haute)
        if (case_x + case_y) // 2 == 1:
            print("Test parité:",case_x, case_y)
            case_y += 1

        # En fonction de ces cases, donne des coordonnées pour pouvoir dessiner les positions
        x = (round(case_x * 42.81 + 42.81)); y = (round(case_y * 21.475 + 21.475))

        # Dessiner un cercle marron correspondant à un monstre
        cv2.circle(image_vierge, (x, y), 10, (0, 100, 200), -1)

        liste_positions_mobss.append((round(case_x * 42.81), round(case_y * 21.475)))


    liste_positions_persos = []
    for x, y in liste_positions_perso:

        case_x = (x) // 42.81
        case_y = (y) // 21.475

        # si les deux cases additionnées ne sont pas paires (mauvais placements) alors baisser la case verticale de 1 (problème observé souvent, reconnaissance d'image trop haute)
        if (case_x + case_y) // 2 == 1:
            case_y += 1

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

    print("Positions et case Mobs:",liste_positions_mobs , liste_real_cases_mobs)
    print("Positions et case Perso", liste_positions_perso, liste_real_cases_perso)

    # Algorithme de pathfinding pour trouver la chemin le plus court enter perso et mob
    shortest_path = laby(liste_real_cases_mobs, liste_real_cases_wakable, liste_real_cases_perso)

    # Si un chemin a bien été trouvé
    if shortest_path != None:

        # Remet des cases de l'algo en cases du jeu
        def inverse_converter_cases(shortest_path):
            liste_cases_deplacements = []
            for i in range (0, len(shortest_path)):
                x, y = shortest_path[i]
                real_y = y - 18 + x
                real_x = 22 - y + x
                liste_cases_deplacements.append((real_y, real_x))
            return liste_cases_deplacements

        # Remet des cases du jeu en position en pixel
        def cases_to_coords(liste_cases_deplacements):
            liste_positions_deplacements = []
            for i in range (0, len(liste_cases_deplacements)):
                x, y = liste_cases_deplacements[i]
                real_x = round(x * 42.81 - 42.81 / 2 + 349); real_y = round(y * 21.475 - 21.475 / 2 + 35)
                liste_positions_deplacements.append((real_x, real_y))
            return liste_positions_deplacements

        liste_cases_deplacements = inverse_converter_cases(shortest_path)
        liste_positions_deplacements = cases_to_coords(liste_cases_deplacements)

        if len(shortest_path) >= 4:
            screen_x, screen_y = facteur_click * liste_positions_deplacements[2][0], facteur_click * liste_positions_deplacements[2][1]
        elif len(shortest_path) == 3:
            screen_x, screen_y = facteur_click * liste_positions_deplacements[-2][0], facteur_click * liste_positions_deplacements[-2][1]
        elif len(shortest_path) == 2:
            screen_x, screen_y = facteur_click * liste_positions_deplacements[-2][0], facteur_click * liste_positions_deplacements[-2][1]
        elif len(shortest_path) == 1:
            screen_x, screen_y = liste_positions_perso[0]
        
        point = (round(screen_x), round(screen_y))
        
        client_point = win32gui.ScreenToClient(hwnd, point)

        lParam = win32api.MAKELONG(client_point[0], client_point[1])

        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        time.sleep(0.1)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)

        return round(facteur_click * liste_positions_deplacements[-1][0]), round(facteur_click * liste_positions_deplacements[-1][1]), (screen_x / facteur_click, screen_y / facteur_click)
    
    else:
        return 1, 4, (liste_positions_perso[0])

def pret():

    # la boucle va etre faite 80 fois
    for i in range (0, 50):

        # je cherche si je suis en combat, c.a.d. si j'ai bien lancé le combat en cliquant sur le groupe de mobs
        en_combat = test_en_combat()

        # si c'est le cas:
        if en_combat:
            # j'appuie sur espace pour accepter le challenge
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x20, 0) 
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x20, 0)
            # j'attends un peu
            time.sleep(random.uniform(0.2, 0.5))
            # j'appuie sur espace pour se mettre prêt
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x20, 0) 
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x20, 0)
            print("Challenge choisi et prêt!")
            # mets fin à la fonction, le personnage est pret, le combat est donc commencé
            return en_combat

        # sinon j'attends un dixième de seconde et je recommence la boucle for
        # cela permet alors d'attendre 8 secondes que le combat se lance
        else:
            time.sleep(0.1)

    # si le combat n'est pas lancé, un l'indique et on le retourne
    print("Combat non engagé")
    return en_combat

def tour_de_jeu():
    # j'initialise une variable x
    x = 0
    while x == 0:

        # prend un screenshot de l'écran DOFUS        
        background_screenshot(hwnd, 1920, 1080)

        # si l'image du commencement de mon tour de jeu est visible, alors j'attribue une autre valuer à x autre que 0
        x, y = matching_templates_file("tour_de_jeu.png")
        
        # et dans ce cas là j'indique dans la console le début de mon tour de jeu
        if x != 0:
            print("Début du tour de jeu!")

        # sinon, pour ne pas attendre éternellement, je regarde si je suis effectivement en combat à attendre mon tour
        else:
            # de ce fait si je ne suis pas en combat x va prendre la valeur de 0
            x = test_en_combat()
            # à laquelle je vais rajouter 1 pour ne pas retomber dans la boucle while
            x -= 1

def test_victoire(boucles):

    # garde en mémoire le nombre de victoires
    global nb_victoires

    # prend un screenshot de la fenetre DOFUS
    background_screenshot(hwnd, 1920, 1080)

    # attribue une valeur à x si la fenetre de level up est repérée
    x, y = matching_templates_file("level_up.png")
    # dans ce cas:
    if x != 0:
        # ça l'indique dans la console
        print("---------------")
        print("---------------")
        print("---------------")
        print("Level Up!")
        print("---------------")
        print("---------------")
        print("---------------")
        # et ça appuie sur échap pour enlever la fenetre
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x0D, 0) 
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x0D, 0)
        # attend un peu le temps que la fenetre de level up ne soit plus visible
        time.sleep(0.3)
    
    # reprend un screenshot de l'écran
    background_screenshot(hwnd, 1920, 1080)

    # attribue une valeur à x si l'onglet de victoire de combat est repéré
    x, y = matching_templates_file("victoire.png")
    # si c'est le cas
    if x != 0:
        # incrémente de 1 le nombre de victoire
        nb_victoires+=1
        # l'indique dans la console
        print("Nombre de boucles effectuées:", boucles)
        print("Victoire numéro ",nb_victoires,"!")
        print("-------------------------------")
        # et ça appuie sur échap pour enlever l'onglet
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x0D, 0) 
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x0D, 0)

def sorts(x1, y1):

    time.sleep(random.uniform(0.100, 0.300))

    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x5A, 0) 
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x5A, 0)
    time.sleep(random.uniform(0.100, 0.200))

    point = (x1, y1)
    client_point = win32gui.ScreenToClient(hwnd, point)
    lParam = win32api.MAKELONG(client_point[0], client_point[1])
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
    time.sleep(random.uniform(0.200, 0.300))

    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x5A, 0) 
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x5A, 0)
    time.sleep(random.uniform(0.200, 0.300))

    point = (x1, y1)
    client_point = win32gui.ScreenToClient(hwnd, point)
    lParam = win32api.MAKELONG(client_point[0], client_point[1])
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
    time.sleep(random.uniform(0.200, 0.300))

    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x20, 0) 
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x20, 0)

    empty_click()

def déplacements_astar(position_personnage):
    # lance la fonction de pathfinding
    x1, y1, position_personnage = path_finding(position_personnage)
    # fais un click pour reset les actions de la souris
    empty_click()
    return x1, y1, position_personnage, x   
             
def changements_de_map():
    global X
    maps = [980 , 897, 980 , 897, 1572 , 247, 1572 , 247, 954 , 36, 1572 , 747, 350 , 251, 954 , 36, 355 , 436, 355 , 436]
    if X == len(maps):
        X = 0
    point = (round(facteur_click * maps[X]), round(facteur_click * maps[X+1]))
    client_point = win32gui.ScreenToClient(hwnd, point)
    lParam = win32api.MAKELONG(client_point[0], client_point[1])
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
    print("Changement de map!")
    time.sleep(6)
    X+=2

def mob_trouvé(dossier):
    alors, nb_mobs = clic_pos_folder(dossier)
    if alors:
        print("Mobs trouvés!")
        return 1
    else:
        return 0


def matching_templates_folder(dossier):
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
    threshold = 0.92

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
                Z+=1
    return x, y, Z # x et y sont les pos de la derniere image trouvée et Z le nombre d'images trouvées

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

def clic_pos_folder(dossier):
    x, y, Z = matching_templates_folder(dossier)
    if x != 0:
        templates = []
        screen_x, screen_y = facteur_click * x, facteur_click * y
        point = (round(screen_x), round(screen_y))
       
        client_point = win32gui.ScreenToClient(hwnd, point)

        lParam = win32api.MAKELONG(client_point[0], client_point[1])

        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
        return 1, Z
    else:
        return 0, Z

def clic_pos_file(file):
    x, y = matching_templates_file(file)
    if x != 0:
        templates = []
        screen_x, screen_y = facteur_click * x, facteur_click * y
        point = (round(screen_x), round(screen_y))

        
        client_point = win32gui.ScreenToClient(hwnd, point)

        lParam = win32api.MAKELONG(client_point[0], client_point[1])

        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
        return 1
    else:
        return 0

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


# boucle infinie
while 1:
    # compteur de boucles
    boucles += 1

    # fais un screenshot de la fenetre dofus
    background_screenshot(hwnd, 1920, 1080)

    # je regarde si je suis en_combat
    en_combat = test_en_combat()
    # check si un combat a été gagné (et si level up en passant)
    test_victoire(boucles)
    # je regarde après à nouveau si je suis en combat au cas où les onglets de victoire cachaient une partie de l'écran
    en_combat = test_en_combat()

    # si je suis en combat:
    if en_combat:
        # je cherche quand c'est à mon tour de jouer
        tour_de_jeu()
        # j'attends un peu au cas où la fin de combat mette du temps à se dérouler
        time.sleep(1.2)
        # je revérifie si je suis toujours bien en combat
        en_combat = test_en_combat()
        # si je suis effectivement toujours en combat:
        if en_combat:
            # je cherche ma position et celle des monstres, et je me déplace vers celui le plus proche
            # je récupère les variables x1, y1, position_personnage, en_combat; 
            # respectivement la position du monstre en x et en y, le tuple de la position de mon perso et si je suis en combat
            x1, y1, position_personnage, en_combat = déplacements_astar(position_personnage)

            en_combat = test_en_combat()
            # Et si je suis effectivement toujours en combat:
            if en_combat:
                # je lance mes sorts sur l'ennemi le plus proche
                sorts(x1, y1)
                time.sleep(0.5)

    # mais si je ne suis pas en combat
    else:
        # check si un combat a été gagné (et si level up en passant)
        test_victoire(boucles)
        # je cherche des groupes de monstres sur la map
        x = mob_trouvé("images_mobs")
        # si j'en ai trouvé:
        if x:
            # je clique dessus
            clic_pos_folder("images_mobs")
            # j'attends d'être prêt
            pret()

        # si je n'ai pas trouvé de groupe de monstres:
        else:
            # je l'indique dans la console et je change de map
            print("Pas de groupe de mobs trouvé")
            changements_de_map()
