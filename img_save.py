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


def img_saver(data, categories): 
    for category in tqdm(categories):
        img_folder = '/home/dhkim/Farfetch_Crawler/img/'+ category 
        if not os.path.isdir(img_folder) : # 없으면 새로 생성하는 조건문 
            os.mkdir(img_folder)
        img_url = data['img_url']
        for index, link in enumerate(img_url) :
            ID_list = data.index
            a = f'/home/dhkim/Farfetch_Crawler/img/{category}/{ID_list[index]}.jpg'
            urlretrieve(link, f'/home/dhkim/Farfetch_Crawler/img/{category}/{ID_list[index]}.jpg')
    return

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
img_saver(df,categories)