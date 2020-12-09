# -*-coding:utf-8-*-
#QQ音乐自动搜索播放音乐
from selenium import webdriver
import time
driver=webdriver.Chrome()
driver.get('https://y.qq.com/')
time.sleep(8)
driver.find_element_by_xpath('//*[@id="divdialog_0"]/div[1]/a/i[1]').click()
time.sleep(5)
driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/span/a[2]').click()
time.sleep(5)
driver.switch_to.frame('frame_tips')
time.sleep(2)
driver.switch_to.frame('ptlogin_iframe')
time.sleep(2)
driver.find_element_by_class_name('nick').click()
time.sleep(5)
driver.switch_to.default_content()#跳出frame，回到主页面
driver.find_element_by_xpath('/html/body/div[1]/div/ul[1]/li[2]/a').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="like_song_box"]/div[1]/a[1]').click()