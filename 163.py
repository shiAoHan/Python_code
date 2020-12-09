'''
Description: 
Version: 1.0
Autor: Shi_Ao_Han
Date: 2020-10-05 07:34:29
LastEditors: Shi_Ao_Han
LastEditTime: 2020-10-12 18:03:05
'''
# -*-coding:utf-8-*-
# 163邮箱
from selenium import webdriver
import time
driver = webdriver.Chrome()
driver.get('https://mail.163.com/')
time.sleep(2)
driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
driver.find_element_by_name('email').send_keys('aqp2000329')
time.sleep(2)
driver.find_element_by_name('password').send_keys('aqp13213570940')
time.sleep(2)
driver.find_element_by_id('dologin').click()
time.sleep(8)
driver.switch_to.default_content()  # 跳出frame，回到主页面
driver.find_element_by_xpath(
    '//*[@id="_mail_component_130_130"]/span[2]').click()
