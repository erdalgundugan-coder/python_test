import mysql.connector

#hatalı yeni kayıt
connection = mysql.connector.connect(
    host="localhost",
    user = "root",
    password="mysql1234",
    database="node-app"
    )
# alter table products
# Add CONSTRAINT fk_catagories_pruducts
# FOREIGN KEY (categories_id) REFERENCE catagories(id)
mycursor = connection.cursor()

# mycursor.execute("show ")
# for x in mycursor:
#     print(x[0])

sql="Select * From Products inner join Catagories on Catagories.id=Products.Catagoriesid where products.name LIKE '%samsung%'  "
mycursor.execute(sql)
result = mycursor.fetchall()
for result in result:
    print(result[0],result[1],result[2],result[-1])