import cv2
import numpy as np
from pynput.keyboard import Key, Controller
import time
import random
from tkinter import *
import win32api
import win32con
import win32gui
import win32ui
import os
import pyautogui

hwnd = win32gui.FindWindow(None, 'Testoibi - Dofus 2.67.6.8')
keyboard = Controller()
looping = 0
X = 0
Y = 0
nb_victoires = 0

def pret():
    global Y
    x = 0
    while x == 0:
        
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, 1920, 1080)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(1920, 1080) , dcObj, (0,0), win32con.SRCCOPY)
        dataBitMap.SaveBitmapFile(cDC, r"C:\Users\tomde\Documents\python\Dofus\testo.png")
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Chargement des images
        img = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\testo.png")
        template = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\utility_images\pret.png")

        # Récupération de la taille de l'image template
        w, h = template.shape[:-1]

        # Recherche du template dans l'image
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        # Définition d'un seuil de correspondance
        threshold = 0.8

        
        # Récupération des positions des correspondances
        positions = np.where(result >= threshold)

        if len(positions[0]) > 0:
            # Boucle pour dessiner des rectangles autour des correspondances
            for pt in zip(*positions[::-1]):
                # Calcul du centre du rectangle dessiné
                x = round(pt[0] + w/2)
                y = round(pt[1] + h/2)
                
            # Affichage des coordonnées centrales
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x20, 0) 
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x20, 0)
            Y = 0
            print("Prêt!")
        else:
            if Y == 50:
                print("Combat non engagé")
                Y = 0
                background_screenshot(hwnd, 1920, 1080)
            else:
                Y+=1
        
def tour_de_jeu():
    x = 0
    while x == 0:
        
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, 1920, 1080)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(1920, 1080) , dcObj, (0,0), win32con.SRCCOPY)
        dataBitMap.SaveBitmapFile(cDC, r"C:\Users\tomde\Documents\python\Dofus\testo.png")
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Chargement des images
        img = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\testo.png")
        template = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\utility_images\tour_de_jeu.png")

        # Récupération de la taille de l'image template
        w, h = template.shape[:-1]

        # Recherche du template dans l'image
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        # Définition d'un seuil de correspondance
        threshold = 0.8

        
        # Récupération des positions des correspondances
        positions = np.where(result >= threshold)

        if len(positions[0]) > 0:
            # Boucle pour dessiner des rectangles autour des correspondances
            for pt in zip(*positions[::-1]):
                # Calcul du centre du rectangle dessiné
                x = round(pt[0] + w/2)
                y = round(pt[1] + h/2)
                
            # Affichage des coordonnées centrales
            print("Début du tour de jeu!")
        else:
            victoire()

def victoire():
    global nb_victoires

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, 1920, 1080)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(1920, 1080) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, r"C:\Users\tomde\Documents\python\Dofus\testo.png")
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # Chargement des images
    img = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\testo.png")
    template = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\utility_images\level_up.png")

    # Récupération de la taille de l'image template
    w, h = template.shape[:-1]

    # Recherche du template dans l'image
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # Définition d'un seuil de correspondance
    threshold = 0.8

    
    # Récupération des positions des correspondances
    positions = np.where(result >= threshold)

    if len(positions[0]) > 0:
        # Boucle pour dessiner des rectangles autour des correspondances
        for pt in zip(*positions[::-1]):
            # Calcul du centre du rectangle dessiné
            x = round(pt[0] + w/2)
            y = round(pt[1] + h/2)
            
        # Affichage des coordonnées centrales
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
        
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, 1920, 1080)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(1920, 1080) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, r"C:\Users\tomde\Documents\python\Dofus\testo.png")
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # Chargement des images
    img = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\testo.png")
    template = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\utility_images\victoire.png")

    # Récupération de la taille de l'image template
    w, h = template.shape[:-1]

    # Recherche du template dans l'image
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # Définition d'un seuil de correspondance
    threshold = 0.8

    
    # Récupération des positions des correspondances
    positions = np.where(result >= threshold)

    if len(positions[0]) > 0:
        # Boucle pour dessiner des rectangles autour des correspondances
        for pt in zip(*positions[::-1]):
            # Calcul du centre du rectangle dessiné
            x = round(pt[0] + w/2)
            y = round(pt[1] + h/2)
            
        # Affichage des coordonnées centrales
        nb_victoires+=1
        print("Victoire numéro ",nb_victoires,"!")
        print("---------------")
        time.sleep(0.1)
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x0D, 0) 
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x0D, 0)
        background_screenshot(hwnd, 1920, 1080)

def bataille():
    tour_de_jeu()
    déplacement()
    sorts()

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

    bataille()

def déplacement():
    # position mob
    x1 = 0
    while x1 == 0:
        
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, 1920, 1080)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(1920, 1080) , dcObj, (0,0), win32con.SRCCOPY)
        dataBitMap.SaveBitmapFile(cDC, r"C:\Users\tomde\Documents\python\Dofus\testo.png")
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())


        # Chargement des images
        images_folder = r"C:\Users\tomde\Documents\python\Dofus\images_mobs_perso\mobs"
        templates = []
        for filename in os.listdir(images_folder):
            template = cv2.imread(os.path.join(images_folder, filename))
            templates.append(template)
        # Chargement de l'image de la fenêtre
        img = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\testo.png")
        x1 = 0
        for i in range (0,len(templates)):
#changer ici pour cible la plus proche
            if x1 == 0:

                # Récupération de la taille de l'image template
                w, h = templates[i].shape[:-1]

                # Recherche du template dans l'image
                result = cv2.matchTemplate(img, templates[i], cv2.TM_CCOEFF_NORMED)

                # Définition d'un seuil de correspondance
                threshold = 0.8

                
                # Récupération des positions des correspondances
                positions = np.where(result >= threshold)

                if len(positions[0]) > 0:
                    # Boucle pour dessiner des rectangles autour des correspondances
                    for pt in zip(*positions[::-1]):
                        # Calcul du centre du rectangle dessiné
                        x1 = round(pt[0] + w/2)
                        y1 = round(pt[1] + h/2)
                        
                    # Affichage des coordonnées centrales
                    print("Mob identifié")


    #positions perso
    x2 = 0
    while x2 == 0:
        
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, 1920, 1080)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(1920, 1080) , dcObj, (0,0), win32con.SRCCOPY)
        dataBitMap.SaveBitmapFile(cDC, r"C:\Users\tomde\Documents\python\Dofus\testo.png")
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())


        # Chargement des images
        images_folder = r"C:\Users\tomde\Documents\python\Dofus\images_mobs_perso\perso"
        templates = []
        for filename in os.listdir(images_folder):
            template = cv2.imread(os.path.join(images_folder, filename))
            templates.append(template)
        # Chargement de l'image de la fenêtre
        img = cv2.imread(r"C:\Users\tomde\Documents\python\Dofus\testo.png")
        for i in range (0,len(templates)):
            if x2 == 0:

                # Récupération de la taille de l'image template
                w, h = templates[i].shape[:-1]

                # Recherche du template dans l'image
                result = cv2.matchTemplate(img, templates[i], cv2.TM_CCOEFF_NORMED)

                # Définition d'un seuil de correspondance
                threshold = 0.8

                
                # Récupération des positions des correspondances
                positions = np.where(result >= threshold)

                if len(positions[0]) > 0:
                    # Boucle pour dessiner des rectangles autour des correspondances
                    for pt in zip(*positions[::-1]):
                        # Calcul du centre du rectangle dessiné
                        x2 = round(pt[0] + w/2)
                        y2 = round(pt[1] + h/2)
                        
                    # Affichage des coordonnées centrales
                    print("Position du perso identifiée")



    # clic déplacement
    print("Pos mobs/perso:", x1, y1,"/",x2, y2, "Milieu:", round((x1+x2)/2), round((y1+y2)/2))
    print("Déplacement...") 
    for i in range (1, 10):
        time.sleep(random.uniform(0.100,0.200))
        point = (round(x2+(x1-x2)*0.05*i), round(y2+(y1-y2)*0.05*i))
        client_point = win32gui.ScreenToClient(hwnd, point)

        lParam = win32api.MAKELONG(client_point[0], client_point[1])
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
    
    sorts(x1, y1)
              
def combat():
    pret()  
    tour_de_jeu()
    déplacement()

def changements_de_map():
    global X
    maps = [980 , 897, 980 , 897, 1572 , 247, 1572 , 247, 954 , 36, 1572 , 747, 350 , 251, 954 , 36, 355 , 436, 355 , 436]
    if X == len(maps):
        X = 0
    point = (maps[X], maps[X+1])
    client_point = win32gui.ScreenToClient(hwnd, point)
    lParam = win32api.MAKELONG(client_point[0], client_point[1])
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
    print("Changement de map!")
    time.sleep(6)
    X+=2

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
    matching_templates()

def matching_templates():
    # Chargement des images
    images_folder = r"C:\Users\tomde\Documents\python\Dofus\images"
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
                
            # Affichage des coordonnées centrales
            clic_pos(x, y)
    changements_de_map()
    background_screenshot(hwnd, 1920, 1080)

def clic_pos(x,y):
    print("Monstre sauvage aperçu!")
    templates = []
    screen_x, screen_y = x, y
    point = (round(screen_x), round(screen_y))

    
    client_point = win32gui.ScreenToClient(hwnd, point)

    lParam = win32api.MAKELONG(client_point[0], client_point[1])

    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)
    combat()

background_screenshot(hwnd, 1920, 1080)