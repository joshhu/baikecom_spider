# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BaikecomSpiderPipeline:
    def open_spider(self, spider):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['baikecom']
        self.baike_items = self.db['baike_items']
        self.olds = set([item['title'] for item in self.baike_items.find({}, {'title': 1})])
        self.start_size = self.olds.__len__()


    def process_item(self, item, spider):
        if item['text'] and item['title'] not in self.olds:
            self.baike_items.insert_one(
                    {
                        'baike_id': item['baike_id'],
                        'title': item['title'],
                        'name': item['name'],
                        'text': item['text'],
                        'page_url': item['page_url'],
                    })
            self.olds.add(item['title'])
            self.start_size += 1
            print(self.start_size)
        return item
    def close_spider(self, spider):
        self.client.close()
