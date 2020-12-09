import pandas
import re
import time
import requests
import urllib3
from lxml import etree
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Jy_jd(object):
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        self.chrome = Chrome(options=options)
        self.chrome.get(
            'https://huodong.ctrip.com/things-to-do/list?pagetype=city&citytype=dt&keyword=%E6%8F%AD%E9%98%B3&pshowcode=Ticket2')
        time.sleep(3)
        self.page = 1
        self.headers = {
            'cookie': 'Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _RSG=KqK3qETfa143fOqQl4rFXB; _RDG=282f24100640c82731283334fcc3364464; _RGUID=4064a5d3-b40d-4d14-b84f-d44bdad18a43; Union=OUID=index&AllianceID=4897&SID=155952&SourceID=&createtime=1600831032&Expires=1601435831593; MKT_OrderClick=ASID=4897155952&AID=4897&CSID=155952&OUID=index&CT=1600831031597&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fsid%3D155952%26allianceid%3D4897%26ouid%3Dindex&VAL={"pc_vid":"1600831028743.427gzc"}; MKT_CKID=1600831031634.5olt5.f6pj; MKT_CKID_LMT=1600831031635; _ga=GA1.2.248639397.1600831032; _gid=GA1.2.1954297618.1600831032; MKT_Pagesource=PC; GUID=09031031210931119554; nfes_isSupportWebP=1; appFloatCnt=1; nfes_isSupportWebP=1; ASP.NET_SessionSvc=MTAuNjAuMzUuMTQ2fDkwOTB8amlucWlhb3xkZWZhdWx0fDE1ODkwMDMyMjQ5NDI; U_TICKET_SELECTED_DISTRICT_CITY=%7B%22value%22%3A%7B%22districtid%22%3A%22835%22%2C%22districtname%22%3A%22%E6%8F%AD%E9%98%B3%22%2C%22isOversea%22%3Anull%7D%2C%22createTime%22%3A1600847243848%2C%22updateDate%22%3A1600847243848%7D; _RF1=113.118.204.141; _gat=1; _pd=%7B%22r%22%3A1%2C%22d%22%3A614%2C%22_d%22%3A613%2C%22p%22%3A634%2C%22_p%22%3A20%2C%22o%22%3A655%2C%22_o%22%3A21%2C%22s%22%3A668%2C%22_s%22%3A13%7D; _bfa=1.1600831028743.427gzc.1.1600843833503.1600847244099.5.49.10650038368; _bfs=1.30; _bfi=p1%3D290510%26p2%3D290510%26v1%3D49%26v2%3D48; _jzqco=%7C%7C%7C%7C1600831031803%7C1.1555887407.1600831031625.1600849509140.1600849530503.1600849509140.1600849530503.0.0.0.19.19; __zpspc=9.4.1600846262.1600849530.14%232%7Cwww.baidu.com%7C%7C%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        }

    def get_url(self):
        while True:
            content = self.chrome.find_element_by_class_name('right-content-list').get_attribute('innerHTML')
            cons = re.findall(r'href="(.*?)" title="(.*?)"', content)
            for con in cons:
                self.detail_url = 'https:' + con[0]
                self.title = con[1]
                print(self.detail_url, self.title)
                self.get_detail()
            self.chrome.find_element_by_class_name('u_icon_enArrowforward').click()
            time.sleep(1)

            self.page += 1
            if self.page == 120:
                break

    def get_detail(self):
        detail_con = requests.get(self.detail_url, verify=False, headers=self.headers).text
        # time.sleep(2)
        '''使用正则获取信息'''
        self.rank = ''.join(re.findall(r'rankText">(.*?)<', detail_con, re.DOTALL))
        self.address = ''.join(re.findall(r'景点地址</p><p class="baseInfoText">(.*?)<', detail_con, re.DOTALL))
        self.mobile = ''.join(re.findall(r'官方电话</p><p class="baseInfoText">(.*?)<', detail_con, re.DOTALL))
        print(self.rank, self.address, self.mobile)
        '''使用xpath获取信息'''
        ret = etree.HTML(detail_con)
        desc_cons = ret.xpath('//div[@class="detailModule normalModule"]//div[@class="moduleContent"]')
        desc_titles = ret.xpath('//div[@class="detailModule normalModule"]//div[@class="moduleTitle"]')
        desc_list = []
        desc_title_list = []
        for d in desc_cons:
            des = ''.join(d.xpath('.//text()'))
            desc_list.append(des)
        for d in desc_titles:
            des = ''.join(d.xpath('.//text()'))
            desc_title_list.append(des)
        desc_dict = dict(zip(desc_title_list, desc_list))
        print(desc_dict)
        '''获取图片链接'''
        img_list = []
        imgs = re.findall(r'background-image:url\((.*?)\)', detail_con, re.DOTALL)
        for img in imgs:
            '''匹配到的同一张图片会有两种尺寸，我们只要大图，所以把尺寸为521*391的匹配出来即可'''
            image = re.search(r'521_391', img)
            if image:
                img_list.append(img)
        print(img_list)
        self.get_ticket()

    def get_ticket(self):
        id = self.detail_url.split('/')[-1]
        print(id)
        ticket_url = f'https://piao.ctrip.com/ticket/dest/{id}?onlyContent=true&onlyShelf=true'
        ticket_res = requests.get(ticket_url, verify=False, headers=self.headers).text
        # time.sleep(1)
        ticket_ret = etree.HTML(ticket_res)
        ticket = ticket_ret.xpath('//table[@class="ticket-table"]//div[@class="ttd-fs-18"]/text()')
        price = ticket_ret.xpath(
            '//table[@class="ticket-table"]//td[@class="td-price"]//strong[@class="ttd-fs-24"]/text()')
        print(ticket)
        print(price)
        '''拿到的列表里可能存在不确定数量的空值，所以这里用while True把空值全部删除，这样才可以确保门票种类与价格正确对应上'''
        while True:
            try:
                ticket.remove(' ')
            except:
                break
        while True:
            try:
                price.remove(' ')
            except:
                break
        '''
            这里多一个if判断是因为我发现有些详情页即便拿到门票信息并剔除掉空值之后仍然存在无法对应的问题，原因是网页规则有变动，
            所以一旦出现这种情况需要使用新的匹配规则，否则会数据会出错（不会报错，但信息对应会错误）
        '''
        if len(ticket) != len(price):
            ticket = ticket_ret.xpath(
                '//table[@class="ticket-table"]/tbody[@class="tkt-bg-gray"]//a[@class="ticket-title "]/text()')
            price = ticket_ret.xpath('//table[@class="ticket-table"]//strong[@class="ttd-fs-24"]/text()')
            while True:
                try:
                    ticket.remove(' ')
                except:
                    break
            while True:
                try:
                    price.remove(' ')
                except:
                    break
            print(ticket)
            print(price)
        ticket_dict = dict(zip(ticket, price))
        print(ticket_dict)

if __name__ == '__main__':
    jy_jd = Jy_jd()
    jy_jd.get_url()
