# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import pymysql
# class QuotesPipeline(object):
#
#     def __init__(self):
#         self.connect = pymysql.connect(
#             host='localhost',
#             db='bobzuishuai',
#             user='bobo',
#             passwd='',
#             use_unicode=True)
#         self.cursor = self.connect.cursor()
#     def process_item(self, item, spider):
#         fly_sql ='''insert into fly(_date,ans_date,_source,department,aera,url,_content,ans_content) values(%s,%s,%s,%s,%s,%s,%s,%s)'''
#         # ( item['date'],item['ans_date'],item['source'],item['department'],item['area'],item['url'],item['_content'],item['ans_content'])
#         self.cursor.execute(fly_sql,
#                             (item['date'],item['ans_date'],
#                              item['source'], item['department'],
#                              item['aera'],item['url'],
#                              item['_content'], item['ans_content']))
#         self.connect.commit()
#
#         return item
#
#     def close_spider(self, spider):
#         self.connect.close()
#         self.cursor.close()



import pymysql
import redis
import pandas
 # --------更换数据库时要更改------------- 
redis_db = redis.Redis(host='',port=,db=1) # 连接本地redis，db数据库默认连接到0号库，写的是索引值
# redis_db = redis.Redis(host='localhost',port=6379,db=1) # 连接本地redis，db数据库默认连接到0号库，写的是索引值
redis_data_dict ='url'  # key的名字，里面的内容随便写，这里的key相当于字典名称，而不是key值。为了后面引用而建的
 
# 这里待优化，数据量多可能会爆掉
class QuotesPipeline(object):
    def __init__(self):
        # 连接mysql
        # --------更换数据库时要更改-------------
        # self.connect = pymysql.connect(
        #                 host='localhost',
        #                 db='',
        #                 user='bobo',
        #                 passwd='',
        #                 use_unicode=True)
        self.connect = pymysql.connect(
                host='',
                db='',
                user='root',
                passwd='',
                use_unicode=True)
        self.cursor = self.connect.cursor()
        # print(redis_db)
        redis_db.flushdb()  # 清空当前数据库中的所有 key，为了后面将mysql数据库中的数据全部保存进去
        # print(redis_db)
        if redis_db.hlen(redis_data_dict) == 0:  # 判断redis数据库中的key，若不存在就读取mysql数据并临时保存在redis中
            # --------更换数据库时要更改-------------
            sql = 'select url from fly'  # 查询表中的现有数据
            # --------------------------------------
            df = pandas.read_sql(sql,self.connect)  # 读取mysql中的数据
             # print(df)
            for url in df['url'].get_values():
                redis_db.hset(redis_data_dict,url,0) # 把每个url写入field中，value值随便设，我设置的0  key field value 三者的关系
 
    def process_item(self,item,spider):
        if redis_db.hexists(redis_data_dict,item['url']): # 比较的是redis_data_dict里面的field
            print("数据库已经存在该条数据，不再继续追加")
        else:
            try:
                self.do_insert(item)
            except pymysql.err.InternalError:
                pass

 
    def do_insert(self, item):
        fly_sql = '''insert into fly(date,ans_date,source,department,aera,url,_content,ans_content) values(%s,%s,%s,%s,%s,%s,%s,%s)'''
        # ( item['date'],item['ans_date'],item['source'],item['department'],item['area'],item['url'],item['_content'],item['ans_content'])
        self.cursor.execute(fly_sql,
                            (item['date'],item['ans_date'],
                             item['source'], item['department'],
                             item['aera'],item['url'],
                             item['_content'], item['ans_content']))
        self.connect.commit()

        return item
 
    def close_spider(self,spider):
        self.cursor.close()  # 关闭游标
        self.connect.close()    # 关闭连接

