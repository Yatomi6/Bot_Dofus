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

chemin_dossier = r"C:\Users\tomde\Documents\Bot Dofus\Photos Matching Templates"
fichiers = os.listdir(chemin_dossier)

hwnd = win32gui.FindWindow(None, 'Arbeiten - Dofus 2.66.4.17')
keyboard = Controller()
looping = 0


def background_screenshot(hwnd, width, height):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x59, 0)
    time.sleep(1)
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, r"C:\Users\tomde\Desktop\test.png")
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x59, 0)
    matching_templates()

def matching_templates():
    global fichiers
    for i in range (len(fichiers)):
        # Chargement des images
        img = cv2.imread(r"C:\Users\tomde\Desktop\test.png")
        print(os.path.join("C:/Users/tomde/Documents/Bot Dofus/Photos Matching Templates", fichiers[i]))
        template = cv2.imread(os.path.join("C:/Users/tomde/Documents/Bot Dofus/Photos Matching Templates", fichiers[i]))

        # Récupération de la taille de l'image template
        w, h = template.shape[:-1]

        # Recherche du template dans l'image
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        # Définition d'un seuil de correspondance
        threshold = 0.98

        indices = np.where(result >= threshold)

        # Vérifier si la liste d'indices n'est pas vide
        if len(indices[0]) > 0:

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

    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x10, 0) 
    

    time.sleep(1)

    #coefficient de 0.8 (faire 0.8*positions) (peut-etre que cest juste pour quand c est en full screen)
    screen_x, screen_y = x, y
    point = (round(0.8*screen_x), round(0.8*screen_y))
    client_point = win32gui.ScreenToClient(hwnd, point)
    lParam = win32api.MAKELONG(client_point[0], client_point[1])

    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)

    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x10, 0)

background_screenshot(hwnd, 1920, 1080)