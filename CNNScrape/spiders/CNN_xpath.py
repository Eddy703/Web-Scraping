# -*- coding: utf-8 -*-
import scrapy
import json
import os
import re

dom = "https://edition.cnn.com"
class CnnXpathSpider(scrapy.Spider):
    name = 'CNN_xpath'
    start_urls = ['https://edition.cnn.com/']

    def parse_inCatagory(self, response):
            articles_urls = response.xpath("////section/div/div/div/ul/li/article/div/div/h3[@class='cd__headline']/a")
            artFwd = []
            with open("./log_articles.json", "a", encoding="utf8") as f:
                for article in articles_urls:
                    link = article.xpath("@href").get()
                    title = article.xpath("/span/text()").get()
                    if re.search(r"^\/(\w+)", link):
                        artFwd.append(dom + link)
                        json.dump({
                                "title": title, "href": link}, f)
                        f.write('\n')
                f.close()

    def parse(self, response):
        urls = response.xpath("////div/div/ul/li/a[@class='nav-flyout__submenu-link']"); fwd = []
        fwd = []
        # output catagory name & link to json file
        # might be removed in the future
        with open("./log_urls_catagories.json", 'a', encoding = 'utf-8') as f:
            for url in urls:
                # if not os.path.exists("./{}".format(url.xpath("text()").get())):
                #     os.mkdir("./{}".format(url.xpath("text()").get()))
                link = url.xpath("@href").get()
                name = url.xpath("text()").get()

                if re.search(r"^\/(\w+)", link):
                    fwd.append(dom + link)
                    json.dump({
                            "catagory": name,"href": (dom + link)}, f)
                    f.write('\n')
            f.close()

        for url in fwd:
            yield scrapy.Request(url, callback=self.parse_inCatagory)
