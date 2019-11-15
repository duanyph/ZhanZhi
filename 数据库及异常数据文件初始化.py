# coding=utf-8
import pymysql,csv
ShuJvKu=pymysql.connect("localhost","root","root","数据同步")
YouBiao=ShuJvKu.cursor()
ChongJian_SQL="""
    CREATE TABLE 站址(
        站址编码 VARCHAR(25),
        名称 VARCHAR(50),
        运维ID VARCHAR(25),
        站址来源 CHAR(20),
        维护状态 CHAR(10),
        FSU状态 CHAR(10),
        注册状态 VARCHAR(10),
        站址细分类型 CHAR(15),
        点位编码 VARCHAR(30),
        发电等待时长 VARCHAR(10),
        一次下电时长 INT,
        所属管理区域 CHAR(15),
        区域经理 CHAR(15),
        区域经理联系电话 VARCHAR(100),
        所属省 CHAR(25),
        所属市 CHAR(25),
        所属区 CHAR(25),
        所属乡镇 CHAR(25),
        供应商名称 VARCHAR(50),
        机房维护人员 VARCHAR(200),
        机房维护人员联系电话 VARCHAR(100),
        铁塔维护人员 VARCHAR(200),
        铁塔维护人员联系电话 VARCHAR(100),
        所属运营商 CHAR(25),
        移动维护人员 VARCHAR(50),
        联通维护人员 VARCHAR(50),
        电信维护人员 VARCHAR(50),
        是否有效 CHAR(5),
        经纬度方式 CHAR(10),
        备注 VARCHAR(100),
        录入日期 DATE);"""
        # UNIQUE(站址名称,站址运维ID,站址编码,FSU运维ID,告警发生时间,告警清除时间,设备告警开始时间,设备告警结束时间));
try:
    YouBiao.execute(ChongJian_SQL)
except:
    pass
ShuJvKu.commit()
ShuJvKu.close()
# 初始化异常数据文件
with open('异常数据.csv','w',encoding='gbk',newline='') as WenJian:
    Xie=csv.writer(WenJian)
    Xie.writerow(['站址编码','名称','运维ID','站址来源','维护状态','FSU状态','注册状态','站址细分类型','点位编码','发电等待时长','一次下电时长','所属管理区域','区域经理','区域经理联系电话','所属省','所属市','所属区','所属乡镇','供应商名称','机房维护人员','机房维护人员联系电话','铁塔维护人员','铁塔维护人员联系电话','所属运营商','移动维护人员','联通维护人员','电信维护人员','是否有效','经纬度方式','备注','录入日期'])