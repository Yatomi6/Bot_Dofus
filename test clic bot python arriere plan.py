from pynput.keyboard import Key, Controller
import time
import random
from tkinter import *
import win32api
import win32con
import win32gui

keyboard = Controller()
looping = 0
hwndMain = "10158754"


#win32api.PostMessage(hwndMain, win32con.WM_KEYDOWN, 0x46, 0) 
#win32api.PostMessage(hwndMain, win32con.WM_KEYUP, 0x46, 0)

time.sleep(1)

#coefficient de 0.8 (faire 0.8*positions)
screen_x, screen_y = 1451 , 587
point = (round(0.8*screen_x), round(0.8*screen_y))
client_point = win32gui.ScreenToClient(hwndMain, point)
lParam = win32api.MAKELONG(client_point[0], client_point[1])

win32api.PostMessage(hwndMain, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
win32api.PostMessage(hwndMain, win32con.WM_LBUTTONUP, None, lParam)

       
