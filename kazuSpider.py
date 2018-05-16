# -*- coding: utf-8 -*-
import requests
import time
import json
import re
from lxml import etree
'''
@author：edqick
@date:2018-05-16
@language:Python with requests,lxml,json...
爬取多玩炉石卡组页面的卡组详情
1.从卡组主页（http://ls.duowan.com/d/）获取卡组列表页面总数（page_alls）
2.根据第1步获取的总数构建出每一个卡组列表页面的链接：http://ls.duowan.com/d/pag{1-page_alls}.html
3.根据第2步得到的页面依次爬取得到每个页面的详情信息：链接，标题，日期，职业等等
4.根据第3步获得的每个详情页面的链接，爬取每个详情页面的卡组详情：卡牌名称，卡牌数量；
由于卡牌详情是由js生成的，根据分析，从第4步获取的页面中获取到p1及p2两个参数，
然后从固定链接（http://huodong.duowan.com/ls_backend/index.php?r=data/index&p1&p2）中获取数据
5.按需存入数据库（MongonDBs）
'''

class kazuSpider():
    start_urls = 'http://ls.duowan.com/d/'
    page_urls = []
    detail_urls = []
    kazu_infos = {}
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "da_ui=5a5770ec8f1a92942; hiido_ui=0.3100047117593445; hd_newui=0.4809064122240587; dw_mini_popup_status=0; 20180514statistics=2518is0woy; 124232be6fdac438c1cc2be2e7f8405b=1; 20180515statistics=fpus999joy; Hm_lvt_66ee381f0140ac33122f0051eae9b401=1525168440,1525250787,1526303509,1526365810; Hm_lpvt_66ee381f0140ac33122f0051eae9b401=1526367686",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }

    def getListPageUrls(self):
        print("----------开始获取列表页面URL----------")
        response = requests.get(self.start_urls,headers=self.headers)
        pageContent = etree.HTML(response.text)
        page_all = pageContent.xpath("//ul[@class='pagnav']/li[8]/a/text()")[0]
        print("共计：%s 个列表页面。"%page_all)
        for num in range(1,int(page_all)+1):
            url_name = "http://ls.duowan.com/d/pag"+str(num)+".html"
            if url_name not in self.page_urls:
                self.page_urls.append(url_name)
        print("最終总列表页面数：" + str(len(self.page_urls)))

    def getdetailPageUrls(self):
        print("----------开始获取详情页面URL----------")
        for url in self.page_urls:
            response = requests.get(url,headers=self.headers)
            pageContent= etree.HTML(response.text)
            urls = pageContent.xpath("//ul[@class='card_list cs-clear']/a")
            for url in urls:
                page_url = url.xpath("./@href")[0]
                match = re.fullmatch('http://ls.duowan.com/\d{4}/\d{12}.html',page_url)#使用正则表达式过滤无效的url
                if match is not None:
                    if page_url not in self.detail_urls:
                        # print(page_url)
                        self.detail_urls.append(page_url)
        print("总详情页面数：" + str(len(self.detail_urls)))

    def getCardsListUrls(self):
        print("----------开始获取卡组信息URL----------")
        num = 1
        for url in self.detail_urls:
            cardUrls = []
            # print(url)
            response = requests.get(url,headers=self.headers)
            pageContent = etree.HTML(response.text)
            cardsJob = pageContent.xpath("//div[@class='mod-crumbs-bd']/a[4]/text()")
            cardsTitle = pageContent.xpath("//div[@id='article']/h1/text()")
            cardsDate = pageContent.xpath("//div[@id='article']/address/span[1]/text()")
            cardDetail = pageContent.xpath("//div/@data-card")
            # print(cardDetail)
            if len(cardsJob)==0:
                cardsJob='多职业套牌'
            if len(cardDetail)==0 or len(cardDetail[0])<20:
                continue
            for card in cardDetail:
                cardUrl = "http://huodong.duowan.com/ls_backend/index.php?r=data/index%s"%(card)
                cardUrls.append(cardUrl)
            self.kazu_infos['card'+str(num)]={'cardsJob':cardsJob,'cardsTitle':cardsTitle,'cardsDate':cardsDate,'url':url,'dataUrl':cardUrls}
            num +=1
        print("总卡组信息数：" + str(len(self.kazu_infos)))

    def resCardsList(self):
        for cards in self.kazu_infos:
            kazu = []
            for url in self.kazu_infos[cards]['dataUrl']:
                cardsInfo = requests.get(url)
                content = json.loads(cardsInfo.text[1:-1],encoding='utf-8')
                # print(content)
                try:
                    kazu.append(content['seconde'])
                except:
                    print(content)
            self.writeToMongo(self.kazu_infos[cards],kazu)

    def writeToMongo(self,kazu_infos,content):
        from pymongo import MongoClient
        print("----------连接MongoDB----------")
        conn = MongoClient("localhost",27017)
        db = conn.lushi
        my_set = db.kazu
        kazu_infos['kazu']=content
        print(kazu_infos)
        print("----------写入数据到MongoDB----------")
        my_set.insert(kazu_infos)


if __name__ == '__main__':
    print("===============主程序开始===============")
    startTime = time.ctime()
    print(startTime)
    ks = kazuSpider()
    ks.getListPageUrls()
    ks.getdetailPageUrls()
    ks.getCardsListUrls()
    ks.resCardsList()
    endTime = time.ctime()
    print(endTime)
    print("===============主程序结束===============")
