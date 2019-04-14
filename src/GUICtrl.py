# coding: UTF-8

import tkinter as tk
import os
import PIL.ImageTk as pilimgtk
import PIL.Image as pilimg
from pprint import pprint
import IconScraper


class GUIController :

#   Class value ------------------------------------
    MAXIMUM_COLUMN = 4
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
        # Window Width were fixed.
        # self.root.resizable(width=False, height=False)

        self.root.title(title)
        geometryText = str(GUIController.__windowWidth) + 'x' + str(GUIController.__windowHeight)
        self.root.geometry(geometryText)

        # Generate window move to front
        self.root.attributes("-topmost", True)

        # Set Focus on generated window
        os.system("open -a Python")

        return

    def IconLoader(self):
        # Panel size
        cv_width    = 200
        cv_height   = 200

        # Load all image files
        self.tkimgs = self.GetPhotoImages()

        bg_RGB = [0, 0, 0]

        gridRow = 0
        gridCol = 0
        for i, tkimg in enumerate(self.tkimgs) :

            bg_RGB[0] = (i * 20)
            bg_RGB[1] = (i * 20)
            bg_RGB[2] = (i * 20)
            rgbText = '#' + ''.join(map(str, bg_RGB))

            # No canvas padding
            self.cv = tk.Canvas(self.root, width=cv_width, height=cv_height, bg=rgbText, highlightthickness=0)
            # self.cv = tk.Canvas(self.root, width=cv_width, height=cv_height, bg=rgbText, highlightthickness=0, relief='ridge')

            # Put canvas from top-left -> left -> next-line-left
            # Put as table, Use grid func
            self.cv.grid(row=gridRow, column=gridCol)
            # self.cv.pack(anchor=tk.NW, side=tk.LEFT)

            self.cv.create_image((cv_width / 2), (cv_height / 2), image=tkimg)

            gridCol += 1

            if (gridCol == GUIController.MAXIMUM_COLUMN) :
                gridRow += 1
                gridCol  = 0

            # 1 2 3 4
            # 5 6 □ □
            # □ □ □ □
            # □ □ □ □

# for i in range(4) :
        #     bg_RGB[0] = (i * 20)
        #     bg_RGB[1] = (i * 20)
        #     bg_RGB[2] = (i * 20)
        #     rgbText = '#' + ''.join(map(str, bg_RGB))
        #
        #     # No canvas padding
        #     self.cv = tk.Canvas(self.root, width=cv_width, height=cv_height, bg=rgbText, highlightthickness=0, relief='ridge')
        #     self.cv.place(x=0, y=0)
        #     # self.cv.create_rectangle(5, 5, 20, 20, fill = 'green', outline = 'red')
        #
        #     # CanvasはWindowの左上から敷き詰める
        #     self.cv.pack(anchor=tk.N, side=tk.LEFT)
        #     # 画像はCanvasの真ん中に配置
        #     self.cv.create_image((cv_width / 2), (cv_height / 2), image=self.tkimgs[i])

    def GetPhotoImages(self) :
        imgs = []
        photoImgs = []
        imgs.append(r'/Users/yuji/Documents/python/L_SL/img/icons/pte1.png')
        imgs.append(r'/Users/yuji/Documents/python/L_SL/img/icons/pte2.png')
        imgs.append(r'/Users/yuji/Documents/python/L_SL/img/icons/pte3.png')
        imgs.append(r'/Users/yuji/Documents/python/L_SL/img/icons/pte4.png')
        imgs.append(r'/Users/yuji/Documents/python/L_SL/img/icons/pte5.png')

        iconScraper = IconScraper.IconScraper()
        iconScraper.GetAllIconURL()

        for img in imgs :
            openImg = pilimg.open(img).convert('RGB')
            photoImgs.append(pilimgtk.PhotoImage(openImg))

        return photoImgs

    def ShowWindow(self):
        self.root.mainloop()
