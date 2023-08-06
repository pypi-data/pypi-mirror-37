from DatabaseCommander.DataBaseUserInfo import IniFileInfo
from DatabaseCommander.OperateDataBase import QueryExportData
from ZipCommander.zipfiledata import ZipFileData
import os
import pytest


ALLLUBANDBCONFIG="all-luban-subsystem-db-config.ini"
ini=IniFileInfo(ALLLUBANDBCONFIG)
alllubanconfig=ini.inisectiondata[0]
path=os.path.dirname(os.path.dirname(__file__))
EXPORT_DATA_PATH = path + os.path.sep + "ExportData" + os.path.sep + "export"
zipfile=ZipFileData(EXPORT_DATA_PATH)

@pytest.fixture(params=alllubanconfig)
def all_db_config(request):
    if request.param != "common-connectionpooling" and \
            request.param != "common-connection-info":
        return request.param

@pytest.fixture()
def db_object(all_db_config):
    if all_db_config!=None:
        try:
            db=QueryExportData(all_db_config)
            return db
        except AttributeError:
            print(all_db_config,"no mysql data")

@pytest.mark.tableexistornot
def test_epid_table_exist_or_not(db_object, all_db_config):
    if all_db_config!=None and db_object!=None:
        epidcorrelationtablenamelist=db_object.filter_table_with_eqid()
        for epidcorrelationtablename in epidcorrelationtablenamelist:
            filelist=zipfile.dir_file_names(all_db_config)
            if epidcorrelationtablename !=None:
                assert epidcorrelationtablename in filelist

@pytest.mark.tablenums
def test_epid_table_data(db_object,all_db_config):
    if all_db_config!=None and db_object!=None:
        epidcorrelationtablenamelist=db_object.filter_table_with_eqid()
        for epidcorrelationtablename in epidcorrelationtablenamelist:
            datanums=db_object.query_table_data_nums(epidcorrelationtablename)
            filenums = zipfile.get_file_data_line_num(all_db_config + os.path.sep
                                                      + epidcorrelationtablename + ".csv")
            assert datanums==filenums


# @pytest.fixture()
# def epid_correlation_table_namelist(db_object, all_db_config):
#     if all_db_config!=None and db_object!=None:
#         epidcorrelationtablenamelist=db_object.filter_table_with_eqid()
#         return epidcorrelationtablenamelist
#
# @pytest.mark.parametrize("epidcorrelationtablename",epid_correlation_table_namelist)
# def test_epid_table_exist_or_not(epidcorrelationtablename,db_object, all_db_config):
#     if all_db_config!=None and db_object!=None:
#         filelist=zipfile.dir_file_name(all_db_config)
#         if epidcorrelationtablename !=None:
#             assert epidcorrelationtablename in filelist

# def test_epid_table_exist_or_not(epid_correlation_table,all_db_config):
#     if all_db_config!=None:
#         filelist=zipfile.dir_file_name(all_db_config)
#         if epid_correlation_table !=None:
#             assert epid_correlation_table in filelist


# cachedata=""
# def datacache(cache):
#     global cachedata
#     key = "cache/lastfailed"
#     cachedata = str(cache.get(key, {}))

# @pytest.fixture()
# skip_or_not="True"
# def not_exist_file(func):
#     def not_exist(cache,all_db_config,epid_table_data_nums,epid_correlation_table):
#         global skip_or_not
#         key="cache/lastfailed"
#         cachedata=cache.get(key, {})
#         strcachedata=str(cachedata)
#         # print("this is d",strcachedata)
#         if all_db_config!=None:
#             # print("here is all_db_config",all_db_config)
#             strall_db_config=str(all_db_config)
#             if strall_db_config not in strcachedata:
#                 skip_or_not="False"
#             else:
#                 skip_or_not="True"
#         func(epid_table_data_nums,all_db_config,epid_correlation_table)
#     return not_exist


if __name__=="__main__":
    pytest.main("test_eqid_correlation_data.py::test_epid_table_data_nums -s -x")
    # print(w.result)
    # d=TestCompareExportData()
    # d.test_compare_epid_correlation_data()

