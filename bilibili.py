'''
Description: 
Version: 1.0
Autor: Shi_Ao_Han
Date: 2020-10-05 17:45:46
LastEditors: Shi_Ao_Han
LastEditTime: 2020-10-12 18:02:34
'''
# -*-coding:utf-8-*-
#bilibili爬取评论
from selenium import webdriver
from time import  sleep
l1=[]
#print("请输入av号:")
av='BV16f4y1R7u6'
from selenium.common.exceptions import NoSuchElementException  #防止错误

def pa(): #定义函数，进行爬取
    list = driver.find_elements_by_css_selector(
        '#comment > div > div.comment > div.bb-comment > div.comment-list > div > div.con > p')
    for i in list:
        l1.append(i.text)

url = 'https://www.bilibili.com/video/'+av
#chrome_path = "D:\Google\chromedriver.exe" #驱动的路径
driver = webdriver.Chrome()
driver.get(url)
sleep(10)
driver.execute_script('window.scrollBy(0,document.body.scrollHeight)')
sleep(1.5)#页面滚动到底部
driver.execute_script('window.scrollBy(0,1000)')
sleep(1.5)
#等待网络
sleep(10)
pa()
while (1):
    try:
        c =driver.find_element_by_css_selector("#comment > div > div.comment > div.bb-comment > div.bottom-page.paging-box-big > a.next")
        #print(c)
        c.click()#模拟点击下一页，当没有下一页的时候就会进行下面一个操作
        sleep(5)
        pa()
        sleep(1)
    except NoSuchElementException as e:
        print("没")
        break
for i in l1:
    print(i)
