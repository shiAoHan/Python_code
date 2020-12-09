# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re

allImag=[]  #all image

    #requests库获取url页面的全部内容，作为返回值返回，不能读取图片的url,只适用获取文本
def getHTMLText(url,timeout=30):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        return ""

    #获取tag      页面中所有<img>标签     将requests库获取的数据，交由bs4清洗：提取出<p>标签中的<img>标签的所有信息，按行存入allImag列表中
def fillImageTag_List(soup):
    data=soup.find_all('p')
    for p in data:
        img=p.find('img')
        if img==None:
            continue
        allImag.append(str(img))           #使用str()将img标签转化为字符串

    # 使用正则表达式提取<img>标签中的src值
def getUrl_List(txtpath):
    with open(txtpath, 'w+', encoding='utf-8') as t:
        for i in allImag:
            url = re.findall('data-src="(.*?)"', i)
            if len(url) == 0:
                continue
            t.write(url[0] + '\n')
    t.close()

    #获取src     页面中所有<img>标签的src值，也就是image的网络地址url，先筛选出所有的<p>标签，进一步选出<img>标签，使用正则提取src值
def fillImageUrl_List(txtpath,soup):
    data = soup.find_all('p')
    with open(txtpath, 'w+', encoding='utf-8') as t:
        for p in data:
            img = p.find('img')
            if img == None:
                continue
            url = re.findall('data-src="(.*?)"', str(img))
            if len(url) == 0:
                continue
            t.write(url[0] + '\n')
    t.close()

    #打印所有image
def printAllImage(txtpath,image_name):
    with open(txtpath,'r+') as image_url_list:
        n=0
        for url in image_url_list:
            image_txt=requests.get(url)
            with open(image_name+str(n)+'.jpg','wb') as image:
                image.write(image_txt.content)
            image.close()
            n=n+1

    #为url、txtPath赋值，为程序提供数据源和数据写入位置
if __name__=="__main__":
    url = 'https://mp.weixin.qq.com/s/x9aSUucHIEPNdqsOQU12Sg'       #公众号文章地址
    txtPath = r'C:\Users\Administrator\Desktop\image_url.txt'       #存储所有图片的网络地址
    image_folder = r'C:\Users\Administrator\Desktop\image'          #爬取前，需要新建image文件夹
    image_name=r'C:\Users\Administrator\Desktop\image\Singapore'
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')       #非自定义函数
    # fillImageTag_List(txtPath)
    # getUrl_List(soup)     #fillImageUrl_List=fillImageTag_List+getUrl_List  两步合一步
    fillImageUrl_List(txtPath,soup)
    printAllImage(txtPath,image_name)
