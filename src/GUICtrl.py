# coding: UTF-8
# View
import tkinter as tk
import os
import PIL.ImageTk as pilimgtk
import PIL.Image as pilimg
from pprint import pprint
import IconScraper
import FileController
import DBController

class GUIController :

#   Class value ------------------------------------
    TARGET_URL = 'https://store.line.me/stickershop/product/4333/'

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

    # IconsFrame target Url
    @property
    def iconsFrame(self):
        return self.__iconsFrame
    @iconsFrame.setter
    def iconsFrame(self, value):
        self.__iconsFrame = value

    # DBController instance
    @property
    def dbctrl(self):
        return self.__dbctrl
    @dbctrl.setter
    def dbctrl(self, value):
        self.__dbctrl = value
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

        # Gadgets placing
        self.GadgetPlacing()

        # Temp --------------------
        self.SetTargetStickerUrl(GUIController.TARGET_URL)
        # Temp --------------------

        self.cv = tk.Canvas(self.root)

        # DB Controller object
        self.dbCtrl = DBController.DBCtrl()

        return

    def DummyFunc(self, urlbox):
        # print('Dummy Func', msg)
        tgtUrl = urlbox.get()
        print(tgtUrl)

        self.SetTargetStickerUrl(tgtUrl)
        self.cv.delete('all')
        self.IconLoader()
        return

    def GadgetPlacing(self) :
        inputFrame = tk.Frame(self.root, bd=0, relief='ridge')
        inputFrame.pack(fill=tk.X)
        # inputFrame.grid(fill='x', row=0, column=0)
        # button1 = tk.Button(inputFrame, text="入力")
        # button1.pack(side="left")

        urlLbl = tk.Label(inputFrame, text='URL')
        urlBox = tk.Entry(inputFrame, width=75)
        urlBtn = tk.Button(inputFrame, text='Get')

        # placeholder setting
        # urlBox.insert(0, 'https://store.line.me/stickershop/product/446/')
        # Button Event : <ButtonRelease-1> = Release light button.
        urlBtn.bind("<ButtonRelease-1>", lambda event, a=urlBox:self.DummyFunc(a))
        # urlBtn.bind("<ButtonRelease-1>", self.DummyFunc)

        urlLbl.pack(side=tk.LEFT)
        urlBox.pack(side=tk.LEFT, expand=1)
        urlBtn.pack(side=tk.LEFT)

        # Tmp
        urlBox.insert(tk.END, 'https://store.line.me/stickershop/product/4333/')

        self.iconsFrame = tk.Frame(self.root, bd=0, relief='ridge')
        self.iconsFrame.pack()
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

        # return

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
            self.cv = tk.Canvas(self.iconsFrame, width=cv_width, height=cv_height, bg=rgbText, highlightthickness=0)
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
        urlId, dirName = self.GetDirName(title, self.tgtStiUrl)

        fCtrl = FileController.FileCtrl()
        relativePath = fCtrl.CheckCreateDirectory(dirName)

        photoImgs = []

        for icon in iconInfos :
            fullpath = relativePath + '/' + icon['id'] + '.png'
            # print(icon['id'], icon['url'], fullpath)
            gotFile = fCtrl.SaveFile(icon['url'], fullpath)

            # PNG convert to jpeg [Warning]
            openImg = pilimg.open(gotFile).convert('RGB')
            photoImgs.append(pilimgtk.PhotoImage(openImg))

        query = 'INSERT INTO sticker_list VALUES(%s, %s, %s, %s)' % (urlId, scraper.tgtUrl, dirName, '-')
        print('query = ', query)

        return photoImgs

    def GetDirName(self, title, url):

        urlId = url.split('/')[5]
        dirName = title.replace(' ', '_')
        dirName = dirName.replace('/', '／')
        dirName = urlId + '_' + dirName

        return urlId, dirName

    def ShowWindow(self):
        self.root.mainloop()
