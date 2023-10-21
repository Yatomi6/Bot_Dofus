import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class Map:
  
    def __init__(self):
        pass
  
    def show_map(self, img_draw):
        img_draw = np.ascontiguousarray(img_draw, dtype=np.uint8)
        _, img_draw2 = cv2.threshold(img_draw, 0, 0, cv2.THRESH_BINARY)
        self.get_wallkable_cell((img_draw.copy()), [], img_draw2)
        self.get_break_cell((img_draw.copy()), [], img_draw2)
        self.show_monster((img_draw.copy()), [], img_draw2)
        cv2.imshow("Losanges", img_draw2)
        cv2.waitKey(10)
      
  
    def get_wallkable_cell(self, img, cases_coords, img_draw):
        lower = (120, 120, 120)
        upper = (255, 255, 255)
        mask = cv2.inRange(img, lower, upper)
        # Appliquer le masque pour remplacer les pixels blancs par du noir
        img[mask > 0] = (0, 0, 0)
        # Convertir l'image en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Appliquer un seuillage pour mettre en évidence les contours
        _, threshold = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(threshold, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        width_sum = 0
        height_sum = 0
        count = 0
        list_invalid = []
        cases_coords = {}
        list_x_pair = []
        list_y_inpair = []
        index = 0
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.09 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                #list_invalid.append(approx)
                if w > 55 and h > 27:
                    width_sum += w
                    height_sum += h
                    count += 1
                    y = self.get_closer_y_or_create(cases_coords, y)
                    if(cases_coords[y] == []):
                        index += 1
                    if index % 2 == 0:
                        list_x = list_x_pair
                    else:
                        list_x = list_y_inpair
                    for try_x in list_x:
                        if x > try_x - 15 and x < try_x + 15:
                            x = try_x
                    if x not in list_x:
                        list_x.append(x)
                    if x not in cases_coords[y]:
                        cases_coords[y].append(x)             
                    points = np.array([[x, y + int(h/2)], [x + int(w/2), y], [x + w, y + int(h/2)], [x + int(w/2), y + h]], np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.polylines(img_draw, [points], True, (0, 0, 255), 2)
            else:
                list_invalid.append(approx)
        for approx in list_invalid:
            x, y, w, h = cv2.boundingRect(approx)
            if w > 55/3 and h > 27/4:
                y = self.get_closer_y_or_create(cases_coords, y, True)
                index = list(cases_coords.keys()).index(y)
                if index % 2 != 0:
                    list_x = list_x_pair
                else:
                    list_x = list_y_inpair
                if(len(list_x) == 0):
                    return 
                x = self.closest_value(list_x, x)
                if x in cases_coords[y]:
                    continue
                w = int(width_sum/count)
                h = int(height_sum/count)
                points = np.array([[x, y + int(h/2)], [x + int(w/2), y], [x + w, y + int(h/2)], [x + int(w/2), y + h]], np.int32)
                points = points.reshape((-1, 1, 2))
                cv2.polylines(img_draw, [points], True, (255, 0, 0), 2)
                cases_coords[y].append(x)

    def closest_value(self, input_list, input_value):
        arr = np.asarray(input_list)
        i = (np.abs(arr - input_value)).argmin()
        return arr[i]
      
    def get_closer_y_or_create(self, cases_coords, y, force = False):
        if list(cases_coords.keys()) == []:
            cases_coords[y] = []
        closer = self.closest_value(list(cases_coords.keys()), y)
        if(not force and not (y >= closer - 10 and y <= closer + 10)):
            cases_coords[y] = []
            closer = y
        return closer

    def get_break_cell(self, img, cases_coords, img_draw):
        lower = (80, 80, 80)
        upper = (255, 255, 255)
        mask = cv2.inRange(img, lower, upper)
        # Appliquer le masque pour remplacer les pixels blancs par du noir
        img[mask > 0] = (0, 0, 0)
        # Convertir l'image en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Appliquer un seuillage pour mettre en évidence les contours
        _, threshold = cv2.threshold(gray, 80, 100, cv2.THRESH_BINARY)
        # Trouver les contours
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Boucle sur les contours
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                if w > 55 and h > 27:
                    y += 20
                    points = np.array([[x, y + int(h/2)], [x + int(w/2), y], [x + w, y + int(h/2)], [x + int(w/2), y + h]], np.int32)
                    points = points.reshape((-1, 1, 2))
                    cv2.polylines(img_draw, [points], True, (150, 150, 150), 2)
                    cases_coords.append((x,y))
                  

    cases_coords_walkable = []
    cases_coords_line_break = []


    def show_monster(self, img, monster_coords, img_draw):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        monster_folder = r"C:\Users\tomde\Documents\python\Dofus\images_mobs_perso\mobs"
        monster_images = os.listdir(monster_folder)
        threshold = 0.8
        for image_name in monster_images:
            fg_img = cv2.imread(os.path.join(monster_folder, image_name), cv2.IMREAD_UNCHANGED)
            fg_img = cv2.cvtColor(fg_img, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(img, fg_img, cv2.TM_CCOEFF_NORMED)
            w, h = fg_img.shape[::-1]
            loc = np.where(result >= threshold)
            for pt in zip(*loc[::-1]):
                center = (int(pt[0] + w/2), int(pt[1] + h/2))
                cv2.circle(img_draw, center, int(max(w,h)/2), (255,0,0), 3)


if __name__ == "__main__":
    test = Map()
    test.show_map(cv2.imread(r"C:\Users\tomde\Pictures\2023_04_21-13;47;43.png"))
    cv2.waitKey(0)