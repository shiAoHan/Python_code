# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
import os


# requests库获取url页面的全部内容，作为返回值返回，不能读取图片的url,只适用获取文本
def getHTMLText(url, timeout=30):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

    # 获取src     页面中所有<img>标签的src值，也就是image的网络地址url，先筛选出所有的<p>标签，进一步选出<img>标签，使用正则提取src值


def fillImageUrl_List(txtpath, soup):
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


def getImageUrlList(txtpath, allurl):
    with open(txtpath, 'w+', encoding='utf-8') as t:
        for url in allurl:
            t.write(url + '\n')
    t.close()

    # 打印所有image


def printAllImage(txtpath, image_file):
    with open(txtpath, 'r+') as image_url_list:
        n = 0
        for url in image_url_list:
            try:
                image_txt = requests.get(url)
                with open(image_file + r'\PPT' + str(n) + '.jpg', 'wb') as image:
                    image.write(image_txt.content)
                image.close()
                n = n + 1
            except requests.exceptions.MissingSchema:
                print('结束')

    # 创建文件夹


def creatImageFile():
    project_path = os.getcwd()
    image_file = project_path + r'\image'
    if not os.path.exists(image_file):
        os.mkdir(image_file)
    return image_file


def main():
    # 为url、txtPath赋值，为程序提供数据源和数据写入位置
    url = 'https://mp.weixin.qq.com/s/fkKgsb3PpLF3l3aKaluM3A'  # 公众号文章地址
    html = getHTMLText(url)
    allUrl = re.findall('data-src="(.*?)"', html)
    txtPath = os.getcwd() + r'\image_url.txt'  # 用image_url.txt 存储所有图片的网络地址
    # soup = BeautifulSoup(html, 'html.parser')       #非自定义函数
    # fillImageUrl_List(txtPath,soup)
    getImageUrlList(txtPath, allUrl)
    image_file = creatImageFile()
    printAllImage(txtPath, image_file)



if __name__ == "__main__":
    main()