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

from fusion_labyrinthe_cadernis import main


facteur_click = 0.8

hwnd = win32gui.FindWindow(None, 'Karie-Rose - Dofus 2.68.5.9')
keyboard = Controller()
looping = 0
X = 0
Y = 0
boucles = 0
nb_victoires = 0
en_combat = 0

position_personnage = (1, 2) #par défaut pour initialiser la variable

def empty_click():
    point = (1475 , 193)
    client_point = win32gui.ScreenToClient(hwnd, point)
    lParam = win32api.MAKELONG(client_point[0], client_point[1])
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)

def pret(en_combat):
    global Y
    if en_combat == 0:
        x = 0
        while x == 0:
            
            background_screenshot(hwnd, 1920, 1080)

            x, y = matching_templates_file("choisir_les_challenges.png")

            if x != 0:
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x20, 0) 
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x20, 0)
                time.sleep(random.uniform(0.2, 0.5))
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x20, 0) 
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x20, 0)
                Y = 0
                print("Challenge choisi et prêt!")
                en_combat = 1
                return en_combat
            else:
                if Y == 60:
                    print("Combat non engagé")
                    Y = 0
                    x = 1
                    return en_combat
                else:
                    Y+=1
          
def tour_de_jeu():
    x = 0
    while x == 0:
        
        background_screenshot(hwnd, 1920, 1080)

        x, y = matching_templates_file("tour_de_jeu.png")
        
        if x != 0:
            print("Début du tour de jeu!")

        x = victoire()
    return x

def victoire():
    global nb_victoires

    background_screenshot(hwnd, 1920, 1080)

    x, y = matching_templates_file("level_up.png")
    if x != 0:
        print("---------------")
        print("---------------")
        print("---------------")
        print("Level Up!")
        print("---------------")
        print("---------------")
        print("---------------")
        time.sleep(0.1)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x0D, 0) 
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x0D, 0)
        time.sleep(0.3)
        
    background_screenshot(hwnd, 1920, 1080)
    x = 0
    x, y = matching_templates_file("victoire.png")
    if x != 0:
        nb_victoires+=1
        print("Victoire numéro ",nb_victoires,"!")
        print("---------------")
        time.sleep(0.1)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x0D, 0) 
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x0D, 0)
        return 0
    else:
        x = 0
        x, y = matching_templates_file("hors_combat.png")
        if x != 0:
            return 0
        return 1

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
    time.sleep(1)
    background_screenshot(hwnd, 1920, 1080)
    x = victoire()
    if x == 1:
        x1, y1, position_personnage = main(position_personnage)
        empty_click()
        return x1, y1, position_personnage, x
    else:
        return 0, 0, position_personnage, x
    

def déplacement():
    # position mob
    x1 = 0
    while x1 == 0:
        
        background_screenshot(hwnd, 1920, 1080)

        x1, y1 ,Z = matching_templates_folder("images_mobs_perso\mobs")
        
        if x1 != 0:
            print(Z, "mobs identifiés")
        else:
            print("Aucun mob identifié")
            empty_click()
            x1 = abs(1-victoire())

    #positions perso
    x2 = 0
    while x2 == 0:
        
        x2, y2 ,Z = matching_templates_folder("images_mobs_perso\perso")
        
        if x2 != 0:
            print(Z, "persos identifiés")
        else:
            print("Aucun perso identifié")
            empty_click()
            x2 = abs(1-victoire())

    # clic déplacement
    print("Pos mobs/perso:", x1, y1,"/",x2, y2)
    for i in range (1, 10):
        time.sleep(random.uniform(0.100,0.200))
        point = (round(x2+(x1-x2)*0.05*i), round(y2+(y1-y2)*0.05*i))
        client_point = win32gui.ScreenToClient(hwnd, point)
        lParam = win32api.MAKELONG(client_point[0], client_point[1])
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
    
    return x1, y1

              
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
        print(nb_mobs, "mobs trouvés")
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
    threshold = 0.9

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
    threshold = 0.9

    
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

        print((round(screen_x), round(screen_y)))

        
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

while 1:
    # doit définir x et y avec des valeurs randoms
    x = 1; y = 1
    boucles += 1

    background_screenshot(hwnd, 1920, 1080)
    if en_combat:
        en_combat = victoire()

    if en_combat != 0: 
        en_combat = tour_de_jeu()
        if en_combat != 0:
            print("position personnage:", round(position_personnage[0]), round(position_personnage[1]))
            x1, y1, position_personnage, en_combat = déplacements_astar(position_personnage)
            if en_combat != 0:
                sorts(x1, y1)
                time.sleep(0.5)

        
    else:
        x = mob_trouvé("images_mobs")
        if x == 1:
            clic_pos_folder("images_mobs")
            en_combat = pret(en_combat)
            if en_combat == 1:
                pret(en_combat)
        else:
            print("Pas de mob trouvé")
            changements_de_map()

    print("Nombre de boucles effectuées:", boucles)