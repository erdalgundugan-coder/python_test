import json
import os

class User:
    def __init__(self, username, password, email):
        self.usarname = username
        self.password = password
        self.email = email


class UserRepository:
    def __init__(self):
        self.users = []
        self.isloggedin = False
        self.currentUser = {}

        #load users from .json file
        # self.loadUsers()

    def loadUsers(self):
        if os.path.exists('users.json'):
            with open('users.json','r',encoding='utf-5') as file:
                users = json.load(file)
                for user in users:
                    newuser =User(username = user['username'],pasword = user['password'], email = user['email'])
                    self.users.append(newuser)
                print(self.users)
    def register(self,user : User):
        self.users.append(user)
        self.savetofile()
        self.loadUsers()

        print('Kullanıcı oluşturuldu.')
        #17
        # print(self.users)

        #pass
    def login(self):
        pass
    def savetofile(self):
        list = []
        for user in self.users:
            list.append(json.dumps(user.__dict__))
        with open('users.json','w') as file:
            json.dump(list, file)
        print(list)
        # pass
    def izle(self):
        self =input('gir:')
        print(self)
    def loggout(self):
        print('çıkış yaptınız.')

repository = UserRepository()


while True:
    print('Menü'.center(50,'*'))
    print()
    secim = input("1- Register\n2- Login\n3- Logout\n4- identitiy\n5- Exit\nSeciminiz : ")
   
    if secim == '5':
        repository.izle()
        break
    else:
        if secim == '1':
            username = input('username :')
            password = input('password : ')
            email = input('email : ')
            user = User(username=username, password=password,email=email)
            #pass #register
            repository.register(user)
            
            #print(repository.users)

        elif secim == '2':
            pass #login
        elif secim == '3':
            repository.loggout()
        elif secim == '4':
            pass #display username
        else:
            print("yanlış seçim.")