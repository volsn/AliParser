from bs4 import BeautifulSoup
from selenium import webdriver
import json
import urllib.request
from fpdf import FPDF

PATH_TO_GECKODRIVER = r'C:\Users\Kolia\Desktop\parser\geckodriver.exe'

def get_products(url, pages=1):
    # Looking for products page
    prds_link = url + '/page/offerlist.htm'
    driver = webdriver.Firefox(executable_path=PATH_TO_GECKODRIVER)

    ids = set()
    for i in range(pages):

        prds_page = prds_link + '?pageNum=' + str(i)
        driver.get(prds_page)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        prds = soup.find_all(attrs={'class': 'offer-list-row-offer'})

        for p in prds:
            ids.add(p['data-offerid'])

    driver.close()
    driver.quit()
    return ids


def get_product_info(prd, percent=0.17):
    url = 'https://detail.1688.com/offer/'
    prd_page = url + prd + '.html'

    driver = webdriver.Firefox()
    driver.get(prd_page)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    driver.close()
    driver.quit()

    # Getting prices and quantities
    info = soup.find_all(attrs={'data-range': True})
    prices = []
    for s in info:
        prices.append(json.loads(s['data-range']))

    # Getting available sizes
    info = soup.find_all(attrs={'data-sku-config': True})
    sizes = []
    for s in info:
        sizes.append(json.loads(s['data-sku-config']))

    # Finding product specifications
    info = soup.find_all(attrs={'class': 'unit-detail-spec-operator'})
    specs = []
    for p in info:
        specs.append(json.loads(p['data-imgs'])['original'])

    # Finding photos
    url = 'https://detail.1688.com/pic/'
    photo_page = url + prd + '.html'

    driver = webdriver.Firefox()
    driver.get(photo_page)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    driver.close()
    driver.quit()

    info = soup.find_all(attrs={'data-img': True})
    photos = []
    for s in info:
        photos.append(s['data-img'])

    answer = {}
    answer['id'] = prd
    answer['prices'] = prices
    answer['sizes'] = sizes
    answer['photos'] = photos
    answer['specs'] = specs

    # Preparing answer for being saved in SQL

    ranges = []
    for r in answer['prices']:
        range_ = ''
        if r['begin'] == '':
            range_ += 'менее '
        else:
            range_ += r['begin']

        if r['end'] == '':
            range_ += 'и более'
        else:
            range_ += '-' + r['end']

        ranges.append(range_ + ' - ' + str(round(float(r['price']) * (1 + percent))) + ' Y')
    answer['prices'] = ranges

    sizes = []
    for s in answer['sizes']:
        sizes.append(s['skuName'])

    answer['sizes'] = sizes

    return answer
