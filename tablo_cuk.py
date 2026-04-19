import mysql.connector


connection = mysql.connector.connect(
    host="localhost",
    user = "root",
    password="mysql1234",
    database="kutuphane"
    )
# alter table products
# Add CONSTRAINT fk_catagories_pruducts
# FOREIGN KEY (categories_id) REFERENCE catagories(id)
# mycursor = connection.cursor()
mycursor = connection.cursor()
mycursor.execute("SHOW TABLES")
for x in mycursor:
    
    print(x)




