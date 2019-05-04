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
import ClipboardController

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
    def dbCtrl(self):
        return self.__dbCtrl
    @dbCtrl.setter
    def dbCtrl(self, value):
        self.__dbCtrl = value

    # DBController instance
    @property
    def clpbrdCtrl(self):
        return self.__clpbrdCtrl
    @clpbrdCtrl.setter
    def clpbrdCtrl(self, value):
        self.__clpbrdCtrl = value
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

        # DB Controller instance
        self.dbCtrl = DBController.DBCtrl()

        # Clipboard controller instance
        self.clpbrdCtrl = ClipboardController.ClipBoardCtrl()

        return

    def ScrapingStickerPage(self, urlbox):
        tgtUrl = urlbox.get()
        print(tgtUrl)

        self.SetTargetStickerUrl(tgtUrl)
        self.cv.delete('all')
        self.IconLoader()
        return

    def CopyURLtoClipboard(self, parent_id, local_id):
        print('Kicked icon id =', parent_id, local_id)
        query = 'SELECT url_sticker_s FROM sticker_detail WHERE local_id=%s' % (local_id)
        result = self.dbCtrl.Read(query, 'detail')
        # result -> [('https://stickershop.line-scdn.net/...png',)]
        self.clpbrdCtrl.CopyToClipboard(result[0][0])

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
        urlBtn.bind("<Button-1>", lambda event, a=urlBox:self.ScrapingStickerPage(a))
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
        self.tkimgs, ids = self.GetPhotoImages(iconScraper)

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

            # gridTxt = 'Grid = [%s, %s]' % (gridRow, gridCol)
            iconId = str(ids[i])

            self.cv.bind("<Button-1>", lambda event, a=0, b=iconId:self.CopyURLtoClipboard(a, b))

            gridCol += 1

            if (gridCol == GUIController.MAXIMUM_COLUMN) :
                gridRow += 1
                gridCol  = 0

    def SetTargetStickerUrl(self, url) :
        self.tgtStiUrl = url

    def GetPhotoImages(self, scraper) :

        # Get all targets of Download icons URL
        iconInfos = scraper.GetAllIconURL()
        # pprint(iconInfos)

        # Get Top title of Sticker.
        title = scraper.GetStickerTitle()
        # Convert some characters, And connect with ID. Same time, Get ID. (URL ID)
        urlId, dirName = self.GetDirName(title, self.tgtStiUrl)

        fCtrl = FileController.FileCtrl()
        relativePath = fCtrl.CheckCreateDirectory(dirName) + '/'

        # python photo image list
        photoImgs = []
        # id numbers
        ids = []

        for icon in iconInfos :
            fullpath = relativePath + icon['id'] + '.png'
            # print(icon['id'], icon['url'], fullpath)
            gotFile = fCtrl.SaveFile(icon['backGroundUrl'], fullpath)

            # PNG convert to jpeg [Warning]
            openImg = pilimg.open(gotFile).convert('RGB')
            photoImgs.append(pilimgtk.PhotoImage(openImg))

            # Save id numbers by getting order
            ids.append(icon['id'])

        # DB process ------------------------------------------------

        # Check list table. Already registered this sticker data or not.
        query = 'SELECT count(*) FROM sticker_list WHERE id=%s' % (urlId)
        result = self.dbCtrl.Read(query, 'count')

        # If not registered.
        if result <= 0 :
            # Insert 1 record to list table. URL-ID, URL, Directory name, Stored directory
            query = 'INSERT INTO sticker_list VALUES(%s, \'%s\', \'%s\', \'%s\')' % (urlId, scraper.tgtUrl, dirName, relativePath)
            self.dbCtrl.Create(query)

            # After registerd into list, Make data of detail.
            query = 'SELECT count(*) FROM sticker_detail WHERE parent_id=%s' % (urlId)
            result = self.dbCtrl.Read(query, 'count')

            if result <= 0:
                # Several records to register.
                query = 'INSERT INTO sticker_detail VALUES (?, ?, ?, ?, ?)'
                values = []
                for icon in iconInfos:
                    # Make data as tuple. (Executemany accepts only [(), (), ()] tuple in list.)
                    value = (urlId, icon['id'], icon['staticUrl'], icon['fbStaticUrl'], icon['backGroundUrl'])
                    values.append(value)

                result = self.dbCtrl.Create(query, values, 'many')

        else :
            print(dirName, 'is already downloaded.')




        return photoImgs, ids

    def GetDirName(self, title, url):

        urlId = url.split('/')[5]
        dirName = title.replace(' ', '_')
        dirName = dirName.replace('/', '／')
        dirName = urlId + '_' + dirName

        return urlId, dirName

    def ShowWindow(self):
        self.root.mainloop()
