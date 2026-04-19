
from dbmanager import DbManager
import datetime
from Student import Student



class App:
    def __init__(self):
        self.db = DbManager()
     
    def initApp(self):
        msg = "***************\n0-Tüm öğrecler Listesi\n1-Öğrenci Listesi\n2-Öğrenci ekle\n3-Öğrenci güncelle\n4-Öğrenci sil\n5-Öğretmen ekle\n6-Sınıflara göre desler\n7-Çıkış (E/Ç)"
        
        while True:
            print(msg)
            islem = input('Seçim : ')
            if islem == '0':
                self.displayStudentsTum()
            elif islem == '1':
                self.displayStudents()
            elif islem == '2':
                self.addStudent()
            elif islem == '3':
                self.updateStudent()
            elif islem == '4':
                self.deleteStudent()
            elif islem == '5':
                print("5 e basıldı.")
            elif islem == '6':
                self.displayClasses()
            elif islem =='e'or islem =='ç':
                print('e veya ç basıldı. seçimden de Çıkış yapıldı.')
                break
            else:
                print('yanlış seçim yapıldı.')      
   #************************************ 
    def displayStudents(self):
        classes = self.db.getClasses()
        for c in classes:
            print(f'{c.id}:{c.name}')

        classid = int(input('hangi sınıf : '))
        students = self.db.getStudentByClassId(classid)
        print(f'{classid}. sınıftaki öğrencilerin Listesi :')
        for index, std in enumerate(students):
            print(f'{index+1}-{std.name} {std.surname}')

    def displayStudentsTum(self):
        studen = self.db.getStudentTum()
        print('sınıflardaki tüm öğrenciler :')
        for index, std in enumerate(studen):
            print(f'S/N : {index+1}, --id : {std.id}, {std.name} {std.surname}, sınıf id : {std.classid}')

    def displayClasses(self):
        classlar = self.db.getClasses()
        for cls in classlar:
            print(f'{cls.id} {cls.name}')
    
    def addStudent(self):
        self.displayClasses()
        classid = int(input('yukardaki Hangi id li sınıfa ekleyeceksin :'))
        number= int(input('okul numarası :'))
        name = input('adı :')
        surname=input('soyadı :')
        year=int(input('doğum yılı :'))
        month=int(input('doğum ay :'))
        day=int(input('doğum gün :'))
        birthdate = datetime.date(year, month, day)
        #birthdate = datetime.date(2000,2,2)

        gender=input('cinsiyet (E/K :')

        studu = Student(None,number,name,surname,birthdate,gender,classid)
        self.db.addStudent(studu)

    def updateStudent(self):
        
        #öğrencileri göster
        self.displayStudentsTum()
        #öğrenci al
        id = int(input('güncellenecek öğrenci seç -id- si: '))
        self.displayClasses()
        classid = int(input('yukardaki Hangi id li sınıfa ekleyeceksin :'))

        number= int(input('okul numarası :'))
        name = input('adı :')
        surname=input('soyadı :')
        year=int(input('doğum yılı :'))
        month=int(input('doğum ay :'))
        day=int(input('doğum gün :'))
        birthdate = datetime.date(year, month, day)
        #birthdate = datetime.date(2000,2,2)

        gender=input('cinsiyet (E/K :')

        studu = Student(id,number,name,surname,birthdate,gender,classid)
        self.db.updateStudent(studu)

    def deleteStudent(self):
        self.displayStudentsTum()
        #öğrenci al
        id = int(input('kaydı silinecek öğrenci seç -id- si: '))
        self.db.deleteStudent(id)
       

    def __del__(self):
        #self.connection.close()
        print('initApp kapatıldı.')
       
app=App()
app.initApp()