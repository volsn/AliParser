from bs4 import BeautifulSoup
from selenium import webdriver
import json


def get_products(url, pages=5):
    
    # Looking for products page
    prds_link = url + '/page/offerlist.htm'
    driver = webdriver.Firefox()

    ids = set()   
    for i in range(pages):
        
        prds_page = prds_link + '?pageNum=' + str(i)
        driver.get(prds_page)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        prds = soup.find_all(attrs={'class':'offer-list-row-offer'})

        for p in prds:
            ids.add(p['data-offerid'])
    
    driver.close()
    driver.quit()
    return ids


def get_product_info(prd):
    
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
        
    
    # Finding photos
    url = 'https://detail.1688.com/pic/'
    photo_page = url + prd + '.html'
    
    driver = webdriver.Firefox()
    driver.get(photo_page)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    driver.close()
    driver.quit()
    
    info = soup.find_all(attrs={'data-img':True})
    products = []
    for s in info:
        products.append(s['data-img'])
        
    
    # Preparing a responce
    answer = {}
    answer['id'] = prd
    answer['prices'] = prices
    answer['sizes'] = sizes
    answer['products'] = products
    print(answer)
    return answer


if __name__ == '__main__':

	with open('store.txt', 'r') as f:
		store = f.read()

	products = get_products(store)
	print(products)

	responce = []
	for prd in products:
		responce.append(get_product_info(prd))

	with open('products.txt', 'w') as f:
		f.write(responce)
