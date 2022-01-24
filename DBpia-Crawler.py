from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

#하단에 입력해주세요.
savename = "DBpia-Crawler" #저장 파일명
keyword = "고고학" #검색어
target_page = 3 #원하는 페이지

url = "https://www.dbpia.co.kr/"
driver = webdriver.Chrome('/usr/local/bin/chromedriver') #Chromedriver 주소
driver.get(url)
search_box = driver.find_element_by_xpath('//*[@id="keyword"]')
search_box_btn = driver.find_element_by_xpath('//*[@id="bnHead"]/div[3]/div/div[1]/div[1]/a')
search_box.send_keys(keyword)
search_box_btn.click()

titleL = []
authorL = []
publisherL = []
journalL = []
volumeL = []
dateL = []
abstractL = []

print("====start====")

iCount = 0
i = 1

while i <= target_page:
    items_source = driver.page_source
    soup = BeautifulSoup(items_source, 'html.parser')
    items = soup.find('div','searchListArea').find('div','listBody').find('ul').find_all('li', 'item')

    for item in items :
        iCount += 1

        title = ''
        try : title = item.find('div','titWrap').find('a').text
        except : title = ''
        titleL.append(title)

        author = ''
        try : author = item.find('li','author').text
        except : author = ''
        authorL.append(author)

        publisher = ''
        try : publisher = item.find('li','publisher').text
        except : publisher = ''
        publisherL.append(publisher)

        journal = ''
        try : journal = item.find('li','journal').text
        except : journal = ''
        journalL.append(journal)

        volume = ''
        try : volume = item.find('li','volume').text
        except : volume = ''
        volumeL.append(volume)

        date = ''
        try : date = item.find('li','date').text
        except : date = ''
        dateL.append(date)

        abstract = ''
        pUrl = ''
        try : pUrl = item.find('div','titWrap').find('a')['href']
        except : pUrl = ''
        if (pUrl != ''):
            pUrl = url + pUrl
            driver.get(pUrl)
            try : driver.find_element_by_xpath('//*[@id="#pub_modalOrganPop"]').click()
            except : pass
            time.sleep(0.1)
            try : driver.find_element_by_xpath('//*[@id="#pub_modalLoginPop"]').click()
            except : pass
            try :
                driver.find_element_by_xpath('//*[@id="pub_abstract"]/div[2]/div/div[1]/div[2]/a').click()
                eachPage = driver.page_source
                ePsoup = BeautifulSoup(eachPage, 'html.parser')
                abstract = ePsoup.find('div','abstFull').find('p','article').text
            except : abstract = ''
        abstractL.append(abstract)

#Next Page
    try :
        driver.get(url)
        search_box = driver.find_element_by_xpath('//*[@id="keyword"]')
        search_box_btn = driver.find_element_by_xpath('//*[@id="bnHead"]/div[3]/div/div[1]/div[1]/a')
        search_box.send_keys(keyword)
        search_box_btn.click()
        time.sleep(2)
        nxt = driver.find_element_by_xpath(f"/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/div[3]/div[3]/a[{i+1}]")
        nxt.click()
        print(i, "page Done")
        i += 1
        time.sleep(2)
    except : break

print("====Done!====")

resultDict = dict(title = titleL,
                author = authorL,
                publisher = publisherL,
                journal = journalL,
                volume = volumeL,
                date = dateL,
                abstract = abstractL)

csv_Name = "~/Desktop/{}.csv".format(savename)
xlsx_Name = "~/Desktop/{}.xlsx".format(savename)
DB = pd.DataFrame(resultDict)
DB.to_csv(csv_Name)
DB.to_excel(xlsx_Name)