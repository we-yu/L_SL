# coding: UTF-8

from pprint import pprint
import sqlite3
import os.path # ファイル操作

class DBCtrl :

    DB_LOCATION = '../db/sqlite/lsl.db'

    # DB File
    @property
    def con(self) :
        return self.__con
    @con.setter
    def con(self, value) :
        self.__con = value
        
    # Cursor object
    @property
    def cursor(self) :
        return self.__cursor
    @cursor.setter
    def cursor(self, value) :
        self.__cursor = value

    def __init__(self) :
        print('Call ' + self.__class__.__name__ + ' Constructor')
        connector = self.CheckCreateDB()

        print(connector)

        # self.cursor = connector.cursor()
        # self.cursor.execute(query)
        # res = self.cursor.fetchall()
        # print('res = ', res)

        cursor = connector.cursor()

        # -----------------------------------------------------
        query = 'SELECT * FROM sticker_list ORDER BY id'
        cursor.execute(query)
        fAll = cursor.fetchall()
        pprint(fAll)
        print('---')
        query = 'SELECT * FROM sticker_detail ORDER BY local_id'
        cursor.execute(query)
        fAll = cursor.fetchall()
        pprint(fAll)
        print('---')
        # -----------------------------------------------------

    def CheckCreateDB(self) :
        relativePath = DBCtrl.DB_LOCATION

        con = sqlite3.connect(relativePath, isolation_level=None)

        return con

    def Create(self) :
        return

    def Read(self) :
        return

    def Update(self) :
        return

    def Delete(self) :
        return

    def ExecuteQuery(self, con, q) :
        try:
            print('Query is [', q, ']')

        except sqlite3.Error as e:
            print('sqlite3.Error occurred : ', e.args[0])

        
        

