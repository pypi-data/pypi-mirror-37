import zipfile
import os
import shutil
import sys
from pprint import pprint
import re
from DatabaseCommander.OperateDataBase import ImportDataOperater
# path=os.path.dirname(os.path.dirname(__file__))

class ZipFileData():
    def __init__(self,filepath):
        self.datafilepath=filepath
        # self.unzip_file()
        # self.datafilelist=dict()
        self.__get_mysql_dir_name()
        self.__get_file_path_list()

    # def get_file_dir_name(self):
    #     dirs=os.listdir(self.filerootpath)
    #     for dir in dirs:
    #         if dir=="fileuuid.txt":
    #             dirs.remove(dir)
    #     return dirs

    # def get_file_name(self,path):
    #     filename=os.listdir(path)
    #     return filename

    def dir_file_names(self, dirname):
        '''获取指定目录下所有文件名'''
        dirfilenames=os.listdir(self.datafilepath + os.path.sep + dirname)
        filename=map(lambda file:file[:-4],dirfilenames)
        return filename

    def __get_mysql_dir_name(self):
        self.datadirlist=[]
        dirlist=os.listdir(self.datafilepath)
        for dir in dirlist:
            if "luban" in dir:
                self.datadirlist.append(dir)

    def get_file_data(self,filepath):
        with open(filepath,encoding="utf-8") as f:
            linedata=list(f.readline().rstrip("\n").replace('"','').split(","))
            # linedata=list(f.readline().rstrip("\n").split('^("?|"{?).*("?|}"?)$'))
            # strlinedata=f.readline()
            # linedata=re.split('^(("|"{)?).*(("|}")?)$',strlinedata)
        return linedata

    def get_file_data_line_num(self,filename):
        '''filename：dbname/filename'''
        filepath=self.datafilepath+os.path.sep+filename
        with open (filepath,encoding="utf-8") as f:
            line_num=len(f.readlines())
        return line_num

    # def get_file_path_list(self):
    # def get_file_path_list(self,rootfilepath):
    #     self.filepathslist=[]
    #     # for root,dir,files in os.walk(self.datafilepath):
    #     for root, dir, files in os.walk(rootfilepath):
    #         if "mongodb" in root:
    #             continue
    #         for file in files:
    #             if ".csv" in file:
    #                 if "copy" not in file:
    #                     filepath=os.path.join(root,file)
    #                     self.filepathslist.append(filepath)

    def __get_file_path_list(self):
        self.filepathsdict=dict()
        for path in self.datadirlist:
        # for root,dir,files in os.walk(self.datafilepath):
            rootfilepath=self.datafilepath+os.path.sep+path
            filelist=list()
            for root, dir, files in os.walk(rootfilepath):
                if "mongodb" in root:
                    continue
                for file in files:
                    if ".csv" in file:
                        if "copy" not in file:
                            filepath=os.path.join(root,file)
                            filelist.append(filepath)
            self.filepathsdict[path]=filelist

    @staticmethod
    def unzip_file(zipfileroot):
        '''解压文件'''
        # self.zipfileroot=filepath+r"/ExportData"
        filerootpath= zipfileroot + r"/export"
        if os.path.exists(filerootpath):
            shutil.rmtree(filerootpath)
        filename=os.listdir(zipfileroot)
        zipfilepath=zipfileroot+filename[0]
        f=zipfile.ZipFile(zipfilepath,'r')
        f.extractall(zipfileroot)
        # for file in f.namelist():
        #     f.extract(file,zipfileroot)
        f.close()

    # def unzip_file(self):
    #     if os.path.exists(self.filerootpath):
    #         shutil.rmtree(self.filerootpath)
    #     filename=os.listdir(self.zipfileroot)
    #     zipfilepath=self.zipfileroot+filename[0]
    #     f=zipfile.ZipFile(zipfilepath,'r')
    #     f.extractall(self.zipfileroot)
    #     # for file in f.namelist():
    #     #     f.extract(file,zipfileroot)
    #     f.close()

if __name__=="__main__":
    z=ZipFileData(r"E:\gittest\CompareDataBase\ExportData\export")
    # print(z.datadirlist)
    # print(list(z.dir_file_name("lubanbe")))
    print(z.get_file_data_line_num("lubanmc\pds_initmark.csv"))
    # z.unzip_file()
    # z.get_file_dir_name()
    # pprint(z.get_file_path_list("F:/GitHubProject/CompareDataBase/ExportData/export/lubanbe"))
    # for key,value in z.filepathsdict.items():
    #     # print(key,value)
    #     for v in value:
    #         print(z.get_file_data_line_num(v))
    #         sum+=z.get_file_data_line_num(v)
    # p=z.get_mysql_dir_name()
    # print(p)

    # data=z.get_file_data("F:/GitHubProject/CompareDataBase/ExportData/export/lubanmcbackendsystem/viewport_mngtree.csv")
    # print(data)
    # for dat in data:
    #     print(dat)
    # print(z.get_file_data_line_num("F:/GitHubProject/CompareDataBase/ExportData/export/lubanbe/attr_template.csv"))
    # data=OperateDataBase("TargetDataBase")
