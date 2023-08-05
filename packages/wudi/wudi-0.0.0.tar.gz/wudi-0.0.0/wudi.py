#coding:utf-8
# 导入selenium的浏览器驱动接口
from selenium import webdriver

# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

# 导入chrome选项
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as BS
class wudi:
    def __init__(self):
        a=1
        # 创建chrome浏览器驱动，无头模式（超爽）
        chrome_options = Options()
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
if __name__=="__main__":
    wd=wudi()
    soup=wd.getSoup("https://beijing.anjuke.com/")
    print(soup)
    wd.close()
