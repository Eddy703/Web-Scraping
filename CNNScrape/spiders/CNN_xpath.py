# -*- coding: utf-8 -*-
import scrapy
import json

class CnnXpathSpider(scrapy.Spider):
    name = 'CNN_xpath'
    allowed_domains = ['edition.cnn.com']
    start_urls = ['https://edition.cnn.com/']

    def parse(self, response):
        urls = response.xpath("////div/div/ul/li/a[@class='nav-flyout__submenu-link']")
        with open("./log_urls_catagories.json", 'w', encoding = 'utf-8') as f:
            for url in urls:
                json.dump({
                        'text': url.xpath("text()").get(),
                        'href': url.xpath("@href").get()
                }, f)
                f.write('\n')
                tmpurl = scrapy.urljoin(url)
                yield scrapy.Request(tmpurl, callback = parse_inCatagory)

    def parse_inCatagory(self, response):
        pass
