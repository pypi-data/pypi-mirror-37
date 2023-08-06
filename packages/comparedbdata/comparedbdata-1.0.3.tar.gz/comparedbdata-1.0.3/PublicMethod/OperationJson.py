import json
import os

class OperationJson():
    def __init__(self,FileName):
        data_dir = str(os.path.dirname(os.path.dirname(__file__)))
        data_dir = data_dir.replace('\\', '/')
        self.file_path = data_dir + "/Configure/"+FileName
        self.data=self.__read_data()

    def __read_data(self):
        '''读取json文件'''
        with open(self.file_path) as fp:
            data=json.load(fp)
            return data

    def get_data(self, key):
        '''根据关键字获取数据'''
        return self.data[key]

    def write_data(self,data):
        '''写入json文件'''
        with open(self.file_path,'w') as fp:
            fp.write(json.dumps(data))


if __name__=='__main__':
    opjson=OperationJson("DataBaseName.json")
    print(opjson.get_data("DataBaseName"))