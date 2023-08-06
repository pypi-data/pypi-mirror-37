from DatabaseCommander.DataBaseUserInfo import IniFileInfo
from DatabaseCommander.OperateDataBase import QueryExportData
from ZipCommander.zipfiledata import ZipFileData
from PublicMethod.OperateIniFile import OperateIni
from copy import deepcopy
import os
import pytest

WHITEINI="whiteList.ini"
ini=IniFileInfo(WHITEINI)
whiteinidata=ini.inisectiondata[0]
whiteinifile=OperateIni(WHITEINI,encoding='gbk')
path=os.path.dirname(os.path.dirname(__file__))
EXPORT_DATA_PATH = path + os.path.sep + "ExportData" + os.path.sep + "export"
zipfile=ZipFileData(EXPORT_DATA_PATH)

class WhiteTableDependData():
    '''获取白名单内关联数据'''
    def __init__(self):
        _dependini = IniFileInfo("wordsrelatetodb.ini")
        self.__dependdata = _dependini.inisectiondata[0]
        self.__query_data()

    def __query_data(self):
        self.result = dict()
        for DBsectionname, value in self.__dependdata.items():
            dboperator = QueryExportData(DBsectionname)
            for keywords, tablenames in value.items():
                if keywords == "planid":
                    tempkeywords = "id"
                elif keywords == "UnitProjKey":
                    continue
                elif keywords == "pic_id":
                    tempkeywords = "file_id"
                else:
                    tempkeywords = keywords
                for tablename in tablenames:
                    self.result[keywords] = dboperator.query_condition_date(tempkeywords, tablename)
        unitProjKeylist = []
        for list in self.result["projId"]:
            for key, value in list.items():
                unitProjKeylist.append({"UnitProjKey": value})
        self.result["UnitProjKey"] = unitProjKeylist

    def according_key_quert_data(self, key:str):
        '''根据key,查询白名单中对应的列表'''
        results = [values for dictkey, values in self.result.items() if key == dictkey][0]
        return results

@pytest.fixture(params=whiteinidata)
def white_db_config(request):
    return request.param

@pytest.fixture()
def white_ini_key_and_value(white_db_config):
    # whitetablename=list(whiteinifile.get_section_data(white_db_config).values())
    whitetablename=whiteinifile.get_section_data(white_db_config)
    return whitetablename

def test(white_ini_key_and_value):
    print(white_ini_key_and_value)

@pytest.fixture()
def db_object(white_db_config):
    if white_db_config!=None:
        db=QueryExportData(white_db_config.lower())
        return db
#
whitetabledepengdata=WhiteTableDependData()
whitedata=whitetabledepengdata.result
#
@pytest.mark.tablenums
def test_white_table_nums(white_db_config,white_ini_key_and_value,db_object):
    def loop_result(result):
        copykeydata = deepcopy(result)
        for data in copykeydata:
            for k,v in data.items():
                data["proxyprojid"]=v
        return copykeydata
    for key,strtable in white_ini_key_and_value.items():
        tablelist=strtable.split(",")
        keydata = whitetabledepengdata.according_key_quert_data(key)
        for table in tablelist:
            data=keydata if table!="projectdataversion" else loop_result(keydata)
            result=db_object.query_data_rownum(table,white_db_config.lower(),
                                               conditionlist=data)
            for table, nums in result.items():
                assert nums == zipfile.get_file_data_line_num(white_db_config.lower()
                                                              + os.path.sep + table + ".csv")

@pytest.mark.tableexistornot
def test_white_table_exist_or_not(white_db_config,white_ini_key_and_value,db_object):
    def loop_result(result):
        copykeydata = deepcopy(result)
        for data in copykeydata:
            for k,v in data.items():
                data["proxyprojid"]=v
        return copykeydata
    for key,strtable in white_ini_key_and_value.items():
        tablelist=strtable.split(",")
        keydata = whitetabledepengdata.according_key_quert_data(key)
        for initable in tablelist:
            data=keydata if initable!="projectdataversion" else loop_result(keydata)
            result=db_object.query_data_rownum(initable,white_db_config.lower(),
                                               conditionlist=data).keys()
            for table in result:
                assert table in zipfile.dir_file_names(white_db_config.lower())

# print(whitedata)

# @pytest.mark.tableexistornot
# def test_white_table_exist_or_not(white_db_config,white_ini_key_and_value,db_object):
#     def loop_result(result):
#         for table in result:
#             assert table in zipfile.dir_file_names(white_db_config.lower())
#     for key,strtable in white_ini_key_and_value.items():
#         tablelist=strtable.split(",")
#         keydata = whitetabledepengdata.according_key_quert_data(key)
#         for table in tablelist:
#             if table=="projectdataversion":
#                 copykeydata = deepcopy(keydata)
#                 for data in copykeydata:
#                     for k,v in data.items():
#                         data["proxyprojid"]=data.pop(k)
#                 result=db_object.query_data_rownum(table,white_db_config.lower(),
#                                                    conditionlist=copykeydata).keys()
#                 loop_result(result)
#             else:
#                 result=db_object.query_data_rownum(table,white_db_config.lower(),
#                                                    conditionlist=keydata).keys()
#                 loop_result(result)
#
# @pytest.mark.tablenums
# def test_white_table_nums(white_db_config,white_ini_key_and_value,db_object):
#     def loop_result(result):
#         for table,nums in result.items():
#             assert nums == zipfile.get_file_data_line_num(white_db_config.lower()
#                                                            +os.path.sep+table+".csv")
#     for key,strtable in white_ini_key_and_value.items():
#         tablelist=strtable.split(",")
#         keydata = whitetabledepengdata.according_key_quert_data(key)
#         for table in tablelist:
#             if table=="projectdataversion":
#                 copykeydata = deepcopy(keydata)
#                 for data in copykeydata:
#                     for k,v in data.items():
#                         data["proxyprojid"]=data.pop(k)
#                 result=db_object.query_data_rownum(table,white_db_config.lower(),
#                                                    conditionlist=copykeydata)
#                 loop_result(result)
#             else:
#                 result=db_object.query_data_rownum(table,white_db_config.lower(),
#                                                    conditionlist=keydata)
#                 loop_result(result)


if __name__ == '__main__':
    w=WhiteTableDependData()
    a=w.according_key_quert_data("ppid")
    # print(a)
    # print(w.result)
