from selenium import webdriver
import pandas as pd 
import sys 
import time
from sqlalchemy import create_engine,types
import re 
from bs4 import BeautifulSoup
from queue import Queue 
from threading import Thread
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests 
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from threading import  Semaphore 
from lmf.dbv2 import db_write



class web:

    def __init__(self):
        self.add_ip()
        self.url="http://www.jy.whzbtb.com/V2PRTS/TendererNoticeInfoListInit.do"
        self.result_q=Queue()
        self.tmp_q=Queue()
        self.ip_q=Queue()
        self.__init_tmp_q(10)
        self.sema=Semaphore(1)
        self.__init_localhost_q()

    def add_ip(self):

        r = requests.get("http://www.trackip.net/")
        txt = r.text
        ip = txt[txt.find('title')+6:txt.find('/title')-1]

        
        i=3
        while i>0:
            x="""http://http.zhiliandaili.cn/Users-whiteIpListNew.html?appid=2605&appkey=a95fd11b1e7f17d7dfe19969222e95b7"""
            r=requests.get(x).json()
            if "data" in r.keys():ips=r["data"]
            else:
                time.sleep(1)
                i-=1
        if ips==None:

            return False
        if ip in ips:
            print("%s已经在白名单中"%ip)
            return True
        i=3
        while i>0:
            x="""http://http.zhiliandaili.cn/Users-whiteIpAddNew.html?appid=2605&appkey=a95fd11b1e7f17d7dfe19969222e95b7&whiteip=%s&index=5"""%ip
            r=requests.get(x).json()
            if "繁忙" not in r["msg"]:
                break
            i-=1
        print("添加ip%s"%ip)

    def get_ip(self):
        self.sema.acquire()
        url="""http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=101&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson="""
    
        r=requests.get(url)
        time.sleep(1)
        self.ip_q.put(r.text)
        self.sema.release()
        return r.text 
    def __init_localhost_q(self,num=2):
        self.localhost_q=Queue()
        for i in range(num):self.localhost_q.put(i)

    def __init_total(self,f2):
        """获取需要爬取的页面总量，先用本地ip爬三次，若失败代理ip爬三次"""
        num=3
        m=3
        while num>0:
            try:
                chrome_option=webdriver.ChromeOptions()
                driver=webdriver.Chrome(chrome_options=chrome_option)
                driver.minimize_window()
                driver.get(self.url)
                self.total=f2(driver)
                print("用本地ip获取总量,全局共%d 页面"%self.total)
                return "sccess"
            except Exception as e:
                traceback.print_exc()
                driver.quit()
                num-=1
                print("用本地ip获取总量,第%d失败"%(3-num))
        while m>0:
            try:
                chrome_option=webdriver.ChromeOptions()
                ip=self.get_ip()
                # ip="1.28.0.90:20455"
                print("使用代理ip %s"%ip)
                chrome_option.add_argument("--proxy-server=http://%s"%(ip))
                driver=webdriver.Chrome(chrome_options=chrome_option)
                driver.minimize_window()
                driver.get(self.url)
                self.total=f2(driver)
                print("全局共%d 页面"%self.total)
                return "sccess"
            except Exception as e:
                traceback.print_exc()
                driver.quit()
                m-=1
                print("用本地ip获取总量,第%d失败"%(3-m))
        return "failed"


    def __init_tmp_q(self,total):
        self.tmp_q.queue.clear()
        for i in range(total):
            self.tmp_q.put(i+1)

    def __read_thread(self,f):
        url=self.url
        if self.localhost_q.empty():
            
            chrome_option=webdriver.ChromeOptions()
            ip=self.get_ip()
            #ip="1.28.0.90:20455"
            print("本次ip %s"%ip)
            if re.match("[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{1,5}",ip) is None:
                print("ip不合法")
                return False
            chrome_option.add_argument("--proxy-server=http://%s"%(ip))
            try:
                driver=webdriver.Chrome(chrome_options=chrome_option)
                driver.minimize_window()
                driver.set_page_load_timeout(20)
                driver.get(url)
                

            except Exception as e:
                traceback.print_exc()

                driver.quit()
                return False
        else:
            try:
                print("使用本机ip")
                self.localhost_q.get()
                driver=webdriver.Chrome()
                driver.minimize_window()
                driver.set_page_load_timeout(20)
                driver.get(url)
            except Exception as e:
                traceback.print_exc()

                driver.quit()
                return False


        while not self.tmp_q.empty():
             try:
                x=self.tmp_q.get(block=False)
             except:
                traceback.print_exc()
                continue
             if x is None:continue
             try:
                df=f(driver,x)
                self.result_q.put(df)

             except Exception as e:
                traceback.print_exc()
                print("第 %d 页面异常"%x)
                self.tmp_q.put(x)
                driver.quit()
                return False
        driver.quit()
        print("线程正常退出")
        return True 

    def read_thread(self,f):
        num=5
        flag=self.__read_thread(f)
        while  not flag and  num>0:
            num-=1
            print("切换ip,本线程第%d次"%(5-num))
            print("已经消耗ip %d 个"%self.ip_q.qsize())
            flag=self.__read_thread(f)
            
    def read_threads(self,f,num=10,total=100):
        bg=time.time()
        ths=[]
        dfs=[]
        
        if total<=5:num=1
        if num/total>1:num=int(total/5)+1 if int(total/5)+1 <4 else num

        print("开始爬%s,本次共 %d 个页面,共%d 个线程"%(self.url,total,num))
        self.result_q.queue.clear()
        self.__init_tmp_q(total)
        for _ in range(num):
            t=Thread(target=self.read_thread,args=(f,))
            ths.append(t)
        for t in ths:
            t.start()
        for t in ths:
            t.join()
        self.__init_localhost_q()
        left_page=self.tmp_q.qsize()
        print("剩余 %d页"%(left_page))
        if left_page>0:
            self.read_thread(f)
            left_page=self.tmp_q.qsize()
            print("剩余 %d页"%(left_page))
        ed=time.time()
        cost=ed-bg
        if cost<100:
            print("耗时%d 秒"%cost)
        else:
            print("耗时%.4f 分"%(cost/60))
        


    def getdf_from_result(self):
        dfs=list(self.result_q.queue)
        df=pd.concat(dfs,ignore_index=False)
        return df 

    def getdf(self,url,f1,f2,total,num):
        self.url=url
        self.__init_total(f2)
        self.__init_tmp_q(self.total)
        if total is None:
            total=self.total
        elif total>self.total:
             total=self.total

        if num is None:num=10

        self.read_threads(f=f1,num=num,total=total)
        df=self.getdf_from_result()
        return df 

    def write(self,**krg):
        url=krg["url"]
        f1=krg["f1"]
        f2=krg["f2"]
        tb=krg["tb"]
        col=krg["col"]
        if "total" not in krg.keys():
            total=None
        else:
            total=krg["total"]

        if "num" not in krg.keys():
            num=None
        else:
            num=krg["num"]
        if "dbtype" not in krg.keys():
            dbtype="postgresql"
        else:
            dbtype=krg["dbtype"]
        if "conp" not in krg.keys():
            conp=["postgres","since2015","127.0.0.1","postgres","public"]
        else:
            conp=krg["conp"]

        df=self.getdf(url,f1,f2,total,num)
        if len(df)>1:
            print(url)
            #print(df)
            df.columns=col
        else:
            df=pd.DataFrame(columns=col)
            print("暂无数据")
        db_write(df,tb,dbtype=dbtype,conp=conp)



