import os
import configparser

class MyConfigParser(configparser.ConfigParser):
    '''因config.items调用的optionxform方法
    会将大写字母转换成小写字母故将其重载'''
    def __init__(self):
        super().__init__()

    def optionxform(self, optionstr):
        return optionstr

class OperateIni ():
    '''传入文件名获取configure目录下完整文件地址'''
    def __init__(self,filename,encoding='utf-8'):
        # data_dir=os.getcwd()
        data_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_path = data_dir + "/Configure/"+filename
        self.config=MyConfigParser()
        self.config.read(self.file_path,encoding)
        self.section_name = self.config.sections()

    def get_section_data(self, SectionName):
        '''读取UTF-8字符集的.ini文件,返回指定section节点下数据'''
        lists=self.config.items(SectionName)
        data={}
        for tuples in lists:
            for i in range(0,len(tuples)):
                data[tuples[0]]=tuples[1]
        return data

    def modify_section_data(self,SectionName,Value,Key):
        '''修改某节点下数据'''
        self.config.set(SectionName,Key,Value)
        with open(self.file_path,'w') as f:
            self.config.write(f)

    # def get_all_section_name(self):
    #     self.section_name=self.config.sections()


if __name__=='__main__':
    OI=OperateIni("DataBaseInfo.ini")
    print(OI.get_section_data("TargetDataBase"))
    # OI.modify_section_data("TargetDataBase","123","port")
    # print(OI.section_name)
