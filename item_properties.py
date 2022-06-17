
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import time
import urllib.request
import os
import pandas as pd
from urllib.parse import quote_plus          
from bs4 import BeautifulSoup as bs 
from selenium import webdriver
import time
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
import re
import os 
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import pdb
from selenium.webdriver.common.by import By

def Farfetch_Item_attributes(df=None, driver= None, chrome_options= None):
    
    df['Attributes'] = None
    df['Composition'] = None
    driver.set_window_size(1000, 1200)
    


    
    
  
    for i in tqdm(range(len(df))):
        compostion_xpath ='//*[@id="panelInner-0"]/div/div[2]/div/div[1]/p'
        attributes_list_xpath = '//*[@id="panelInner-0"]/div/div[1]/div[2]/ul'
        attribute_xpath_f ='//*[@id="panelInner-0"]/div/div[1]/div[2]/ul/li['

        url = df.iloc[i].loc['item_url']
        driver.get(url)
        try:
            attributes = driver.find_element(by = By.XPATH, value = attributes_list_xpath)
            attributes_len = len(attributes.find_elements(by = By.TAG_NAME, value = "li"))
        except NoSuchElementException as e:
            try:
                attributes_list_xpath = '//*[@id="panelInner-0"]/div/div[1]/div[3]/ul'
                attribute_xpath_f ='//*[@id="panelInner-0"]/div/div[1]/div[3]/ul/li['

                attributes = driver.find_element(by = By.XPATH, value = attributes_list_xpath)
                attributes_len = len(attributes.find_elements(by = By.TAG_NAME, value = "li"))

            except NoSuchElementException as e:

                attributes_len = 0

        attributes =[]
        for j in range(1, attributes_len+1):
            attribute = driver.find_element(by = By.XPATH, value = attribute_xpath_f+str(j)+']').get_attribute("textContent")
            attributes.append(attribute)

        try:
            compostion = driver.find_element(by = By.XPATH, value = compostion_xpath).get_attribute("textContent")
        except NoSuchElementException as e:
            try:
                compostion_xpath ='//*[@id="panelInner-0"]/div/div[3]/div/div[1]/p'
                compostion = driver.find_element(by = By.XPATH, value = compostion_xpath).get_attribute("textContent")
            except NoSuchElementException as e:
                 compostion = None


        df['Attributes'][i] = attributes
        df['Composition'][i] = compostion

        if (i % 500 == 0):
            df.to_csv('/home/dhkim/Farfetch_Crawler/data/data.csv')
    return df

display = Display(visible = 0, size = (1920,1000))
display.start()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")

chrome_path = "/home/dhkim/chromedriver"
categories = ['jeans','knitwear','sweatshirts-and-t-shirts','coats','jackets',
                       'leather-and-fur','denim','trousers','shirts','outerwear']
driver = webdriver.Chrome(chrome_path,options=chrome_options)


#이미지 저장
df = pd.read_csv('/home/dhkim/Farfetch_Crawler/data/data.csv')
df = Farfetch_Item_attributes(df, driver, chrome_options)
