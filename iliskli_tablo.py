import mysql.connector
<<<<<<< HEAD

#hatalı yeni kayıt
=======
#tetst v2

>>>>>>> c95bac10d2963790b9914a7470c324fb84dd2f1f
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
