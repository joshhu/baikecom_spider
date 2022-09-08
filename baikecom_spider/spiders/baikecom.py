import scrapy
import re
import urllib
from baikecom_spider.items import BaikecomSpiderItem

class BaikecomSpider(scrapy.Spider):
    name = 'baikecom'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/%E5%90%89%E5%A4%9A%C2%B7%E8%8C%83%E7%BD%97%E8%8B%8F%E5%A7%86/328361']

    def parse(self, response):
        page_url = response.request.url
        item_name = re.sub('/', '', re.sub('https://baike.baidu.com/item/',
                                           '', urllib.parse.unquote(response.url)))
        # 下面為百度百科香港的xpath
        # head_title = ''.join(response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').getall()).replace('/', '')
        # sub_title = ''.join(response.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h2/text()').getall()).replace('/', '')

        # 下面為百度百科中文的xpath
        head_title = ''.join(response.xpath('//dd[contains(@class, "lemmaWgt-lemmaTitle-title") and contains(@class, "J-lemma-title")]/span/h1/text()').getall()).replace('/', '')
        sub_title = ''.join(response.xpath('//dl[contains(@class, "lemmaWgt-lemmaTitle") and contains(@class, "lemmaWgt-lemmaTitle-")]/div[@class="lemma-desc"]/text()').getall()).replace('/', '')
        title = head_title + sub_title
        
        baike_item = BaikecomSpiderItem()
        baike_item['page_url'] = page_url
        baike_item['baike_id'] = item_name
        baike_item['title'] = title
        baike_item['name'] = head_title
        baike_item['text'] = ''
        for para in response.xpath('//div[@class="main-content"]/div[@class="para"] |//div[@class="main_tab main_tab-defaultTab  curTab"]/div[@class="para"] | //div[@class="lemma-summary"]/div[@class="para"]'):
                texts = para.xpath('.//text()').extract()
                for text in texts:
                    baike_item['text'] += text.strip('\n')
        yield baike_item

        items = set(response.xpath(
            '//a[contains(@href, "/item/")]/@href').re(r'/item/[A-Za-z0-9%\u4E00-\u9FA5]+'))
        for item in items:
            new_url = 'https://baike.baidu.com' + urllib.parse.unquote(item)
            new_item_name = re.sub(
                '/', '', re.sub('https://baike.baidu.com/item/', '', new_url))
            yield scrapy.Request(new_url, callback=self.parse)