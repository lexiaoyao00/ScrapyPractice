# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter
import openpyxl


CWD_PATH = os.getcwd()
OUTPUT_DIR = os.path.join(CWD_PATH,'outputs')

class NyaaPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active

        self.ws.title = "nyaa_result"
        self.ws.append(["类型","标题", "种子","磁力","大小","上传时间","上传人数","下载人数","下载次数"])

    def close_spider(self, spider):
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        file_pat = os.path.join(OUTPUT_DIR,"nyaa_result.xlsx")
        self.wb.save(file_pat)

    def process_item(self, item, spider):
        category = item.get('category','')
        title = item.get('title','')
        torrent = item.get('torrent','')
        magnet = item.get('magnet','')
        size = item.get('size','')
        date = item.get('date','')
        seeder = item.get('seeder','')
        leecher = item.get('leecher','')
        downloads = item.get('downloads','')

        self.ws.append((category,title,torrent,magnet,size,date,seeder,leecher,downloads))

        return item

class DoubanPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active

        self.ws.title = "Top250"
        self.ws.append(["标题", "评分", "主题","时长","简介"])

    def close_spider(self,spider):
        self.wb.save("top250.xlsx")

    def process_item(self, item, spider):
        title = item.get('title','')
        rank = item.get('rank','')
        subject = item.get('subject','')
        duration = item.get('duration','')
        intro = item.get('intro','')
        self.ws.append((title,rank,subject,duration,intro))

        return item
