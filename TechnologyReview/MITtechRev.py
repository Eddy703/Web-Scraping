from bs4 import BeautifulSoup as BS
from datetime import datetime as dt
import re
import requests
import csv
import os
import time

today = str(dt.today())[0:10]


def createDir(loc):
    if not os.path.exists(loc):
        os.mkdir(loc)


def storeArticle(link, module, title, mode='w'):
    global today
    if re.match('\/magazine\/', link):
        return
    c = requests.Session().get(link)
    c_soup = BS(c.text, 'lxml')
    plst = []
    if module == 'Download-Article':
        with open('./contents/{}/{}.csv'.format(today, module), mode, encoding='utf8') as f:
            writer = csv.writer(f)
            for ele in c_soup.find('div', class_='download__dek download__dek--full').children:
                if re.match('<p>', str(ele)):
                    plst.append("".join(str(string)for string in ele.stripped_strings))
            paragrahs = "\n".join(plst)
            overview = ""
            author = str(c_soup.find('div', class_= 'download__author-meta').p.strong.string)
            published_date = str(c_soup.find('time', class_= 'download__time-posted').string)
            # published_date = article_info.string
            # print ("{}\n{}\n{}\n{}\n".format(top_story_title, overview, author, paragrahs))
            row = [link, title, overview, author,published_date, paragrahs]
            writer.writerow(row)
            f.close()
        return
    print('Storing... {}\t{}'.format(module, title))
    with open('./contents/{}/{}.csv'.format(today, module), mode, encoding='utf8') as f:
        writer = csv.writer(f)
        for ele in c_soup.find('div', class_="article-body__content").children:
            if re.match('<p>', str(ele)):
                plst.append("".join(str(string).replace(',',' commaSign ')for string in ele.stripped_strings))
        paragrahs = "\n".join(plst)
        overview = c_soup.find('h2', class_='article-topper__subtitle').string
        info = c_soup.find_all('li', class_='article-topper__meta-item')
        author = info[0].a.string
        published_date = info[1].string
        row = [link, title, overview, author,published_date, paragrahs]
        writer.writerow(row)
        f.close()
    return


def MyTool():

    createDir('./contents')

    url = 'https://www.technologyreview.com'
    # try:
    r = requests.Session().get(url)
    if r.status_code != 200:
        print("Connection is not established....\nQuitting program...")
        quit()
    else:
        createDir('./contents/{}'.format(today))
        site = BS(r.text, 'lxml')
        top_stories = site.find_all('article', class_='top-story')
        for top_story in top_stories:
            link = url + str(top_story.a['href'])
            top_story_title = "".join([str(string)
                                       for string in top_story.stripped_strings])
            storeArticle(link, 'Top-Story', top_story_title)
        head = site.find('article', class_='hp-lead')
        head_title = str(head.h2.string)
        head_link = url + str(head.a['href'])
        storeArticle(head_link, 'head-story', head_title)
        download_stories = site.find_all('article', class_='download__article')
        for download_article in download_stories:
            title = str(download_article.h3.string)
            link = url + str(download_article.a['href'])
            storeArticle(link, 'Download-Article', title)
        grid_stories = site.find_all('div', class_='grid-tz__hgroup')
        for grid_story in grid_stories:
            title = str(grid_story.h2.string)
            link = url + str(grid_story.a['href'])
            storeArticle(link, 'Grid-Story', title)
        features_stories = site.find_all('div', class_='grid-tz__hgroup')
        for features_story in features_stories:
            feature_mod = site.find('div', class_="cover-tz__hgroup")
            fmtitle = str(feature_mod.a.h2.string)
            fmlink = url + str(feature_mod.a['href'])
            storeArticle(fmlink, 'Features', fmtitle, 'w')
            title = str(features_story.h2.string)
            link = url + str(features_story.a['href'])
            storeArticle(link, 'Features', title, 'a')
        sponsored_stories = site.find_all('div', class_='group-tz__hgroup')
        for ss in sponsored_stories:
            title = str(ss.a.h2.string)
            link = url + str(ss.a['href'])
            storeArticle(link, 'Sponsored', title)
            # inside article:
            # article-body__content < div //for article paragrahs

            # article-topper__hgroup--bottom
            # article-topper__subtitle < h2 < div  //catch line or overview
            # article-topper__meta-info <ul

            # top-story < article
            # top-story__title < a. h2

            # hp-lead < article
            # hp-lead__title < a.h2

            # download__header < header
            # download__article < article
            # download__article < a. h3

            # grid-tz__hgroup < div
            # grid-tz__overline < h5
            # grid-tz__title < h2 << href

            # cover-tz__hgroup < div
            # cover-tz__overline < h5 << href for catagory
            # cover-tz__title <  a. h2

            # feature-tz__hgroup < div
            # feature-tz_overline__link < h5 << href catagory
            # feature-tz__title < h2 << href

            # group-tz__hgroup < div
            # group-tz__issponsored << h4
            # group-tz__title < a.h2
        # except Exception as e:


if __name__ == '__main__':
    os.system('clear')
    print("-" * 10 + "MIT TechnologyReview Scraper" + "-" * 10)
    MyTool()
