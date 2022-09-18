from contextlib import nullcontext
from PySide2.QtUiTools import QUiLoader
from time import time
from PySide2.QtUiTools import loadUiType
from PySide2.QtGui import QStandardItemModel,QStandardItem
import os
from PySide2.QtWidgets import (QApplication, QHBoxLayout, QItemDelegate, QPushButton, QTableView, QWidget)
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import DataBase
def read_data_to_tableview():
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
        item10=QStandardItem(i[9])
        item11=QStandardItem(i[10])
        item12=QStandardItem(i[13])
        item1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item5.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item6.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item7.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item8.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item9.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item10.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item11.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item12.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        Data.Model.appendRow([item1,item2,item3,item4,item5,item6,item7,item8,item9,item10,item11,item12])
    print("数据加载成功！")    
class Form:
    Main_Form=None
class Data:
    DataBase=None
    Model=None 
    Student_Data=None
class Main_Form(QWidget):
    def __init__(self):
        self.ui=QUiLoader().load('history.ui') 
class MyButtonDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(MyButtonDelegate, self).__init__(parent)
    def ShowButtonClicked(self):
        if os.path.isfile(os.getcwd()+"\\Data\\"+Data.Student_Data[self.sender().index[0]][12])!=True:
            QMessageBox.about(Form.Main_Form.ui,"提示","材料文件不存在！\n文件可能丢失！通常保存在程序根目录的Data文件夹下！")     
            return 
        os.startfile(os.getcwd()+"\\Data\\"+Data.Student_Data[self.sender().index[0]][12])    
    def paint(self, painter, option, index):
        if not Form.Main_Form.ui.tableView.indexWidget(index):
            button_read = QPushButton(
                self.tr('查看材料'),
                Form.Main_Form.ui.tableView,            
                clicked=self.ShowButtonClicked
            )
            button_read.index = [index.row(), index.column()]
            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(button_read)
            h_box_layout.setContentsMargins(0, 0, 0, 0)
            h_box_layout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(h_box_layout)
            Form.Main_Form.ui.tableView.setIndexWidget(
                index,
                widget
            )
if __name__=="__main__":
    Data.DataBase=DataBase.DataBaseSqlite()
    Data.DataBase.Connect_DataBase()  
    app=QApplication([])
    Form.Main_Form=Main_Form()
    Form.Main_Form.ui.show() 
    Form.Main_Form.ui.tableView.setItemDelegateForColumn(12, MyButtonDelegate(Form.Main_Form.ui.tableView))  
    Data.Model = QStandardItemModel(0, 13)
    Data.Model.setHorizontalHeaderLabels(["学号","姓名","性别","班级","是否住校","是否在校","班主任","入校时间","出校时间","是否请假","请假理由","操作时间","查看材料"])
    Form.Main_Form.ui.tableView.setModel(Data.Model) 
    Form.Main_Form.ui.tableView.setColumnWidth(11,200)
    Form.Main_Form.ui.tableView.setColumnWidth(10,200)
    Form.Main_Form.ui.tableView.setColumnWidth(7,200)
    Form.Main_Form.ui.tableView.setColumnWidth(8,200)
    Form.Main_Form.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
    Form.Main_Form.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    Data.Student_Data=Data.DataBase.Excute("SELECT * FROM History ;")
    read_data_to_tableview()
    app.exec_()     