# def greeting(name):
#     print('hello',name)

# print(greeting('Erdal'))

# sayhello = greeting
# print(greeting('erdal'))
# print(sayhello('ali'))

# def outher(num1):
#     print('outher')
#     def inner_increment(num1):
#         print('inner')
#         return num1+1
#     num2 = inner_increment(num1)
#     print(num1,num2)
# outher(20)


# def fa(num):
#     if not isinstance(num, int):
#         raise TypeError("number değer yazın")
#     elif  num <= 0:
#         raise TypeError("sıfırdan büyük rakam girin")
#     else:
#         def fax(num):
#             if num <= 1:
#                 return 1
#             return num*fax(num-1)
#         return fax(num)
# print(fa(11))
# while True:
#     def usalma(number):
#         def inner(power):
#             return number ** power
#         return inner
#     x = int(input('x üzeri y için, X : '))
#     y = int(input('x üzeri y için, y : '))
#     two=usalma(x)
#     print(f'{x} üzeri {y} işlem sonucu : '+str(two(y)))

# def yetki_sorgula(page):
#     def inner(rol):
#         if rol =='admin':
#             return "{0} rolü {1} sayfasına ulaşabilir.".format (rol, page)
#         else:
#             return "{0} rolü {1} sayfasına ulaşamaz.".format(rol,page)
#     return inner    
# user1 = yetki_sorgula('Product Edit Page')
# # print(user1(input('kullanıcı adı : ')))
# def islem(islem_adi):
#     def toplam(*args):
#         toplam =0
#         for i in args:
#             toplam += i
#         return toplam
#     def carpma(*args):
#         carpim = 1
#         for i in args:
#             carpim *=i
#         return carpim
        
#     if islem_adi == "toplama":
#         return toplam
#     else:
#         return carpma
    
# toplama = islem("toplama")
# print(toplama(1,3,5,6,7))

# carpma = islem("carpma")
# print(carpma(1,2,3,6,4))
# def toplama(a,b):
#     return a+b
# def cikarma(a,b):
#     return a-b
# def carpma(a,b):
#     return a*b
# def bolme(a,b):
#     return a/b

# def islem(f1,f2,f3,f4,islem_adi):
#     if islem_adi == "toplama":
#         print(f1(2,3))
#     elif islem_adi == "cikarma":
#         print(f2(5,3))
#     elif islem_adi =="carpma":
#         print(f3(3,4))
#     elif islem_adi =="bolme":
#         print(f4(10,2))
#     else:
#         print("geçersiz işlem")
# islem(toplama, cikarma, carpma, bolme,"toplama")
# islem(toplama, cikarma, carpma, bolme,"toplama")
# islem(toplama, cikarma, carpma, bolme,"carpma")
# islem(toplama, cikarma, carpma, bolme,"bolme")
# islem(toplama, cikarma, carpma, bolme,"karısik")
# def my_decorator(func):
#     def wrapper():
#         print("fonksiyondan önceki işlemler")
#         func()
#         print("fonksiyondan sonraki işlemler")
#     return wrapper


# @my_decorator   
# def saygreeting():
#     print("greeting")
# @my_decorator  
# def sayhello():
#     print('Hello')
# sayhello()
# saygreeting()

# import math
# import time
# def caculate_time(func):
#     def inner(*args,**kwargs):
#         start = time.time()
#         time.sleep(1)
#         func(*args,**kwargs)
#         finish = time.time()
#         print("fonksiyon "+ func.__name__+' '+ str(finish-start)+ " saniye sürdü.")
#     return inner
# @caculate_time
# def usalma(a,b):    
#     math.pow(a,b)     
# @caculate_time
# def faktoriyel(num):
#     math.factorial(num)   

# usalma(114,118)
# faktoriyel(36)
def cube(x):
    print(x**3)
cube(int(input('küpü alıcak sayı girin : ')))