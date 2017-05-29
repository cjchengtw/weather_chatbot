# -*- coding: utf-8 -*-
# /usr/bin/python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql
import database
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

# available since 2.4.0
from selenium.webdriver.support.ui import WebDriverWait

# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC

# 建立 driver
driver = webdriver.Firefox()

# 去 google
driver.get("http://www.google.com")

# 顯示標題
print(driver.title)

# 找到搜尋框
inputElement = driver.find_element_by_name("q")

# 搜尋框輸入字
inputElement.send_keys("cheese!")

# 提交
inputElement.submit()

try:
    # 直到標題有 cheese
    WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

    # 顯示標題，可看到 cheese
    print(driver.title)
except TimeoutException:
    print('time out')
finally:
    driver.quit()




def get_soup(url):
    res = requests.get(url)  # 從網址存網站頁面
    res.encoding = 'utf-8'  # 修正requests和bs4自行猜測的編碼為utf-8
    soup = BeautifulSoup(res.text, "lxml")  # 存成文字內容
    return soup
def weather_crawler():
    url = "http://www.cwb.gov.tw/V7/observe/24real/Data/46692.htm"
    soup = get_soup(url)
    count = 0
    for i in soup.table.tr.next_siblings:
        if i == '\n':
            pass
        else:
            time = str(i).split("</th>")[0].split(">")[2]
            year = datetime.now().year
            time = datetime.strptime('{} {}'.format(year,time), '%Y %m/%d %H:%M')
            with database.Database() as db:
                sql = """SELECT * FROM  weather"""
                db.execute(sql)
                if db.fetchone()[0] > time:
                    print("時間： {}".format(time))  # ex: 2017-05-29 13:30:00
                    tpr = str(i).split("</td>")[0].split(">")[4]  # 攝氏溫度 ex:29.5
                    print("攝氏溫度： {}".format(tpr))
                    wet = str(i).split("</td>")[1].split(">")[1]
                    print("相對溼度： {}".format(wet))  # 相對溼度 ex:85.1
                    count += 1
                    sql = """INSERT INTO weather (time,tpr,wet,uv) VALUES (%s,%s,%s,%s)"""
                    db.execute(sql, (time, tpr, wet, None))





    print(count)
def station_crawler():
    url = "http://www.cwb.gov.tw/V7/observe/real/ObsN.htm"
    soup = get_soup(url)
    print(soup.find("table",id=63).findAll("a"))
    for i in soup.find("table",id=63).findAll("a"):
        name = i.get_text()
        #print(i.get_text()) #ex: 鞍部
        station_id = i['href'].split(".")[0]
        #print(i['href'].split(".")[0]) #ex:46691
        #url = "http://www.cwb.gov.tw/V7/observe/real/{}.htm#ui-tabs-3".format(station_id)
        url = "http://www.cwb.gov.tw/V7/google/46691_map.htm"
        soup = get_soup(url)
        print(str(soup.get_text).split("<"))
        with database.Database() as db:
            sql = """SELECT * FROM  station"""
            db.execute(sql)
            #sql = """INSERT INTO stationi (time,tpr,wet,uv) VALUES (%s,%s,%s,%s)"""
            #db.execute(sql, (None, name,station_id, None))
#crawler()



station_crawler()












