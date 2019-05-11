# coding: UTF-8

import pyperclip as pyclip

class ClipBoardCtrl :

    def __init__(self) :
        print('Call ' + self.__class__.__name__ + ' Constructor')

    def CopyToClipboard(self, txt) :
        print(txt, ': Copy to your clipboard')
        pyclip.copy(txt)
