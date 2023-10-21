import cv2
import numpy as np
from pynput.keyboard import Key, Controller
import time
import random
from tkinter import *
import win32api
import win32con
import win32gui


keyboard = Controller()
looping = 0
hwndMain = win32gui.FindWindow(None, 'Arbeiten - Dofus 2.66.4.17')

def matching_templates():
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
        # Calcul du centre du rectangle dessiné
        x = round(pt[0] + w/2)
        y = round(pt[1] + h/2)
        
    # Affichage des coordonnées centrales
    print(x, y)

    clic_pos(x, y)
    


def clic_pos(x,y):

    #win32api.PostMessage(hwndMain, win32con.WM_KEYDOWN, 0x46, 0) 
    #win32api.PostMessage(hwndMain, win32con.WM_KEYUP, 0x46, 0)
    #pour voir d autres touches : https://github.com/mariobarbosa777/minwinpy/blob/master/minwinpy.py

    time.sleep(1)

    #coefficient de 0.8 (faire 0.8*positions) (peut-etre que cest juste pour quand c est en full screen)
    screen_x, screen_y = x, y
    point = (round(0.8*screen_x), round(0.8*screen_y))
    client_point = win32gui.ScreenToClient(hwndMain, point)
    lParam = win32api.MAKELONG(client_point[0], client_point[1])

    win32api.PostMessage(hwndMain, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.PostMessage(hwndMain, win32con.WM_LBUTTONUP, None, lParam)

       


matching_templates()
