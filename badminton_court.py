
'''動態網頁擷取'''
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import time 
import os, sys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tqdm import tqdm
import requests
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Page:

    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
        self.driver.get(url)

    def pass_alert(self):
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
    def click_button(self, selector="id", info=""):
        button = self.driver.find_element(selector, info)
        button.click()
    def enter_text(self, selector, info, text):
        element = self.driver.find_element(selector, info)
        element.send_keys(text)
def update_csvs(username=os.environ['USER'], password=os.environ['PASSWORD']):

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920, 1080")
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)

    # opts = webdriver.ChromeOptions()
    # opts.add_argument('--headless')
    # driver = webdriver.Chrome(options=opts)
    url = "https://rent.pe.ntu.edu.tw/member/?U=login"
    new_page = Page(url, driver)
    new_page.click_button("css selector", "a.LoginBtn")
    new_page.enter_text("id", 'ContentPlaceHolder1_UsernameTextBox', username)
    new_page.enter_text("id", 'ContentPlaceHolder1_PasswordTextBox', password)
    new_page.click_button("id", "ContentPlaceHolder1_SubmitButton")
    new_page.pass_alert()
    new_page.click_button("xpath", '//a[@href="'+"/order/?Add=A:2"+'"]')

    # js_code = "arguments[0].scrollIntoView();"
    # element = driver.find_element(By.CLASS_NAME, "SubVenuesMenu")
    # driver.execute_script(js_code, element)

    # driver.execute_script("window.scrollTo(0, 600)")

    DATE = {0:"日", 1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六"}

    courts = driver.find_elements("class name", "VSMenu")
    soup_col = []
    cur_scroll = 0
    for court in tqdm(courts):
        suc = 0
        while suc!=1:
            try:
                court.click()
                time.sleep(0.5)
                soup_col.append(BS(driver.page_source, "lxml"))
                suc = 1
            except:
                driver.execute_script(f"window.scrollTo(0, {cur_scroll})")
                print("cur scroll:", cur_scroll)
                pass
            cur_scroll+=50
            if cur_scroll>1080: cur_scroll=0

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
                # if numm==0: dates.append(f"{day['d']} ({DATE[num%7]})")
                if numm==0: dates.append(f"{day['d']}")
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

    online_pd = pd.DataFrame(online, columns=dates, index=index, dtype='int64')
    online_pd = online_pd.loc[:, (online_pd != 0).any(axis=0)]
    offline_pd = pd.DataFrame(offline, columns=dates, index=index, dtype='int64')
    offline_pd = offline_pd.loc[:, (offline_pd != 0).any(axis=0)]
    online_pd.to_csv(os.path.join(summary_path, "可線上租借剩餘場數.csv"))
    offline_pd.to_csv(os.path.join(summary_path, "可現場租借剩餘場數.csv"))

    ret_msg = f"{'='*10}\n可線上租借剩餘場數\n{'='*10}\n{online_pd}\n{'='*10}可現場租借剩餘場數{'='*10}\n{offline_pd}"
def Query_all():
    update_csvs()
    online_pd = pd.read_csv("./summary/可線上租借剩餘場數.csv")
    offline_pd = pd.read_csv("./summary/可現場租借剩餘場數.csv")
    week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]

    ret_col = []
    ret_col.append("=== 可線上租借剩餘場數 ===\n")
    for column in online_pd.columns.values[1:]:
        ret = f"{column} "
        weekday = datetime.strptime(column, '%Y-%m-%d').weekday()
        ret += f"{week_list[weekday]}\n"
        for date, court in zip(online_pd['Unnamed: 0'].values, online_pd[column].values):
            ret += date.ljust(8)
            ret += str(court).rjust(4)
            ret += '\n'
        ret_col.append(ret)
    ret_col.append("=== 可現場租借剩餘場數 ===\n")
    for column in offline_pd.columns.values[1:]:
        ret = f"{column} "
        weekday = datetime.strptime(column, '%Y-%m-%d').weekday()
        ret += f"{week_list[weekday]}\n"
        for date, court in zip(offline_pd['Unnamed: 0'].values, offline_pd[column].values):
            ret += date.ljust(8)
            ret += str(court).rjust(4)
            ret += '\n'
        ret_col.append(ret)
    return ret_col
def Query(username=os.environ['USER'], password=os.environ['PASSWORD'], assign_date="2023-04-11"):
    update_csvs(username=os.environ['USER'], password=os.environ['PASSWORD'])
    try:
        online_pd = pd.read_csv("./summary/可線上租借剩餘場數.csv")
        offline_pd = pd.read_csv("./summary/可現場租借剩餘場數.csv")
        ret = ""
        for date, courts in zip(online_pd['Unnamed: 0'].values, online_pd[assign_date].values):
            ret += date.ljust(8)
            ret += str(courts).rjust(4)
            ret += '\n'
        return ret
    except:
        ret = ""
        for date, courts in zip(offline_pd['Unnamed: 0'].values, offline_pd[assign_date].values):
            ret += date.ljust(8)
            ret += str(courts).rjust(4)
            ret += '\n'
        return ret
        

if __name__ == "__main__":
    msg = Query(username=os.environ['USER'], password=os.environ['PASSWORD'], assign_date="2023-04-11")
    msg = Query_all()
    print(msg)