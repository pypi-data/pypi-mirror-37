#coding:utf-8
# 导入selenium的浏览器驱动接口
from selenium import webdriver

# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

# 导入chrome选项
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as BS
import time

class wudi:
    def __init__(self,nohead=1):
        a=1
        # 创建chrome浏览器驱动，无头模式（超爽）
        chrome_options = Options()
        if nohead==1:
            chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
    def getPage(self,url):
        self.driver.get(url)
        return self.driver.page_source

    def getSoup(self,url):
        data=self.getPage(url)
        return BS(data,'html.parser')
    def close(self):
        self.driver.quit()
    def get_detail(soup):
        #for pd in soup.select('span.price-det'):
        #    print pd
        for lil in soup.select('li.list-item'):
            #print lil
            print(lil.select('span.comm-address')[0].get_text().encode("UTF-8"))
            print(lil.select('span.price-det')[0].get_text())
    def login_vipkid(self,usrname,passwd):
        url=u"http://sso.vipkid.com.cn/user/login"
        soup=self.getSoup(url)
        #wd.driver.find_elements_by_tag_name("input")[0].send_keys("zhaomingming")
        #wd.driver.find_elements_by_tag_name("input")[1].send_keys("20180717Vipkid")
        self.driver.find_elements_by_tag_name("input")[0].send_keys(usrname)
        self.driver.find_elements_by_tag_name("input")[1].send_keys(passwd)
        self.driver.find_elements_by_tag_name("button")[0].click()
        time.sleep(3)
        self.driver.save_screenshot(u"vipkid_login.png")

        self.driver.find_elements_by_tag_name("button")[2].click()
        vcode=input("input verify code: ")
        self.driver.find_elements_by_tag_name("input")[2].send_keys(str(vcode))
        self.driver.find_elements_by_tag_name("button")[3].click()
        time.sleep(3)
        self.driver.save_screenshot("vipkid_login_success.png")

        #url1="http://clt.management.vipkid.com.cn/operation/classroom/classroom/82177652"

        #soup=self.getSoup(url1)
        #time.sleep(3)
        print(self.driver.current_url)
        self.driver.save_screenshot("vipkid_login_class.png")
    def get_video_index(self,class_id,re_run_flag=0):
        if re_run_flag:
            self.getSoup("http://clt.management.vipkid.com.cn/operation/classroom/classroom/%s"%(class_id))
            time.sleep(3)
            self.driver.switch_to.frame(self.driver.find_elements_by_id("supplierClassRoom")[0])
        index=0
        ci=0
        for tv,sv in zip(self.driver.find_elements_by_class_name("t-video"),self.driver.find_elements_by_class_name("s-v
ideo")):
              tvv=tv.find_elements_by_tag_name("video")
              svv=sv.find_elements_by_tag_name("video")
              print(len(tv.find_elements_by_tag_name("video"))," vs ",len(sv.find_elements_by_tag_name("video")))
              if len(tvv)>0:
                    print(" %s teacher : %s"%(class_id,tvv[0].get_attribute("src")))
              if len(svv)>0:
                    print(" %s student : %s"%(class_id,svv[0].get_attribute("src")))
              if len(tvv)>0 and len(svv)>0:
                  index=ci
                  print("index = %s"%(index))
              ci+=1
        return index

    def get_video_url(self,class_id):
        self.getSoup("http://clt.management.vipkid.com.cn/operation/classroom/classroom/%s"%(class_id))
        time.sleep(6)
        self.driver.switch_to.frame(self.driver.find_elements_by_id("supplierClassRoom")[0])

        index=self.get_video_index(class_id)
        url_teacher=self.driver.find_elements_by_class_name("t-video")[index].find_elements_by_tag_name("video")[0].get_
attribute("src")
        url_student=self.driver.find_elements_by_class_name("s-video")[index].find_elements_by_tag_name("video")[0].get_
attribute("src")
        url={"student":url_student,"teacher":url_teacher}
        return url
    '''
    def get_video_url(self,class_id):
        self.getSoup(u"http://clt.management.vipkid.com.cn/operation/classroom/classroom/%s"%(class_id))
        time.sleep(3)
        self.driver.switch_to.frame(self.driver.find_elements_by_id("supplierClassRoom")[0])
        url_teacher=self.driver.find_elements_by_class_name("t-video")[0].find_elements_by_tag_name("video")[0].get_attribute("src")
        url_student=self.driver.find_elements_by_class_name("s-video")[0].find_elements_by_tag_name("video")[0].get_attribute("src")
        url={"student":url_student,"teacher":url_teacher}
        return url
    '''
if __name__=="__main__":
    wd=wudi()
    soup=wd.getSoup("https://beijing.anjuke.com/")
    print(soup)
    wd.login_vipkid("zhaomingming","20180717Vipkid")
    print(wd.get_video_url("82177652"))

    wd.close()
