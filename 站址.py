import requests,json,pymysql,time,re,csv,pytesseract
from PIL import Image
from bs4 import BeautifulSoup
headers1={
    "Host": "117.158.221.16:8989",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
HuiHua=requests.Session()
HuiHua.headers.update(headers1)
RiQi=time.strftime("%Y-%m-%d", time.localtime())
try:
    ShuJvKu=pymysql.connect("localhost","root","root","数据同步")
except:
    print("数据库连接失败！请确认数据库地址及账号密码是否正确，或网络是否正常！")
    exit()
YouBiao=ShuJvKu.cursor()
# 验证码识别
def ShiBie(TuPian_URL):
    # 图片除燥
    def ChuZao(TuPian):
        Kuan,Gao=TuPian.size
        for x in range(Kuan):
            TuPian.putpixel((x,0),(255))
            TuPian.putpixel((x,Gao-1),(255))
        for y in range(Gao):
            TuPian.putpixel((0,y),(255))
            TuPian.putpixel((Kuan-1,y),(255))
        for x in range(2,Kuan-1):
            for y in range(2,Gao-1):
                TongJi=0
                for a in range(x-1,x+2):
                    for b in range(y-1,y+2):
                        if TuPian.getpixel((a,b))<=200:
                            TongJi=TongJi+1
                if TongJi<4:
                    TuPian.putpixel((x,y),(255))
                elif TongJi>6:
                    TuPian.putpixel((x,y),(0))
        return TuPian
    TuPian=Image.open(TuPian_URL).convert('L')
    for a in range(3):
        TuPian=ChuZao(TuPian)
    return pytesseract.image_to_string(TuPian,lang="eng")
# 登陆函数
def DengLu():
    # 初始化会话
    HuiHua.get(url="http://117.158.221.16:8989/baf/jsp/uiframe/login.jsp")
    # 验证码处理
    YanZhengMa_URL="http://117.158.221.16:8989/servlet/ValidateCodeServlet"
    YanZhengMa=HuiHua.get(url=YanZhengMa_URL)
    open("验证码.jpg","wb+").write(YanZhengMa.content)
    # 提交登录信息
    TiJiao_URl="http://117.158.221.16:8989/jf/login/checkLogin"
    TiJiao={
        "loginName":"铁塔运维账号",
        "password":"密码",
        "picCode":ShiBie("验证码.jpg"),
        "chkRememberMe":"on",}
    XiangYing=HuiHua.post(url=TiJiao_URl,data=TiJiao)
    ZhuanTaiMa=json.loads(XiangYing.text)['status']
    if ZhuanTaiMa==3:
        print("验证码错误,重试中~")
        DengLu()
    elif ZhuanTaiMa=='-2':
        print("账号或密码错误,请修改后重试~")
        exit()
    elif ZhuanTaiMa=='1':
        print("登录成功！")
# 初始化查询参数
def ChaXun():
    a=HuiHua.get("http://117.158.221.16:8989/business/resMge/siteMge/listSite.xhtml")
    DiZhiYe=BeautifulSoup(a.text,"lxml")
    try:
        ViewState_Zhi=DiZhiYe.find("input",id="javax.faces.ViewState")["value"]
    except:
        print("获取到错误数据，程序将终止！请稍后重试！")
        exit()
    ChaXun_URl="http://117.158.221.16:8989/business/resMge/siteMge/listSite.xhtml"
    HuiHua.headers.update({"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Referer": ChaXun_URl})
    # 初始化查询参数
    CanShu2={
        "AJAXREQUEST":"_viewRoot",
        "queryForm":"queryForm",
        "queryForm:unitHidden":"",
        "queryForm:exportSiteIds":"",
        "queryForm:queryFlag1":"queryFlag1",
        "queryForm:j_id60":"",
        "queryForm:j_id64":"",
        "queryForm:j_id68":"",
        "queryForm:queryDWCompanyId":"",
        "queryForm:queryDWCompanyName":"",
        "queryForm:queryDWPersonId":"",
        "queryForm:queryDWPersonName":"",
        "queryForm:queryTypeHid_hiddenValue":"",
        "queryForm:querystatusSelid_hiddenValue":"1,2,3,6,7,8",
        "queryForm:querystatusSelid":"1",
        "queryForm:querystatusSelid":"2",
        "queryForm:querystatusSelid":"3",
        "queryForm:querystatusSelid":"6",
        "queryForm:querystatusSelid":"7",
        "queryForm:querystatusSelid":"8",
        "queryForm:queryFactoryHid_hiddenValue":"",
        "queryForm:queryFsuStatusHid_hiddenValue":"",
        "queryForm:queryoperatorStationHid_hiddenValue":"",
        "queryForm:queryIsReliefHid_hiddenValue":"",
        "queryForm:subOperatorHid_hiddenValue":"",
        "queryForm:queryCoordWay_hiddenValue":"",
        "queryForm:addapplymajor_hiddenValue":"",
        "queryForm:querySiteSourceHid_hiddenValue":"",
        "queryForm:queryReminderHid_hiddenValue":"",
        "queryForm:queryStaItemHid_hiddenValue":"",
        "queryForm:queryLockFlag_hiddenValue":"",
        "queryForm:queryBuildWays_hiddenValue":"",
        "queryForm:queryComTypes":"",
        "queryForm:queryComTypeNames":"",
        "queryForm:queryIsRent_hiddenValue":"",
        "queryForm:queryCrewVillageId":"",
        "queryForm:hideFlag":"",
        "queryForm:queryCrewVillageName":"",
        "queryForm:j_id130":"",
        "queryForm:countSizeText":"",
        "queryForm:msg":"0",
        "queryForm:currPageObjId":"1",
        "queryForm:pageSizeText":"300",
        "javax.faces.ViewState":ViewState_Zhi,
        "queryForm:j_id145":"queryForm:j_id145",
        "AJAX:EVENTS_COUNT":"1",
        }
    CanShu1={
        "AJAXREQUEST":"_viewRoot",
        "queryForm":"queryForm",
        "queryForm:unitHidden":"",
        "queryForm:exportSiteIds":"",
        "queryForm:queryFlag1":"queryFlag1",
        "queryForm:j_id60":"",
        "queryForm:j_id64":"",
        "queryForm:j_id68":"",
        "queryForm:queryDWCompanyId":"",
        "queryForm:queryDWCompanyName":"",
        "queryForm:queryDWPersonId":"",
        "queryForm:queryDWPersonName":"",
        "queryForm:queryTypeHid_hiddenValue":"",
        "queryForm:querystatusSelid_hiddenValue":"1,2,3,6,7,8",
        "queryForm:querystatusSelid":"1",
        "queryForm:querystatusSelid":"2",
        "queryForm:querystatusSelid":"3",
        "queryForm:querystatusSelid":"6",
        "queryForm:querystatusSelid":"7",
        "queryForm:querystatusSelid":"8",
        "queryForm:queryFactoryHid_hiddenValue":"",
        "queryForm:queryFsuStatusHid_hiddenValue":"",
        "queryForm:queryoperatorStationHid_hiddenValue":"",
        "queryForm:queryIsReliefHid_hiddenValue":"",
        "queryForm:subOperatorHid_hiddenValue":"",
        "queryForm:queryCoordWay_hiddenValue":"",
        "queryForm:addapplymajor_hiddenValue":"",
        "queryForm:querySiteSourceHid_hiddenValue":"",
        "queryForm:queryReminderHid_hiddenValue":"",
        "queryForm:queryStaItemHid_hiddenValue":"",
        "queryForm:queryLockFlag_hiddenValue":"",
        "queryForm:queryBuildWays_hiddenValue":"",
        "queryForm:queryComTypes":"",
        "queryForm:queryComTypeNames":"",
        "queryForm:queryIsRent_hiddenValue":"",
        "queryForm:queryCrewVillageId":"",
        "queryForm:hideFlag":"",
        "queryForm:queryCrewVillageName":"",
        "queryForm:j_id130":"",
        "queryForm:countSizeText":"",
        "queryForm:msg":"0",
        "queryForm:currPageObjId":"1",
        "queryForm:pageSizeText":"300",
        "javax.faces.ViewState":ViewState_Zhi,
        "queryForm:siteQueryId":"queryForm:siteQueryId",}
    HuiHua.post(ChaXun_URl,data=CanShu1)
    try:
        ChaXun=HuiHua.post(ChaXun_URl,data=CanShu2)
        if ChaXun.status_code!=200:
            raise NameError("响应异常！")
    except:
        print("数据获取失败！重试中~")
        time.sleep(2)
        try:
            ChaXun=HuiHua.post(ChaXun_URl,data=CanShu2)
            if ChaXun.status_code!=200:
                raise NameError("响应异常！")
        except:
            print("数据获取失败！重试中~")
            time.sleep(2)
            try:
                ChaXun=HuiHua.post(ChaXun_URl,data=CanShu2)
                if ChaXun.status_code!=200:
                    raise NameError("响应异常！")
            except:
                print("数据获取失败，程序将终止！请稍后重试！")
                exit()
    # open("a1.html","w+",encoding="utf-8").write(ChaXun.text)
    # exit()
    # 处理返回数据
    print("正在处理第 1 页数据~")
    ShuJv=BeautifulSoup(ChaXun.text,"lxml")
    try:
        LieBiao=ShuJv.find_all("tr",class_="rich-table-row")
    except:
        print("获取到错误数据，程序将终止！请稍后重试！")
        exit()
    ShuJvJi=[]
    for a in LieBiao:
        a=a.find_all("center")
        # 空数据处理
        b=[]
        for c in a:
            if c.get_text()!="":
                b.append(c.get_text())
            else:
                b.append(None)
        b.append(RiQi)
        ShuJvJi.append(b[2:])
    YouBiao.execute("BEGIN")
    YouBiao.executemany("INSERT INTO 站址 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",ShuJvJi)
    YouBiao.execute("COMMIT")
    # 初始化查询参数
    YeShu=ShuJv.find("td",class_="rich-datascr-info").get_text()
    YeShu=int(re.findall("共(\d+)页",YeShu)[0])
    print("本次获取共计 "+str(YeShu)+" 页数据~")
    HuiHua.headers.update({"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Referer": ChaXun_URl})
    selStatusHid_Ji=ShuJv.find_all("input",attrs={'name':"selStatusHid"})
    selStatusHid_Ji=list(map(lambda a:a["value"],selStatusHid_Ji))
    selServiceStatusHid_Ji=ShuJv.find_all("input",attrs={'name':"selServiceStatusHid"})
    selServiceStatusHid_Ji=list(map(lambda a:a["value"],selServiceStatusHid_Ji))
    maintenanceperson_Ji=ShuJv.find_all("input",attrs={'name':"maintenanceperson"})
    maintenanceperson_Ji=list(map(lambda a:a["value"],maintenanceperson_Ji))
    CanShu={}
    for a in range(300):
        b={
            "selStatusHid":selStatusHid_Ji[a],
            "selServiceStatusHid":selServiceStatusHid_Ji[a],
            "maintenanceperson":maintenanceperson_Ji[a]}
        CanShu.update(b)
    HuoQv(YeShu,ChaXun_URl,ViewState_Zhi,CanShu)
# 获取数据并入库
def HuoQv(YeShu,ChaXun_URl,ViewState_Zhi,CanShu2):
    CanShu1={
    "AJAXREQUEST":"_viewRoot",
    "listForm":"listForm",
    "autoScroll":"",
    "javax.faces.ViewState":ViewState_Zhi,
    "ajaxSingle":"listForm:list:itemScroller",
    "AJAX:EVENTS_COUNT":"1",}
    for Ye in range(2,YeShu+1):
        CanShu={}
        CanShu.update(CanShu1);CanShu.update(CanShu2)
        CanShu["listForm:list:itemScroller"]=Ye
        try:
            ChaXun=HuiHua.post(ChaXun_URl,data=CanShu)
            if ChaXun.status_code!=200:
                raise NameError("响应异常！")
        except:
            print("数据获取失败！重试中~")
            time.sleep(2)
            try:
                ChaXun=HuiHua.post(ChaXun_URl,data=CanShu)
                if ChaXun.status_code!=200:
                    raise NameError("响应异常！")
            except:
                print("数据获取失败！重试中~")
                time.sleep(2)
                try:
                    ChaXun=HuiHua.post(ChaXun_URl,data=CanShu)
                    if ChaXun.status_code!=200:
                        raise NameError("响应异常！")
                except:
                    print("数据获取失败，程序将终止！请稍后重试！")
                    exit()
            # open("a"+str(Ye)+".html","w+",encoding="utf-8").write(ChaXun.text)
            # continue
        print("正在处理第 "+str(Ye)+" 页数据~")
        ShuJv=BeautifulSoup(ChaXun.text,"lxml")
        try:
            LieBiao=ShuJv.find_all("tr",class_="rich-table-row")
        except:
            print("获取到错误数据！")
            a=input("若想停止运行请输入(小写) t，输入其他则继续运行>")
            if a=="t":
                exit()
        # 构建分页参数
        selStatusHid_Ji=ShuJv.find_all("input",attrs={'name':"selStatusHid"})
        selStatusHid_Ji=list(map(lambda a:a["value"],selStatusHid_Ji))
        selServiceStatusHid_Ji=ShuJv.find_all("input",attrs={'name':"selServiceStatusHid"})
        selServiceStatusHid_Ji=list(map(lambda a:a["value"],selServiceStatusHid_Ji))
        maintenanceperson_Ji=ShuJv.find_all("input",attrs={'name':"maintenanceperson"})
        maintenanceperson_Ji=list(map(lambda a:a["value"],maintenanceperson_Ji))
        CanShu2={}
        for a in range(len(maintenanceperson_Ji)):
            b={
                "selStatusHid":selStatusHid_Ji[a],
                "selServiceStatusHid":selServiceStatusHid_Ji[a],
                "maintenanceperson":maintenanceperson_Ji[a]}
            CanShu2.update(b)
        # 结构化数据并入库
        def JieGouHua(JiLu):
            JiLu=JiLu.find_all("center")
            b=[]
            for c in JiLu:
                if c.get_text()!="":
                    b.append(c.get_text())
                else:
                    b.append(None)
            b.append(RiQi)
            return (b[2:])
        ShuJvJi=list(map(JieGouHua,LieBiao))
        YouBiao.execute("BEGIN;")
        try:
            YouBiao.executemany("INSERT INTO 站址 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",ShuJvJi)
        except:
            for a in ShuJvJi:
                # try:
                YouBiao.execute("INSERT INTO 站址 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);" % tuple(a))
                # except:
                #     with open('异常数据.csv', 'a', newline='') as WenJian:
                #         Xie=csv.writer(WenJian)
                #         Xie.writerow(a)
        YouBiao.execute("COMMIT;")
while 1:
    # try:
    a1=time.time()
    DengLu()
    ChaXun()
    YouBiao.close()
    ShuJvKu.close()
    print(RiQi+" 日数据处理完成！")
    a2=time.time()-a1
    time.sleep(86400-a2)
    # except:
    #     pass
    RiQi=time.strftime("%Y-%m-%d", time.localtime())
    try:
        ShuJvKu=pymysql.connect("localhost","root","root","数据同步")
    except:
        print("数据库连接失败！重试中~")
        try:
            ShuJvKu=pymysql.connect("localhost","root","root","数据同步")
        except:
            print("数据库连接失败！重试中~")
            try:
                ShuJvKu=pymysql.connect("localhost","root","root","数据同步")
            except:
                print("数据库连接失败！请确认数据库地址及账号密码是否正确，或网络是否正常！程序将退出！")
                exit()
    YouBiao=ShuJvKu.cursor()