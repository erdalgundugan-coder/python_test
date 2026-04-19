#  error handling => hata yönetimi
# error => hata
# print(a) => NameError
# int('1a2') => ValueError
# print(10/0) => ZeroDivisionError
# print('denem'e) => SyntaxError
while True:
    try:
        x = int(input('x: '))
        y = int (input('y: '))
        print(x/y)
    except Exception as ex:
        print('hatalı giriş yapıldı',ex)
    else:
       break
    finally:
        print('try except sonlandı.')