import mysql.connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "mysql1234",
    database ="eddb"
        )
mycursor =mydb.cursor()
# mycursor.execute("SHOW DATABASES")
# #mycursor.execute("CREATE DATABASE mydatabase")
# for x in mycursor:
#     print(x)
#mycursor.execute("CREATE DATABASE scholldb")
#mycursor=mydb.cursor()
mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)
