import time
from tkinter import *
import pyautogui
import mouse
import os
from collections import OrderedDict
import random
 
window = Tk()
window.title("DOFUS BOT")
window.configure(bg="#FFFFFF")
window.geometry ( '750x500' )

width = window.winfo_width(); height = window.winfo_height()

nbTour = IntVar(); maj = IntVar(); boucle = IntVar(); x=0; p=0; y=0; t=0; nbCombat=0
positions=[]; positions_de_clicks=[]; positions_clean=[]; exceptions=["\n"]; positions_recup=[]; positions_lambda=[]

def on_click(x, y, button, pressed):
    if not pressed:
        # Exécutez votre code ici
        print("Cliquez à l'emplacement x: {0} y: {1}".format(x, y))

def remove_duplicates_with_exceptions(positions, exceptions):
    positions_clean = [item for i, item in enumerate(positions) if item not in positions[:i] or item in exceptions]

def quitter():
    window.destroy()

def refresh_trajets():
    trajets.delete(0, END)
    os.chdir(r"C:\Users\tomde\Documents\Bot Dofus")
    trajet_file = [x.replace('.txt', '') for x in os.listdir()]
    for item in trajet_file:
        trajets.insert(0, item)

def creer_trajet():
    window.iconify()
    global positions

    window_creation_trajet = Toplevel(window)

    window_creation_trajet.title("Création Trajet")
    window_creation_trajet.configure(bg="#FFFFFF")
    
    window_creation_trajet.geometry ( '1860x800+25+40' )
    window_creation_trajet.attributes('-alpha',0.5)

    width_creation = window_creation_trajet.winfo_width(); heightcreation = window_creation_trajet.winfo_height()

    v = StringVar()

    def enregistrer_trajet():
        positions.pop()
        if positions[-1]=="bas" or positions[-1]=="haut" or positions[-1]=="droite" or positions[-1]=="gauche" or positions[-1]=="temps" or positions[-1]=="noMaj":
                positions.pop()
        
        nom_fichier = file_name.get()  
        open(r"C:\Users\tomde\Documents\Bot Dofus\lambda.txt",'w')
        os.rename(r"C:\Users\tomde\Documents\Bot Dofus\lambda.txt", os.path.join(r"C:\Users\tomde\Documents\Bot Dofus", nom_fichier+".txt"))
        test = open(os.path.join(r"C:\Users\tomde\Documents\Bot Dofus", nom_fichier+".txt"), "a")
        for i in positions:
            if i == "haut":
                test.write("haut\n")
            elif i == "bas":
                test.write("bas\n")
            elif i == "droite":
                test.write("droite\n")
            elif i == "gauche":
                test.write("gauche\n")
            elif i == "noMaj":
                test.write("noMaj\n")
            elif i == "temps":
                test.write("temps\n")
            else:
                test.write(str(i)+"\n")
        test.close()
        file_name.delete(0, END)
        refresh_trajets()
        positions.clear()
        window.deiconify()
        window_creation_trajet.destroy()

    def clic_transition():
        if len(positions)!=0:
            positions.pop()
            print(positions)

    def clic_delete_last():
        v.set(None)
        if len(positions)!=0:
            if positions[-2]=="bas" or positions[-2]=="haut" or positions[-2]=="droite" or positions[-2]=="gauche":
                positions.pop(), positions.pop()
                print(positions)
            else:
                positions.pop()
                print(positions)
        
    def clic(event):
        global positions
        
        if len(positions)>=1:
            if positions[-1]=="bas" or positions[-1]=="haut" or positions[-1]=="droite" or positions[-1]=="gauche" or positions[-1]=="temps" or positions[-1]=="noMaj":
                positions.pop()           
        if v.get()=="ressource":
            positions.append(mouse.get_position())
            remove_duplicates_with_exceptions       #supprime les mêmes éléments de la liste  
            print(positions)
        if v.get()=="bas":
            positions.append("bas")
            positions.append(mouse.get_position())
            remove_duplicates_with_exceptions       #supprime les mêmes éléments de la liste
            print(positions)
        if v.get()=="haut":
            positions.append("haut")
            positions.append(mouse.get_position())
            remove_duplicates_with_exceptions       #supprime les mêmes éléments de la liste
            print(positions)
        if v.get()=="droite":
            positions.append("droite")
            positions.append(mouse.get_position())
            remove_duplicates_with_exceptions       #supprime les mêmes éléments de la liste
            print(positions)
        if v.get()=="gauche":
            positions.append("gauche")
            positions.append(mouse.get_position())
            remove_duplicates_with_exceptions       #supprime les mêmes éléments de la liste
            print(positions)
        if v.get()=="noMaj":
            positions.append("noMaj")
            positions.append(mouse.get_position())
            remove_duplicates_with_exceptions       #supprime les mêmes éléments de la liste
            print(positions)
        if v.get()=="temps":
            positions.append("temps")
            positions.append(mouse.get_position())
            remove_duplicates_with_exceptions       #supprime les mêmes éléments de la liste
            print(positions)
        if v.get()=="havresac":
            positions.append("havresac")
            remove_duplicates_with_exceptions       #supprime les mêmes éléments de la liste
            print(positions)

    file_name=Entry(window_creation_trajet, fg="#FFFFFF", bg="black")
    file_name.place(x=0, y=0, relwidth=width/7, height=30)  
  
    ressource = Radiobutton(window_creation_trajet, text="Ressource", variable=v, value="ressource", command=clic_transition)
    ressource.place(x=0, y=50, relwidth=width/7, height=30)
    
    haut = Radiobutton(window_creation_trajet, text="Haut", variable=v, value="haut", command=clic_transition)
    haut.place(relx=width/24.5, y=100, relwidth=width/14, height=30)
    
    droite = Radiobutton(window_creation_trajet, text="Droite", variable=v, value="droite", command=clic_transition)
    droite.place(relx=width/14, y=130, relwidth=width/14, height=30)
    gauche = Radiobutton(window_creation_trajet, text="Gauche", variable=v, value="gauche", command=clic_transition)
    gauche.place(x=0/14, y=130, relwidth=width/14, height=30)

    bas = Radiobutton(window_creation_trajet, text="Bas", variable=v, value="bas", command=clic_transition)
    bas.place(relx=width/24.5, y=160, relwidth=width/14, height=30)
    
    noMaj = Radiobutton(window_creation_trajet, text="noMaj", variable=v, value="noMaj", command=clic_transition)
    noMaj.place(relx=0, y=230, relwidth=width/7, height=30)

    havresac = Radiobutton(window_creation_trajet, text="havresac", variable=v, value="havresac", command=clic_transition)
    havresac.place(relx=0, y=270, relwidth=width/7, height=30)

    temps = Radiobutton(window_creation_trajet, text="temps", variable=v, value="temps", command=clic_transition)
    temps.place(relx=0, y=300, relwidth=width/7, height=30)

    delete_last = Button(window_creation_trajet, text="Supprimer le dernier", command=clic_delete_last)
    delete_last.place(x=0, y=330, relwidth=width/7, height=30)

    Button(window_creation_trajet, text="Enregistrer", font="Arial 8", command=enregistrer_trajet).place(x=0, y=360, relwidth=width/7, height=30)

    window_creation_trajet.bind("<Button-1>", clic)

    window_creation_trajet.update()
    window_creation_trajet.mainloop()


def faire_trajet():
    
    global positions, p, y, x, maj, t, boucle
    print ("début_trajet", p, nbCombat)
    i=0
    if boucle.get()==1:
        print("ok")

        while t<int(nbBoucles.get()):
            print(positions[p:len(positions)])
            t+=1
            for i in positions[p:len(positions)]:
                if pyautogui.locateOnScreen(r"C:\Users\tomde\Documents\Bot Dofus\levelup.png", confidence=0.9):
                    pyautogui.click(360 , 585)
                if pyautogui.locateOnScreen(r"C:\Users\tomde\Documents\Bot Dofus\pret.png", confidence=0.9):
                    p=positions.index(i)
                    combat()
                
                if maj.get()==1:
                    pyautogui.keyDown("shift")
                if i=="havresac":
                    pyautogui.keyUp("shift")
                    pyautogui.press("h")
                    time.sleep(random.uniform(float(temps_clics.get())-0.5, float(temps_clics.get())+0.5))
                    p+=1
                elif i=="noMaj":
                    x="noMaj"
                    p+=1
                elif i=="temps":
                    x="temps"
                    p+=1
                elif y==33:
                    positions_de_clicks=positions[p].split()
                    pyautogui.click(int(positions_de_clicks[0]), y)
                    pyautogui.keyUp("shift")
                    time.sleep(random.uniform(float(temps_maps.get())-0.5, float(temps_maps.get())+0.5))
                    y=0
                    p+=1
                elif y==900:
                    positions_de_clicks=positions[p].split()
                    pyautogui.click(int(positions_de_clicks[0]), y)
                    pyautogui.keyUp("shift")
                    time.sleep(random.uniform(float(temps_maps.get())-0.5, float(temps_maps.get())+0.5))
                    y=0
                    p+=1
                elif x==360:
                    positions_de_clicks=positions[p].split()
                    pyautogui.click(x, int(positions_de_clicks[1]))
                    pyautogui.keyUp("shift")
                    time.sleep(random.uniform(float(temps_maps.get())-0.5, float(temps_maps.get())+0.5))
                    x=0
                    p+=1
                elif x==1556:
                    positions_de_clicks=positions[p].split()
                    pyautogui.click(x, int(positions_de_clicks[1]))
                    pyautogui.keyUp("shift")
                    time.sleep(random.uniform(float(temps_maps.get())-0.5, float(temps_maps.get())+0.5))
                    x=0
                    p+=1
                elif x=="temps":
                    positions_de_clicks=positions[p].split()
                    pyautogui.click(int(positions_de_clicks[0]), int(positions_de_clicks[1]))
                    pyautogui.keyUp("shift")
                    time.sleep(random.uniform(float(temps_maps.get())-0.5, float(temps_maps.get())+0.5))
                    x=0
                    p+=1
                elif x=="noMaj":
                    if maj.get()==1:
                        pyautogui.keyUp("shift")
                    positions_de_clicks=positions[p].split()
                    pyautogui.click(int(positions_de_clicks[0]), int(positions_de_clicks[1]))
                    pyautogui.keyUp("shift")
                    time.sleep(random.uniform(float(temps_maps.get())-0.5, float(temps_maps.get())+0.5))
                    x=0
                    p+=1
                elif i == "haut":
                    y=33
                    p+=1
                elif i == "bas":
                    y=900
                    p+=1
                elif i == "gauche":
                    x=360
                    p+=1
                elif i == "droite":
                    x=1556
                    p+=1  
                else:
                    positions_de_clicks=positions[p].split()
                    pyautogui.click(int(positions_de_clicks[0]), int(positions_de_clicks[1]))
                    pyautogui.keyUp("shift")
                    time.sleep(random.uniform(float(temps_clics.get())-0.5, float(temps_clics.get())+0.5))
                    p+=1
            p=0     
        
    

    window.deiconify()
    positions.clear()

def combat():
    global nbCombat

    time.sleep(5) 

    pyautogui.click(1373 , 952)
           
    time.sleep(2)

    while pyautogui.locateOnScreen(r"C:\Users\tomde\Documents\Bot Dofus\victoire.png", confidence=0.9 )==None:
        for i in range (2):
            pyautogui.press("z")         
            time.sleep(1.4)
            pyautogui.click(1306 , 852)
            pyautogui.click(500, 500)
            time.sleep(1)
        pyautogui.press("space")
        time.sleep(3)
        if pyautogui.locateOnScreen(r"C:\Users\tomde\Documents\Bot Dofus\ok.png", confidence=0.8 )!=None:
            pyautogui.press("enter")
        
        time.sleep(2)
    
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(20)

    nbCombat+=1
    faire_trajet()
        

def executer_trajet():
    global positions
    for line in open(trajets.get(trajets.curselection())+".txt", 'r'):
        positions.append(line)
    positions = [x.replace('\n', '') for x in positions]; positions = [x.replace('(', '') for x in positions]; positions = [x.replace(')', '') for x in positions]; positions = [x.replace(',', '') for x in positions]
    
   
    window.iconify()
    faire_trajet()

    

Button(window, text="Exécuter le trajet sélectionné", font="Arial 8", command=executer_trajet).place(relx=0, rely=0, relwidth=width/2, relheight=0.1*height)
Button(window, text="Créer un trajet", font="Arial 8", command=creer_trajet).place(relx=0, rely=height*0.1, relwidth=width/2,relheight=0.1*height)

temps_clics=Entry(window, fg="#FFFFFF", bg="black")
temps_clics.place(relx=0, rely=height*0.2, relwidth=width/4, relheight=0.1*height)
temps_maps=Entry(window, fg="#FFFFFF", bg="black")
temps_maps.place(relx=0.25*width, rely=height*0.2, relwidth=width/4, relheight=0.1*height)

Checkbutton(window, text="Maj Activé", variable=maj).place(relx=0, rely=height*0.3, relwidth=width/4, relheight=0.1*height)
Checkbutton(window, text="Boucler  Nombre:", variable=boucle).place(relx=0.25*width, rely=height*0.3, relwidth=width*3/16, relheight=0.1*height)
nbBoucles=Entry(window, fg="#FFFFFF", bg="black")
nbBoucles.place(relx=7/16*width, rely=height*0.3, relwidth=width/16, relheight=0.1*height)

Button(window, text="Quitter", font="Arial 8", command=quitter).place(relx=0, rely=height*0.9, relwidth=width/2, relheight=0.1*height)

trajets = Listbox(window, font="Calibri 13", selectbackground='#121216', fg='#FFFFFF', bg="#121216", selectmode=SINGLE)
trajets.place(relx=width/2, y=0, relwidth=width/2, relheight=height)

refresh_trajets()

window.mainloop()