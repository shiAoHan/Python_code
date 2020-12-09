# coding = utf-8
import re
import os
import json
import time
import urllib3
import requests
import transform_location as t_l
from lxml import etree
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Headers = {
    # 'cookie': 'Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _RSG=KqK3qETfa143fOqQl4rFXB; _RDG=282f24100640c82731283334fcc3364464; _RGUID=4064a5d3-b40d-4d14-b84f-d44bdad18a43; Union=OUID=index&AllianceID=4897&SID=155952&SourceID=&createtime=1600831032&Expires=1601435831593; MKT_OrderClick=ASID=4897155952&AID=4897&CSID=155952&OUID=index&CT=1600831031597&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fsid%3D155952%26allianceid%3D4897%26ouid%3Dindex&VAL={"pc_vid":"1600831028743.427gzc"}; MKT_CKID=1600831031634.5olt5.f6pj; MKT_CKID_LMT=1600831031635; _ga=GA1.2.248639397.1600831032; _gid=GA1.2.1954297618.1600831032; MKT_Pagesource=PC; GUID=09031031210931119554; nfes_isSupportWebP=1; appFloatCnt=1; nfes_isSupportWebP=1; ASP.NET_SessionSvc=MTAuNjAuMzUuMTQ2fDkwOTB8amlucWlhb3xkZWZhdWx0fDE1ODkwMDMyMjQ5NDI; U_TICKET_SELECTED_DISTRICT_CITY=%7B%22value%22%3A%7B%22districtid%22%3A%22835%22%2C%22districtname%22%3A%22%E6%8F%AD%E9%98%B3%22%2C%22isOversea%22%3Anull%7D%2C%22createTime%22%3A1600847243848%2C%22updateDate%22%3A1600847243848%7D; _RF1=113.118.204.141; _gat=1; _pd=%7B%22r%22%3A1%2C%22d%22%3A614%2C%22_d%22%3A613%2C%22p%22%3A634%2C%22_p%22%3A20%2C%22o%22%3A655%2C%22_o%22%3A21%2C%22s%22%3A668%2C%22_s%22%3A13%7D; _bfa=1.1600831028743.427gzc.1.1600843833503.1600847244099.5.49.10650038368; _bfs=1.30; _bfi=p1%3D290510%26p2%3D290510%26v1%3D49%26v2%3D48; _jzqco=%7C%7C%7C%7C1600831031803%7C1.1555887407.1600831031625.1600849509140.1600849530503.1600849509140.1600849530503.0.0.0.19.19; __zpspc=9.4.1600846262.1600849530.14%232%7Cwww.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}


def get_city(file_path):
    f = open(file_path, 'r', encoding='utf-8')
    cities = []
    for c in f:
        cities.append(c.replace('\n', ''))
    f.close()
    return cities


def draw_point(location):
    artist.find_element_by_id('x1').clear()
    artist.find_element_by_id('x1').send_keys(str(location[0]))
    artist.find_element_by_id('y1').clear()
    artist.find_element_by_id('y1').send_keys(str(location[1]))
    time.sleep(1)
    artist.find_element_by_id('button1').click()
    pass


def print_city_url(city):
    url = 'https://huodong.ctrip.com/things-to-do/list?pagetype=city&citytype=dt&keyword=' + city + '&pshowcode=Ticket2'
    print(city, ':', url)
    return url


def get_csv(pickpocket, city_url, t):
    page = 1
    pickpocket.get(city_url)
    time.sleep(3)
    while True:
        content = pickpocket.find_element_by_class_name('right-content-list').get_attribute('innerHTML')
        cons = re.findall(r'href="(.*?)" title="(.*?)"', content)
        print("当前页码：", page)
        for con in cons:
            detail_url = 'https:' + con[0]
            title = con[1]
            print(title)
            detail = get_detail(detail_url)
            location = get_location(detail[0])
            print(location)
            if location[2] != 0 or location[3] < 70:
                continue
            t.write('\n{1},{2},{3},{4},{5},{6},{7}'.format(chr(12288), location[0], location[1], title, detail[0],
                                                           detail[2], detail[3], detail[1]))
            draw_point(location)
        if page == maxPage:
            break
        try:
            pickpocket.find_element_by_class_name('u_icon_enArrowforward').click()
        except:
            break
        time.sleep(1)
        page += 1


def get_detail(detail_url):
    detail_con = requests.get(detail_url, verify=False, headers=Headers).text
    '''使用正则获取信息'''
    address = ''.join(re.findall(r'景点地址</p><p class="baseInfoText">(.*?)<', detail_con, re.DOTALL)).replace('\n', '').replace(',', '，')
    mobile = ''.join(re.findall(r'官方电话</p><p class="baseInfoText">(.*?)<', detail_con, re.DOTALL))
    '''使用xpath获取信息'''
    ret = etree.HTML(detail_con)
    desc_con = ret.xpath('//div[@class="detailModule normalModule"]//div[@class="moduleContent"]')
    try:
        content0 = ''.join(desc_con[0].xpath('.//text()'))
        introduction = content0.replace('\n', '').replace(',', '，')
    except:
        introduction = ''
    '''获取图片链接'''
    try:
        image = re.findall(r'background-image:url\((.*?)\)', detail_con, re.DOTALL)[0]
    except:
        image = ''
    return [address, mobile, introduction, image]


def get_location(address):
    try:
        ak = "99AO36G6CGA1sdePauND5vzral0iMgRA"
        url = "http://api.map.baidu.com/geocoding/v3/?address=" + address + "&output=json&ak=" + ak
        text = requests.get(url, verify=False, headers=Headers).text
        location_info = json.loads(text)
        if location_info["status"] != 0:
            return ['', '', 1, 0]
        status = location_info["status"]
        lng = location_info["result"]["location"]["lng"]
        lat = location_info["result"]["location"]["lat"]
        comprehension = location_info["result"]["comprehension"]
        # return [lng, lat, status, comprehension]
        location = t_l.bd09_to_wgs84(lng, lat)  # 百度坐标系转WGS84
        return [location[0], location[1], status, comprehension]
    except:
        return [0, 0, 1, 0]


def get_TD_location(address):
    try:
        tk = "5afdd46cdc487a3362b188b4856bc83a"
        url = 'http://api.tianditu.gov.cn/geocoder?ds={"keyWord":"' + address + '"}&tk=' + tk
        text = requests.get(url, verify=False, headers=Headers).text
        location_info = json.loads(text)
        if location_info["status"] != '0':
            return ['', '', 1, 0]
        status = 0
        lng = location_info["location"]["lon"]
        lat = location_info["location"]["lat"]
        score = location_info["location"]["score"]
        return [lng, lat, status, score]
    except:
        return [0, 0, 1, 0]


def main():
    file_path = r"C:\Users\Administrator\Desktop\city.txt"
    csv_path = r'C:\Users\Administrator\Desktop\景点地图.csv'
    Ctrip_ticket = 'https://piao.ctrip.com/ticket'

    options = Options()
    options.add_argument('--headless')
    pickpocket = Chrome(options=options)  # pickpocket 扒手

    with open(csv_path, 'w+', encoding='utf-8') as t:
        header = '{1},{2},{3},{4},{5},{6},{7}'.format(chr(12288), "longitude", "latitude", "title", "address",
                                                      "introduction", "image", "mobile")
        t.write(header)
        pickpocket.get(Ctrip_ticket)
        time.sleep(3)
        city_list = get_city(file_path)
        for city in city_list:
            city_url = print_city_url(city)
            get_csv(pickpocket, city_url, t)
    t.close()


if __name__ == "__main__":
    target = "携程景点"
    maxPage = 1
    artist = Chrome()   # artist 画家
    artist.maximize_window()
    artist.get(r"file:///E:\Project\HTML\test.html")
    main()
