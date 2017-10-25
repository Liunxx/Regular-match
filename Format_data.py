import  csv
import re


class formatdata(object):
    #函数初始化
    def __init__(self):
        self.phoneNumber=[]
        self.content={}
        self.result={}
        self.loadData()
        self.final_result=[]#最终的结果
        self.final_phoneNumber=[]#最终的电话号码
        self.final_Name=[]#最终的姓名

    #把最终的数据进行分析，处理，整合，并写入csv文件，同时也是程序入口
    def analydata(self):
        for i in self.phoneNumber:
             if self.regre(i):
                 self.result[i]=self.content[i]
        self.getPhoneNumber()
        self.getName()
        self.ConsData()
        self.writeData()

    #利用正则对初始文件里的电话进行初步筛选
    def regre(self,con):
        pattern=re.compile(r'\d{3}-\d{3}-\d{4}|\(\d{3}\)\s*\d{3}-\d{4}|\d{3}\.\d{3}\.\d{4}|\d{10}|\d{1}-\d{3}-\d{3}-\d{4}')
        matcher=pattern.match(con)
        if matcher:
            return 1
        return 0

    #利用正则对电话号码进行处理，形成最终所要的形式
    def getPhoneNumber(self):
        pattern1=re.compile(r'(\d{3})-(\d{3})-(\d{4})')
        pattern2=re.compile(r'(\d{3})\.(\d{3})\.(\d{4})')
        pattern3=re.compile(r'\((\d{3})\)\s*(\d{3})-(\d{4})')
        pattern4=re.compile(r'(\d{3})(\d{3})(\d{4})')
        pattern5=re.compile(r'\d{1}-(\d{3})-(\d{3})-(\d{4})')
        num1=num2=num3=''
        for number in self.result:
            matcher1=pattern1.match(number)
            if matcher1:
                num1=matcher1.group(1)
                num2=matcher1.group(2)
                num3=matcher1.group(3)
            matcher2 = pattern2.match(number)
            if matcher2:
                num1 = matcher2.group(1)
                num2 = matcher2.group(2)
                num3 = matcher2.group(3)
            matcher3 = pattern3.match(number)
            if matcher3:
                num1 = matcher3.group(1)
                num2 = matcher3.group(2)
                num3 = matcher3.group(3)
            matcher4=pattern4.match(number)
            if matcher4:
                num1 = matcher4.group(1)
                num2 = matcher4.group(2)
                num3 = matcher4.group(3)
            matcher5 = pattern5.match(number)
            if matcher5:
                num1 = matcher5.group(1)
                num2 = matcher5.group(2)
                num3 = matcher5.group(3)
            phoneNumber='('+num1+') '+num2+'-'+num3
            self.final_phoneNumber.append(phoneNumber)
    #利用正则对姓名进行处理，得到最后想要的形式
    def getName(self):
        pattern1 = re.compile(r'[A-Z]\.')
        pattern2 = re.compile(r'([A-Z]*[a-z]*),')
        for number in self.result:
            tmp = ['', '', '']
            m = self.result[number].split(" ")
            mid_index = 3
            last_index = 3
            last_str = ''
            for index, j in enumerate(m):
                matcher = re.match(pattern1, j)
                if matcher:
                    mid_index = index
                matcher2 = re.match(pattern2, j)
                if matcher2:
                    last_index = index
                    last_str = matcher2.group(1)
            if len(m) == 2:
                tmp[1] = ''
                if last_index != 3:
                    tmp[2] = last_str
                    m.remove(m[last_index])
                else:
                    tmp[2] = m[1]
                tmp[0] = m[0]
            if len(m) == 3:
                tmp[1] = m[mid_index]
                m.remove(m[mid_index])
                if last_index != 3:
                    tmp[2] = last_str
                    m.remove(m[last_index])
                else:
                    tmp[2] = m[1]
                tmp[0] = m[0]
            self.final_Name.append(tmp)
    ###利用此函数把姓名和电话号码整合到一个list里
    def ConsData(self):
        for i in range(len(self.final_phoneNumber)):
            tmp_result = []
            for j in self.final_Name[i]:
                 tmp_result.append(j)
            tmp_result.append(self.final_phoneNumber[i])
            self.final_result.append(tmp_result)
    ###对csv里的数据进行读取
    def loadData(self):
         reader=csv.reader(open('data.csv', 'r'))
         for con in reader:
             self.phoneNumber.append(con[1])
             self.content[con[1]]=con[0]
    #写数据函数
    def writeData(self):
        HeadFile=['First','M.I.','Last','Number']
        csvFile=open('data3.csv','w')
        writer=csv.writer(csvFile)
        writer.writerow(HeadFile)
        for res in self.final_result:
            writer.writerow(res)
        csvFile.close()


if __name__=="__main__":
    fd=formatdata()
    fd.analydata()
