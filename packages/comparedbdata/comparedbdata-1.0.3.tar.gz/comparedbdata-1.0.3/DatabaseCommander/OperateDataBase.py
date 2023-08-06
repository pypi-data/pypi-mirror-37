from DatabaseCommander.ConnectDB import ConnectDataBase,DBConnectInfo
from PublicMethod.OperateIniFile import OperateIni


class QueryExportData():
    '''导出数据操作类'''
    def __init__(self,SectionName):
        self.DataBase=DBConnectInfo(SectionName)
        self.Connect =self.DataBase.connect
        # self.DataBaseName=self.DataBase.get_value('databasename')
        operateini=OperateIni("DataBaseInfo.ini")
        self.epid=list(operateini.get_section_data("epid").values())[0]

    def __init_client_cursor_encode(self,connect=None):
        '''初始化数据库游标'''
        if connect==None:
            curs = self.Connect.cursor()
        else:
            curs=connect.cursor()
        curs.execute("SET NAMES utf8")
        self.Connect.commit()
        return curs

    def query_condition_date(self, keyname:str, tablename:str):
        '''根据企业id查询‘关键字’数据
        result：返回列表嵌套的字典'''
        sqlwithepid='select %s from %s where epid=%s' %( keyname,tablename,self.epid)
        sqlwithenterpriseId='select %s from %s where enterpriseId=%s' %( keyname,tablename,self.epid)
        cursor=self.__init_client_cursor_encode()
        try:
            cursor.execute(sqlwithepid)
        except:
            cursor.execute(sqlwithenterpriseId)
        result=cursor.fetchall()
        # resultmap=map(lambda tablelist:list(tablelist.values())[0],result)
        cursor.close()
        return result
        # return resultmap

    def query_datanum_depend_epid(self,tablename:str):
        '''根据企业id查询数据'''
        sql='select count(*) from %s where epid=%s' %(tablename,self.epid)
        cursor=self.__init_client_cursor_encode()
        cursor.execute(sql)
        result=cursor.fetchall()
        cursor.close()
        return result

    def query_table_data_nums(self, tablename):
        '''根据tablename查询数据数量'''
        sql='select count(*) from %s' %(tablename)
        cursor=self.__init_client_cursor_encode()
        cursor.execute(sql)
        result=cursor.fetchall()
        cursor.close()
        if result != None:
            data_nums= int(result[0]['count(*)'])
            return data_nums

    def filter_table_with_eqid(self,):
        '''返回数据库下包含epid字段且有数据的表名称'''
        sql = "SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS " \
              "where TABLE_SCHEMA ='%s' and (COLUMN_NAME='epid' OR " \
              "COLUMN_NAME='share_epid' OR COLUMN_NAME='enterpirseid')" \
              % (self.DataBase.mysqldbname)
        cursor = self.__init_client_cursor_encode()
        cursor.execute(sql)
        cursor.close()
        eqidtables = map(lambda tablelist: list(tablelist.values())[0], cursor.fetchall())
        eqidtablelist=filter(lambda tablename:self.query_table_data_nums(tablename),eqidtables)
        return eqidtablelist


    def query_data_rownum(self, tablename:str, dbname:str, conditionlist):
        """ 查询数据的数量
        dbname : 需要夸库查询的数据库名称
        conditionlist : 查询条件list
        """
        # conditionlist=self.query_condition_date(tablename=tablename,
        #                                         keyname=keyname)
        resultdict=dict()
        db=DBConnectInfo(dbname)
        connect=db.connect
        def query_submeter():
            '''辅助函数:查询数据库下所有表名'''
            sql="SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS " \
                "where TABLE_SCHEMA ='%s'" %(db.mysqldbname)
            cursor=self.__init_client_cursor_encode(connect)
            cursor.execute(sql)
            tablenamelist=map(lambda tablelist:list(tablelist.values())[0],cursor.fetchall())
            return  tablenamelist
        alltablename=query_submeter()
        #过滤分表名称
        targettablenamelist=filter(lambda tablist:tablist.startswith(tablename),alltablename)
        for targettablename in targettablenamelist:
            totalrowsnum = 0
            for condition in conditionlist:
                for key,value in condition.items():
                    sql="select count(*) from %s where %s='%s'" %(targettablename,key,value)
                    cursor=self.__init_client_cursor_encode(connect)
                    cursor.execute(sql)
                    result=cursor.fetchone()
                    if result != None:
                        totalrowsnum += int(result['count(*)'])
                    cursor.close()
            if totalrowsnum!=0:
                resultdict[targettablename]=totalrowsnum
        return resultdict

class AbstractDataOperater():
    '''数据库操作抽象类'''
    def __init__(self,SectionName):
        self.DataBase=ConnectDataBase(SectionName)
        self.Connect =self.DataBase.connect_SQL_database()
        self.DataBaseName=self.DataBase.get_value('databasename')

    def init_client_cursor_encode(self):
        '''初始化数据库游标'''
        curs = self.Connect.cursor()
        curs.execute("SET NAMES utf8")
        self.Connect.commit()
        return curs

class ImportDataOperater(AbstractDataOperater):
    '''数据库查询操作类
    SectionName:数据库配置文件中，对应想链接的数据库配置'''
    def __init__(self,SectionName,NumPerPage=100000):
        super().__init__(SectionName)
        self.NumPerPage = NumPerPage

    def get_all_table_name(self):
        '''获取连接的数据库下所有表的名称'''
        sql="SHOW TABLES"
        Cursor=self.init_client_cursor_encode()
        results=[]
        TableNumber=Cursor.execute(sql)
        TableNames=Cursor.fetchall()
        Cursor.close()
        TableKey='Tables_in_{0}'.format(self.DataBaseName)
        for i in range(TableNumber):
            results.append(TableNames[i][TableKey])
        return results

    def __create_pagination_query_sql(self, TableName, CurrentPageIndex):
        '''创建获取当前页后面数据的SQL语句'''
        StartIndex = self.__calculate_start_index(CurrentPageIndex)
        Sql = r'select * from %s total_table limit %s,%s' % (TableName, StartIndex, self.NumPerPage)
        return Sql

    def __create_query_column_names(self,TableName):
        '''查询指定表单主键'''
        # Sql=r"select COLUMN_NAME from information_schema.COLUMNS where table_name = '{0}'" .format(TableName)
        Sql='''SELECT c.COLUMN_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS t,information_schema.TABLES AS ts,information_schema.KEY_COLUMN_USAGE AS c 
        WHERE t.TABLE_NAME = ts.TABLE_NAME AND ts.TABLE_NAME  = c.TABLE_NAME AND t.TABLE_SCHEMA = "{}" AND t.CONSTRAINT_TYPE = 'PRIMARY KEY' 
        AND t.TABLE_NAME='{}';'''.format(self.DataBaseName,TableName)
        return Sql

    # def __create_query_line_sql(self,TableName,*Values):
    #     "创建查询表单单条数据语句"
    #     colunmnames=self.query_each_page(TableName,0,3)
    #     Sql=r"select * from {0} where {}={}".format(TableName)

    def query_each_page(self, TableName, CurrentPageIndex):
        '''返回每一页查询的数据,1为执行分页查询，2为查询表单单条数据，其他为查询指定表单colunm names'''
        Query_Sql = self.__create_pagination_query_sql(TableName, CurrentPageIndex)
        Cursor = self.init_client_cursor_encode()
        Cursor.execute(Query_Sql)
        result = Cursor.fetchall()
        Cursor.close()
        listresult=[]
        for dict in result:
            for key,value in dict.items():      #转换返回的datetime格式
                if isinstance(value,bytes):
                    dict[key]=int(str(value).lstrip(r"b'\x").rstrip("'"),16)
                else:
                    dict[key] = str(value)
            listresult.append(list(dict.values()))
        return listresult

    def __calculate_start_index(self, CurrentPageIndex):
        '''计算当前开始的行数'''
        startIndex = CurrentPageIndex * self.NumPerPage
        return startIndex

    def calculate_total_rows_num(self, TableName):
        ''''' 计算总行数 '''
        Sql = r'select count(*) from %s total_table' % TableName
        Cursor = self.init_client_cursor_encode()
        Cursor.execute(Sql)
        Result = Cursor.fetchone()
        Cursor.close()
        if Result != None:
            TotalRowsNum = int(Result['count(*)'])
            return TotalRowsNum

    def calculate_total_pages(self, TableName):
        ''''' 计算总页数 '''
        TotalRowsNum = self.calculate_total_rows_num(TableName)
        TotalPages = 0
        if (TotalRowsNum % self.NumPerPage) == 0:
            TotalPages = TotalRowsNum / self.NumPerPage
        else:
            TotalPages = (TotalRowsNum//self.NumPerPage) + 1
        return int(TotalPages)


if __name__=='__main__':
    # base=OperateDataBase("OriginalDataBase")
    # print(base.get_all_table_name())
    # data=base.get_table_data("15","20")
    # print(data)
    # lenth=base.get_table_data_number()
    # print(lenth)

    # for num in base.nested_list_to_list(data):
    #     print(num)
    # r=base.nested_list_to_list(data)
    # r.next(3)
    # r.send(data)

    # pag = ImportDataOperater("TargetDataBase")
    # sql ='bimtimedim_gj0001'
    # total_page=pag.calculate_total_pages(sql)
    # for currentpage in range(total_page):
    #     p=pag.query_each_page(sql, currentpage)
    #     print(p)
    # print(pag.get_all_table_name())
    # print(pag.query_each_page(sql,0,3))
    # pag.create_query_line_sql("",params)
    # for ret in pag.query_for_list(sql):
    #     print (ret)
    sql=QueryExportData("lubancenterbuilder")
    builder_project='builder_project'
    data=sql.query_condition_date("ppid",builder_project)
    result=sql.query_data_rownum("azcg_aggr", "lubanbe", data)
    # print(result)
    # result=sql.query_datanum_depend_epid("builder_client_user")
    # print(result)
    # result=sql.filter_table_with_eqid()
    # print(list(result))
    # print(len(list(result)))

    # print(sql.query_table_data_nums("builder_proj_curoperate"))