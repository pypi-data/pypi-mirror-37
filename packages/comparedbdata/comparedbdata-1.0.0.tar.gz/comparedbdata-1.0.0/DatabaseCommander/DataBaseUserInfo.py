from PublicMethod.OperateIniFile import OperateIni

class DataBaseInfoManager(OperateIni):
    '''读取配置文件中的db配置'''
    def __init__(self,SectionName,Filename='DataBaseInfo.ini'):
        super().__init__(Filename)
        self.SectionName=SectionName
        self.Data=self.get_section_data(SectionName)

    def get_value(self, Key):
        '''获取指定Key的Value'''
        for key,value in self.Data.items():
            if key==Key:
                return value

    def modify_database_name(self,Value,Key="databasename"):
        '''修改配置中DataBaseName节点'''
        self.modify_section_data(self.SectionName,Value,Key)

class IniFileInfo():
    """组织ini文件数据"""
    def __init__(self,*configfilenames):
        self.inisectiondata = []
        for configfilename in configfilenames:
            self.ini_all_section_data(configfilename)

    # def ini_all_section_data(self):
    #     self.all_section_data=dict()
    #     for section in self.section_namelist:
    #         sectiondata=self.operationini.get_section_data(section)
    #         for key,value in sectiondata.items():
    #             valuelist=value.split(",")
    #             sectiondata[key]=valuelist
    #         self.all_section_data[section]=sectiondata

    def ini_all_section_data(self,filename):
        '''获取ini文件组装成数据'''
        # self.white_section_data = dict()
        # self.commontable_section_data = dict()
        section_data=dict()
        # for file in self.configfilenames:
        self.operationini=OperateIni(filename=filename,encoding="gbk")
        self.section_namelist=self.operationini.section_name
        for section in self.section_namelist:
            sectiondata=self.operationini.get_section_data(section)
            for key,value in sectiondata.items():
                valuelist=value.split(",")
                sectiondata[key]=valuelist
                section_data[section]=sectiondata
        self.inisectiondata.append(section_data)
            # if filename=="whiteList.ini":
            #     self.white_section_data[section]=sectiondata
            # elif filename=="commTable.ini":
            #     self.commontable_section_data[section]=sectiondata

    # def get_key_value(self,keyname:str):
    #     '''遍历所有节点，返回所有节点下指定key的值'''
    #     keyvaluelist=[]
    #     for section in self.section_namelist:
    #         sectiondata=self.operationini.get_section_data(section)
    #         for key,value in sectiondata.items():
    #             if key==keyname:
    #                 keyvaluelist.append(value)
    #     return keyvaluelist


if __name__=='__main__':
    Info=DataBaseInfoManager("TargetDataBase")
    # print(Info.get_value("databasename"))
    # Info.modify_database_name("123")
    w=IniFileInfo("whiteList.ini", "commTable.ini")
    # print(w.white_section_data)
    # print(w.commontable_section_data)
    print(w.inisectiondata[0])
    print(w.inisectiondata[1])


