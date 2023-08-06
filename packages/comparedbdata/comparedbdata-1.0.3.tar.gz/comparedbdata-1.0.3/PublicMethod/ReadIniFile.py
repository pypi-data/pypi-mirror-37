import os
import configparser

class MyConfigParser(configparser.ConfigParser):
    '''因config.items调用的optionxform方法
    会将大写字母转换成小写字母故将其重载'''
    def __init__(self):
        super().__init__()

    def optionxform(self, optionstr):
        return optionstr

class FindFileContentAndDir ():
    '''传入文件名获取configure目录下完整文件地址'''
    def __init__(self,filename):
        data_dir = str(os.path.dirname(os.path.dirname(__file__)))
        data_dir = data_dir.replace('\\', '/')
        self.file_path = data_dir + "/Configure/"+filename
        self.__init_config()
        self.get_all_section_name()

    def __init_config(self):
        self.config=MyConfigParser()
        self.config.read(self.file_path,encoding='utf-8')

    def get_all_section_name(self):
        '''获取配置文件所有节点名称'''
        self.allsectionname = self.config.sections()

    def section_data(self,sectionname):
        '''读取UTF-8字符集的.ini文件,返回指定section节点下数据'''
        lists=self.config.items(sectionname)
        data={}
        for tuples in lists:
            for i in range(0,len(tuples)):
                data[tuples[0]]=tuples[1]
        return data

if __name__=="__main__":
    print(FindFileContentAndDir("DataBaseInfo.ini").section_data("TargetDataBase"))
    test=FindFileContentAndDir("DataBaseInfo.ini")
    a=test.allsectionname
    print(a)