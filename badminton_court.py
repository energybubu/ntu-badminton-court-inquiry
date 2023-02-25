
'''動態網頁擷取'''
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import time 
import sys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

driver = webdriver.Chrome("/Users/bubuenergy/Desktop/chromedriver")
class Page:
    def __init__(self, url):
        self.url = url
        driver.get(url)

    def pass_alert(self):
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    def click_button(self, selector="id", info=""):
        button = driver.find_element(selector, info)
        button.click()
    def enter_text(self, selector, info, text):
        element = driver.find_element(selector, info)
        element.send_keys(text)
url = "https://rent.pe.ntu.edu.tw/member/?U=login"

new_page = Page(url)
new_page.click_button("css selector", "a.LoginBtn")
new_page.enter_text("id", 'ContentPlaceHolder1_UsernameTextBox', sys.argv[1])
new_page.enter_text("id", 'ContentPlaceHolder1_PasswordTextBox', sys.argv[2])
new_page.click_button("id", "ContentPlaceHolder1_SubmitButton")
new_page.pass_alert()
new_page.click_button("xpath", '//a[@href="'+"/order/?Add=A:2"+'"]')
driver.execute_script("window.scrollTo(0, 200)")

DATE = {0:"日", 1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六"}

courts = driver.find_elements("class name", "VSMenu")
soup_col = []
for court in tqdm(courts):
    suc = 0
    while suc!=1:
        try:
            court.click()
            time.sleep(0.5)
            soup_col.append(BS(driver.page_source, "lxml"))
            suc = 1
        except:
            print("Please scroll your screen to see '一面, 二面.....'")
            pass

import os 
if not os.path.isdir("./court_information"): os.mkdir("./court_information")
if not os.path.isdir("./summary"): os.mkdir("./summary")
court_path = "./court_information"
summary_path = "./summary"


import numpy as np
online = np.zeros([14, 21])
offline = np.zeros([14, 21])
dates = []
index = [f"{i}-{i+1}" for i in range(8, 22)]

'''靜態網頁擷取'''
for numm, soup in enumerate(soup_col):
    table = soup.find("div", {"class":"SContents"})

    with open(os.path.join(court_path, f"court{numm+1}.txt"), "w") as file:
        file.write(f"這是第{numm+1}面\n")
        
        days = table.find_all('div', {"class":"D"})
        '''可以網上租借的時段'''
        file.write("可以網上租借\n")
        for num, day in enumerate(days):
            availables = day.find_all('a', {"class":"S Hover"})
            if numm==0: dates.append(f"{day['d']} ({DATE[num%7]})")
            if availables:
                file.write(str(day['d'])+" "+str(DATE[num%7])+"\n")
            for available in availables:
                file.write(str(available['title'])+"\n")
                online[int(available['title'].split(' ')[0])-8][num] += 1

        '''可以現場租借的時段'''
        file.write("請至現場租借\n")
        for num, day in enumerate(days):
            all_possible = day.find_all('div', {'s':'N'})
            print_day = 0
            for possible in all_possible:
                if len(possible.contents)>=2:
                    if possible.contents[1]['class'][1] == "N4":
                        if print_day==0:
                            file.write(str(day['d'])+" "+str(DATE[num%7])+"\n")
                            print_day = 1
                        file.write(possible.contents[0].get_text()+"\n")
                        offline[int(possible.contents[0].get_text().split()[0])-8][num] += 1

import pandas as pd
online_pd = pd.DataFrame(online, columns=dates, index=index)
online_pd = online_pd.loc[:, (online_pd != 0).any(axis=0)]
offline_pd = pd.DataFrame(offline, columns=dates, index=index)
offline_pd = offline_pd.loc[:, (offline_pd != 0).any(axis=0)]
print("="*10, "可線上租借剩餘場數", "="*10)
print(online_pd)
print("="*10, "可現場租借剩餘場數", "="*10)
print(offline_pd)
online_pd.to_csv(os.path.join(summary_path, "可線上租借剩餘場數.csv"))
offline_pd.to_csv(os.path.join(summary_path, "可現場租借剩餘場數.csv"))
