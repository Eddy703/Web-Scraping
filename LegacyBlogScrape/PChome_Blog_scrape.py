################################################################  #
#  This scraper is coded under Ubuntu 18.04 LTS                                                                                              #
#os.system command might be different if you are running on Windows                                               #
#please change it, if you wish to, and theoretical this works on any PCHome's blog home page,   #
#and this scraper scrape from the last page for ascending time order                                                     #
# Example: the first article on the last page is named as  {last page number}-1-{title}.csv                 #
#In order to use this scraper on another blogger, please find their id,                                                      #
# Example: for http://mypaper.pchome.com.tw/yakumo1987, you just have to give yakumo1987 #
##################################################################



import csv
import requests
import re
import os
from bs4 import BeautifulSoup as BS


def PCHomeblogScrape(id , page_num):
    articles_counter = 0
    # article_links=[]
    os.mkdir('./BlogPosts')
    os.mkdir('./BlogPosts/{}'.format(id))
    while (page_num > 0):
        url = 'http://mypaper.pchome.com.tw/{}/P{}'.format(id, page_num-1)
        connection = requests.get(url)
        if (connection.status_code != 200 ):
            print ('Connection is not established')
            break
        soup = BS(connection.text,'lxml')
        for link in set(soup.find_all('h3', class_ = 'title brk_h')):

        #article_links.append(link.a['href'])
            #print (link.a['href'])
            url = 'http://mypaper.pchome.com.tw/'+str(link.a['href'])
            connection = requests.get(url)
            if(connection.status_code != 200):
                print('Cannot connect to article. ')
                break
            content_soup  = BS(connection.text, 'lxml')
            titles =  content_soup.find('h3', class_='title brk_h').stripped_strings
            title= "".join([str(title).strip() for title in titles])
            articles_counter += 1
            with open('./BlogPosts/{}/{}-{}-{}.csv'.format(id, str(page_num), str(articles_counter), title), 'w', encoding='utf8') as f:
                f.write(title + '\n')
                #print(title)
                contents = content_soup.find('div', class_ = 'text_01').stripped_strings
                para=[str(content) for content in contents]
                content= "\n".join(para)
                f.write(content)
                print('Scraped blog with title {}!'.format(title))
        print('Page {} Scraped {} articles'.format(page_num, articles_counter))
        articles_counter = 0
        page_num -= 1
    print('DONE! See the output at ./BlogPosts/<id>  ! ')

if __name__ == '__main__':
    os.system('clear')
    print('--------------------------- Blog posts scraper ---------------------------')
    id = input("Tell me the ID of the user: ")
    page_numbers = int(input('Tell me how many pages does the user have: '))
    PCHomeblogScrape(id, page_numbers)
