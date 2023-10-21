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

x, y = (844, 277)



hwnd = win32gui.FindWindow(None, 'Karie-Rose - Dofus 2.68.5.9')

screen_x, screen_y = x, y
point = (round(screen_x), round(screen_y))


client_point = win32gui.ScreenToClient(hwnd, point)

lParam = win32api.MAKELONG(client_point[0], client_point[1])

win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lParam)

pyautogui.click(x, y)