from xml.etree.ElementTree import tostring
from faker import Faker
import csv
import random
import datetime
from time import strftime
fake = Faker("zh_CN")
Data=[]
for i in range(1000):
    
    Class_=random.randint(1,3)
    Class=""
    Sex_=random.randint(0,1)
    Sex=""
    banji=random.randint(1,26)
    Student_ID=""
    if Class_==1:
        Class="高一"
        Student_ID="21"+str(Sex_)+str(banji).zfill(2)+str(random.randint(1,50)).zfill(2)
    if Class_==2:
        Class="高二"
        Student_ID="22"+str(Sex_)+str(banji).zfill(2)+str(random.randint(1,50)).zfill(2)
    if Class_==3:
        Class="高三"
        Student_ID="23"+str(Sex_)+str(banji).zfill(2)+str(random.randint(1,50)).zfill(2)
    if Sex_==0:
        Sex="女"
    if Sex_==1:
        Sex="男"        
    Data.append([Student_ID,fake.name(),Sex,Class+"_"+str(banji),str(random.randint(0,1)),str(random.randint(0,1)),fake.name(),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
print(Data)
with open("new_data.csv", mode="w+", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    for i in Data:
        writer.writerow(i)