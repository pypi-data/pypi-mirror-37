import pymysql
import pymongo
from DatabaseCommander.DataBaseUserInfo import DataBaseInfoManager
from PublicMethod.OperateIniFile import OperateIni


class DBConnectInfo():
    CHARSET = "utf8"

    def __init__(self, section):
        self.operateini = OperateIni("all-luban-subsystem-db-config.ini")
        self.get_mysql_connect_common_info()
        self.__get_section_DB_name(section)
        if self.mysqldbname:
            self.connect = self.__connect_mysql_service()
        if self.mongodbname:
            self.mongoconnect = self.__connect_mongo_service()

    def get_mysql_connect_common_info(self):
        commondata = self.operateini.get_section_data("common-connection-info")
        for key, value in commondata.items():
            if key == "mysql.db.host":
                mysqlhostandport = value.split(":")
                self.mysqlhost = mysqlhostandport[0]
                self.mysqlport = mysqlhostandport[1]
            elif key == "mysql.db.username":
                self.username = value
            elif key == "mysql.db.password":
                self.password = value
            elif key == "mongo.db.host":
                mongohostandport = value.split(":")
                self.mongohost = mongohostandport[0]
                self.mongoport = mongohostandport[1]
            elif key == "mongo.db.username":
                self.mongousername = value
            elif key == "mongo.db.password":
                self.mongopassword = value
            else:
                raise KeyError("key无效")

    def __get_section_DB_name(self, section: str):
        '''获取指定节点下数据库名称'''
        mysqlkey = "mysql.database"
        mongokey = "mongo.database"
        self.mysqldbname = None
        self.mongodbname = None
        dbnamedict = self.operateini.get_section_data(section)
        try:
            self.mysqldbname = dbnamedict[mysqlkey]
            self.mongodbname = dbnamedict[mongokey]
        except KeyError as e:
            print("No This db:", e)

    def __connect_mysql_service(self):
        Connect = pymysql.Connect(host=self.mysqlhost,
                                  port=int(self.mysqlport),
                                  user=self.username,
                                  password=self.password,
                                  db=self.mysqldbname,
                                  charset=self.CHARSET,
                                  cursorclass=pymysql.cursors.DictCursor)
        return Connect

    def __connect_mongo_service(self):
        mongo_client = pymongo.MongoClient(host=self.mongohost,
                                           port=int(self.mongoport),
                                           username=self.mongousername,
                                           password=self.mongopassword
                                           )
        return mongo_client

    def __del__(self):
        if self.mysqldbname:
            self.connect.close()
        if self.mongodbname:
            self.mongoconnect.close()


class ConnectDataBase(DataBaseInfoManager):
    def __init__(self,SectionName):
        super().__init__(SectionName)

    def connect_SQL_database(self):
        '''建立与数据库的连接'''
        Host = self.get_value('host')
        Port = self.get_value('port')
        User = self.get_value('user')
        PassWord = self.get_value('password')
        DataBaseName = self.get_value('databasename')
        Charset=self.get_value('charset')
        Connect = pymysql.Connect(host=Host, port=int(Port), user=User, password=PassWord,
                                  db=DataBaseName,charset=Charset,cursorclass = pymysql.cursors.DictCursor)
        return Connect


if __name__=="__main__":
    # Info=ConnectDataBase("TargetDataBase")
    # print(Info.connect_SQL_database())
    test=DBConnectInfo("lubanbe")
    # print(test.mongodbname)
    print(test.mongoconnect)
    # print(test.mongopassword)
    # print(test.mongohost)
    # print(test.mongoport)
    # print(test.mongousername)
    # print(test.connect)
    # print(test.mysqlhost)
    # print(test.mysqlport)
    # print(test.username)
    # print(test.password)
    # print(test.mysqldbname)
    # test.__get_section_DB_name("lubanbimco")
    # print(test.lubanbimcomongo)
    # test.get_DB_connect_info("lubanbimco")
