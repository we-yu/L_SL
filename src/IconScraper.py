# coding: UTF-8

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import sys
import re

TARGET_URL = 'https://store.line.me/stickershop/product/1206683/ja'

class IconScraper :

    def __init__(self):
        print('Call ' + self.__class__.__name__ + ' Constructor')

    def GetAllIconURL(self):
        print('Call ' + sys._getframe().f_code.co_name)

        # Request page and get parser
        sticker_req  = requests.get(TARGET_URL)
        sticker_soup = BeautifulSoup(sticker_req.content, 'html.parser')

        # Extract Sticker ID (Might be all stickers manages by this ID)

        # mdCMN38Item01

        # Make ID condition
        re_condition = r'Item01$'
        stickerTitle = sticker_soup.find('ul', class_=re.compile(re_condition))
        # stickerTitle = sticker_soup.select('ul.mdCMN38Item01')
        print(stickerTitle)
        print(stickerTitle.ul['class'])



        # Get Title-text



