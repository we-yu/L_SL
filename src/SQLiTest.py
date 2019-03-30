# coding: UTF-8
import sqlite3
from pprint import pprint

# https://www.htmllifehack.xyz/entry/2018/08/03/231351

# Use SQLite by Python3

# Create DB file.
con = sqlite3.connect('sample.db')

# Create cursor-object
cursor = con.cursor()

# Create new table, name is "data_set" -> field is id, name, date
# query = 'CREATE TABLE data_set(id, name, date)'
# Create Table
# execute = kick single query
# cursor.execute(query)

### Create DATA --------------------------------------------------------------------------------------

# Execute multiple queries in 1 time. On this case, use triple ['] for command sentence.
queries =\
    '''
    DROP TABLE IF EXISTS data_set;
    CREATE TABLE data_set(id, name, date);
    '''

cursor.executescript(queries)

# Insert record for Table with placeholder
# query = 'INSERT INTO data_set(id, name, date) VALUES(?, ?, ?)'
# values = (1, 'saito', 19900810)
# cursor.execute(query, values)

# Insert multiple data
data = [
    (1, 'Saito', 19980810),
    (2, 'Hori', 19961025),
    (3, 'Yoda', 19880103),
    (4, 'Nishino', 20000530)
]
query = 'INSERT INTO data_set VALUES(?, ?, ?)'
cursor.executemany(query, data)

# Only insert, Data is not updated. To updated, Need commit.
# con.commit()
# This is auto Commit
con = sqlite3.connect('sample.db', isolation_level=None)

### Read DATA --------------------------------------------------------------------------------------

query = 'SELECT * FROM data_set'
# Get all data from executed query (Type = List)
cursor.execute(query)
fAll = cursor.fetchall()
pprint(fAll)

print('---')

# Get data 1 by 1
cursor.execute(query)
fOne = cursor.fetchone()
pprint(fOne)
fOne = cursor.fetchone()
pprint(fOne)
fOne = cursor.fetchone()
pprint(fOne)

print('---')

# Get data as non-list (with loop)
cursor.execute(query)
for row in cursor :
    print(row[0], row[1], row[2])

print('---')

### Delete DATA --------------------------------------------------------------------------------------

# Delete target record
query = 'DELETE FROM data_set WHERE id=?'
values = (2 ,)
cursor.execute(query, values)
query = 'SELECT * FROM data_set'
cursor.execute(query)
pprint( cursor.fetchall() )

print('---')

# Delete all values from Table
query = 'DELETE FROM data_set'
cursor.execute(query)
query = 'SELECT * FROM data_set'
cursor.execute(query)
pprint( cursor.fetchall() )

print('---')

# Delete Table
query = 'DROP TABLE data_set'
cursor.execute(query)
# query = 'SELECT * FROM data_set'
# cursor.execute(query)
# pprint( cursor.fetchall() )
