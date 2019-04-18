import pymysql

db = pymysql.connect("localhost","root","609586869","test" )

cursor = db.cursor()

cursor.execute("")

data = cursor.fetchone()

print ("Database version : %s " % data)

db.close()

