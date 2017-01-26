##import MySQLdb
##
##db = MySQLdb.connect(host="52.24.233.106",    # your host, usually localhost
##                     user="user1",         # your username
##                     passwd="zxcv1234",  # your password
##                     db="autolog")        # name of the data base
##
### you must create a Cursor object. It will let
###  you execute all the queries you need
##cur = db.cursor()
##
### Use all the SQL you like
##cur.execute("SELECT * FROM sf_grids")
##
### print all the first cell of all the rows
##for row in cur.fetchall():
##    print row
##
##db.close()


import pymysql

db = pymysql.connect(host='52.24.233.106',
                     port=3306,
                     user='user1',
                     passwd='zxcv1234',
                     db='autolog',
                     autocommit=True)

cur = conn.cursor()

cur.execute("SELECT * FROM sf_grids")

for row in cur:
    print(row)

cur.close()

cur.execute("""INSERT INTO sf_grids
               (average_speed, unique_cars)
               VALUES (123, 456)""")
conn.commit()

conn.close()
