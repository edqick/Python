from pachong.cardInfo import *
from pachong.interfaceMysql import *
'''
1.从CSV文件中读取数据并存入MySQL数据库
'''

if __name__ == '__main__':
    ci = cardInfo()
    ci.get_to_csv('./card.csv')