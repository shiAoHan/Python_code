'''
Description: QQ自动发说说
Version: 1.1
Autor: Shi_Ao_Han
Date: 2020-10-05 09:51:43
LastEditors: Shi_Ao_Han
LastEditTime: 2020-10-12 18:05:59
'''
# -*-coding:utf-8-*-
#QQ自动发说说
from selenium import webdriver
import time
#import win32api,win32con    #pip install pywin32库 模拟鼠标键盘动作
driver=webdriver.Chrome()
driver.get('https://qzone.qq.com/')
time.sleep(5)
driver.switch_to.frame('login_frame')
time.sleep(2)
driver.find_element_by_class_name('nick').click()#登录页面点击头像
time.sleep(5)
driver.switch_to.default_content()#跳出frame，回到主页面
time.sleep(2)
driver.find_element_by_xpath('//*[@id="qz_notification"]/a[2]').click()#关闭页面弹窗广告
time.sleep(2)
driver.find_element_by_xpath('//*[@id="$1_substitutor_content"]').click()#点击“说点什么吧”
time.sleep(2)
now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
driver.find_element_by_css_selector('div.textinput.textarea.c_tx2.input_focus.textinput_focus').send_keys('Test by python at '+now)  #输入内容
time.sleep(2)
driver.find_element_by_css_selector('div.op').click()#点击发表
time.sleep(20)
# win32api.keybd_event(17,0,0,0)  #ctrl键位码是17
# win32api.keybd_event(13,0,0,0)  #enter键位码是13
# win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0) #按下ctrl+enter键发送
# win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)





'''
from selenium import webdriver
import time
driver=webdriver.Chrome()
driver.get('https://qzone.qq.com/')
time.sleep(5)
driver.switch_to.frame('login_frame')
time.sleep(2)
driver.find_element_by_class_name('nick').click()#登录页面点击头像
time.sleep(5)
driver.switch_to.default_content()#跳出frame，回到主页面
time.sleep(2)
driver.find_element_by_xpath('//*[@id="qz_notification"]/a[2]').click()#关闭页面弹窗广告
time.sleep(2)
driver.find_element_by_xpath('//*[@id="$1_substitutor_content"]').click()#点击“说点什么吧”
time.sleep(2)
driver.find_element_by_css_selector('div.textinput.textarea.c_tx2.input_focus.textinput_focus').send_keys('Test by python.')  #输入内容
time.sleep(2)
driver.find_element_by_css_selector('div.op').click()#点击发表
time.sleep(20)
'''