from DatabaseCommander.DataBaseUserInfo import IniFileInfo
from DatabaseCommander.OperateDataBase import QueryExportData
from ZipCommander.zipfiledata import ZipFileData
import os
from PublicMethod.OperateIniFile import OperateIni
import pytest

COMMONTABLE="commTable.ini"
ini=IniFileInfo(COMMONTABLE)
commoninidata=ini.inisectiondata[0]
comminifile=OperateIni(COMMONTABLE)
path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(path)
# path=os.path.dirname(os.path.dirname(__file__))
EXPORT_DATA_PATH = path + os.path.sep + "ExportData" + os.path.sep + "export"
zipfile=ZipFileData(EXPORT_DATA_PATH)

@pytest.fixture(params=commoninidata)
def common_db_config(request):
    return request.param

@pytest.fixture()
def common_table_name_list(common_db_config):
    commontablename=list(comminifile.get_section_data(common_db_config).values())
    commonlist=commontablename[0].split(",")
    return commonlist

@pytest.mark.tableexistornot
def test_common_table_exist_or_not(common_table_name_list,common_db_config):
    dbconfig=common_db_config.lower()
    db=QueryExportData(dbconfig)
    for common_table_name in common_table_name_list:
        nums=db.query_table_data_nums(common_table_name)
        if nums!=0:
            filelist = zipfile.dir_file_names(common_db_config)
            assert common_table_name in filelist

@pytest.mark.tablenums
def test_common_table_nums(common_table_name_list,common_db_config):
    dbconfig=common_db_config.lower()
    db=QueryExportData(dbconfig)
    for common_table_name in common_table_name_list:
        nums=db.query_table_data_nums(common_table_name)
        if nums!=0:
            filenums = zipfile.get_file_data_line_num(dbconfig + os.path.sep
                                                      + common_table_name + ".csv")
            assert filenums==nums

# @pytest.fixture()
# def common_table_name(common_table_name_list):
#     for common_table in common_table_name_list:
#         return common_table

# def test(common_table_name_list):
#     # pass
#     print(common_table_name_list)

# def common_table_nums(common_db_config,common_table_name):
#     # try:
#     print(common_table_name)
#     dbconfig=common_db_config.lower()
#     # print(dbconfig)
#     db=QueryExportData(dbconfig)
#     nums=db.query_table_data_nums(common_table_name)
#     print(nums)
#     if nums!=0:
#         return common_table_name
#     # except AttributeError:
#     #     print(common_db_config,"no mysql data")

if __name__ == '__main__':
    pytest.main(['-m=tableexistornot','-v','-n=auto'])
    # pytest.main(['-s', 'mark_01.py', "-m=webtest"])



