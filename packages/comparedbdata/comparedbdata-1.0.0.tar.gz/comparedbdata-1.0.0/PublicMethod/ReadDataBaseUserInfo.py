from PublicMethod.ReadIniFile import FindFileContentAndDir

class GetConnectDataBaseInfo(FindFileContentAndDir):
    '''读取配置文件中的db配置'''
    def __init__(self,SectionName,Filename='DataBaseInfo.ini',):
        super().__init__(Filename)
        self.Data=self.section_data(SectionName)

    def get_value(self, Key):
        for key,value in self.Data.items():
            if key==Key:
                return value

if __name__=='__main__':
    Info=GetConnectDataBaseInfo("OriginalDataBase")
    print(Info.get_value("host"))