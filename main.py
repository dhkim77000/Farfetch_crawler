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

def url_filter(index, url,conditons, ID_list):
    if(index ==0):
        if(conditons[0] in url):  #상품 이미지만 추출
            if('preview' in url) :  #프리뷰 있으면 사이즈 키워서 리턴
                url = re.sub('100/output=preview','',url) + '600'
                return url
            else: return url #없으면 그냥 리턴
        else: return None  #유효하지 않은 링크
    else:
        if(ID_list[index-1] in url): return None  #이미 중복된 상품 이미지
        else:
            if('preview' in url) :                         #URL 필터 후 추출
                url = re.sub('100/output=preview','',url) + '600' 
                return url
            else: return url
            
def selenium_scroll_option():
    SCROLL_PAUSE_SEC = 1
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)
        new_height = driver.execute_script("return document.body.scrollHeight")
  
        if new_height == last_height:
            return 1
        last_height = new_height

def Farfetch_crawler(url,category,driver,chrome_options):
    
    driver.set_window_size(1000, 1200)
    driver.get(url)
    
    action = ActionChains(driver)
    selenium_scroll_option()
    item_name = []
    ID_list = []
    img_urls =[]
    item_urls=[]
    brands = []
    price_list = []
    
    #products = driver.find_elements_by_tag_name('img')
    products = driver.find_elements(by = By.TAG_NAME, value = 'img')
    products_num = 0
    for product in products:
        if(product.get_attribute('data-component')=='ProductCardImagePrimary'): products_num+=1
    
    
    img_xpath_f = '//*[@id="slice-container"]/div[3]/div/div[2]/div/div[1]/ul/div['
    img_xpath_b = ']/a/div[1]/div/img'

    item_xpath_f = '//*[@id="slice-container"]/div[3]/div[2]/div[2]/div/div[1]/ul/div['
    item_xpath_b =']/a'
    name_xpath_f = '//*[@id="slice-container"]/div[3]/div/div[2]/div/div[1]/ul/div['
    name_xpath_b = ']/a/div[2]/div[1]/p[2]'
    brand_xpath_f = '//*[@id="slice-container"]/div[3]/div/div[2]/div/div[1]/ul/div['
    brand_xpath_b = "]/a/div[2]/div[1]/p[1]"
    price_xpath_f = '//*[@id="slice-container"]/div[3]/div/div[2]/div/div[1]/ul/div['
    price_xpath_b = "]/a/div[2]/div[2]/p"
    
    action = ActionChains(driver)
    
    for i in range(1,products_num+1): 
        try:
            #product = driver.find_element_by_xpath(img_xpath_f+str(i)+img_xpath_b)
            product = driver.find_element(by = By.XPATH, value = img_xpath_f+str(i)+img_xpath_b)
        except NoSuchElementException:
            continue
        
        #brand = driver.find_element_by_xpath(brand_xpath_f+str(i)+brand_xpath_b).get_attribute("textContent")
        brand = driver.find_element(by = By.XPATH, value = brand_xpath_f+str(i)+brand_xpath_b).get_attribute("textContent")

        #price = driver.find_element_by_xpath(price_xpath_f+str(i)+price_xpath_b).get_attribute("textContent")
        price = driver.find_element(by = By.XPATH, value = price_xpath_f+str(i)+price_xpath_b).get_attribute("textContent")

        #item_url = driver.find_element_by_xpath(item_xpath_f+str(i)+item_xpath_b).get_attribute('href')
        item_url = driver.find_element(by = By.XPATH, value = item_xpath_f+str(i)+item_xpath_b).get_attribute('href')
        img_url = product.get_attribute('src')
        
        img_urls.append(img_url)
        item_urls.append(item_url)
        brands.append(brand)
        price_list.append(price)
        #item = driver.find_element_by_xpath(name_xpath_f+str(i)+name_xpath_b).get_attribute("textContent")
        item = driver.find_element(by = By.XPATH, value = name_xpath_f+str(i)+name_xpath_b).get_attribute("textContent")
        ID = re.findall('_(\d.*?)_',img_url)[0]
        
        item_name.append(item)
        ID_list.append(ID)
       
    


   
    category_list = [category] * len(brands)

        
    img_folder = './img'
    data_df = pd.DataFrame({'Brand' : brands,
                            'Item': item_name,
                       'img_url': img_urls,
                        'item_url' :item_urls,
                        'Category':category_list,
                       'Price':price_list},
                           index = ID_list)
    
    
    return data_df

def Farfetch_data(Category ,driver= None, chrome_options= None):
    print("-------------------crawling data from Farfetch-------------------")
    base_url = 'https://www.farfetch.com/uk/shopping/men/clothing-2/items.aspx?view=90&rootCategory=Men&category='
    url_f = "https://www.farfetch.com/uk/shopping/men/clothing-2/items.aspx?page="
    url_b = "&view=90&rootCategory=Men&category="
    category_dic = {'jeans':'136337',
                    'knitwear' : '136396|136399',
                  'sweatshirts-and-t-shirts':'136398|136397|136333|136332',
                   'coats':'136412|136416|139363|136413|136418|136419',
                   'jackets':'136402|136410|136340',
                    'leather-and-fur':'136400|136405|136414',
                    'denim':'136403',
                    'trousers':'136338|136441',
                    'shirts':'136331',
                   'outerwear':'136468|136404|136401|136403|136406|136407|136409|136408|136411|136417'
                   }
    
    for i,category in tqdm(enumerate(Category)):
        print('\n-------------------'+category+'-------------------')
        category_url = category_dic.get(category)
        url = base_url+ category_url
        page = page_finder(url, driver, chrome_options)
        if i == 0:
            for j, p in enumerate(range(1, page+1)):
                print('\n-------------------page{}-------------------'.format(p))
                if(p == 1):
                    url = base_url+ category_url
                else:
                    url = url_f+str(p)+url_b+category_url
                if(j==0 and p == 1):
                    df = Farfetch_crawler(url,category, driver, chrome_options)
                else:
                    temp = Farfetch_crawler(url, category, driver, chrome_options)
                    df = pd.concat([df, temp])

                
        else:
            for j, p in tqdm(enumerate(range(1, page+1))):
                print('\n-------------page{}---------------'.format(p))
                if(p == 1):
                    url = base_url+ category_url
                else:
                    url = url_f+str(p)+url_b+category_url
                temp = Farfetch_crawler(url, category, driver, chrome_options)
                df = pd.concat([df, temp])
        df.to_csv('/home/dhkim/Farfetch_Crawler/data/data.csv')
    return df

def page_finder(url, driver,chrome_options):
   
    driver.set_window_size(1000, 1200)
    driver.get(url)
    #pdb.set_trace()
    action = ActionChains(driver)
    selenium_scroll_option()
    #page = driver.find_element_by_xpath('//*[@id="slice-container"]/div[3]/div/div[2]/div/div[2]/div/div[2]').text
    page = driver.find_element(by = By.XPATH, value = '//*[@id="slice-container"]/div[3]/div/div[2]/div/div[2]/div/div[2]').text

    page = int(page.split()[2])
    return page

def Farfetch_Item_attributes(df=None, driver= None, chrome_options= None):
    
    df['Attributes'] = None
    df['Composition'] = None
    driver.set_window_size(1000, 1200)
    
    
    attributes_list_xpath = '//*[@id="panelInner-0"]/div/div[1]/div[3]/ul'
    attribute_xpath_f ='//*[@id="panelInner-0"]/div/div[1]/div[3]/ul/li['
    compostion_xpath ='//*[@id="panelInner-0"]/div/div[2]/div/div[1]/p'
    for i in range(len(df)):
        
        url = df.iloc[i].loc['item_url']
        driver.get(url)
        attributes = driver.find_element_by_xpath(attributes_list_xpath)
        attributes_len = len(attributes.find_elements_by_tag_name("li"))
        attributes =[]
        for j in range(1, attributes_len+1):
            attribute = driver.find_element_by_xpath(attribute_xpath_f+str(j)+']').get_attribute("textContent")
          
            attributes.append(attribute)
        compostion = driver.find_element_by_xpath(compostion_xpath).get_attribute("textContent")
        df['Attributes'][i] = attributes
        df['Composition'][i] = compostion
    return df
        
def img_saver(data, categories): 
    for category in categories:
        img_folder = './img/'+ category 
        print(img_folder)
        if not os.path.isdir(img_folder) : # 없으면 새로 생성하는 조건문 
            os.mkdir(img_folder)
        img_url = data['img_url']
        for index, link in enumerate(img_url) :
            ID_list = data.index
            a = f'./img/{category}/{ID_list[index]}.jpg'
            urlretrieve(link, f'./img/{category}/{ID_list[index]}.jpg')
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


#1차 데이터 크롤링 
df = Farfetch_data(categories, driver, chrome_options)
df.to_csv('/home/dhkim/Farfetch_Crawler/data')
#이미지 저장d
#img_saver(df,categories)
#2차 데이터 크롤링
#chrome_options = webdriver.ChromeOptions()
#driver = webdriver.Chrome(chrome_path,options=chrome_options)
#df = Farfetch_Item_attributes(knit[:5], driver, chrome_options)