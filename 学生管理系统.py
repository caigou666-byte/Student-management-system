from contextlib import nullcontext
import datetime
import random
import shutil
import time
import uuid
from PySide2.QtUiTools import QUiLoader
from time import time
from PySide2.QtUiTools import loadUiType
from PySide2.QtGui import QStandardItemModel,QStandardItem
import sqlite3
import os
from PySide2.QtWidgets import (QApplication, QHBoxLayout, QItemDelegate, QPushButton, QTableView, QWidget)
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import DataBase
def verify_date_str_lawyer(datetime_str):
    return QDateTime.fromString(datetime_str,"yyyy-MM-dd H:mm:ss").isValid()
    # datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')        
def ShowGaoyi():
    Data.Student_Data=Data.DataBase.Excute("SELECT * FROM student WHERE Class LIKE '%高一%';")
    a=Data.DataBase.Excute("SELECT COUNT(*) FROM student WHERE Class LIKE '%高一%';")[0][0]
    b=Data.DataBase.Excute("SELECT COUNT(*) FROM student where Whether_Or_Not_In_School='0'AND Class LIKE '%高一%' OR Whether_Or_Not_In_School='否' AND Class LIKE '%高一%';")[0][0]
    Control.read_data_to_tableview("高一",int(a)-int(b),b)
def ShowGaoer():
    Data.Student_Data=Data.DataBase.Excute("SELECT * FROM student WHERE Class LIKE '%高二%';")
    a=Data.DataBase.Excute("SELECT COUNT(*) FROM student WHERE Class LIKE '%高二%';")[0][0]
    b=Data.DataBase.Excute("SELECT COUNT(*) FROM student where Whether_Or_Not_In_School='0'AND Class LIKE '%高二%' OR Whether_Or_Not_In_School='否' AND Class LIKE '%高二%';")[0][0]
    Control.read_data_to_tableview("高二",int(a)-int(b),b)
def ShowGaosan():
    Data.Student_Data=Data.DataBase.Excute("SELECT * FROM student WHERE Class LIKE '%高三%';")
    a=Data.DataBase.Excute("SELECT COUNT(*) FROM student WHERE Class LIKE '%高三%';")[0][0]
    b=Data.DataBase.Excute("SELECT COUNT(*) FROM student where Whether_Or_Not_In_School='0'AND Class LIKE '%高三%' OR Whether_Or_Not_In_School='否' AND Class LIKE '%高三%';")[0][0]
    Control.read_data_to_tableview("高三",int(a)-int(b),b)  
def ShowQuanbu():
    Data.Student_Data=Data.DataBase.Excute("SELECT * FROM student ;")
    a=Data.DataBase.Excute("SELECT COUNT(*) FROM student ;")[0][0]
    b=Data.DataBase.Excute("SELECT COUNT(*) FROM student where Whether_Or_Not_In_School='0' OR Whether_Or_Not_In_School='否';")[0][0]
    Control.read_data_to_tableview("全部",int(a)-int(b),b)
def showJianSuo(SQL1,SQL2,SQL3,d):
    Data.Student_Data=Data.DataBase.Excute(SQL1)
    a=Data.DataBase.Excute(SQL2)[0][0]
    b=Data.DataBase.Excute(SQL3)[0][0]
    Control.read_data_to_tableview1("检索数据的",int(a)-int(b),b,d)    
class Form:
    Main_Form=None
    Insert_Form=None
    Change_Form=None
    Leave_Application_Form=None
    Vacation_Form=None
    Search_Form=None
class Main_Form(QWidget):#登录窗口
    def __init__(self):
        self.ui=QUiLoader().load('main.ui')#加载布局文件.ui
        #连接信号     
        self.ui.a1.clicked.connect(self.Show_Senior_One_Students)
        self.ui.a2.clicked.connect(self.Show_Senior_Two_Students)
        self.ui.a3.clicked.connect(self.Show_Senior_Three_Students)
        self.ui.pushButton_6.clicked.connect(self.Insert_Form)
        self.ui.a4.clicked.connect(self.Show_All_Students)
        self.ui.a5.clicked.connect(self.Search)
        self.ui.a6.clicked.connect(self.History)
    def History(self):
        os.startfile(os.getcwd()+"\\history.exe")      
    def Search(self):
        Form.Search_Form=Search_Form()
        Form.Search_Form.ui.show()

    def Show_All_Students(self):
        ShowQuanbu()
    def Show_Senior_One_Students(self):
        ShowGaoyi()
    def Show_Senior_Two_Students(self):
        ShowGaoer()
    def Show_Senior_Three_Students(self):
        ShowGaosan()
    def Insert_Form(self):
        Form.Insert_Form=Insert_Form() 
        Form.Insert_Form.ui.dateTimeEdit.setCalendarPopup(True)
        Form.Insert_Form.ui.dateTimeEdit_2.setCalendarPopup(True) 
        Form.Insert_Form.ui.radioButton_8.setChecked(True) 
        Form.Insert_Form.ui.dateTimeEdit_2.setDisabled(True)
        Form.Insert_Form.ui.radioButton_16.setDisabled(True)
        Form.Insert_Form.ui.radioButton_17.setDisabled(True)  
        Form.Insert_Form.ui.show()

class DropArea(QLabel):
    def __init__(self, *args, **kwargs):
        super(DropArea, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
 
    def dragEnterEvent(self, event):
        # print("drag event")
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
 
    def dropEvent(self, event):
        # print("drop event")
        files = list()
        urls = [u for u in event.mimeData().urls()]
        for url in urls:
            # print(url.path())
            files.append(url.toLocalFile())
        Data.Pic=files[0]
        if QPixmap().load(files[0])==True :
            self.setPixmap(QPixmap(files[0]))
        else:
            QMessageBox.about(Form.Vacation_Form.ui,"提示","请上传正确的图片材料！")
            return
class Search_Form(QWidget):
    def __init__(self):
        self.ui=QUiLoader().load('search.ui')
        self.ui.Button.clicked.connect(self.SaveData)
    def SaveData(self):
       
        if self.ui.b1.isChecked():
            Sex="男"
        elif self.ui.b2.isChecked(): 
            Sex="女"
        elif self.ui.b3.isChecked():
            Sex=""
        if self.ui.c1.isChecked():
            Class="高一"
        elif self.ui.c2.isChecked(): 
            Class="高二"
        elif self.ui.c3.isChecked():
            Class="高三"
        else:
            Class=""    
        Class=Class+"_"+self.ui.d1.text()

        if self.ui.e1.isChecked():
            a="是"
        elif self.ui.e2.isChecked(): 
            a="否"
        elif self.ui.e3.isChecked():
            a=""    

        if self.ui.f1.isChecked():
            b="是"
        elif self.ui.f2.isChecked(): 
            b="否"
        elif self.ui.f3.isChecked():
            b="" 

        if self.ui.h1.isChecked():
            c="是"
        elif self.ui.h2.isChecked(): 
            c="否"
        elif self.ui.h3.isChecked():
            c="" 
        if self.ui.i1.isChecked():
            d="是"
        elif self.ui.i2.isChecked(): 
            d="否"
        elif self.ui.i3.isChecked():
            d="" 
        SQL1="SELECT * FROM student WHERE Name LIKE '%%%s%%' AND Sex LIKE '%%%s%%' AND Class LIKE '%%%s%%' AND Whether_Or_Not_Accommodation LIKE '%%%s%%' AND Whether_Or_Not_In_School LIKE '%%%s%%' AND Headteacher LIKE '%%%s%%' AND Whether_To_Ask_For_Leave LIKE '%%%s%%' ;"%(self.ui.a1.text(),Sex,Class,a,b,self.ui.g1.text(),c)           
        SQL2="SELECT COUNT(*) FROM student WHERE Name LIKE '%%%s%%' AND Sex LIKE '%%%s%%' AND Class LIKE '%%%s%%' AND Whether_Or_Not_Accommodation LIKE '%%%s%%' AND Whether_Or_Not_In_School LIKE '%%%s%%' AND Headteacher LIKE '%%%s%%' AND Whether_To_Ask_For_Leave LIKE '%%%s%%';"%(self.ui.a1.text(),Sex,Class,a,b,self.ui.g1.text(),c)  
        SQL3="SELECT COUNT(*) FROM student WHERE Name LIKE '%%%s%%' AND Sex LIKE '%%%s%%' AND Class LIKE '%%%s%%' AND Whether_Or_Not_Accommodation LIKE '%%%s%%' AND Whether_Or_Not_In_School in('0','否') AND Headteacher LIKE '%%%s%%' AND Whether_To_Ask_For_Leave LIKE '%%%s%%';"%(self.ui.a1.text(),Sex,Class,a,self.ui.g1.text(),c)  
        showJianSuo(SQL1,SQL2,SQL3,d)
        QMessageBox.about(Form.Search_Form.ui,"提示","检索成功！\n留意主界面数据的变化！")    
class Vacation_Form(QWidget):
    data=None
    def __init__(self,data):
        self.data=data
        self.ui=QUiLoader().load('Vacation.ui')
        self.ui.labe1.setText("学号：%s\n姓名：%s\n班级：%s"%(data["Name"],data["Student_ID"],data["Class"]))
        self.ui.Button.clicked.connect(self.SaveData)
        self.ui.Button_2.clicked.connect(self.CleanPic)
        self.ui.dropArea = DropArea(self.ui.widget)
        self.ui.dropArea.setGeometry(QRect(10, 180, 581, 331))
        self.ui.dropArea.setStyleSheet(u"QLabel{border:5px dashed #242424;}")
        self.ui.dropArea.setScaledContents(True)
    def CleanPic(self):
        self.ui.dropArea.setPixmap("")
        Data.Pic=""
    def SaveData(self):
        # print(self)
        if  Data.Pic=='':
            QMessageBox.about(Form.Vacation_Form.ui,"提示","请上传图片材料！")
            return
        else:
            b = QMessageBox.question(Form.Vacation_Form.ui, '提示', '确定要销假?\n警告：该学生必须回到学校才能销假！\n同时会清除出校时间！\n(按回车确定)', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) 
            if b == QMessageBox.Yes:  
                print("删除")
                q=Data.Pic.split("/")
                q=q[len(q)-1]
                aa=Data.DataBase.Excute("SELECT * FROM student where Student_ID='%s';"%(self.data["Student_ID"]))[0]
                bb=Data.DataBase.Excute("SELECT * FROM StudentsGentOut where Student_ID='%s';"%(self.data["Student_ID"]))[0][1]
                # print(aa)
                cc='';
                dd=str(uuid.uuid4())+"."+q.split(".")[1]
                shutil.copy(Data.Pic,"./Data/") 
                os.rename("./Data/"+q,"./Data/"+dd)
                print("INSERT INTO History(Student_ID,Name,Sex,Class,Whether_Or_Not_Accommodation,Whether_Or_Not_In_School,Headteacher,Time_Of_Admission,School_Leaving_Time,Whether_To_Ask_For_Leave,Reasons,Pic_encryption,Pic_unencrypted,Operation_Time)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],bb,cc,dd,str(QDateTime.currentDateTime().toString("yyyy-MM-dd H:mm:ss"))))
                Data.DataBase.Submit_For_Execution("INSERT INTO History(Student_ID,Name,Sex,Class,Whether_Or_Not_Accommodation,Whether_Or_Not_In_School,Headteacher,Time_Of_Admission,School_Leaving_Time,Whether_To_Ask_For_Leave,Reasons,Pic_encryption,Pic_unencrypted,Operation_Time)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(aa[0],aa[1],aa[2],aa[3],aa[4],aa[5],aa[6],aa[7],aa[8],aa[9],bb,cc,dd,str(QDateTime.currentDateTime().toString("yyyy-MM-dd H:mm:ss"))))
                Data.DataBase.Submit_For_Execution("UPDATE student SET Whether_To_Ask_For_Leave='否',School_Leaving_Time='',Whether_Or_Not_In_School='是' WHERE Student_ID='%s';"%(self.data["Student_ID"]))
                Data.DataBase.Submit_For_Execution("DELETE FROM StudentsGentOut WHERE Student_ID='%s';"%(self.data["Student_ID"]))
                ShowQuanbu()
                self.ui.close()
            else:  
                print("取消")  
               
class Leave_Application_Form(QWidget):
    data=None
    def __init__(self,data):
        self.data=data
        self.ui=QUiLoader().load('LeaveApplication.ui')
        self.ui.labe1.setText("学号：%s\n姓名：%s\n班级：%s"%(data["Name"],data["Student_ID"],data["Class"]))
        self.ui.Button.clicked.connect(self.SaveData)
    def SaveData(self):
        if self.ui.lineEdit.text()=="":
            QMessageBox.about(Form.Leave_Application_Form.ui,"提示","请填写请假理由！")
            return
        Data.DataBase.Submit_For_Execution("UPDATE student SET Whether_To_Ask_For_Leave='是' WHERE Student_ID='%s';"%(self.data["Student_ID"]))
        Data.DataBase.Submit_For_Execution("INSERT INTO StudentsGentOut(Student_ID,Reasons)VALUES('%s','%s');"%(self.data["Student_ID"],self.ui.lineEdit.text()))
        QMessageBox.about(Form.Leave_Application_Form.ui,"提示","请假申请成功！")
        ShowQuanbu()
        self.ui.close() 
class Insert_Form(QWidget):
    def __init__(self):
        self.ui=QUiLoader().load('insert.ui')
        #连接信号     
        self.ui.Button.clicked.connect(self.SaveData)
        self.ui.radioButton_10.clicked.connect(self.Now_Time_clicked_1)
        self.ui.radioButton_11.clicked.connect(self.Choose_Other_Time_clicked_1)
        self.ui.radioButton_16.clicked.connect(self.Now_Time_clicked_2)
        self.ui.radioButton_17.clicked.connect(self.Choose_Other_Time_clicked_2)
        self.ui.radioButton_8.clicked.connect(self.At_School)
        self.ui.radioButton_9.clicked.connect(self.Leave_School)
    def At_School(self):
        self.ui.dateTimeEdit_2.setDisabled(True)
        self.ui.radioButton_16.setDisabled(True)
        self.ui.radioButton_17.setDisabled(True)
    def Leave_School(self):
        self.ui.radioButton_16.setDisabled(False)
        self.ui.radioButton_17.setDisabled(False) 
        self.ui.radioButton_16.setChecked(True)  
    def Now_Time_clicked_1(self):
        self.ui.dateTimeEdit.setDisabled(True)
    def Choose_Other_Time_clicked_1(self):
        self.ui.dateTimeEdit.setDisabled(False)
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())    
    def Now_Time_clicked_2(self):
        self.ui.dateTimeEdit_2.setDisabled(True)
    def Choose_Other_Time_clicked_2(self):
        self.ui.dateTimeEdit_2.setDisabled(False)
        self.ui.dateTimeEdit_2.setDateTime(QDateTime.currentDateTime()) 

    def SaveData(self):
        if Form.Insert_Form.ui.lineEdit.text()=="":
            QMessageBox.about(Form.Insert_Form.ui,'提示','请输入姓名！')
            return
        if Form.Insert_Form.ui.lineEdit_2.text()=="":
            QMessageBox.about(Form.Insert_Form.ui,'提示','请输入班级！')
            return  
        if Form.Insert_Form.ui.lineEdit_3.text()=="":
            QMessageBox.about(Form.Insert_Form.ui,'提示','请输入班主任姓名！')
            return  
        if Form.Insert_Form.ui.radioButton_4.isChecked()==True:
            Sex="男"
        else:
            Sex="女"
        if  Form.Insert_Form.ui.radioButton.isChecked()==True: 
            Class="高一"
        elif Form.Insert_Form.ui.radioButton_2.isChecked()==True:
            Class="高二"    
        else:
            Class="高三"
        if Form.Insert_Form.ui.radioButton_6.isChecked()==True:  
            Accommodation="是"
        else:
            Accommodation="否"
        if self.ui.radioButton_8.isChecked()==True:  
            InSchool="是"
            Leave_School_Time=""
        else:
            InSchool="否"
            if self.ui.radioButton_16.isChecked()==True:
                # strptime
                Leave_School_Time=str(QDateTime.currentDateTime().toString("yyyy-MM-dd H:mm:ss"))
            else:
                Leave_School_Time=str(self.ui.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd H:mm:ss"))
        if self.ui.radioButton_10.isChecked()==True:
            In_School_Time=str(QDateTime.currentDateTime().toString("yyyy-MM-dd H:mm:ss"))
        else:
            In_School_Time=str(self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd H:mm:ss"))
        ###编码###
        if Class=="高一":
            a="21"
        elif Class=="高二":
            a="22"  
        else:
            a="23"
        if Sex=="男":
            b="1"
        else:
            b="0"
        Student_ID=a+b+str(self.ui.lineEdit_2.text()).zfill(2)+str(random.randint(1,50)).zfill(2)  
        SQL="INSERT INTO student(Student_ID,Name,Sex,Class,Whether_Or_Not_Accommodation,Whether_Or_Not_In_School,Headteacher,Time_Of_Admission,School_Leaving_Time,Whether_To_Ask_For_Leave)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(Student_ID,self.ui.lineEdit.text(),Sex,Class+"_"+self.ui.lineEdit_2.text(),Accommodation,InSchool,self.ui.lineEdit_3.text(),In_School_Time,Leave_School_Time,"否")    
        Data.DataBase.Submit_For_Execution(SQL)
        ShowQuanbu()
        QMessageBox.about(Form.Insert_Form.ui,'提示','数据插入成功！')
        self.ui.close()       
class Change_Form():
    student_id=""
    def __init__(self):
        self.ui=QUiLoader().load('change.ui')#加载布局文件.ui    
        self.ui.Button.clicked.connect(self.Save_Data)
        self.ui.radioButton_10.clicked.connect(self.Now_Time_clicked_1)
        self.ui.radioButton_11.clicked.connect(self.Choose_Other_Time_clicked_1)
        self.ui.radioButton_16.clicked.connect(self.Now_Time_clicked_2)
        self.ui.radioButton_17.clicked.connect(self.Choose_Other_Time_clicked_2)
        self.ui.radioButton_8.clicked.connect(self.At_School)
        self.ui.radioButton_9.clicked.connect(self.Leave_School)
    def At_School(self):
        self.ui.dateTimeEdit_2.setDisabled(True)
        self.ui.radioButton_16.setDisabled(True)
        self.ui.radioButton_17.setDisabled(True)
    def Leave_School(self):
        self.ui.radioButton_16.setDisabled(False)
        self.ui.radioButton_17.setDisabled(False) 
        self.ui.radioButton_16.setChecked(True)  
    def Now_Time_clicked_1(self):
        self.ui.dateTimeEdit.setDisabled(True)
    def Choose_Other_Time_clicked_1(self):
        self.ui.dateTimeEdit.setDisabled(False)
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())    
    def Now_Time_clicked_2(self):
        self.ui.dateTimeEdit_2.setDisabled(True)
    def Choose_Other_Time_clicked_2(self):
        self.ui.dateTimeEdit_2.setDisabled(False)
        self.ui.dateTimeEdit_2.setDateTime(QDateTime.currentDateTime()) 

    def Save_Data(self):
        if self.ui.lineEdit.text()=="":
            QMessageBox.about(self.ui,'提示','请输入姓名！')
            return
        if self.ui.lineEdit_2.text()=="":
            QMessageBox.about(self.ui,'提示','请输入班级！')
            return  
        if self.ui.lineEdit_3.text()=="":
            QMessageBox.about(self.ui,'提示','请输入班主任姓名！')
            return  
        if self.ui.radioButton_4.isChecked()==True:
            Sex="男"
        else:
            Sex="女"
        if  self.ui.radioButton.isChecked()==True: 
            Class="高一"
        elif self.ui.radioButton_2.isChecked()==True:
            Class="高二"    
        else:
            Class="高三"
        if self.ui.radioButton_6.isChecked()==True:  
            Accommodation="是"
        else:
            Accommodation="否"
        if self.ui.radioButton_8.isChecked()==True:  
            InSchool="是"
            Leave_School_Time=""
        else:
            InSchool="否"
            if self.ui.radioButton_16.isChecked()==True:
                # strptime
                Leave_School_Time=str(QDateTime.currentDateTime().toString("yyyy-MM-dd H:mm:ss"))
            else:
                Leave_School_Time=str(self.ui.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd H:mm:ss"))
        if self.ui.radioButton_10.isChecked()==True:
            In_School_Time=str(QDateTime.currentDateTime().toString("yyyy-MM-dd H:mm:ss"))
        else:
            In_School_Time=str(self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd H:mm:ss"))
        SQL="UPDATE student SET Sex='%s',Class='%s',Whether_Or_Not_Accommodation='%s',Whether_Or_Not_In_School='%s',Headteacher='%s',Name='%s',Time_Of_Admission='%s',School_Leaving_Time='%s' WHERE Student_ID='%s'"%(Sex,Class+"_"+self.ui.lineEdit_2.text(),Accommodation,InSchool,self.ui.lineEdit_3.text(),self.ui.lineEdit.text(),In_School_Time,Leave_School_Time,self.student_id)
        Data.DataBase.Submit_For_Execution(SQL)
        ShowQuanbu()
        QMessageBox.about(self.ui,'提示','数据修改成功！')
        self.ui.close()
class Control:
    def read_data_to_tableview1(Class,AtSchool,OutSchool,d):
        count=0
        Data.Model.removeRows(0,Data.Model.rowCount())
        for i in Data.Student_Data:
            item1 = QStandardItem(i[0])
            item2 = QStandardItem(i[1])
            item3 = QStandardItem(i[2])
            item4 = QStandardItem(i[3])
            item5 = QStandardItem(i[4])
            item6 = QStandardItem(i[5])
            item7 = QStandardItem(i[6])
            item8=QStandardItem(i[7])
            item9=QStandardItem(i[8])
            # item10=QStandardItem(i[9])
            item1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item5.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item6.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item7.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item8.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item9.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # print(i[0],i[9])
            if i[9]=="1" or i[9]=="是":
                item10=QStandardItem(i[9])
                item10.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item10.setBackground(QBrush(Qt.red))
                
                item11=QStandardItem(Data.DataBase.Excute("SELECT Reasons FROM StudentsGentOut WHERE Student_ID='%s';"%(i[0]))[0][0])
                item11.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            else:
                item10=QStandardItem("否")
                item10.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item11=QStandardItem("")    
            if i[5]=="1" or i[5]=="是":
                item6.setBackground(QBrush(Qt.green))
                if d=="是":
                    count=count+1
                    continue           
            else:
                item6.setBackground(QBrush(Qt.red)) 
                if verify_date_str_lawyer(i[8]):
                    Leave_School_Time=QDateTime.fromString(i[8],"yyyy-MM-dd H:mm:ss")
                    if int(Leave_School_Time.secsTo(QDateTime.currentDateTime()))/(3600)>24:
                        if d=="是" or d=="":
                            item9.setBackground(QBrush(Qt.yellow))
                        elif d=="否":
                            count=count+1
                            continue
                    elif d=="是":
                        count=count+1
                        continue     
                elif d=="是":
                    count=count+1
                    continue    
            Data.Model.appendRow([item1,item2,item3,item4,item5,item6,item7,item8,item9,item10,item11])
            if d=="是":
                Form.Main_Form.ui.pushButton_4.setText("当前显示%s学生，在校%s人，不在校%s人，总人数%s人"%(Class,str(0),str(int(AtSchool)+int(OutSchool)-count),str(int(AtSchool)+int(OutSchool)-count)))        
            elif d=="否":
                Form.Main_Form.ui.pushButton_4.setText("当前显示%s学生，在校%s人，不在校%s人，总人数%s人"%(Class,str(AtSchool),str(int(OutSchool)-count),str(int(AtSchool)+int(OutSchool)-count)))        
            else:        
                Form.Main_Form.ui.pushButton_4.setText("当前显示%s学生，在校%s人，不在校%s人，总人数%s人"%(Class,str(AtSchool),str(OutSchool),str(int(AtSchool)+int(OutSchool))))    
        print("数据加载成功！")  
        # print(count)  
    def read_data_to_tableview(Class,AtSchool,OutSchool):
        Data.Model.removeRows(0,Data.Model.rowCount())
        # Data.Students_On_Leave=Data.DataBase.Excute("SELECT Student_ID FROM StudentsGentOut WHERE Student_ID !='';")[0]
        for i in Data.Student_Data:
            item1 = QStandardItem(i[0])
            item2 = QStandardItem(i[1])
            item3 = QStandardItem(i[2])
            item4 = QStandardItem(i[3])
            item5 = QStandardItem(i[4])
            item6 = QStandardItem(i[5])
            item7 = QStandardItem(i[6])
            item8=QStandardItem(i[7])
            item9=QStandardItem(i[8])
            # item10=QStandardItem(i[9])
            item1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item5.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item6.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item7.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item8.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item9.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # print(i[0],i[9])
            if i[9]=="1" or i[9]=="是":
                item10=QStandardItem(i[9])
                item10.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item10.setBackground(QBrush(Qt.red))
                
                item11=QStandardItem(Data.DataBase.Excute("SELECT Reasons FROM StudentsGentOut WHERE Student_ID='%s';"%(i[0]))[0][0])
                item11.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            else:
                item10=QStandardItem("否")
                item10.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item11=QStandardItem("")    
            if i[5]=="1" or i[5]=="是":
                item6.setBackground(QBrush(Qt.green))
            else:
                item6.setBackground(QBrush(Qt.red)) 
                if verify_date_str_lawyer(i[8]):
                    Leave_School_Time=QDateTime.fromString(i[8],"yyyy-MM-dd H:mm:ss")
                    if int(Leave_School_Time.secsTo(QDateTime.currentDateTime()))/(3600)>24:
                        item9.setBackground(QBrush(Qt.yellow))

            Data.Model.appendRow([item1,item2,item3,item4,item5,item6,item7,item8,item9,item10,item11])
            Form.Main_Form.ui.pushButton_4.setText("当前显示%s学生，在校%s人，不在校%s人，总人数%s人"%(Class,str(AtSchool),str(OutSchool),str(int(AtSchool)+int(OutSchool))))
        print("数据加载成功！")    
class Data:
    DataBase=None
    Student_Count=0     
    Student_Data=None
    Model=None 
    Students_On_Leave=None   
    Pic=""   
class MyButtonDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(MyButtonDelegate, self).__init__(parent)
    def DeleteButtonClicked(self):
        a = QMessageBox.question(self.parent(), '提示', '确定删除该数据?(按回车确定)', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) 
        if a == QMessageBox.Yes:  

            SQL="DELETE FROM student where Student_ID='%s'"%(Data.Student_Data[self.sender().index[0]][0])
            Data.DataBase.Submit_For_Execution(SQL)
            Data.Student_Data=Data.DataBase.Excute("SELECT * FROM student ;")
            Control.read_data_to_tableview()
        else:  
            print("取消")
    def ChangeButtonClicked(self):
        Form.Change_Form=Change_Form()   
         
        Information=Data.Student_Data[self.sender().index[0]]
        print("选中的数据",Information)
        Form.Change_Form.student_id=Information[0]
        Form.Change_Form.ui.lineEdit.setText(Information[1])
        if Information[2]=="男":
            Form.Change_Form.ui.radioButton_4.setChecked(True)
        else:
            Form.Change_Form.ui.radioButton_5.setChecked(True)
        Class=Information[3].split("_")
        if Class[0]=="高一":
            Form.Change_Form.ui.radioButton.setChecked(True)   
        elif Class[0]=="高二":
            Form.Change_Form.ui.radioButton_2.setChecked(True)   
        else:
            Form.Change_Form.ui.radioButton_3.setChecked(True) 
        Form.Change_Form.ui.lineEdit_2.setText(Class[1])
        if Information[4]=="是" or Information[4]=="1":
            Form.Change_Form.ui.radioButton_6.setChecked(True) 
        else:
            Form.Change_Form.ui.radioButton_7.setChecked(True)    
        if Information[5]=="是" or Information[5]=="1":
            Form.Change_Form.ui.radioButton_8.setChecked(True) 
            Form.Change_Form.ui.dateTimeEdit_2.setDisabled(True)
            Form.Change_Form.ui.radioButton_16.setDisabled(True)
            Form.Change_Form.ui.radioButton_17.setDisabled(True) 
        else:
            Form.Change_Form.ui.radioButton_9.setChecked(True) 
        Form.Change_Form.ui.lineEdit_3.setText(Information[6])  
        if verify_date_str_lawyer(Information[7])==False:
            Form.Change_Form.ui.radioButton_10.setChecked(True)
        else:
            Form.Change_Form.ui.radioButton_11.setChecked(True) 
            Form.Change_Form.ui.dateTimeEdit.setDateTime(QDateTime.fromString(Information[7],"yyyy-MM-dd H:mm:ss")) 
            
        if verify_date_str_lawyer(Information[8])==False and Form.Change_Form.ui.radioButton_9.isChecked()==True:
            Form.Change_Form.ui.radioButton_16.setChecked(True)
        else:
            Form.Change_Form.ui.radioButton_17.setChecked(True) 
            Form.Change_Form.ui.dateTimeEdit_2.setDateTime(QDateTime.fromString(Information[8],"yyyy-MM-dd H:mm:ss"))   
 
        Form.Change_Form.ui.dateTimeEdit.setCalendarPopup(True)
        Form.Change_Form.ui.dateTimeEdit_2.setCalendarPopup(True)
        Form.Change_Form.ui.show() 
    def Leave_Application(self):   
        SQL="SELECT Whether_To_Ask_For_Leave FROM student WHERE Student_ID='%s'"%(Data.Student_Data[self.sender().index[0]][0])
        a=Data.DataBase.Excute(SQL)[0][0]
        if a=="1" or a=="是":
            QMessageBox.about(self.parent(),"提示","该学生已经请假请假！\n再次申请请假，请先销假！")
            return
        data={
                "Name":Data.Student_Data[self.sender().index[0]][1],
                "Student_ID":Data.Student_Data[self.sender().index[0]][0],
                "Class":Data.Student_Data[self.sender().index[0]][3]
            }
        Form.Leave_Application_Form=Leave_Application_Form(data)
        Form.Leave_Application_Form.ui.show()
    def VacationButtonClicked(self):
        SQL="SELECT Whether_To_Ask_For_Leave FROM student WHERE Student_ID='%s'"%(Data.Student_Data[self.sender().index[0]][0])
        a=Data.DataBase.Excute(SQL)[0][0]
        if a=="1" or a=="是":
            data={
                "Name":Data.Student_Data[self.sender().index[0]][1],
                "Student_ID":Data.Student_Data[self.sender().index[0]][0],
                "Class":Data.Student_Data[self.sender().index[0]][3]
            }
            Form.Vacation_Form=Vacation_Form(data)
            Form.Vacation_Form.ui.show()
        else:
            QMessageBox.about(self.parent(),"提示","该学生未请假！")
            return
    def paint(self, painter, option, index):
        if not Form.Main_Form.ui.tableView.indexWidget(index):
            button_read = QPushButton(
                self.tr('删除数据'),
                Form.Main_Form.ui.tableView,            
                clicked=self.DeleteButtonClicked
            )
            # button_read.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))
            button_write = QPushButton(
                self.tr('修改数据'),
                Form.Main_Form.ui.tableView,
                clicked=self.ChangeButtonClicked
            )

            # print(data)
            button_LeaveApplication= QPushButton(
                self.tr('请假申请'),
                Form.Main_Form.ui.tableView,
        
                clicked=self.Leave_Application
            )
            button_Vacation = QPushButton(
                self.tr('销假'),
                Form.Main_Form.ui.tableView,
                clicked=self.VacationButtonClicked
            )
            # button_write.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))
            button_read.index = [index.row(), index.column()]
            button_write.index = [index.row(), index.column()]
            button_LeaveApplication.index = [index.row(), index.column()]
            button_Vacation.index = [index.row(), index.column()]
            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(button_read)
            h_box_layout.addWidget(button_write)
            h_box_layout.addWidget(button_LeaveApplication)
            h_box_layout.addWidget(button_Vacation)
            h_box_layout.setContentsMargins(0, 0, 0, 0)
            h_box_layout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(h_box_layout)
            Form.Main_Form.ui.tableView.setIndexWidget(
                index,
                widget
            )
if __name__=="__main__":
    # print(verify_date_str_lawyer("123"))
    Data.DataBase=DataBase.DataBaseSqlite()
    Data.DataBase.Connect_DataBase()
    Data.Student_Count=Data.DataBase.Excute("SELECT COUNT(*) FROM student ;")[0][0]
    
    app=QApplication([])
    Form.Main_Form=Main_Form()
    Form.Main_Form.ui.show()

    Form.Main_Form.ui.tableView.setItemDelegateForColumn(11, MyButtonDelegate(Form.Main_Form.ui.tableView))  
    Data.Model = QStandardItemModel(0, 12)
    Data.Model.setHorizontalHeaderLabels(["学号","姓名","性别","班级","是否住校","是否在校","班主任","入校时间","出校时间","是否请假","请假理由","操作"])

    Form.Main_Form.ui.tableView.setModel(Data.Model) 
    Form.Main_Form.ui.tableView.setColumnWidth(11,300)
    Form.Main_Form.ui.tableView.setColumnWidth(10,250)
    Form.Main_Form.ui.tableView.setColumnWidth(7,200)
    Form.Main_Form.ui.tableView.setColumnWidth(8,200)

    Form.Main_Form.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
    Form.Main_Form.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    Form.Main_Form.ui.tableView.horizontalHeader().setFont(QFont('Microsoft YaHei', 18, QFont.Bold))

    ShowQuanbu()   
    app.exec_()



