import mysql.connector
from datetime import datetime

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "mysql1234",
    database = "schooldb"
)

mycursor = connection.cursor()
# # while True:
# #     idgir=int(input("id girin (1-12) : "))
# #     mycursor.execute(f'Select * From Student Where id={idgir}')
# #     studen = mycursor.fetchone()
# #     print(f'{studen[0]}. kişinin adı : {studen[2]} {studen[3]}')
# mycursor.execute('Select * From Student Order By name, surname, id')
# result = mycursor.fetchall()
# for studen in result:
#     print(f'{studen[0]}. kişinin adı : {studen[2]} {studen[3]}')
# sql = "Select COUNT(*) from Student where name='Ali'"
# mycursor.execute(sql)
# result = mycursor.fetchone()
# print(f"result:{result[0]}")
# sql = "Select * From student"
# mycursor.execute(sql)
# result = mycursor.fetchall()
# for res in result:
#     print(res[1],res[2],res[3]) 
# sql = "Select * From student where Birthdate LIKE '2003%'"
sql = "Select COUNT(id) from student where gender='E'"
mycursor.execute(sql)
result = mycursor.fetchall()
for res in result:
    print(res[0 ])