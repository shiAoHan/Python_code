# coding=utf-8
import requests
from bs4 import BeautifulSoup

allUniv = []  # all university


# requests库获取url页面的全部内容，作为返回值返回
def getHTMLText(url, timeout=30):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""


# 将requests库获取的数据，交由bs4清洗，提取出<tr>中的<td>（表格）中的<a>标签中的信息，每一行的数据先按列存入singleUniv一维数组，然后按行存入allUniv二维数组中
def fillUnivList(soup):
    data = soup.find_all('tr')  # 找到所有的tr，一个tr包含一所学校的所有信息："排名","学校名称","省份","类型","总分","办学层次"
    for tr in data:
        ltd = tr.find_all('td')  # 找到tr中所有的td，一个td包含学校的一个具体信息，如排名、学校名称等
        if len(ltd) == 0:  # 如果tr中没有找到td，进入下一次循环
            continue
        singleUniv = []
        for td in ltd:
            tda = td.find('a')  # 寻找td中的<a>标签，其中包含学校名称，实际网站中只会有一个<a>标签，使用find()即可，存入tda中
            if tda:
                UniName = tda.string  # 如果tda不为空,将学校名称赋值给UniName，下一步存入singleUniv中
                singleUniv.append(UniName)
                print(singleUniv)
            elif td.string.strip():  # strip方法去除两侧（不包含内部）空格的字符串，如果不为空，存入singleUniv中
                singleUniv.append(td.string.strip())
        allUniv.append(singleUniv)


# 将allUniv中的数据写入txtPath路径所指的txt文件中，并使用string.format格式化每条数据
# 也可在参数中添加num参数，控制写入的数据量——前num名
def printUnivListInText(txtpath):
    with open(txtpath, 'w+', encoding='utf-8') as t:
        s = '{1:^4}{2:{0}^10}{3:{0}^7}{4:{0}^6}{5:{0}^8}{6:{0}^8}'.format(chr(12288), "排名", "学校名称", "省份", "类型", "总分","办学层次")
        t.write(s)
        # 排名1到100有办学层次的信息，排名100之后没有
        for i in range(100):
            u = allUniv[i]
            t.write('\n{1:^4}{2:{0}^12}{3:{0}^4}{4:{0}^10}{5:{0}^8.5}{6:{0}^8}'.format(chr(12288), u[0], u[1], u[2], u[3],float(u[4]), u[5]))
        for i in range(100, len(allUniv)):
            u = allUniv[i]
            t.write('\n{1:^4}{2:{0}^12}{3:{0}^4}{4:{0}^10}{5:{0}^8.5}'.format(chr(12288), u[0], u[1], u[2], u[3],float(u[4])))
    t.close()


def printUnivListInCsv(txtpath):
    with open(txtpath, 'w+', encoding='utf-8') as t:
        s ='{1},{2},{3},{4},{5},{6}'.format(chr(12288), "排名", "学校名称", "省份", "类型", "总分","办学层次")
        t.write(s)
        # 排名1到100有办学层次的信息，排名100之后没有
        for i in range(100):
            u = allUniv[i]
            t.write('\n{1},{2},{3},{4},{5},{6}'.format(chr(12288), u[0], u[1], u[2], u[3],float(u[4]), u[5]))
        for i in range(100, len(allUniv)):
            u = allUniv[i]
            t.write('\n{1},{2},{3},{4},{5}'.format(chr(12288), u[0], u[1], u[2], u[3],float(u[4])))
    t.close()

# 为url、txtPath赋值，为程序提供数据源和数据写入位置
if __name__ == "__main__":
    url = 'https://www.shanghairanking.cn/rankings/bcur/2020'
    txtPath = r'C:\Users\Administrator\Desktop\test.csv'
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')  # 非自定义函数
    fillUnivList(soup)
    printUnivListInCsv(txtPath)  # 可在参数中填入参数num，返回指定排名范围内的信息

# 数据嵌套的形式是：
"""
<tr data-v-45ac69d8>

<td data-v-45ac69d8>
1           # 排名
</td>

<td class="align-left" data-v-45ac69d8>
<a href="/institution/tsinghua-university" data-v-45ac69d8>
清华大学    #学校名称
</a>
<p style="display:none" data-v-45ac69d8></p>
</td>

<td data-v-45ac69d8>
北京      #省份
</td>

<td data-v-45ac69d8>
综合      #类型
</td>

<td data-v-45ac69d8>
852.5    #总分
</td>

<td data-v-45ac69d8>
38.2       #办学层次
</td>

</tr>
"""
