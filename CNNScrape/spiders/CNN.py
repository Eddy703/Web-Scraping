# -*- coding: utf-8 -*-
import scrapy
import json
import os
import re
import sqlite3
"""
 TO-DO:
 - DB issue
 - Index error (optional)
 Done:
 - Get Catagories from homepage
 - Store titles and corresponding links
 - Grab article author, time and content
"""
transaction = []
if not os.path.exists("./Catagories"):
    os.mkdir("./Catagories")

connection = sqlite3.connect("./scraped_content.db")
c = connection.cursor()

def create_table():
    return c.execute("CREATE TABLE IF NOT EXISTS Article(catagory TEXT, time TEXT, author TEXT, editorial TEXT, content TEXT)")

def transaction_bld(sql):
    global connection; global c; global transaction
    transaction.append(sql)
    if len(transaction) > 5:
        c.execute("BEGIN TRANSACTION")
        for s in transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        transaction = []

dom = "https://edition.cnn.com"
create_table()

class CnnXpathSpider(scrapy.Spider):
    name = 'CNN_xpath'
    start_urls = ['https://edition.cnn.com/']
    create_table()

    # Initial parse
    def parse(self, response):
        urls = response.xpath("////div/div/ul/li/a[@class='nav-flyout__submenu-link']"); fwd = []
        with open("./log_urls_catagories.txt", 'w', encoding = 'utf-8') as f:  # Logging
            for url in urls:
                link = url.xpath("@href").get()
                if re.search(r"^\/(\w+)", link):
                    f.write(dom + link); f.write('\n')
                    yield scrapy.Request((dom + link), callback = self.parse_inCatagory)
            f.close()

    #Create catagories and grab article links
    def parse_inCatagory(self, response):
            catagory = response.request.url.split('/')[-1]
            articles_urls = response.xpath("////section/div/div/div/ul/li/article/div/div/h3[@class='cd__headline']/a")
            artFwd = []
            # Store the tiles and links as json, just in case of size limit when reusing
            with open("./Catagories/{}.json".format(catagory), "a", encoding="utf8") as f:
                for article in articles_urls:
                    link = article.xpath("@href").get()
                    title = article.xpath("span/text()").get()
                    if re.search(r"^\/(\w+)", link):
                        artFwd.append(dom + link)
                        json.dump({
                                "title": title, "href": (dom+link)}, f)
                        f.write('\n')
                f.close()
            for art in artFwd:
                if re.search(r"(\/live-news)|(\/videos)|(\/gallery)|(\/vr)|(\/vr-archives)|(\/profiles)", art):
                    continue
                elif re.search(r"(\/travel)", art):
                    yield scrapy.Request(art, callback = self.tra_content)
                else:
                    yield scrapy.Request(art, callback = self.norm_content)

    def tra_content(self, response):
        catagory = response.request.url.split('/')[-3]
        st= response.css("div.Article__subtitle::text").getall()
        author = st[0].replace(", CNN", "")
        time = st[-1]
        content = "\n".join(response.css("div.Article__body *::text").getall()).strip()
        sql = """INSERT INTO Article(catagory = ?, time = ?, author = ?, content = ?)""".format(catagory, time, author, content)
        transaction_bld(sql)

    def norm_content(self, response):
        catagory = response.request.url.split('/')[-3]
        content ="\n".join(response.css("div.l-container *::text").getall())
        editorial = response.css("span.metadata__byline__author a::text").get()
        time = response.css("p.update-time::text").get()
        if response.css("span.metadata__byline__author::text"):
            author = author = response.css("div.Article_subtitle::text").get()
            sql = """INSERT INTO Article(catagory = ?, time = ?, author = ?, editorial = ?, content = ?)""".format(catagory, time, author, editorial, content)
            transaction_bld(sql)
        else:
            sql = """INSERT INTO Article(catagory = ?, time = ?, editorial = ?, content = ?)""".format(catagory, time, editorial, content)
            transaction_bld(sql)
