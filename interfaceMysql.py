from MySQLdb import connections as cont
'''
MySQL数据库接口
'''
class interfaceMysql():
    conn = None
    cursor = None
    def getConn(self,user,password,host,database):
        self.conn = cont.Connection(user=user, # 连接MySQL数据库
                                        password=password,
                                        host=host,
                                        database=database, charset='utf8')
        self.cursor = self.conn.cursor()  # 获取游标

    def selectMysql(self,sql):
        select = (sql)#创建查询语句
        self.cursor.execute(select)#执行查询语句
        return self.cursor

    def updateMysql(self,table,filed,filedValue,condition,conditionValue):
        select = ("update %s set %s='%s' where %s=%s;"%(table,filed,filedValue,condition,conditionValue))# 创建查询语句
        print(select)
        self.cursor.execute(select)  # 执行查询语句
        self.conn.commit()  # 提交到数据库

    def delMysql(self,table,condition,conditionValue):
        select = ("delete from %s where %s='%s';"%(table,condition,conditionValue))  # 创建查询语句
        print(select)
        self.cursor.execute(select)  # 执行查询语句
        self.conn.commit()  # 提交到数据库

    def insertMysql(self,table,values):
        insert = ('insert into %s values(%s,"%s","%s","%s","%s","%s","%s",%s);'%(table,values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7]))  # 创建插入语句
        #print(insert)
        self.cursor.execute(insert)  # 执行插入语句
        self.conn.commit()#提交到数据库

    def closeConn(self):
        self.cursor.close()  # 关闭连接
        self.conn.close()

# ------------------------------------------------------------
# inter_mysql = interfaceMysql()
# inter_mysql.getConn('root','123456','127.0.0.1','two')
# select_sql = "select * from article_article;"
# zs = [1,'zhangsan']
# ls = [2,'lisi']
# inter_mysql.insertMysql('test',zs)#增
# inter_mysql.insertMysql('test',ls)
# inter_mysql.delMysql('test','name','world')#删
# inter_mysql.updateMysql('test','name','world','id',1)#改
# cursor = inter_mysql.selectMysql(select_sql)#查
# inter_mysql.closeConn()#关闭链接
# ------------------------------------------------------------
