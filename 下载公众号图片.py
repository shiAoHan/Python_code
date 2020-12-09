# coding=utf-8
import requests
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


# 创建图片文件夹
def creatImageFile():
    project_path = os.getcwd()
    image_file = project_path + r'\image'
    if not os.path.exists(image_file):
        os.mkdir(image_file)
    return image_file


# 打印图片
def printAllImage(urls, image_file):
    n = 0
    for url in urls:
        try:
            image_txt = requests.get(url)
            with open(image_file + r'\image' + str(n) + '.jpg', 'wb') as image:
                image.write(image_txt.content)
            image.close()
            n = n + 1
        except requests.exceptions.MissingSchema:
            print('下载结束')


# 为url、txtPath赋值，为程序提供数据源和数据写入位置
def main():
    # 此处填公众号文章地址，注意应该写在英文引号里
    url = 'https://mp.weixin.qq.com/s/fkKgsb3PpLF3l3aKaluM3A'  
    html = getHTMLText(url)
    allImageUrl = re.findall('data-src="(.*?)"', html)
    image_file = creatImageFile()
    printAllImage(allImageUrl, image_file)


if __name__ == "__main__":
    main()