import sqlite3
import os
class DataBaseSqlite:
    DataBaseFileName="Student_Information.db"
    Connect=None
    Cursor=None
    def DataBaseIsExist(self):
        return os.path.exists("Student_Information.db") 
    def Connect_DataBase(self):
        if self.DataBaseIsExist==False:
            return False
        self.Connect = sqlite3.connect(self.DataBaseFileName)
        self.Cursor = self.Connect.cursor() 
    def Excute(self,SQL):
        self.Cursor.execute(SQL)
        return self.Cursor.fetchall()
    def Submit_For_Execution(self,SQL):
        self.Cursor.execute(SQL)
        self.Connect.commit()
    def Close(self):
        self.Connect.close()
        