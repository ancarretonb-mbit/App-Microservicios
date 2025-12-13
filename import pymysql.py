import pymysql

conn = pymysql.connect(
    host="mysql_pictures",
    user="mbit",
    password="mbit",
    database="Pictures",
    port=3306
)
print("Conectado correctamente")
conn.close()
