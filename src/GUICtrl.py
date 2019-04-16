# coding: UTF-8
# View
import tkinter as tk
import os
import PIL.ImageTk as pilimgtk
import PIL.Image as pilimg
from pprint import pprint
import IconScraper
import FileController

class GUIController :

#   Class value ------------------------------------
    TARGET_URL = 'https://store.line.me/stickershop/product/4333/ja'

    MAXIMUM_COLUMN = 4
    __windowWidth   = 0
    __windowHeight  = 0
#   Setting property -------------------------------
    # tkinter root
    @property
    def root(self) :
        return self.__root
    @root.setter
    def root(self, value) :
        self.__root = value

    # Load target Url
    @property
    def tgtStiUrl(self):
        return self.__tgtStiUrl
    @tgtStiUrl.setter
    def tgtStiUrl(self, value):
        self.__tgtStiUrl = value
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

        # Generate window move to front [Warning]
        self.root.attributes("-topmost", True)

        # Set Focus on generated window
        os.system("open -a Python")

        # Temp --------------------
        self.SetTargetStickerUrl(GUIController.TARGET_URL)
        # Temp --------------------

        return

    def IconLoader(self):
        # Panel size
        cv_width    = 200
        cv_height   = 200

        # Scaper instantiate
        iconScraper = IconScraper.IconScraper(self.tgtStiUrl)
        # Load all image files
        self.tkimgs = self.GetPhotoImages(iconScraper)

        bg_RGB = [0, 0, 0]

        gridRow = 0
        gridCol = 0
        for i, tkimg in enumerate(self.tkimgs) :

            # 1 2 3 4
            # 5 6 □ □
            # □ □ □ □
            # □ □ □ □

            bg_RGB[0] = (i * 5)
            bg_RGB[1] = (i * 5)
            bg_RGB[2] = (i * 5)
            rgbText = '#' + ''.join(map(str, bg_RGB))

            # No canvas padding
            self.cv = tk.Canvas(self.root, width=cv_width, height=cv_height, bg=rgbText, highlightthickness=0)
            # self.cv = tk.Canvas(self.root, width=cv_width, height=cv_height, bg=rgbText, highlightthickness=0, relief='ridge')

            # Put canvas from top-left -> left -> next-line-left
            # Put as table, Use grid func
            self.cv.grid(row=gridRow, column=gridCol)
            # self.cv.pack(anchor=tk.NW, side=tk.LEFT)

            # 画像はCanvasの真ん中に配置
            self.cv.create_image((cv_width / 2), (cv_height / 2), image=tkimg)

            gridCol += 1

            if (gridCol == GUIController.MAXIMUM_COLUMN) :
                gridRow += 1
                gridCol  = 0

    def SetTargetStickerUrl(self, url) :
        self.tgtStiUrl = url

    def GetPhotoImages(self, scraper) :
        iconInfos = scraper.GetAllIconURL()
        # pprint(iconInfos)

        title = scraper.GetStickerTitle()
        dirName = self.GetDirName(title, self.tgtStiUrl)

        fCtrl = FileController.FileCtrl()
        relativePath = fCtrl.CheckCreateDirectory(dirName)

        photoImgs = []

        for icon in iconInfos :
            fullpath = relativePath + '/' + icon['id'] + '.png'
            print(icon['id'], icon['url'], fullpath)
            gotFile = fCtrl.SaveFile(icon['url'], fullpath)

            # PNG convert to jpeg [Warning]
            openImg = pilimg.open(gotFile).convert('RGB')
            photoImgs.append(pilimgtk.PhotoImage(openImg))

        return photoImgs

    def GetDirName(self, title, url):

        urlId = url.split('/')[5]
        dirName = title.replace(' ', '_')
        dirName = dirName.replace('/', '／')
        dirName = urlId + '_' + dirName

        return dirName

    def ShowWindow(self):
        self.root.mainloop()
