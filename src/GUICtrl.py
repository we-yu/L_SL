# coding: UTF-8
# View
import tkinter as tk
import os
import PIL.ImageTk as pilimgtk
import PIL.Image as pilimg
from pprint import pprint
import ControlManager

import IconScraper
import FileController
import DBController
import ClipboardController

class GUIController:

#   Class value ------------------------------------
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

    # Currently target sticker's URL ID
    @property
    def parentId(self):
        return self.__parentId
    @parentId.setter
    def parentId(self, value):
        self.__parentId = value

    # Size radios group variable
    @property
    def groupVar(self):
        return self.__groupVar
    @groupVar.setter
    def groupVar(self, value):
        self.__groupVar = value

    # IconsFrame target Url
    @property
    def iconsFrame(self):
        return self.__iconsFrame
    @iconsFrame.setter
    def iconsFrame(self, value):
        self.__iconsFrame = value

    # galleryFrame
    @property
    def galleryFrame(self):
        return self.__galleryFrame
    @galleryFrame.setter
    def galleryFrame(self, value):
        self.__galleryFrame = value

    # galleryTag
    @property
    def galleryTag(self):
        return self.__galleryTag
    @galleryTag.setter
    def galleryTag(self, value):
        self.__galleryTag = value

    # outerCV
    @property
    def outerCV(self):
        return self.__outerCV
    @outerCV.setter
    def outerCV(self, value):
        self.__outerCV = value

    # DBController instance
    @property
    def dbCtrl(self):
        return self.__dbCtrl
    @dbCtrl.setter
    def dbCtrl(self, value):
        self.__dbCtrl = value

    # DBController instance
    @property
    def clpBrdCtrl(self):
        return self.__clpBrdCtrl
    @clpBrdCtrl.setter
    def clpBrdCtrl(self, value):
        self.__clpBrdCtrl = value

    # ControlManager instance
    @property
    def ctrlMng(self):
        return self.__ctrlMng
    @ctrlMng.setter
    def ctrlMng(self, value):
        self.__ctrlMng = value
    #   ------------------------------------------------

    def __init__(self, title, width, height, managerInstance) :

        # ControlManagerインスタンスへのリンクをセット
        self.ctrlMng = managerInstance

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
        # self.SetTargetStickerUrl(GUIController.TARGET_URL)
        # Temp --------------------

        # Initialize (If not have this, First time .delete('all') going to be error)
        # self.cv = tk.Canvas(self.root)
        # self.outerCV = tk.Canvas(self.root)
        # gf = self.SetGallaryFrame()

        # DB Controller instanceをマネージャから取得
        self.dbCtrl = self.ctrlMng.objects['dbCtrl']

        # Clipboard controller instanceをマネージャから取得
        self.clpBrdCtrl = self.ctrlMng.objects['cpBrdCtrl']

        return


    def GadgetPlacing(self) :
        inputFrame = tk.Frame(self.root, bd=0, relief='ridge')
        inputFrame.pack(fill=tk.X)
        # inputFrame.grid(fill='x', row=0, column=0)
        # button1 = tk.Button(inputFrame, text="入力")
        # button1.pack(side="left")

        urlLbl = tk.Label(inputFrame, text='URL')
        urlBox = tk.Entry(inputFrame, width=60)
        urlBtn = tk.Button(inputFrame, text='Get')

        # placeholder setting
        # urlBox.insert(0, 'https://store.line.me/stickershop/product/446/')
        # Button Event : <ButtonRelease-1> = Release light button.
        urlBtn.bind("<Button-1>", lambda event, a=urlBox:self.ScrapingStickerPage(a))
        # urlBtn.bind("<ButtonRelease-1>", self.DummyFunc)

        # Radio button group control
        # Radio group value should be class value.
        # self.groupVar = tk.IntVar()
        # self.groupVar.set(2)
        self.groupVar = tk.StringVar()
        self.groupVar.set('S')
        # groupVar = tk.StringVar(value='sizeL')

        radioTexts = ['L', 'M', 'S']
        radioButtons = []

        # self.groupVarを軸としてL/M/Sのラジオボタンを設定。初期値はSを指定。
        for i ,rText in enumerate(radioTexts) :
            radioButtons.append(tk.Radiobutton(inputFrame, text=rText, value=rText, variable=self.groupVar))

        # Label, URL-box, Get Buttonを配置。
        urlLbl.pack(side=tk.LEFT)
        # urlBox.pack(side=tk.LEFT, expand=1)
        urlBox.pack(side=tk.LEFT)

        urlBtn.pack(side=tk.LEFT)

        # RadioButtonはForで設置
        for rBtn in radioButtons :
            rBtn.pack(side=tk.LEFT)

        # Tmp URLの初期値を設定
        urlBox.insert(tk.END, 'https://store.line.me/stickershop/product/1252985/')

        self.SetIconsFrame()

        return

    # Getボタンを押した時に起動。対象のページからアイコンをロードし、既存のフレームを削除し、新たに敷き直す。
    def ScrapingStickerPage(self, urlbox):
        tgtUrl = urlbox.get()
        print(tgtUrl)

        self.SetTargetStickerUrl(tgtUrl)
        # if GUIController.BUTTON_COUNER > 0 :
        #     # self.cv.delete('all')
        #     self.outerCV.delete(self.galleryTag)
        #     print('DEL1', self.outerCV)
        #     self.outerCV.delete('all')
        #     self.outerCV = None
        #     print('DEL2', self.outerCV)
        #     self.DelIconsFrame()
        #     self.SetIconsFrame()
        self.DelIconsFrame()
        self.SetIconsFrame()
        self.IconLoader()
        return

    def CopyURLtoClipboard(self, parent_id, local_id):
        print('Kicked icon id =', parent_id, local_id)
        print(self.groupVar.get().lower())

        sticker_size = self.groupVar.get().lower()
        selectTarget = 'url_sticker_%s' % (sticker_size)
        query = 'SELECT %s FROM sticker_detail WHERE (parent_id=%s) AND (local_id=%s)' % (selectTarget, parent_id, local_id)
        result = self.dbCtrl.Read(query, 'detail')
        # result -> [('https://stickershop.line-scdn.net/...png',)]
        self.clpBrdCtrl.CopyToClipboard(result[0][0])

    # アイコン敷き詰め用フレームをセット
    def SetIconsFrame(self):
        self.iconsFrame = tk.Frame(self.root, bd=0, relief='ridge')
        self.iconsFrame.pack()

    # アイコン敷き詰め用フレームを削除
    def DelIconsFrame(self):
        self.iconsFrame.pack_forget()

    def SetGallaryFrame(self):
        # Make vertical scrollbar to see all stickers -----------------------
        self.outerCV = tk.Canvas(self.iconsFrame, width=GUIController.__windowWidth, height=GUIController.__windowHeight)

        scrollbar = tk.Scrollbar(self.iconsFrame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.outerCV.yview)

        self.outerCV.config(scrollregion=(0, 0, 2000, 2000), yscrollcommand=scrollbar.set)
        self.outerCV.pack(fill=tk.BOTH)

        galleryFrame = tk.Frame(self.outerCV)
        self.galleryTag = self.outerCV.create_window((0, 0), window=galleryFrame, anchor=tk.NW, width=self.outerCV.cget('width'))
        return galleryFrame
        # --------------------------------------------------------------------

    def IconLoader(self):
        # Panel size
        cv_width    = 200
        cv_height   = 200

        # Scaper instantiate
        iconScraper = IconScraper.IconScraper(self.tgtStiUrl)

        # Load all image files
        # self.tkimgs, ids = self.GetPhotoImages(iconScraper)
        self.tkimgs, self.parentId, ids = self.ctrlMng.GetPhotoImages(self.tgtStiUrl)

        # print(self.tkimgs, self.parentId, ids)

        gFrame = self.SetGallaryFrame()

        bg_RGB = [0, 0, 0]

        gridRow = 0
        gridCol = 0

        for i, tkimg in enumerate(self.tkimgs) :

            # 1 2 3 4
            # 5 6 □ □
            # □ □ □ □
            # □ □ □ □

            bg_RGB[0] = '00'
            bg_RGB[1] = '88'
            bg_RGB[2] = '00'
            rgbText = '#' + ''.join(map(str, bg_RGB))

            # No canvas padding
            self.cv = tk.Canvas(gFrame, width=cv_width, height=cv_height, bg=rgbText, highlightthickness=0)
            # self.cv = tk.Canvas(self.root, width=cv_width, height=cv_height, bg=rgbText, highlightthickness=0, relief='ridge')

            # Put canvas from top-left -> left -> next-line-left
            # Put as table, Use grid func
            self.cv.grid(row=gridRow, column=gridCol)
            # self.cv.pack(anchor=tk.NW, side=tk.LEFT)

            # 画像はCanvasの真ん中に配置
            self.cv.create_image((cv_width / 2), (cv_height / 2), image=tkimg)

            # gridTxt = 'Grid = [%s, %s]' % (gridRow, gridCol)
            iconId = str(ids[i])

            # http://memopy.hatenadiary.jp/entry/2017/06/13/214928
            # Define event, When clicked Canvas.
            self.cv.bind("<Button-1>", lambda event, a=self.parentId, b=iconId:self.CopyURLtoClipboard(a, b))

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
        self.parentId, dirName = self.GetDirName(title, self.tgtStiUrl)
        urlId = self.parentId

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
