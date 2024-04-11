import mysql.connector

#connection object
conn_obj = mysql.connector.connect(
    host="sql6.freesqldatabase.com",
    user="sql6696949",
    passwd="a3sVJfE6jS",
)

# print(conn_obj)

cur_obj = conn_obj.cursor()

try:
    cur_obj.execute("SHOW DATABASES")
except:
    conn_obj.rollback()

for db in cur_obj:
    print(db)

try:
    cur_obj.execute("USE sql6696949")
    cur_obj.execute("SELECT * FROM Employee")
except:
    conn_obj.rollback()

for row in cur_obj:
    print(row)

conn_obj.close()