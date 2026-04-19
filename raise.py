
'''
def check_passwod(psw):
    import re
    if len(psw) < 7:
        raise Exception("parola en az 7 karakter olmalıdır.")
    elif not re.search("[a-z]", psw):
        raise Exception("parola küçük harf içermelidir.")
    elif not re.search("[A-Z]",psw):
        raise Exception("parola büyük harf içermelidir.")
    elif not re.search("[0-9]",psw):
        raise Exception("parola rakam içermelidir.")
    elif re.search("\s",psw):
        raise Exception("parolanız boşluk içermemelidir.")
    elif not re.search("[_@$]",psw):
        raise Exception("parolanız alfa numetrik harf içermelidir.")
    else:
        print("giriş başarılı.")

password = 'AAAAAAa8@'

try:
    check_passwod(password)
except Exception as ex:
    print(ex)
else:
    print("giriş tamamlandı: else.")
finally:
    print("validation tamamlandı.")
'''
class Person:
    def __init__(self, name, year):
        if len(name) > 10:
            raise Exception("name alanı fazla karakter içeriyor.")
        else:
            self.name = name
p = Person('Allllllliiiiiiiiii',1989)
