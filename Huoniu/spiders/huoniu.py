# -*- coding: utf-8 -*-
import scrapy, re, json
from Huoniu.items import HuoniuItem


class HuoniuSpider(scrapy.Spider):
    name = 'huoniu'
    allowed_domains = ['www.xdudvd.cn']
    base_url = 'http://www.xdudvd.cn/vshare/index.php?appName=firebull'
    start_urls = ['http://www.xdudvd.cn/api/v1/video/shareHot.json?appName=firebull&start=0&size=1000']

    def item(self, response):
        item = HuoniuItem()
        item['src'] = 'http:' + re.findall('<script>var src=\'(.*?)\'', response.text, re.S)[0]
        yield item

    def parse(self, response):
        html = json.loads(response.body)
        cards = html['cards']
        for card in cards:
            uid = card['video']['publisher']['uid']
            wid = card['video']['wid']
            roomId = card['video']['publisher']['roomId']
            url = self.base_url + '&uid=' + str(uid) + '&wid=' + str(wid) + '&roomId=' + str(roomId)
            yield scrapy.Request(url=url, callback=self.item, dont_filter=True)
