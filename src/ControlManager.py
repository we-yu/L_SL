# coding: UTF-8
import PIL.ImageTk as pilimgtk
import PIL.Image as pilimg
import GUICtrl
import IconScraper
import FileController
import DBController
import ClipboardController

from pprint import pprint

class ControlManager:
    title = 'LineStickerLider'
    width = '800'
    height = '700'

    @property
    def windowTitle(self):
        return self.__windowTitle
    @windowTitle.setter
    def windowTitle(self, value):
        self.__windowTitle = value

    @property
    def windowWidth(self):
        return self.__windowWidth
    @windowWidth.setter
    def windowWidth(self, value):
        self.__windowWidth = value

    @property
    def windowHeight(self):
        return self.__windowHeight
    @windowHeight.setter
    def windowHeight(self, value):
        self.__windowHeight = value

    @property
    def instances(self):
        return self.__instances
    @instances.setter
    def instances(self, value):
        key = value[0]
        val = value[1]
        self.__instances[key] = val

    @property
    def objects(self):
        return self.__objects
    @objects.setter
    def objects(self, value):
        key = value[0]
        val = value[1]
        self.__objects[key] = val

    def __init__(self):
        print('Call ' + self.__class__.__name__ + ' Constructor')
        self.windowTitle  = ControlManager.title
        self.windowWidth  = ControlManager.width
        self.windowHeight = ControlManager.height

        # Define instances. (Instantiate not yet)
        # self.instances['fileCtrl']('AABBCC') // This is instantiate.
        self.__instances = {}
        self.__objects = {}

        self.instances = ('ctrlMng',    self)
        self.instances = ('guiCtrl',    GUICtrl.GUIController)
        self.instances = ('dbCtrl',     DBController.DBCtrl)
        self.instances = ('cpBrdCtrl',  ClipboardController.ClipBoardCtrl)
        self.instances = ('scrp',       IconScraper.IconScraper)
        self.instances = ('fileCtrl',   FileController.FileCtrl)

        self.objects = ('ctrlMng',   self.instances['ctrlMng'])
        self.objects = ('dbCtrl',    self.instances['dbCtrl']())
        self.objects = ('cpBrdCtrl', self.instances['cpBrdCtrl']())
        self.objects = ('guiCtrl',   self.instances['guiCtrl'](self.windowTitle, self.windowWidth, self.windowHeight, self.objects['ctrlMng']))

        # inst = self.instances['fileCtrl']('AABBCC')
        # print(self.instances['fileCtrl'])
        # inst.TestFunction()
        # print(self.instances['fileCtrl'])

        # self.instances['fileCtrl']('AABBCC')
        # print(hex(id(self.instances['fileCtrl'])))
        # self.instances['fileCtrl'].TestFunction(self)
        # print(hex(id(self.instances['fileCtrl'])))
        # print(self.instances.items())

    def ApplicationStart(self):
        self.objects['guiCtrl'].ShowWindow()
        return

    def CopyURLtoClipboard(self, parent_id, local_id, grp):
        print('on Manager', parent_id, local_id, grp.get().lower())
        sticker_size = grp.get().lower()
        selectTarget = 'url_sticker_%s' % (sticker_size)
        query = 'SELECT %s FROM sticker_detail WHERE (parent_id=%s) AND (local_id=%s)' % (selectTarget, parent_id, local_id)
        result = self.objects['dbCtrl'].Read(query, 'detail')
        # result -> [('https://stickershop.line-scdn.net/...png',)]
        self.objects['cpBrdCtrl'].CopyToClipboard(result[0][0])

    # Get photo images from target URL
    def GetPhotoImages(self, tgtStiUrl) :

        self.objects = ('scrp', self.instances['scrp'](tgtStiUrl))
        scraper = self.objects['scrp']

        # Get all targets of Download icons URL
        iconInfos = scraper.GetAllIconURL()
        # pprint(iconInfos)

        # Get Top title of Sticker.
        title = scraper.GetStickerTitle()
        # Convert some characters, And connect with ID. Same time, Get ID. (URL ID)
        urlId   = self.GetUrlID(tgtStiUrl)
        dirName = self.GetDirName(title, urlId)

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
        result = self.objects['dbCtrl'].Read(query, 'count')

        print('query, result = ', query, '¥n', result)

        # If not registered.
        if result <= 0 :
            # Insert 1 record to list table. URL-ID, URL, Directory name, Stored directory
            query = 'INSERT INTO sticker_list VALUES(%s, \'%s\', \'%s\', \'%s\')' % (urlId, scraper.tgtUrl, dirName, relativePath)
            self.objects['dbCtrl'].Create(query)

            # After registerd into list, Make data of detail.
            query = 'SELECT count(*) FROM sticker_detail WHERE parent_id=%s' % (urlId)
            result = self.objects['dbCtrl'].Read(query, 'count')

            if result <= 0:
                # Several records to register.
                query = 'INSERT INTO sticker_detail VALUES (?, ?, ?, ?, ?)'
                values = []
                for icon in iconInfos:
                    # Make data as tuple. (Executemany accepts only [(), (), ()] tuple in list.)
                    value = (urlId, icon['id'], icon['staticUrl'], icon['fbStaticUrl'], icon['backGroundUrl'])
                    values.append(value)

                result = self.objects['dbCtrl'].Create(query, values, 'many')
        else :
            print(dirName, 'is already downloaded.')

        return photoImgs, urlId, ids

    def GetUrlID(self, url):
        urlId = url.split('/')[5]
        return urlId

    def GetDirName(self, title, urlId):
        # urlId = url.split('/')[5]
        dirName = title.replace(' ', '_')
        dirName = dirName.replace('/', '／')
        dirName = urlId + '_' + dirName
        return dirName
