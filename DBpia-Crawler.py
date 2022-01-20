import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv
import datetime
import time
from time import sleep

keyword = "고고학"
page = 1
url = "https://www.dbpia.co.kr/"

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get(url)

search_box = driver.find_element_by_xpath('//*[@id="keyword"]')
search_box_btn = driver.find_element_by_xpath('//*[@id="bnHead"]/div[3]/div/div[1]/div[1]/a')
search_box.send_keys(keyword)
search_box_btn.click()

wCount = 0
while(True):
    time.sleep(1)
    try:
        more = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='contents']/div[2]/div[3]/div[3]/div[3]/div/a")))
        driver.execute_script("arguments[0].click()",more)
    except:
        print('retry')
        break
    wCount += 1
    print(" + page [{}]".format(wCount))


items_source = driver.page_source
soup = BeautifulSoup(items_source, 'html.parser')

items = soup.find('div','searchListArea').find('div','listBody').find('ul').find_all('li', 'item')

# 제목, 저자, 학회, 학보, 볼륨, 발표일, 초록
titleL = []
authorL = []
publisherL = []
journalL = []
volumeL = []
dateL = []
abstractL = []
tLen = len(items)
print("start parsing")

iCount = 0
for item in items :
    iCount += 1
    if iCount % 20 == 0:
        print(" parsing.. [{}/{}]".format(iCount, tLen))

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
        
#여기 아래 부분이 문제인듯 씨발
        try :
            driver.find_element_by_xpath('//*[@id="pub_abstract"]/div[2]/div/div[1]/div[2]/a').click()
            eachPage = driver.page_source
            ePsoup = BeautifulSoup(eachPage, 'html.parser')
            abstract = ePsoup.find('div','abstFull').find('p','article').text
        except : abstract = ''
    abstractL.append(abstract)

print("date to .csv file")

resultDict = dict(title = titleL,
              author = authorL,
              publisher = publisherL,
              journal = journalL,
              volume = volumeL,
              date = dateL,
              abstract = abstractL)

csv_Name = "~/Desktop/{}.csv".format(keyword)
xlsx_Name = "~/Desktop/{}.xlsx".format(keyword)
DB = pd.DataFrame(resultDict)
DB.to_csv(csv_Name)
DB.to_excel(xlsx_Name)