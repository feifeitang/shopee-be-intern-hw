import json
from notify import notify
import os
import pandas as pd
import random
import re
import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

ROOT_PATH = os.getcwd()


class Crawler:
    def crawler(keyword):
        CHROMEDRIVER_PATH = ROOT_PATH + \
            '/env/lib/python3.9/site-packages/chromedriver_py/chromedriver_mac64'

        keyword = keyword
        page = 5
        ecode = 'utf-8-sig'
        my_headers = {
            'authority': 'shopee.tw',
            'method': 'GET',
            'path': '/api/v1/item_detail/?item_id=1147052312&shop_id=17400098',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
            'cookie': '_ga=GA1.2.1087113924.1519696808; SPC_IA=-1; SPC_F=SDsFai6wYMRFvHCNzyBRCvFIp92UnuU3; REC_T_ID=f2be85da-1b61-11e8-a60b-d09466041854; __BWfp=c1519696822183x3c2b15d09; __utmz=88845529.1521362936.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _atrk_siteuid=HEgUlHUKcEXQZWpB; SPC_EC=-; SPC_U=-; SPC_T_ID="vBBUETICFqj4EWefxIdZzfzutfKhrgytH2wyevGxiObL3hFEfy0dpQSOM/yFzaGYQLUANrPe7QZ4hqLZotPs72MhLd8aK0qhIwD5fqDrlRs="; SPC_T_IV="IpxA2sGrOUQhMH4IaolDSA=="; cto_lwid=2fc9d64c-3cfd-4cf9-9de7-a1516b03ed79; csrftoken=EDL9jQV76T97qmB7PaTPorKtfMlU7eUO; bannerShown=true; _gac_UA-61915057-6=1.1529645767.EAIaIQobChMIwvrkw8bm2wIVkBiPCh2bZAZgEAAYASAAEgIglPD_BwE; _gid=GA1.2.1275115921.1529896103; SPC_SI=2flgu0yh38oo0v2xyzns9a2sk6rz9ou8; __utma=88845529.1087113924.1519696808.1528465088.1529902919.7; __utmc=88845529; appier_utmz=%7B%22csr%22%3A%22(direct)%22%2C%22timestamp%22%3A1529902919%7D; _atrk_sync_cookie=true; _gat=1',
            'if-none-match': "55b03-9ff4fb127aff56426f5ec9022baec594",
            'referer': 'https://shopee.tw/6-9-%F0%9F%87%B0%F0%9F%87%B7%E9%9F%93%E5%9C%8B%E9%80%A3%E7%B7%9A-omg!%E6%96%B0%E8%89%B2%E7%99%BB%E5%A0%B4%F0%9F%94%A5%E4%BA%A4%E5%8F%89%E7%BE%8E%E8%83%8CBra%E5%BD%88%E5%8A%9B%E8%83%8C%E5%BF%83-i.17400098.1147052312',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'x-api-source': 'pc',
            'x-requested-with': 'XMLHttpRequest'
        }

        def goods_detail(item_id, shop_id):
            url = 'https://shopee.tw/api/v2/item/get?itemid=' + \
                str(item_id) + '&shopid=' + str(shop_id)
            r = requests.get(url, headers=my_headers)
            st = r.text.replace("\\n", "^n")
            st = st.replace("\\t", "^t")
            st = st.replace("\\r", "^r")

            gj = json.loads(st)
            return gj

        # set config
        desired_capabilities = DesiredCapabilities.CHROME.copy()
        desired_capabilities['chrome.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'

        service = Service(executable_path=CHROMEDRIVER_PATH)

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")

        # open brower
        print('open brower')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        time.sleep(5)
        print('sleep...')

        driver.get('https://shopee.tw/search?keyword=' + keyword)
        time.sleep(10)

        print('---------- crawler start ----------')
        tStart = time.time()  # timer start

        for i in range(int(page)):

            itemid = []
            shopid = []
            name = []
            price = []
            description = []
            hashtag_list = []
            historical_sold = []
            shop_location = []

            driver.get('https://shopee.tw/search?keyword=' +
                       keyword + '&page=' + str(i))

            # scroll page
            for scroll in range(6):
                driver.execute_script('window.scrollBy(0,1000)')
                time.sleep(2)

            # get item info
            for item, thename in zip(driver.find_elements(By.XPATH, '//*[@data-sqe="link"]'), driver.find_elements(By.XPATH, '//*[@data-sqe="name"]')):
                # itemid & shopid
                getID = item.get_attribute('href')
                theitemid = int((getID[getID.rfind('.')+1:getID.rfind('?')]))
                theshopid = int(
                    getID[getID[:getID.rfind('.')].rfind('.')+1:getID.rfind('.')])
                itemid.append(theitemid)
                shopid.append(theshopid)

                # name
                getname = thename.text.split('\n')[0]
                print('fetch: '+getname)
                name.append(getname)

                # price
                thecontent = item.text
                thecontent = thecontent[(
                    thecontent.find(getname)) + len(getname):]
                thecontent = thecontent.replace('???', '000')
                thecut = thecontent.split('\n')

                if re.search('???|???|???|???|??????|????????????', thecontent):
                    if re.search('?????????', thecontent):
                        if '??????' in thecut[-3][1:]:
                            theprice = thecut[-4][1:]
                        else:
                            theprice = thecut[-3][1:]

                    else:
                        theprice = thecut[-2][1:]
                else:
                    if re.search('?????????', thecontent):
                        theprice = thecut[-2][1:]
                    else:
                        theprice = thecut[-1][1:]

                theprice = theprice.replace('$', '')
                theprice = theprice.replace(',', '')
                theprice = theprice.replace('???', '')
                theprice = theprice.replace('???', '')
                theprice = theprice.replace(' ', '')
                if ' - ' in theprice:
                    theprice = (int(theprice.split(' - ')
                                [0]) + int(theprice.split(' - ')[1]))/2
                if '-' in theprice:
                    theprice = (
                        int(theprice.split('-')[0]) + int(theprice.split('-')[1]))/2
                price.append(int(theprice))

                # get item detail info
                itemDetail = goods_detail(
                    item_id=theitemid, shop_id=theshopid)['item']

                description.append(itemDetail['description'])  # description
                hashtag_list.append(itemDetail['hashtag_list'])  # hashtag_list
                historical_sold.append(
                    itemDetail['historical_sold'])  # historical_sold
                shop_location.append(
                    itemDetail['shop_location'])  # shop_location

            dic = {
                'ItemID': itemid,
                'ShopID': shopid,
                'ItemName': name,
                'Price': price,
                'Description': description,
                'Tag': hashtag_list,
                'HistoricalSold': historical_sold,
                'ShopLocation': shop_location,
            }

            container_product = pd.DataFrame(dic)
            # scratch file
            container_product.to_csv('shopeeAPIData'+str(i+1) +
                                     '_Product.csv', encoding=ecode)

            time.sleep(random.randint(5, 10))

        container_product.to_csv(
            'product_info.csv', encoding=ecode, index=False)
        tEnd = time.time()  # timer stop
        totalTime = int(tEnd - tStart)
        minute = totalTime // 60
        second = totalTime % 60

        notify_msg = 'crawler completed, completed in ' + \
            str(minute) + ' mins ' + str(second) + ' secs'
        print(notify_msg)
        notify(notify_msg)
