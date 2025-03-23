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


class CollectorPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def get_items(self):
        return self.items


class HanimePipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active

        self.ws.title = "hanime"
        self.ws.append(["ID","观看网址",'标题'])

    def close_spider(self,spider):
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        file_pat = os.path.join(OUTPUT_DIR,"hanime.xlsx")
        self.wb.save(file_pat)

    def process_item(self, item, spider):
        id = item.get('id','')
        href = item.get('watch_href','')
        title = item.get('title','')
        self.ws.append((id,href,title))

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