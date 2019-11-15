import pymysql,json,pandas
PeiZhi=json.load(open('筛选配置.json', 'r'))
try:
    ShuJvKu=pymysql.connect(host="127.0.0.1",port=2221,user="root",passwd="root",db="数据同步")
except:
    input("数据库连接失败，请稍后重试！请按任意键关闭~")
    exit()
SQL_YuJv="SELECT * FROM 站址 WHERE "
for a,b in PeiZhi.items():
    if b!=[""] and b!=[]:
        SQL_YuJv=SQL_YuJv+"("
        for c in b:
            if c!="":
                if c[0] not in "<>=":
                    SQL_YuJv=SQL_YuJv+a+"='"+c+"' or "
                else:
                    SQL_YuJv=SQL_YuJv+a+c+" and "
        if SQL_YuJv[-3]=="o":
            SQL_YuJv=SQL_YuJv[:-4]+") and "
        elif SQL_YuJv[-3]=="n":
            SQL_YuJv=SQL_YuJv[:-5]+") and "
SQL_YuJv=SQL_YuJv[:-5]
# YouBiao=ShuJvKu.cursor()
# YouBiao.execute(SQL_YuJv)
# print(YouBiao.fetchone())
ShuJv=pandas.read_sql(SQL_YuJv,ShuJvKu)
ShuJv.to_excel("导出.xlsx",index=False)