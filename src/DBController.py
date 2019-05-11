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
        self.con = self.CheckCreateDB()

        # self.cursor = connector.cursor()
        # self.cursor.execute(query)
        # res = self.cursor.fetchall()
        # print('res = ', res)

        self.cursor = self.con.cursor()

        # -----------------------------------------------------
        # query = 'SELECT * FROM sticker_list ORDER BY id'
        # self.cursor.execute(query)
        # fAll = self.cursor.fetchall()
        # pprint(fAll)
        # print('---')
        # query = 'SELECT * FROM sticker_detail ORDER BY local_id'
        # self.cursor.execute(query)
        # fAll = self.cursor.fetchall()
        # pprint(fAll)
        # print('---')
        # -----------------------------------------------------

    def CheckCreateDB(self) :
        relativePath = DBCtrl.DB_LOCATION
        con = sqlite3.connect(relativePath, isolation_level=None)
        return con

    def Create(self, query, data=None, type=None) :

        if type == 'many' :
            dbResult = self.cursor.executemany(query, data)
        else :
            dbResult = self.cursor.execute(query)
        self.con.commit()
        return dbResult

    def Read(self, query, type=None) :
        self.cursor.execute(query)

        if type == 'count' :
            dbResult = self.cursor.fetchone()
            dbResult = int(dbResult[0])
        else :
            dbResult = self.cursor.fetchall()

        return dbResult

    def Update(self) :
        return

    def Delete(self) :
        return

    def ExecuteQuery(self, con, q) :
        try:
            print('Query is [', q, ']')
        except sqlite3.Error as e:
            print('sqlite3.Error occurred : ', e.args[0])

        
        

