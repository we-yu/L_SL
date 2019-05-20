# coding: UTF-8
# View

import os.path # ファイル操作
import urllib.request as urlreq # ファイルダウンロード＆保存

class FileCtrl :

    ICONS_DIRECTORY = '../img/icons/'

    instCheck = ''
    def __init__(self, msg=None) :
        print('Call ' + self.__class__.__name__ + ' Constructor')
        FileCtrl.instCheck = msg

    def CheckCreateDirectory(self, dirName):
        relativePath = FileCtrl.ICONS_DIRECTORY + dirName

        if not os.path.exists(relativePath):
            # ディレクトリが存在しない場合は作成
            os.mkdir(relativePath)
            # print('Create',relativePath)

        return relativePath

    def SaveFile(self, targetUrl, fileName) :

        if not os.path.exists(fileName):
            stat = urlreq.urlretrieve(targetUrl, fileName)
            print(stat[0])

        return fileName

    def TestFunction(self):
        print('TestFunc F-ctrl', FileCtrl.instCheck)


