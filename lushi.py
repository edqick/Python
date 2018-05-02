import json
import csv
'''
解析炉石卡牌部分数据
利用json文件的数据提取数据并保存进csv文件中
'''
class lushi():
    cards_list = []
    card_heraders = []

    def card_info_split(self):
        with open('F:\PycharmProjects\demo\pachong\cards.json',encoding='UTF-8') as f:
            jsons = f.readlines()
            cards = json.loads(json.dumps(jsons))#先将json文件读入为json类型对象，再转换为字符串
            cards_json = cards[0].split('({')
            cards_warrior = cards_json[1][:-2]
            cards_details = cards_warrior.split('"warrior":{')#去除头部
            cards_detail = cards_details[1][:-2].split('},')#去除末尾的后大括号
            for card in cards_detail:
                cards_info = {}
                card_des = card.split(':{')[1]
                card_fileds = card_des.split(',')
                if len(card_fileds)<2:
                    card_fileds.pop(0)
                for fileds in card_fileds:
                    filed = fileds.split(',')[0]
                    info = filed.split(':')
                    if len(info)<2:#去除不必要的元素
                        info.pop(0)
                    if len(info)==2:#去除字符串中的引号
                        if len(info[1])<2:#排除不带引号的数字
                            cards_info[info[0][1:-1]] = info[1]
                        else:
                            cards_info[info[0][1:-1]] = info[1][1:-1]

                    if len(info) == 3:#组合url字符串
                        cards_info[info[0][1:-1]] = info[1][1:]+':'+info[2][:-1]

                    if len(info) >1 :#获取头字段
                        if len(self.card_heraders)<9:
                            self.card_heraders.append(info[0][1:-1])

                if len(cards_info) >0:#排除空列表
                    self.cards_list.append(cards_info)
        return self.cards_list

    def write_to_csv(self,filename):#写入csv文件
        with open(filename+'.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, self.card_heraders)
            writer.writeheader()
            writer.writerows(self.cards_list)


ls = lushi()
headers = ls.card_heraders
cards_list = ls.card_info_split()
#print(headers)
#print(cards_list)
#ls.write_to_csv('lushi_card2')




