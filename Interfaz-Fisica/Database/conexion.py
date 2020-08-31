
import pymysql

class DataBase:
    def __init__ (self):
        self.connection = pymysql.connect(
            host='localhost', #ip
            user='root',
            password='12345',
            db='cupratos'
        )
        self.cursor = self.connection.cursor()
        print("Conexion establecida exitosa")

    def select_user(self,id):
        pass  
dataBase = DataBase()    
