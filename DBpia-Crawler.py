from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

#Input
savename = "DBpia-Crawler" #File name
keyword = "고고학" #Search keyword
target_page = 3 #Page
driver = webdriver.Chrome('/usr/local/bin/chromedriver') #Chromedriver path

#Chromedriver setting
url = "https://www.dbpia.co.kr/"
driver.get(url)
driver.find_element_by_xpath('//*[@id="keyword"]').send_keys(keyword)
driver.find_element_by_xpath('//*[@id="bnHead"]/div[3]/div/div[1]/div[1]/a').click()

#Save list
titleL = []
authorL = []
publisherL = []
journalL = []
volumeL = []
dateL = []

print("====start====")

#Crawling
for i in range(target_page):

    items_source = driver.page_source
    soup = BeautifulSoup(items_source, 'html.parser')
    items = soup.find('div','searchListArea').find('div','listBody').find('ul').find_all('li', 'item')
    time.sleep(2)

    for item in items :

        #title
        title = ''
        try : title = item.find('div','titWrap').find('a').text
        except : title = ''
        titleL.append(title)

        #author
        author = ''
        try : author = item.find('li','author').text
        except : author = ''
        authorL.append(author)

        #publisher
        publisher = ''
        try : publisher = item.find('li','publisher').text
        except : publisher = ''
        publisherL.append(publisher)

        #journal
        journal = ''
        try : journal = item.find('li','journal').text
        except : journal = ''
        journalL.append(journal)

        #volume
        volume = ''
        try : volume = item.find('li','volume').text
        except : volume = ''
        volumeL.append(volume)

        #date
        date = ''
        try : date = item.find('li','date').text
        except : date = ''
        dateL.append(date)
        
    #Next page
    try:
        driver.find_element_by_xpath(f'//*[@id="pcPaging{str(i+1)}"]').click()
        time.sleep(2)
    except:
        pass
    print(i, "Done")
    i += 1
    time.sleep(2)
    
    #Next button
    if i % 10 == 0:
        driver.find_element_by_xpath('//*[@id="next"]').click()

print("====Done!====")

#Save
resultDict = dict(title = titleL,
                author = authorL,
                publisher = publisherL,
                journal = journalL,
                volume = volumeL,
                date = dateL)

csv_Name = "~/Desktop/{}.csv".format(savename)
xlsx_Name = "~/Desktop/{}.xlsx".format(savename)
DB = pd.DataFrame(resultDict)
DB.to_csv(csv_Name)
DB.to_excel(xlsx_Name)