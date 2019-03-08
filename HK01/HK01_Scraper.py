from bs4 import BeautifulSoup as BS
import os
from time import sleep as Pause
from datetime import datetime as dt
import requests
import csv
import re

str1 = "下載《香港01》App，打開App首頁，撳「＋」選取「01眾樂迷」做你嘅「已選頻道」，每日都睇盡【01眾樂迷】精彩內容啦！即睇 【01眾樂迷專屬頻道】"
str2 = "下載「香港01」App ，即睇城中熱話："
today = str(dt.today())[0:10]

print(f'*'*10 + f'HK01 articles scrape(Paragraphs only)' + f'*'*10) #Discrption of the file
Pause(1)
os.system('clear')

r=requests.get("https://www.hk01.com/") #request to get the site/ goto the site

print(f'Connected' if r.status_code == 200 else 'Connection failed') #check if .get succeed or not

data=r.text #get the html file
soup=BS(data,'lxml') #parse the html

href_lst = set(soup.find_all('a', href=re.compile('/'))) #find everythin that contains hyperlink

urls=[] #initialize an empty list for storing the url for later use (just for this particular file)

uCount=0 #count the relevant links

if not os.path.exists('./ScrapedContents/{}'.format(today)):
    os.mkdir('./ScrapedContents/{}'.format(today))

with open('./ScrapedContents/{}/url.csv'.format(today),'w',encoding='utf-8') as f: #create a file to store the contents
    writer=csv.writer(f) #used to write the row

    inlst=[] #initialize an empty list for writing in csv
    for item in href_lst: #iterate through the returned list

        if not(re.match('/[A-Za-z]*/[0-9]+/|/[A-Za-z...]|https://', item['href'])):
            #condition for filtering out unwanted links (such as /zone/18, /channel/18)
            url="https://www.hk01.com"+item['href'] #make a complete url instead of just /(*)/(*)/(*)
            title = str(item['href']).replace(str(re.compile('\/*.+\/')),'')
            urls.append(url)
            uCount+=1
            sublst=[title, url]
            inlst.append([title, url]) #stores the sublist into a wholelist for actually writing in later

    for subl in inlst:      #writing in !
        writer.writerow(subl)

f.close()

inlst2=[]
cCount=0
with open('./ScrapedContents/{}/content.csv'.format(today), 'w', encoding='utf-8') as k:
    kWriter=csv.writer(k)

    for url in urls:

        if url== "https://www.hk01.com/":
            #another condition for filtering unwanted link, this is for the hyperlink that links back to homepage
            continue

        c = requests.get(url)
        content=c.text
        content_soup=BS(content,'lxml')
        para_lst=content_soup.find_all('p', class_=re.compile('wa4tvz-0 hmJMOX sc-gqjmRU jTjJUk|u02q31-0 gvqXdj sc-gqjmRU gBjLGB'))

        completeContent=[]

        for para in para_lst:
            if (para.string == str2) or (para.string == str1):
                para.string.replace_with('')
            completeContent.append("".join(para.stripped_strings))
            #add seperated paragraphs to a list for joining back to a whole paragraph

        paragraph=''.join(completeContent)
        print(f'Scraping {url} \n' if c.status_code==200 else f'Error: requests.get failed')
        inlst2.append([str(url),paragraph])

    for subls in inlst2:
        kWriter.writerow(subls)
        cCount+=1

k.close() #close the file

#Conclusion on running this scraper
print(f'Done scraping, clearing screen in 6 seconds.')
Pause(6)
os.system('clear')
print(f'Received {uCount} relevant URLs and scraped {cCount} actual articles.')
