from lxml import html
import traceback
from fake_useragent import UserAgent
from requests_html import HTMLSession
import random
import requests
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning


from requests_html import AsyncHTMLSession
import asyncio
import pyppeteer
   
async def scrape(catalog_number):

	proxies = [{'http':'193.9.158.30:8085','https':'193.9.158.30:8085'},{'http':'46.161.62.121:8085','https':'46.161.62.121:8085'}]

	# Sproxies = []

	ua = UserAgent()

	scraper_loop=asyncio.new_event_loop()
	asyncio.set_event_loop(scraper_loop)
	session = AsyncHTMLSession()
	
	browser = await pyppeteer.launch({ 
        'ignoreHTTPSErrors':True, 
        'headless':True, 
        'handleSIGINT':False, 
        'handleSIGTERM':False, 
        'handleSIGHUP':False
    })
	session._browser = browser

	headers = {'User-Agent':ua.random,'Host':'google.com','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7','Cache-Control': 'no-cache','Connection': 'keep-alive','Upgrade-Insecure-Requests':'1'}

	# catalog_number = input('Введите каталожный номер:')

	print('Пожалуйста, ожидайте...')

	try:

		warnings.simplefilter('ignore')

		if proxies:

			proxy = random.choice(proxies)

			r = await session.get('https://www.sigmaaldrich.com/catalog/product/aldrich/'+catalog_number+'?lang=en&region=US',headers=headers,verify=False,proxies={'http': 'http://'+proxy['http']},timeout=20)

		else:

			r = await session.get('https://www.sigmaaldrich.com/catalog/product/aldrich/'+catalog_number+'?lang=en&region=US',headers=headers,verify=False,timeout=20)


		await r.html.arender(timeout=10)

		js = r.html.html

		tree = html.fromstring(js)

		price = tree.xpath('//td[@class="price"]/p/text()')

		weight = tree.xpath('//td[@class="packSize"]/text()')

		sku = tree.xpath('//td[@class="sku"]/p/text()')


		if (price   and sku and weight):

			print ('{0:15} | {1:15} | {2:15}'.format('SKU-Pack Size','Pack Size','Price (EUR)'))
			print ('{0:15} | {1:15} | {2:15}'.format(sku[0],weight[0],price[0]))
			return ('{0:15} | {1:15} | {2:15}\n{3:15} | {4:15} | {5:15}'.format('SKU-Pack Size','Pack Size','Price (EUR)', sku[0],weight[0],price[0]))

		else:

			print('Нет информации для этого каталожного номера...')

	except Exception as e:

		print(e)

		# continue


# if __name__ == "__main__":
# 	asyncio.run(main())
