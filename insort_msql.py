import mysql.connector



def insertProduct(list):
    
    connection = mysql.connector.connect(host="localhost", user ="root", password ="mysql1234", database = "node-app")
    cursor = connection.cursor()

    sql = "INSERT INTO Product(name,price,imageUrl,descprition) VALUES (%s,%s,%s,%s)"
    values = list

    cursor.executemany(sql,values)
    try:
        connection.commit()
    except mysql.connector.Error as err:
        print('hata', err)
    finally:
        connection.close()
        print("database bağlantısı kapandı.erdal.")
list=[]
while True:
    name = input("ürün adı:")
    price = input("ürün fiyatı:")
    imageUrl = input("ürün imaj adı:")
    descprition = input("ürün açıklaması:")
    list.append((name,price,imageUrl,descprition))
    result = input("devam etmek istiyormusunuz ( e/h ) :")
    if result=='h':
        print("Kayıtlarınız veri tabanına aktarılıyor...")
        print(list)
        insertProduct(list)
        break
    
    #insertProduct(name,price,imageUrl,descprition)