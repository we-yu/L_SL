# coding: UTF-8

import tkinter as tk
import os
import PIL.ImageTk as pilimgtk
import PIL.Image as pilimg

class GUIController :

#   Class value ------------------------------------
    __windowWidth   = 0
    __windowHeight  = 0
#   Setting property -------------------------------
    @property
    def root(self) :
        return self.__root
    @root.setter
    def root(self, value) :
        self.__root = value
#   ------------------------------------------------

    def __init__(self, title, width, height) :
        GUIController.__windowWidth   = width
        GUIController.__windowHeight  = height

        print("Constructor Kicked")
        self.root = tk.Tk()

        self.root.title(title)
        geometryText = str(GUIController.__windowWidth) + 'x' + str(GUIController.__windowHeight)
        self.root.geometry(geometryText)

        # Generate window move to front
        self.root.attributes("-topmost", True)

        # Set Focus on generated window
        os.system("open -a Python")

        return

    def IconLoader(self):
        cv_width    = 200
        cv_height   = 200

        # ------------------------
        self.tkimg = []
        filepath = r'/Users/yuji/Documents/python/L_SL/img/icons/pte1.png'
        # There's warning now
        img = pilimg.open(filepath).convert('RGB')
        self.tkimg.append(pilimgtk.PhotoImage(img))
        filepath = r'/Users/yuji/Documents/python/L_SL/img/icons/pte2.png'
        # There's warning now
        img = pilimg.open(filepath).convert('RGB')
        self.tkimg.append(pilimgtk.PhotoImage(img))
        filepath = r'/Users/yuji/Documents/python/L_SL/img/icons/pte3.png'
        # There's warning now
        img = pilimg.open(filepath).convert('RGB')
        self.tkimg.append(pilimgtk.PhotoImage(img))
        filepath = r'/Users/yuji/Documents/python/L_SL/img/icons/pte4.png'
        # There's warning now
        img = pilimg.open(filepath).convert('RGB')
        self.tkimg.append(pilimgtk.PhotoImage(img))
        # ------------------------
        bg_RGB = [0, 0, 0]
        for i in range(4) :
            bg_RGB[0] = (i * 20)
            bg_RGB[1] = (i * 20)
            bg_RGB[2] = (i * 20)
            rgbText = '#' + ''.join(map(str, bg_RGB))

            self.cv = tk.Canvas(self.root, width=cv_width, height=cv_height, bg=rgbText, relief=tk.RAISED)
            self.cv.place(x=0, y=0)
            # self.cv.create_rectangle(5, 5, 20, 20, fill = 'green', outline = 'red')
            self.cv.pack(anchor=tk.N, side=tk.LEFT)

            self.cv.create_image(cv_width / 2, cv_height / 2, image=self.tkimg[i])

    def SetPhotoImages(self) :
        imgs = []
        return imgs

    def ShowWindow(self):
                    self.root.mainloop()
