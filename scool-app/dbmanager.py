import mysql.connector
import datetime
from Connection import connection
from Student import Student
from Classes import Classes
# from Teacher import Teacher
# From Classone import Classone


class DbManager:
    def __init__(self):
        self.connection = connection
        self.cursor = self.connection.cursor()
    
    def getStudentById(self,id):
        sql = "select * from student where id = %s "
        value = (id,)
        self.cursor.execute(sql, value)
        try:
            obj = self.cursor.fetchall()
            return Student.CreateStudent(obj)
        except mysql.connector.Error as err:
            print("Hata..:",err)
    def getStudentByClassId(self,classid):
        sql = "select * from student where classid = %s "
        value = (classid,)
        self.cursor.execute(sql, value)
        try:
            obj = self.cursor.fetchall()
            return Student.CreateStudent(obj)
        except mysql.connector.Error as err:
            print("Hata..:",err)
        
    def addStudent(self,student: Student):
        sql = "INSERT INTO student(studentNumber,name,surname,birthdate,gender,classid) VALUES (%s,%s,%s,%s,%s,%s)"
        value =(student.studentNumber,student.name,student.surname,student.birthdate,student.gender,student.classid)
        self.cursor.execute(sql,value)
        try:
            self.connection.commit()
            print(f'{self.cursor.rowcount} tane kayıt eklendi.')
            print(f'son eklenen kaydın id si :{self.cursor.lastrowid}')
        except mysql.connector.Error as err:
            print("Hata:",err)

    def deleteStudent(self,studentid):
        sql = "delete from student where id=%s"
        value = (studentid,)
        self.cursor.execute(sql,value)
        try:
            self.connection.commit()
            print(f'{studentid} id nolu, {self.cursor.rowcount} tane kayıt sisildi.')
            
        except mysql.connector.Error as err:
            print("Hata:",err)

    def updateStudent(self,student: Student):
        sql = "update student set studentNumber=%s,name=%s,surname=%s,birthdate=%s,gender=%s,classid=%s where id=%s"
        value =(student.studentNumber,student.name,student.surname,student.birthdate,student.gender,student.classid,student.id)
        self.cursor.execute(sql,value)
        try:
            self.connection.commit()
            print(f'{self.cursor.rowcount} tane kayıt güncellendi.')
          
        except mysql.connector.Error as err:
            print("Hata:",err)
        #****************************************
    def getClasses(self):
        sql = "select * from class "
        self.cursor.execute(sql)
        try:
            obj = self.cursor.fetchall()
            return Classes.CreateClasses(obj)
        except mysql.connector.Error as err:
            print("Hata..:",err)

    def getStudentTum(self):
        sql = "select * from student order by name"#order by name ASC ekledim a-z sıraladı,DESC olsaydı z-a sıralardı
        self.cursor.execute(sql)
        try:
            obj = self.cursor.fetchall()
            return Student.CreateStudent(obj)
        except mysql.connector.Error as err:
            print("Hata..:",err)

    def __del__(self):
        self.connection.close()
        print('db. kapatıldı.')
# db = DbManager()           

# #self.displayClasses()
# classid = int(input('yukardaki Hangi id li sınıfa ekleyeceksin :'))
# number= int(input('okul numarası :'))
# name = input('adı :')
# surname=input('soyadı :')
# # year=int(input('doğum yılı :'))
# # month=int(input('doğum ay :'))
# # day=int(input('doğum gün :'))
# # birthdate = datetime.date(year,month,day)
# birthdate = datetime.date(2000, 2, 2)

# gender=input('cinsiyet (E/K :')

# students = Student(None,number,name,surname,birthdate,gender,classid)
# db.addStudent(students)   
    
#     #     self.connection.close()
#     #     print('db kayıt silindi.')


#     #     pass
#     # def editStudent(self,student: Student):
#     #     pass
#     # def addTeacher(self,teacher: Teacher):
#     #     pass
#     # def editTeacher(self,teacher: Teacher):
#     #     pass

# # db = DbManager()
# # # student= db.getStudentById(4)
# # # print(student[0].name)
  
# # # print(yedi.surname)
# # # print("********************************")
# # # yed= db.getStudentById(3)

# # # print(yed.name)
# # # print(yed.surname)
# # # student=db.getStudentByClassId(1)

# # # print(student[1].name)
# # # student=db.getStudentByClassId(1)

# # # print(student[1].name)

# # den=db.getStudentById(6)
# # # den[0].name='Çınar'
# # # den[0].surname='Turan'
# # # den[0].studentNumber='421'
# # # #self,id,studentNumber,name,surname,birthdate,gender,classid0
# # # #= [None,151,"Fatma","güntek",1999-4-19,"Kadın",1]
# # # db.addStudent(den[0])
# # #print(den[0].name)

# # den[0].name='Çın+a'
# # den[0].surname='Tur+n'
# # den[0].studentNumber='538'

# # db.updateStudent(den[0])
