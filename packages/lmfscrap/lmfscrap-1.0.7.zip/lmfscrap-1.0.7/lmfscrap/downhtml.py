from selenium import webdriver
import pandas as pd 
import sys 
import time
from sqlalchemy import create_engine,types
import psycopg2
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



class page:
    def __init__(self):
        self.add_ip()
        self.tmp_q=Queue()
        self.ip_q=Queue()

        self.sema=Semaphore(1)
        self.__init_localhost_q()
    def add_ip(self):
        r = requests.get("http://www.trackip.net/")
        txt = r.text
        ip = txt[txt.find('title')+6:txt.find('/title')-1]
        i=3
        while i>0:
            x="""http://http.zhiliandaili.cn/Users-whiteIpAddNew.html?appid=2605&appkey=a95fd11b1e7f17d7dfe19969222e95b7&whiteip=%s"""%ip
            r=requests.get(x).json()
            if "存在" in r["msg"] or "成功" in r["msg"]:break

            if "最多数量" in r["msg"]:
                time.sleep(1)
                x="""http://http.zhiliandaili.cn/Users-whiteIpAddNew.html?appid=2605&appkey=a95fd11b1e7f17d7dfe19969222e95b7&whiteip=%s&index=5"""%ip
                r=requests.get(x).json()
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

    def __init_tmp_q(self,arr):
        self.tmp_q.queue.clear()
        for i in arr:
            self.tmp_q.put(i)

    def __read_thread(self,f):
        conp=self.conp
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
                self.db_write(conp,x,df)
                time.sleep(0.1)
                size=self.tmp_q.qsize()
                if size%100==0: print("还剩 %d 页"%size)

             except Exception as e:
                traceback.print_exc()
                print("第 %s 页面异常"%x)
                self.tmp_q.put(x)
                driver.quit()
                return False
        driver.quit()
        print("线程正常退出")
        return True 


    def read_thread(self,f):
        num=10
        flag=self.__read_thread(f)
        while  not flag and  num>0:
            num-=1
            print("切换ip,本线程第%d次"%(5-num))
            print("已经消耗ip %d 个"%self.ip_q.qsize())
            flag=self.__read_thread(f)

    def read_threads(self,f,arr,num=10):
        bg=time.time()
        ths=[]
        dfs=[]
        total=len(arr)
        if total<=5:num=1
        if total!=0:
            if num/total>1:
                num=int(total/5)+1 if int(total/5)+1 <4 else num

        print("本次共 %d 个页面,共%d 个线程"%(total,num))

        self.__init_tmp_q(arr)
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


    def db_write(self,conp,href,page):

        dbtype="postgresql"
        if dbtype=='postgresql':
            con=psycopg2.connect(user=conp[0], password=conp[1], host=conp[2], port="5432",database=conp[3])
        elif dbtype=='mssql':
            con=pymssql.connect(user=conp[0], password=conp[1], host=conp[2],database=conp[3])
        elif dbtype=='oracle':
            con = cx_Oracle.connect("%s/%s@%s/%s"%(conp[0],conp[1],conp[2],conp[3]))
        else:
            con = MySQLdb.connect(user=conp[0],passwd=conp[1],host=conp[2],db=conp[3])
        sql="""insert into %s.%s values($lmf$%s$lmf$,$lmf$%s$lmf$)"""%(conp[4],conp[5],href,page)
        cur=con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

    def db_write_many(self,conp,data):

        dbtype="postgresql"
        if dbtype=='postgresql':
            con=psycopg2.connect(user=conp[0], password=conp[1], host=conp[2], port="5432",database=conp[3])
        elif dbtype=='mssql':
            con=pymssql.connect(user=conp[0], password=conp[1], host=conp[2],database=conp[3])
        elif dbtype=='oracle':
            con = cx_Oracle.connect("%s/%s@%s/%s"%(conp[0],conp[1],conp[2],conp[3]))
        else:
            con = MySQLdb.connect(user=conp[0],passwd=conp[1],host=conp[2],db=conp[3])
        sql="""insert into %s.%s values(href,page)"""%(conp[4],conp[5])
        cur=con.cursor()
        cur.executemany(sql,data)
        con.commit()
        cur.close()
        con.close()


    def db_command(self,sql,conp):

        """db_command 仅仅到数据库"""
        dbtype="postgresql"
        if dbtype=='postgresql':
            con=psycopg2.connect(user=conp[0], password=conp[1], host=conp[2], port="5432",database=conp[3])
        elif dbtype=='mssql':
            con=pymssql.connect(user=conp[0], password=conp[1], host=conp[2],database=conp[3])
        elif dbtype=='oracle':
            con = cx_Oracle.connect("%s/%s@%s/%s"%(conp[0],conp[1],conp[2],conp[3]))
        else:
            con = MySQLdb.connect(user=conp[0],passwd=conp[1],host=conp[2],db=conp[3])
        cur=con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()



    def write(self,**arg):
        tb=arg['tb']
        conp=arg["conp"]

        f=arg["f"]
        num=arg["num"]
        arr=arg["arr"]

        
        sql="create table if not exists %s.%s(href text,page text,primary key(href))"%(conp[4],tb)
        self.db_command(sql,conp)
        print("创建表if不存在")
        conp.append(tb)
        print(conp)
        self.conp=conp
        self.read_threads(f=f,num=num,arr=arr)
        return self.tmp_q.qsize()



