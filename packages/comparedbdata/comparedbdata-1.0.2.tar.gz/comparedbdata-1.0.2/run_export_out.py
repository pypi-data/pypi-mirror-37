import argparse
from PublicMethod.OperateIniFile import OperateIni
from collections import namedtuple
import pytest


COMMONCONNECTIONINFO="common-connection-info"
EPID="epid"
LUBANEPID="90001000"

DbCongifClass=namedtuple("dbconfigtuple",['host','port','username','password'])
DbCongifClass.__new__.__defaults__=('192.168.3.26',"3306","root","luban123docker")

def config_command():
    parser=argparse.ArgumentParser()
    parser.add_argument('-sh',"--mysqlhost",type=str,help='设置mysql数据库地址',
                        default='192.168.3.26',)
    parser.add_argument('-sp','--mysqlport',type=str,help='设置mysql数据库端口号',
                        default='3306')
    parser.add_argument('-su','--mysqlusername',type=str,help='设置mysql数据库用户名',
                        default='root')
    parser.add_argument('-spw','--mysqlpassword',type=str,help='设置mysql数据库密码',
                        default='luban123docker')
    args=parser.parse_args()
    dbconfiginfo=DbCongifClass(args.mysqlhost,args.mysqlport,args.mysqlusername,args.mysqlpassword)
    return dbconfiginfo

def set_db_info(dbconfig,epid=LUBANEPID):
    alldbconfig=OperateIni("all-luban-subsystem-db-config.ini")
    dictalldbconfig=dict(dbconfig._asdict())
    # nametuple不支持带“.”的名称所以在这里加上
    new_dict={"mysql.db."+key:value for key,value in dictalldbconfig.items()}
    for key,value in new_dict.items():
        if key=='mysql.db.host':
            port=dictalldbconfig.get('port')
            alldbconfig.modify_section_data(COMMONCONNECTIONINFO,value+':'+port,key)
        elif key=='mysql.db.port':
            continue
        else:
            alldbconfig.modify_section_data(COMMONCONNECTIONINFO,value,key)
    if epid!=LUBANEPID and epid!="":
        epidconfig=OperateIni("DataBaseInfo.ini")
        epidconfig.modify_section_data(EPID,epid,EPID)

def compare_table_or_data(testcommand:str):
    '''运行哪个测试用例'''
    inttestcommand=int(testcommand)
    if inttestcommand==1:
        pytest.main(['-m=tableexistornot', '-v','testcase'])
    elif inttestcommand==2:
        pytest.main(['-m=tablenums','-v','--html=./report.html','-n=auto',"testcase"])
    elif inttestcommand==3:
        pytest.main("-v -n auto --html=./report.html testcase/test_common_data.py")
    elif inttestcommand==4:
        pytest.main("-v -n auto --html=./report.html testcase/test_eqid_correlation_data.py")
    elif inttestcommand==5:
        pytest.main("-v -n auto --html=./report.html testcase/test_white_config_data.py")
    elif inttestcommand==6:
        pytest.main("-v -n auto --html=./report.html testcase")
    else:
        exit()

def run_test():
    while True:
        runornot=input("输入:1.开始运行对比工具 2.退出程序\n"
                       "请输入你的选择：")
        print("************************************")
        if runornot=="1":
            run_test_controler()
        else:
            break

def run_test_controler():
    print("默认企业id为90001000（即鲁班软件研发中心），数据库地址为正式外网地址，"
          "如使用默认值直接回车即可，运行完成后会在当前运行目录生成测试报告")
    host=input("请输入数据库地址：")
    port=input("请输入数据库端口号：")
    username=input("请输入数据库用户名：")
    password=input("请输入数据库密码：")
    epid=input("请输入企业id：")
    print("************************************")
    dbconfiginfo = DbCongifClass(host, port, username, password) \
        if host != "" or port != "" or username != "" or password != "" else DbCongifClass()
    set_db_info(dbconfiginfo,epid)
    while True:
        command=input("请输入需要执行的pytest命令：\n"
                      " 1：对比数据表是否存在\n"
                      " 2：对比表中数据是否正确\n"
                      " 3：对比common配置中的表及数据\n"
                      " 4：对比epid配置中的表及数据\n"
                      " 5：对比white配置中的表及数据\n"
                      " 6：执行所有用例\n"
                      " 7：退出程序\n"
                      "请输入你的选择：")
        compare_table_or_data(command)


if __name__ == '__main__':
    # set_db_info()
    # pytest.main("testcase/test_common_data.py::test_common_table_exist_or_not -v -x")
    # compare_table_or_data("test_common_data.py::test_common_table_nums -x -v")
    try:
        run_test()
    except:
        print("************************************\n"
            '按任意键关闭窗口')
        input()