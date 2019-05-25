# coding: UTF-8
# View
import tkinter as tk
import os

from pprint import pprint

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
        self.root.resizable(width=False, height=False)

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

        return

    def GadgetPlacing(self) :
        inputFrame = tk.Frame(self.root, bd=0, relief='ridge')
        inputFrame.pack(fill=tk.X)

        urlLbl = tk.Label(inputFrame, text='URL')
        urlBox = tk.Entry(inputFrame, width=60)
        urlBtn = tk.Button(inputFrame, text='Get')

        # Event binding for button
        urlBtn.bind("<ButtonRelease-1>", lambda event, a=urlBox:self.ReloadIconsFrame(a))

        self.groupVar = tk.StringVar()
        self.groupVar.set('S')

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
    def ReloadIconsFrame(self, urlbox):
        tgtUrl = urlbox.get()
        # print(tgtUrl)

        self.SetTargetStickerUrl(tgtUrl)
        self.DelIconsFrame()
        self.SetIconsFrame()
        self.IconLoader()
        return

    # アイコン敷き詰め用フレームをセット
    def SetIconsFrame(self):
        self.iconsFrame = tk.Frame(self.root, bd=0, relief='ridge')
        self.iconsFrame.pack()

    # アイコン敷き詰め用フレームを削除
    def DelIconsFrame(self):
        self.iconsFrame.pack_forget()

    # IconsFrameの上にOuterCVキャンバスセット。スクロールバーはこれにアタッチ。さらにその上にGalleryFrameを生成。
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
        # --------------------------------------------------------------------
        return galleryFrame

    def IconLoader(self):
        # Panel size
        cv_width    = 200
        cv_height   = 200

        # Load all image files
        self.tkimgs, self.parentId, ids = self.ctrlMng.GetPhotoImages(self.tgtStiUrl)

        gFrame = self.SetGallaryFrame()

        bg_RGB = ['00', '80', '00']
        rgbText = '#' + ''.join(map(str, bg_RGB))

        gridRow = 0
        gridCol = 0

        for i, tkimg in enumerate(self.tkimgs) :

            # 1 2 3 4
            # 5 6 □ □
            # □ □ □ □
            # □ □ □ □

            # No canvas padding
            self.cv = tk.Canvas(gFrame, width=cv_width, height=cv_height, bg=rgbText, highlightthickness=0)

            # Put canvas from top-left -> left -> next-line-left
            # Put as table, Use grid func
            self.cv.grid(row=gridRow, column=gridCol)

            # 画像はCanvasの真ん中に配置
            self.cv.create_image((cv_width / 2), (cv_height / 2), image=tkimg)

            # Get icon's unique ID, Target icon is on this time.
            iconId = str(ids[i])

            # http://memopy.hatenadiary.jp/entry/2017/06/13/214928
            # Define event, When clicked Canvas.
            self.cv.bind("<Button-1>", lambda event, a=self.parentId, b=iconId, c=self.groupVar:self.ctrlMng.CopyURLtoClipboard(a, b, c))

            gridCol += 1

            if (gridCol == GUIController.MAXIMUM_COLUMN) :
                gridRow += 1
                gridCol  = 0

    def SetTargetStickerUrl(self, url) :
            self.tgtStiUrl = url

    def ShowWindow(self):
        self.root.mainloop()
